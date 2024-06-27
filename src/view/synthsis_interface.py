from PySide6.QtCore import Qt, QUrl, QPropertyAnimation, QRect, Signal, Slot
from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QGridLayout, QHBoxLayout
# from PySide6.QtGui import QPalette, QColor

from qfluentwidgets import BodyLabel, PushButton, ScrollArea, ComboBox, StrongBodyLabel, CheckBox, PlainTextEdit
from qfluentwidgets.multimedia import StandardMediaPlayBar

class TextToolBar(QWidget):
    def __init__(self, text_edit: PlainTextEdit, parent=None):
        super().__init__(parent)
        self.text_edit = text_edit
        self.hbox_layout = QHBoxLayout(self)
        
class TextInput(PlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText(self.tr("请输入文本"))

class SynthsisInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.vbox_layout = QVBoxLayout(self)
        self.strongLabel = StrongBodyLabel("语音合成", self)
        self.label = BodyLabel("speech synthesis", self)
        
        
        
    def _init_widget(self):
        ...
    
    
    