import config, random
prefix = config.prefix

def command_response(command):
    user_input = command.replace(prefix+'randcaps','')
    message_output = []
    for i in range(len(user_input)):
        char = user_input[i]
        char = [char.lower(),char.upper()]
        message_output.append(random.choice(char))
    return ''.join(message_output)
