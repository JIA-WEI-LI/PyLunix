from typing import Union, Callable
from PyQt5.QtWidgets import QCheckBox, QWidget, QStyleOptionButton, QStyle
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen
from PyQt5.QtCore import QSize, Qt, QRect

from ...common.stylesheet import PyLunixStyleSheet
from ...icon_manager.win_icons.win_icon import WinIcon

class CheckBox(QCheckBox):
    def __init__(self, text: str = "", icon: QIcon = None, parent: QWidget = None):
        super().__init__(text, parent)
        self.isPressed = False
        self.isHover = False
        self._icon_source = None

        self.setProperty("class", "CheckBox")
        self.setIconSize(QSize(16, 16))

        if text: self.setText(text)
        if icon: self.setIcon(icon)
        else: self.setIcon(QIcon())

        PyLunixStyleSheet.CHECK_BOX.apply(self)

    def setIcon(self, icon: Union[QIcon, Callable]):
        if callable(icon):
            self.setIconSource(icon)
        else:
            super().setIcon(icon)
            self._icon_source = None
            self._icon = icon

    def setIconSource(self, icon_accessor):
        self._icon_source = icon_accessor
        self.updateIcon()

    def _get_icon_color(self) -> str:
        if not self.isEnabled():
            name = "CheckBoxForegroundCheckedDisabled" if self.isChecked() else "CheckBoxForegroundUncheckedDisabled"
        elif self.isPressed:
            name = "CheckBoxForegroundCheckedPressed" if self.isChecked() else "CheckBoxForegroundUncheckedPressed"
        elif self.isHover:
            name = "CheckBoxForegroundCheckedPointerOver" if self.isChecked() else "CheckBoxForegroundUncheckedPointerOver"
        else:
            name = "CheckBoxForegroundChecked" if self.isChecked() else "CheckBoxForegroundUnchecked"
        return PyLunixStyleSheet.CHECK_BOX.get_value(name)
    
    def _get_indicator_icon_color(self) -> str:
        if not self.isEnabled():
            name = "CheckBoxCheckGlyphForegroundCheckedDisabled" if self.isChecked() else "CheckBoxCheckGlyphForegroundUncheckedDisabled"
        elif self.isPressed:
            name = "CheckBoxCheckGlyphForegroundCheckedPressed" if self.isChecked() else "CheckBoxCheckGlyphForegroundUncheckedPressed"
        elif self.isHover:
            name = "CheckBoxCheckGlyphForegroundCheckedPointerOver" if self.isChecked() else "CheckBoxCheckGlyphForegroundUncheckedPointerOver"
        else:
            name = "CheckBoxCheckGlyphForegroundChecked" if self.isChecked() else "CheckBoxCheckGlyphForegroundUnchecked"
        return PyLunixStyleSheet.CHECK_BOX.get_value(name)

    def updateIcon(self):
        if hasattr(self, "_icon_source") and callable(self._icon_source):
            try:
                color = self._get_icon_color()
                icon = self._icon_source(color)
                if icon:
                    super().setIcon(icon)
                    self._icon = icon
                    self.update()
            except Exception as e:
                print(f"[CheckBox] Failed to update icon: {e}")

    def enterEvent(self, event):
        self.isHover = True
        super().enterEvent(event)
        self.update()

    def leaveEvent(self, event):
        self.isHover = False
        super().leaveEvent(event)
        self.update()

    def mousePressEvent(self, event):
        self.isPressed = True
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.isPressed = False
        super().mouseReleaseEvent(event)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)

        opt = QStyleOptionButton()
        self.initStyleOption(opt)
        rect = self.style().subElementRect(QStyle.SubElement.SE_CheckBoxIndicator, opt, self)
        
        def _background_color() -> str:
            if not self.isEnabled():
                name = "CheckBoxCheckBackgroundFillCheckedDisabled" if self.isChecked() else "CheckBoxCheckBackgroundFillUncheckedDisabled"
            elif self.isPressed:
                name = "CheckBoxCheckBackgroundFillCheckedPressed" if self.isChecked() else "CheckBoxCheckBackgroundFillUncheckedPressed"
            elif self.isHover:
                name = "CheckBoxCheckBackgroundFillCheckedPointerOver" if self.isChecked() else "CheckBoxCheckBackgroundFillUncheckedPointerOver"
            else:
                name = "CheckBoxCheckBackgroundFillChecked" if self.isChecked() else "CheckBoxCheckBackgroundFillUnchecked"
            return PyLunixStyleSheet.CHECK_BOX.get_value(name)

        def _border_color() -> str:
            if not self.isEnabled():
                name = "CheckBoxCheckBackgroundStrokeCheckedDisabled" if self.isChecked() else "CheckBoxCheckBackgroundStrokeUncheckedDisabled"
            elif self.isPressed:
                name = "CheckBoxCheckBackgroundStrokeCheckedPressed" if self.isChecked() else "CheckBoxCheckBackgroundStrokeUncheckedPressed"
            elif self.isHover:
                name = "CheckBoxCheckBackgroundStrokeCheckedPointerOver" if self.isChecked() else "CheckBoxCheckBackgroundStrokeUncheckedPointerOver"
            else:
                name = "CheckBoxCheckBackgroundStrokeChecked" if self.isChecked() else "CheckBoxCheckBackgroundStrokeUnchecked"
            return PyLunixStyleSheet.CHECK_BOX.get_value(name)


        painter.setBrush(QColor(_background_color()))
        painter.setPen(QPen(QColor(_border_color()), 1))
        painter.drawRoundedRect(rect.adjusted(0, 0, -1, -1), 5, 5)

        GLYPH_SIZE = 14
        
        color = self._get_indicator_icon_color()
        indicator_icon = None

        target_glyph_accessor = None
        
        if self.checkState() == Qt.CheckState.Checked:
            target_glyph_accessor = WinIcon.CHECKMARK 
        elif self.checkState() == Qt.CheckState.PartiallyChecked:
            if hasattr(WinIcon, 'INDETERMINATE'):
                target_glyph_accessor = WinIcon.INDETERMINATE
            else:
                target_glyph_accessor = WinIcon.CHECKMARK 

        if target_glyph_accessor and callable(target_glyph_accessor):
            try:
                indicator_icon = target_glyph_accessor(color)
            except Exception as e:
                print(f"[CheckBox] Failed to get themed indicator icon: {e}")

        if isinstance(indicator_icon, QIcon):
            pixmap = indicator_icon.pixmap(QSize(GLYPH_SIZE, GLYPH_SIZE), QIcon.Mode.Normal if self.isEnabled() else QIcon.Mode.Disabled)
            icon_rect = QRect(
                rect.x() + (rect.width() - pixmap.width()) // 2,
                rect.y() + (rect.height() - pixmap.height()) // 2,
                pixmap.width(),
                pixmap.height()
            )
            painter.drawPixmap(icon_rect, pixmap)

        content_rect = self.style().subElementRect(QStyle.SubElement.SE_CheckBoxContents, opt, self)
        opt.rect = content_rect
        self.style().drawControl(QStyle.ControlElement.CE_CheckBoxLabel, opt, painter, self)
        painter.end()