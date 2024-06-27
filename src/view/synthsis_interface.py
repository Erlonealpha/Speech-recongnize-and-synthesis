from PySide6.QtCore import Qt, QUrl, QPropertyAnimation, QRect, Signal, Slot
from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QGridLayout, QHBoxLayout
# from PySide6.QtGui import QPalette, QColor

from qfluentwidgets import BodyLabel, PushButton, ScrollArea, ComboBox, StrongBodyLabel, CheckBox, PlainTextEdit
from qfluentwidgets.multimedia import StandardMediaPlayBar



class SynthsisInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
    def _init_widget(self):
        ...
    
    
    
    