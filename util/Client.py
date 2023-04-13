import logging
import os
import requests
from dotenv import load_dotenv

from . import RenderRequest

LOGGER = logging.getLogger(__name__)

MODULE_PATH = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(MODULE_PATH, '../.env'))

SERVER_URL = os.getenv("SERVER_URL")
SERVER_API_URL = SERVER_URL + os.getenv("API_EXT")


def get_all_requests():
    try:
        response = requests.get(SERVER_API_URL + '/get')
    except requests.exceptions.ConnectionError:
        LOGGER.error('failed to connect to server %s', SERVER_API_URL)
        return

    results = response.json()['results']
    return [RenderRequest.RenderRequest.from_dict(result) for result in results]


def get_request(uuid):
    try:
        response = requests.get(SERVER_API_URL + '/get/{}'.format(uuid))
    except requests.exceptions.ConnectionError:
        LOGGER.error('failed to connect to server %s', SERVER_API_URL)
        return

    return RenderRequest.RenderRequest.from_dict(response.json())


def add_request(data):
    try:
        response = requests.post(SERVER_API_URL + '/post', json=data)
    except requests.exceptions.ConnectionError:
        LOGGER.error('failed to connect to server %s', SERVER_API_URL)
        return

    return RenderRequest.RenderRequest.from_dict(response.json())


def remove_request(uuid):
    try:
        response = requests.delete(SERVER_API_URL + '/delete/{}'.format(uuid))
    except requests.exceptions.ConnectionError:
        LOGGER.error('failed to connect to server %s', SERVER_API_URL)
        return

    return RenderRequest.RenderRequest.from_dict(response.json())


def update_request(uuid, params):
    try:
        response = requests.put(
            SERVER_API_URL + '/put/{}'.format(uuid),
            params
        )
    except requests.exceptions.ConnectionError:
        LOGGER.error('failed to connect to server %s', SERVER_API_URL)
        return

    return RenderRequest.RenderRequest.from_dict(response.json())


def send_notification(uuid, args):
    try:
        response = requests.put(
            SERVER_API_URL + '/logs/post/{}'.format(uuid),
            '{};{};{};{};{}'.format(args[0], args[1], args[2], args[3], args[4])
        )
    except requests.exceptions.ConnectionError:
        LOGGER.error('failed to connect to server %s', SERVER_API_URL)
        return

    return RenderRequest.RenderRequest.from_dict(response.json())
