from typing import Union, Optional
from PyQt5.QtWidgets import QAction, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
    
from ..text_box.text_box import TextBox, TextBoxEdit
from ..text_block.text_block import TextBlock
from ..tool_button.tool_button import TransparentToolButton
from ....common.stylesheet import PyLunixStyleSheet
from ....common.typography import TypographyStyle
from ....icons.win_icon_kit.win_icon import WinIcon
from ....utils.style_parser import extract_numbers
from ....utils.math_utils import safe_eval_math, IncrementNumberRounder, DecimalFormatter

class NumberBoxButton(TransparentToolButton):
    def __init__(self, icon: WinIcon, parent=None):
        super().__init__(icon, parent)
        self.isPressed = False
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(23, 23)

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

    def action(self):
        return self._action
    
    def mousePressEvent(self, e):
        self.isPressed = True
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        self.isPressed = False
        super().mouseReleaseEvent(e)

class NumberBoxEdit(TextBoxEdit):
    _BUTTON_CLASS = NumberBoxButton
    def __init__(self, text: str = "", 
                 foreground : Optional[Union[Qt.GlobalColor, QColor, str]] = None, 
                 accepts_expression: bool = False,
                 parent=None):
        super().__init__(text, foreground, parent)
        # self.setProperty("class", "NumberBox")

        rounder = IncrementNumberRounder(increment=0.25)
        self.NumberFormatter = DecimalFormatter(fraction_digits=2, number_rounder=rounder)
        if accepts_expression: 
            self.returnPressed.connect(self._simple_calculation)

    def _simple_calculation(self):
        input_str = self.text().strip()
        if not input_str:
            return

        try:
            expression = input_str.replace('^', '**')
            result = safe_eval_math(expression)
            formatted_result = f"{result:.8f}".rstrip('0').rstrip('.')
            self.setText(formatted_result)
        except (ValueError, TypeError) as e:
            self.setText(input_str)
        except Exception:
            self.setText(input_str)

# region NumberBox
class NumberBox(QWidget):
    def __init__(self, text: str="", header: Optional[str]=None, parent = None):
        super().__init__(parent)
        self.setProperty("class", "NumberBox")

        self.Vlayout = QVBoxLayout(self)
        top_header_margin = extract_numbers(PyLunixStyleSheet.NUMBER_BOX.get_value("NumberBoxTopHeaderMargin"))
        self.Vlayout.setContentsMargins(
            top_header_margin[0], 
            top_header_margin[1],
            top_header_margin[2],
            top_header_margin[3])
        self.Vlayout.setSpacing(0)

        self.header_label = None
        if header:
            self.setHeader(header)
        
        self.numberBoxEdit = NumberBoxEdit(text=text, parent=self) 
        self.Vlayout.addWidget(self.numberBoxEdit)

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
        return self.numberBoxEdit

    def text(self) -> str:
        return self.numberBoxEdit.text()
    
    def clear(self):
        self.numberBoxEdit.clear()
    
    def setText(self, text: str):
        self.numberBoxEdit.setText(text)

    def setPlaceholderText(self, text: str):
        self.numberBoxEdit.setPlaceholderText(text)

    def setClearButtonAlwaysVisible(self, always_visible: bool=True):
        self._clearButtonAlwaysVisible = always_visible
        self.numberBoxEdit._updateClearButtonVisibility()

    def setReadOnly(self, read_only: bool):
        self.numberBoxEdit.setReadOnly(read_only)

    def setFocus(self):
        self.numberBoxEdit.setFocus()
    
    def setHighlightColor(self, background: QColor, text: Optional[QColor]=None):
        self.numberBoxEdit.setHighlightColor(background, text)
        self.numberBoxEdit.update()

    def setTextStyle(self,
                     font_style: Optional[TypographyStyle] = None,
                     font_family: Optional[str] = None,
                     font_size: Optional[int] = None,
                     font_weight: Optional[QFont.Weight] = None):
        self.numberBoxEdit.setTextStyle(font_style=font_style,
                                     font_family=font_family,
                                     font_size=font_size,
                                     font_weight=font_weight)

    def setTextColor(self, color: Union[Qt.GlobalColor, QColor, str]):
        self.numberBoxEdit.setTextColor(color)
# endregion