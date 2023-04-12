import atexit
import datetime
import logging
import os
import subprocess
import time
import platform
from dotenv import load_dotenv

from util import Client
from util import RenderRequest

logging.basicConfig(level=logging.INFO)
load_dotenv()
LOGGER = logging.getLogger(__name__)

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))

WORKER_NAME = platform.node()
UNREAL_EXE = os.getenv("UNREAL_EXE")


def render(uuid, project_path, level_path, sequence_path, config_path):
    command = [
        UNREAL_EXE,
        project_path,

        level_path,
        "-JobId={}".format(uuid),
        "-ProjectPath={}".format(project_path),
        "-LevelSequence={}".format(sequence_path),
        "-MoviePipelineConfig={}".format(config_path),

        "-game",
        "-MoviePipelineLocalExecutorClass=/Script/MovieRenderPipelineCore.MoviePipelinePythonHostExecutor",
        "-ExecutorPythonClass=/Engine/PythonTypes.RenderExecutor",

        "-windowed",
        "-resX=1280",
        "-resY=720",

        "-StdOut",
        "-FullStdOutLogOutput"
    ]
    env = os.environ.copy()
    env["UE_PYTHONPATH"] = MODULE_PATH
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env
    )
    return proc.communicate()


def sendExit():
    Client.send_notification('', ['', datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                                  'Worker {} Disconnecting from Farm'.format(WORKER_NAME),
                                  'Worker {} Disconnection from Farm'.format(WORKER_NAME),
                                  "WARN"])


if __name__ == '__main__':
    atexit.register(sendExit)
    LOGGER.info('Starting render worker %s', WORKER_NAME)
    Client.send_notification('', ['', datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                                  'Worker {} Connecting to Farm'.format(WORKER_NAME),
                                  'Worker {} Connecting to Farm'.format(WORKER_NAME),
                                  "INFO"])
    while True:
        reqs = Client.get_all_requests()
        uuids = [req.uuid for req in reqs
                 if req.worker == WORKER_NAME and
                 req.status == RenderRequest.RenderStatus.ready_to_start]

        for uuid in uuids:
            LOGGER.info('rendering job %s', uuid)

            req = RenderRequest.RenderRequest.from_db(uuid)
            output = render(
                uuid,
                req.project_path,
                req.level_path,
                req.sequence_path,
                req.config_path
            )

            LOGGER.info("finished rendering job %s", uuid)

        time.sleep(10)
        LOGGER.info('current job(s) finished, searching for new job(s)')
