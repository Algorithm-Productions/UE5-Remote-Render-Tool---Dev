import logging
import platform
import time
import os
from datetime import datetime, timedelta
import uuid as genUUID

from dotenv import load_dotenv

from flask import send_from_directory, make_response, redirect, url_for
from flask import request
from flask import render_template

from util.datatypes import RenderArchive, RenderRequest, RenderLog
from util.ManagerFlaskApp import ManagerFlaskApp
from util.datatypes.RenderLog import LogType
from util.datatypes.RenderArchive import HardwareStats
from util.datatypes.RenderSettings import RenderSettings
from util.datatypes.enums import RenderStatus

load_dotenv()
MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
HTML_FOLDER = os.path.join(MODULE_PATH, 'html')

LOGGER = logging.getLogger(__name__)
DEFAULT_WORKER = os.getenv("DEFAULT_WORKER")

app = ManagerFlaskApp(__name__)
FLASK_EXE = os.getenv("FLASK_EXE")

MANAGER_NAME = platform.node()

API_EXT = os.getenv("API_EXT")
ARCHIVE_API_EXT = os.getenv("ARCHIVE_API_EXT")
LOG_API_EXT = os.getenv("LOG_API_EXT")


# Route Section

@app.route('/')
def index_page():
    logs = getLogsToDisplay()
    return render_template('landing.html', logs=logs)


@app.route('/queue/')
def queue_page():
    rrequests = RenderRequest.RenderRequest.read_all()
    if not rrequests:
        return render_template('error.html', errorText="No Ongoing Renders", title="Render Queue",
                               page_passer="queue_page")

    jsons = [rrequest.to_dict() for rrequest in rrequests]

    return render_template('queue.html', requests=jsons)


@app.route('/archive/')
def archive_page():
    rrequests = RenderArchive.RenderArchive.read_all()
    if not rrequests:
        return render_template('error.html', errorText="No Archived Renders", title="Render Archive",
                               page_passer="archive_page")

    jsons = [rrequest.to_dict() for rrequest in rrequests]

    return render_template('archive.html', requests=jsons)


@app.route('/archive/<uuid>')
def archive_entry(uuid):
    rr = RenderArchive.RenderArchive.read(uuid)

    return render_template('archive_entry.html', entry=rr.to_dict(), uuid=uuid)


@app.route('/logs/')
def logs_page():
    rrequests = RenderLog.read_all()
    if not rrequests:
        return render_template('error.html', errorText="No logs", title="Application Logs",
                               page_passer="logs_page")

    jsons = [rrequest.to_dict() for rrequest in rrequests]

    return render_template('logs.html', requests=jsons)


@app.route('/logs/<uuid>')
def logs_entry(uuid):
    rn = RenderLog.RenderLog.read(uuid)

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
# Start of Queue API Section


@app.post('{}/post'.format(API_EXT))
def create_request():
    data = request.get_json(force=True)
    req = RenderRequest.RenderRequest.from_dict(data)
    req.save_self()
    new_request_trigger(req)

    buildLog(req.uuid, [req.uuid, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                        'Creating Request {} on DB'.format(req.uuid),
                        'Creating Request {} on DB'.format(req.uuid), "INFO"]).save_self()

    return req.to_dict()


@app.get('{}/get'.format(API_EXT))
def get_all_requests():
    reqs = RenderRequest.RenderRequest.read_all()
    if not reqs:
        return {"results": []}

    jsons = [req.to_dict() if req else {} for req in reqs]

    return {"results": jsons}


@app.get('{}/get/<uuid>'.format(API_EXT))
def get_request(uuid):
    res = RenderRequest.RenderRequest.read(uuid)
    return res.to_dict()


@app.put('{}/put/<uuid>'.format(API_EXT))
def update_request(uuid):
    content = request.data.decode('utf-8')
    progress, time_estimate, status = content.split(';')

    rr = RenderRequest.RenderRequest.read(uuid)
    if not rr:
        return {}

    rr.update({
        "progress": int(float(progress)),
        "time_estimate": time_estimate,
        "status": status
    })
    return rr.to_dict()


@app.delete('{}/delete/'.format(API_EXT))
def delete_all_requests():
    responses = RenderRequest.RenderRequest.read_all()
    RenderRequest.RenderRequest.remove_all()

    buildLog('', ['', datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                  'Deleting All Requests from DB',
                  'Deleting All Requests from DB', "CRITICAL"]).save_self()

    return {"results": [res.to_dict for res in responses]}


@app.delete('{}/delete/<uuid>'.format(API_EXT))
def delete_request(uuid):
    res = RenderRequest.RenderRequest.read(uuid)
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
    renderRequest = RenderRequest.RenderRequest.read(args[0])
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
    reqs = RenderArchive.RenderArchive.read_all()
    if not reqs:
        return {"results": []}

    jsons = [req.to_dict() if req else {} for req in reqs]

    return {"results": jsons}


@app.get('{}{}/get/<uuid>'.format(API_EXT, ARCHIVE_API_EXT))
def get_archive(uuid):
    res = RenderArchive.RenderArchive.read(uuid)
    return res.to_dict()


@app.put('{}{}/<uuid>'.format(API_EXT, ARCHIVE_API_EXT))
def update_archive(uuid):
    pass


@app.delete('{}{}/delete'.format(API_EXT, ARCHIVE_API_EXT))
def delete_all_archives():
    responses = RenderArchive.RenderArchive.read_all()
    RenderArchive.RenderArchive.remove_all()

    buildLog('', ['', datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                  'Deleting All Archives from DB',
                  'Deleting All Archives from DB', "CRITICAL"]).save_self()

    return {"results": [res.to_dict for res in responses]}


@app.delete('{}{}/delete/<uuid>'.format(API_EXT, ARCHIVE_API_EXT))
def delete_archive(uuid):
    res = RenderArchive.RenderArchive.read(uuid)
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
    reqs = RenderArchive.RenderArchive.read_all()
    if not reqs:
        return {"results": []}

    jsons = [req.to_dict() if req else {} for req in reqs]

    return {"results": jsons}


@app.get('{}{}/get/<uuid>'.format(API_EXT, LOG_API_EXT))
def get_log(uuid):
    res = RenderLog.RenderLog.read(uuid)
    return res.to_dict()


@app.put('{}{}/put/<uuid>'.format(API_EXT, LOG_API_EXT))
def update_log(uuid):
    content = request.data.decode('utf-8')
    res = RenderLog.RenderLog.read(uuid)

    if (not res) or (not content):
        return {}

    parsedContent = eval(content)
    if not parsedContent:
        return {}

    res.update(parsedContent)
    return res.to_dict()

@app.delete('{}{}/delete'.format(API_EXT, LOG_API_EXT))
def delete_all_logs():
    responses = RenderLog.RenderLog.read_all()
    RenderLog.RenderLog.remove_all()

    buildLog('', ['', datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                  'Deleting All Logs from DB',
                  'Deleting All Logs from DB', "CRITICAL"]).save_self()

    return {"results": [res.to_dict for res in responses]}


@app.delete('{}{}/delete/<uuid>'.format(API_EXT, LOG_API_EXT))
def delete_log(uuid):
    res = RenderLog.RenderLog.read(uuid)
    res.remove_self()

    return res.to_dict()


# End of Logs API Section
# Start of Helper Methods Section


def new_request_trigger(req):
    if req.worker:
        req.update({"status": RenderStatus.RenderStatus.ready_to_start})
        return

    assign_request(req, DEFAULT_WORKER)

    time.sleep(3)
    LOGGER.info('assigned job %s to %s', req.uuid, DEFAULT_WORKER)


def assign_request(req, worker):
    req.assign(worker)
    req.update({"status": RenderStatus.RenderStatus.ready_to_start})


def buildArchive(uuid, renderRequest, metadata):
    renderArchive = RenderArchive.RenderArchive(uuid=uuid, render_request=renderRequest)
    renderArchive.project_name = metadata[1]
    renderArchive.hardware_stats = HardwareStats.HardwareStats.from_dict(eval(metadata[2]))
    renderArchive.finish_time = metadata[3]
    renderArchive.avg_frame = float(metadata[4])
    renderArchive.frame_map = metadata[5].strip('][').split(', ')
    renderArchive.render_settings = RenderSettings.from_dict(eval(metadata[6]))

    renderArchive.total_time = str(
        datetime.strptime(renderArchive.finish_time, "%m/%d/%Y, %H:%M:%S") - datetime.strptime(
            renderRequest.time_created, "%m/%d/%Y, %H:%M:%S"))

    return renderArchive


def buildLog(jobUUID, metadata):
    return RenderLog.RenderLog(uuid=str(genUUID.uuid4())[:5], jobUUID=jobUUID, timestamp=metadata[1],
                               message=metadata[2], log=metadata[3],
                               logType=(metadata[4].upper() if LogType.contains(metadata[4].upper()) else ''))


def getLogsToDisplay():
    allLogs = RenderLog.RenderLog.read_all()
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


# End of Helper Methods Section
# Start of Main


if __name__ == '__main__':
    import os

    env = os.environ.copy()
    env['PYTHONPATH'] += os.pathsep + MODULE_PATH

    app.run(port=5000, debug=True)
