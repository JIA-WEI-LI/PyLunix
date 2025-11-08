from typing import Union, Callable
from PyQt5.QtWidgets import QPushButton, QWidget
from PyQt5.QtGui import QIcon, QPainter
from PyQt5.QtCore import QSize, QRectF, Qt, QTimer

from ...common.stylesheet import PyLunixStyleSheet

class BaseButton(QPushButton):
    def __init__(self, text: str = "", icon: QIcon = None, parent: QWidget = None):
        super().__init__(text=text, parent=parent)
        self.isPressed = False
        self.isHover = False
        self._icon_cache = {}
        self._icon_source = None
        self._current_icon_color = None

        self.setProperty("class", "PushButton")
        self.setMinimumHeight(32)
        self.setIconSize(QSize(16, 16))
        self.setText(text if text else "")
        self.setIcon(icon if icon else QIcon())

    def setIcon(self, icon: Union[QIcon, Callable]):
        if callable(icon):
            self._icon = QIcon()
            self.setIconSource(icon)
        else:
            super().setIcon(icon)
            self._icon_source = None
            self._icon = icon

    def setIconSource(self, icon_accessor):
        self._icon_source = icon_accessor
        self.updateIcon()

    def _get_icon_color(self) -> str:
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
        if not callable(getattr(self, "_icon_source", None)):
            return
        color = self._get_icon_color()
        if color == self._current_icon_color:
            return
        self._current_icon_color = color
        if color not in self._icon_cache:
            self._icon_cache[color] = self._icon_source(color)
        super().setIcon(self._icon_cache[color])
        self._icon = self._icon_cache[color]

    def sizeHint(self):
        base = super().sizeHint()
        icon_h = self.iconSize().height()

        if base.height() < icon_h:
            return QSize(base.width(), icon_h + 10)
        return base

    def enterEvent(self, e): self.isHover = True; self.updateIcon(); super().enterEvent(e)
    def leaveEvent(self, e): self.isHover = False; self.updateIcon(); super().leaveEvent(e)
    def mousePressEvent(self, e): self.isPressed = True; self.updateIcon(); super().mousePressEvent(e)
    def mouseReleaseEvent(self, e): self.isPressed = False; self.updateIcon(); super().mouseReleaseEvent(e)

    def showEvent(self, e):
        super().showEvent(e)
        self.updateIcon()

    def paintEvent(self, e):
        super().paintEvent(e)

        if callable(getattr(self, "_icon", None)):
            self.updateIcon()
        current_icon = getattr(self, "_icon", None)
        if not hasattr(current_icon, "isNull") or current_icon.isNull():
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)

        if not self.isEnabled():
            painter.setOpacity(0.36)
        elif self.isPressed:
            painter.setOpacity(0.78)

        icon_width = self.iconSize().width()
        icon_height = self.iconSize().height()
        icon_y = (self.height() - icon_height) / 2

        text_width = self.fontMetrics().horizontalAdvance(self.text()) if self.text() else 0
        spacing = 6

        total_width = icon_width + spacing + text_width if text_width else icon_width
        icon_x = (self.width() - total_width) / 2

        if self.layoutDirection() == Qt.LayoutDirection.RightToLeft:
            icon_x = self.width() - icon_x - icon_width

        rect = QRectF(icon_x, icon_y, icon_width, icon_height)
        self._icon.paint(painter, rect.toRect())

        painter.end()

class PushButton(BaseButton):
    def __init__(self, text: str = "", icon: QIcon = None, parent: QWidget = None):
        super().__init__(text=text, icon=icon, parent=parent)
        self.setProperty("class", "PushButton")

        PyLunixStyleSheet.BUTTON.apply(self)

class PrimaryButton(BaseButton):
    def __init__(self, text: str = "", icon: QIcon = None, parent: QWidget = None):
        super().__init__(text=text, icon=icon, parent=parent)
        self.setProperty("class", "PrimaryButton")

        PyLunixStyleSheet.BUTTON.apply(self)

    def _get_icon_color(self) -> str:
        if not self.isEnabled():
            name = "AccentButtonForegroundDisabled"
        elif self.isPressed:
            name = "AccentButtonForegroundPressed"
        elif self.isHover:
            name = "AccentButtonForegroundPointerOver"
        else:
            name = "AccentButtonForeground"
        return PyLunixStyleSheet.BUTTON.get_value(name)

class TransparentPushButton(BaseButton):
    def __init__(self, text: str = "", icon: QIcon = None, parent: QWidget = None):
        super().__init__(text=text, icon=icon, parent=parent)
        self.setProperty("class", "TransparentPushButton")

        PyLunixStyleSheet.BUTTON.apply(self)