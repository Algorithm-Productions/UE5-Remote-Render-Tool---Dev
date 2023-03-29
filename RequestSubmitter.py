import logging

from util import Client

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def send(data):
    req = Client.add_request(data)
    if req:
        LOGGER.info('request %s sent to server', req.uuid)


if __name__ == '__main__':
    test_job_a = {
        'name': 'street_seq01',
        'owner': 'TEST_SUBMITTER_01',
        'project_path': r'C:\Users\Cinema_4D\Documents\Unreal Projects\ArchVizInterior 5.0\ArchVizInterior.uproject',
        'level_path': '/Game/Maps/ArchVis_Lightmap',
        'sequence_path': '/Game/Cinematic/archviz_cine_shot0030',
        'config_path': '/Game/Cinematic/TestConfig'
    }

    test_job_b = {
        'name': 'street_seq02',
        'owner': 'TEST_SUBMITTER_01',
        'project_path': r'C:\Users\Cinema_4D\Documents\Unreal Projects\ArchVizInterior 5.0\ArchVizInterior.uproject',
        'level_path': '/Game/Maps/ArchVis_Lightmap',
        'sequence_path': '/Game/Cinematic/archviz_cine_shot0040',
        'config_path': '/Game/Cinematic/TestConfig1'
    }

    for job in [test_job_a, test_job_b]:
        send(job)
