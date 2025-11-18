from typing import Union, Callable
from PyQt5.QtWidgets import QWidget, QToolButton
from PyQt5.QtGui import QIcon, QPainter, QColor
from PyQt5.QtCore import QSize, QRectF, Qt

from ....common.stylesheet import PyLunixStyleSheet

class ToolButton(QToolButton):
    def __init__(self, icon: QIcon, parent: QWidget = None):
        super().__init__(parent=parent)
        self.isPressed = False
        self.isHover = False
        self._icon_source = None

        self.setProperty("class", "ToolButton")
        self.setIconSize(QSize(16, 16))
        self.setIcon(icon if icon else QIcon())
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        # self.adjustToSquare()

        PyLunixStyleSheet.TOOL_BUTTON.apply(self)

    def setIcon(self, icon: Union[QIcon, Callable]):
        if callable(icon):
            self.setIconSource(icon)
        else:
            super().setIcon(icon)
            self._icon_source = None
            self._icon = icon

    def setIconSource(self, icon_accessor: Callable[[str], QIcon]):
        self._icon_source = icon_accessor
        self.updateIcon()

    def adjustToSquare(self, padding: int = 8):
        size = self.iconSize()
        side = max(size.width(), size.height()) + padding
        self.setFixedSize(side, side)

    def _get_icon_color(self) -> str:
        if not self.isEnabled():
            name = "ToolButtonForegroundDisabled"
        elif self.isPressed:
            name = "ToolButtonForegroundPressed"
        elif self.isHover:
            name = "ToolButtonForegroundPointerOver"
        else:
            name = "ToolButtonForeground"
        return PyLunixStyleSheet.TOOL_BUTTON.get_value(name)

    def updateIcon(self):
        if hasattr(self, "_icon_source") and callable(self._icon_source):
            try:
                color = self._get_icon_color()
                icon = self._icon_source(color)
                if icon:
                    super().setIcon(icon)
                    self._icon = icon
            except Exception as e:
                print(f"[ToolButton] Failed to update icon: {e}")

    def mousePressEvent(self, event): self.isPressed = True; super().mousePressEvent(event)
    def mouseReleaseEvent(self, event): self.isPressed = False; super().mouseReleaseEvent(event)
    def enterEvent(self, event): self.isHover = True; self.update(); super().enterEvent(event)
    def leaveEvent(self, event): self.isHover = False; self.update(); super().leaveEvent(event)

    def showEvent(self, event):
        super().showEvent(event)
        self.updateIcon()

    def paintEvent(self, event):
        original_text = self.text()
        super().setText("")
        original_icon = self.icon()
        super().setIcon(QIcon())
        super().paintEvent(event)
        super().setText(original_text)
        super().setIcon(original_icon)

        if not hasattr(self, "_icon") or self._icon.isNull():
            if not self.text():
                 return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)

        color_name = self._get_icon_color() 
        current_color = QColor(color_name)
        painter.setPen(current_color)

        if not self.isEnabled():
            painter.setOpacity(0.36)
        elif self.isPressed:
            painter.setOpacity(0.78)

        icon_width = self.iconSize().width()
        icon_height = self.iconSize().height()
        icon_y = (self.height() - icon_height) / 2

        current_text = self.text()
        text_width = self.fontMetrics().width(current_text) if current_text else 0
        spacing = 6

        has_text = bool(current_text)
        total_width = icon_width
        if has_text:
             total_width += spacing + text_width

        start_x = (self.width() - total_width) / 2
        icon_x = start_x
        
        if self.layoutDirection() == Qt.RightToLeft:
            text_x = start_x
            icon_x = text_x + text_width + spacing
        
        if hasattr(self, "_icon") and not self._icon.isNull():
            icon_rect = QRectF(icon_x, icon_y, icon_width, icon_height)
            self._icon.paint(painter, icon_rect.toRect())
        else:
            if has_text:
                text_x = start_x

        if has_text:
            text_x = icon_x + icon_width + spacing
            text_y = (self.height() + self.fontMetrics().ascent() - self.fontMetrics().descent()) / 2
            text_rect = QRectF(text_x, 0, text_width, self.height())
            painter.drawText(text_rect, Qt.AlignLeft | Qt.AlignVCenter, current_text)

        painter.end()

class PrimaryToolButton(ToolButton):
    def __init__(self, icon: QIcon = None, parent: QWidget = None):
        super().__init__(icon=icon, parent=parent)
        self.setProperty("class", "PrimaryToolButton")

    def _get_icon_color(self) -> str:
        if not self.isEnabled():
            name = "AccentToolButtonForegroundDisabled"
        elif self.isPressed:
            name = "AccentToolButtonForegroundPressed"
        elif self.isHover:
            name = "AccentToolButtonForegroundPointerOver"
        else:
            name = "AccentToolButtonForeground"
        return PyLunixStyleSheet.TOOL_BUTTON.get_value(name)
    
class ToggleToolButton(ToolButton):
    def __init__(self, icon: QIcon = None, parent: QWidget = None):
        super().__init__(icon=icon, parent=parent)
        self._icon_on = None
        self._icon_off = None
        
        self._postInit()
        self.setProperty("class", "ToggleToolButton")
        
    def _postInit(self):
        self.setCheckable(True)
        self.setChecked(False)
        self.toggled.connect(self._on_toggle_state_changed)

    def setToggleIcons(self, icon_on: Union[QIcon, Callable], icon_off: Union[QIcon, Callable]):
        self._icon_on = icon_on
        self._icon_off = icon_off
        self._applyToggle()

    def _get_icon_color(self) -> str:
        if self.isChecked():
            if not self.isEnabled():
                name = "AccentToolButtonForegroundDisabled"
            elif self.isPressed:
                name = "AccentToolButtonForegroundPressed"
            elif self.isHover:
                name = "AccentToolButtonForegroundPointerOver"
            else:
                name = "AccentToolButtonForeground"
        elif not self.isEnabled():
            name = "ToolButtonForegroundDisabled"
        elif self.isPressed:
            name = "ToolButtonForegroundPressed"
        elif self.isHover:
            name = "ToolButtonForegroundPointerOver"
        else:
            name = "ToolButtonForeground"
        return PyLunixStyleSheet.TOOL_BUTTON.get_value(name)

    def _applyToggle(self):
        if self._icon_on and self._icon_off:
            icon = self._icon_on if self.isChecked() else self._icon_off
            if callable(icon):
                self.setIconSource(icon)
            else:
                self.setIcon(icon)

    def _on_toggle_state_changed(self, checked: bool):
        self._applyToggle()
        self.updateIcon()

    def setChecked(self, checked: bool):
        super().setChecked(checked)
        self._applyToggle()
        self.updateIcon()

class TransparentToolButton(ToolButton):
    def __init__(self, icon: QIcon = None, parent: QWidget = None):
        super().__init__(icon=icon, parent=parent)
        self.setProperty("class", "TransparentToolButton")

class TransparentToggleToolButton(ToggleToolButton):
    def __init__(self, icon: QIcon = None, parent: QWidget = None):
        super().__init__(icon=icon, parent=parent)
        self.setProperty("class", "TransparentToggleToolButton")