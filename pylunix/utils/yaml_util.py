import os
import yaml 
import threading
from types import SimpleNamespace 
from typing import Any, Dict, Optional

_FILE_CACHE: Dict[str, Dict[str, Any]] = {}
_CACHE_LOCK = threading.RLock()

class YAMLProcessor:
    def __init__(self, path: str):
        self.path = path
        data = self._load_file_cached(self.path)
        self.data = data or {}
        self.ns = self.dict_to_namespace(self.data)
        
#region Cache Helpers
    @staticmethod
    def _get_mtime(path: str) -> float:
        try:
            return os.path.getmtime(path)
        except Exception:
            return 0.0

    @classmethod
    def _load_file_cached(cls, path: str) -> Dict[str, Any]:
        path = str(path)
        with _CACHE_LOCK:
            mtime = cls._get_mtime(path)
            cached = _FILE_CACHE.get(path)
            if cached:
                if cached.get("mtime") == mtime:
                    return cached.get("data")
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
            except FileNotFoundError:
                data = {}
            _FILE_CACHE[path] = {"mtime": mtime, "data": data}
            return data

    @classmethod
    def clear_cache(cls):
        """Clear the internal file cache (useful for tests / dev)."""
        with _CACHE_LOCK:
            _FILE_CACHE.clear()

    @classmethod
    def force_reload(cls, path: str):
        """Force reload a specific file into cache (useful when you programmatically update a file)."""
        path = str(path)
        with _CACHE_LOCK:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
            except FileNotFoundError:
                data = {}
            mtime = cls._get_mtime(path)
            _FILE_CACHE[path] = {"mtime": mtime, "data": data}
            return data
        
#endregion

#region Basic Utilities
    def reload(self) -> Dict[str, Any]:
        """Reload the instance's path and update internal data/namespace."""
        newdata = self._load_file_cached(self.path) or {}
        self.data = newdata
        self.ns = self.dict_to_namespace(self.data)
        return self.data

    def yaml_to_dict(self) -> Dict[str, Any]:
        """Return the (cached) dict representation of the file."""
        return dict(self._load_file_cached(self.path) or {})
        
    def dict_to_namespace(self, obj: Any) -> Any:
        """Recursively convert dict->SimpleNamespace; lists preserved."""
        if isinstance(obj, dict):
            return SimpleNamespace(**{k: self.dict_to_namespace(v) for k, v in obj.items()})
        elif isinstance(obj, list):
            return [self.dict_to_namespace(item) for item in obj]
        else:
            return obj

    def yaml_to_namespace(self) -> SimpleNamespace:
        data = self._load_file_cached(self.path) or {}
        return self.dict_to_namespace(data)
#endregion

#region Resolving Helpers
    def resolve_value(self, value: Any) -> Any:
        """
        Expand {a.b.c} style tokens against self.data.
        If value is not a token string, return it unchanged.
        If token not found, return None (caller can fallback).
        """
        if not isinstance(value, str):
            return value

        if value.startswith("{") and value.endswith("}"):
            key_path = value.strip("{}").split(".")
            result = self.data
            for k in key_path:
                if isinstance(result, dict) and (k in result):
                    result = result[k]
                else:
                    return None
            return result
        return value

    def _get_theme_dict(self, theme: str) -> Dict[str, Any]:
        """Return the dict for a given theme inside self.data, or {}."""
        if not isinstance(self.data, dict):
            return {}
        theme_dict = self.data.get(theme)
        if isinstance(theme_dict, dict):
            return theme_dict
        alt = self.data.get("Themes")
        if isinstance(alt, dict):
            return alt.get(theme, {}) or {}
        return {}

    def resolve(self, path: str, theme: str = "Default") -> Dict[str, Any]:
        """
        Resolve a component YAML (path) using values from self.data (the theme resource).
        - Uses cached load for `path`
        - For each component entry, expand tokens with resolve_value()
        - Lookup values under the specified theme namespace (from self.data)
        Returns a dict: {component_key: resolved_value_or_original}
        """
        comp_data = self._load_file_cached(path) or {}
        resolved: Dict[str, Any] = {}

        theme_dict = self._get_theme_dict(theme)

        for comp, attrs in (comp_data.items() if isinstance(comp_data, dict) else []):
            keys = []
            if isinstance(attrs, str):
                keys = [self.resolve_value(attrs)]
            elif isinstance(attrs, list):
                keys = [self.resolve_value(v) for v in attrs]
            elif isinstance(attrs, dict):
                keys = [self.resolve_value(v) for v in attrs.values()]
            elif attrs is None:
                keys = []
            else:
                keys = [attrs]

            found = None
            for key in keys:
                if key is None:
                    continue
                if isinstance(key, (dict, list)):
                    found = key
                    break
                if isinstance(theme_dict, dict) and key in theme_dict:
                    found = theme_dict.get(key)
                    break
                if isinstance(key, str) and "." in key:
                    cur = theme_dict
                    ok = True
                    for part in key.split("."):
                        if isinstance(cur, dict) and part in cur:
                            cur = cur[part]
                        else:
                            ok = False
                            break
                    if ok:
                        found = cur
                        break
                if not isinstance(key, str) or (isinstance(key, str) and not key.startswith("{")):
                    found = key
                    break
            resolved[comp] = found if found is not None else attrs

        return resolved
#endregion