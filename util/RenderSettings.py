class AASettings:
    def __int__(
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

    def to_dict(self):
        return self.__dict__


class ConsoleSettings:
    def __int__(
            self,
            consoleVariables=None,
            startConsoleCommands=None,
            endConsoleCommands=None
    ):
        if not consoleVariables:
            consoleVariables = {}
        if not startConsoleCommands:
            startConsoleCommands = []
        if not endConsoleCommands:
            endConsoleCommands = []

        self.consoleVariables = consoleVariables
        self.startConsoleCommands = startConsoleCommands
        self.endConsoleCommands = endConsoleCommands

    @classmethod
    def from_dict(cls, data):
        consoleVariables = (eval(data["consoleVariables"]) or {}) if data else {}
        startConsoleCommands = (data["consoleVariables"] or []) if data else []
        endConsoleCommands = (data["endConsoleCommands"] or []) if data else []

        return cls(
            consoleVariables=consoleVariables,
            startConsoleCommands=startConsoleCommands,
            endConsoleCommands=endConsoleCommands
        )

    def to_dict(self):
        return self.__dict__


class HighResSettings:
    def __int__(
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

    def to_dict(self):
        return self.__dict__


class OutputSettings:
    def __int__(
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

    def to_dict(self):
        return self.__dict__


class RenderSettings(object):
    def __init__(
            self,
            output_type='',
            enabled_render_types=None,
            aa_settings=None,
            console_settings=None,
            high_res_settings=None,
            output_settings=None
    ):
        if not enabled_render_types:
            enabled_render_types = []

        self.output_type = output_type
        self.enabled_render_types = enabled_render_types
        self.aa_settings = aa_settings
        self.console_settings = console_settings
        self.high_res_settings = high_res_settings
        self.output_settings = output_settings

    @classmethod
    def from_dict(cls, data):
        output_type = (data["output_type"] or '') if data else ''
        enabled_render_types = (data["enabled_render_types"] or '') if data else ''
        aa_settings = (AASettings.from_dict(data.get('aa_settings'))) if data else None
        console_settings = (ConsoleSettings.from_dict(data.get('console_settings'))) if data else None
        high_res_settings = (HighResSettings.from_dict(data.get('high_res_settings'))) if data else None
        output_settings = (OutputSettings.from_dict(data.get('output_settings'))) if data else None

        return cls(
            output_type=output_type,
            enabled_render_types=enabled_render_types,
            aa_settings=aa_settings,
            console_settings=console_settings,
            high_res_settings=high_res_settings,
            output_settings=output_settings
        )

    def copy(self):
        return RenderSettings(
            output_type=self.output_type,
            enabled_render_types=self.enabled_render_types,
            aa_settings=self.aa_settings,
            console_settings=self.console_settings,
            high_res_settings=self.high_res_settings,
            output_settings=self.output_settings
        )

    def to_dict(self):
        copy = self.copy()
        if self.aa_settings:
            copy.render_request = self.aa_settings.to_dict()
        if self.console_settings:
            copy.render_request = self.console_settings.to_dict()
        if self.high_res_settings:
            copy.render_request = self.high_res_settings.to_dict()
        if self.output_settings:
            copy.render_request = self.output_settings.to_dict()

        return copy.__dict__
