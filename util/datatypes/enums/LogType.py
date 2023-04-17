"""
    Copyright Algorithm Productions LLC. 2023.
"""

from util.datatypes.abstracts.EnumProperty import EnumProperty


class LogType(EnumProperty):
    """
        Enum Class to Represent all Types of Log Messages.

        :type: Enum.
        :author: vitor@bu.edu.
    """
    ERROR = "ERROR"
    WARNING = "WARN"
    INFO = "INFO"
    CRITICAL = "CRITICAL"

    @classmethod
    def contains(cls, item):
        return item in [cls.ERROR, cls.WARNING, cls.INFO, cls.CRITICAL]

    @classmethod
    def getNumVal(cls, logType):
        """
            Get a Numeric Value for each of the Enum Values.
            Used for Sorting.

            :param logType: Enum Value.
            :type logType: LogType.
            :return: Numerical Value for the Enum.
            :type: Integer.
        """
        if logType == LogType.ERROR:
            return 3
        elif logType == LogType.WARNING:
            return 2
        elif logType == LogType.INFO:
            return 1
        elif logType == LogType.CRITICAL:
            return 4
        else:
            return 0
