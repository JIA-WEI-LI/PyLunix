from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer

from ..button.button import BaseButton
from ....common.stylesheet import PyLunixStyleSheet

class RepeatButton(BaseButton):
    def __init__(self, text: str = "", icon: QIcon = None, parent: QWidget = None, *args, **kwargs):
        super().__init__(text=text, icon=icon, parent=parent)

        self.setAutoRepeat(False)
        self._repeat_delay = kwargs.pop("repeat_delay", 400)
        self._repeat_interval = kwargs.pop("repeat_interval", 100)

        self._repeat_timer = QTimer(self)
        self._repeat_timer.timeout.connect(self._on_repeat_timeout)

        self.pressed.connect(self._start_repeat)
        self.released.connect(self._stop_repeat)
        self.setProperty("class", "RepeatButton")

        PyLunixStyleSheet.REPEAT_BUTTON.apply(self)

    def _start_repeat(self):
        self._repeat_timer.start(self._repeat_delay)

    def _stop_repeat(self):
        self._repeat_timer.stop()

    def _on_repeat_timeout(self):
        self.click()
        self._repeat_timer.setInterval(self._repeat_interval)

    def setRepeatDelay(self, delay_ms: int):
        self._repeat_delay = delay_ms

    def setRepeatInterval(self, interval_ms: int):
        self._repeat_interval = interval_ms

    def repeatDelay(self) -> int:
        return self._repeat_delay

    def repeatInterval(self) -> int:
        return self._repeat_interval