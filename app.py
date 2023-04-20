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

NODE_NAME = platform.node()
SERVER_URL = os.getenv('SERVER_URL')
SERVER_PORT = os.getenv('SERVER_PORT')
SERVER_DATABASE = os.getenv('DATABASE_FOLDER')
AUTHENTICATION_TOKEN = os.getenv('AUTHENTICATION_TOKEN')
DEBUG = args.debug or os.getenv('DEBUG', False)

from remote_render import app, __version__

print(f'Running UE5 Remote Render Tool [v{__version__}]: '
      f'mode={args.mode} '
      f'node={NODE_NAME} '
      f'host={SERVER_URL} '
      f'port={SERVER_PORT} '
      f'auth_token={AUTHENTICATION_TOKEN} '
      f'debug={DEBUG}')

try:
    if args.mode == 'manager':

        app.run(host=SERVER_URL,
                port=SERVER_PORT,
                database_path=SERVER_DATABASE,
                debug=DEBUG)

    elif args.mode == 'submitter':
        submitter_path = os.path.abspath('./remote_render/submitter/GUISubmitter.py')
        subprocess.call(['python', submitter_path, '--server_host', SERVER_URL, '--server_port', SERVER_PORT,
                          '--auth_token',  AUTHENTICATION_TOKEN], shell=True)

    elif args.mode == 'worker':
        #TODO: This
        submitter_path = os.path.abspath('./remote_render/worker/GUIWorker.py')
        subprocess.call(['python', submitter_path, '--server_host', SERVER_URL, '--server_port', SERVER_PORT,
                          '--auth_token',  AUTHENTICATION_TOKEN], shell=True)

except KeyboardInterrupt:
    print('Keyboard interrupt')
finally:
    print(f'Shutting down UE5 Remote Render Tool [v{__version__}]')

