import datetime
import os
import platform
import uuid as genUUID

from flask import Flask

from util.datatypes import RenderLog

MANAGER_NAME = platform.node()

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.dirname(MODULE_PATH)
DATABASE = os.path.join(ROOT_PATH, os.getenv("DATABASE_FOLDER"))
ARCHIVE = os.path.join(ROOT_PATH, os.getenv("DATABASE_FOLDER") + os.getenv("ARCHIVE_FOLDER"))
LOGS = os.path.join(ROOT_PATH, os.getenv("DATABASE_FOLDER") + os.getenv("LOG_FOLDER"))


def genFolders():
    if not os.path.exists(DATABASE):
        os.mkdir(DATABASE)
    if not os.path.exists(ARCHIVE):
        os.mkdir(ARCHIVE)
    if not os.path.exists(LOGS):
        os.mkdir(LOGS)


class ManagerFlaskApp(Flask):
    WORKERS = []

    def add_worker(self, worker):
        if worker not in self.WORKERS:
            self.WORKERS.append(worker)
            return "Added Worker"
        else:
            return "Worker Already Active"

    def remove_worker(self, worker):
        if worker in self.WORKERS:
            self.WORKERS.remove(worker)
            return "Removed Worker"
        else:
            return "Worker Not Active"

    def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
        with self.app_context():
            genFolders()

        if not debug:
            with self.app_context():
                RenderLog.RenderLog(uuid=str(genUUID.uuid4())[:5], jobUUID='',
                                    timestamp=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                                    message='App Manager at {} is Starting!'.format(MANAGER_NAME),
                                    log='App Manager at {} is Starting!'.format(MANAGER_NAME),
                                    logType="INFO").save_self()

        try:
            super().run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)
        finally:
            if not debug:
                RenderLog.RenderLog(uuid=str(genUUID.uuid4())[:5], jobUUID='',
                                    timestamp=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                                    message='App Manager at {} is Shutting Down!'.format(
                                        MANAGER_NAME),
                                    log='App Manager at {} is Shutting Down!'.format(MANAGER_NAME),
                                    logType="CRITICAL").save_self()
