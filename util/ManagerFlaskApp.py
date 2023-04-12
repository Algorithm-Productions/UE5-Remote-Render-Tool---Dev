import datetime
import os
import platform
import uuid as genUUID

from flask import Flask

from util import RenderNotification

MANAGER_NAME = platform.node()

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.dirname(MODULE_PATH)
DATABASE = os.path.join(ROOT_PATH, os.getenv("DATABASE_FOLDER"))
ARCHIVE = os.path.join(ROOT_PATH, os.getenv("DATABASE_FOLDER") + os.getenv("ARCHIVE_FOLDER"))
NOTIFICATIONS = os.path.join(ROOT_PATH, os.getenv("DATABASE_FOLDER") + os.getenv("NOTIFICATION_FOLDER"))


def genFolders():
    if not os.path.exists(DATABASE):
        os.mkdir(DATABASE)
    if not os.path.exists(ARCHIVE):
        os.mkdir(ARCHIVE)
    if not os.path.exists(NOTIFICATIONS):
        os.mkdir(NOTIFICATIONS)


class ManagerFlaskApp(Flask):
    def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
        with self.app_context():
            genFolders()

        if not debug:
            with self.app_context():
                RenderNotification.RenderNotification(uuid=str(genUUID.uuid4())[:5], jobUUID='',
                                                      timestamp=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                                                      message='App Manager at {} is Starting!'.format(MANAGER_NAME),
                                                      log='App Manager at {} is Starting!'.format(MANAGER_NAME),
                                                      notificationType="INFO").write_json()

        try:
            super().run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)
        finally:
            if debug:
                RenderNotification.RenderNotification(uuid=str(genUUID.uuid4())[:5], jobUUID='',
                                                      timestamp=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                                                      message='App Manager at {} is Shutting Down!'.format(
                                                          MANAGER_NAME),
                                                      log='App Manager at {} is Shutting Down!'.format(MANAGER_NAME),
                                                      notificationType="CRITICAL").write_json()
