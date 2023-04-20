from ..abstracts.UnrealOverride import UnrealOverride


class OutputSettingsOverride(UnrealOverride):
    UNREAL_MAPPINGS = {
        "outputDirectory": ["output_directory", "path"],
        "fileNameFormat": ["file_name_format", "str"],
        "outputResolutionX": ["output_resolution", "resolutionX"],
        "outputResolutionY": ["output_resolution", "resolutionY"],
        "useCustomFrameRate": ["use_custom_frame_rate", "bool"],
        "outputFrameRate": ["output_frame_rate", "frameRate"],
        "overrideExistingOutput": ["override_existing_output", "bool"],
        "zeroPadFrameNumbers": ["zero_pad_frame_numbers", "int"],
        "frameNumberOffset": ["frame_number_offset", "int"],
        "handleFrameCount": ["handle_frame_count", "int"],
        "outputFrameStep": ["output_frame_step", "int"],
        "useCustomPlaybackRange": ["use_custom_playback_range", "bool"],
        "customStartFrame": ["custom_start_frame", "int"],
        "customEndFrame": ["custom_end_frame", "int"],
        "versionNumber": ["version_number", "float"],
        "autoVersion": ["auto_version", "bool"]
    }
    UNREAL_SETTING_KEY = "output"

    def __init__(
            self,
            outputDirectoryFlag=False,
            fileNameFormatFlag=False,
            outputResolutionXFlag=False,
            outputResolutionYFlag=False,
            useCustomFrameRateFlag=False,
            outputFrameRateFlag=False,
            overrideExistingOutputFlag=False,
            zeroPadFrameNumbersFlag=False,
            frameNumberOffsetFlag=False,
            handleFrameCountFlag=False,
            outputFrameStepFlag=False,
            useCustomPlaybackRangeFlag=False,
            customStartFrameFlag=False,
            customEndFrameFlag=False,
            versionNumberFlag=False,
            autoVersionFlag=False
    ):
        self.outputDirectoryFlag = outputDirectoryFlag
        self.fileNameFormatFlag = fileNameFormatFlag
        self.outputResolutionXFlag = outputResolutionXFlag
        self.outputResolutionYFlag = outputResolutionYFlag
        self.useCustomFrameRateFlag = useCustomFrameRateFlag
        self.outputFrameRateFlag = outputFrameRateFlag
        self.overrideExistingOutputFlag = overrideExistingOutputFlag
        self.zeroPadFrameNumbersFlag = zeroPadFrameNumbersFlag
        self.frameNumberOffsetFlag = frameNumberOffsetFlag
        self.handleFrameCountFlag = handleFrameCountFlag
        self.outputFrameStepFlag = outputFrameStepFlag
        self.useCustomPlaybackRangeFlag = useCustomPlaybackRangeFlag
        self.customStartFrameFlag = customStartFrameFlag
        self.customEndFrameFlag = customEndFrameFlag
        self.versionNumberFlag = versionNumberFlag
        self.autoVersionFlag = autoVersionFlag

    @classmethod
    def from_dict(cls, data):
        outputDirectoryFlag = (data["outputDirectoryFlag"] or False) if data else False
        fileNameFormatFlag = (data["fileNameFormatFlag"] or False) if data else False
        outputResolutionXFlag = (data["outputResolutionXFlag"] or False) if data else False
        outputResolutionYFlag = (data["outputResolutionYFlag"] or False) if data else False
        useCustomFrameRateFlag = (data["useCustomFrameRateFlag"] or False) if data else False
        outputFrameRateFlag = (data["outputFrameRateFlag"] or False) if data else False
        overrideExistingOutputFlag = (data["overrideExistingOutputFlag"] or False) if data else False
        zeroPadFrameNumbersFlag = (data["zeroPadFrameNumbersFlag"] or False) if data else False
        frameNumberOffsetFlag = (data["frameNumberOffsetFlag"] or False) if data else False
        handleFrameCountFlag = (data["handleFrameCountFlag"] or False) if data else False
        outputFrameStepFlag = (data["outputFrameStepFlag"] or False) if data else False
        useCustomPlaybackRangeFlag = (data["useCustomPlaybackRangeFlag"] or False) if data else False
        customStartFrameFlag = (data["customStartFrameFlag"] or False) if data else False
        customEndFrameFlag = (data["customEndFrameFlag"] or False) if data else False
        versionNumberFlag = (data["versionNumberFlag"] or False) if data else False
        autoVersionFlag = (data["autoVersionFlag"] or False) if data else False

        return cls(
            outputDirectoryFlag=outputDirectoryFlag,
            fileNameFormatFlag=fileNameFormatFlag,
            outputResolutionXFlag=outputResolutionXFlag,
            outputResolutionYFlag=outputResolutionYFlag,
            useCustomFrameRateFlag=useCustomFrameRateFlag,
            outputFrameRateFlag=outputFrameRateFlag,
            overrideExistingOutputFlag=overrideExistingOutputFlag,
            zeroPadFrameNumbersFlag=zeroPadFrameNumbersFlag,
            frameNumberOffsetFlag=frameNumberOffsetFlag,
            handleFrameCountFlag=handleFrameCountFlag,
            outputFrameStepFlag=outputFrameStepFlag,
            useCustomPlaybackRangeFlag=useCustomPlaybackRangeFlag,
            customStartFrameFlag=customStartFrameFlag,
            customEndFrameFlag=customEndFrameFlag,
            versionNumberFlag=versionNumberFlag,
            autoVersionFlag=autoVersionFlag
        )
