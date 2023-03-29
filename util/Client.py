import logging
import requests

from . import RenderRequest


LOGGER = logging.getLogger(__name__)

SERVER_URL = 'http://127.0.0.1:5000'
SERVER_API_URL = SERVER_URL + '/api'


def get_all_requests():
    try:
        response = requests.get(SERVER_API_URL+'/get')
    except requests.exceptions.ConnectionError:
        LOGGER.error('failed to connect to server %s', SERVER_API_URL)
        return

    results = response.json()['results']
    return [RenderRequest.RenderRequest.from_dict(result) for result in results]


def get_request(uuid):
    try:
        response = requests.get(SERVER_API_URL+'/get/{}'.format(uuid))
    except requests.exceptions.ConnectionError:
        LOGGER.error('failed to connect to server %s', SERVER_API_URL)
        return

    return RenderRequest.RenderRequest.from_dict(response.json())


def add_request(data):
    try:
        response = requests.post(SERVER_API_URL+'/post', json=data)
    except requests.exceptions.ConnectionError:
        LOGGER.error('failed to connect to server %s', SERVER_API_URL)
        return
    
    return RenderRequest.RenderRequest.from_dict(response.json())


def remove_request(uuid):
    try:
        response = requests.delete(SERVER_API_URL+'/delete/{}'.format(uuid))
    except requests.exceptions.ConnectionError:
        LOGGER.error('failed to connect to server %s', SERVER_API_URL)
        return
    
    return RenderRequest.RenderRequest.from_dict(response.json())


def update_request(uuid, params):
    try:
        response = requests.put(
            SERVER_API_URL+'/put/{}'.format(uuid),
            params
        )
    except requests.exceptions.ConnectionError:
        LOGGER.error('failed to connect to server %s', SERVER_API_URL)
        return

    return RenderRequest.RenderRequest.from_dict(response.json())
