import logging
import time
import os

from flask import Flask
from flask import request
from flask import render_template

from util import RenderRequest


MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
HTML_FOLDER = os.path.join(MODULE_PATH, 'html')

LOGGER = logging.getLogger(__name__)

app = Flask(__name__)
FLASK_EXE = r'E:\Epic\UE_5.0\Engine\Binaries\ThirdParty\Python3\Win64\Scripts\flask.exe'


@app.route('/')
def index_page():
    rrequests = RenderRequest.read_all()
    if not rrequests:
        return 'Welcome!'

    jsons = [rrequest.to_dict() for rrequest in rrequests]

    return render_template('index.html', requests=jsons)


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
        return

    worker = 'RENDER_MACHINE_01'
    assign_request(req, worker)

    time.sleep(4)
    LOGGER.info('assigned job %s to %s', req.uuid, worker)


def assign_request(req, worker):
    req.assign(worker)
    req.update(status=RenderRequest.RenderStatus.ready_to_start)


if __name__ == '__main__':
    import subprocess
    import os

    env = os.environ.copy()
    env['PYTHONPATH'] += os.pathsep + MODULE_PATH

    command = [
        FLASK_EXE,
        '--app',
        'RequestManager.py',
        '--debug',
        'run',
        '-h',
        'localhost',
        '-p',
        '5000'
    ]

    proc = subprocess.Popen(command, env=env)
    LOGGER.info(proc.communicate())
