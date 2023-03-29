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
UNREAL_PROJECT = r"C:\Users\Cinema_4D\Documents\Unreal Projects\ArchVizInterior 5.0\ArchVizInterior.uproject"


def render(uuid, projectPath, levelPath, sequencePath, configPath):
    command = [
        UNREAL_EXE,
        projectPath,

        levelPath,
        "-JobId={}".format(uuid),
        "-LevelSequence={}".format(sequencePath),
        "-MoviePipelineConfig={}".format(configPath),

        "-game",
        "-MoviePipelineLocalExecutorClass=/Script/MovieRenderPipelineCore.MoviePipelinePythonHostExecutor",
        "-ExecutorPythonClass=/Engine/PythonTypes.RequestExecutor",

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
