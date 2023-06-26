import random

def command_response(command):
    options = command.split(',')
    return random.choice(options)
