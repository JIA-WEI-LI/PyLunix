from typing import Union, Callable, Optional, Dict
from PyQt5.QtWidgets import QPushButton, QWidget
from PyQt5.QtGui import QIcon, QPainter
from PyQt5.QtCore import QSize, QRectF, Qt

from ....common.stylesheet import PyLunixStyleSheet
from ....common.factories import StateColorResolver

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

    def __init__(self, 
                 text: str = "", 
                 icon: Optional[Union[QIcon, Callable]] = None,
                 component_name: str = "Button", 
                 parent: Optional[QWidget] = None):
        """
        Initialize the BaseButton.

        Args:
            text (str): The text displayed on the button. Defaults to "".
            icon (Union[QIcon, Callable], optional): The initial icon. Can be a static 
                QIcon or a callable for dynamic coloring. Defaults to None.
            component_name (str): The semantic name used for style resolution. Defaults to "Button".
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(text=text, parent=parent)
        self.isPressed = False
        self.isHover = False
        self._component_name = component_name
        self._icon_cache: Dict[str, QIcon] = {}
        self._icon_source = None
        self._current_icon_color = None
        self._custom_icon_color = None
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

    def setIconColor(self, color: Optional[str]):
        """
        Manually override the icon color.

        Args:
            color (Optional[str]): A hex color string (e.g., "#FF0000"). 
                Pass None to revert to automatic theme-based coloring.
        """
        self._custom_icon_color = color
        self.updateIcon()

    def getIconColor(self) -> str:
        """
        Retrieve the current effective icon color.

        Returns:
            str: The custom color if set, otherwise the resolved theme color.
        """
        if self._custom_icon_color:
            return self._custom_icon_color
        
        return self._get_icon_color()

    def _get_icon_color(self) -> str:
        """
        Resolve the icon color from the stylesheet based on component state.

        Returns:
            str: Resolved color hex string.
        """
        return StateColorResolver.resolve(self._component_name, "Foreground", self, theme_type="BUTTON")

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
        target_color = self.getIconColor()
        if target_color == self._current_icon_color:
            return
        self._current_icon_color = target_color
        if target_color not in self._icon_cache:
            self._icon_cache[target_color] = self._icon_source(target_color)
        self._icon = self._icon_cache[target_color]

        if not super().icon().isNull():
            super().setIcon(QIcon())

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
    
    def enterEvent(self, event):
        self.isHover = True
        self.updateIcon()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.isHover = False
        self.isPressed = False
        self.updateIcon()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.isPressed = True
            self.updateIcon()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.isPressed = False
        self.updateIcon()
        super().mouseReleaseEvent(event)

    def changeEvent(self, event):
        """
        Handle state changes, such as enabling/disabling the button.
        """
        super().changeEvent(event)
        if event.type() == event.EnabledChange:
            self.updateIcon()

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
    def __init__(self, text: str = "", icon: QIcon = None, parent: Optional[QWidget] = None):
        super().__init__(text=text, icon=icon, parent=parent)
        self.setProperty("class", "PushButton")
        PyLunixStyleSheet.BUTTON.apply(self)
#  endregion

# region Primary Button
class PrimaryButton(BaseButton):
    """
    High-priority button using the theme's accent color, equivalent to WinUI 3's AccentButtonStyle.
    """
    def __init__(self, text: str = "", icon: QIcon = None, parent: Optional[QWidget] = None):
        super().__init__(text=text, icon=icon, component_name="AccentButton", parent=parent)
        self.setProperty("class", "PrimaryButton")
        PyLunixStyleSheet.BUTTON.apply(self)
# endregion

# region Subtle PushButton
class SubtleButton(BaseButton):
    """
    A flat, transparent button style typically used for secondary actions or toolbars,
    equivalent to WinUI 3's SubtleButtonStyle.
    """
    def __init__(self, text: str = "", icon: QIcon = None, parent: Optional[QWidget] = None):
        super().__init__(text=text, icon=icon, component_name="Button", parent=parent)
        self.setProperty("class", "SubtleButton")
        PyLunixStyleSheet.BUTTON.apply(self)
# endregion