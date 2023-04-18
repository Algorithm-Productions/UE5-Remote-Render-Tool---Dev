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
        """
            @inheritDoc - UnrealDataType
        """
        return cls(
            consoleVariables=str(unrealClass.console_variables),
            startConsoleCommands=str(unrealClass.start_console_commands),
            endConsoleCommands=str(unrealClass.end_console_commands)
        )
