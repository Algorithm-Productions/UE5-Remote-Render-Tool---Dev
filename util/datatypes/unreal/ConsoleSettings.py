from util.datatypes.abstracts.UnrealDataType import UnrealDataType


class ConsoleSettings(UnrealDataType):
    def __init__(
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
        consoleVariables = (data["consoleVariables"] or {}) if data else {}
        startConsoleCommands = (data["consoleVariables"] or []) if data else []
        endConsoleCommands = (data["endConsoleCommands"] or []) if data else []

        return cls(
            consoleVariables=consoleVariables,
            startConsoleCommands=startConsoleCommands,
            endConsoleCommands=endConsoleCommands
        )

    @classmethod
    def from_unreal(cls, unrealClass):
        return cls(
            consoleVariables=str(unrealClass.console_variables),
            startConsoleCommands=str(unrealClass.start_console_commands),
            endConsoleCommands=str(unrealClass.end_console_commands)
        )
