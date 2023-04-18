import logging

import eel
import platform

import remote_render.util.Client as Client

eel.init("frontend")

NECESSARY_KEYS = ['name', 'owner', 'worker', 'project_path', 'level_path', 'sequence_path', 'config_path',
                  'output_path']

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


@eel.expose
def connectToServer():
    res = Client.ping_server()
    return res and res.status_code == 200


@eel.expose
def getWorkers():
    res = Client.get_workers()
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
