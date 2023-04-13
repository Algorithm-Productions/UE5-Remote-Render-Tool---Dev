from util.datatypes.unreal import AASettings, ConsoleSettings, HighResSettings, OutputSettings


class RenderSettings(object):
    def __init__(
            self,
            output_types=None,
            render_types=None,
            aa_settings=None,
            console_settings=None,
            high_res_settings=None,
            output_settings=None
    ):
        if not output_types:
            output_types = []
        if not render_types:
            render_types = []

        self.output_types = output_types
        self.render_types = render_types
        self.aa_settings = aa_settings
        self.console_settings = console_settings
        self.high_res_settings = high_res_settings
        self.output_settings = output_settings

    @classmethod
    def from_dict(cls, data):
        output_types = (data["output_types"] or []) if data else []
        render_types = (data["render_types"] or []) if data else []
        aa_settings = (AASettings.AASettings.from_dict(data.get('aa_settings'))) if data else None
        console_settings = (ConsoleSettings.ConsoleSettings.from_dict(data.get('console_settings'))) if data else None
        high_res_settings = (HighResSettings.HighResSettings.from_dict(data.get('high_res_settings'))) if data else None
        output_settings = (OutputSettings.OutputSettings.from_dict(data.get('output_settings'))) if data else None

        return cls(
            output_types=output_types,
            render_types=render_types,
            aa_settings=aa_settings,
            console_settings=console_settings,
            high_res_settings=high_res_settings,
            output_settings=output_settings
        )

    def copy(self):
        return RenderSettings(
            output_types=self.output_types,
            render_types=self.render_types,
            aa_settings=self.aa_settings,
            console_settings=self.console_settings,
            high_res_settings=self.high_res_settings,
            output_settings=self.output_settings
        )

    def to_dict(self):
        copy = self.copy()
        if self.aa_settings:
            copy.aa_settings = self.aa_settings.to_dict()
        if self.console_settings:
            copy.console_settings = self.console_settings.to_dict()
        if self.high_res_settings:
            copy.high_res_settings = self.high_res_settings.to_dict()
        if self.output_settings:
            copy.output_settings = self.output_settings.to_dict()

        return copy.__dict__
