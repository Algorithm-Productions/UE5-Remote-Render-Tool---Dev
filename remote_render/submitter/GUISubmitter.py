import logging
import os
import platform
import eel
import argparse
from dotenv import load_dotenv
from remote_render.util import BackendClient as Client
from remote_render import __version__

LOGGER = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('--server_host', type=str, default='localhost', help='Server Host for the Render Manager.')
parser.add_argument('--server_port', type=int, default=5000, help='Server port for the Render Manager.')
parser.add_argument('--auth_token', type=str, default=None, required=False,
                    help='Authentication token for the Render Manager.')
parser.add_argument('-e', '--env', type=str, required=False,
                    help='Path to env file. Default=.env')
parser.add_argument('-d', '--debug', action='store_true', help='Run in debug mode.')
args = parser.parse_args()

if args.env:
    load_dotenv(args.env)
else:
    load_dotenv()

NODE_NAME = platform.node()
SERVER_URL = args.server_host
SERVER_PORT = args.server_port
AUTH_TOKEN = args.auth_token
DEBUG = args.debug or os.getenv('DEBUG', False)

print('Starting GUISubmitter')
client = Client(SERVER_URL, SERVER_PORT, AUTH_TOKEN)

if args.env:
    load_dotenv(args.env)
else:
    load_dotenv()

LOGGER = logging.getLogger(__name__)
MANAGER_NAME = platform.node()
SERVER_URL = os.getenv('SERVER_URL')
SERVER_PORT = os.getenv('SERVER_PORT')
SERVER_DATABASE = os.getenv('DATABASE_FOLDER')
DEBUG = args.debug or os.getenv('DEBUG', False)

eel.init("frontend")

NECESSARY_KEYS = ['name', 'owner', 'worker', 'project_path', 'level_path', 'sequence_path', 'config_path',
                  'output_path']

client = Client()

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


@eel.expose
def connectToServer():
    res = Client.ping_server()
    return res and res.status_code == 200


@eel.expose
def getWorkers():
    res = Client.get_workers()
    print(res)
    return res


@eel.expose
def send_request(data):
    data['owner'] = platform.node()
    verified, msg = verifyData(data)
    if verified:
        send(data)

    return msg


def verifyData(data):
    for key in NECESSARY_KEYS:
        if (key not in data.keys()) or (not data[key]):
            return False, "Missing Data for Key: {}".format(key)

    return True, "200"


def send(data):
    req = Client.create_request(data)
    if req:
        LOGGER.info('request %s sent to server', req.uuid)


eel.start("templates/landing.html")
