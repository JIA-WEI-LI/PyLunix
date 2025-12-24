from typing import Union, Optional, Dict
from PyQt5.QtWidgets import QAction, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QFont
    
from ..text_box.text_box import TextBoxEdit
from ..text_block.text_block import TextBlock
from ..tool_button.tool_button import TransparentToolButton
from ....common.stylesheet import PyLunixStyleSheet
from ....common.typography import TypographyStyle
from ....icons.win_icon_kit.win_icon import WinIcon
from ....utils.style_parser import extract_numbers
from ....utils.math_utils import safe_eval_math

# region NumberBoxButton
class NumberBoxButton(TransparentToolButton):
    """
    Small functional button used within the NumberBox context.

    This button is typically used for incremental changes or specific actions 
    within a numeric input field. It supports QAction binding and cursor changes.
    """

    def __init__(self, icon: WinIcon, parent: Optional[QWidget] = None):
        """
        Initialize the NumberBoxButton.

        Args:
            icon (WinIcon): The icon to display on the button.
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(icon, parent)
        self.isPressed = False
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(23, 23)

    def setAction(self, action: QAction):
        """
        Bind a QAction to the button.

        Synchronizes the button's state (enabled, visible, checked) with the action.

        Args:
            action (QAction): The action to be triggered when clicked.
        """
        self._action = action
        self._onActionChanged()
        self.clicked.connect(action.trigger)
        action.toggled.connect(self.setChecked)
        action.changed.connect(self._onActionChanged)

    def _onActionChanged(self):
        """Update the button's properties based on the associated QAction."""
        action = self.action()
        self.setEnabled(action.isEnabled())
        self.setVisible(action.isVisible())
        self.setCheckable(action.isCheckable())
        self.setChecked(action.isChecked())

    def action(self) -> QAction:
        """Retrieve the currently bound QAction."""
        return self._action
    
    def mousePressEvent(self, e):
        self.isPressed = True
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        self.isPressed = False
        super().mouseReleaseEvent(e)
# endregion

# region NumberBoxEdit
class NumberBoxEdit(TextBoxEdit):
    """
    An enhanced numeric input field with optional math expression evaluation.

    This class extends TextBoxEdit to handle numeric values specifically. If 
    enabled, it can parse and calculate strings like '10 + 5' into their 
    numeric results on enter.

    Signals:
        valueChanged (object): Emitted when the internal numeric value changes.
    """

    _BUTTON_CLASS = NumberBoxButton
    valueChanged = pyqtSignal(object)

    def __init__(self, text: str = "", 
                 foreground: Optional[Union[Qt.GlobalColor, QColor, str]] = None, 
                 accepts_expression: bool = False,
                 parent: Optional[QWidget] = None):
        """
        Initialize the NumberBoxEdit.

        Args:
            text (str): Initial numeric text.
            foreground (Union[Qt.GlobalColor, QColor, str], optional): Text color.
            accepts_expression (bool): Whether to evaluate math formulas on return.
            parent (QWidget, optional): Parent widget.
        """
        super().__init__(text, foreground, parent)
        self._internal_value: Optional[float] = None
        self._accepts_expression = accepts_expression
        self._update_internal_value_from_text(text)

        self.textChanged.connect(self._on_text_changed)
        self.returnPressed.connect(self._returnPressed_handler)

    @property
    def value(self) -> Optional[float]:
        """
        The current numeric value of the input field.
        
        Returns:
            Optional[float]: The float value if valid, else None.
        """
        self._update_internal_value_from_text(self.text())
        return self._internal_value

    def _update_internal_value_from_text(self, text: str):
        """Internal logic to parse text into a float and emit valueChanged."""
        try:
            new_value = float(text)
        except ValueError:
            new_value = None
        
        if new_value is not None and new_value != self._internal_value:
            self._internal_value = new_value 
            self.valueChanged.emit(self._internal_value)

    def _on_text_changed(self, new_text: str):
        """Trigger value update whenever text is modified."""
        self._update_internal_value_from_text(new_text)

    def _simple_calculation(self):
        """
        Parses and evaluates the current text as a mathematical expression.
        
        Uses 'safe_eval_math' to perform calculations. Replaces '^' with '**' 
        for Python compatibility.
        """
        input_str = self.text().strip()
        if not input_str:
            return

        try:
            expression = input_str.replace('^', '**')
            result = safe_eval_math(expression)
            self._internal_value = result
            formatted_result = f"{result:.8f}".rstrip('0').rstrip('.')
            self.setText(formatted_result)
        except (ValueError, TypeError):
            self.setText(str(self._internal_value))
        except Exception:
            self.setText(str(self._internal_value))

    def setAcceptsExpression(self, accepts_expression: bool = False):
        """Enable or disable math expression evaluation."""
        self._accepts_expression = accepts_expression
        self.returnPressed.connect(self._returnPressed_handler)

    def _returnPressed_handler(self):
        if self._accepts_expression:
            self._simple_calculation()
        current_text = self.text().strip()
        try:
            new_value = float(current_text)
            self._update_internal_value_from_text(new_value)
        except ValueError:
            if self._internal_value is not None:
                self.setText(str(self._internal_value))
            else:
                self.clear()
# endregion

# region NumberBox
class NumberBox(QWidget):
    """
    A composite widget combining a label (header) and a numeric input field.

    This is the primary container for themed numeric inputs in PyLunix. It 
    manages the layout between an optional header text and the NumberBoxEdit.

    Signals:
        valueChanged (object): Emitted when the input value changes.
    """
    valueChanged = pyqtSignal(object)

    def __init__(self, 
                 text: str = "", 
                 header: Optional[str] = None, 
                 accepts_expression: bool = False, 
                 parent: Optional[QWidget] = None):
        """
        Initialize the NumberBox.

        Args:
            text (str): Default text for the edit field.
            header (str, optional): Title text displayed above the edit field.
            accepts_expression (bool): Allow math evaluation in the edit field.
            parent (QWidget, optional): Parent widget.
        """
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
        
        self.numberBoxEdit = NumberBoxEdit(text=text, accepts_expression=accepts_expression, parent=self) 
        self.Vlayout.addWidget(self.numberBoxEdit)
        self.numberBoxEdit.valueChanged.connect(self.valueChanged.emit)

    def setHeader(self, text: str):
        """
        Set or update the header label text above the input.

        Args:
            text (str): The header text.
        """
        if not self.header_label:
            self.header_label = TextBlock(text, parent=self)
            self.header_label.setProperty("class", "TextBlock")
            self.Vlayout.addWidget(self.header_label)
            PyLunixStyleSheet.TEXT_BLOCK.apply(self.header_label)
        else:
            self.header_label.setText(text)

    @property
    def edit(self) -> NumberBoxEdit:
        """Access to the internal NumberBoxEdit instance."""
        return self.numberBoxEdit
    
    @property
    def value(self) -> Optional[float]:
        """Retrieve the current float value from the edit field."""
        self.edit._update_internal_value_from_text(self.text())
        return self.edit._internal_value

    def text(self) -> str:
        """Retrieve the raw text from the input field."""
        return self.numberBoxEdit.text()
    
    def clear(self):
        """Clear all text in the input field."""
        self.numberBoxEdit.clear()
    
    def setText(self, text: str):
        """Set the text of the input field."""
        self.numberBoxEdit.setText(text)

    def setPlaceholderText(self, text: str):
        """Set the placeholder text of the input field."""
        self.numberBoxEdit.setPlaceholderText(text)

    def setReadOnly(self, read_only: bool):
        """Enable or disable read-only mode."""
        self.numberBoxEdit.setReadOnly(read_only)

    def setFocus(self):
        """Set focus to the input field."""
        self.numberBoxEdit.setFocus()
    
    def setHighlightColor(self, background: QColor, text: Optional[QColor] = None):
        """Set the selection/highlight color for the input field."""
        self.numberBoxEdit.setHighlightColor(background, text)
        self.numberBoxEdit.update()

    def setTextStyle(self,
                     font_style: Optional[TypographyStyle] = None,
                     font_family: Optional[str] = None,
                     font_size: Optional[int] = None,
                     font_weight: Optional[QFont.Weight] = None):
        """Apply typography and font styles to the input field."""
        self.numberBoxEdit.setTextStyle(font_style=font_style,
                                     font_family=font_family,
                                     font_size=font_size,
                                     font_weight=font_weight)

    def setTextColor(self, color: Union[Qt.GlobalColor, QColor, str]):
        """Set the foreground text color."""
        self.numberBoxEdit.setTextColor(color)

    def setAcceptsExpression(self, accepts_expression: bool = False):
        """Configure whether the input field evaluates mathematical expressions."""
        self.numberBoxEdit.setAcceptsExpression(accepts_expression)
# endregion