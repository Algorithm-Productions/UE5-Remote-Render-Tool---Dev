import logging
import socket
import uuid as genUUID
import os
import json
from datetime import datetime


LOGGER = logging.getLogger(__name__)

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.dirname(MODULE_PATH)
DATABASE = os.path.join(ROOT_PATH, 'database')


class RenderStatus(object):
    unassigned = 'un-assigned'
    ready_to_start = 'ready to start'
    in_progress = 'in progress'
    finished = 'finished'
    errored = 'errored'
    cancelled = 'cancelled'
    paused = 'paused'


class RenderRequest(object):
    def __init__(
            self,
            uuid='',
            name='',
            owner='',
            worker='',
            time_created='',
            priority=0,
            category='',
            tags=[],
            status='',
            project_path='',
            level_path='',
            sequence_path='',
            config_path='',
            output_path='',
            width=0,
            height=0,
            frame_rate=0,
            format='',
            start_frame=0,
            end_frame=0,
            time_estimate='',
            progress=0
    ):
        self.uuid = uuid or str(genUUID.uuid4())[:4]
        self.name = name
        self.owner = owner or socket.gethostname()
        self.worker = worker
        self.time_created = time_created or datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.priority = priority or 0
        self.category = category
        self.tags = tags
        self.status = status or RenderStatus.unassigned
        self.project_path = project_path
        self.level_path = level_path
        self.sequence_path = sequence_path
        self.config_path = config_path
        self.output_path = output_path
        self.width = width or 1280
        self.height = height or 720
        self.frame_rate = frame_rate or 30
        self.format = format or 'JPG'
        self.start_frame = start_frame or 0
        self.end_frame = end_frame or 0
        self.length = self.end_frame - self.start_frame
        self.time_estimate = time_estimate
        self.progress = progress

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
    def from_dict(cls, d):
        uuid = d.get('uuid') or ''
        name = d.get('name') or ''
        owner = d.get('owner') or ''
        worker = d.get('worker') or ''
        time_created = d.get('time_created') or ''
        priority = d.get('priority') or 0
        category = d.get('category') or ''
        tags = d.get('tags') or []
        status = d.get('status') or ''
        project_path = d.get('project_path')
        level_path = d.get('level_path') or ''
        sequence_path = d.get('sequence_path') or ''
        config_path = d.get('config_path') or ''
        output_path = d.get('output_path') or ''
        width = d.get('width') or 0
        height = d.get('height') or 0
        frame_rate = d.get('frame_rate') or 0
        format = d.get('format') or ''
        start_frame = d.get('start_frame') or 0
        end_frame = d.get('end_frame') or 0
        time_estimate = d.get('time_estimate') or ''
        progress = d.get('progress') or 0

        return cls(
            uuid=uuid,
            name=name,
            owner=owner,
            worker=worker,
            time_created=time_created,
            priority=priority,
            category=category,
            tags=tags,
            status=status,
            project_path=project_path,
            level_path=level_path,
            sequence_path=sequence_path,
            config_path=config_path,
            output_path=output_path,
            width=width,
            height=height,
            frame_rate=frame_rate,
            format=format,
            start_frame=start_frame,
            end_frame=end_frame,
            time_estimate=time_estimate,
            progress=progress
        )

    def to_dict(self):
        return self.__dict__

    def write_json(self):
        write_db(self.__dict__)

    def remove(self):
        remove_db(self.uuid)

    def update(self, progress=0, status='', time_estimate=''):
        if progress:
            self.progress = progress
        if status:
            self.status = status
        if time_estimate:
            self.time_estimate = time_estimate

        write_db(self.__dict__)

    def assign(self, worker):
        self.worker = worker

        write_db(self.__dict__)

def read_all():
    rrequests = list()
    files = os.listdir(DATABASE)
    uuids = [os.path.splitext(os.path.basename(f))[0] for f in files if f.endswith('.json')]
    for uuid in uuids:
        rrequest = RenderRequest.from_db(uuid)
        rrequests.append(rrequest)

    return rrequests


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
