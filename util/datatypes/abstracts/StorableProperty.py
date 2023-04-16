"""
    Copyright Algorithm Productions LLC. 2023.
"""

from abc import ABC, abstractmethod


class StorableProperty(ABC):
    """
        Abstract Class Representing a Property of en Entity Object in the Manager's Database.

        :type: ABC.
        :author: vitor@bu.edu.
    """

    @classmethod
    @abstractmethod
    def from_dict(cls, data):
        """
            Abstract Method to Extract a Property Object from a Python Dictionary.

            :param data: Python Data Dictionary.
            :type data: Dictionary.
            :return: Extracted Property Object.
            :type: Property Object.
        """
        pass

    def to_dict(self):
        """
            Wrapper Method to help get the Dictionary Form of the Property Object.

            :return: Dictionary Form of the Property Object.
            :type: Dictionary.
        """
        return self.__dict__
