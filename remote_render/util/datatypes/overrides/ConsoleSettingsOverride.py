from ..abstracts.UnrealOverride import UnrealOverride


class ConsoleSettingsOverride(UnrealOverride):
    UNREAL_MAPPINGS = {
        "consoleVariables": ["console_variables", "map"],
        "startConsoleCommands": ["start_console_commands", "array"],
        "endConsoleCommands": ["end_console_commands", "array"]
    }
    UNREAL_SETTING_KEY = "console"

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
