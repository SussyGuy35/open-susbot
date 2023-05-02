import config, random
prefix = config.prefix

def command_response(command):
    options = command.replace(prefix+'pick','').split(',')
    return random.choice(options)
