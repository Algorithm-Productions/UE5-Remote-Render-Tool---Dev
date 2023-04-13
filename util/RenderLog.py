import logging
import socket
import uuid as genUUID
import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

LOGGER = logging.getLogger(__name__)

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.dirname(MODULE_PATH)

load_dotenv(os.path.join(MODULE_PATH, '../.env'))

DATABASE = os.path.join(ROOT_PATH, os.getenv("DATABASE_FOLDER") + os.getenv("LOG_FOLDER"))


class LogType(object):
    ERROR = "ERROR"
    WARNING = "WARN"
    INFO = "INFO"
    CRITICAL = "CRITICAL"

    @classmethod
    def from_string(cls, string):
        if string == "ERROR":
            return LogType.ERROR
        elif string == "WARN":
            return LogType.WARNING
        elif string == "INFO":
            return LogType.INFO
        elif string == "CRITICAL":
            return LogType.CRITICAL
        else:
            return None

    @classmethod
    def to_string(cls, notificationType):
        if notificationType == LogType.ERROR:
            return "ERROR"
        elif notificationType == LogType.WARNING:
            return "WARNING"
        elif notificationType == LogType.INFO:
            return "INFO"
        elif notificationType == LogType.CRITICAL:
            return "CRITICAL"
        else:
            return ''

    @classmethod
    def getNumVal(cls, notificationType):
        if notificationType == LogType.ERROR:
            return 3
        elif notificationType == LogType.WARNING:
            return 2
        elif notificationType == LogType.INFO:
            return 1
        elif notificationType == LogType.CRITICAL:
            return 4
        else:
            return 0


class RenderLog(object):
    def __init__(
            self,
            uuid='',
            jobUUID='',
            timestamp=None,
            message='',
            log='',
            logType=None
    ):
        self.uuid = uuid or str(genUUID.uuid4())[:4]
        self.jobUUID = jobUUID or ''
        self.timestamp = timestamp or datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.message = message or ''
        self.log = log or ''
        self.logType = logType or LogType.INFO
        self.cleared = False

    def __eq__(self, other):
        return self.logType == other.notificationType and self.timestamp == other.timestamp

    def __lt__(self, other):
        if self.logType == other.notificationType:
            return datetime.strptime(self.timestamp, "%m/%d/%Y, %H:%M:%S") > datetime.strptime(other.timestamp,
                                                                                               "%m/%d/%Y, %H:%M:%S")
        else:
            return LogType.getNumVal(self.logType) < LogType.getNumVal(
                other.notificationType)

    def __str__(self):
        return self.to_dict().__str__()

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
        jobUUID = data.get('jobUUID') or ''
        timestamp = data.get('timestamp') or ''
        message = data.get('message') or ''
        log = data.get('log') or ''
        logType = LogType.from_string(data.get('notificationType')) or None

        return cls(
            uuid=uuid,
            jobUUID=jobUUID,
            timestamp=timestamp,
            message=message,
            log=log,
            logType=logType
        )

    def clear(self):
        self.cleared = True

    def to_dict(self):
        return self.__dict__

    def write_json(self):
        write_db(self.__dict__)

    def remove(self):
        remove_db(self.uuid)


def read_all():
    reqs = list()
    files = os.listdir(DATABASE)
    uuids = [os.path.splitext(os.path.basename(f))[0] for f in files if f.endswith('.json')]
    for uuid in uuids:
        req = RenderLog.from_db(uuid)
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
