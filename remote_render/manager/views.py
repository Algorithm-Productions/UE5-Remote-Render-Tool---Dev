import logging
import platform
import time
import os
from datetime import datetime, timedelta
import uuid as genUUID

from dotenv import load_dotenv
from flask import request, render_template, send_from_directory, make_response, redirect, url_for
from remote_render.util.datatypes import RenderArchive, RenderRequest, RenderLog, RenderSettings, \
    RenderStatus, HardwareStats, LogType
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
    requests = RenderRequest.read_all()
    if not requests:
        return render_template('error.html', errorText="No Ongoing Renders", title="Render Queue",
                               page_passer="queue_page")

    jsons = [request.to_dict() for request in requests]

    return render_template('queue.html', requests=jsons)


@app.route('/archive/')
def archive_page():
    requests = RenderArchive.read_all()
    if not requests:
        return render_template('error.html', errorText="No Archived Renders", title="Render Archive",
                               page_passer="archive_page")

    jsons = [request.to_dict() for request in requests]

    return render_template('archive.html', requests=jsons)


@app.route('/archive/<uuid>')
def archive_entry(uuid):
    rr = RenderArchive.read(uuid)
    return render_template('archive_entry.html', entry=rr.to_dict(), uuid=uuid)


@app.route('/logs/')
def logs_page():
    requests = RenderLog.read_all()
    if not requests:
        return render_template('error.html', errorText="No logs", title="Application Logs",
                               page_passer="logs_page")

    jsons = [request.to_dict() for request in requests]

    return render_template('logs.html', requests=jsons)


@app.route('/logs/<uuid>')
def logs_entry(uuid):
    rn = RenderLog.read(uuid)

    return render_template('logs_entry.html', entry=rn.to_dict(), uuid=uuid)


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


# End of Routes Section
# Start of the General API Section

@app.post('{}/ping'.format(API_EXT))
def ping():
    return "Pong"


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


# End of the General API Section
# Start of Queue API Section

@app.post('{}/post'.format(API_EXT))
def create_request():
    data = request.get_json(force=True)
    req = RenderRequest.from_dict(data)
    req.save_self()
    new_request_trigger(req)

    buildLog(req.uuid, [req.uuid, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                        'Creating Request {} on DB'.format(req.uuid),
                        'Creating Request {} on DB'.format(req.uuid), "INFO"]).save_self()

    return req.to_dict()


@app.get('{}/get'.format(API_EXT))
def get_all_requests():
    reqs = RenderRequest.read_all()
    if not reqs:
        return {"results": []}

    jsons = [req.to_dict() if req else {} for req in reqs]

    return {"results": jsons}


@app.get('{}/get/<uuid>'.format(API_EXT))
def get_request(uuid):
    res = RenderRequest.read(uuid)
    return res.to_dict()


@app.put('{}/put/<uuid>'.format(API_EXT))
def update_request(uuid):
    content = request.data.decode('utf-8')
    progress, time_estimate, status = content.split(';')

    rr = RenderRequest.read(uuid)
    if not rr:
        return {}

    rr.update({"progress": int(float(progress)),
               "time_estimate": time_estimate,
               "status": status})

    return rr.to_dict()


@app.delete('{}/delete/'.format(API_EXT))
def delete_all_requests():
    responses = RenderRequest.read_all()
    RenderRequest.remove_all()

    buildLog('', ['', datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                  'Deleting All Requests from DB',
                  'Deleting All Requests from DB', "CRITICAL"]).save_self()

    return {"results": [res.to_dict for res in responses]}


@app.delete('{}/delete/<uuid>'.format(API_EXT))
def delete_request(uuid):
    res = RenderRequest.read(uuid)
    res.remove_self()

    buildLog(uuid, [uuid, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                    'Deleting Request {} from DB'.format(uuid),
                    'Deleting Request {} from DB'.format(uuid), "WARN"]).save_self()

    return res.to_dict()


# End of Queue API Section
# Start of Archive API Section


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
    reqs = RenderArchive.read_all()
    if not reqs:
        return {"results": []}

    jsons = [req.to_dict() if req else {} for req in reqs]

    return {"results": jsons}


@app.get('{}{}/get/<uuid>'.format(API_EXT, ARCHIVE_API_EXT))
def get_archive(uuid):
    res = RenderArchive.read(uuid)
    return res.to_dict()


@app.put('{}{}/<uuid>'.format(API_EXT, ARCHIVE_API_EXT))
def update_archive(uuid):
    pass


@app.delete('{}{}/delete'.format(API_EXT, ARCHIVE_API_EXT))
def delete_all_archives():
    responses = RenderArchive.read_all()
    RenderArchive.remove_all()

    buildLog('', ['', datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                  'Deleting All Archives from DB',
                  'Deleting All Archives from DB', "CRITICAL"]).save_self()

    return {"results": [res.to_dict for res in responses]}


@app.delete('{}{}/delete/<uuid>'.format(API_EXT, ARCHIVE_API_EXT))
def delete_archive(uuid):
    res = RenderArchive.read(uuid)
    res.remove_self()

    buildLog(uuid, [uuid, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                    'Deleting Archive {} from DB'.format(uuid),
                    'Deleting Archive {} from DB'.format(uuid), "WARN"]).save_self()

    return res.to_dict()


# End of Archive API Section


# Start of Logs API Section
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
    reqs = RenderArchive.read_all()
    if not reqs:
        return {"results": []}

    jsons = [req.to_dict() if req else {} for req in reqs]

    return {"results": jsons}


@app.get('{}{}/get/<uuid>'.format(API_EXT, LOG_API_EXT))
def get_log(uuid):
    res = RenderLog.read(uuid)
    return res.to_dict()


@app.put('{}{}/put/<uuid>'.format(API_EXT, LOG_API_EXT))
def update_log(uuid):
    content = request.data.decode('utf-8')
    res = RenderLog.read(uuid)

    if (not res) or (not content):
        return {}

    parsedContent = eval(content)
    if not parsedContent:
        return {}

    res.update(parsedContent)
    return res.to_dict()


@app.delete('{}{}/delete'.format(API_EXT, LOG_API_EXT))
def delete_all_logs():
    responses = RenderLog.read_all()
    RenderLog.remove_all()

    buildLog('', ['', datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                  'Deleting All Logs from DB',
                  'Deleting All Logs from DB', "CRITICAL"]).save_self()

    return {"results": [res.to_dict for res in responses]}


@app.delete('{}{}/delete/<uuid>'.format(API_EXT, LOG_API_EXT))
def delete_log(uuid):
    res = RenderLog.read(uuid)
    res.remove_self()
    return res.to_dict()


# End of Logs API Section
# TODO: Move to Manager class (?)
# Start of Helper Methods Section


def new_request_trigger(req):
    if req.worker:
        req.update({"status": RenderStatus.ready_to_start})
        return

    assign_request(req, DEFAULT_WORKER)

    time.sleep(3)
    LOGGER.info('assigned job %s to %s', req.uuid, DEFAULT_WORKER)


def assign_request(req, worker):
    req.assign(worker)
    req.update({"status": RenderStatus.ready_to_start})


def buildArchive(uuid, renderRequest, metadata):
    renderArchive = RenderArchive(uuid=uuid, render_request=renderRequest)
    renderArchive.project_name = metadata[1]
    renderArchive.hardware_stats = HardwareStats.from_dict(eval(metadata[2]))
    renderArchive.finish_time = metadata[3]
    renderArchive.avg_frame = float(metadata[4])
    renderArchive.frame_map = metadata[5].strip('][').split(', ')
    renderArchive.render_settings = RenderSettings.from_dict(eval(metadata[6]))

    renderArchive.total_time = str(
        datetime.strptime(renderArchive.finish_time, "%m/%d/%Y, %H:%M:%S") - datetime.strptime(
            renderRequest.time_created, "%m/%d/%Y, %H:%M:%S"))

    return renderArchive


def buildLog(jobUUID, metadata):
    return RenderLog(uuid=str(genUUID.uuid4())[:5], jobUUID=jobUUID, timestamp=metadata[1],
                     message=metadata[2], log=metadata[3],
                     logType=(metadata[4].upper() if LogType.contains(metadata[4].upper()) else ''))


def getLogsToDisplay():
    allLogs = RenderLog.read_all()
    objList = []

    for log in allLogs:
        deleted = checkAgeAndClear(log)
        if log.logType != LogType.INFO and (not deleted) and (not log.cleared):
            objList.append(log)

    objList.sort()
    returnList = [log.to_dict() for log in objList]

    return returnList


def checkAgeAndClear(log):
    curDate = datetime.now()
    logDate = datetime.strptime(log.timestamp, "%m/%d/%Y, %H:%M:%S")

    diff = curDate - logDate
    if diff.days >= 7:
        log.remove()
        return True
    else:
        return False
