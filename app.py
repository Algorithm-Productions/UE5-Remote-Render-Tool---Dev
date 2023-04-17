import logging
import platform
import os
import argparse
from dotenv import load_dotenv

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--mode', type=str, choices=['manager', 'worker'], help='Run app as manager or worker.')
parser.add_argument('-e', '--env', type=str, required=False, help='Path to env file. Default=.env')
parser.add_argument('-d', '--debug', action='store_true', help='Run in debug mode')
args = parser.parse_args()

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

from remote_render import app, __version__

try:

    print(f'Running UE5 Remote Render Tool: '
          f'host={SERVER_URL} port={SERVER_PORT} manager={MANAGER_NAME} debug={DEBUG} version={__version__}')

    app.run(host=SERVER_URL,
            port=SERVER_PORT,
            database_path=SERVER_DATABASE,
            debug=DEBUG)
finally:
    print('App closed')

