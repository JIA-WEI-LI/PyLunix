from typing import Optional
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer

from ..button.button import BaseButton
from ....common.stylesheet import PyLunixStyleSheet

class RepeatButton(BaseButton):
    """
    A button that continues to trigger the click event while being pressed.

    This component mimics the behavior of keyboard keys or spin box arrows, 
    where holding the button down triggers an initial action, waits for a 
    short delay, and then repeatedly triggers the action at a fixed interval.

    Attributes:
        _repeat_delay (int): The initial delay in milliseconds before repeating starts.
        _repeat_interval (int): The interval in milliseconds between consecutive clicks.
        _repeat_timer (QTimer): Internal timer managing the repetition logic.
    """

    def __init__(self, text: str = "", icon: QIcon = None, parent: QWidget = None, *args, **kwargs):
        """
        Initialize the RepeatButton.

        Args:
            text (str): The text displayed on the button.
            icon (QIcon, optional): The icon displayed on the button.
            parent (QWidget, optional): The parent widget.
            repeat_delay (int, optional): Initial wait time (ms). Defaults to 400.
            repeat_interval (int, optional): Repetition speed (ms). Defaults to 100.
        """
        super().__init__(text=text, icon=icon, parent=parent)

        # Disable native auto-repeat to use our custom QTimer logic for better control
        self.setAutoRepeat(False)
        self._repeat_delay = kwargs.pop("repeat_delay", 400)
        self._repeat_interval = kwargs.pop("repeat_interval", 100)

        # Setup the repeat mechanism
        self._repeat_timer = QTimer(self)
        self._repeat_timer.timeout.connect(self._on_repeat_timeout)

        # Connect internal press/release signals to manage the timer
        self.pressed.connect(self._start_repeat)
        self.released.connect(self._stop_repeat)
        
        self.setProperty("class", "RepeatButton")
        PyLunixStyleSheet.REPEAT_BUTTON.apply(self)

    def _start_repeat(self):
        """Starts the repeat timer with the initial delay when the button is pressed."""
        self._repeat_timer.start(self._repeat_delay)

    def _stop_repeat(self):
        """Stops the repeat timer immediately when the button is released."""
        self._repeat_timer.stop()

    def _on_repeat_timeout(self):
        """
        Handles the timer timeout event.
        
        Triggers a click and switches the timer from the 'initial delay' 
        to the 'continuous interval' mode.
        """
        self.click()
        self._repeat_timer.setInterval(self._repeat_interval)

    def setRepeatDelay(self, delay_ms: int):
        """
        Set the delay before the first repetition occurs.

        Args:
            delay_ms (int): Delay in milliseconds.
        """
        self._repeat_delay = delay_ms

    def setRepeatInterval(self, interval_ms: int):
        """
        Set the interval between repeated click events.

        Args:
            interval_ms (int): Interval in milliseconds.
        """
        self._repeat_interval = interval_ms

    def repeatDelay(self) -> int:
        """Return the current repeat delay in milliseconds."""
        return self._repeat_delay

    def repeatInterval(self) -> int:
        """Return the current repeat interval in milliseconds."""
        return self._repeat_interval