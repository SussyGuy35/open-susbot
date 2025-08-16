import discord
from lib.sussyutils import get_prefix
from lib.locareader import get_string_by_id
import lib.sussyhelper as ssyhelper

loca_sheet = "loca/loca - help.csv"

cmd_names = ["help", "h", "gethelp"]

# add help entry for this command
ssyhelper.HelpManager.add_command_help(
    ssyhelper.CommandHelp(
        command_name="help",
        command_type=ssyhelper.CommandType.HYBRID,
        description=get_string_by_id(loca_sheet, "help_cmd_desc"),
        usage=get_string_by_id(loca_sheet, "help_cmd_usage"),
        parameters=[
            ssyhelper.CommandParameterDescription(
                name="option",
                description=get_string_by_id(loca_sheet, "help_param_option_desc"),
                required=False
            ),
            ssyhelper.CommandParameterDescription(
                name="subcommand",
                description=get_string_by_id(loca_sheet, "help_param_subcommand_desc"),
                required=False
            )
        ],
        aliases=cmd_names[1:]
    ),
    ssyhelper.HelpSection.CORE
)

# command logic

pages = [
    ssyhelper.HelpSection.CORE,
    ssyhelper.HelpSection.GENERAL,
    ssyhelper.HelpSection.GENERAL2,
    ssyhelper.HelpSection.FUN,
    ssyhelper.HelpSection.MODERATION
]


def parse_command_args(args: list[str]) -> ssyhelper.HelpSection | str | None:
    if len(args) < 1:
        return None
    
    try:
        index = int(args[0]) - 1
        if 0 <= index < len(pages):
            return pages[index]
        else:
            return None
    except ValueError:
        return args[0]  # Return the command name if it's not an index


def get_command_name(name: str, command_type: ssyhelper.CommandType, parameters: list[ssyhelper.CommandParameterDescription] | None, prefix: str | None = None) -> str:
    if command_type == ssyhelper.CommandType.PREFIX:
        if prefix is None:
            raise ValueError("Prefix must be provided for prefix commands.")
        para_str = ""
        if parameters:
            para_str = " " + " ".join(f"<{param.name}>" if param.required else f"[{param.name}]" for param in parameters)
        return f"`{prefix}{name}{para_str}`"
    elif command_type == ssyhelper.CommandType.SLASH:
        return f"`/{name}`"
    elif command_type == ssyhelper.CommandType.HYBRID:
        if prefix is None:
            raise ValueError("Prefix must be provided for hybrid commands.")
        para_str = ""
        if parameters:
            para_str = " " + " ".join(f"<{param.name}>" if param.required else f"[{param.name}]" for param in parameters)
        return f"`{prefix}{name}{para_str}`, `/{name}`"


def get_sub_command_name(name: str, parent_name: str, command_type: ssyhelper.CommandType, parameters: list[ssyhelper.CommandParameterDescription] | None, prefix: str | None = None) -> str:
    if command_type == ssyhelper.CommandType.PREFIX:
        if prefix is None:
            raise ValueError("Prefix must be provided for prefix commands.")
        para_str = ""
        if parameters:
            para_str = " " + " ".join(f"<{param.name}>" if param.required else f"[{param.name}]" for param in parameters)
        return f"`{prefix}{parent_name} {name}{para_str}`"
    elif command_type == ssyhelper.CommandType.SLASH:
        return f"`/{parent_name}_{name}`"
    elif command_type == ssyhelper.CommandType.HYBRID:
        if prefix is None:
            raise ValueError("Prefix must be provided for hybrid commands.")
        para_str = ""
        if parameters:
            para_str = " " + " ".join(f"<{param.name}>" if param.required else f"[{param.name}]" for param in parameters)
        return f"`{prefix}{parent_name} {name}{para_str}`, `/{parent_name}_{name}`"


def get_help_text(section: ssyhelper.HelpSection, prefix: str) -> discord.Embed:
    response = discord.Embed(
        title=get_string_by_id(loca_sheet, "help_title"),
        color=discord.Color.blurple()
    )
    response.set_footer(text=get_string_by_id(loca_sheet, "help_footer").format(pages.index(section) + 1, len(pages)) + " | " + get_string_by_id(loca_sheet, "help_footer2").format(prefix))

    commands = ssyhelper.HelpManager.get_commands_help_section(section)
    for command in commands:
        if isinstance(command, ssyhelper.CommandHelpGroup):
            response.add_field(
                name=f"{get_string_by_id(loca_sheet, "commands_group")}: {get_command_name(command.command_name, command.command_type, command.parameters, prefix)}",
                value=command.description,
                inline=False
            )
        else:
            response.add_field(
                name=get_command_name(command.command_name, command.command_type, command.parameters, prefix),
                value=command.description,
                inline=False
            )
    
    return response


def get_command_help_text(command_name: str, prefix: str) -> discord.Embed:
    command = ssyhelper.HelpManager.get_command_help(command_name)
    if command is None:
        return discord.Embed(
            title=get_string_by_id(loca_sheet, "help_invalid_command"),
            description=get_string_by_id(loca_sheet, 'help_invalid_command_desc'),
            color=discord.Color.red()
        )

    # command group

    if isinstance(command, ssyhelper.CommandHelpGroup):
        response = discord.Embed(
            title=f"{get_string_by_id(loca_sheet, "commands_group")}: {get_command_name(command.command_name, command.command_type, command.parameters, prefix)}",
            description=command.description,
            color=discord.Color.blurple()
        )

        response.add_field(
            name=get_string_by_id(loca_sheet, "help_usage"),
            value=command.usage
        )

        if command.aliases:
            aliases = ", ".join(f"`{alias}`" for alias in command.aliases)
            response.add_field(name=get_string_by_id(loca_sheet, "help_aliases"), value=aliases)
        
        response.add_field(
            name=get_string_by_id(loca_sheet, "help_commands_in_group"),
            value="\n".join(
                f"`{cmd.command_name}` - {cmd.description}" for cmd in command.commands
            )
        )
        return response
    

    response = discord.Embed(
        title=get_command_name(command.command_name, command.command_type, command.parameters, prefix),
        description=command.description,
        color=discord.Color.blurple()
    )
    response.add_field(
        name=get_string_by_id(loca_sheet, "help_usage"),
        value=command.usage
    )

    if command.parameters:
        params = "\n".join(
            f"{'**[*]**' if param.required else ''} `{param.name}` - {param.description}".strip() for param in command.parameters
        )
        response.add_field(name=get_string_by_id(loca_sheet, "help_parameters"), value=params)

    if command.aliases:
        aliases = ", ".join(f"`{alias}`" for alias in command.aliases)
        response.add_field(name=get_string_by_id(loca_sheet, "help_aliases"), value=aliases)
    
    return response


def get_sub_command_help_text(parent_command_name: str, command_name: str, prefix: str) -> discord.Embed:
    command = ssyhelper.HelpManager.get_command_help(parent_command_name)
    if command is None or not isinstance(command, ssyhelper.CommandHelpGroup):
        return discord.Embed(
            title=get_string_by_id(loca_sheet, "help_invalid_command"),
            description=get_string_by_id(loca_sheet, 'help_invalid_command_desc'),
            color=discord.Color.red()
        )
    sub_command = next((cmd for cmd in command.commands if cmd.command_name == command_name), None)
    if sub_command is None:
        return discord.Embed(
            title=get_string_by_id(loca_sheet, "help_invalid_subcommand"),
            description=get_string_by_id(loca_sheet, 'help_invalid_subcommand_desc').format(command_name),
            color=discord.Color.red()
        )
    response = discord.Embed(
        title=get_sub_command_name(sub_command.command_name, command.command_name, sub_command.command_type, sub_command.parameters, prefix),
        description=sub_command.description,
        color=discord.Color.blurple()
    )

    response.add_field(
        name=get_string_by_id(loca_sheet, "help_usage"),
        value=sub_command.usage
    )

    if sub_command.parameters:
        params = "\n".join(
            f"{'**[*]**' if param.required else ''} `{param.name}` - {param.description}".strip() for param in sub_command.parameters
        )
        response.add_field(name=get_string_by_id(loca_sheet, "help_parameters"), value=params)
    
    if sub_command.aliases:
        aliases = ", ".join(f"`{alias}`" for alias in sub_command.aliases)
        response.add_field(name=get_string_by_id(loca_sheet, "help_aliases"), value=aliases)
    
    return response


async def command_listener(message: discord.Message, args: list[str]):
    prefix = get_prefix(message.guild) if message.guild else get_prefix(None)
    option = parse_command_args(args)
    if option is None:
        await message.channel.send(embed=get_help_text(ssyhelper.HelpSection.CORE, prefix))
        return
    if isinstance(option, str):
        if len(args) > 1:
            sub_command = args[1]
            await message.channel.send(embed=get_sub_command_help_text(option, sub_command, prefix))
            return
        await message.channel.send(embed=get_command_help_text(option, prefix))
        return

    await message.channel.send(embed=get_help_text(option, prefix))


async def slash_command_listener(ctx: discord.Interaction, option: str | None = None, subcommand: str | None = None):
    await ctx.response.defer()
    print(f"{ctx.user} used help commands!")
    prefix = get_prefix(ctx.guild) if ctx.guild else get_prefix(None)
    if option is None:
        await ctx.followup.send(embed=get_help_text(ssyhelper.HelpSection.CORE, prefix), ephemeral=True)
    else:
        opt = parse_command_args([option])
        
        if opt is None:
            await ctx.followup.send(embed=get_help_text(ssyhelper.HelpSection.CORE, prefix), ephemeral=True)
            return
        
        if isinstance(opt, str):
            if subcommand:
                await ctx.followup.send(embed=get_sub_command_help_text(opt, subcommand, prefix), ephemeral=True)
                return
            await ctx.followup.send(embed=get_command_help_text(option, prefix), ephemeral=True)
            return
        
        await ctx.followup.send(embed=get_help_text(opt, prefix), ephemeral=True)
