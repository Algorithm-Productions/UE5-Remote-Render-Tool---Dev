"""
    Copyright Algorithm Productions LLC. 2023.
"""

import os
from dotenv import load_dotenv

from util.datatypes import HardwareStats, RenderSettings, RenderRequest
from util.datatypes.abstracts.StorableEntity import StorableEntity

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.dirname(MODULE_PATH)

load_dotenv(os.path.join(MODULE_PATH, '../../.env'))

DATABASE = os.path.join(ROOT_PATH, "../" + os.getenv("DATABASE_FOLDER") + os.getenv("ARCHIVE_FOLDER"))


class RenderArchive(StorableEntity):
    """
        Entity Object Class to represent an Archive of a Render Job.

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
            project_name='',
            render_request=None,
            hardware_stats=None,
            total_time='',
            finish_time='',
            avg_frame=0,
            frame_map=None,
            render_settings=None
    ):
        """
            Class Constructor.
            Takes in every Parameter as an Optional, allowing for the creation of Empty Objects.

            :param uuid: Entity UUID.
            :type uuid: String.
            :param project_name: Name of the Project for the Render Job.
            :type project_name: String.
            :param render_request: Archive of the Render Request for the Job.
            :type render_request: RenderRequest.
            :param hardware_stats: Hardware Info for the Machine that ran the Job.
            :type hardware_stats: HardwareStats.
            :param total_time: Total Render Time the Job took.
            :type total_time: Datetime.Deltatime.
            :param finish_time: Timestamp of when the Job finished Rendering.
            :type finish_time: Datetime.
            :param avg_frame: Average Time (in Seconds) it took to Render each Frame.
            :type avg_frame: Float.
            :param frame_map: List of Times (in Seconds) it took to Render each Frame.
            :type frame_map: List of Floats.
            :param render_settings: Settings the Render Job had enabled.
            :type render_settings: RenderSettings.
        """
        if not frame_map:
            frame_map = []

        super().__init__((uuid or render_request.uuid))
        self.project_name = project_name
        self.render_request = render_request
        self.hardware_stats = hardware_stats
        self.total_time = total_time
        self.finish_time = finish_time
        self.avg_frame = avg_frame
        self.frame_map = frame_map
        self.render_settings = render_settings

    @classmethod
    def from_dict(cls, data):
        """
            @inheritDoc - StorableEntity
        """
        uuid = data.get('uuid') or ''
        project_name = data.get('project_name') or ''
        total_time = data.get('total_time') or ''
        finish_time = data.get('finish_time') or ''
        avg_frame = data.get('avg_frame') or ''
        frame_map = data.get('frame_map') or ''

        render_request = RenderRequest.RenderRequest.from_dict(data.get('render_request'))
        hardware_stats = HardwareStats.HardwareStats.from_dict(data.get('hardware_stats'))
        render_settings = RenderSettings.RenderSettings.from_dict(data.get('render_settings'))

        return cls(
            uuid=uuid,
            project_name=project_name,
            render_request=render_request,
            hardware_stats=hardware_stats,
            total_time=total_time,
            finish_time=finish_time,
            avg_frame=avg_frame,
            frame_map=frame_map,
            render_settings=render_settings
        )

    def copy(self):
        """
            Helper Method to Create a Copy of the Entity Object.

            :return: Entity Object with same Fields as Self.
        """
        return RenderArchive(
            uuid=self.uuid,
            project_name=self.project_name,
            render_request=self.render_request,
            hardware_stats=self.hardware_stats,
            total_time=self.total_time,
            finish_time=self.finish_time,
            avg_frame=self.avg_frame,
            frame_map=self.frame_map,
            render_settings=self.render_settings
        )

    def to_dict(self):
        """
            @inheritDoc - StorableEntity

            Custom Implementation to account for Complex Fields.
        """
        copy = self.copy()
        if self.render_request:
            copy.render_request = self.render_request.to_dict()
        if self.hardware_stats:
            copy.hardware_stats = self.hardware_stats.to_dict()
        if self.render_settings:
            copy.render_settings = self.render_settings.to_dict()
        return copy.__dict__
