"""
    Copyright Algorithm Productions LLC. 2023.
"""

from abc import ABC, abstractmethod


class UnrealDataType(ABC):
    """
        Abstract Class Representing any DataTypes that come from Unreal Libraries.

        :type: ABC.
        :author: vitor@bu.edu.
    """

    @classmethod
    @abstractmethod
    def from_unreal(cls, unrealClass):
        """
            Abstract Method to Extract a Data Object from its Unreal Class.

            :param unrealClass: Unreal Class Object to Extract from.
            :type unrealClass: unreal.Object.
            :return: Extracted Data Object.
            :type: Data Object.
        """
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data):
        """
            Abstract Method to Extract a Data Object from a Python Dictionary.

            :param data: Python Data Dictionary.
            :type data: Dictionary.
            :return: Extracted Data Object.
            :type: Data Object.
        """
        pass

    def to_dict(self):
        """
            Wrapper Method to help get the Dictionary Form of the Data Object.

            :return: Dictionary Form of the Data Object.
            :type: Dictionary.
        """
        return self.__dict__
