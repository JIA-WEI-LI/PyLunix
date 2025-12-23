from typing import Optional, Union
from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
   
from ....common.stylesheet import PyLunixStyleSheet

class RichTextBlock(QTextBrowser):
    """
    A read-only text container for displaying styled HTML or rich text.

    RichTextBlock simplifies the process of displaying formatted text while 
    maintaining theme consistency. It is specifically configured to behave 
    more like a dynamic label by hiding scrollbars by default and providing 
    utility methods for text interaction and selection highlighting.

    Attributes:
        None (Inherits all attributes from QTextBrowser).
    """

    def __init__(self, text: Optional[str] = None, parent: Optional[object] = None):
        """
        Initialize the RichTextBlock.

        Args:
            text (str, optional): The initial HTML or rich text string to display.
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(parent)
        
        # Set the CSS class for styling via PyLunixStyleSheet
        self.setProperty("class", "RichTextBlock")

        # Disable scrollbars to mimic a static text block appearance
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Set initial content if provided
        if text is not None: 
            self.setHtml(text)

        # Apply specific stylesheet for rich text blocks
        PyLunixStyleSheet.RICHTEXT_BLOCK.apply(self)

    def setTextSelection(self, 
                         type: Qt.TextInteractionFlag = Qt.TextInteractionFlag.NoTextInteraction,
                         highlight_color: Optional[Union[Qt.GlobalColor, QColor, str]] = None):
        """
        Configure how users can interact with the text and customize selection colors.

        This method adjusts the mouse cursor automatically based on whether the 
        text is selectable.

        Args:
            type (Qt.TextInteractionFlag): Flags determining interaction (Selectable, etc.).
                Defaults to NoTextInteraction.
            highlight_color (QColor, optional): The background color for selected text.
        """
        # Update interaction behavior
        self.setTextInteractionFlags(type)

        # Automatically update the cursor based on interaction flags
        selectable_flags = [
            Qt.TextInteractionFlag.TextSelectableByMouse, 
            Qt.TextInteractionFlag.TextBrowserInteraction, 
            Qt.TextInteractionFlag.TextSelectableByKeyboard, 
            Qt.TextInteractionFlag.TextEditorInteraction,
            # Handle combined flag for mouse and keyboard selection
            Qt.TextInteractionFlag.TextSelectableByMouse | Qt.TextInteractionFlag.TextSelectableByKeyboard
        ]

        if type in selectable_flags:
            self.setCursor(Qt.CursorShape.IBeamCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)

        # Customize the selection palette colors
        if highlight_color is not None:
            palette = self.palette()
            palette.setColor(QPalette.Highlight, QColor(highlight_color)) 
            palette.setColor(QPalette.HighlightedText, QColor(Qt.white)) 
            self.setPalette(palette)