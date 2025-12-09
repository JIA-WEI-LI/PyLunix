import os
from enum import Enum

from .typography import PyLnuixTypography, TypographyStyle
from .theme_manager import ThemeManager
from ..utils.yaml_util import YAMLProcessor

theme_manager = ThemeManager.get_instance()

class PyLunixStyleSheet(Enum):
    def __new__(cls, value, components_dir, typography_style):
        obj = object.__new__(cls)
        obj._value_ = value
        obj._components_dir = components_dir
        obj._typography_style = typography_style
        return obj
    
    BUTTON = "button", "controls", TypographyStyle.BODY
    CHECK_BOX = "check_box", "controls", TypographyStyle.BODY
    HYPERLINK_BUTTON = "hyperlink_button", "controls", TypographyStyle.BODY
    LIST_BOX = "list_box", "controls", TypographyStyle.BODY
    PASSWORD_BOX = "password_box", "controls", TypographyStyle.BODY
    RADIO_BUTTON = "radio_button", "controls", TypographyStyle.BODY
    REPEAT_BUTTON = "repeat_button", "controls", TypographyStyle.BODY
    RICHTEXT_BLOCK = "richtext_block", "controls", TypographyStyle.BODY
    TEXT_BLOCK = "text_block", "controls", TypographyStyle.BODY
    TEXT_BOX = "text_box", "controls", TypographyStyle.BODY
    TOGGLE_BUTTON = "toggle_button", "controls", TypographyStyle.BODY
    TOOL_BUTTON = "tool_button", "controls", TypographyStyle.BODY

    def apply(self, widget, register=True):
        widget.setObjectName(self.value)
        components_dir = self._components_dir

        if register:
            theme_manager.register(widget, components_dir, self.value)

        try:
            widget.setFont(PyLnuixTypography.get_font(self._typography_style))
        except Exception as e:
            print("[stylesheet.py] : " + e)

    def get_value(self, name:str, components_dir:str=None):
        components_dir = self._components_dir if components_dir is None else components_dir
        return theme_manager.get_resolved_value(name, components_dir, self.value)