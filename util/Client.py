import logging
import os
import requests
from dotenv import load_dotenv

from .datatypes import RenderArchive, RenderRequest, RenderLog

LOGGER = logging.getLogger(__name__)

MODULE_PATH = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(MODULE_PATH, '../.env'))

SERVER_URL = os.getenv("SERVER_URL")
SERVER_API_URL = SERVER_URL + os.getenv("API_EXT")

ARCHIVE_API_EXT = os.getenv("ARCHIVE_API_EXT")
LOG_API_EXT = os.getenv("LOG_API_EXT")

# Start of the General Methods Section


def ping_server(data=None):
    try:
        response = requests.post(SERVER_API_URL + '/ping', json=data)
    except requests.exceptions.ConnectionError:
        LOGGER.error('failed to connect to server %s', SERVER_API_URL)
        return

    return response


def register_worker(worker_name, data=None):
    try:
        response = requests.post(SERVER_API_URL + '/register/'.format(worker_name), json=data)
    except requests.exceptions.ConnectionError:
        LOGGER.error('failed to connect to server %s', SERVER_API_URL)
        return

    return response


# End of the General Methods Section
# Start of Abstract Methods Section


def create(data, specialPath=''):
    try:
        response = requests.post(SERVER_API_URL + specialPath + '/post', json=data)
    except requests.exceptions.ConnectionError:
        LOGGER.error('failed to connect to server %s', SERVER_API_URL)
        return

    return response


def get_all(specialPath=''):
    try:
        response = requests.get(SERVER_API_URL + specialPath + '/get')
    except requests.exceptions.ConnectionError:
        LOGGER.error('failed to connect to server %s', SERVER_API_URL)
        return

    if (not response) or (not response.json()) or (not response.json()['results']):
        return []

    return response.json()['results']


def get(uuid, specialPath=''):
    try:
        response = requests.get(SERVER_API_URL + specialPath + '/get/{}'.format(uuid))
    except requests.exceptions.ConnectionError:
        LOGGER.error('failed to connect to server %s', SERVER_API_URL)
        return

    return response


def update(uuid, params, specialPath=''):
    try:
        response = requests.put(
            SERVER_API_URL + specialPath + '/put/{}'.format(uuid),
            params
        )
    except requests.exceptions.ConnectionError:
        LOGGER.error('failed to connect to server %s', SERVER_API_URL)
        return

    return response


def delete_all(specialPath=''):
    try:
        response = requests.delete(SERVER_API_URL + specialPath + '/delete')
    except requests.exceptions.ConnectionError:
        LOGGER.error('failed to connect to server %s', SERVER_API_URL)
        return

    if (not response) or (not response.json()) or (not response.json()['results']):
        return []

    return response.json()['results']


def delete(uuid, specialPath=''):
    try:
        response = requests.delete(SERVER_API_URL + specialPath + '/delete/{}'.format(uuid))
    except requests.exceptions.ConnectionError:
        LOGGER.error('failed to connect to server %s', SERVER_API_URL)
        return

    return response


# End of Abstract Methods Section
# Start of Queue Methods Section


def create_request(data):
    response = create(data)
    return RenderRequest.RenderRequest.from_dict(response.json()) if (response and response.json()) else None


def get_all_requests():
    response = get_all()
    return [(RenderRequest.RenderRequest.from_dict(res) if res else None) for res in
            response] if response else []


def get_request(uuid):
    response = get(uuid)
    return RenderRequest.RenderRequest.from_dict(response.json()) if (response and response.json()) else None


def update_request(uuid, params):
    response = update(uuid, params)
    return RenderRequest.RenderRequest.from_dict(response.json()) if (response and response.json()) else None


def delete_all_requests():
    response = delete_all()
    return [(RenderRequest.RenderRequest.from_dict(res.json()) if (res and res.json()) else None) for res in
            response] if response else []


def delete_request(uuid):
    response = delete(uuid)
    return RenderRequest.RenderRequest.from_dict(response.json()) if (response and response.json()) else None


# End of Queue Methods Section
# Start of Archives Methods Section


def create_archive(data):
    response = create(data, ARCHIVE_API_EXT)
    return RenderArchive.RenderArchive.from_dict(response.json()) if (response and response.json()) else None


def get_all_archives():
    response = get_all(ARCHIVE_API_EXT)
    return [(RenderArchive.RenderArchive.from_dict(res) if res else None) for res in
            response] if response else []


def get_archive(uuid):
    response = get(uuid, ARCHIVE_API_EXT)
    return RenderArchive.RenderArchive.from_dict(response.json()) if (response and response.json()) else None


def update_archive(uuid, params):
    response = update(uuid, params, ARCHIVE_API_EXT)
    return RenderArchive.RenderArchive.from_dict(response.json()) if (response and response.json()) else None


def delete_all_archives():
    response = delete_all(ARCHIVE_API_EXT)
    return [(RenderArchive.RenderArchive.from_dict(res) if res else None) for res in
            response] if response else []


def delete_archive(uuid):
    response = delete(uuid, ARCHIVE_API_EXT)
    return RenderRequest.RenderRequest.from_dict(response.json()) if (response and response.json()) else None


# End of Archives Methods Section
# Start of Logs Methods Section


def create_log(data):
    response = create(data, LOG_API_EXT)
    return RenderLog.RenderLog.from_dict(response.json()) if (response and response.json()) else None


def get_all_logs():
    response = get_all(LOG_API_EXT)
    return [(RenderLog.RenderLog.from_dict(res.json()) if (res and res.json()) else None) for res in
            response] if response else []


def get_log(uuid):
    response = get(uuid, LOG_API_EXT)
    return RenderLog.RenderLog.from_dict(response.json()) if (response and response.json()) else None


def update_log(uuid, params):
    response = update(uuid, params, LOG_API_EXT)
    return RenderLog.RenderLog.from_dict(response.json()) if (response and response.json()) else None


def delete_all_logs():
    response = delete_all(LOG_API_EXT)
    return [(RenderLog.RenderLog.from_dict(res) if res else None) for res in
            response] if response else []


def delete_log(uuid):
    response = delete(uuid, LOG_API_EXT)
    return RenderLog.RenderLog.from_dict(response.json()) if (response and response.json()) else None

# End of Logs Methods Section
