import config, random
prefix = config.prefix

def command_response(command):
    user_input = command.replace(prefix+'randcaps','')
    message_output = []
    for i in range(len(user_input)):
        char = user_input[i]
        chooses = [char.lower(),char.upper()]
        message_output.append(random.choice(chooses))
    return ''.join(message_output)