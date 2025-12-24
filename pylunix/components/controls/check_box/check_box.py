from typing import Union, Callable
from PyQt5.QtWidgets import QCheckBox, QWidget, QStyleOptionButton, QStyle
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen
from PyQt5.QtCore import QSize, Qt, QRect

from ....common.stylesheet import PyLunixStyleSheet
from ....icons import WinIcon

class CheckBox(QCheckBox):
    """
    Themed CheckBox with support for dynamic icon coloring and custom indicator rendering.

    This class extends QCheckBox to provide a modern look and feel consistent with 
    the PyLunix theme. It supports dynamic re-coloring of the checkbox glyphs 
    (Checkmark/Indeterminate) and an optional secondary icon.

    Attributes:
        isPressed (bool): Tracks whether the mouse button is currently pressed.
        isHover (bool): Tracks whether the mouse pointer is over the widget.
        _icon_source (Optional[Callable[[str], QIcon]]): A callback that takes a color 
            hex string and returns a QIcon for the secondary icon.
    """
    def __init__(self, text: str = "", icon: QIcon = None, parent: QWidget = None):
        """
        Initialize the CheckBox.

        Args:
            text (str): The text displayed next to the checkbox. Defaults to "".
            icon (Union[QIcon, Callable], optional): An optional icon to display. 
                Can be a static QIcon or a dynamic callable. Defaults to None.
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(text, parent)
        self.isPressed = False
        self.isHover = False
        self._icon_source = None

        self.setProperty("class", "CheckBox")
        self.setIconSize(QSize(16, 16))

        if text: self.setText(text)
        if icon: self.setIcon(icon)
        else: self.setIcon(QIcon())

        PyLunixStyleSheet.CHECK_BOX.apply(self)

    def setIcon(self, icon: Union[QIcon, Callable]):
        """
        Set the checkbox's secondary icon.

        If a callable is provided, the icon will update its color based on the 
        checkbox's state.

        Args:
            icon (Union[QIcon, Callable]): A QIcon instance or a function that 
                returns a QIcon based on a color string.
        """
        if callable(icon):
            self.setIconSource(icon)
        else:
            super().setIcon(icon)
            self._icon_source = None
            self._icon = icon

    def setIconSource(self, icon_accessor):
        """
        Assign a dynamic icon source callback for the secondary icon.

        Args:
            icon_accessor (Callable): A function accepting a color string 
                and returning a QIcon.
        """
        self._icon_source = icon_accessor
        self.updateIcon()

    def _get_icon_color(self) -> str:
        """
        Determine the secondary icon color based on the current state and check state.

        Returns:
            str: The color value hex string from the stylesheet.
        """
        if not self.isEnabled():
            name = "CheckBoxForegroundCheckedDisabled" if self.isChecked() else "CheckBoxForegroundUncheckedDisabled"
        elif self.isPressed:
            name = "CheckBoxForegroundCheckedPressed" if self.isChecked() else "CheckBoxForegroundUncheckedPressed"
        elif self.isHover:
            name = "CheckBoxForegroundCheckedPointerOver" if self.isChecked() else "CheckBoxForegroundUncheckedPointerOver"
        else:
            name = "CheckBoxForegroundChecked" if self.isChecked() else "CheckBoxForegroundUnchecked"
        return PyLunixStyleSheet.CHECK_BOX.get_value(name)
    
    def _get_indicator_icon_color(self) -> str:
        """
        Retrieve the color for the checkmark/glyph inside the checkbox indicator.

        Returns:
            str: The glyph color value hex string from the stylesheet.
        """
        if not self.isEnabled():
            name = "CheckBoxCheckGlyphForegroundCheckedDisabled" if self.isChecked() else "CheckBoxCheckGlyphForegroundUncheckedDisabled"
        elif self.isPressed:
            name = "CheckBoxCheckGlyphForegroundCheckedPressed" if self.isChecked() else "CheckBoxCheckGlyphForegroundUncheckedPressed"
        elif self.isHover:
            name = "CheckBoxCheckGlyphForegroundCheckedPointerOver" if self.isChecked() else "CheckBoxCheckGlyphForegroundUncheckedPointerOver"
        else:
            name = "CheckBoxCheckGlyphForegroundChecked" if self.isChecked() else "CheckBoxCheckGlyphForegroundUnchecked"
        return PyLunixStyleSheet.CHECK_BOX.get_value(name)

    def updateIcon(self):
        """
        Refresh the secondary icon based on the current state color.
        """
        if hasattr(self, "_icon_source") and callable(self._icon_source):
            try:
                color = self._get_icon_color()
                icon = self._icon_source(color)
                if icon:
                    super().setIcon(icon)
                    self._icon = icon
                    self.update()
            except Exception as e:
                print(f"[CheckBox] Failed to update icon: {e}")

    def enterEvent(self, event):
        """Handle mouse enter event to trigger hover styles."""
        self.isHover = True
        super().enterEvent(event)
        self.update()

    def leaveEvent(self, event):
        """Handle mouse leave event to clear hover styles."""
        self.isHover = False
        super().leaveEvent(event)
        self.update()

    def mousePressEvent(self, event):
        """Handle mouse press event to trigger pressed styles."""
        self.isPressed = True
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """Handle mouse release event to clear pressed styles."""
        self.isPressed = False
        super().mouseReleaseEvent(event)

    def paintEvent(self, e):
        """
        Custom paint engine for the CheckBox.

        Manually renders the checkbox indicator (background, border, and glyph) 
        and the standard label to allow for precise theme integration.

        Args:
            e (QPaintEvent): The paint event provided by Qt.
        """
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)

        opt = QStyleOptionButton()
        self.initStyleOption(opt)
        rect = self.style().subElementRect(QStyle.SubElement.SE_CheckBoxIndicator, opt, self)
        
        def _background_color() -> str:
            if not self.isEnabled():
                name = "CheckBoxCheckBackgroundFillCheckedDisabled" if self.isChecked() else "CheckBoxCheckBackgroundFillUncheckedDisabled"
            elif self.isPressed:
                name = "CheckBoxCheckBackgroundFillCheckedPressed" if self.isChecked() else "CheckBoxCheckBackgroundFillUncheckedPressed"
            elif self.isHover:
                name = "CheckBoxCheckBackgroundFillCheckedPointerOver" if self.isChecked() else "CheckBoxCheckBackgroundFillUncheckedPointerOver"
            else:
                name = "CheckBoxCheckBackgroundFillChecked" if self.isChecked() else "CheckBoxCheckBackgroundFillUnchecked"
            return PyLunixStyleSheet.CHECK_BOX.get_value(name)

        def _border_color() -> str:
            if not self.isEnabled():
                name = "CheckBoxCheckBackgroundStrokeCheckedDisabled" if self.isChecked() else "CheckBoxCheckBackgroundStrokeUncheckedDisabled"
            elif self.isPressed:
                name = "CheckBoxCheckBackgroundStrokeCheckedPressed" if self.isChecked() else "CheckBoxCheckBackgroundStrokeUncheckedPressed"
            elif self.isHover:
                name = "CheckBoxCheckBackgroundStrokeCheckedPointerOver" if self.isChecked() else "CheckBoxCheckBackgroundStrokeUncheckedPointerOver"
            else:
                name = "CheckBoxCheckBackgroundStrokeChecked" if self.isChecked() else "CheckBoxCheckBackgroundStrokeUnchecked"
            return PyLunixStyleSheet.CHECK_BOX.get_value(name)


        painter.setBrush(QColor(_background_color()))
        painter.setPen(QPen(QColor(_border_color()), 1))
        painter.drawRoundedRect(rect.adjusted(0, 0, -1, -1), 5, 5)

        GLYPH_SIZE = 14
        
        color = self._get_indicator_icon_color()
        indicator_icon = None

        target_glyph_accessor = None
        
        if self.checkState() == Qt.CheckState.Checked:
            target_glyph_accessor = WinIcon.CHECKMARK 
        elif self.checkState() == Qt.CheckState.PartiallyChecked:
            if hasattr(WinIcon, 'INDETERMINATE'):
                target_glyph_accessor = WinIcon.INDETERMINATE
            else:
                target_glyph_accessor = WinIcon.CHECKMARK 

        if target_glyph_accessor and callable(target_glyph_accessor):
            try:
                indicator_icon = target_glyph_accessor(color)
            except Exception as e:
                print(f"[CheckBox] Failed to get themed indicator icon: {e}")

        if isinstance(indicator_icon, QIcon):
            pixmap = indicator_icon.pixmap(QSize(GLYPH_SIZE, GLYPH_SIZE), QIcon.Mode.Normal if self.isEnabled() else QIcon.Mode.Disabled)
            icon_rect = QRect(
                rect.x() + (rect.width() - pixmap.width()) // 2,
                rect.y() + (rect.height() - pixmap.height()) // 2,
                pixmap.width(),
                pixmap.height()
            )
            painter.drawPixmap(icon_rect, pixmap)

        content_rect = self.style().subElementRect(QStyle.SubElement.SE_CheckBoxContents, opt, self)
        opt.rect = content_rect
        self.style().drawControl(QStyle.ControlElement.CE_CheckBoxLabel, opt, painter, self)
        painter.end()