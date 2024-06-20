# Speech Recognition
from os import remove
from pathlib import Path
from threading import Thread
from functools import partial

from PySide6.QtCore import Qt, QUrl, QPropertyAnimation, QRect, Signal, Slot
from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QGridLayout, QHBoxLayout
# from PySide6.QtGui import QPalette, QColor

from qfluentwidgets import BodyLabel, PushButton, ScrollArea, ComboBox, StrongBodyLabel, CheckBox, PlainTextEdit
from qfluentwidgets.multimedia import StandardMediaPlayBar

class TextToolBar(QFrame):
    def __init__(self, text, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("TextToolBar")
        self.text = text
        
        self.hblayout = QHBoxLayout(self)
        self.btn_copy = PushButton("复制")
        self.btn_clear = PushButton("清空")
        self.btn_translate = PushButton("翻译为")
        self.combox_translate = ComboBox()
        self.combox_translate.addItems(["中文", "英文", "日文"])
        
        self.hblayout.addWidget(self.btn_copy, 1, Qt.AlignmentFlag.AlignLeft)
        self.hblayout.addWidget(self.btn_translate, 1, Qt.AlignmentFlag.AlignRight)
        self.hblayout.addWidget(self.combox_translate, 1, Qt.AlignmentFlag.AlignRight)
        self.hblayout.addWidget(self.btn_clear, 1, Qt.AlignmentFlag.AlignRight)
    def connect_btns(self):
        self.btn_copy.clicked.connect(self.copy_text)
        self.btn_clear.clicked.connect(self.clear_text)
        self.btn_translate.clicked.connect(self.translate_text)
    def copy_text(self):
        pass
    def clear_text(self):
        pass
    def translate_text(self):
        pass

class SpeechRecInterface(QWidget):
    # ret_text_s = Signal(str)
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._init_ui()
        
        self.vblayout = QVBoxLayout(self)
        self.strongLabel = StrongBodyLabel("语音识别")
        self.label = BodyLabel("speech recognition")
        
        
    def _init_ui(self):
        self.setObjectName("SpeechRecInterface")
    
    def _init_btns(self):
        self.btn_start = PushButton("开始实时识别")
        self.btn_stop = PushButton("停止实时识别")
        self.btn_loadfile = PushButton("读取音频文件")
        self.btn_rec_record = PushButton("开始识别录音")
        self.btn_play_record = PushButton("播放录音")
        
        self.model_select = ComboBox("模型选择")
        self.voice_select = ComboBox("音色选择")
        self.lang_select = ComboBox("主要语言选择")
        
        self.save_record = CheckBox("保存录音")
        self.translate_to_mainlang = CheckBox("始终翻译成主要语言")
        
        self._selects()
        self.connect_btns()
        self.connect_check_boxes()
    def btns_layout(self):
        btns_layout = QGridLayout()

        
    def _selects(self):
        self.model_select.addItems(["模型1", "模型2", "模型3"])
        self.voice_select.addItems(["音色1", "音色2", "音色3"]) # 音色选择会根据模型自动更新
        self.lang_select.addItems(["主要语言1", "主要语言2", "主要语言3"])
    
    def connect_btns(self):
        self.btn_start.clicked.connect(self.start_rec_stream)
        self.btn_stop.clicked.connect(self.stop_rec_stream)
        self.btn_loadfile.clicked.connect(self.load_file)
        self.btn_rec_record.clicked.connect(self.start_rec_record)
        self.btn_play_record.clicked.connect(self.play_record)
        
    def connect_check_boxes(self):
        self.save_record.stateChanged.connect(self.save_record_changed)
        self.translate_to_mainlang.stateChanged.connect(self.translate_to_mainlang_changed)
        
        
    def start_rec_stream(self):
        pass
    def stop_rec_stream(self):
        pass
    
    def load_file(self):
        pass
    def start_rec_record(self):
        pass
    def play_record(self):
        pass
    
    def save_record_changed(self, state):
        pass
    def translate_to_mainlang_changed(self, state):
        pass

    
    