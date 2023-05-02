import config

prefix = config.prefix

def command_response(command):
    return command.replace(prefix+'echo ','')