import os
from pathlib import Path
from typing import Any, Dict, Union, Set
import logging
import threading

from .widget_registry import WidgetRegistry
from ..utils.yaml_util import YAMLProcessor
from ..utils.qss_utils import QSSProcessor

logger = logging.getLogger("ThemeManager")

class ThemeManager:
    _instance = None
    _CACHE_LOCK = threading.RLock()

    _RESOLVED_CACHE: Dict[str, Dict[str, Any]] = {}
    _RAW_DATA_CACHE: Dict[str, Dict[str, Any]] = {}
    _COMMON_DICT_CACHE: Dict[str, Any] = None

    _LOADED_COMPONENTS: Set[str] = set()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.theme = "Default"

        self.common_yaml_path = Path(__file__).parent.parent / "resources" / "common_themeresources_any.yaml"

        self.yaml_processor = YAMLProcessor(str(self.common_yaml_path))
        self._COMMON_DICT_CACHE = self.yaml_processor.yaml_to_dict()
        self.component_resources: Dict[str, str] = dict(self._COMMON_DICT_CACHE)
        # self.component_resources: Dict[str, str] = dict(self.yaml_processor.yaml_to_dict())
        self.qss_processor = QSSProcessor(self.component_resources)
        self.widget_registry = WidgetRegistry(self.qss_processor)

    def register(self, widget, components_dir: str, component_name: str):
        self.load_component(components_dir, component_name)
        self.widget_registry.register(widget, component_name)
    
    def load_component(self, components_dir: str, component_name: str):

        with self._CACHE_LOCK:
            if component_name in self._LOADED_COMPONENTS:
                return
            
        resolved_data, yaml_path = self.get_resolved_data_and_path(components_dir, component_name)

        for name, value in resolved_data.items():
            if value is None:
                value = self.get_default_value(yaml_path, name)
            self.component_resources[name] = value

        self.qss_processor.set_variables(self.component_resources)

        with self._CACHE_LOCK:
            self._LOADED_COMPONENTS.add(component_name)

        return value
    
    def get_resolved_value(self, name: str, components_dir: str, component_name: str):
        resolved_data, yaml_path = self.get_resolved_data_and_path(components_dir, component_name)

        value = resolved_data.get(name)
        if value is None:
            value = self.get_default_value(yaml_path, name)
        return value
    
    def get_resolved_data_and_path(self, components_dir: str, component_name: str):
        with self._CACHE_LOCK:
            if component_name in self._RESOLVED_CACHE:
                cached = self._RESOLVED_CACHE[component_name]
                return cached["data"], cached["path"]

            DIR = os.path.dirname(os.path.dirname(__file__))
            yaml_path = os.path.join(DIR, components_dir, component_name, f"{component_name}.yaml")

            process = YAMLProcessor(self.common_yaml_path)
            resolved_data = process.resolve(yaml_path, self.theme)

            self._RESOLVED_CACHE[component_name] = {"data": resolved_data, "path": yaml_path}

            return resolved_data, yaml_path
    
    def get_default_value(self, yaml_path: str, name: str):
        raw_data = None
        with self._CACHE_LOCK:
            if yaml_path in self._RAW_DATA_CACHE:
                raw_data = self._RAW_DATA_CACHE[yaml_path]
            else:
                old_processor = YAMLProcessor(yaml_path)
                raw_data = old_processor.yaml_to_dict()
                self._RAW_DATA_CACHE[yaml_path] = raw_data

        value = raw_data.get(name)
        if isinstance(value, str):
            value = self._COMMON_DICT_CACHE.get(value, value)

        return value
    
    def set_theme(self, theme: str="Default"):
        if self.theme == theme:
            return 
        self.theme = theme

        with self._CACHE_LOCK:
            self._RESOLVED_CACHE.clear()
            components_to_reload = list(self._LOADED_COMPONENTS)
            self._LOADED_COMPONENTS.clear()

        for component_name in components_to_reload:
            self.load_component("controls", component_name)

        self.widget_registry.update_all()
