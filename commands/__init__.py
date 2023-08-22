"""Init commands."""
from os.path import dirname, basename, isfile, join
import glob
import importlib


def load_module(name):
    """Load module with the given name."""
    try:
        module = importlib.import_module(f".{name}", '.commands')
    except ModuleNotFoundError:
        print(f"Module '{name}' not found")
        # exit(1)
    else:
        return module


__all__ = [
    basename(f)[:-3]
    for f in glob.glob(join(dirname(__file__), "*.py"))
    if isfile(f) and not f.endswith('__init__.py')
]

modules = {}
for module in __all__:
    mod = load_module(module)
    modules[mod.command] = mod
