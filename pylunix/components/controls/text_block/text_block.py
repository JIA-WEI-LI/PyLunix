from typing import Union, Optional
from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt

from ....common.stylesheet import PyLunixStyleSheet
from ....common.typography import TypographyStyle, PyLnuixTypography

class TextBlock(QLabel):
    def __init__(self, text: str, 
                 font_family: Optional[str] = None,
                 font_size: Optional[int] = None,
                 font_weight: Optional[QFont.Weight] = None,
                 parent: QWidget=None):
        super().__init__(text=text, parent=parent)

        self._font_family = font_family
        self._font_size = font_size
        self._font_weight = font_weight

        self.setProperty("class", "TextBlock")
        self.setMinimumHeight(36)
        self.setText(text if text else "")

        PyLunixStyleSheet.TEXT_BLOCK.apply(self)

        if (self._font_family is not None or 
            self._font_size is not None or 
            self._font_weight is not None):
            current_font = self.font()

            final_family = self._font_family if self._font_family is not None else current_font.family()
            final_size = self._font_size if self._font_size is not None else current_font.pixelSize()
            final_weight = self._font_weight if self._font_weight is not None else current_font.weight()

            font = QFont(final_family, final_size, final_weight)
            self.setFont(font)

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