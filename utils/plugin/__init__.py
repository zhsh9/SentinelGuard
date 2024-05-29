import os
import importlib
import inspect
from utils.plugin.template import PluginTemplate

# Collect all files under the current directory
plugin_dir = os.path.dirname(__file__)
plugin_files = [f for f in os.listdir(plugin_dir) if f.endswith('.py') and f not in ('__init__.py', 'template.py')]

# Init a container to store all plugin classes
plugin_classes = {}
for plugin_file in plugin_files:
    module_name = f'utils.plugin.{plugin_file[:-3]}'  # Create the full module name
    module = importlib.import_module(module_name)
    # Traverse all members inside each module, and find the classes that inherits from PluginTemplate
    for name, obj in inspect.getmembers(module, inspect.isclass):
        if issubclass(obj, PluginTemplate) and obj is not PluginTemplate:
            plugin_classes[name] = obj

__all__ = ['plugin_classes']
