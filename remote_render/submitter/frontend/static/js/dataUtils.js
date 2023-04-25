const submitForm = () => {
    const basicSettingsForm = document.getElementById("basicSettingsForm")
    const outputSettings = document.getElementById("outputSettingsForm")
    const aaSettings = document.getElementById("aaSettingsForm")
    const consoleSettings = document.getElementById("consoleSettingsForm")
    const highResSettings = document.getElementById("highResSettingsForm")

    const override = {
        'output_types_flag': false,
        'render_types_flag': false,
        'aa_settings_flags': {
            'spatialSampleCountFlag': aaSettings.elements.spatialSampleCountFlag.checked,
            'temporalSampleCountFlag': aaSettings.elements.temporalSampleCountFlag.checked,
            'overrideAAFlag': aaSettings.elements.overrideAAFlag.checked,
            'aaMethodFlag': aaSettings.elements.aaMethodFlag.checked,
            'useCameraCutForWarmUpFlag': aaSettings.elements.useCameraCutForWarmUpFlag.checked,
            'renderWarmUpFramesFlag': aaSettings.elements.renderWarmUpFramesFlag.checked,
            'renderWarmUpCountFlag': aaSettings.elements.renderWarmUpCountFlag.checked,
            'engineWarmUpCountFlag': aaSettings.elements.engineWarmUpCountFlag.checked
        },
        'console_settings_flags': {
            'consoleVariablesFlag': consoleSettings.elements.consoleVariablesFlag.checked,
            'startConsoleCommandsFlag': consoleSettings.elements.startConsoleCommandsFlag.checked,
            'endConsoleCommandsFlag': consoleSettings.elements.endConsoleCommandsFlag.checked
        },
        'high_res_settings_flags': {
            'tileCountFlag': highResSettings.elements.tileCountFlag.checked,
            'textureSharpnessBiasFlag': highResSettings.elements.textureSharpnessBiasFlag.checked,
            'overlapRatioFlag': highResSettings.elements.overlapRatioFlag.checked,
            'overrideSubSurfaceScatteringFlag': highResSettings.elements.overrideSubSurfaceScatteringFlag.checked,
            'burleySampleCountFlag': highResSettings.elements.burleySampleCountFlag.checked
        },
        'output_settings_flags': {
            'outputDirectoryFlag': true,
            'fileNameFormatFlag': outputSettings.elements.fileNameFormatFlag.checked,
            'outputResolutionXFlag': outputSettings.elements.outputResolutionXFlag.checked,
            'outputResolutionYFlag': outputSettings.elements.outputResolutionYFlag.checked,
            'useCustomFrameRateFlag': outputSettings.elements.useCustomFrameRateFlag.checked,
            'outputFrameRateFlag': outputSettings.elements.outputFrameRateFlag.checked,
            'overrideExistingOutputFlag': outputSettings.elements.overrideExistingOutputFlag.checked,
            'zeroPadFrameNumbersFlag': outputSettings.elements.zeroPadFrameNumbersFlag.checked,
            'frameNumberOffsetFlag': outputSettings.elements.frameNumberOffsetFlag.checked,
            'handleFrameCountFlag': outputSettings.elements.handleFrameCountFlag.checked,
            'outputFrameStepFlag': outputSettings.elements.outputFrameStepFlag.checked,
            'useCustomPlaybackRangeFlag': outputSettings.elements.useCustomPlaybackRangeFlag.checked,
            'customStartFrameFlag': outputSettings.elements.customStartFrameFlag.checked,
            'customEndFrameFlag': outputSettings.elements.customEndFrameFlag.checked,
            'versionNumberFlag': outputSettings.elements.versionNumberFlag.checked,
            'autoVersionFlag': outputSettings.elements.autoVersionFlag.checked
        }
    }
    const settings = {
        'output_types': [],
        'render_types': [],
        'aa_settings': {
            'spatialSampleCount': aaSettings.elements.spatialSampleCount.value,
            'temporalSampleCount': aaSettings.elements.temporalSampleCount.value,
            'overrideAA': parseBools(aaSettings.elements.overrideAA.value),
            'aaMethod': aaSettings.elements.aaMethod.value,
            'useCameraCutForWarmUp': parseBools(aaSettings.elements.useCameraCutForWarmUp.value),
            'renderWarmUpFrames': parseBools(aaSettings.elements.renderWarmUpFrames.value),
            'renderWarmUpCount': aaSettings.elements.renderWarmUpCount.value,
            'engineWarmUpCount': aaSettings.elements.engineWarmUpCount.value
        },
        'console_settings': {
            'consoleVariables': parseConsoleVariables(consoleSettings.elements.consoleVariables.value),
            'startConsoleCommands': parseConsoleCommands(consoleSettings.elements.startConsoleCommands.value),
            'endConsoleCommands': parseConsoleCommands(consoleSettings.elements.endConsoleCommands.value)
        },
        'high_res_settings': {
            'tileCount': highResSettings.elements.tileCount.value,
            'textureSharpnessBias': highResSettings.elements.textureSharpnessBias.value,
            'overlapRatio': highResSettings.elements.overlapRatio.value,
            'overrideSubSurfaceScattering': parseBools(highResSettings.elements.overrideSubSurfaceScattering.value),
            'burleySampleCount': highResSettings.elements.burleySampleCount.value
        },
        'output_settings': {
            'outputDirectory': outputSettings.elements.outputDirectory.value,
            'fileNameFormat': outputSettings.elements.fileNameFormat.value,
            'outputResolutionX': outputSettings.elements.outputResolutionX.value,
            'outputResolutionY': outputSettings.elements.outputResolutionY.value,
            'useCustomFrameRate': parseBools(outputSettings.elements.useCustomFrameRate.value),
            'outputFrameRate': outputSettings.elements.outputFrameRate.value,
            'overrideExistingOutput': parseBools(outputSettings.elements.overrideExistingOutput.value),
            'zeroPadFrameNumbers': outputSettings.elements.zeroPadFrameNumbers.value,
            'frameNumberOffset': outputSettings.elements.frameNumberOffset.value,
            'handleFrameCount': outputSettings.elements.handleFrameCount.value,
            'outputFrameStep': outputSettings.elements.outputFrameStep.value,
            'useCustomPlaybackRange': parseBools(outputSettings.elements.useCustomPlaybackRange.value),
            'customStartFrame': outputSettings.elements.customStartFrame.value,
            'customEndFrame': outputSettings.elements.customEndFrame.value,
            'versionNumber': outputSettings.elements.versionNumber.value,
            'autoVersion': parseBools(outputSettings.elements.autoVersion.value)
        }
    }

    const formData = {
        'name': basicSettingsForm.elements.name.value,
        'owner': '',
        'worker': basicSettingsForm.elements.worker.value,
        'project_path': basicSettingsForm.elements.project_path.value,
        'level_path': basicSettingsForm.elements.level_path.value,
        'sequence_path': basicSettingsForm.elements.sequence_path.value,
        'config_path': basicSettingsForm.elements.config_path.value,
        'config_override': override,
        'render_settings': settings
    }

    eel.send_request(formData)(formCallBack)
}

const parseConsoleVariables = (text) => {
    const returnDict = {}

    const splitLines = text.split("\n")
    splitLines.forEach((line) => {
        const splitLine = line.split(":")
        if (splitLine.length === 2)
            returnDict[splitLine[0]] = splitLine[1]
    })

    return returnDict
}

const parseConsoleCommands = (text) => (text.split("\n"))

const parseBools = (value) => (value === "True")

const formCallBack = (res) => {
    if (res === "200")
        window.location.href = "landing.html"
    else {
        document.getElementById("notificationWrapper").hidden = false
        document.getElementById("notificationText").innerText = res
    }
}