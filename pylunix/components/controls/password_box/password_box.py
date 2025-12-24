from typing import Optional, Union
from PyQt5.QtWidgets import QLineEdit, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QFont

from ..text_block.text_block import TextBlock
from ..text_box.text_box import _BaseTextBoxEdit
from ..tool_button.tool_button import TransparentToolButton
from ....common.stylesheet import PyLunixStyleSheet
from ....common.typography import TypographyStyle
from ....icons.win_icon_kit.win_icon import WinIcon
from ....utils.style_parser import extract_numbers

# region PasswordBoxButton
class PasswordBoxButton(TransparentToolButton):
    """
    A specialized tool button for the PasswordBox that emits signals on press and release.

    This button is designed to trigger password visibility toggling, specifically 
    reacting to the start and end of a mouse click.

    Signals:
        pressed_signal: Emitted when the left mouse button is pressed.
        released_signal: Emitted when the left mouse button is released.
    """

    def __init__(self, icon: WinIcon, parent: Optional[QWidget] = None):
        """
        Initialize the PasswordBoxButton.

        Args:
            icon (WinIcon): The icon (e.g., Eye icon) to display.
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(icon, parent)
        self.isPressed = False
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(23, 23)

    def mousePressEvent(self, e):
        """Handle mouse press to emit pressed_signal."""
        if e.button() == Qt.MouseButton.LeftButton:
            self.isPressed = True
            self.pressed_signal.emit()
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        """Handle mouse release to emit released_signal."""
        if e.button() == Qt.MouseButton.LeftButton:
            self.isPressed = False
            self.released_signal.emit()
        super().mouseReleaseEvent(e)
# endregion

# region PasswordBoxEdit
class PasswordBoxEdit(_BaseTextBoxEdit):
    """
    An input field that conceals characters and provides a toggle to reveal them.

    This class extends the base text box to include a 'reveal' button. The text 
    is hidden by default and only shown when the user holds down the reveal button.

    Attributes:
        revealButton (PasswordBoxButton): The button used to toggle password visibility.
    """
    _BUTTON_CLASS = PasswordBoxButton

    def __init__(self, text: str = "", parent: Optional[QWidget] = None):
        """
        Initialize the PasswordBoxEdit.

        Args:
            text (str): The initial text in the box. Defaults to "".
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(text, parent)
        self.setProperty("class", "PasswordBoxEdit")

        self._isRevealButtonEnabled = True
        self._revealButtonAlwaysVisible = False

        # Setup reveal button
        self.revealButton = self._BUTTON_CLASS(WinIcon.REDEYE, self)
        self.hBoxLayout.addWidget(self.revealButton, 0, Qt.AlignmentFlag.AlignRight) 
        
        # Connect signals for temporary password revelation
        self.revealButton.pressed_signal.connect(lambda: self._toggleEchoMode(True))
        self.revealButton.released_signal.connect(lambda: self._toggleEchoMode(False))
        self.textChanged.connect(self._updateRevealButtonVisibility)

        self.setEchoMode(QLineEdit.EchoMode.Password)
        self._updateRevealButtonVisibility()
        self._adjustTextMargins() 

        PyLunixStyleSheet.PASSWORD_BOX.apply(self)

    def _toggleEchoMode(self, checked: bool):
        """
        Switch between Password and Normal echo modes.

        Args:
            checked (bool): If True, shows plain text; if False, hides it.
        """
        if checked:
            self.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.setEchoMode(QLineEdit.EchoMode.Password)

    def _adjustTextMargins(self):
        """Recalculate margins to prevent text from overlapping with buttons."""
        left = len(self.leftButtons) * 30
        right = len(self.rightButtons) * 30
        
        if self.isRevealButtonEnabled():
            right += 28 

        m = self.textMargins()
        self.setTextMargins(left, m.top(), right, m.bottom())
        
    def isRevealButtonEnabled(self) -> bool:
        """Check if the password reveal functionality is active."""
        return self._isRevealButtonEnabled

    def _updateRevealButtonVisibility(self):
        """
        Determine if the reveal button should be shown based on focus, 
        read-only status, and content presence.
        """
        should_be_visible = (
            (self.hasFocus() and 
             bool(self.text() and not self.isReadOnly()) and 
             self.isRevealButtonEnabled()) or self._revealButtonAlwaysVisible
        )
        self.revealButton.setVisible(should_be_visible)
        self._adjustTextMargins()

    def setRevealButtonAlwaysVisible(self, always_visible: bool = True):
        """Set whether the reveal button stays visible even without focus."""
        self._revealButtonAlwaysVisible = always_visible
        self._updateRevealButtonVisibility()

    def setReadOnly(self, read_only: bool):
        """Set the edit field to read-only and update UI state."""
        super().setReadOnly(read_only)
        self._updateRevealButtonVisibility()
# endregion

# region PasswordBox
class PasswordBox(QWidget):
    """
    A themed password input widget with an optional header label.

    This is a high-level component that wraps PasswordBoxEdit and provides 
    layout management for a title (header).
    """

    def __init__(self, text: str = "", header: Optional[str] = None, parent: Optional[QWidget] = None):
        """
        Initialize the PasswordBox.

        Args:
            text (str): Default text for the password field.
            header (str, optional): Label text to display above the input.
            parent (QWidget, optional): The parent widget.
        """
        super().__init__(parent)
        self.setProperty("class", "PasswordBox")

        self.Vlayout = QVBoxLayout(self)
        top_header_margin = extract_numbers(PyLunixStyleSheet.PASSWORD_BOX.get_value("PasswordBoxTopHeaderMargin"))
        self.Vlayout.setContentsMargins(
            top_header_margin[0], 
            top_header_margin[1],
            top_header_margin[2],
            top_header_margin[3])
        self.Vlayout.setSpacing(0)

        self.header_label = None
        if header:
            self.setHeader(header)
        
        self.passwordBoxEdit = PasswordBoxEdit(text=text, parent=self) 
        self.Vlayout.addWidget(self.passwordBoxEdit)

    def setHeader(self, text: str):
        """Set or update the header label text above the password field."""
        if not self.header_label:
            self.header_label = TextBlock(text, parent=self)
            self.header_label.setProperty("class", "TextBlock")
            self.Vlayout.addWidget(self.header_label)
            PyLunixStyleSheet.TEXT_BLOCK.apply(self.header_label)
        else:
            self.header_label.setText(text)

    @property
    def edit(self) -> PasswordBoxEdit:
        """Access the internal PasswordBoxEdit instance."""
        return self.passwordBoxEdit

    def text(self) -> str:
        """Get the current password text."""
        return self.passwordBoxEdit.text()
    
    def clear(self):
        """Clear the password field."""
        self.passwordBoxEdit.clear()
    
    def setText(self, text: str):
        """Set the password field text."""
        self.passwordBoxEdit.setText(text)

    def setPlaceholderText(self, text: str):
        """Set the helper text shown when the box is empty."""
        self.passwordBoxEdit.setPlaceholderText(text)

    def setRevealButtonAlwaysVisible(self, always_visible: bool = True):
        """Force the reveal button to be visible at all times."""
        self.passwordBoxEdit.setRevealButtonAlwaysVisible(always_visible)

    def setReadOnly(self, read_only: bool):
        """Set the component to read-only state."""
        self.passwordBoxEdit.setReadOnly(read_only)

    def setFocus(self):
        """Grant keyboard focus to the input field."""
        self.passwordBoxEdit.setFocus()
    
    def setHighlightColor(self, background: QColor, text: Optional[QColor] = None):
        """Define colors for text selection."""
        self.passwordBoxEdit.setHighlightColor(background, text)
        self.passwordBoxEdit.update()

    def setTextStyle(self,
                     font_style: Optional[TypographyStyle] = None,
                     font_family: Optional[str] = None,
                     font_size: Optional[int] = None,
                     font_weight: Optional[QFont.Weight] = None):
        """Apply typography settings to the input field."""
        self.passwordBoxEdit.setTextStyle(font_style=font_style,
                                           font_family=font_family,
                                           font_size=font_size,
                                           font_weight=font_weight)
        
    def setEchoMode(self, mode: QLineEdit.EchoMode):
        """Set the echo mode (Normal, Password, NoEcho, etc.)."""
        self.passwordBoxEdit.setEchoMode(mode)
# endregion