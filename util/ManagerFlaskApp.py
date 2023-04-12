import datetime
import os
import platform
import uuid as genUUID

from flask import Flask

from util import RenderNotification

MANAGER_NAME = platform.node()


class ManagerFlaskApp(Flask):
    def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
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
