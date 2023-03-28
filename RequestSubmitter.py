import logging

from util import client

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def send(data):
    req = client.add_request(data)
    if req:
        LOGGER.info('request %s sent to server', req.uid)


if __name__ == '__main__':
    test_job_a = {
        'name': 'street_seq01',
        'owner': 'TEST_SUBMITTER_01',
        'umap_path': '/Game/Maps/ArchVis_Lightmap',
        'useq_path': '/Game/Cinematic/archviz_cine_shot0030',
        'uconfig_path': '/Config/TestConfig'
    }

    test_job_b = {
        'name': 'street_seq02',
        'owner': 'TEST_SUBMITTER_01',
        'umap_path': '/Game/Maps/ArchVis_Lightmap',
        'useq_path': '/Game/Cinematic/archviz_cine_shot0040',
        'uconfig_path': '/Config/TestConfig1'
    }

    for job in [test_job_a, test_job_b]:
        send(job)
