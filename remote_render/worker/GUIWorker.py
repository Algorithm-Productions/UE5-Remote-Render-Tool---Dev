import logging
import os
import platform
import eel
import argparse
from dotenv import load_dotenv
import sys

current_dir = os.path.dirname(__file__)
module_dir = os.path.abspath(os.path.join(current_dir, '../../'))
sys.path.append(module_dir)

os.chdir(current_dir)

from remote_render.util.Worker import Worker

from remote_render.util import Client

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('--server_host', type=str, default='localhost', help='Host for the Render Manager.')
parser.add_argument('--server_port', type=str, default='5000', help='Port for the Render Manager.')
parser.add_argument('--auth_token', type=str, default=None, help='Auth token for the Render Manager.')
parser.add_argument('--submitter_host', type=str, default='localhost', help='Host for the Submitter App')
parser.add_argument('--submitter_port', type=str, default='8081', help='Port for the Submitter App')
parser.add_argument('-e', '--env', type=str, required=False, help='Path to env file. Default=.env')
parser.add_argument('-d', '--debug', action='store_true', help='Run in debug mode.')
args = parser.parse_args()

if args.env:
    load_dotenv(args.env)
else:
    load_dotenv()

if args.auth_token:
    AUTH_TOKEN = args.auth_token
else:
    AUTH_TOKEN = 'beepboopity'

NODE_NAME = platform.node()
SERVER_URL = args.server_host
SERVER_PORT = args.server_port
SUBMITTER_HOST = args.submitter_host
SUBMITTER_PORT = args.submitter_port
DEBUG = args.debug or os.getenv('DEBUG', False)
UNREAL_EXE = os.getenv("UNREAL_EXE")

print(f'Running Client: node={NODE_NAME} host={SERVER_URL} port={SERVER_PORT}, auth_token={AUTH_TOKEN}')
client = Client(backend_host=SERVER_URL, backend_port=SERVER_PORT, backend_auth_token=AUTH_TOKEN)

eel.init("frontend")


class GUIClient(object):
    WORKER = None

    def startWorker(self):
        self.WORKER = Worker(platform.node(), client, UNREAL_EXE)
        self.WORKER.start()

    def stopWorker(self):
        self.WORKER.stop()


GUICLIENT = GUIClient()

@eel.expose
def connectToServer():
    res = client.ping_server()
    return res and res.status_code == 200


@eel.expose
def startWorker():
    GUICLIENT.startWorker()


@eel.expose
def closeWorker():
    GUICLIENT.stopWorker()


print(f'Running GUIWorker: node={NODE_NAME} host={SUBMITTER_HOST} port={SUBMITTER_PORT}')
eel.start('templates/landing.html', host=SUBMITTER_HOST, port=SUBMITTER_PORT)
