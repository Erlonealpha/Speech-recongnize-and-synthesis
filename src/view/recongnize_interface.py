# Speech Recognition
from os import remove
from pathlib import Path
from threading import Thread
from functools import partial

from PySide6.QtCore import Qt, QUrl, QPropertyAnimation, QRect, Signal, Slot
from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QGridLayout, QHBoxLayout, QSpacerItem, \
                            QSizePolicy, QLabel, QStackedWidget
# from PySide6.QtGui import QPalette, QColor

from qfluentwidgets import BodyLabel, PushButton, ScrollArea, ComboBox, StrongBodyLabel, CheckBox, \
                            TabBar, SpinBox, TabCloseButtonDisplayMode, TransparentToolButton, FluentIcon
from qfluentwidgets.multimedia import StandardMediaPlayBar

from pyperclip import copy as perclip_copy

from .overlay_interface import SubWidget

class StatusBar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("StatusBar")
        self.resize(800, 50)
        self.setFixedHeight(50)

        self.state = QLabel(self)
        self.now_record = QLabel(self)
        self.init_status()
    def init_status(self):
        self.state.setText("")
        self.now_record.setText(f"{self.tr('当前未选择录音文件')}")
    def initLayout(self):
        self.hb_layout = QHBoxLayout(self)
    
    def set_now_record(self, name):
        self.now_record.setText(f"{self.tr('当前选择录音文件')}: {name}")
    
    def start_record_animation(self):
        self.state.setText(self.tr("正在录音..."))
    def status_resumed(self):
        self.state.setText("")
        
        

class TextDisplay(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.view = QWidget()
        self.setWidgetResizable(True)
        self.setObjectName("TextDisplay")

        self.vboxLayout = QVBoxLayout()
        self.text_display = BodyLabel(self)
        self.text_display.setText(self.tr("Recognition Result"))
        self.text_display.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vboxLayout.addWidget(self.text_display)
        
        self.view.setLayout(self.vboxLayout)
        self.setWidget(self.view)
    def text(self):
        return self.text_display.text()
    def set_text(self, text):
        self.text_display.setText(text)
    
class TextToolBar(QFrame):
    def __init__(self, text_widget: TextDisplay, parent:QWidget=None):
        super().__init__(parent=parent)
        self.setObjectName("TextToolBar")
        self.resize(800, 50)
        self.setFixedHeight(50)
        self.text = text_widget
        
        self.hb_layout = QHBoxLayout(self)
        self.btn_copy = PushButton("复制")
        self.btn_clear = PushButton("清空")
        self.btn_translate = PushButton("翻译为")
        self.combox_translate = ComboBox()
        self.combox_translate.addItems(["中文", "英文", "日文"])
        
        self.hb_layout.addWidget(self.btn_copy, 1, Qt.AlignmentFlag.AlignLeft)
        
        w = parent.width() if parent is not None else 800
        spacer = QSpacerItem(w, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        spacer_2 = QSpacerItem(w/2, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.hb_layout.addItem(spacer)
        self.hb_layout.addWidget(self.btn_translate, 2, Qt.AlignmentFlag.AlignRight)
        self.hb_layout.addWidget(self.combox_translate, 2, Qt.AlignmentFlag.AlignRight)
        self.hb_layout.addItem(spacer_2)
        self.hb_layout.addWidget(self.btn_clear, 1, Qt.AlignmentFlag.AlignRight)
        
        self.connect_btns()
    def connect_btns(self):
        self.btn_copy.clicked.connect(self.copy_text)
        self.btn_clear.clicked.connect(self.clear_text)
        self.btn_translate.clicked.connect(self.translate_text)
    def copy_text(self):
        print('copy_text')
        perclip_copy(self.text.text())
        
    def clear_text(self):
        print('clear_text')
        self.text.set_text("")
    def translate_text(self):
        print('translate_text')

class ButtonInterface(QWidget):
    """ Tab interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # self.tabCount = 1

        # self.tabBar = TabBar(self)
        # self.stackedWidget = QStackedWidget(self)
        self.tabView = QWidget(self)
        self.controlPanel = QFrame(self)

        self.btn_start = PushButton(self.tr("开始实时识别"), self)
        self.btn_stop = PushButton(self.tr("停止实时识别"), self)
        self.btn_loadfile = PushButton(self.tr("读取音频文件"), self)
        self.btn_rec_record = PushButton(self.tr("开始识别录音"), self)
        self.btn_play_record = PushButton(self.tr("播放录音"), self)
        
        self.model_selectLabel = BodyLabel(self.tr("模型选择"), self)
        self.model_select = ComboBox(self)
        self.lang_selectLabel = BodyLabel(self.tr("主要语言选择"), self)
        self.lang_select = ComboBox(self)
        
        self.save_record = CheckBox(self.tr("保存录音"), self)
        self.translate_to_mainlang = CheckBox(self.tr("始终翻译成主要语言"), self)
        
        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout(self.tabView)
        self.panelLayout = QVBoxLayout(self.controlPanel)

        self.__initWidget()

    def __initWidget(self):
        self.initLayout()

        self.translate_to_mainlang.setChecked(True)
        
        self.model_select.addItems(["模型1", "模型2", "模型3"])
        self.lang_select.addItems(["主要语言1", "主要语言2", "主要语言3"])
        
        self.controlPanel.setObjectName('controlPanel')

    def initLayout(self):
        self.setFixedHeight(220)
        self.controlPanel.setFixedWidth(220)
        self.hBoxLayout.addWidget(self.tabView, 1)
        self.hBoxLayout.addWidget(self.controlPanel, 0, Qt.AlignRight)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        
        hl1 = QHBoxLayout()
        hl1.addWidget(self.btn_start)
        hl1.addWidget(self.btn_stop)
        hl2 = QHBoxLayout()
        hl2.addWidget(self.btn_loadfile)
        hl2.addWidget(self.btn_rec_record)
        
        self.vBoxLayout.addLayout(hl1)
        self.vBoxLayout.addLayout(hl2)
        self.vBoxLayout.addWidget(self.btn_play_record)
        self.vBoxLayout.setContentsMargins(24, 32, 12, 32)

        self.panelLayout.setSpacing(8)
        self.panelLayout.setContentsMargins(14, 16, 14, 14)
        self.panelLayout.setAlignment(Qt.AlignTop)

        self.panelLayout.addWidget(self.model_selectLabel)
        self.panelLayout.addWidget(self.model_select)
        self.panelLayout.addWidget(self.lang_selectLabel)
        self.panelLayout.addWidget(self.lang_select)
        self.panelLayout.addSpacing(4)
        self.panelLayout.addWidget(self.save_record)
        self.panelLayout.addWidget(self.translate_to_mainlang)

class SubMediaPlayer(StandardMediaPlayBar):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.close_button = TransparentToolButton(FluentIcon.CLOSE, self)
        self.buttonLayout.addWidget(self.close_button, alignment=Qt.AlignmentFlag.AlignRight)

class SpeechRecInterface(QWidget):
    # ret_text_s = Signal(str)
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._init_ui()
        
        self.subplayer = None
        
        self.vb_layout = QVBoxLayout(self)
        self.strongLabel = StrongBodyLabel("语音识别", self)
        self.label = BodyLabel("speech recognition", self)
        self.button_interface = ButtonInterface(self)
        self.textDisplay = TextDisplay(self)
        self.textToolBar = TextToolBar(self.textDisplay, self)
        self.connect_btns()

        self.vb_layout.addWidget(self.strongLabel)
        self.vb_layout.addWidget(self.label)
        self.vb_layout.addWidget(self.button_interface)
        self.vb_layout.addWidget(self.textToolBar)
        self.vb_layout.addWidget(self.textDisplay)
        
        # self.Overlay = SiOverlay(self)
        # self.Overlay.addInterface(SubMediaPlayer(self), "SubPlayer")
        
    def _init_ui(self):
        self.setObjectName("SpeechRecInterface")
        self.resize(800, 600)

    def connect_btns(self):
        self.button_interface.btn_start.clicked.connect(self.start_rec_stream)
        self.button_interface.btn_stop.clicked.connect(self.stop_rec_stream)
        self.button_interface.btn_loadfile.clicked.connect(self.load_file)
        self.button_interface.btn_rec_record.clicked.connect(self.start_rec_record)
        self.button_interface.btn_play_record.clicked.connect(self.play_record)

        self.button_interface.save_record.stateChanged.connect(self.save_record_changed)
        self.button_interface.translate_to_mainlang.stateChanged.connect(self.translate_to_mainlang_changed)

    def start_rec_stream(self):
        pass
    def stop_rec_stream(self):
        pass
    
    def load_file(self):
        pass
    def start_rec_record(self):
        pass
    
    def play_record(self):
        print('play_record')
        if self.subplayer is None or not self.subplayer.isVisible():
            player = SubMediaPlayer(self)
            player.resize(self.width(), 100)
            self.setMinimumWidth(player.width())
            self.subplayer = SubWidget(player, self)
            player.close_button.clicked.connect(self.subplayer.close_with_animation)
            self.subplayer.move(self.rect().bottomLeft() - self.subplayer.rect().bottomLeft())
            self.subplayer.show()
    def resizeEvent(self, event):
        # and self.subplayer.pos().y() - self.subplayer.height() == 0
        if self.subplayer and self.subplayer.isVisible():
            self.subplayer.move(self.rect().bottomLeft() - self.subplayer.rect().bottomLeft())
        super().resizeEvent(event)
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = event.globalPos() - self.frameGeometry().topLeft()
            close_sub = not ((self.subplayer is None or not self.subplayer.isVisible()) and self.subplayer.rect().contains(event.pos()))
            event.accept()
            if close_sub:
                self.subplayer.close_with_animation()
                self.setMinimumWidth(0)
    
    def save_record_changed(self, state):
        pass
    def translate_to_mainlang_changed(self, state):
        pass


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = SpeechRecInterface()
    w.show()
    sys.exit(app.exec())