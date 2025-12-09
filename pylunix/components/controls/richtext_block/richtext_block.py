from typing import Optional
from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
   
from ....common.stylesheet import PyLunixStyleSheet

class RichTextBlock(QTextBrowser):
    def __init__(self, text: Optional[str]=None, parent=None):
        super().__init__(parent)
        
        self.setProperty("class", "RichTextBlock")

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        if text is not None: self.setHtml(text)

        PyLunixStyleSheet.RICHTEXT_BLOCK.apply(self)

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