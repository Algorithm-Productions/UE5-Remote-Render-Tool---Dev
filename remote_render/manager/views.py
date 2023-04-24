import logging
import platform
import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from flask import request, render_template, send_from_directory, make_response, redirect, url_for

from remote_render.manager.ManagerUtils import buildLog, buildArchive, new_request_trigger, getLogsToDisplay
from remote_render.util.ManagerFlaskApp import abstract_read_one, abstract_update, abstract_delete_all, \
    abstract_delete, abstract_read_all
from remote_render.util.datatypes import RenderArchive, RenderRequest, RenderLog
from remote_render import app

LOGGER = logging.getLogger(__name__)
MANAGER_NAME = platform.node()
MODULE_PATH = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(MODULE_PATH, '../../.env'))
API_EXT = "/api"
ARCHIVE_API_EXT = "/archives"
LOG_API_EXT = "/logs"
DEFAULT_WORKER = os.getenv("DEFAULT_WORKER")


#################
# Route Section #
#################

@app.route('/')
def index_page():
    return render_template('landing.html', logs=getLogsToDisplay())


@app.route('/queue/')
def queue_page():
    reqs = RenderRequest.read_all()
    if not reqs:
        return render_template('error.html', errorText="No Ongoing Renders", title="Render Queue",
                               page_passer="queue_page")

    jsons = [req.to_dict() for req in reqs]

    return render_template('queue.html', requests=jsons)


@app.route('/archive/')
def archive_page():
    reqs = RenderArchive.read_all()
    if not reqs:
        return render_template('error.html', errorText="No Archived Renders", title="Render Archive",
                               page_passer="archive_page")

    jsons = [req.to_dict() for req in reqs]

    return render_template('archive.html', requests=jsons)


@app.route('/archive/<uuid>')
def archive_entry(uuid):
    rr = RenderArchive.read(uuid)
    return render_template('archive_entry.html', entry=rr.to_dict(), uuid=uuid)


@app.route('/logs/')
def logs_page():
    reqs = RenderLog.read_all()
    if not reqs:
        return render_template('error.html', errorText="No logs", title="Application Logs",
                               page_passer="logs_page")

    jsons = [req.to_dict() for req in reqs]

    return render_template('logs.html', requests=jsons)


@app.route('/logs/<uuid>')
def logs_entry(uuid):
    log = RenderLog.read(uuid)
    if not log:
        return render_template('error.html', errorText="Log not Found", title="Application Logs",
                               page_passer="logs_page")

    return render_template('logs_entry.html', entry=log.to_dict(), uuid=uuid)


@app.route("/set")
@app.route("/set/<theme>")
def set_theme(theme="lightmode-index_page"):
    args = theme.split("-")
    if len(args) == 3:
        res = make_response(redirect(url_for(args[1], uuid=args[2])))
    else:
        res = make_response(redirect(url_for(args[1])))

    expiration = (datetime.now() + timedelta(days=30))

    res.set_cookie("theme", args[0], expires=expiration)
    return res


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.png', mimetype='image/vnd.microsoft.icon')


#######################
# General API Section #
#######################

@app.post('{}/ping'.format(API_EXT))
def ping():
    return {'response': "Pong"}


@app.post('{}/worker/post/<worker_name>'.format(API_EXT))
def add_worker(worker_name):
    buildLog('', ['', datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                  'Adding {} From App'.format(worker_name),
                  'Adding {} From App'.format(worker_name), "INFO"]).save_self()
    return {'response': app.add_worker(worker_name)}


@app.get('{}/worker/get'.format(API_EXT))
def get_workers():
    return {'results': app.WORKERS}


@app.delete('{}/worker/delete/<worker_name>'.format(API_EXT))
def remove_worker(worker_name):
    buildLog('', ['', datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                  'Removing {} From App'.format(worker_name),
                  'Removing {} From App'.format(worker_name), "WARN"]).save_self()
    return {'response': app.remove_worker(worker_name)}


#####################
# Queue API Section #
#####################


@app.post('{}/post'.format(API_EXT))
def create_request():
    data = request.get_json(force=True)
    req = RenderRequest.from_dict(data)
    req.save_self()
    new_request_trigger(req, DEFAULT_WORKER, LOGGER)

    buildLog(req.uuid, [req.uuid, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                        'Creating Request {} on DB'.format(req.uuid),
                        'Creating Request {} on DB'.format(req.uuid), "INFO"]).save_self()

    return req.to_dict()


@app.get('{}/get'.format(API_EXT))
def get_all_requests():
    return abstract_read_all(RenderRequest.read_all())


@app.get('{}/get/<uuid>'.format(API_EXT))
def get_request(uuid):
    return abstract_read_one(RenderRequest.read(uuid))


@app.put('{}/put/<uuid>'.format(API_EXT))
def update_request(uuid):
    progress, time_estimate, status = request.data.decode('utf-8').split(';')
    return abstract_update(RenderRequest.read(uuid), "", {"progress": int(float(progress)),
                                                          "time_estimate": time_estimate,
                                                          "status": status})


@app.delete('{}/delete/'.format(API_EXT))
def delete_all_requests():
    return abstract_delete_all("Requests", True)


@app.delete('{}/delete/<uuid>'.format(API_EXT))
def delete_request(uuid):
    return abstract_delete(uuid, "Request", True)


#######################
# Archive API Section #
#######################


@app.post('{}{}/post'.format(API_EXT, ARCHIVE_API_EXT))
def create_archive():
    content = request.data.decode('utf-8')

    args = content.split(";")
    renderRequest = RenderRequest.read(args[0])
    if (not renderRequest) or len(args) != 7:
        return {}

    renderArchive = buildArchive(args[0], renderRequest, args)
    renderArchive.save_self()

    buildLog(args[0], [args[0], datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                       'Archiving Request {}'.format(args[0]),
                       'Archiving Request {}'.format(args[0]), "INFO"]).save_self()

    return renderArchive.to_dict()


@app.get('{}{}/get'.format(API_EXT, ARCHIVE_API_EXT))
def get_all_archives():
    return abstract_read_all(RenderArchive.read_all())


@app.get('{}{}/get/<uuid>'.format(API_EXT, ARCHIVE_API_EXT))
def get_archive(uuid):
    return abstract_read_one(RenderArchive.read(uuid))


@app.put('{}{}/<uuid>'.format(API_EXT, ARCHIVE_API_EXT))
def update_archive(uuid):
    return abstract_update(RenderArchive.read(uuid), request.data.decode('utf-8'))


@app.delete('{}{}/delete'.format(API_EXT, ARCHIVE_API_EXT))
def delete_all_archives():
    return abstract_delete_all("Archives", True)


@app.delete('{}{}/delete/<uuid>'.format(API_EXT, ARCHIVE_API_EXT))
def delete_archive(uuid):
    return abstract_delete(uuid, "Archive", True)


####################
# Logs API Section #
####################


@app.post('{}{}/post'.format(API_EXT, LOG_API_EXT))
def create_log():
    content = request.data.decode('utf-8')

    args = content.split(";")
    if len(args) != 5:
        return {}

    renderLog = buildLog(args[0], args)
    renderLog.save_self()

    return renderLog.to_dict()


@app.get('{}{}/get'.format(API_EXT, LOG_API_EXT))
def get_all_logs():
    return abstract_read_all(RenderLog.read_all())


@app.get('{}{}/get/<uuid>'.format(API_EXT, LOG_API_EXT))
def get_log(uuid):
    return abstract_read_one(RenderLog.read(uuid))


@app.put('{}{}/put/<uuid>'.format(API_EXT, LOG_API_EXT))
def update_log(uuid):
    return abstract_update(RenderLog.read(uuid), request.data.decode('utf-8'))


@app.delete('{}{}/delete'.format(API_EXT, LOG_API_EXT))
def delete_all_logs():
    return abstract_delete_all("Logs", True)


@app.delete('{}{}/delete/<uuid>'.format(API_EXT, LOG_API_EXT))
def delete_log(uuid):
    return abstract_delete(uuid, "Log", False)
