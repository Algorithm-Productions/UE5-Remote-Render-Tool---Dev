from util.datatypes.abstracts.UnrealDataType import UnrealDataType


class AASettings(UnrealDataType):
    def __init__(
            self,
            spatialSampleCount=0,
            temporalSampleCount=0,
            overrideAA=False,
            aaMethod='',
            useCameraCutForWarmUp=False,
            renderWarmUpFrames=False,
            renderWarmUpCount=0,
            engineWarmUpCount=0
    ):
        self.spatialSampleCount = spatialSampleCount
        self.temporalSampleCount = temporalSampleCount
        self.overrideAA = overrideAA
        self.aaMethod = aaMethod
        self.useCameraCutForWarmUp = useCameraCutForWarmUp
        self.renderWarmUpFrames = renderWarmUpFrames
        self.renderWarmUpCount = renderWarmUpCount
        self.engineWarmUpCount = engineWarmUpCount

    @classmethod
    def from_dict(cls, data):
        spatialSampleCount = (data["spatialSampleCount"] or 0) if data else 0
        temporalSampleCount = (data["temporalSampleCount"] or 0) if data else 0
        overrideAA = (data["overrideAA"] or False) if data else 0
        aaMethod = (data["aaMethod"] or '') if data else 0
        useCameraCutForWarmUp = (data["useCameraCutForWarmUp"] or False) if data else 0
        renderWarmUpFrames = (data["renderWarmUpFrames"] or False) if data else 0
        renderWarmUpCount = (data["renderWarmUpCount"] or 0) if data else 0
        engineWarmUpCount = (data["engineWarmUpCount"] or 0) if data else 0

        return cls(
            spatialSampleCount=spatialSampleCount,
            temporalSampleCount=temporalSampleCount,
            overrideAA=overrideAA,
            aaMethod=aaMethod,
            useCameraCutForWarmUp=useCameraCutForWarmUp,
            renderWarmUpFrames=renderWarmUpFrames,
            renderWarmUpCount=renderWarmUpCount,
            engineWarmUpCount=engineWarmUpCount
        )

    @classmethod
    def from_unreal(cls, unrealClass):
        return cls(
            spatialSampleCount=unrealClass.spatial_sample_count,
            temporalSampleCount=unrealClass.temporal_sample_count,
            overrideAA=unrealClass.override_anti_aliasing,
            aaMethod=str(unrealClass.anti_aliasing_method),
            useCameraCutForWarmUp=unrealClass.use_camera_cut_for_warm_up,
            renderWarmUpFrames=unrealClass.render_warm_up_frames,
            renderWarmUpCount=unrealClass.render_warm_up_count,
            engineWarmUpCount=unrealClass.engine_warm_up_count
        )
