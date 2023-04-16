"""
    Copyright Algorithm Productions LLC. 2023.
"""

from util.datatypes.abstracts.UnrealDataType import UnrealDataType


class HighResSettings(UnrealDataType):
    """
        Python Form of the unreal.MoviePipelineHighResSetting Class.

        :type: UnrealDataType.
        :author: vitor@bu.edu.
    """

    def __init__(
            self,
            tileCount=0,
            textureSharpnessBias=0.0,
            overlapRatio=0.0,
            overrideSubSurfaceScattering=False,
            burleySampleCount=0
    ):
        """
            Class Constructor.
            Takes in every Parameter as an Optional, allowing for the creation of Empty Objects.

            :param tileCount: Amount of Tiles to Split the Render into.
            :type tileCount: Integer.
            :param textureSharpnessBias: Float Percentage to use in determining Texture Sharpness.
            :type textureSharpnessBias: Float (Between 0 and 1).
            :param overlapRatio: How much of each Tile is re-rendered in the other Tiles.
            :type overlapRatio: Float.
            :param overrideSubSurfaceScattering: Should we increase Sub-Surface samples to improve quality?
            :type overrideSubSurfaceScattering: Boolean.
            :param burleySampleCount: Amount of Sub-Surface Samples taken.
            :type burleySampleCount: Integer.
        """
        self.tileCount = tileCount
        self.textureSharpnessBias = textureSharpnessBias
        self.overlapRatio = overlapRatio
        self.overrideSubSurfaceScattering = overrideSubSurfaceScattering
        self.burleySampleCount = burleySampleCount

    @classmethod
    def from_dict(cls, data):
        """
            @inheritDoc - UnrealDataType
        """
        tileCount = (data["tileCount"] or 0) if data else 0
        textureSharpnessBias = (data["textureSharpnessBias"] or 0.0) if data else 0.0
        overlapRatio = (data["overlapRatio"] or 0.0) if data else 0.0
        overrideSubSurfaceScattering = (data["overrideSubSurfaceScattering"] or False) if data else False
        burleySampleCount = (data["burleySampleCount"] or 0) if data else 0

        return cls(
            tileCount=tileCount,
            textureSharpnessBias=textureSharpnessBias,
            overlapRatio=overlapRatio,
            overrideSubSurfaceScattering=overrideSubSurfaceScattering,
            burleySampleCount=burleySampleCount
        )

    @classmethod
    def from_unreal(cls, unrealClass):
        """
            @inheritDoc - UnrealDataType
        """
        return cls(
            tileCount=unrealClass.tile_count,
            textureSharpnessBias=unrealClass.texture_sharpness_bias,
            overlapRatio=unrealClass.overlap_ratio,
            overrideSubSurfaceScattering=unrealClass.override_sub_surface_scattering,
            burleySampleCount=unrealClass.burley_sample_count
        )
