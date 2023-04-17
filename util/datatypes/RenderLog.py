"""
    Copyright Algorithm Productions LLC. 2023.
"""

import os
from datetime import datetime

from util.datatypes.abstracts.StorableEntity import StorableEntity
from dotenv import load_dotenv

from util.datatypes.enums.LogType import LogType

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.dirname(MODULE_PATH)

load_dotenv(os.path.join(MODULE_PATH, '../../.env'))

DATABASE = os.path.join(ROOT_PATH, "../" + os.getenv("DATABASE_FOLDER") + os.getenv("LOG_FOLDER"))


class RenderLog(StorableEntity):
    """
        Entity Object Class to represent a Log Message for the Render System.

        :type: StorableEntity.
        :author: vitor@bu.edu.
    """

    """
        Update to Boilerplate Class Variable using the proper Database Path.
    """
    DATABASE = DATABASE

    def __init__(
            self,
            uuid='',
            jobUUID='',
            timestamp=None,
            message='',
            log='',
            logType=None,
            cleared=False
    ):
        """
            Class Constructor.
            Takes in every Parameter as an Optional, allowing for the creation of Empty Objects.

            :param uuid: Entity UUID.
            :type uuid: String.
            :param jobUUID: UUID of the Job the Log refers to.
            :type jobUUID: String.
            :param timestamp: Timestamp when the Log was Emitted.
            :type timestamp: Datetime.
            :param message: Shortened Log Message.
            :type message: String.
            :param log: Extended Log Message.
            :type log: String.
            :param logType: The type of Log this object is.
            :type logType: LogType.
        """
        super().__init__(uuid)
        self.jobUUID = jobUUID or ''
        self.timestamp = timestamp or datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.message = message or ''
        self.log = log or ''
        self.logType = logType or LogType.INFO
        self.cleared = cleared

    @classmethod
    def from_dict(cls, data):
        """
            @inheritDoc - StorableEntity
        """
        uuid = data.get('uuid') or ''
        jobUUID = data.get('jobUUID') or ''
        timestamp = data.get('timestamp') or ''
        message = data.get('message') or ''
        log = data.get('log') or ''
        logType = (data.get('logType').upper() if LogType.contains(data.get('logType').upper()) else '')
        cleared = data.get('cleared')

        return cls(
            uuid=uuid,
            jobUUID=jobUUID,
            timestamp=timestamp,
            message=message,
            log=log,
            logType=logType,
            cleared=cleared
        )

    def clear(self):
        """
            Helper Method to Clear the Log Notification.

            :return: None
        """
        self.update({"cleared": True})

    def __eq__(self, other):
        """
            Helper Method to assert whether a Log equals another in terms of Priority.
            Uses logType and timestamp Fields.

            :param other: Other Log to Compare to.
            :type other: RenderLog.
            :return: Whether or not the two Logs are Equal.
            :type: Boolean.
        """
        return self.logType == other.logType and self.timestamp == other.timestamp

    def __lt__(self, other):
        """
            Helper Method to assert whether a Log has higher priority then another.
            Uses logType and timestamp Fields.

            :param other: Other Log to Compare to.
            :type other: RenderLog.
            :return: Which log has higher priority (0 for Equal, >0 for Higher Priority, <0 for Lower Priority).
            :type: Integer.
        """
        if self.logType == other.logType:
            return datetime.strptime(self.timestamp, "%m/%d/%Y, %H:%M:%S") > datetime.strptime(other.timestamp,
                                                                                               "%m/%d/%Y, %H:%M:%S")
        else:
            return LogType.getNumVal(self.logType) < LogType.getNumVal(
                other.notificationType)
