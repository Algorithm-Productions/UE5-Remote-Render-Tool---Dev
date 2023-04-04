import logging
import time
import os
from dotenv import load_dotenv

from flask import Flask, send_from_directory
from flask import request
from flask import render_template

from util import RenderRequest

load_dotenv()
MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
HTML_FOLDER = os.path.join(MODULE_PATH, 'html')

LOGGER = logging.getLogger(__name__)
DEFAULT_WORKER = os.getenv("DEFAULT_WORKER")

app = Flask(__name__)
FLASK_EXE = os.getenv("FLASK_EXE")


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.png', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def index_page():
    return render_template('landing.html')


@app.route('/queue/')
def queue_page():
    rrequests = RenderRequest.read_all()
    if not rrequests:
        return render_template('error.html', errorText="No Ongoing Renders", title="Render Queue")

    jsons = [rrequest.to_dict() for rrequest in rrequests]

    return render_template('queue.html', requests=jsons)


@app.route('/archive/')
def archive_page():
    rrequests = RenderRequest.read_archive()
    if not rrequests:
        return render_template('error.html', errorText="No Ongoing Renders", title="Render Archive")

    jsons = [rrequest.to_dict() for rrequest in rrequests]

    return render_template('archive.html', requests=jsons)


@app.get('/api/get')
def get_all_requests():
    rrequests = RenderRequest.read_all()
    jsons = [rrequest.to_dict() for rrequest in rrequests]

    return {"results": jsons}


@app.get('/api/get/<uuid>')
def get_request(uuid):
    rr = RenderRequest.RenderRequest.from_db(uuid)
    return rr.to_dict()


@app.delete('/api/delete/<uuid>')
def delete_request(uuid):
    RenderRequest.remove_db(uuid)


@app.post('/api/post')
def create_request():
    data = request.get_json(force=True)
    req = RenderRequest.RenderRequest.from_dict(data)
    req.write_json()
    new_request_trigger(req)

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


if __name__ == '__main__':
    import os

    env = os.environ.copy()
    env['PYTHONPATH'] += os.pathsep + MODULE_PATH

    app.run(port=5000, debug=True)
