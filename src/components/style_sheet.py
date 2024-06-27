from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget

from enum import Enum

class StyleSheet(Enum):
    MAIN_INTERFACE = "",
    REC_INTERFACE = "",
    SYNTH_INTERFACE = "",
    SETTING_INTERFACE = "",
    
    def aplly_style(self, widget: QWidget):
        theme = ...
        with open(f"resources/qss/{theme}/{self.value}.qss", "r") as f:
            style = f.read()
            widget.setStyleSheet(style)
