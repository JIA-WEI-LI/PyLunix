from typing import Union, Callable
from PyQt5.QtWidgets import QWidget, QRadioButton
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen
from PyQt5.QtCore import QSize, QRectF, Qt

from ....common.stylesheet import PyLunixStyleSheet

class RadioButton(QRadioButton):
    def __init__(self, text: str = "", icon: QIcon = None, parent: QWidget = None):
        super().__init__(text=text, parent=parent)
        self.isPressed = False
        self.isHover = False
        self._icon_source = None

        self.setProperty("class", "RadioButton")
        self.setIconSize(QSize(16, 16))

        if text: self.setText(text)
        if icon: self.setIcon(icon)
        else: self.setIcon(QIcon())

        PyLunixStyleSheet.RADIO_BUTTON.apply(self)
        self.setAttribute(Qt.WidgetAttribute.WA_MacShowFocusRect, False)    # macOS

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

    def _get_icon_color(self) -> str:
        if not self.isEnabled():
            name = "RadioButtonForegroundDisabled"
        elif self.isPressed:
            name = "RadioButtonForegroundPressed"
        elif self.isHover:
            name = "RadioButtonForegroundPointerOver"
        else:
            name = "RadioButtonForeground"
        return PyLunixStyleSheet.RADIO_BUTTON.get_value(name)

    def updateIcon(self):
        if hasattr(self, "_icon_source") and callable(self._icon_source):
            try:
                color = self._get_icon_color()
                icon = self._icon_source(color)
                if icon:
                    super().setIcon(icon)
                    self._icon = icon
            except Exception as e:
                print(f"[RadioButton] Failed to update icon: {e}")

    def mousePressEvent(self, event): self.isPressed = True; super().mousePressEvent(event)
    def mouseReleaseEvent(self, event): self.isPressed = False; super().mouseReleaseEvent(event)
    def enterEvent(self, event): self.isHover = True; self.update(); super().enterEvent(event)
    def leaveEvent(self, event): self.isHover = False; self.update(); super().leaveEvent(event)

    def showEvent(self, event):
        super().showEvent(event)
        self.updateIcon()

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        self._drawIndicator(painter)
        painter.end()

    def _drawIndicator(self, painter: QPainter):
        size = 16
        cx = 4
        cy = (self.height() - size) // 2
        outer_rect = QRectF(cx, cy, size, size)

        border_stroke_key = "RadioButtonOuterEllipseStroke"
        fill_color_key = "RadioButtonOuterEllipseFill"
        dot_color_key = "RadioButtonCheckGlyphFill"

        if self.isChecked():
            if self.isEnabled():
                border_stroke_key = "RadioButtonOuterEllipseCheckedStroke"
                fill_color_key = "RadioButtonOuterEllipseCheckedFill"
                dot_color_key = "RadioButtonCheckGlyphFill"
                
                if self.isPressed:
                    border_stroke_key += "Pressed"
                    fill_color_key += "Pressed"
                    dot_color_key += "Pressed"
                elif self.isHover:
                    border_stroke_key += "PointerOver"
                    fill_color_key += "PointerOver"
                    dot_color_key += "PointerOver"
            else:
                border_stroke_key = "RadioButtonOuterEllipseCheckedStrokeDisabled"
                fill_color_key = "RadioButtonOuterEllipseCheckedFillDisabled"
                dot_color_key = "RadioButtonCheckGlyphFillDisabled"
        
            border_color = QColor(PyLunixStyleSheet.RADIO_BUTTON.get_value(border_stroke_key))
            fill_color = QColor(PyLunixStyleSheet.RADIO_BUTTON.get_value(fill_color_key))
            dot_color = QColor(PyLunixStyleSheet.RADIO_BUTTON.get_value(dot_color_key))

        else:
            dot_color = Qt.GlobalColor.transparent

            if self.isEnabled():
                border_stroke_key = "RadioButtonOuterEllipseStroke"
                fill_color_key = "RadioButtonOuterEllipseFill"
                
                if self.isPressed:
                    border_stroke_key += "Pressed"
                    fill_color_key += "Pressed"
                elif self.isHover:
                    border_stroke_key += "PointerOver"
                    fill_color_key += "PointerOver"
            else:
                border_stroke_key = "RadioButtonOuterEllipseStrokeDisabled"
                fill_color_key = "RadioButtonOuterEllipseFillDisabled"
            

            border_color = QColor(PyLunixStyleSheet.RADIO_BUTTON.get_value(border_stroke_key))

            fill_color_value = PyLunixStyleSheet.RADIO_BUTTON.get_value(fill_color_key)
            fill_color = QColor(fill_color_value) if fill_color_value.startswith("#") else Qt.GlobalColor.transparent
            
            if fill_color_value.lower().endswith("transparentbrush"):
                fill_color = Qt.GlobalColor.transparent

        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        
        pen = QPen(border_color)
        pen.setWidthF(1.0)
        painter.setPen(pen)
        painter.setBrush(fill_color)
        painter.drawEllipse(outer_rect)

        if self.isChecked():
            inner_size = size * 0.5
            inner_offset = (size - inner_size) / 2
            inner_rect = QRectF(cx + inner_offset, cy + inner_offset, inner_size, inner_size)
            painter.setBrush(dot_color)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(inner_rect)