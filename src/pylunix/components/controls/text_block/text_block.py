from typing import Union, Optional
from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt, QEvent

from ....common.stylesheet import PyLunixStyleSheet
from ....common.typography import TypographyStyle, PyLnuixTypography
from ....common.factories import StateColorResolver

class TextBlock(QLabel):
    """
    An enhanced Label widget designed with WinUI 3 design principles, 
    supporting fluent typography styles and adaptive interactive states.

    The TextBlock is the foundational text component of the PyLunix UI system. 
    It extends QLabel to provide high-level control over typography, 
    automatic theme-based color resolution, and subtle micro-interactions 
    (hover/press states) reminiscent of Fluent Design.

    Key Features:
    - Adaptive Rendering: Automatically updates colors based on application themes.
    - Typography First: Built-in support for predefined text styles (Title, Body, Caption).
    - Interactive Feedback: Optional color transitions during mouse interactions.
    - Precision Layout: Enhanced handling of padding, alignment, and selection.

    Attributes:
        isPressed (bool): True if the mouse button is currently held down over the widget.
        isHover (bool): True if the mouse cursor is currently positioned over the widget.
        _is_interactive (bool): Determines if the widget provides visual feedback on interaction.
    """

    def __init__(self, text: str, 
                 font_family: Optional[str] = None,
                 font_size: Optional[int] = None,
                 font_weight: Optional[QFont.Weight] = None,
                 foreground: Optional[Union[Qt.GlobalColor, QColor, str]] = None,
                 is_interactive: bool = False,
                 parent: QWidget = None):
        """
        Initialize the TextBlock with typography and theme parameters.

        Args:
            text (str): The initial content of the text block.
            font_family (str, optional): Custom font family (e.g., 'Segoe UI Variable').
            font_size (int, optional): Font size in pixels. Defaults to theme standard.
            font_weight (QFont.Weight, optional): Weight of the font (e.g., QFont.Bold).
            foreground (Union, optional): Hardcoded color override. If None, resolves via theme.
            is_interactive (bool): Enable hover and press visual states. Defaults to False.
            parent (QWidget, optional): Parent container widget.
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
        return StateColorResolver.resolve("TextBlock", "Foreground", self, theme_type="TEXT_BLOCK")

# region Text Properties
    def setFontSize(self, size: int):
        """Update only the font size."""
        self._font_size = size
        self.setFont(QFont(self._font_family, self._font_size, self._font_weight))

    def setFontFamily(self, family: str):
        """Update only the font family."""
        self._font_family = family
        self.setFont(QFont(self._font_family, self._font_size, self._font_weight))

    def setFontWeight(self, weight: QFont.Weight):
        """Update only the font weight (Note: Method name 'setFontWidget' refers to 'Weight')."""
        self._font_weight = weight
        self.setFont(QFont(self._font_family, self._font_size, self._font_weight))

    def setFontStyle(self, style: TypographyStyle):
        """
        Apply a predefined typography style from the PyLnuix system.

        This is the recommended way to set text appearance to maintain 
        design consistency across the application, similar to WinUI 3's 
        TextBlock Style property.

        Args:
            style (TypographyStyle): The style enum (e.g., Title, Subtitle, Body, Caption).
        """
        font = PyLnuixTypography.get_font(style)
        self.setFont(font)

    def setTextSelection(self, 
                         type: Qt.TextInteractionFlag = Qt.TextInteractionFlag.NoTextInteraction,
                         highlight_color: Optional[Qt.GlobalColor] = None):
        """
        Configure text interaction and selection aesthetics.

        Args:
            type (Qt.TextInteractionFlag): Defines how the user can interact with the text.
                Defaults to NoTextInteraction (static text).
            highlight_color (Qt.GlobalColor, optional): The color of the selection 
                background. Uses theme default if None.
        
        Note:
            Enabling selection will automatically change the cursor to an I-Beam 
            shape to provide visual affordance.
        """
        self.setTextInteractionFlags(type)
        selectable = [
            Qt.TextInteractionFlag.TextSelectableByMouse, 
            Qt.TextInteractionFlag.TextBrowserInteraction, 
            Qt.TextInteractionFlag.TextSelectableByKeyboard, 
            Qt.TextInteractionFlag.TextEditorInteraction, 
            Qt.TextInteractionFlag.TextSelectableByMouse | 
            Qt.TextInteractionFlag.TextSelectableByKeyboard
        ]

        self.setCursor(Qt.CursorShape.IBeamCursor if type in selectable else Qt.CursorShape.ArrowCursor)

        if highlight_color is not None:
            palette = self.palette()
            palette.setColor(QPalette.ColorRole.Highlight, QColor(highlight_color)) 
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor(Qt.white)) 
            self.setPalette(palette)

    def setTextColor(self, color: Union[Qt.GlobalColor, QColor, str]):
        """Manually set the foreground color, overriding theme defaults."""
        self._foreground = color
        self._setTextgroundColor()

    def _setTextgroundColor(self):
        """
        Updates the widget's palette to reflect current state and theme.

        This method orchestrates the color resolution process, checking for 
        user overrides first, then falling back to the StateColorResolver 
        which handles 'Normal', 'Hover', and 'Pressed' color logic.
        """
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