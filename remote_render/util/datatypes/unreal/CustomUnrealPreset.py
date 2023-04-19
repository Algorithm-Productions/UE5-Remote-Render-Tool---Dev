import unreal


@unreal.uclass()
class CustomUnrealPreset(unreal.MoviePipelineMasterConfig):
    def __init__(self, preset):
        super(CustomUnrealPreset, self).__init__(preset)
        self.copy_from(preset)

    def update_properties(self, overrides, config):
        self.update_output(overrides["output_settings_flags"], config["output_settings"])
        self.update_high_res(overrides["high_res_settings_flags"], config["high_res_settings"])
        self.update_aa(overrides["aa_settings_flags"], config["aa_settings"])
        self.update_console(overrides["console_settings_flags"], config["console_settings"])

    def update_output(self, overrides, config):
        currSettings = self.find_or_add_setting_by_class(
            unreal.MoviePipelineOutputSetting
        )
        if overrides["outputDirectoryFlag"]:
            currSettings.set_editor_property(
                'output_directory',
                unreal.DirectoryPath(config["outputDirectory"])
            )
        if overrides["fileNameFormatFlag"]:
            currSettings.set_editor_property(
                'file_name_format',
                config["fileNameFormat"]
            )
        if overrides["outputResolutionXFlag"]:
            currSettings.set_editor_property(
                'output_resolution',
                unreal.IntPoint(int(config["outputResolutionX"]), currSettings.output_resolution.y)
            )
        if overrides["outputResolutionYFlag"]:
            currSettings.set_editor_property(
                'output_resolution',
                unreal.IntPoint(currSettings.output_resolution.x, int(config["outputResolutionY"]))
            )
        if overrides["useCustomFrameRateFlag"]:
            currSettings.set_editor_property(
                'use_custom_frame_rate',
                bool(config["useCustomFrameRate"])
            )
        if overrides["outputFrameRateFlag"]:
            currSettings.set_editor_property(
                'output_frame_rate',
                unreal.FrameRate(config["outputFrameRate"], 1)
            )
        if overrides["overrideExistingOutputFlag"]:
            currSettings.set_editor_property(
                'override_existing_output',
                bool(config["overrideExistingOutput"])
            )
        if overrides["zeroPadFrameNumbersFlag"]:
            currSettings.set_editor_property(
                'zero_pad_frame_numbers',
                int(config["zeroPadFrameNumbers"])
            )
        if overrides["frameNumberOffsetFlag"]:
            currSettings.set_editor_property(
                'frame_number_offset',
                int(config["frameNumberOffset"])
            )
        if overrides["handleFrameCountFlag"]:
            currSettings.set_editor_property(
                'handle_frame_count',
                int(config["handleFrameCount"])
            )
        if overrides["outputFrameStepFlag"]:
            currSettings.set_editor_property(
                'output_frame_step',
                int(config["outputFrameStep"])
            )
        if overrides["useCustomPlaybackRangeFlag"]:
            currSettings.set_editor_property(
                'use_custom_playback_range',
                bool(config["useCustomPlaybackRange"])
            )
        if overrides["customStartFrameFlag"]:
            currSettings.set_editor_property(
                'custom_start_frame',
                int(config["customStartFrame"])
            )
        if overrides["customEndFrameFlag"]:
            currSettings.set_editor_property(
                'custom_end_frame',
                int(config["customEndFrame"])
            )
        if overrides["versionNumberFlag"]:
            currSettings.set_editor_property(
                'version_number',
                int(config["versionNumber"])
            )
        if overrides["autoVersionFlag"]:
            currSettings.set_editor_property(
                'auto_version',
                bool(config["autoVersion"])
            )

    def update_high_res(self, overrides, config):
        currSettings = self.find_or_add_setting_by_class(
            unreal.MoviePipelineHighResSetting
        )
        if overrides["tileCountFlag"]:
            currSettings.set_editor_property(
                'tile_count',
                int(config["tileCount"])
            )
        if overrides["textureSharpnessBiasFlag"]:
            currSettings.set_editor_property(
                'texture_sharpness_bias',
                float(config["textureSharpnessBias"])
            )
        if overrides["overlapRatioFlag"]:
            currSettings.set_editor_property(
                'overlap_ratio',
                float(config["overlapRatio"])
            )
        if overrides["overrideSubSurfaceScatteringFlag"]:
            currSettings.set_editor_property(
                'override_sub_surface_scattering',
                bool(config["overrideSubSurfaceScattering"])
            )
        if overrides["burleySampleCountFlag"]:
            currSettings.set_editor_property(
                'burley_sample_count',
                int(config["burleySampleCount"])
            )

    def update_aa(self, overrides, config):
        currSettings = self.find_or_add_setting_by_class(
            unreal.MoviePipelineAntiAliasingSetting
        )
        if overrides["spatialSampleCountFlag"]:
            currSettings.set_editor_property(
                'spatial_sample_count',
                int(config["spatialSampleCount"])
            )
        if overrides["temporalSampleCountFlag"]:
            currSettings.set_editor_property(
                'temporal_sample_count',
                int(config["temporalSampleCount"])
            )
        if overrides["overrideAAFlag"]:
            currSettings.set_editor_property(
                'override_anti_aliasing',
                bool(config["overrideAA"])
            )
        if overrides["aaMethodFlag"]:
            method = unreal.AntiAliasingMethod.AAM_NONE
            if config["aaMethod"] == "FXAA":
                method = unreal.AntiAliasingMethod.AAM_FXAA
            elif config["aaMethod"] == "MSAA":
                method = unreal.AntiAliasingMethod.AAM_MSAA
            elif config["aaMethod"] == "TEMPORAL_AA":
                method = unreal.AntiAliasingMethod.TEMPORAL_AA
            currSettings.set_editor_property(
                'anti_aliasing_method',
                method
            )
        if overrides["useCameraCutForWarmUpFlag"]:
            currSettings.set_editor_property(
                'use_camera_cut_for_warm_up',
                bool(config["useCameraCutForWarmUp"])
            )
        if overrides["renderWarmUpFramesFlag"]:
            currSettings.set_editor_property(
                'render_warm_up_frames',
                bool(config["renderWarmUpFrames"])
            )
        if overrides["renderWarmUpCountFlag"]:
            currSettings.set_editor_property(
                'render_warm_up_count',
                int(config["renderWarmUpCount"])
            )
        if overrides["engineWarmUpCountFlag"]:
            currSettings.set_editor_property(
                'engine_warm_up_count',
                int(config["engineWarmUpCount"])
            )

    def update_console(self, overrides, config):
        currSettings = self.find_or_add_setting_by_class(
            unreal.MoviePipelineConsoleVariableSetting
        )
        if overrides["consoleVariablesFlag"]:
            pass
        if overrides["startConsoleCommandsFlag"]:
            currSettings.set_editor_property(
                'start_console_commands',
                self.buildArray(config["startConsoleCommands"])
            )
        if overrides["endConsoleCommandsFlag"]:
            currSettings.set_editor_property(
                'end_console_commands',
                self.buildArray(config["endConsoleCommands"])
            )

    def buildArray(self, array):
        returnArray = unreal.Array
        for item in array:
            returnArray.append(item)

        return returnArray
