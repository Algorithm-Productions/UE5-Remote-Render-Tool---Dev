import datetime
import os
import platform
import uuid as genUUID
from flask import Flask
from remote_render.util.datatypes import RenderLog

MANAGER_NAME = platform.node()

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.dirname(MODULE_PATH)
DATABASE = os.getenv("DATABASE_FOLDER")
ARCHIVE = os.getenv("DATABASE_FOLDER") + os.getenv("ARCHIVE_FOLDER")
LOGS = os.getenv("DATABASE_FOLDER") + os.getenv("LOG_FOLDER")


def genFolders():
    if not os.path.exists(DATABASE):
        os.mkdir(DATABASE)
    if not os.path.exists(ARCHIVE):
        os.mkdir(ARCHIVE)
    if not os.path.exists(LOGS):
        os.mkdir(LOGS)


class ManagerFlaskApp(Flask):
    def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
        with self.app_context():
            print('Generating app folders')
            genFolders()

        if not debug:
            with self.app_context():
                RenderLog(uuid=str(genUUID.uuid4())[:5],
                          jobUUID='',
                          timestamp=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                          message='App Manager at {} is Starting!'.format(MANAGER_NAME),
                          log='App Manager at {} is Starting!'.format(MANAGER_NAME),
                          logType="INFO").save_self()

        try:
            print('Running flask non-debug')
            super().run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)
        finally:
            if not debug:
                RenderLog(uuid=str(genUUID.uuid4())[:5],
                          jobUUID='',
                          timestamp=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                          message='App Manager at {} is Shutting Down!'.format(MANAGER_NAME),
                          log='App Manager at {} is Shutting Down!'.format(MANAGER_NAME),
                          logType="CRITICAL").save_self()
