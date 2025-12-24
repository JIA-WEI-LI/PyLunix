from typing import Union, Callable, Optional
from PyQt5.QtWidgets import QWidget, QRadioButton
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen
from PyQt5.QtCore import QSize, QRectF, Qt

from ....common.stylesheet import PyLunixStyleSheet

class RadioButton(QRadioButton):
    """
    A custom-themed RadioButton with dynamic icon and indicator rendering.

    This class extends QRadioButton to provide specialized drawing logic for the 
    circular indicator, supporting various states (hover, pressed, checked, disabled). 
    It also supports dynamic icon coloring based on the current theme state.

    Attributes:
        isPressed (bool): Tracks mouse press state for visual feedback.
        isHover (bool): Tracks mouse hover state for visual feedback.
        _icon_source (Optional[Callable]): Callback for generating theme-aware icons.
    """

    def __init__(self, text: str = "", icon: Optional[QIcon] = None, parent: Optional[QWidget] = None):
        """
        Initialize the RadioButton.

        Args:
            text (str): The label text. Defaults to "".
            icon (QIcon, optional): Initial icon. Defaults to None.
            parent (QWidget, optional): Parent widget. Defaults to None.
        """
        super().__init__(text=text, parent=parent)
        self.isPressed = False
        self.isHover = False
        self._icon_source = None
        self._icon = QIcon()

        self.setProperty("class", "RadioButton")
        self.setIconSize(QSize(16, 16))

        if text: self.setText(text)
        if icon: self.setIcon(icon)
        else: self.setIcon(QIcon())

        # Apply the RadioButton specific stylesheet
        PyLunixStyleSheet.RADIO_BUTTON.apply(self)
        
        # Disable macOS specific focus ring for a cleaner cross-platform look
        self.setAttribute(Qt.WidgetAttribute.WA_MacShowFocusRect, False)

    def setIcon(self, icon: Union[QIcon, Callable]):
        """
        Set a static icon or a dynamic icon source.

        Args:
            icon (Union[QIcon, Callable]): Either a QIcon or a function 
                returning a QIcon based on color.
        """
        if callable(icon):
            self.setIconSource(icon)
        else:
            super().setIcon(icon)
            self._icon_source = None
            self._icon = icon

    def setIconSource(self, icon_accessor: Callable[[str], QIcon]):
        """
        Assign a dynamic icon generator callback.

        Args:
            icon_accessor (Callable): Function that takes a color string 
                and returns a QIcon.
        """
        self._icon_source = icon_accessor
        self.updateIcon()

    def _get_icon_color(self) -> str:
        """
        Determine the state-based foreground color from the stylesheet.

        Returns:
            str: Hex color string.
        """
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
        """Update the displayed icon using the icon source callback."""
        if hasattr(self, "_icon_source") and callable(self._icon_source):
            try:
                color = self._get_icon_color()
                icon = self._icon_source(color)
                if icon:
                    super().setIcon(icon)
                    self._icon = icon
            except Exception as e:
                print(f"[RadioButton] Failed to update icon: {e}")

    def mousePressEvent(self, event): 
        """Handle mouse press and trigger visual update."""
        self.isPressed = True; super().mousePressEvent(event)
        
    def mouseReleaseEvent(self, event): 
        """Handle mouse release and trigger visual update."""
        self.isPressed = False; super().mouseReleaseEvent(event)
        
    def enterEvent(self, event): 
        """Handle hover enter."""
        self.isHover = True; self.update(); super().enterEvent(event)
        
    def leaveEvent(self, event): 
        """Handle hover leave."""
        self.isHover = False; self.update(); super().leaveEvent(event)

    def showEvent(self, event):
        """Ensure icon state is correct when the button is first shown."""
        super().showEvent(event)
        self.updateIcon()

    def paintEvent(self, e):
        """
        Custom paint engine to render the radio button components.

        First calls the base implementation for text and layout, then 
        draws the custom indicator.
        """
        super().paintEvent(e)
        painter = QPainter(self)
        self._drawIndicator(painter)
        painter.end()

    def _drawIndicator(self, painter: QPainter):
        """
        Manually draws the radio button's circular indicator.

        Logic:
        1. Selects colors based on (Checked/Unchecked) + (Enabled/Disabled) + (Hover/Pressed).
        2. Draws the outer border ellipse.
        3. If checked, draws the inner dot (glyph).

        Args:
            painter (QPainter): The active painter from paintEvent.
        """
        size = 16
        cx = 4
        cy = (self.height() - size) // 2
        outer_rect = QRectF(cx, cy, size, size)

        # Default key values
        border_stroke_key = "RadioButtonOuterEllipseStroke"
        fill_color_key = "RadioButtonOuterEllipseFill"
        dot_color_key = "RadioButtonCheckGlyphFill"

        # State management for key names
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

        # Draw logic
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        
        # Draw Outer Ring
        pen = QPen(border_color)
        pen.setWidthF(1.0)
        painter.setPen(pen)
        painter.setBrush(fill_color)
        painter.drawEllipse(outer_rect)

        # Draw Inner Check Dot
        if self.isChecked():
            inner_size = size * 0.5
            inner_offset = (size - inner_size) / 2
            inner_rect = QRectF(cx + inner_offset, cy + inner_offset, inner_size, inner_size)
            painter.setBrush(dot_color)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(inner_rect)