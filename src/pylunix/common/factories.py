from PyQt5.QtWidgets import QWidget

from .stylesheet import PyLunixStyleSheet

class StateColorResolver:
    @staticmethod
    def resolve(component: str, attribute: str, widget: QWidget, theme_type="BUTTON") -> str:
        is_enabled = widget.isEnabled()
        is_pressed = getattr(widget, "isPressed", False)
        is_hover = getattr(widget, "isHover", False)

        is_checked = False
        if hasattr(widget, "isChecked"):
            is_checked = widget.isChecked()

        state_suffix = ""
        
        if is_checked:
            state_suffix = "Checked"
            if not is_enabled: state_suffix += "Disabled"
            elif is_pressed: state_suffix += "Pressed"
            elif is_hover: state_suffix += "PointerOver"
        else:
            if not is_enabled: state_suffix = "Disabled"
            elif is_pressed: state_suffix = "Pressed"
            elif is_hover: state_suffix = "PointerOver"
            else: state_suffix = "" # Normal state

        name = f"{component}{attribute}{state_suffix}"
        stylesheet_category = getattr(PyLunixStyleSheet, theme_type)
        return stylesheet_category.get_value(name)