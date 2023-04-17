import datetime
import os
import platform
import uuid as genUUID
from flask import Flask
from remote_render.util.datatypes import RenderLog

MANAGER_NAME = platform.node()

class ManagerFlaskApp(Flask):

    def run(self, host, port, database_path, debug=False, load_dotenv=True, **options):

        self.check_database(database_path)

        if not debug:
            self.emit_start_log()
        try:
            super().run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)
        finally:
            if not debug:
                self.emit_shutdown_log()

    def check_database(self, database_path):

        with self.app_context():
            os.makedirs(database_path, exist_ok=True)
            os.makedirs(os.path.join(database_path, 'archive'), exist_ok=True)
            os.makedirs(os.path.join(database_path, 'logs'), exist_ok=True)

    def emit_start_log(self):
        with self.app_context():
            RenderLog(uuid=str(genUUID.uuid4())[:5],
                      jobUUID='',
                      timestamp=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                      message='App Manager at {} is Starting!'.format(MANAGER_NAME),
                      log='App Manager at {} is Starting!'.format(MANAGER_NAME),
                      logType="INFO").save_self()


    def emit_shutdown_log(self):
        with self.app_context():
            RenderLog(uuid=str(genUUID.uuid4())[:5],
                      jobUUID='',
                      timestamp=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                      message='App Manager at {} is Shutting Down!'.format(MANAGER_NAME),
                      log='App Manager at {} is Shutting Down!'.format(MANAGER_NAME),
                      logType="CRITICAL").save_self()
