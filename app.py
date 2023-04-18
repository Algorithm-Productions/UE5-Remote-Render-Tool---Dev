import logging
import platform
import os
import argparse
from dotenv import load_dotenv
import subprocess

LOGGER = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--mode', type=str, choices=['manager', 'worker', 'submitter'], default='manager',
                    help='Run app as manager, worker or submitter.')
parser.add_argument('-e', '--env', type=str, required=False, help='Path to env file. Default=.env')
parser.add_argument('-d', '--debug', action='store_true', help='Run in debug mode')
args = parser.parse_args()

if args.env:
    load_dotenv(args.env)
else:
    load_dotenv()

MANAGER_NAME = platform.node()
SERVER_URL = os.getenv('SERVER_URL')
SERVER_PORT = os.getenv('SERVER_PORT')
SERVER_DATABASE = os.getenv('DATABASE_FOLDER')
DEBUG = args.debug or os.getenv('DEBUG', False)

from remote_render import app, __version__

if args.mode == 'manager':

    try:
        print(f'Running UE5 Remote Render Tool Manager [v{__version__}]: '
              f'host={SERVER_URL} '
              f'port={SERVER_PORT} '
              f'manager={MANAGER_NAME} '
              f'debug={DEBUG}')

        app.run(host=SERVER_URL,
                port=SERVER_PORT,
                database_path=SERVER_DATABASE,
                debug=DEBUG)
    finally:
        print(f'Shutting down UE5 Remote Render Tool Manager [v{__version__}]')

elif args.mode == 'submitter':


    try:
        print(f'Running UE5 Remote Render Tool Submitter [v{__version__}]: ')
        subprocess.run('python3',
                       './remote_render/submitter/GUISubmitter.py',
                       f'--server_host {SERVER_URL}',
                       f'--server_port {SERVER_PORT}',
                       f'--authentication_token {AUTHENTICATION_TOKEN}',

                       )
    finally:

        print(f'Shutting down UE5 Remote Render Tool [v{__version__}]')

