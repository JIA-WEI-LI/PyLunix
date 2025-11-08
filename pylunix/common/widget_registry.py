import weakref
from pathlib import Path
import logging
from typing import Dict, Set

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
            
        qss_path = Path("pylunix/controls") / component_name / f"{component_name}.qss"
        
        if qss_path.exists():
            self._existing_qss_paths[component_name] = qss_path
            return qss_path
        else:
            self._missing_qss_components.add(component_name)
            logger.warning("[widget_registry] QSS file not found for component '%s': %s", component_name, qss_path)
            return None

    def register(self, widget, component_name: str | None = None):
        if widget in self._widgets:
            self._widgets[widget] = component_name
            return

        self._widgets[widget] = component_name

        applied = False
        
        qss_path = self._get_qss_path(component_name)
        if qss_path:
            try:
                qss_content = self._qss_manager.apply_to_file(str(qss_path))
                widget.setStyleSheet(qss_content)
                applied = True
            except Exception as e:
                logger.exception("Failed to apply qss for %s: %s", qss_path, e)
        if not applied:
            qss_path_prop = widget.property("qss_path")
            if qss_path_prop:
                qss_path_prop = Path(str(qss_path_prop))
                if qss_path_prop.exists():
                    try:
                        qss_content = self._qss_manager.apply_to_file(str(qss_path_prop))
                        widget.setStyleSheet(qss_content)
                        applied = True
                    except Exception:
                        logger.exception("Failed to apply qss from widget property qss_path=%s", qss_path_prop)

        if not applied:
            logger.debug("No QSS applied for widget %r (component=%r).", widget, component_name)

    def update_all(self):
        for widget, component_name in list(self._widgets.items()):
            if widget is None:
                continue
            
            applied = False
            qss_path = self._get_qss_path(component_name)
            if qss_path:
                try:
                    qss_content = self._qss_manager.apply_to_file(str(qss_path))
                    widget.setStyleSheet(qss_content)
                    applied = True
                except Exception:
                    logger.exception("Failed to reapply qss for %s", qss_path)
            
            if not applied:
                qss_path_prop = widget.property("qss_path")
                if qss_path_prop:
                    # (此處省略了快取，但理想情況下也應該快取)
                    qss_path_prop = Path(str(qss_path_prop))
                    if qss_path_prop.exists():
                        try:
                            qss_content = self._qss_manager.apply_to_file(str(qss_path_prop))
                            widget.setStyleSheet(qss_content)
                            applied = True
                        except Exception:
                            logger.exception("Failed to reapply qss from widget property %s", qss_path_prop)
            if not applied:
                logger.debug("Skipped reapplying QSS for widget %r (component=%r).", widget, component_name)
                
            if hasattr(widget, 'updateIcon'):
                try:
                    widget.updateIcon()
                except Exception:
                    logger.exception("Failed to call update_icon on widget %r", widget)