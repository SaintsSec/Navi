"""Init commands."""
from os.path import dirname, basename, isfile, join
import glob
import importlib
import logging

# Initialize an empty dictionary for modules, alias-to-command mapping, and command usage
modules = {}
alias_to_command = {}
command_usage = {}


def load_module(name):
    """Load module with the given name."""
    try:
        module = importlib.import_module(f".{name}", 'commands')
    except ModuleNotFoundError:
        print(f"Module '{name}' not found")
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s %(levelname)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            filename="logs/error.log",
        )

        logging.error(f"Module '{name}' not found")
        # exit(1)
    else:
        return module


__all__ = [
    basename(f)[:-3]
    for f in glob.glob(join(dirname(__file__), "*.py"))
    if isfile(f) and not f.endswith('__init__.py')
]

for module_name in __all__:
    mod = load_module(module_name)
    if mod:
        if hasattr(mod, 'command'):
            modules[mod.command] = mod
            alias_to_command[mod.command] = mod.command  # Map the command to itself
            aliases = getattr(mod, 'aliases', [])  # Safely get the aliases attribute, default to an empty list
            for alias in aliases:
                alias_to_command[alias] = mod.command  # Map each alias to the main command
            use = getattr(mod, 'use', None)  # Safely get the use attribute, default to None
            if use:
                command_usage[mod.command] = use
        else:
            print(f"Warning: The module '{module_name}' is not installed correctly. Ignoring module.")

# Export modules, alias_to_command, and command_usage for use in other scripts
__all__.extend(['modules', 'alias_to_command', 'command_usage'])
