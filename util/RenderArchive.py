import logging
import os
import json
from dotenv import load_dotenv

from util.RenderRequest import RenderRequest

LOGGER = logging.getLogger(__name__)

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.dirname(MODULE_PATH)

load_dotenv(os.path.join(MODULE_PATH, '../.env'))

DATABASE = os.path.join(ROOT_PATH, os.getenv("DATABASE_FOLDER") + os.getenv("ARCHIVE_FOLDER"))


class HardwareStats(object):
    def __init__(
            self,
            name='',
            cpu='',
            gpu='',
            ram='',
            vram=''
    ):
        self.name = name
        self.cpu = cpu
        self.gpu = gpu
        self.ram = ram
        self.vram = vram

    @classmethod
    def from_dict(cls, data):
        name = data.get('name') or ''
        cpu = data.get('cpu') or ''
        gpu = data.get('gpu') or ''
        ram = data.get('ram') or ''
        vram = data.get('vram') or ''

        return cls(
            name=name,
            cpu=cpu,
            gpu=gpu,
            ram=ram,
            vram=vram
        )

    def to_dict(self):
        return self.__dict__


class RenderArchive(object):
    def __init__(
            self,
            uuid='',
            renderRequest=None,
            hardwareStats=None,
            totalTime='',
            finishTime='',
            avgFrame=0,
            frameMap=None,
            perFrameSamples=0,
            resolution=''
    ):
        if not frameMap:
            frameMap = []

        self.uuid = uuid or renderRequest.uuid
        self.renderRequest = renderRequest
        self.hardwareStats = hardwareStats
        self.totalTime = totalTime
        self.finishTime = finishTime
        self.avgFrame = avgFrame
        self.frameMap = frameMap
        self.perFrameSamples = perFrameSamples
        self.resolution = resolution

    @classmethod
    def from_db(cls, uuid):
        request_file = os.path.join(DATABASE, '{}.json'.format(uuid))
        with open(request_file, 'r') as fp:
            try:
                request_dict = json.load(fp)
            except Exception as e:
                LOGGER.error('Failed to load request object from db: %s', e)
                return None
        return cls.from_dict(request_dict)

    @classmethod
    def from_dict(cls, data):
        uuid = data.get('uuid') or ''
        totalTime = data.get('totalTime') or ''
        finishTime = data.get('finishTime') or ''
        avgFrame = data.get('avgFrame') or ''
        frameMap = data.get('frameMap') or ''
        perFrameSamples = data.get('perFrameSamples') or ''
        resolution = data.get('resolution') or ''

        renderRequest = RenderRequest.from_dict(data.get('renderRequest'))
        hardwareStats = HardwareStats.from_dict(data.get('hardwareStats'))

        return cls(
            uuid=uuid,
            renderRequest=renderRequest,
            hardwareStats=hardwareStats,
            totalTime=totalTime,
            finishTime=finishTime,
            avgFrame=avgFrame,
            frameMap=frameMap,
            perFrameSamples=perFrameSamples,
            resolution=resolution
        )

    def copy(self):
        return RenderArchive(
            uuid=self.uuid,
            renderRequest=self.renderRequest,
            hardwareStats=self.hardwareStats,
            totalTime=self.totalTime,
            finishTime=self.finishTime,
            avgFrame=self.avgFrame,
            frameMap=self.frameMap,
            perFrameSamples=self.perFrameSamples,
            resolution=self.resolution
        )

    def to_dict(self):
        copy = self.copy()
        if self.renderRequest:
            copy.renderRequest = self.renderRequest.to_dict()
        if copy.hardwareStats:
            copy.hardwareStats = self.hardwareStats.to_dict()
        return copy.__dict__

    def write_json(self):
        write_db(self.to_dict())

    def remove(self):
        remove_db(self.uuid)


def read_all():
    reqs = list()
    files = os.listdir(DATABASE)
    uuids = [os.path.splitext(os.path.basename(f))[0] for f in files if f.endswith('.json')]
    for uuid in uuids:
        req = RenderRequest.from_db(uuid)
        reqs.append(req)

    return reqs


def remove_db(uuid):
    os.remove(os.path.join(DATABASE, '{}.json'.format(uuid)))


def remove_all():
    files = os.path.join(DATABASE, '*.json')
    for file in files:
        os.remove(file)


def write_db(d):
    uuid = d['uuid']
    LOGGER.info('writing to %s', uuid)
    with open(os.path.join(DATABASE, '{}.json'.format(uuid)), 'w') as fp:
        json.dump(d, fp, indent=4)
