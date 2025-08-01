class CommandParameterDescription:
    def __init__(self, name: str, description: str, required: bool = True):
        self.name = name
        self.description = description
        self.required = required

class CommandHelp:
    def __init__(self, command_name: str, description: str, usage: str, parameters: list[CommandParameterDescription] | None = None):
        self.command_name = command_name
        self.description = description
        self.usage = usage
        self.parameters = parameters

class HelpManager:
    commands_help: list[CommandHelp] = []
    
    @classmethod
    def add_command_help(cls, command_help: CommandHelp):
        cls.commands_help.append(command_help)
