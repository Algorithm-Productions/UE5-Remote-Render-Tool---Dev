"""
    Copyright Algorithm Productions LLC. 2023.
"""

from remote_render.util.datatypes.abstracts.UnrealDataType import UnrealDataType


class OutputSettings(UnrealDataType):
    """
        Python Form of the unreal.MoviePipelineOutputSetting Class.

        :type: UnrealDataType.
        :author: vitor@bu.edu.
    """

    def __init__(
            self,
            outputDirectory='',
            fileNameFormat='',
            outputResolutionX=0,
            outputResolutionY=0,
            useCustomFrameRate=False,
            outputFrameRate=0,
            overrideExistingOutput=False,
            zeroPadFrameNumbers=0,
            frameNumberOffset=0,
            handleFrameCount=0,
            outputFrameStep=0,
            useCustomPlaybackRange=False,
            customStartFrame=0,
            customEndFrame=0,
            versionNumber=0,
            autoVersion=False
    ):
        """
            Class Constructor.
            Takes in every Parameter as an Optional, allowing for the creation of Empty Objects.

            :param outputDirectory: Path to the Output Directory for the Render.
            :type outputDirectory: String.
            :param fileNameFormat: Format for the Names of the Output Files.
            :type fileNameFormat: String.
            :param outputResolutionX: Width Resolution to Render In.
            :type outputResolutionX: Integer.
            :param outputResolutionY: Height Resolution to Render In.
            :type outputResolutionY: Integer.
            :param useCustomFrameRate: Should the Render use a Custom Frame Rate?
            :type useCustomFrameRate: Boolean.
            :param outputFrameRate: Custom Frame Rate for the Render.
            :type outputFrameRate: Integer.
            :param overrideExistingOutput: Should the Render Override Existing Files in the Directory?
            :type overrideExistingOutput: Boolean.
            :param zeroPadFrameNumbers: Amount of Digits to Pad To in Frame Names.
            :type zeroPadFrameNumbers: Integer.
            :param frameNumberOffset: Amount of Numbers to Offset Frame Names by.
            :type frameNumberOffset: Integer.
            :param handleFrameCount: Amount of Frames to Extend the Render to on either side.
            :type handleFrameCount: Integer.
            :param outputFrameStep: Size of the step between each Rendered Frame.
            :type outputFrameStep: Integer.
            :param useCustomPlaybackRange: Should the Render use a Custom Frame Range?
            :type useCustomPlaybackRange: Boolean.
            :param customStartFrame: Start Frame for the Custom Range.
            :type customStartFrame: Integer.
            :param customEndFrame: End Frame for the Custom Range.
            :type customEndFrame: Integer.
            :param versionNumber: Version Number of the Render.
            :type versionNumber: Float.
            :param autoVersion: Should UE auto-generate Version Numbers for the Render?
            :type autoVersion: Boolean.
        """
        self.outputDirectory = outputDirectory
        self.fileNameFormat = fileNameFormat
        self.outputResolutionX = outputResolutionX
        self.outputResolutionY = outputResolutionY
        self.useCustomFrameRate = useCustomFrameRate
        self.outputFrameRate = outputFrameRate
        self.overrideExistingOutput = overrideExistingOutput
        self.zeroPadFrameNumbers = zeroPadFrameNumbers
        self.frameNumberOffset = frameNumberOffset
        self.handleFrameCount = handleFrameCount
        self.outputFrameStep = outputFrameStep
        self.useCustomPlaybackRange = useCustomPlaybackRange
        self.customStartFrame = customStartFrame
        self.customEndFrame = customEndFrame
        self.versionNumber = versionNumber
        self.autoVersion = autoVersion

    @classmethod
    def from_dict(cls, data):
        """
            @inheritDoc - UnrealDataType
        """
        outputDirectory = (data["outputDirectory"] or '') if data else ''
        fileNameFormat = (data["fileNameFormat"] or '') if data else ''
        outputResolutionX = (data["outputResolutionX"] or 0) if data else 0
        outputResolutionY = (data["outputResolutionY"] or 0) if data else 0
        useCustomFrameRate = (data["useCustomFrameRate"] or False) if data else False
        outputFrameRate = (data["outputFrameRate"] or 0) if data else 0
        overrideExistingOutput = (data["overrideExistingOutput"] or False) if data else False
        zeroPadFrameNumbers = (data["zeroPadFrameNumbers"] or 0) if data else 0
        frameNumberOffset = (data["frameNumberOffset"] or 0) if data else 0
        handleFrameCount = (data["handleFrameCount"] or 0) if data else 0
        outputFrameStep = (data["outputFrameStep"] or 0) if data else 0
        useCustomPlaybackRange = (data["useCustomPlaybackRange"] or False) if data else False
        customStartFrame = (data["customStartFrame"] or 0) if data else 0
        customEndFrame = (data["customEndFrame"] or 0) if data else 0
        versionNumber = (data["versionNumber"] or 0) if data else 0
        autoVersion = (data["autoVersion"] or False) if data else False

        return cls(
            outputDirectory=outputDirectory,
            fileNameFormat=fileNameFormat,
            outputResolutionX=outputResolutionX,
            outputResolutionY=outputResolutionY,
            useCustomFrameRate=useCustomFrameRate,
            outputFrameRate=outputFrameRate,
            overrideExistingOutput=overrideExistingOutput,
            zeroPadFrameNumbers=zeroPadFrameNumbers,
            frameNumberOffset=frameNumberOffset,
            handleFrameCount=handleFrameCount,
            outputFrameStep=outputFrameStep,
            useCustomPlaybackRange=useCustomPlaybackRange,
            customStartFrame=customStartFrame,
            customEndFrame=customEndFrame,
            versionNumber=versionNumber,
            autoVersion=autoVersion
        )

    @classmethod
    def from_unreal(cls, unrealClass):
        """
            @inheritDoc - UnrealDataType
        """
        return cls(
            outputDirectory=unrealClass.output_directory.path,
            fileNameFormat=unrealClass.file_name_format,
            outputResolutionX=unrealClass.output_resolution.x,
            outputResolutionY=unrealClass.output_resolution.y,
            useCustomFrameRate=unrealClass.use_custom_frame_rate,
            outputFrameRate=unrealClass.output_frame_rate.numerator,
            overrideExistingOutput=unrealClass.override_existing_output,
            zeroPadFrameNumbers=unrealClass.zero_pad_frame_numbers,
            frameNumberOffset=unrealClass.frame_number_offset,
            handleFrameCount=unrealClass.handle_frame_count,
            outputFrameStep=unrealClass.output_frame_step,
            useCustomPlaybackRange=unrealClass.use_custom_playback_range,
            customStartFrame=unrealClass.custom_start_frame,
            customEndFrame=unrealClass.custom_end_frame,
            versionNumber=unrealClass.version_number,
            autoVersion=unrealClass.auto_version
        )
