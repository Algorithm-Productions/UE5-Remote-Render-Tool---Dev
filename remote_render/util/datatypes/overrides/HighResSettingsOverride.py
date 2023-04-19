from ..abstracts.StorableProperty import StorableProperty


class HighResSettingsOverride(StorableProperty):
    UNREAL_MAPPINGS = {
        "tileCount": "tile_count",
        "textureSharpnessBias": "texture_sharpness_bias",
        "overlapRatio": "overlap_ratio",
        "overrideSubSurfaceScattering": "override_sub_surface_scattering",
        "burleySampleCount": "burley_sample_count"
    }

    def __init__(
            self,
            tileCountFlag=False,
            textureSharpnessBiasFlag=False,
            overlapRatioFlag=False,
            overrideSubSurfaceScatteringFlag=False,
            burleySampleCountFlag=False
    ):
        self.tileCountFlag = tileCountFlag
        self.textureSharpnessBiasFlag = textureSharpnessBiasFlag
        self.overlapRatioFlag = overlapRatioFlag
        self.overrideSubSurfaceScatteringFlag = overrideSubSurfaceScatteringFlag
        self.burleySampleCountFlag = burleySampleCountFlag

    @classmethod
    def from_dict(cls, data):
        tileCountFlag = (data["tileCountFlag"] or False) if data else False
        textureSharpnessBiasFlag = (data["textureSharpnessBiasFlag"] or False) if data else False
        overlapRatioFlag = (data["overlapRatioFlag"] or False) if data else False
        overrideSubSurfaceScatteringFlag = (data["overrideSubSurfaceScatteringFlag"] or False) if data else False
        burleySampleCountFlag = (data["burleySampleCountFlag"] or False) if data else False

        return cls(
            tileCountFlag=tileCountFlag,
            textureSharpnessBiasFlag=textureSharpnessBiasFlag,
            overlapRatioFlag=overlapRatioFlag,
            overrideSubSurfaceScatteringFlag=overrideSubSurfaceScatteringFlag,
            burleySampleCountFlag=burleySampleCountFlag
        )

    @classmethod
    def changeUnreal(cls, unrealObject, config, flags):
        for key, val in config.items():
            if flags[key + "Flag"]:
                unrealObject[cls.UNREAL_MAPPINGS[key]] = val
