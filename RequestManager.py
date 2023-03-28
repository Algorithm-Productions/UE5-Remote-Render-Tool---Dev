import logging
import time
import os

from flask import Flask
from flask import request
from flask import render_template

from util import renderRequest

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
HTML_FOLDER = os.path.join(MODULE_PATH, 'html')
LOGGER = logging.getLogger(__name__)
app = Flask(__name__)
FLASK_EXE = r'C:\Users\Cinema_4D\Desktop\Victor\UE5-Remote-Render-Tool\venv\Scripts\flask.exe'


@app.route('/')
def index_page():
    reqs = renderRequest.read_all()
    if not reqs:
        return 'Welcome!'

    jsons = [req.to_dict() for req in reqs]

    return render_template('index.html', requests=jsons)


@app.get('/api/get')
def get_all_requests():
    reqs = renderRequest.read_all()
    jsons = [req.to_dict() for req in reqs]

    return {"results": jsons}


@app.get('/api/get/<uid>')
def get_request(uid):
    req = renderRequest.RenderRequest.from_db(uid)
    return req.to_dict()


@app.delete('/api/delete/<uid>')
def delete_request(uid):
    renderRequest.remove_db(uid)


@app.post('/api/post')
def create_request():
    data = request.get_json(force=True)
    req = renderRequest.RenderRequest.from_dict(data)
    req.write_json()
    new_request_trigger(req)

    return req.to_dict()


@app.put('/api/put/<uid>')
def update_request(uid):
    content = request.data.decode('utf-8')
    progress, time_estimate, status = content.split(';')

    req = renderRequest.RenderRequest.from_db(uid)
    if not req:
        return {}

    req.update(
        progress=int(float(progress)),
        time_estimate=time_estimate,
        status=status
    )
    return req.to_dict()


def new_request_trigger(req):
    if req.worker:
        return

    worker = 'RENDER_MACHINE_01'
    assign_request(req, worker)

    time.sleep(4)
    LOGGER.info('assigned job %s to %s', req.uid, worker)


def assign_request(req, worker):
    req.assign(worker)
    req.update(status=renderRequest.RenderStatus.ready_to_start)


if __name__ == '__main__':
    import subprocess
    import os

    env = os.environ.copy()
    print(env)
    env['PYTHONPATH'] += os.pathsep + MODULE_PATH

    command = [
        FLASK_EXE,
        '--app',
        'requestManager.py',
        '--debug',
        'run',
        '-h',
        'localhost',
        '-p',
        '5000'
    ]

    process = subprocess.Popen(command, env=env)
    LOGGER.info(process.communicate())
