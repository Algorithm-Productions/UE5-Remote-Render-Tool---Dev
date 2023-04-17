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

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
HTML_FOLDER = os.path.join(MODULE_PATH, 'html')

LOGGER = logging.getLogger(__name__)
DEFAULT_WORKER = os.getenv("DEFAULT_WORKER")

ROOT_PATH = os.path.dirname(MODULE_PATH)
DATABASE = os.path.join(ROOT_PATH, os.getenv("DATABASE_FOLDER"))
ARCHIVE = os.path.join(ROOT_PATH, os.getenv("DATABASE_FOLDER") + os.getenv("ARCHIVE_FOLDER"))
LOGS = os.path.join(ROOT_PATH, os.getenv("DATABASE_FOLDER") + os.getenv("LOG_FOLDER"))

FLASK_EXE = os.getenv("FLASK_EXE")

MANAGER_NAME = platform.node()
SERVER_URL = os.getenv('SERVER_URL')
SERVER_PORT = os.getenv('SERVER_PORT')

API_EXT = os.getenv("API_EXT")
ARCHIVE_API_EXT = os.getenv("ARCHIVE_API_EXT")
LOG_API_EXT = os.getenv("LOG_API_EXT")

from remote_render import app, __version__


try:
    print(f'Running UE5 Remote Render Tool host={SERVER_URL} port={SERVER_PORT} debug={args.debug} version={__version__}')
    app.run(host=SERVER_URL,
            port=SERVER_PORT,
            debug=args.debug)

except KeyboardInterrupt:
    print('Shutting down app')
finally:
    print('App closed')

