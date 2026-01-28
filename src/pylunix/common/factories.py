from PyQt5.QtWidgets import QWidget

from .stylesheet import PyLunixStyleSheet

class StateColorResolver:
    @staticmethod
    def resolve(component: str, attribute: str, widget: QWidget, theme_type="BUTTON") -> str:
        is_enabled = widget.isEnabled()
        is_pressed = getattr(widget, "isPressed", False)
        is_hover = getattr(widget, "isHover", False)

        if not is_enabled: 
            state = "Disabled"
        elif is_pressed: 
            state = "Pressed"
        elif is_hover: 
            state = "PointerOver"
        else: 
            state = "" # Normal

        name = f"{component}{attribute}{state}"
        
        stylesheet_category = getattr(PyLunixStyleSheet, theme_type)
        return stylesheet_category.get_value(name)