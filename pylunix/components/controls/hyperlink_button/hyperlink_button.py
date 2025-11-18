from typing import Union, Callable
from PyQt5.QtWidgets import QPushButton, QWidget, QToolButton
from PyQt5.QtGui import QIcon, QPainter, QCursor, QDesktopServices, QMouseEvent
from PyQt5.QtCore import QSize, QRectF, Qt, QUrl, QEvent, QTimer

from ....common.stylesheet import PyLunixStyleSheet

class HyperlinkButton(QPushButton):
    def __init__(self, text: str = "", icon: QIcon = None, parent: QWidget = None, *args, **kwargs):
        self._url = kwargs.pop("url", None)
        self.auto_prefix_http = kwargs.pop("auto_prefix_http", False)
        self.ctrl_click_enabled = kwargs.pop("ctrl_click_enabled", False)
        self.middle_click_enabled = kwargs.pop("middle_click_enabled", False)

        super().__init__(text=text, parent=parent)
        self.isPressed = False
        self.isHover = False
        self._icon_cache = {}
        self._icon_source = None
        self._current_icon_color = None

        self.setMinimumHeight(32)
        self.setIconSize(QSize(16, 16))
        self.setText(text if text else "")
        self.setIcon(icon if icon else QIcon())

        if self.ctrl_click_enabled:
            self.installEventFilter(self)

        if self._url:
            self.setToolTip(self._url)

        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setProperty("class", "HyperlinkButton")

        PyLunixStyleSheet.HYPERLINK_BUTTON.apply(self)

    def setIcon(self, icon: Union[QIcon, Callable]):
        if callable(icon):
            self.setIconSource(icon)
        else:
            super().setIcon(icon)
            self._icon_source = None
            self._icon = icon

    def setIconSource(self, icon_accessor):
        self._icon_source = icon_accessor
        self.updateIcon()

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
        
    def setUrl(self, url: str):
        self._url = url
        self.setToolTip(url)

    def url(self) -> str:
        return self._url

    def _normalize_url(self, url: str) -> QUrl:
        if self.auto_prefix_http and not url.lower().startswith(("http://", "https://")):
            url = "http://" + url
        return QUrl(url)

    def _open_url(self):
        if self._url:
            QDesktopServices.openUrl(self._normalize_url(self._url))

    def _get_icon_color(self) -> str:
        if not self.isEnabled():
            name = "HyperlinkButtonForegroundDisabled"
        elif self.isPressed:
            name = "HyperlinkButtonForegroundPressed"
        elif self.isHover:
            name = "HyperlinkButtonForegroundPointerOver"
        else:
            name = "HyperlinkButtonForeground"
        return PyLunixStyleSheet.BUTTON.color(name)

    def enterEvent(self, e): self.isHover = True; self.updateIcon(); super().enterEvent(e)
    def leaveEvent(self, e): self.isHover = False; self.updateIcon(); super().leaveEvent(e)
    def mousePressEvent(self, e): self.isPressed = True; self.updateIcon(); super().mousePressEvent(e)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.MiddleButton and self.middle_click_enabled:
            self._open_url()
        elif event.button() == Qt.MouseButton.LeftButton:
            if self.ctrl_click_enabled and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                self._open_url()
            else:
                self._open_url()
        super().mouseReleaseEvent(event)

    def eventFilter(self, obj, event):
        if obj is self and event.type() == QEvent.MouseButtonRelease:
            if event.modifiers() & Qt.ShiftModifier:
                return True
        return super().eventFilter(obj, event)
    
    def showEvent(self, e):
        super().showEvent(e)
        self.updateIcon()

    def paintEvent(self, e):
        super().paintEvent(e)

        if self._icon.isNull():
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

        text_width = self.fontMetrics().width(self.text()) if self.text() else 0
        spacing = 6

        total_width = icon_width + spacing + text_width if text_width else icon_width
        icon_x = (self.width() - total_width) / 2

        if self.layoutDirection() == Qt.LayoutDirection.RightToLeft:
            icon_x = self.width() - icon_x - icon_width

        rect = QRectF(icon_x, icon_y, icon_width, icon_height)
        self._icon.paint(painter, rect.toRect())

        painter.end()