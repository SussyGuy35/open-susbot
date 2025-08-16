import enum

class HelpSection(enum.Enum):
    CORE = 1
    GENERAL = 2
    GENERAL2 = 3
    FUN = 4
    MODERATION = 5


class CommandType(enum.Enum):
    PREFIX = 1
    SLASH = 2
    HYBRID = 3


class CommandParameterDescription:
    def __init__(self, name: str, description: str, required: bool = True):
        self.name = name
        self.description = description
        self.required = required


class CommandHelp:
    def __init__(self, command_name: str, command_type: CommandType, description: str, usage: str, parameters: list[CommandParameterDescription] | None = None, aliases: list[str] | None = None):
        self.command_name = command_name
        self.command_type = command_type
        self.description = description
        self.usage = usage
        self.parameters = parameters
        self.aliases = aliases


class CommandHelpGroup(CommandHelp):
    def __init__(self, group_name: str, command_type: CommandType, description: str, usage: str, commands: list[CommandHelp], aliases: list[str] | None = None):
        super().__init__(group_name, command_type, description, usage, aliases=aliases)
        self.commands = commands


class HelpManager:
    commands_help: dict[int, list[CommandHelp]] = {
        HelpSection.CORE.value: [],
        HelpSection.GENERAL.value: [],
        HelpSection.GENERAL2.value: [],
        HelpSection.FUN.value: [],
        HelpSection.MODERATION.value: []
    }


    @classmethod
    def add_command_help(cls, command_help: CommandHelp, section: HelpSection):
        cls.commands_help[section.value].append(command_help)


    @classmethod
    def get_commands_help_section(cls, section: HelpSection) -> list[CommandHelp]:
        return cls.commands_help.get(section.value, [])


    @classmethod
    def get_command_help(cls, command_name: str) -> CommandHelp | None:
        for section in cls.commands_help.values():
            for command_help in section:
                if (
                    command_help.command_name == command_name
                    or (command_help.aliases and command_name in command_help.aliases)
                ):
                    return command_help
                

        return None
