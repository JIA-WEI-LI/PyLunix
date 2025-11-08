import os
from enum import Enum
from .theme_manager import ThemeManager
from ..utils.yaml_util import YAMLProcessor

theme_manager = ThemeManager.get_instance()

class PyLunixStyleSheet(Enum):
    def __new__(cls, value, components_dir):
        obj = object.__new__(cls)
        obj._value_ = value
        obj._components_dir = components_dir
        return obj
    
    BUTTON = "button", "controls"

    def apply(self, widget, register=True):
        widget.setObjectName(self.value)
        components_dir = self._components_dir
        if register:
            theme_manager.register(widget, components_dir, self.value)

    def get_value(self, name:str, components_dir:str=None):
        components_dir = self._components_dir if components_dir is None else components_dir
        return theme_manager.get_resolved_value(name, components_dir, self.value)