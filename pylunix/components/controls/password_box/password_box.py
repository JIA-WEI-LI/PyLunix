from typing import Optional
from PyQt5.QtWidgets import QLineEdit, QWidget, QVBoxLayout, QStyleOptionFrame, QStyle
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QFont, QPalette, QPen

from ..text_block.text_block import TextBlock
from ..text_box.text_box import _BaseTextBoxEdit
from ..tool_button.tool_button import TransparentToolButton
from ....common.stylesheet import PyLunixStyleSheet
from ....common.typography import TypographyStyle
from ....icons.win_icon_kit.win_icon import WinIcon
from ....utils.style_parser import extract_numbers

class PasswordBoxButton(TransparentToolButton):
    pressed_signal = pyqtSignal()
    released_signal = pyqtSignal()

    def __init__(self, icon, parent=None):
        super().__init__(icon, parent)
        self.isPressed = False
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(23, 23)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.isPressed = True
            self.pressed_signal.emit()
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.isPressed = False
            self.released_signal.emit()
        super().mouseReleaseEvent(e)

class PasswordBoxEdit(_BaseTextBoxEdit):
    _BUTTON_CLASS = PasswordBoxButton
    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)
        self.setProperty("class", "PasswordBoxEdit")

        self._isRevealButtonEnabled = True
        self._revealButtonAlwaysVisible = False

        self.revealButton = self._BUTTON_CLASS(WinIcon.REDEYE, self)
        self.hBoxLayout.addWidget(self.revealButton, 0, Qt.AlignmentFlag.AlignRight) 
        
        self.revealButton.pressed_signal.connect(lambda: self._toggleEchoMode(True))
        self.revealButton.released_signal.connect(lambda: self._toggleEchoMode(False))
        self.textChanged.connect(self._updateRevealButtonVisibility)

        self.setEchoMode(QLineEdit.EchoMode.Password)
        self._updateRevealButtonVisibility()
        self._adjustTextMargins() 

        PyLunixStyleSheet.PASSWORD_BOX.apply(self)

    def _toggleEchoMode(self, checked: bool):
        if checked:
            self.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.setEchoMode(QLineEdit.EchoMode.Password)

    def _adjustTextMargins(self):
        left = len(self.leftButtons) * 30
        right = len(self.rightButtons) * 30
        
        if self.isRevealButtonEnabled():
            right += 28 

        m = self.textMargins()
        self.setTextMargins(left, m.top(), right, m.bottom())
        
    def isRevealButtonEnabled(self) -> bool:
        return self._isRevealButtonEnabled

    def _updateRevealButtonVisibility(self):
        should_be_visible = (
            (self.hasFocus() and 
             bool(self.text() and not self.isReadOnly()) and 
             self.isRevealButtonEnabled()) or self._revealButtonAlwaysVisible
        )
        self.revealButton.setVisible(should_be_visible)
        self._adjustTextMargins()

    def setRevealButtonAlwaysVisible(self, always_visible: bool=True):
        self._revealButtonAlwaysVisible = always_visible
        self._updateRevealButtonVisibility()

    def setReadOnly(self, read_only: bool):
        super().setReadOnly(read_only)
        self._updateRevealButtonVisibility()

class PasswordBox(QWidget):
    def __init__(self, text: str="", header: Optional[str]=None, parent = None):
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

    def setHeader(self, text:str):
        if not self.header_label:
            self.header_label = TextBlock(text, parent=self)
            self.header_label.setProperty("class", "TextBlock")
            self.Vlayout.addWidget(self.header_label)
            PyLunixStyleSheet.TEXT_BLOCK.apply(self.header_label)
        else:
            self.header_label.setText(text)

    @property
    def edit(self):
        return self.passwordBoxEdit

    def text(self) -> str:
        return self.passwordBoxEdit.text()
    
    def clear(self):
        self.passwordBoxEdit.clear()
    
    def setText(self, text: str):
        self.passwordBoxEdit.setText(text)

    def setPlaceholderText(self, text: str):
        self.passwordBoxEdit.setPlaceholderText(text)

    def setRevealButtonAlwaysVisible(self, always_visible: bool=True):
        self._revealButtonAlwaysVisible = always_visible
        self.passwordBoxEdit._updateRevealButtonVisibility()

    def setReadOnly(self, read_only: bool):
        self.passwordBoxEdit.setReadOnly(read_only)

    def setFocus(self):
        self.passwordBoxEdit.setFocus()
    
    def setHighlightColor(self, background: QColor, text: Optional[QColor]=None):
        self.passwordBoxEdit.setHighlightColor(background, text)
        self.passwordBoxEdit.update()

    def setTextStyle(self,
                     font_style: Optional[TypographyStyle] = None,
                     font_family: Optional[str] = None,
                     font_size: Optional[int] = None,
                     font_weight: Optional[QFont.Weight] = None):
        self.passwordBoxEdit.setTextStyle(font_style=font_style,
                                           font_family=font_family,
                                           font_size=font_size,
                                           font_weight=font_weight)
        
    def setEchoMode(self, mode: QLineEdit.EchoMode):
        self.passwordBoxEdit.setEchoMode(mode)
# endregion