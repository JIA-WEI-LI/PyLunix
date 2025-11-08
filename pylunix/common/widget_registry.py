import weakref
from pathlib import Path
import logging
from typing import Dict, Set

from ..config.path import component_qss_path

logger = logging.getLogger("WidgetRegistry")

class WidgetRegistry:
    def __init__(self, qss_manager):
        self._widgets = weakref.WeakKeyDictionary()
        self._qss_manager = qss_manager

        self._existing_qss_paths: Dict[str, Path] = {}
        self._missing_qss_components: Set[str] = set()

    def _get_qss_path(self, component_name: str) -> Path | None:
        if not component_name:
            return None
        
        if component_name in self._existing_qss_paths:
            return self._existing_qss_paths[component_name]
        
        if component_name in self._missing_qss_components:
            return None
            
        qss_path = component_qss_path("controls", component_name)
        
        if qss_path.exists():
            self._existing_qss_paths[component_name] = qss_path
            return qss_path
        else:
            self._missing_qss_components.add(component_name)
            logger.warning("[widget_registry] QSS file not found for component '%s': %s", component_name, qss_path)
            return None

    def register(self, widget, component_name: str | None = None):
        self._widgets[widget] = component_name

        applied = self._apply_qss(widget, component_name)

        if not applied:
            logger.debug("No QSS applied for widget %r (component=%r).", widget, component_name)

        if not applied:
            logger.debug("No QSS applied for widget %r (component=%r).", widget, component_name)

    def _apply_qss(self, widget, component_name: str | None) -> bool:
        applied = False

        qss_path = self._get_qss_path(component_name)
        if qss_path:
            applied = self._apply_qss_from_path(widget, qss_path)

        if not applied:
            qss_path_prop = widget.property("qss_path")
            if qss_path_prop:
                qss_path_prop = Path(str(qss_path_prop))
                if qss_path_prop.exists():
                    applied = self._apply_qss_from_path(widget, qss_path_prop)
        return applied
    
    def _apply_qss_from_path(self, widget, qss_path: Path) -> bool:
        try:
            qss_content = self._qss_manager.apply_to_file(str(qss_path))
            widget.setStyleSheet(qss_content)
            return True
        except Exception:
            logger.exception("Failed to apply QSS from %s", qss_path)
            return False

    def update_all(self):
        for widget, component_name in list(self._widgets.items()):
            if widget is None:
                continue

            applied = self._apply_qss(widget, component_name)

            if not applied:
                logger.debug("Skipped reapplying QSS for widget %r (component=%r).", widget, component_name)

            if hasattr(widget, 'updateIcon'):
                try:
                    widget.updateIcon()
                except Exception:
                    logger.exception("Failed to call updateIcon on widget %r", widget)