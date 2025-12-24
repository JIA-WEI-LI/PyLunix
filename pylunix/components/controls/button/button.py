from typing import Union, Callable, Optional, Dict
from PyQt5.QtWidgets import QPushButton, QWidget
from PyQt5.QtGui import QIcon, QPainter
from PyQt5.QtCore import QSize, QRectF, Qt

from ....common.stylesheet import PyLunixStyleSheet

# region BaseButton
class BaseButton(QPushButton):
    """
    Base button class with support for dynamic icon coloring and custom state rendering.

    This class extends QPushButton to provide enhanced icon management. It allows 
    icons to dynamically change color based on the button's current state 
    (Normal, Hover, Pressed, or Disabled) by using a callback-based icon source.

    Attributes:
        isPressed (bool): Tracks whether the mouse button is currently pressed.
        isHover (bool): Tracks whether the mouse pointer is over the button.
        _icon_cache (Dict[str, QIcon]): Cache for storing generated icons to optimize performance.
        _icon_source (Optional[Callable[[str], QIcon]]): A callback that takes a color hex string 
            and returns a QIcon.
    """

    def __init__(self, text: str = "", icon: Optional[Union[QIcon, Callable]] = None, parent: Optional[QWidget] = None):
        """
        Initialize the BaseButton.

        Args:
            text (str): The text displayed on the button. Defaults to "".
            icon (Union[QIcon, Callable], optional): The initial icon. Can be a static 
                QIcon or a callable for dynamic coloring. Defaults to None.
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(text=text, parent=parent)
        self.isPressed = False
        self.isHover = False
        self._icon_cache: Dict[str, QIcon] = {}
        self._icon_source = None
        self._current_icon_color = None
        self._icon = QIcon()

        self.setProperty("class", "PushButton")
        self.setMinimumHeight(36)
        self.setIconSize(QSize(16, 16))
        
        if text:
            self.setText(text)
        if icon:
            self.setIcon(icon)

    def setIcon(self, icon: Union[QIcon, Callable]):
        """
        Set the button's icon.

        If a callable is provided, the button enables dynamic re-coloring mode.

        Args:
            icon (Union[QIcon, Callable]): A QIcon instance or a function that 
                returns a QIcon based on a color string.

        .. code-block:: python
        
            button.setIcon(WinIcon.CHECKMARK)
        """
        if callable(icon):
            self._icon = QIcon()
            self.setIconSource(icon)
        else:
            super().setIcon(icon)
            self._icon_source = None
            self._icon = icon

    def setIconSource(self, icon_accessor: Callable[[str], QIcon]):
        """
        Assign a dynamic icon source callback.

        Args:
            icon_accessor (Callable): A function accepting a color string (e.g., "#FFFFFF") 
                and returning a QIcon.
        """
        self._icon_source = icon_accessor
        self.updateIcon()

    def _get_icon_color(self) -> str:
        """
        Determine the appropriate icon color based on the current button state.

        Returns:
            str: The color value retrieved from the PyLunixStyleSheet.
        """
        if not self.isEnabled():
            name = "ButtonForegroundDisabled"
        elif self.isPressed:
            name = "ButtonForegroundPressed"
        elif self.isHover:
            name = "ButtonForegroundPointerOver"
        else:
            name = "ButtonForeground"
        return PyLunixStyleSheet.BUTTON.get_value(name)

    def updateIcon(self):
        """
        Refresh the icon based on the current state color.

        Uses an internal cache to avoid redundant icon generation.

        .. code-block:: python

            button._icon_cache.clear()
            button.updateIcon()
        """
        if not callable(getattr(self, "_icon_source", None)):
            return
        color = self._get_icon_color()
        if color == self._current_icon_color:
            return
        self._current_icon_color = color
        if color not in self._icon_cache:
            self._icon_cache[color] = self._icon_source(color)
        self._icon = self._icon_cache[color]
        # Clear native icon to prevent default rendering
        super().setIcon(QIcon())

    def sizeHint(self) -> QSize:
        """
        Calculate the recommended size for the button.

        Returns:
            QSize: The calculated size hint, ensuring minimum height for icons.
        """
        base = super().sizeHint()
        icon_h = self.iconSize().height()

        if base.height() < icon_h:
            return QSize(base.width(), icon_h + 10)
        return base

    def paintEvent(self, e):
        """
        Custom paint engine for the button.

        Handles manual rendering of icons and text to support precise alignment, 
        transparency effects, and Right-to-Left (RTL) layouts.

        Args:
            e (QPaintEvent): The paint event provided by Qt.
        """
        super().paintEvent(e)

        if callable(getattr(self, "_icon", None)):
            self.updateIcon()
        
        current_icon = getattr(self, "_icon", None)
        if not hasattr(current_icon, "isNull") or current_icon.isNull():
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

        # Apply state-based opacity
        if not self.isEnabled():
            painter.setOpacity(0.36)
        elif self.isPressed:
            painter.setOpacity(0.78)

        # Logic for centering icon and text
        icon_width = self.iconSize().width()
        icon_height = self.iconSize().height()
        icon_y = (self.height() - icon_height) / 2

        text_width = self.fontMetrics().horizontalAdvance(self.text()) if self.text() else 0
        spacing = 28 # Customizable spacing between icon and text

        total_content_width = icon_width + (spacing if text_width else 0) + text_width
        icon_x = (self.width() - total_content_width) / 2

        # Handle RTL Layouts
        if self.layoutDirection() == Qt.RightToLeft:
            icon_x = self.width() - icon_x - icon_width

        rect = QRectF(icon_x, icon_y, icon_width, icon_height)
        current_icon.paint(painter, rect.toRect())

        painter.end()
# endregion

# region PushButton
class PushButton(BaseButton):
    """
    Standard themed PushButton for general use.
    """
    def __init__(self, text: str = "", icon: QIcon = None, parent: QWidget = None):
        super().__init__(text=text, icon=icon, parent=parent)
        self.setProperty("class", "PushButton")
        PyLunixStyleSheet.BUTTON.apply(self)
#  endregion

# region Primary Button
class PrimaryButton(BaseButton):
    """
    High-priority button using the theme's accent color.
    """
    def __init__(self, text: str = "", icon: QIcon = None, parent: QWidget = None):
        super().__init__(text=text, icon=icon, parent=parent)
        self.setProperty("class", "PrimaryButton")
        PyLunixStyleSheet.BUTTON.apply(self)

    def _get_icon_color(self) -> str:
        """
        Retrieve icon colors specific to the Accent/Primary style.
        """
        if not self.isEnabled():
            name = "AccentButtonForegroundDisabled"
        elif self.isPressed:
            name = "AccentButtonForegroundPressed"
        elif self.isHover:
            name = "AccentButtonForegroundPointerOver"
        else:
            name = "AccentButtonForeground"
        return PyLunixStyleSheet.BUTTON.get_value(name)
# endregion

# region Transparent PushButton
class TransparentPushButton(BaseButton):
    """
    A flat, transparent button style typically used for toolbars or secondary actions.
    """
    def __init__(self, text: str = "", icon: QIcon = None, parent: QWidget = None):
        super().__init__(text=text, icon=icon, parent=parent)
        self.setProperty("class", "TransparentPushButton")
        PyLunixStyleSheet.BUTTON.apply(self)
# endregion