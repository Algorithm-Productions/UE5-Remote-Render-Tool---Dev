import os
from datetime import datetime

from util.StorableEntity import StorableEntity
from dotenv import load_dotenv

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.dirname(MODULE_PATH)

load_dotenv(os.path.join(MODULE_PATH, '../.env'))

DATABASE = os.path.join(ROOT_PATH, os.getenv("DATABASE_FOLDER") + os.getenv("NOTIFICATION_FOLDER"))


class NotificationType(object):
    ERROR = "ERROR"
    WARNING = "WARN"
    INFO = "INFO"
    CRITICAL = "CRITICAL"

    @classmethod
    def from_string(cls, string):
        if string == "ERROR":
            return NotificationType.ERROR
        elif string == "WARN":
            return NotificationType.WARNING
        elif string == "INFO":
            return NotificationType.INFO
        elif string == "CRITICAL":
            return NotificationType.CRITICAL
        else:
            return None

    @classmethod
    def to_string(cls, notificationType):
        if notificationType == NotificationType.ERROR:
            return "ERROR"
        elif notificationType == NotificationType.WARNING:
            return "WARNING"
        elif notificationType == NotificationType.INFO:
            return "INFO"
        elif notificationType == NotificationType.CRITICAL:
            return "CRITICAL"
        else:
            return ''

    @classmethod
    def getNumVal(cls, notificationType):
        if notificationType == NotificationType.ERROR:
            return 3
        elif notificationType == NotificationType.WARNING:
            return 2
        elif notificationType == NotificationType.INFO:
            return 1
        elif notificationType == NotificationType.CRITICAL:
            return 4
        else:
            return 0


class RenderLog(StorableEntity):
    DATABASE = DATABASE

    def __init__(
            self,
            uuid='',
            jobUUID='',
            timestamp=None,
            message='',
            log='',
            notificationType=None
    ):
        super().__init__(uuid)
        self.jobUUID = jobUUID or ''
        self.timestamp = timestamp or datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.message = message or ''
        self.log = log or ''
        self.notificationType = notificationType or NotificationType.INFO
        self.cleared = False

    @classmethod
    def from_dict(cls, data):
        uuid = data.get('uuid') or ''
        jobUUID = data.get('jobUUID') or ''
        timestamp = data.get('timestamp') or ''
        message = data.get('message') or ''
        log = data.get('log') or ''
        notificationType = NotificationType.from_string(data.get('notificationType')) or None

        return cls(
            uuid=uuid,
            jobUUID=jobUUID,
            timestamp=timestamp,
            message=message,
            log=log,
            notificationType=notificationType
        )

    def clear(self):
        self.cleared = True

    def __eq__(self, other):
        return self.notificationType == other.notificationType and self.timestamp == other.timestamp

    def __lt__(self, other):
        if self.notificationType == other.notificationType:
            return datetime.strptime(self.timestamp, "%m/%d/%Y, %H:%M:%S") > datetime.strptime(other.timestamp,
                                                                                               "%m/%d/%Y, %H:%M:%S")
        else:
            return NotificationType.getNumVal(self.notificationType) < NotificationType.getNumVal(
                other.notificationType)

    def __str__(self):
        return self.to_dict().__str__()
