from typing import Union, Callable
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon

from ..button.button import BaseButton
from ...common.stylesheet import PyLunixStyleSheet

class ToggleButton(BaseButton):
    def __init__(self, text: str = "", icon: QIcon = None, parent: QWidget = None):
        super().__init__(text=text, icon=icon, parent=parent)
        self._text_on = None
        self._text_off = None
        self._icon_on = None
        self._icon_off = None
        
        self._postInit()
        self.setProperty("class", "ToggleButton")
        PyLunixStyleSheet.TOGGLE_BUTTON.apply(self)
        
    def _postInit(self):
        self.setCheckable(True)
        self.setChecked(False)
        self.toggled.connect(self._on_toggle_state_changed)

    def setToggleIcons(self, icon_on: Union[QIcon, Callable], icon_off: Union[QIcon, Callable]):
        self._icon_on = icon_on
        self._icon_off = icon_off
        self._applyToggle()

    def setToggleText(self, text_on: str, text_off: str):
        self._text_on = text_on
        self._text_off = text_off
        self._applyToggle()

    def setChecked(self, checked: bool):
        super().setChecked(checked)
        self._applyToggle()
        self.updateIcon()

    def _get_icon_color(self) -> str:
        if self.isChecked():
            if not self.isEnabled():
                name = "ToggleButtonForegroundCheckedDisabled"
            elif self.isPressed:
                name = "ToggleButtonForegroundCheckedPressed"
            elif self.isHover:
                name = "ToggleButtonForegroundCheckedPointerOver"
            else:
                name = "ToggleButtonForegroundChecked"
        elif not self.isEnabled():
            name = "ToggleButtonForegroundDisabled"
        elif self.isPressed:
            name = "ToggleButtonForegroundPressed"
        elif self.isHover:
            name = "ToggleButtonForegroundPointerOver"
        else:
            name = "ToggleButtonForeground"
        return PyLunixStyleSheet.TOGGLE_BUTTON.get_value(name)
        
    def _applyToggle(self):
        if self._text_on and self._text_off:
            text = self._text_on if self.isChecked() else self._text_off
            self.setText(text)

        if self._icon_on and self._icon_off:
            icon = self._icon_on if self.isChecked() else self._icon_off
            if callable(icon):
                self.setIconSource(icon)
            else:
                self.setIcon(icon)

    def _on_toggle_state_changed(self, checked: bool):
        self._applyToggle()
        self.updateIcon()

class TransparentToggleButton(ToggleButton):
    def __init__(self, text: str = "", icon: QIcon = None, parent: QWidget = None):
        super().__init__(text=text, icon=icon, parent=parent)
        self.setProperty("class", "TransparentToggleButton")
        PyLunixStyleSheet.TOGGLE_BUTTON.apply(self)

class SegmentedButton(ToggleButton):
    def __init__(self, text: str = "", icon: QIcon = None, parent: QWidget = None):
        super().__init__(text=text, icon=icon, parent=parent)
        self.setProperty("class", "SegmentedButton")
        PyLunixStyleSheet.TOGGLE_BUTTON.apply(self)