from PyQt5.QtWidgets import QWidget

from .stylesheet import PyLunixStyleSheet

class StateColorResolver:
    @staticmethod
    def resolve(component: str, property_name: str, widget: QWidget, theme_type="BUTTON") -> str:
        state_suffix = ""
        if not widget.isEnabled():
            state_suffix = "Disabled"
        elif getattr(widget, "isPressed", False):
            state_suffix = "Pressed"
        elif getattr(widget, "isHover", False):
            state_suffix = "PointerOver"
        else:
            state_suffix = ""

        variable_name = f"{component}{property_name}{state_suffix}"
        stylesheet_category = getattr(PyLunixStyleSheet, theme_type)
        return stylesheet_category.get_value(variable_name)