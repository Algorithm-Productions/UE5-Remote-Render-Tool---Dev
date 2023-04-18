from ..abstracts.StorableProperty import StorableProperty


class HighResSettingsOverride(StorableProperty):
    def __init__(
            self,
            tileCountFlag=False,
            textureSharpnessBiasFlag=False,
            overlapRatioFlag=False,
            overrideSubSurfaceScatteringFlag=False,
            burleySampleCountFlag=False
    ):
        self.tileCountFlag = tileCountFlag,
        self.textureSharpnessBiasFlag = textureSharpnessBiasFlag,
        self.overlapRatioFlag = overlapRatioFlag,
        self.overrideSubSurfaceScatteringFlag = overrideSubSurfaceScatteringFlag,
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
