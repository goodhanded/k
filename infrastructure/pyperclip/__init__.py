import pkgutil
import importlib

# Dynamically import all submodules in the infrastructure.pyperclip package
__all__ = [name for _, name, _ in pkgutil.iter_modules(__path__)]
for module in __all__:
    importlib.import_module("." + module, package=__name__)
