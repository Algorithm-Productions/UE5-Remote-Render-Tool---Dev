from util.datatypes.abstracts.UnrealDataType import UnrealDataType


class HighResSettings(UnrealDataType):
    def __init__(
            self,
            tileCount=0,
            textureSharpnessBias=0.0,
            overlapRatio=0.0,
            overrideSubSurfaceScattering=False,
            burleySampleCount=0
    ):
        self.tileCount = tileCount
        self.textureSharpnessBias = textureSharpnessBias
        self.overlapRatio = overlapRatio
        self.overrideSubSurfaceScattering = overrideSubSurfaceScattering
        self.burleySampleCount = burleySampleCount

    @classmethod
    def from_dict(cls, data):
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
        return cls(
            tileCount=unrealClass.tile_count,
            textureSharpnessBias=unrealClass.texture_sharpness_bias,
            overlapRatio=unrealClass.overlap_ratio,
            overrideSubSurfaceScattering=unrealClass.override_sub_surface_scattering,
            burleySampleCount=unrealClass.burley_sample_count
        )
