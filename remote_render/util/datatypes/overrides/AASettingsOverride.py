from ..abstracts.StorableProperty import StorableProperty


class AASettingsOverride(StorableProperty):
    def __init__(
            self,
            spatialSampleCountFlag=False,
            temporalSampleCountFlag=False,
            overrideAAFlag=False,
            aaMethodFlag=False,
            useCameraCutForWarmUpFlag=False,
            renderWarmUpFramesFlag=False,
            renderWarmUpCountFlag=False,
            engineWarmUpCountFlag=False
    ):
        self.spatialSampleCountFlag = spatialSampleCountFlag
        self.temporalSampleCountFlag = temporalSampleCountFlag
        self.overrideAAFlag = overrideAAFlag
        self.aaMethodFlag = aaMethodFlag
        self.useCameraCutForWarmUpFlag = useCameraCutForWarmUpFlag
        self.renderWarmUpFramesFlag = renderWarmUpFramesFlag
        self.renderWarmUpCountFlag = renderWarmUpCountFlag
        self.engineWarmUpCountFlag = engineWarmUpCountFlag

    @classmethod
    def from_dict(cls, data):
        spatialSampleCountFlag = (data["spatialSampleCountFlag"] or False) if data else False
        temporalSampleCountFlag = (data["temporalSampleCountFlag"] or False) if data else False
        overrideAAFlag = (data["overrideAAFlag"] or False) if data else False
        aaMethodFlag = (data["aaMethodFlag"] or False) if data else False
        useCameraCutForWarmUpFlag = (data["useCameraCutForWarmUpFlag"] or False) if data else False
        renderWarmUpFramesFlag = (data["renderWarmUpFramesFlag"] or False) if data else False
        renderWarmUpCountFlag = (data["renderWarmUpCountFlag"] or False) if data else False
        engineWarmUpCountFlag = (data["engineWarmUpCountFlag"] or False) if data else False

        return cls(
            spatialSampleCountFlag=spatialSampleCountFlag,
            temporalSampleCountFlag=temporalSampleCountFlag,
            overrideAAFlag=overrideAAFlag,
            aaMethodFlag=aaMethodFlag,
            useCameraCutForWarmUpFlag=useCameraCutForWarmUpFlag,
            renderWarmUpFramesFlag=renderWarmUpFramesFlag,
            renderWarmUpCountFlag=renderWarmUpCountFlag,
            engineWarmUpCountFlag=engineWarmUpCountFlag
        )
