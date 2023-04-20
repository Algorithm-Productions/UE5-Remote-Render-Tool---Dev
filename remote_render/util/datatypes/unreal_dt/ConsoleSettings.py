"""
    Copyright Algorithm Productions LLC. 2023.
"""

from ..abstracts.UnrealDataType import UnrealDataType


class ConsoleSettings(UnrealDataType):
    """
        Python Form of the unreal.MoviePipelineConsoleVariableSetting Class.

        :type: UnrealDataType.
        :author: vitor@bu.edu.
    """

    def __init__(
            self,
            consoleVariables=None,
            startConsoleCommands=None,
            endConsoleCommands=None
    ):
        """
            Class Constructor.
            Takes in every Parameter as an Optional, allowing for the creation of Empty Objects.

            :param consoleVariables: Map of Variables that are used in Console Commands.
            :type consoleVariables: Dictionary.
            :param startConsoleCommands: List of Commands to run at the Start of each Render.
            :type startConsoleCommands: List of Strings.
            :param endConsoleCommands: List of Commands to run at the End of each Render.
            :type endConsoleCommands: List of Strings.
        """
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
        """
            @inheritDoc - UnrealDataType
        """
        consoleVariables = (dict(data["consoleVariables"]) or {}) if data else {}
        startConsoleCommands = (list(data["startConsoleCommands"]) or []) if data else []
        endConsoleCommands = (list(data["endConsoleCommands"]) or []) if data else []

        return cls(
            consoleVariables=consoleVariables,
            startConsoleCommands=startConsoleCommands,
            endConsoleCommands=endConsoleCommands
        )

    @classmethod
    def from_unreal(cls, unrealClass):
        """
            @inheritDoc - UnrealDataType
        """
        return cls(
            consoleVariables=dict(unrealClass.console_variables),
            startConsoleCommands=list(unrealClass.start_console_commands),
            endConsoleCommands=list(unrealClass.end_console_commands)
        )
