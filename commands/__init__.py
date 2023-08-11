import os
import importlib

__globals = globals()

for file in os.listdir(os.path.dirname(__file__)):
    if file != "__init__.py" and file[len(file)-3:] == ".py":
        mod_name = file[:-3]   # strip .py at the end
        __globals[mod_name] = importlib.import_module('.' + mod_name, package=__name__)
        print("Loaded module:", mod_name)