"""Init commands."""
from os.path import dirname, basename, isfile, join
import glob
import importlib
import logging

# Initialize an empty dictionary for modules and alias-to-command mapping
modules = {}
alias_to_command = {}


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
        modules[mod.command] = mod
        alias_to_command[mod.command] = mod.command  # Map the command to itself
        aliases = getattr(mod, 'aliases', [])  # Safely get the aliases attribute, default to an empty list
        for alias in aliases:
            alias_to_command[alias] = mod.command  # Map each alias to the main command

# Export modules and alias_to_command for use in other scripts
__all__.extend(['modules', 'alias_to_command'])
