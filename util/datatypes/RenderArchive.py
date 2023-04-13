import os
from dotenv import load_dotenv

from util.datatypes import HardwareStats, RenderSettings, RenderRequest
from util.datatypes.abstracts.StorableEntity import StorableEntity

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.dirname(MODULE_PATH)

load_dotenv(os.path.join(MODULE_PATH, '../../.env'))

DATABASE = os.path.join(ROOT_PATH, "../" + os.getenv("DATABASE_FOLDER") + os.getenv("ARCHIVE_FOLDER"))


class RenderArchive(StorableEntity):
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
        copy = self.copy()
        if self.render_request:
            copy.render_request = self.render_request.to_dict()
        if self.hardware_stats:
            copy.hardware_stats = self.hardware_stats.to_dict()
        if self.render_settings:
            copy.render_settings = self.render_settings.to_dict()
        return copy.__dict__
