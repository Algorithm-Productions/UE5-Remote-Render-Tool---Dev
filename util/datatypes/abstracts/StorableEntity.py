"""
    Copyright Algorithm Productions LLC. 2023.
"""

import json
import logging
import os
import uuid as genUUID
from abc import ABC, abstractmethod

LOGGER = logging.getLogger(__name__)


class StorableEntity(ABC):
    """
        Abstract Class Representing a Storable Entity in the Manager's Database.

        :type: ABC.
        :author: vitor@bu.edu.
    """

    """
        Boilerplate Class Variable to store the Path on the DB for any Entity Objects.
    """
    DATABASE = ''

    def __init__(self, uuid):
        """
            Class Constructor. Sets Entity UUID.

            :param uuid: UUID for the Entity to Create.
            :type uuid: String
        """
        self.uuid = uuid or str(genUUID.uuid4())[:4]

    @classmethod
    @abstractmethod
    def from_dict(cls, data):
        """
            Abstract Method to Extract an Entity Object from a Python Dictionary.

            :param data: Python Data Dictionary.
            :type data: Dictionary.
            :return: Extracted Entity Object.
            :type: Entity Object.
        """
        pass

    @classmethod
    def write_db(cls, data):
        """
            Class Method to Save an Entity Object (in Dictionary Form) into its Database.

            :param data: Dictionary Form of the Entity Object to Save.
            :type data: Dictionary.
            :return: None.
        """
        uuid = data['uuid']
        LOGGER.info('writing to %s', uuid)
        with open(os.path.join(cls.DATABASE, '{}.json'.format(uuid)), 'w') as fp:
            json.dump(data, fp, indent=4)

    @classmethod
    def read_all(cls):
        """
            Class Method to Fetch every Entity Object from the Manager's Database.

            :return: List of Entity Objects found in the Database.
            :type: List of Entity Objects.
        """
        reqs = list()
        files = os.listdir(cls.DATABASE)
        uuids = [os.path.splitext(os.path.basename(f))[0] for f in files if f.endswith('.json')]
        for uuid in uuids:
            req = cls.read(uuid)
            reqs.append(req)

        return reqs

    @classmethod
    def read(cls, uuid):
        """
            Class Method to Fetch a single Entity Object from the Manager's Database.

            :param uuid: UUID of the Object to Fetch.
            :type uuid: String.
            :return: Fetched Entity Object.
            :type: Entity Object.
        """
        request_file = os.path.join(cls.DATABASE, '{}.json'.format(uuid))
        with open(request_file, 'r') as fp:
            try:
                request_dict = json.load(fp)
            except Exception as e:
                LOGGER.error('Failed to load request object from db: %s', e)
                return None
        return cls.from_dict(request_dict)

    @classmethod
    def remove_all(cls):
        """
            Class Method to Delete every Entity Object from the Manager's Database.

            :return: None.
        """
        files = os.path.join(cls.DATABASE, '*.json')
        for file in files:
            os.remove(file)

    @classmethod
    def remove(cls, uuid):
        """
            Class Method to Delete a single Entity Object from the Manager's Database.

            :param uuid: UUID of the Object to Delete.
            :type uuid: String.
            :return: None.
        """
        os.remove(os.path.join(cls.DATABASE, '{}.json'.format(uuid)))

    def __str__(self):
        """
            Override of the Default __str__ Method to provide a more readable Output.

            :return: Stringified Dictionary form of the Storable Entity.
            :type: String.
        """
        return self.to_dict().__str__()

    def to_dict(self):
        """
            Wrapper Method to help get the Dictionary Form of the Entity Object.

            :return: Dictionary Form of the Entity Object.
            :type: Dictionary.
        """
        return self.__dict__

    def save_self(self):
        """
            Helper Method to Save the Entity Object onto the Manager's Database.

            :return: None.
        """
        self.__class__.write_db(self.to_dict())

    def remove_self(self):
        """
            Helper Method to Remove the Entity Object from the Manager's Database

            :return: None.
        """
        self.__class__.remove(self.uuid)

    def update(self, data):
        """
            Helper Method to Update the contents of the Entity Object.
            Note: Updates both the Live Object, and the Stored Version.

            :param data: Dictionary with Updated Data.
            :type data: Dictionary.
            :return: None.
        """
        selfDict = self.to_dict()

        for key, item in data.items():
            if key in selfDict.keys():
                selfDict[key] = item

        self.__class__.write_db(selfDict)
