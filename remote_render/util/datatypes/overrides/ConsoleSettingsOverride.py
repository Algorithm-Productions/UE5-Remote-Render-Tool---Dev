from ..abstracts.StorableProperty import StorableProperty


class ConsoleSettingsOverride(StorableProperty):
    UNREAL_MAPPINGS = {
        "consoleVariables": "console_variables",
        "startConsoleCommands": "start_console_commands",
        "endConsoleCommands": "end_console_commands"
    }

    def __init__(
            self,
            consoleVariablesFlag=False,
            startConsoleCommandsFlag=False,
            endConsoleCommandsFlag=False
    ):
        self.consoleVariablesFlag = consoleVariablesFlag
        self.startConsoleCommandsFlag = startConsoleCommandsFlag
        self.endConsoleCommandsFlag = endConsoleCommandsFlag

    @classmethod
    def from_dict(cls, data):
        consoleVariablesFlag = (data["consoleVariablesFlag"] or False) if data else False
        startConsoleCommandsFlag = (data["startConsoleCommandsFlag"] or False) if data else False
        endConsoleCommandsFlag = (data["endConsoleCommandsFlag"] or False) if data else False

        return cls(
            consoleVariablesFlag=consoleVariablesFlag,
            startConsoleCommandsFlag=startConsoleCommandsFlag,
            endConsoleCommandsFlag=endConsoleCommandsFlag
        )

    @classmethod
    def changeUnreal(cls, unrealObject, config, flags):
        #for key, val in config.items():
        #    if flags[key + "Flag"]:
        #        unrealObject[cls.UNREAL_MAPPINGS[key]] = val
        pass
