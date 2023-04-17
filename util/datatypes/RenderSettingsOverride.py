from util.datatypes import RenderSettings
from util.datatypes.abstracts.StorableProperty import StorableProperty


class RenderSettingsOverride(StorableProperty):
    def __init__(
            self,
            overridenBools=None,
            renderSettings=None
    ):
        """
            Class Constructor.
            Takes in every Parameter as an Optional, allowing for the creation of Empty Objects.

            :param overridenBools: Map of Settings with Overwritten Flags.
            :type overridenBools: Dict
            :param renderSettings: Actual Render Settings Object to get Overwrites from.
            :type renderSettings: RenderSettings.RenderSettings.
        """
        self.overridenBools = overridenBools
        self.renderSettings = renderSettings

    @classmethod
    def from_dict(cls, data):
        """
            @inheritDoc - StorableProperty
        """
        overridenBools = eval(data['overridenBools']) if data and data['overridenBools'] else {}
        renderSettings = RenderSettings.RenderSettings.from_dict(data.get('renderSettings'))

        return cls(
            overridenBools=overridenBools,
            renderSettings=renderSettings
        )

    def copy(self):
        """
            Helper Method to Create a Copy of the Property Object.

            :return: Property Object with same Fields as Self.
        """
        return RenderSettingsOverride(
            overridenBools=self.overridenBools,
            renderSettings=self.renderSettings
        )

    def to_dict(self):
        """
            @inheritDoc - StorableProperty

            Custom Implementation to account for Complex Fields.
        """
        copy = self.copy()
        if self.overridenBools:
            copy.overridenBools = self.overridenBools.to_dict()
        if self.renderSettings:
            copy.renderSettings = self.renderSettings.to_dict()

        return copy.__dict__
