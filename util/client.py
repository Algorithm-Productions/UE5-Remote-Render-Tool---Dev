import logging
import requests

from . import renderRequest

LOGGER = logging.getLogger(__name__)

SERVER_URL = 'http://127.0.0.1:5000/api'


def get_all_requests():
    try:
        response = requests.get(SERVER_URL + '/get')
    except requests.exceptions.ConnectionError:
        LOGGER.error('failed to connect to server %s', SERVER_URL)
        return

    results = response.json()['results']
    return [renderRequest.RenderRequest.from_dict(result) for result in results]


def get_request(uid):
    try:
        response = requests.get(SERVER_URL + '/get/{}'.format(uid))
    except requests.exceptions.ConnectionError:
        LOGGER.error('failed to connect to server %s', SERVER_URL)
        return

    return renderRequest.RenderRequest.from_dict(response.json())


def add_request(data):
    try:
        response = requests.post(SERVER_URL + '/post', json=data)
    except requests.exceptions.ConnectionError:
        LOGGER.error('failed to connect to server %s', SERVER_URL)
        return

    return renderRequest.RenderRequest.from_dict(response.json())


def update_request(uid, progress=0, status='', time_estimate=''):
    try:
        response = requests.put(
            SERVER_URL + '/put/{}'.format(uid),
            params={
                'progress': progress,
                'status': status,
                'time_estimate': time_estimate
            }
        )
    except requests.exceptions.ConnectionError:
        LOGGER.error('failed to connect to server %s', SERVER_URL)
        return

    return renderRequest.RenderRequest.from_dict(response.json())


def remove_all_requests():
    try:
        response = requests.delete(SERVER_URL + '/delete')
    except requests.exceptions.ConnectionError:
        LOGGER.error('failed to connect to server %s', SERVER_URL)
        return

    return renderRequest.RenderRequest.from_dict(response.json())


def remove_request(uid):
    try:
        response = requests.delete(SERVER_URL + '/delete/{}'.format(uid))
    except requests.exceptions.ConnectionError:
        LOGGER.error('failed to connect to server %s', SERVER_URL)
        return

    return renderRequest.RenderRequest.from_dict(response.json())
