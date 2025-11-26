
from typing import Optional, Union
from PyQt5.QtWidgets import QAction, QLineEdit, QHBoxLayout, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QRectF, QEvent
from PyQt5.QtGui import QPainter, QPainterPath, QColor, QPalette, QFont, QPen

from ..text_block.text_block import TextBlock
from ..tool_button.tool_button import TransparentToolButton
from ....common.stylesheet import PyLunixStyleSheet
from ....common.typography import TypographyStyle, PyLnuixTypography
from ....icons.win_icon_kit.win_icon import WinIcon
from ....utils.style_parser import extract_numbers

class _BaseTextBoxEdit(QLineEdit):
    _BUTTON_CLASS = None
    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)

        if self._BUTTON_CLASS is None:
            raise NotImplementedError("Subclasses must define the '_BUTTON_CLASS' attribute.")
        
        self.leftButtons = []
        self.rightButtons = []
        
        default_palette = self.palette()
        self._default_highlight_bg = default_palette.color(QPalette.Highlight)
        self._default_highlight_text = default_palette.color(QPalette.HighlightedText)

        self.hBoxLayout = QHBoxLayout(self)
        inner_button_margin = extract_numbers(PyLunixStyleSheet.TEXT_BOX.get_value("TextBoxInnerButtonMargin"))
        self.hBoxLayout.setContentsMargins(
            inner_button_margin[0], 
            inner_button_margin[1],
            inner_button_margin[2],
            inner_button_margin[3])
        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

    def addAction(self, action: QAction, position: QLineEdit.ActionPosition = QLineEdit.ActionPosition.TrailingPosition):
        button = self._BUTTON_CLASS(action.icon(), self) 
        button.setAction(action)

        if position == QLineEdit.ActionPosition.LeadingPosition:
            self.hBoxLayout.insertWidget(len(self.leftButtons), button, 0, Qt.AlignmentFlag.AlignLeading)
            if not self.leftButtons:
                self.hBoxLayout.insertStretch(1, 1)
            self.leftButtons.append(button)
        else:
            insert_index = self.hBoxLayout.count() - len(self.rightButtons)

            if self.leftButtons:
                insert_index = self.hBoxLayout.count() - 1 - len(self.rightButtons)
            else:
                 insert_index = self.hBoxLayout.count() - 1 - len(self.rightButtons) 

            self.hBoxLayout.insertWidget(insert_index, button, 0, Qt.AlignmentFlag.AlignRight)
            self.rightButtons.append(button)

        self._adjustTextMargins()

    def _adjustTextMargins(self):
        left = len(self.leftButtons) * 30
        right = len(self.rightButtons) * 30
        
        m = self.textMargins()
        self.setTextMargins(left, m.top(), right, m.bottom())

    def setTextStyle(self,
                     font_style: Optional[TypographyStyle] = None,
                     font_family: Optional[str] = None,
                     font_size: Optional[int] = None,
                     font_weight: Optional[QFont.Weight] = None):
        if font_style is not None:
            final_font = PyLnuixTypography.get_font(font_style)
        else:
            final_font = self.font()
        
        if (font_family is not None or 
            font_size is not None or 
            font_weight is not None):

            final_family = font_family if font_family is not None else final_font.family()
            final_size = font_size if font_size is not None else final_font.pixelSize()
            final_weight = font_weight if font_weight is not None else final_font.weight()

            final_font = QFont(final_family, final_size, final_weight)

        self.setFont(final_font)

    def setHighlightColor(self, background: QColor, text: Optional[QColor] = None):
        palette = self.palette()
        if background is None:
            bg_color = self._default_highlight_bg
        else:
            bg_color = QColor(background) if isinstance(background, str) else background
        palette.setColor(QPalette.Highlight, bg_color)
        
        if text is None:
            text_color = self._default_highlight_text
        else:
            text_color = QColor(text) if isinstance(text, str) else text
        palette.setColor(QPalette.HighlightedText, text_color)
        self.setPalette(palette)

    def enterEvent(self, a0):
        self.setCursor(Qt.CursorShape.IBeamCursor)
        return super().enterEvent(a0)
    
    def focusInEvent(self, e):
        super().focusInEvent(e)
        if hasattr(self, '_updateRevealButtonVisibility'):
            self._updateRevealButtonVisibility()
        elif hasattr(self, '_updateClearButtonVisibility'):
            self._updateClearButtonVisibility()

    def focusOutEvent(self, e):
        super().focusOutEvent(e)
        if hasattr(self, '_updateRevealButtonVisibility'):
            self._updateRevealButtonVisibility()
        elif hasattr(self, '_updateClearButtonVisibility'):
            self._updateClearButtonVisibility()

    # region PaintEvent
    def paintEvent(self, e):
        super().paintEvent(e)
        
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        border_default_color = PyLunixStyleSheet.TEXT_BOX.get_value("TextControlBorderBrush")
        border_focus_color = PyLunixStyleSheet.TEXT_BOX.get_value("TextControlBorderBrushFocused")
        border_disabled_color = PyLunixStyleSheet.TEXT_BOX.get_value("TextControlBorderBrushDisabled")

        contents_margins = self.contentsMargins()
        border_width = self.width() - contents_margins.left() - contents_margins.right()
        border_height = self.height()

        if self.hasFocus():
            focus_border_color = QColor(border_default_color)
            focus_border_width = 1.0 
            focus_border_radius = 4.0
            
            painter.setPen(QPen(focus_border_color, focus_border_width))
            painter.setBrush(Qt.BrushStyle.NoBrush) 
            
            rect = self.rect().adjusted(
                int(focus_border_width / 2), 
                int(focus_border_width / 2), 
                -int(focus_border_width / 2), 
                -int(focus_border_width / 2)
            )
            painter.drawRoundedRect(rect, focus_border_radius, focus_border_radius)

        path = QPainterPath()
        path.addRoundedRect(QRectF(contents_margins.left(), border_height - 10, border_width, 10), 5, 5)

        rectPath = QPainterPath()
        rectPath.addRect(contents_margins.left(), border_height - 10, border_width, 8)
        path = path.subtracted(rectPath)

        if not self.isEnabled():
            painter.fillPath(path, QColor(border_disabled_color))
        else:
            painter.fillPath(path, QColor(border_focus_color if self.hasFocus() else border_default_color))

class TextBoxButton(TransparentToolButton):
    def __init__(self, icon, parent=None):
        super().__init__(icon, parent)
        self.isPressed = False
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(23, 23)

    def action(self):
        return self._action

    def setAction(self, action: QAction):
        self._action = action
        self._onActionChanged()
        self.clicked.connect(action.trigger)
        action.toggled.connect(self.setChecked)
        action.changed.connect(self._onActionChanged)

    def _onActionChanged(self):
        action = self.action()
        self.setEnabled(action.isEnabled())
        self.setVisible(action.isVisible())
        self.setCheckable(action.isCheckable())
        self.setChecked(action.isChecked())

    def mousePressEvent(self, e):
        self.isPressed = True
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        self.isPressed = False
        super().mouseReleaseEvent(e)
# endregion

# region TextBoxEdit
class TextBoxEdit(_BaseTextBoxEdit):
    _BUTTON_CLASS = TextBoxButton
    def __init__(self, text: str = "", foreground : Optional[Union[Qt.GlobalColor, QColor, str]] = None, parent=None):
        super().__init__(text, parent)
        self.setProperty("class", "TextBoxEdit")

        self._isClearButtonEnabled = True
        self._clearButtonAlwaysVisible = False
        self._foreground = foreground

        self.isPressed = False
        self.isHover = False

        self.clearButton = TextBoxButton(WinIcon.CLEAR, self)
        self.hBoxLayout.addWidget(self.clearButton, 0, Qt.AlignmentFlag.AlignRight) 
        
        self.clearButton.clicked.connect(self.clear)
        self.textChanged.connect(self._updateClearButtonVisibility)

        self._updateClearButtonVisibility()
        self._adjustTextMargins()

        PyLunixStyleSheet.TEXT_BOX.apply(self)

    def _adjustTextMargins(self):
        left = len(self.leftButtons) * 30
        right = len(self.rightButtons) * 30
        
        if self.isClearButtonEnabled():
            right += 28

        m = self.textMargins()
        self.setTextMargins(left, m.top(), right, m.bottom())

    def isClearButtonEnabled(self) -> bool:
        return self._isClearButtonEnabled

    def _updateClearButtonVisibility(self):
        should_be_visible = (
            (self.hasFocus() and 
             bool(self.text() and not self.isReadOnly()) and 
             self.isClearButtonEnabled()) or self._clearButtonAlwaysVisible
        )
        self.clearButton.setVisible(should_be_visible)
        self._adjustTextMargins()

    def setClearButtonAlwaysVisible(self, always_visible: bool=True):
        self._clearButtonAlwaysVisible = always_visible
        self._updateClearButtonVisibility()

    def setReadOnly(self, read_only: bool):
        super().setReadOnly(read_only)
        self._updateClearButtonVisibility()

    def setTextColor(self, color: Union[Qt.GlobalColor, QColor, str]):
        self._foreground = color
        self._setTextgroundColor()

    def _get_text_color(self) ->str:
        if not self.isEnabled():
            name = "TextBlockForegroundDisabled"
        elif self.isPressed:
            name = "TextBlockForegroundPressed"
        elif self.isHover:
            name = "TextBlockForegroundPointerOver"
        else:
            name = "TextBlockForeground"
        return PyLunixStyleSheet.TEXT_BOX.get_value(name)

    def _setTextgroundColor(self):
        color = self._get_text_color() if self._foreground is None else self._foreground

        palette = self.palette()
        if isinstance(color, Qt.GlobalColor):
            palette.setColor(QPalette.ColorRole.Text, QColor(color))
        elif isinstance(color, QColor):
            palette.setColor(QPalette.ColorRole.Text, color)
        elif isinstance(color, str):
            palette.setColor(QPalette.ColorRole.Text, QColor(color))
        self.setPalette(palette)

    def enterEvent(self, e): self.isHover = True; self._setTextgroundColor(); super().enterEvent(e)
    def leaveEvent(self, e): self.isHover = False; self._setTextgroundColor(); super().leaveEvent(e)
    def mousePressEvent(self, e): self.isPressed = True; self._setTextgroundColor(); super().mousePressEvent(e)
    def mouseReleaseEvent(self, e): self.isPressed = False; self._setTextgroundColor(); super().mouseReleaseEvent(e)
    
    def changeEvent(self, event: QEvent):
        if event.type() == QEvent.Type.StyleChange or event.type() == QEvent.Type.PaletteChange:
            self._setTextgroundColor()
        super().changeEvent(event)
# endregion

class TextBox(QWidget):
    def __init__(self, text: str="", header: Optional[str]=None, parent = None):
        super().__init__(parent)
        self.setProperty("class", "TextBox")

        self.Vlayout = QVBoxLayout(self)
        top_header_margin = extract_numbers(PyLunixStyleSheet.TEXT_BOX.get_value("TextBoxTopHeaderMargin"))
        self.Vlayout.setContentsMargins(
            top_header_margin[0], 
            top_header_margin[1],
            top_header_margin[2],
            top_header_margin[3])
        self.Vlayout.setSpacing(0)

        self.header_label = None
        if header:
            self.setHeader(header)
        
        self.textBoxEdit = TextBoxEdit(text=text, parent=self) 
        self.Vlayout.addWidget(self.textBoxEdit)

    def setHeader(self, text:str):
        if not self.header_label:
            self.header_label = TextBlock(text, parent=self)
            self.header_label.setProperty("class", "TextBlock")
            self.Vlayout.addWidget(self.header_label)
            PyLunixStyleSheet.TEXT_BLOCK.apply(self.header_label)
        else:
            self.header_label.setText(text)

# region TextBoxEdit Proxy Methods
    @property
    def edit(self):
        return self.textBoxEdit

    def text(self) -> str:
        return self.textBoxEdit.text()
    
    def clear(self):
        self.textBoxEdit.clear()
    
    def setText(self, text: str):
        self.textBoxEdit.setText(text)

    def setPlaceholderText(self, text: str):
        self.textBoxEdit.setPlaceholderText(text)

    def setClearButtonAlwaysVisible(self, always_visible: bool=True):
        self._clearButtonAlwaysVisible = always_visible
        self.textBoxEdit._updateClearButtonVisibility()

    def setReadOnly(self, read_only: bool):
        self.textBoxEdit.setReadOnly(read_only)

    def setFocus(self):
        self.textBoxEdit.setFocus()
    
    def setHighlightColor(self, background: QColor, text: Optional[QColor]=None):
        self.textBoxEdit.setHighlightColor(background, text)
        self.textBoxEdit.update()

    def setTextStyle(self,
                     font_style: Optional[TypographyStyle] = None,
                     font_family: Optional[str] = None,
                     font_size: Optional[int] = None,
                     font_weight: Optional[QFont.Weight] = None):
        self.textBoxEdit.setTextStyle(font_style=font_style,
                                     font_family=font_family,
                                     font_size=font_size,
                                     font_weight=font_weight)
        
    def setEchoMode(self, mode: QLineEdit.EchoMode):
        self.textBoxEdit.setEchoMode(mode)

    def setTextColor(self, color: Union[Qt.GlobalColor, QColor, str]):
        self.textBoxEdit.setTextColor(color)
# endregion