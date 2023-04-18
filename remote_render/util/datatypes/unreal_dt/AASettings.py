"""
    Copyright Algorithm Productions LLC. 2023.
"""

from ..abstracts.UnrealDataType import UnrealDataType


class AASettings(UnrealDataType):
    """
        Python Form of the unreal.MoviePipelineAntiAliasingSetting Class.

        :type: UnrealDataType.
        :author: vitor@bu.edu.
    """

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
        """
            Class Constructor.
            Takes in every Parameter as an Optional, allowing for the creation of Empty Objects.

            :param spatialSampleCount: Amount of Spatial Samples to take in the Render.
            :type spatialSampleCount: Integer.
            :param temporalSampleCount: Amount of Temporal Samples to take in the Render.
            :type temporalSampleCount: Integer.
            :param overrideAA: Should we Override the existing AA Method?
            :type overrideAA: Boolean.
            :param aaMethod: Specific AA Method to Use.
            :type aaMethod: unreal.AntiAliasingMethod.
            :param useCameraCutForWarmUp: Should we use the Excess in the Camera Cut Track to Determine Engine Warmup?
            :type useCameraCutForWarmUp: Boolean.
            :param renderWarmUpFrames: Should we Submit Warm Up Frames to the GPU before each Render?
            :type renderWarmUpFrames: Boolean.
            :param renderWarmUpCount: Amount of Warm Up Frames to run before each Render.
            :type renderWarmUpCount: Integer.
            :param engineWarmUpCount: Amount of Warm Up Frames to run before the Engine Starts.
            :type engineWarmUpCount: Integer.
        """
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
        """
            @inheritDoc - UnrealDataType
        """
        spatialSampleCount = (data["spatialSampleCount"] or 0) if data else 0
        temporalSampleCount = (data["temporalSampleCount"] or 0) if data else 0
        overrideAA = (data["overrideAA"] or False) if data else False
        aaMethod = (data["aaMethod"] or '') if data else ''
        useCameraCutForWarmUp = (data["useCameraCutForWarmUp"] or False) if data else False
        renderWarmUpFrames = (data["renderWarmUpFrames"] or False) if data else False
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
        """
            @inheritDoc - UnrealDataType
        """
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
