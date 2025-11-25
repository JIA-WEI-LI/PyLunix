from typing import Union, Optional
from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt, QEvent

from ....common.stylesheet import PyLunixStyleSheet
from ....common.typography import TypographyStyle, PyLnuixTypography

class TextBlock(QLabel):
    def __init__(self, text: str, 
                 font_family: Optional[str] = None,
                 font_size: Optional[int] = None,
                 font_weight: Optional[QFont.Weight] = None,
                 foreground: Optional[Union[Qt.GlobalColor, QColor, str]] = None,
                 parent: QWidget=None):
        super().__init__(text=text, parent=parent)

        self._font_family = font_family
        self._font_size = font_size
        self._font_weight = font_weight
        self._foreground = foreground

        self.isPressed = False
        self.isHover = False

        self.setProperty("class", "TextBlock")
        self.setMinimumHeight(36)
        self.setText(text if text else "")
        self._setTextgroundColor()

        PyLunixStyleSheet.TEXT_BLOCK.apply(self)

        if foreground is not None:
            self.setTextColor(foreground)

        if (self._font_family is not None or 
            self._font_size is not None or 
            self._font_weight is not None):
            current_font = self.font()

            final_family = self._font_family if self._font_family is not None else current_font.family()
            final_size = self._font_size if self._font_size is not None else current_font.pixelSize()
            final_weight = self._font_weight if self._font_weight is not None else current_font.weight()

            font = QFont(final_family, final_size, final_weight)
            self.setFont(font)

    def _get_text_color(self) ->str:
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
    def setFont(self, font: QFont):
        return super().setFont(font)
    
    def setFontSize(self, size: int):
        self._font_size = size
        font = QFont(self._font_family, self._font_size, self._font_weight)
        self.setFont(font)

    def setFontFamily(self, family: str):
        self._font_family = family
        font = QFont(self._font_family, self._font_size, self._font_weight)
        self.setFont(font)

    def setFontWidget(self, widget: QFont.Weight):
        self._font_weight = widget
        font = QFont(self._font_family, self._font_size, self._font_weight)
        self.setFont(font)

    def setFontStyle(self, style: TypographyStyle):
        font = PyLnuixTypography.get_font(style)
        self.setFont(font)

    def setTextSelection(self, 
                         type: Qt.TextInteractionFlag = Qt.TextInteractionFlag.NoTextInteraction,
                         highlight_color: Optional[Qt.GlobalColor] = None):
        
        self.setTextInteractionFlags(type)

        if type in [Qt.TextInteractionFlag.TextSelectableByMouse, 
                Qt.TextInteractionFlag.TextBrowserInteraction, 
                Qt.TextInteractionFlag.TextSelectableByKeyboard, 
                Qt.TextInteractionFlag.TextEditorInteraction, 
                Qt.TextInteractionFlag.TextSelectableByMouse | Qt.TextInteractionFlag.TextSelectableByKeyboard]:
            self.setCursor(Qt.CursorShape.IBeamCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)

        if highlight_color is not None:
            palette = self.palette()
            palette.setColor(QPalette.Highlight, QColor(highlight_color)) 
            palette.setColor(QPalette.HighlightedText, QColor(Qt.white)) 
            self.setPalette(palette)

    def setTextColor(self, color: Union[Qt.GlobalColor, QColor, str]):
        self._foreground = color
        self._setTextgroundColor()

    def _setTextgroundColor(self):
        color = self._get_text_color() if self._foreground is None else self._foreground

        palette = self.palette()
        if isinstance(color, Qt.GlobalColor):
            palette.setColor(QPalette.ColorRole.WindowText, QColor(color))
        elif isinstance(color, QColor):
            palette.setColor(QPalette.ColorRole.WindowText, color)
        elif isinstance(color, str):
            palette.setColor(QPalette.ColorRole.WindowText, QColor(color))
        self.setPalette(palette)
# endregion

# region Event
    def enterEvent(self, e): self.isHover = True; self._setTextgroundColor(); super().enterEvent(e)
    def leaveEvent(self, e): self.isHover = False; self._setTextgroundColor(); super().leaveEvent(e)
    def mousePressEvent(self, e): self.isPressed = True; self._setTextgroundColor(); super().mousePressEvent(e)
    def mouseReleaseEvent(self, e): self.isPressed = False; self._setTextgroundColor(); super().mouseReleaseEvent(e)
    
    def changeEvent(self, event: QEvent):
        if event.type() == QEvent.Type.StyleChange or event.type() == QEvent.Type.PaletteChange:
            self._setTextgroundColor()
        super().changeEvent(event)
# endregion