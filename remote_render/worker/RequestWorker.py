import atexit
import datetime
import logging
import os
import subprocess
import time
import platform
from dotenv import load_dotenv

from remote_render.util import Client
from remote_render.util.datatypes import RenderRequest
from remote_render.util.datatypes.enums import RenderStatus

logging.basicConfig(level=logging.INFO)
load_dotenv()
LOGGER = logging.getLogger(__name__)

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))

WORKER_NAME = platform.node()
UNREAL_EXE = os.getenv("UNREAL_EXE")


def render(uuid, project_path, level_path, sequence_path, config_path, config_override, render_settings):
    command = [
        UNREAL_EXE,
        project_path,

        level_path,
        "-JobId={}".format(uuid),
        "-ProjectPath={}".format(project_path),
        "-LevelSequence={}".format(sequence_path),
        "-MoviePipelineConfig={}".format(config_path),
        "-ConfigOverride={}".format(config_override),
        "-RenderSettings={}".format(render_settings),

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
    Client.delete_worker(WORKER_NAME)


if __name__ == '__main__':
    atexit.register(sendExit)
    LOGGER.info('Starting render worker %s', WORKER_NAME)
    Client.add_worker(WORKER_NAME)

    while True:
        reqs = Client.get_all_requests()
        uuids = [req.uuid for req in reqs
                 if req.worker == WORKER_NAME and
                 req.status == RenderStatus.ready_to_start]

        for uuid in uuids:
            LOGGER.info('rendering job %s', uuid)

            req = RenderRequest.read(uuid)
            output = render(
                uuid,
                req.project_path,
                req.level_path,
                req.sequence_path,
                req.config_path,
                req.config_override.to_dict(),
                req.render_settings.to_dict()
            )

            LOGGER.info("finished rendering job %s", uuid)

        time.sleep(10)
        LOGGER.info('current job(s) finished, searching for new job(s)')
