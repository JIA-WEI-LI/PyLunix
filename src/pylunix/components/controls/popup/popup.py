from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPoint, QRect

class Popup(QWidget):
    """
    A base primitive for creating top-level transient windows.

    This class handles the core logic for windows that appear above main UI 
    content, such as Flyouts, Tooltips, or Dropdowns. It manages window flags 
    for light-dismiss behavior and provides coordinate calculation logic that 
    is screen-aware.

    Attributes:
        is_light_dismiss_enabled (bool): If True, the window uses Qt.Popup and 
                                        closes automatically on loss of focus.
    """
    def __init__(self, is_light_dismiss_enabled:bool = True, parent=None):
        """
        Initialize the Popup with specific window flags based on dismiss behavior.

        Args:
            is_light_dismiss_enabled (bool): Whether the window should auto-hide 
                                            when clicking outside. Defaults to True.
            parent (QWidget, optional): The parent widget.
        """
        super().__init__(parent)
        self.is_light_dismiss_enabled = is_light_dismiss_enabled

        flags = Qt.WindowType.FramelessWindowHint | Qt.WindowType.NoDropShadowWindowHint
        
        if self.is_light_dismiss_enabled:
            self.setWindowFlags(
                Qt.WindowType.FramelessWindowHint | 
                Qt.WindowType.Popup | 
                Qt.WindowType.NoDropShadowWindowHint
            )
        else:
            self.setWindowFlags(
                Qt.WindowType.FramelessWindowHint | 
                Qt.WindowType.Tool | 
                Qt.WindowType.WindowStaysOnTopHint | 
                Qt.WindowType.NoDropShadowWindowHint
            )

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setProperty("class", "Popup")

    def calculate_position(self, target_widget, placement="Bottom", offset=8):
        """
        Calculates the global screen coordinates relative to a target widget.

        This method ensures the popup is positioned correctly based on the requested 
        alignment and performs screen boundary checks to prevent clipping or 
        off-screen rendering.

        Args:
            target_widget (QWidget): The anchor widget to align against.
            placement (str): Positioning mode ("Top", "Bottom", "Left", "Right").
            offset (int): Pixel distance from the target widget.

        Returns:
            QPoint: The calculated global position for the popup.
        """
        self.adjustSize()
        
        global_pos = target_widget.mapToGlobal(QPoint(0, 0))
        target_rect = QRect(global_pos, target_widget.size())
        
        popup_w, popup_h = self.width(), self.height()
        x, y = 0, 0
        
        if placement == "Bottom":
            x = target_rect.center().x() - (popup_w // 2)
            y = target_rect.bottom() + offset
        elif placement == "Top":
            x = target_rect.center().x() - (popup_w // 2)
            y = target_rect.top() - popup_h - offset
        elif placement == "Left":
            x = target_rect.left() - popup_w - offset
            y = target_rect.center().y() - (popup_h // 2)
        elif placement == "Right":
            x = target_rect.right() + offset
            y = target_rect.center().y() - (popup_h // 2)

        screen = target_widget.screen()
        screen_geo = screen.availableGeometry()
        
        if x < screen_geo.left(): x = screen_geo.left() + 5
        if x + popup_w > screen_geo.right(): x = screen_geo.right() - popup_w - 5
        
        if placement == "Bottom" and y + popup_h > screen_geo.bottom():
            y = target_rect.top() - popup_h - offset
        elif placement == "Top" and y < screen_geo.top():
            y = target_rect.bottom() + offset
            
        return QPoint(x, y)