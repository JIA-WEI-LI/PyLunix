from PyQt5.QtWidgets import QVBoxLayout, QGraphicsDropShadowEffect, QFrame
from PyQt5.QtCore import QPropertyAnimation, QRect, QEasingCurve
from PyQt5.QtGui import QColor

from ..popup.popup import Popup
from pylunix.common.stylesheet import PyLunixStyleSheet

class Flyout(Popup):
    """
    A lightweight, animated popup container for displaying contextual information.

    The Flyout inherits from the Popup base class and provides a transient surface 
    for hosting arbitrary content. It features WinUI-inspired visuals including:
    - Drop shadow effects
    - Smooth slide-in animations using Quintic easing
    - Configurable Light Dismiss behavior
    - Smart edge-detection and auto-flip positioning

    Attributes:
        container (QFrame): The styled inner frame that holds the content and shadow.
        content_layout (QVBoxLayout): The internal layout where hosted widgets reside.
        animation (QPropertyAnimation): Handles the smooth entry geometry effect.
    """
    def __init__(self, parent=None):
        """
        Initialize the Flyout with a translucent background and shadow effects.

        Args:
            parent (QWidget, optional): The parent widget.
        """
        super().__init__(is_light_dismiss_enabled=True, parent=parent)
        self.setProperty("class", "Flyout")

        self.container = QFrame(self)
        self.container.setObjectName("FlyoutContainer")
        
        self.content_layout = QVBoxLayout(self.container)
        self.content_layout.setContentsMargins(16, 15, 16, 17)
        self.content_layout.setSpacing(8)

        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(250)
        self.animation.setEasingCurve(QEasingCurve.OutQuint)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 4)
        self.container.setGraphicsEffect(shadow)

        PyLunixStyleSheet.FLYOUT.apply(self)

    def set_content_layout(self, layout: QVBoxLayout):
        """
        Populates the Flyout with content from a provided layout.

        This method clears any existing widgets in the Flyout before transferring 
        ownership of widgets from the source layout to the Flyout's internal layout.

        Args:
            layout (QVBoxLayout): The source layout containing widgets to be hosted.
        """
        self._clear_layout(self.content_layout)

        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                self.content_layout.addWidget(item.widget())
            elif item.layout():
                self.content_layout.addLayout(item.layout())
            elif item.spacerItem():
                self.content_layout.addItem(item.spacerItem())

        self.container.adjustSize()
        self.adjustSize()

    def _clear_layout(self, layout):
        """
        Recursively deletes all widgets and nested layouts within a layout.

        Internal helper used to ensure clean memory management when updating content.
        """
        if layout is None:
            return
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())

    def show_at(self, target_widget, placement:str="Top", offset:int=8):
        """
        Positions and displays the Flyout relative to a target widget with animation.

        The method calculates global coordinates via the base Popup class, ensures 
        the Flyout does not go off-screen, and triggers a slide-in animation.

        Args:
            target_widget (QWidget): The anchor widget to position the Flyout against.
            placement (str): The desired side relative to target ("Top", "Bottom", "Left", "Right"). 
            offset (int): The distance (pixels) between the Flyout and the target widget.
        """
        pos = self.calculate_position(target_widget, placement, offset)
        
        end_rect = QRect(pos.x(), pos.y(), self.width(), self.height())
        
        dx, dy = 0, 0
        if "Bottom" in placement: dy = -10
        elif "Top" in placement: dy = 10
        elif "Left" in placement: dx = 10
        elif "Right" in placement: dx = -10

        start_rect = QRect(pos.x() + dx, pos.y() + dy, self.width(), self.height())

        self.setGeometry(end_rect)
        self.animation.setStartValue(start_rect)
        self.animation.setEndValue(end_rect)
        
        self.show()
        self.animation.start()