from typing import Union, Optional
from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt, QEvent

from ....common.stylesheet import PyLunixStyleSheet
from ....common.typography import TypographyStyle, PyLnuixTypography

class TextBlock(QLabel):
    """
    An enhanced Label widget supporting typography styles and interactive states.

    This class serves as the primary text component in the PyLunix UI system. 
    It supports dynamic font properties, theme-aware coloring, and optional 
    interactive feedback (changing color on hover or press).

    Attributes:
        isPressed (bool): Internal state tracking if the mouse is currently pressing the text.
        isHover (bool): Internal state tracking if the mouse is hovering over the text.
        _is_interactive (bool): If True, the widget will update its foreground color 
                                based on mouse events.
    """

    def __init__(self, text: str, 
                 font_family: Optional[str] = None,
                 font_size: Optional[int] = None,
                 font_weight: Optional[QFont.Weight] = None,
                 foreground: Optional[Union[Qt.GlobalColor, QColor, str]] = None,
                 is_interactive: bool = False,
                 parent: QWidget = None):
        """
        Initialize the TextBlock.

        Args:
            text (str): The initial text content.
            font_family (str, optional): Custom font family name.
            font_size (int, optional): Custom font size in pixels.
            font_weight (QFont.Weight, optional): Custom font weight.
            foreground (Union, optional): Manual override for text color.
            is_interactive (bool): Enable or disable hover/press color changes.
            parent (QWidget, optional): Parent widget.
        """
        super().__init__(text=text, parent=parent)

        self._font_family = font_family
        self._font_size = font_size
        self._font_weight = font_weight
        self._foreground = foreground
        self._is_interactive = is_interactive

        self.isPressed = False
        self.isHover = False

        # Set identity for QSS styling
        self.setProperty("class", "TextBlock")
        self.setMinimumHeight(36)
        self.setText(text if text else "")
        
        # Apply theme-based styling
        PyLunixStyleSheet.TEXT_BLOCK.apply(self)
        
        # Priority 1: User defined foreground color
        if foreground is not None:
            self.setTextColor(foreground)
        # Priority 2: Style-based or default theme color
        else:
            self._setTextgroundColor()

        # Handle custom font overrides
        if (self._font_family is not None or 
            self._font_size is not None or 
            self._font_weight is not None):
            current_font = self.font()
            final_family = self._font_family if self._font_family is not None else current_font.family()
            final_size = self._font_size if self._font_size is not None else current_font.pixelSize()
            final_weight = self._font_weight if self._font_weight is not None else current_font.weight()
            self.setFont(QFont(final_family, final_size, final_weight))

    def _get_text_color(self) -> str:
        """Determines the appropriate theme key based on the current state."""
        if not self.isEnabled():
            name = "TextBlockForegroundDisabled"
        elif self.isPressed:
            name = "TextBlockForegroundPressed"
        elif self.isHover:
            name = "TextBlockForegroundPointerOver"
        else:
            name = "TextBlockForeground"
        return PyLunixStyleSheet.TEXT_BLOCK.get_value(name)

# region Text Properties
    def setFontSize(self, size: int):
        """Update only the font size."""
        self._font_size = size
        self.setFont(QFont(self._font_family, self._font_size, self._font_weight))

    def setFontFamily(self, family: str):
        """Update only the font family."""
        self._font_family = family
        self.setFont(QFont(self._font_family, self._font_size, self._font_weight))

    def setFontWidget(self, weight: QFont.Weight):
        """Update only the font weight (Note: Method name 'setFontWidget' refers to 'Weight')."""
        self._font_weight = weight
        self.setFont(QFont(self._font_family, self._font_size, self._font_weight))

    def setFontStyle(self, style: TypographyStyle):
        """Apply a predefined PyLnuixTypography style (e.g., Title, Body)."""
        font = PyLnuixTypography.get_font(style)
        self.setFont(font)

    def setTextSelection(self, 
                         type: Qt.TextInteractionFlag = Qt.TextInteractionFlag.NoTextInteraction,
                         highlight_color: Optional[Qt.GlobalColor] = None):
        """
        Enable text selection and customize the selection highlight color.
        
        Automatically updates the cursor to an I-Beam when selectable.
        """
        self.setTextInteractionFlags(type)
        selectable = [
            Qt.TextInteractionFlag.TextSelectableByMouse, 
            Qt.TextInteractionFlag.TextBrowserInteraction, 
            Qt.TextInteractionFlag.TextSelectableByKeyboard, 
            Qt.TextInteractionFlag.TextEditorInteraction, 
            Qt.TextInteractionFlag.TextSelectableByMouse | Qt.TextInteractionFlag.TextSelectableByKeyboard
        ]

        self.setCursor(Qt.CursorShape.IBeamCursor if type in selectable else Qt.CursorShape.ArrowCursor)

        if highlight_color is not None:
            palette = self.palette()
            palette.setColor(QPalette.Highlight, QColor(highlight_color)) 
            palette.setColor(QPalette.HighlightedText, QColor(Qt.white)) 
            self.setPalette(palette)

    def setTextColor(self, color: Union[Qt.GlobalColor, QColor, str]):
        """Manually set the foreground color, overriding theme defaults."""
        self._foreground = color
        self._setTextgroundColor()

    def _setTextgroundColor(self):
        """Internal method to update the QPalette's WindowText role."""
        color = self._get_text_color() if self._foreground is None else self._foreground
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.WindowText, QColor(color))
        self.setPalette(palette)
# endregion

# region Event
    def enterEvent(self, e): 
        if self._is_interactive:
            self.isHover = True
            self._setTextgroundColor()
        super().enterEvent(e)

    def leaveEvent(self, e): 
        if self._is_interactive:
            self.isHover = False
            self._setTextgroundColor()
        super().leaveEvent(e)

    def mousePressEvent(self, e): 
        if self._is_interactive:
            self.isPressed = True
            self._setTextgroundColor()
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e): 
        if self._is_interactive:
            self.isPressed = False
            self._setTextgroundColor()
        super().mouseReleaseEvent(e)

    def changeEvent(self, event: QEvent):
        """Handle theme or palette changes to refresh colors."""
        if event.type() in [QEvent.Type.StyleChange, QEvent.Type.PaletteChange]:
            self._setTextgroundColor()
        super().changeEvent(event)
# endregion