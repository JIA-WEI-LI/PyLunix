from typing import Union, Callable
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon

from ..button.button import BaseButton
from ....common.stylesheet import PyLunixStyleSheet

class ToggleButton(BaseButton):
    """
    A binary state button that toggles between 'On' and 'Off' states.

    This class manages independent icons and labels for checked and unchecked states.
    It automatically updates its appearance when the toggle state changes.

    Attributes:
        _text_on (str): Label displayed when the button is checked.
        _text_off (str): Label displayed when the button is unchecked.
        _icon_on (Union[QIcon, Callable]): Icon or icon-generator used in checked state.
        _icon_off (Union[QIcon, Callable]): Icon or icon-generator used in unchecked state.
    """
    def __init__(self, text: str = "", icon: QIcon = None, parent: QWidget = None):
        """
        Initialize the ToggleButton.

        Args:
            text (str): Default initial text.
            icon (QIcon, optional): Default initial icon.
            parent (QWidget, optional): Parent widget.
        """
        super().__init__(text=text, icon=icon, parent=parent)
        self._text_on = None
        self._text_off = None
        self._icon_on = None
        self._icon_off = None
        
        self._postInit()
        self.setProperty("class", "ToggleButton")
        PyLunixStyleSheet.TOGGLE_BUTTON.apply(self)
        
    def _postInit(self):
        """Internal setup for checkable properties and signal connections."""
        self.setCheckable(True)
        self.setChecked(False)
        self.toggled.connect(self._on_toggle_state_changed)

    def setToggleIcons(self, icon_on: Union[QIcon, Callable], icon_off: Union[QIcon, Callable]):
        """
        Assign separate icons for the 'On' and 'Off' states.

        Args:
            icon_on (Union[QIcon, Callable]): Icon to show when checked=True.
            icon_off (Union[QIcon, Callable]): Icon to show when checked=False.
        """
        self._icon_on = icon_on
        self._icon_off = icon_off
        self._applyToggle()

    def setToggleText(self, text_on: str, text_off: str):
        """
        Assign separate text labels for the 'On' and 'Off' states.

        Args:
            text_on (str): Text to show when checked=True.
            text_off (str): Text to show when checked=False.
        """
        self._text_on = text_on
        self._text_off = text_off
        self._applyToggle()

    def setChecked(self, checked: bool):
        """
        Sets the check state and refreshes the toggle visuals.

        Args:
            checked (bool): True to check (On), False to uncheck (Off).
        """
        super().setChecked(checked)
        self._applyToggle()
        self.updateIcon()

    def _get_icon_color(self) -> str:
        """
        Determines the theme color key based on both interaction state and toggle state.
        
        This handles complex state combinations (e.g., Checked + Hover).
        """
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
        """Updates the text and icon based on the current checked state."""
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
        """Callback for the 'toggled' signal."""
        self._applyToggle()
        self.updateIcon()

class TransparentToggleButton(ToggleButton):
    """
    A ToggleButton with a transparent background. 
    Ideal for toolbar actions or subtle UI toggles.
    """
    def __init__(self, text: str = "", icon: QIcon = None, parent: QWidget = None):
        super().__init__(text=text, icon=icon, parent=parent)
        self.setProperty("class", "TransparentToggleButton")
        PyLunixStyleSheet.TOGGLE_BUTTON.apply(self)

class SegmentedButton(ToggleButton):
    """
    A ToggleButton styled as part of a segmented control group. 
    Typically used for switching views or filter modes.
    """
    def __init__(self, text: str = "", icon: QIcon = None, parent: QWidget = None):
        super().__init__(text=text, icon=icon, parent=parent)
        self.setProperty("class", "SegmentedButton")
        PyLunixStyleSheet.TOGGLE_BUTTON.apply(self)