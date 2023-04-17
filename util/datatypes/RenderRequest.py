"""
    Copyright Algorithm Productions LLC. 2023.
"""

import os
from datetime import datetime, timedelta
import socket

from dotenv import load_dotenv

from util.datatypes.enums import RenderStatus
from util.datatypes.abstracts.StorableEntity import StorableEntity

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.dirname(MODULE_PATH)

load_dotenv(os.path.join(MODULE_PATH, '../../.env'))

DATABASE = os.path.join(ROOT_PATH, "../" + os.getenv("DATABASE_FOLDER"))


class RenderRequest(StorableEntity):
    """
        Entity Object Class to represent a Render Request in the System.

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
            name='',
            owner='',
            worker='',
            time_created='',
            priority=0,
            category='',
            tags=None,
            status='',
            project_path='',
            level_path='',
            sequence_path='',
            config_path='',
            output_path='',
            time_estimate='',
            estimated_finish='',
            progress=0
    ):
        """
            Class Constructor.
            Takes in every Parameter as an Optional, allowing for the creation of Empty Objects.

            :param uuid: Entity UUID.
            :type uuid: String.
            :param name: Name for the Render Request.
            :type name: String.
            :param owner: Name of the Machine who submitted the Request.
            :type owner: String.
            :param worker: Name of the Machine who rendered the Request.
            :type worker: String.
            :param time_created: Timestamp of when the Request was created.
            :type time_created: Datetime.
            :param priority: Render priority for the Job [UNIMPLEMENTED].
            :type priority: Integer.
            :param category: Job Category the Request falls into [UNIMPLEMENTED].
            :type category: String.
            :param tags: Tags to attach to the Request [UNIMPLEMENTED].
            :type tags: List of Strings.
            :param status: Current Status of the Request Job.
            :type status: RenderStatus.
            :param project_path: Path to the Project the Request refers to.
            :type project_path: String.
            :param level_path: In-Project Path to the Level the Request refers to.
            :type level_path: String.
            :param sequence_path: In-Project Path to the Sequence the Request refers to.
            :type sequence_path: String.
            :param config_path: In-Project Path to the UConfig the Request wants to use.
            :type config_path: String.
            :param output_path: Path to the Output Directory the Request wants to use.
            :type output_path: String.
            :param time_estimate: Current Time Estimate for the Request Job.
            :type time_estimate: String.
            :param estimated_finish: Current Estimated Finish for the Request Job.
            :type estimated_finish: Datetime.
            :param progress: Current Progress of the Request Job.
            :type progress: Integer.
        """
        super().__init__(uuid)
        self.name = name
        self.owner = owner or socket.gethostname()
        self.worker = worker
        self.time_created = time_created or datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.priority = priority or 0
        self.category = category
        self.tags = [] if tags is None else tags
        self.status = status or RenderStatus.RenderStatus.unassigned
        self.project_path = project_path
        self.level_path = level_path
        self.sequence_path = sequence_path
        self.config_path = config_path
        self.output_path = output_path
        self.time_estimate = time_estimate
        self.progress = progress
        self.estimated_finish = estimated_finish or ''
        self.calcFinish(estimated_finish)

    @classmethod
    def from_dict(cls, data):
        """
            @inheritDoc - StorableEntity
        """
        uuid = data.get('uuid') or ''
        name = data.get('name') or ''
        owner = data.get('owner') or ''
        worker = data.get('worker') or ''
        time_created = data.get('time_created') or ''
        priority = data.get('priority') or 0
        category = data.get('category') or ''
        tags = data.get('tags') or []
        status = data.get('status') or ''
        project_path = data.get('project_path')
        level_path = data.get('level_path') or ''
        sequence_path = data.get('sequence_path') or ''
        config_path = data.get('config_path') or ''
        output_path = data.get('output_path') or ''
        time_estimate = data.get('time_estimate') or ''
        estimated_finish = data.get('estimated_finish') or ''
        progress = data.get('progress') or 0

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
            time_estimate=time_estimate,
            estimated_finish=estimated_finish,
            progress=progress
        )

    def assign(self, worker):
        """
            Helper Method to assign a Worker to a Request.

            :param worker: Name of the Worker to Assign to the Request.
            :type worker: String.
            :return: None
        """
        self.update({"worker": worker})

    def calcFinish(self, defaultVal, ignoreDefault=False):
        """
            Helper Method to Calculate the current Estimated Finish Time.

            :param defaultVal: Default Value to use in case of an Error.
            :type defaultVal: String.
            :param ignoreDefault: Whether or not we should Default to the Default Value.
            :type ignoreDefault: Boolean.
            :return: None
        """
        value = ((not ignoreDefault) and defaultVal) or ''
        if self.time_estimate == 'N/A':
            value = 'N/A'
        elif self.time_estimate != '':
            start = datetime.now()
            end = datetime.strptime(self.time_estimate, '%Hh:%Mm:%Ss')
            delta = timedelta(hours=end.hour, minutes=end.minute, seconds=end.second, microseconds=end.microsecond)
            value = ((not ignoreDefault) and defaultVal) or (
                (start + delta).strftime("%m/%d/%Y, %H:%M:%S"))

        self.update({"estimated_finish": value})
