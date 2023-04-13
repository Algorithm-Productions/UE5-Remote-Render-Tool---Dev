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

from util import RenderRequest, RenderArchive, RenderNotification
from util.ManagerFlaskApp import ManagerFlaskApp
from util.RenderNotification import NotificationType
from util.RenderArchive import HardwareStats
from util.RenderSettings import RenderSettings

load_dotenv()
MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
HTML_FOLDER = os.path.join(MODULE_PATH, 'html')

LOGGER = logging.getLogger(__name__)
DEFAULT_WORKER = os.getenv("DEFAULT_WORKER")

app = ManagerFlaskApp(__name__)
FLASK_EXE = os.getenv("FLASK_EXE")

MANAGER_NAME = platform.node()


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.png', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def index_page():
    notifications = getNotificationsToDisplay()
    return render_template('landing.html', notifications=notifications)


@app.route('/queue/')
def queue_page():
    rrequests = RenderRequest.read_all()
    if not rrequests:
        return render_template('error.html', errorText="No Ongoing Renders", title="Render Queue",
                               page_passer="queue_page")

    jsons = [rrequest.to_dict() for rrequest in rrequests]

    return render_template('queue.html', requests=jsons)


@app.route('/archive/')
def archive_page():
    rrequests = RenderArchive.read_all()
    if not rrequests:
        return render_template('error.html', errorText="No Archived Renders", title="Render Archive",
                               page_passer="archive_page")

    jsons = [rrequest.to_dict() for rrequest in rrequests]

    return render_template('archive.html', requests=jsons)


@app.route('/archive/<uuid>')
def archive_entry(uuid):
    rr = RenderArchive.RenderArchive.from_db(uuid)

    return render_template('archive_entry.html', entry=rr.to_dict(), uuid=uuid)


@app.route('/logs/')
def logs_page():
    rrequests = RenderNotification.read_all()
    if not rrequests:
        return render_template('error.html', errorText="No logs", title="Application Logs",
                               page_passer="logs_page")

    jsons = [rrequest.to_dict() for rrequest in rrequests]

    return render_template('logs.html', requests=jsons)


@app.route('/logs/<uuid>')
def logs_entry(uuid):
    rn = RenderNotification.RenderNotification.from_db(uuid)

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


@app.get('/api/get')
def get_all_requests():
    rrequests = RenderRequest.read_all()
    if not rrequests:
        return {"results": []}

    jsons = [rrequest.to_dict() if rrequest else {} for rrequest in rrequests]

    return {"results": jsons}


@app.get('/api/get/<uuid>')
def get_request(uuid):
    rr = RenderRequest.RenderRequest.from_db(uuid)
    return rr.to_dict()


@app.delete('/api/delete/<uuid>')
def delete_request(uuid):
    buildNotification(uuid, [uuid, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                             'Deleting Request {} from DB'.format(uuid),
                             'Deleting Request {} from DB'.format(uuid), "WARN"]).write_json()
    renderRequest = RenderRequest.RenderRequest.from_db(uuid)

    renderRequest.remove()

    return renderRequest.to_dict()


@app.post('/api/post')
def create_request():
    data = request.get_json(force=True)
    req = RenderRequest.RenderRequest.from_dict(data)
    req.write_json()
    new_request_trigger(req)

    buildNotification(req.uuid, [req.uuid, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                                 'Creating Request {} on DB'.format(req.uuid),
                                 'Creating Request {} on DB'.format(req.uuid), "INFO"]).write_json()

    return req.to_dict()


@app.put('/api/put/<uuid>')
def update_request(uuid):
    content = request.data.decode('utf-8')
    progress, time_estimate, status = content.split(';')

    rr = RenderRequest.RenderRequest.from_db(uuid)
    if not rr:
        return {}

    rr.update(
        progress=int(float(progress)),
        time_estimate=time_estimate,
        status=status
    )
    return rr.to_dict()


@app.put('/api/archive/post/<uuid>')
def archive_request(uuid):
    content = request.data.decode('utf-8')

    args = content.split(";")
    renderRequest = RenderRequest.RenderRequest.from_db(uuid)
    if (not renderRequest) or len(args) != 6:
        return {}

    renderArchive = buildArchive(uuid, renderRequest, args)
    renderArchive.write_json()

    buildNotification(uuid, [uuid, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                             'Archiving Request {}'.format(uuid),
                             'Archiving Request {}'.format(uuid), "INFO"]).write_json()

    return renderArchive.to_dict()


@app.delete('/api/archive/delete/<uuid>')
def delete_archive(uuid):
    buildNotification(uuid, [uuid, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                             'Deleting Archive {} from DB'.format(uuid),
                             'Deleting Archive {} from DB'.format(uuid), "WARN"]).write_json()

    renderArchive = RenderArchive.RenderArchive.from_db(uuid)
    renderArchive.remove()

    return renderArchive.to_dict()


@app.put('/api/logs/post/')
def render_notification():
    content = request.data.decode('utf-8')

    args = content.split(";")
    if len(args) != 5:
        return {}

    renderNotification = buildNotification(args[0], args)
    renderNotification.write_json()

    return renderNotification.to_dict()


@app.delete('/api/logs/delete/<uuid>')
def delete_notification(uuid):
    renderNotification = RenderNotification.RenderNotification.from_db(uuid)
    renderNotification.remove()

    return renderNotification.to_dict()


def new_request_trigger(req):
    if req.worker:
        req.update(status=RenderRequest.RenderStatus.ready_to_start)
        return

    assign_request(req, DEFAULT_WORKER)

    time.sleep(3)
    LOGGER.info('assigned job %s to %s', req.uuid, DEFAULT_WORKER)


def assign_request(req, worker):
    req.assign(worker)
    req.update(status=RenderRequest.RenderStatus.ready_to_start)


def buildArchive(uuid, renderRequest, metadata):
    renderArchive = RenderArchive.RenderArchive(uuid=uuid, render_request=renderRequest)
    renderArchive.project_name = metadata[0]
    renderArchive.hardware_stats = HardwareStats.from_dict(eval(metadata[1]))
    renderArchive.finish_time = metadata[2]
    renderArchive.avg_frame = float(metadata[3])
    renderArchive.frame_map = metadata[4].strip('][').split(', ')
    print(metadata[4])
    renderArchive.render_settings = RenderSettings.from_dict(eval(metadata[5]))

    renderArchive.total_time = str(
        datetime.strptime(renderArchive.finish_time, "%m/%d/%Y, %H:%M:%S") - datetime.strptime(
            renderRequest.time_created, "%m/%d/%Y, %H:%M:%S"))

    return renderArchive


def buildNotification(jobUUID, metadata):
    return RenderNotification.RenderNotification(uuid=str(genUUID.uuid4())[:5], jobUUID=jobUUID, timestamp=metadata[1],
                                                 message=metadata[2], log=metadata[3],
                                                 notificationType=NotificationType.from_string(metadata[4]))


def getNotificationsToDisplay():
    allNotifications = RenderNotification.read_all()
    objList = []

    for notification in allNotifications:
        deleted = checkAgeAndClear(notification)
        if notification.notificationType != NotificationType.INFO and (not deleted):
            objList.append(notification)

    objList.sort()
    returnList = [notification.to_dict() for notification in objList]

    return returnList


def checkAgeAndClear(notification):
    curDate = datetime.now()
    notificationDate = datetime.strptime(notification.timestamp, "%m/%d/%Y, %H:%M:%S")

    diff = curDate - notificationDate
    if diff.days >= 7:
        notification.remove()
        return True
    else:
        return False


if __name__ == '__main__':
    import os

    env = os.environ.copy()
    env['PYTHONPATH'] += os.pathsep + MODULE_PATH

    app.run(port=5000, debug=True)
