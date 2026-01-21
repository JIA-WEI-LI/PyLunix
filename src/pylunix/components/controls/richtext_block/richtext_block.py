from typing import Optional, Union
from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtGui import QPalette, QColor, QDesktopServices, QTextOption, QTextBlockFormat, QTextCursor
from PyQt5.QtCore import Qt, QUrl
   
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
        Initializes the RichTextBlock with default Fluent styles.

        Args:
            text (str, optional): The initial HTML or rich text string to display.
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.setProperty("class", "RichTextBlock")

        # Basic Configurations
        self.setOpenLinks(False) 
        self.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.document().setDocumentMargin(0)
        self.anchorClicked.connect(self._handle_link_click)

        self.setReadOnly(True)
        self.setFrameStyle(0)
        
        # UI Policy: Disable scrollbars to behave like a label
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        if text is not None: 
            self.setHtml(text)

        # Use documentLayout's signal for more reliable height updates
        self.document().contentsChanged.connect(self._adjust_size)

        PyLunixStyleSheet.RICHTEXT_BLOCK.apply(self)
        self.update_font()

    def _adjust_size(self):
        """
        Automatically adjusts the fixed height of the widget to match its content.
        Triggered whenever the document layout or content changes.
        """
        doc_height = self.document().size().height()
        self.setFixedHeight(int(doc_height) + 2)

    def _handle_link_click(self, url: QUrl):
        """
        Handles hyperlink clicks by opening them in the system's default browser.

        Args:
            url (QUrl): The URL of the clicked anchor tag.
        """
        QDesktopServices.openUrl(url)

    def update_font(self):
        """
        Syncs the document's default font with the widget's current font.
        Ensures consistency when the parent or theme changes the font.
        """
        current_font = self.font()
        self.document().setDefaultFont(current_font)

    def setTextAlignment(self, alignment: Qt.Alignment):
        """
        Sets the text alignment for the entire document.

        Args:
            alignment (Qt.Alignment): The desired alignment (e.g., Qt.AlignCenter).
        """
        self.setAlignment(alignment)
        option = self.document().defaultTextOption()
        option.setAlignment(alignment)
        self.document().setDefaultTextOption(option)

    def setLineHeight(self, value: float, is_percentage: bool = True):
        """
        Adjusts the line spacing of the text.

        Args:
            value (float): The height value.
            is_percentage (bool): If True, treats value as a percentage (100 = single spacing). 
                If False, treats value as a fixed pixel height. Defaults to True.
        """
        cursor = self.textCursor()
        cursor.select(QTextCursor.Document)
        
        block_format = QTextBlockFormat()
        if is_percentage:
            block_format.setLineHeight(value, QTextBlockFormat.ProportionalHeight)
        else:
            block_format.setLineHeight(value, QTextBlockFormat.FixedHeight)
            
        cursor.setBlockFormat(block_format)
        self._adjust_size()

    # def setWordWrap(self, wrap: bool):
    #     if wrap:
    #         self.setLineWrapMode(QTextBrowser.WidgetWidth)
    #         option = self.document().defaultTextOption()
    #         option.setWrapMode(QTextOption.WordWrap)
    #     else:
    #         self.setLineWrapMode(QTextBrowser.NoWrap)
    #         option = self.document().defaultTextOption()
    #         option.setWrapMode(QTextOption.NoWrap)
        
    #     self.document().setDefaultTextOption(option)
    #     self._adjust_size()

    def setTextSelection(self, 
                         type: Qt.TextInteractionFlag = Qt.TextInteractionFlag.NoTextInteraction,
                         highlight_color: Optional[Union[Qt.GlobalColor, QColor, str]] = None):
        """
        Configures text interaction behavior and selection aesthetics.

        This method automatically updates the mouse cursor (Arrow vs. IBeam) based on 
        whether the text is selectable, matching the expected UX of modern OSs.

        Args:
            interaction_type (Qt.TextInteractionFlag): Flags to enable selection/interaction.
                Defaults to NoTextInteraction.
            highlight_color (QColor, optional): The background color for selected text.
                If provided, updates the widget's palette.
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

        if type & (Qt.TextInteractionFlag.TextSelectableByMouse | Qt.TextInteractionFlag.TextSelectableByKeyboard):
            self.setCursor(Qt.CursorShape.IBeamCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)

        # Customize the selection palette colors
        if highlight_color is not None:
            palette = self.palette()
            palette.setColor(QPalette.Highlight, QColor(highlight_color)) 
            palette.setColor(QPalette.HighlightedText, QColor(Qt.white)) 
            self.setPalette(palette)