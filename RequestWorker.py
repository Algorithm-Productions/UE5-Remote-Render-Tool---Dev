import logging
import os
import subprocess
import time

from util import Client
from util import RenderRequest


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))

WORKER_NAME = 'RENDER_MACHINE_01'
UNREAL_EXE = r'C:\Program Files\Epic Games\UE_5.0\Engine\Binaries\Win64\UnrealEditor.exe'


def render(uuid, project_path, level_path, sequence_path, config_path):
    command = [
        UNREAL_EXE,
        project_path,

        level_path,
        "-JobId={}".format(uuid),
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


if __name__ == '__main__':
    LOGGER.info('Starting render worker %s', WORKER_NAME)
    while True:
        rrequests = Client.get_all_requests()
        uuids = [rrequest.uuid for rrequest in rrequests
                if rrequest.worker == WORKER_NAME and
                rrequest.status == RenderRequest.RenderStatus.ready_to_start]

        for uuid in uuids:
            LOGGER.info('rendering job %s', uuid)

            rrequest = RenderRequest.RenderRequest.from_db(uuid)
            output = render(
                uuid,
                rrequest.project_path,
                rrequest.level_path,
                rrequest.sequence_path,
                rrequest.config_path
            )

            LOGGER.info("finished rendering job %s", uuid)

        time.sleep(10)
        LOGGER.info('current job(s) finished, searching for new job(s)')
