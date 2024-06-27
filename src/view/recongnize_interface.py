# Speech Recognition
from os import remove
from pathlib import Path
from threading import Thread
from functools import partial
from utils.utils import call_delay
from os.path import join as _join

from PySide6.QtCore import Qt, QUrl, QPropertyAnimation, QRect, Signal, Slot
from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QGridLayout, QHBoxLayout, QSpacerItem, \
                            QSizePolicy, QLabel, QStackedWidget, QFileDialog
# from PySide6.QtGui import QPalette, QColor

from qfluentwidgets import  BodyLabel, PushButton, ScrollArea, ComboBox, StrongBodyLabel, CheckBox, \
                            IndeterminateProgressBar, TransparentToolButton, FluentIcon, StateToolTip, \
                            InfoBar, InfoBarPosition
from qfluentwidgets.multimedia import StandardMediaPlayBar

from pyperclip import copy as perclip_copy

from .overlay_interface import SubWidget
from components.globals import Globals
from record.record import Record
from datetime import datetime

class StatusBar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("StatusBar")
        # self.resize(800, 50)
        self.setFixedHeight(50)

        self.state = QLabel(self)
        self.state_bar = IndeterminateProgressBar(self)
        
        self.now_record = QLabel(self)
        
        self.hbox_layout = QHBoxLayout()
        self.vbox_layout = QVBoxLayout(self)
        
        self.hbox_layout.setContentsMargins(16, 0, 16, 0)
        self.hbox_layout.addWidget(self.state, 1, Qt.AlignmentFlag.AlignLeft)
        self.hbox_layout.addWidget(self.now_record, 1, Qt.AlignmentFlag.AlignRight)
        
        self.vbox_layout.addLayout(self.hbox_layout)
        self.vbox_layout.addWidget(self.state_bar, 0.5)
        
        self.init_status()
    def init_status(self):
        self.state_bar.pause()
        # self.state_bar.resume()
        self.state.setText("")
        self.now_record.setText(f"{self.tr('当前未选择录音文件')}")
    
    def set_state(self, state):
        self.state.setText(state)
    def resume_state(self):
        self.state.setText("")
    def set_now_record(self, name):
        self.now_record.setText(f"{self.tr('当前选择录音文件')}: {name}")
        
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
        # self.resize(800, 50)
        self.setFixedHeight(50)
        self.text = text_widget
        
        self.hb_layout = QHBoxLayout(self)
        self.hb_translate_layout = QHBoxLayout()
        self.btn_copy = PushButton("复制")
        self.btn_clear = PushButton("清空")
        self.btn_translate = PushButton("翻译为")
        self.combox_translate = ComboBox()
        self.combox_translate.addItems(["中文", "英文", "日文"])
        
        self.hb_layout.addWidget(self.btn_copy, 1, Qt.AlignmentFlag.AlignLeft)
        
        w = parent.width() if parent is not None else 800
        spacer = QSpacerItem(w*2, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        # spacer_2 = QSpacerItem(w/4, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.hb_layout.addItem(spacer)
        self.hb_translate_layout.addWidget(self.btn_translate, 1, Qt.AlignmentFlag.AlignRight)
        self.hb_translate_layout.addWidget(self.combox_translate, 1, Qt.AlignmentFlag.AlignRight)
        self.hb_layout.addLayout(self.hb_translate_layout, 0)
        # self.hb_layout.addItem(spacer_2)
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
        self.btn_start_record = PushButton(self.tr("开始录音"), self)
        self.btn_stop_record = PushButton(self.tr("停止录音"), self)
        
        self.model_selectLabel = BodyLabel(self.tr("模型选择"), self)
        self.model_select = ComboBox(self)
        self.lang_selectLabel = BodyLabel(self.tr("主要语言选择"), self)
        self.lang_select = ComboBox(self)
        
        self.btn_save_record_path = PushButton(self.tr("选择保存录音路径"), self)
        self.save_record = CheckBox(self.tr("保存录音"), self)
        self.translate_to_mainlang = CheckBox(self.tr("始终翻译成主要语言"), self)
        
        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout(self.tabView)
        self.panelLayout = QVBoxLayout(self.controlPanel)

        self.__initWidget()

    def __initWidget(self):
        self.initLayout()

        self.translate_to_mainlang.setChecked(True)
        
        
        self.model_select.addItems(list(Globals.rec_models))
        self.lang_select.addItems(["中文", "英语", "日语"])
        
        self.controlPanel.setObjectName('controlPanel')

    def initLayout(self):
        self.setFixedHeight(250)
        self.controlPanel.setFixedWidth(220)
        self.hBoxLayout.addWidget(self.tabView, 1)
        self.hBoxLayout.addWidget(self.controlPanel, 0, Qt.AlignRight)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        
        hl1 = QHBoxLayout()
        hl1.addWidget(self.btn_start)
        hl1.addWidget(self.btn_stop)
        hl2 = QHBoxLayout()
        hl2.addWidget(self.btn_rec_record)
        hl2.addWidget(self.btn_loadfile)
        hl3 = QHBoxLayout()
        hl3.addWidget(self.btn_start_record)
        hl3.addWidget(self.btn_stop_record)
        
        self.vBoxLayout.addLayout(hl1)
        self.vBoxLayout.addLayout(hl2)
        self.vBoxLayout.addLayout(hl3)
        self.vBoxLayout.addWidget(self.btn_play_record)
        self.vBoxLayout.setContentsMargins(24, 32, 12, 32)

        self.panelLayout.setSpacing(8)
        self.panelLayout.setContentsMargins(14, 16, 14, 14)
        self.panelLayout.setAlignment(Qt.AlignTop)

        self.panelLayout.addWidget(self.model_selectLabel)
        self.panelLayout.addWidget(self.model_select)
        self.panelLayout.addWidget(self.lang_selectLabel)
        self.panelLayout.addWidget(self.lang_select)
        self.panelLayout.addWidget(self.btn_save_record_path)
        self.panelLayout.addSpacing(4)
        self.panelLayout.addWidget(self.save_record)
        self.panelLayout.addWidget(self.translate_to_mainlang)

class SubMediaPlayer(StandardMediaPlayBar):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.close_button = TransparentToolButton(FluentIcon.CLOSE, self)
        self.buttonLayout.addWidget(self.close_button)


# ================================== Recognizer Interface ==================================
# 语音识别界面                                                                              =
# ==========================================================================================
class SpeechRecInterface(QWidget):
    # ret_text_s = Signal(str)
    hide_status = Signal(tuple)
    rec_resoult = Signal(str)
    rec_resoult_stream = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._init_ui()
        
        self.rec_model_inited_lst = []
        self.rec_stream_started = False
        self.rec_record_started = False
        self.record_started = False
        self.subplayer = None
        self.player = None
        self.audio_file = None
        self.save_path = "./records"
        
        self.vb_layout = QVBoxLayout(self)
        self.strongLabel = StrongBodyLabel("语音识别", self)
        self.label = BodyLabel("speech recognition", self)
        self.status_bar = StatusBar(self)
        self.button_interface = ButtonInterface(self)
        self.textDisplay = TextDisplay(self)
        self.textToolBar = TextToolBar(self.textDisplay, self)
        self.connect_btns()

        self.vb_layout.addWidget(self.strongLabel)
        self.vb_layout.addWidget(self.label)
        self.vb_layout.addWidget(self.status_bar)
        self.vb_layout.addWidget(self.button_interface)
        self.vb_layout.addWidget(self.textToolBar)
        self.vb_layout.addWidget(self.textDisplay)
        
        self.hide_status.connect(self.hide_loading_status)
        
    def _init_ui(self):
        self.setObjectName("SpeechRecInterface")
        # self.resize(800, 600)

    def connect_btns(self):
        self.button_interface.btn_start.clicked.connect(self.start_rec_stream)
        self.button_interface.btn_stop.clicked.connect(self.stop_rec_stream)
        self.button_interface.btn_loadfile.clicked.connect(self.load_file)
        self.button_interface.btn_rec_record.clicked.connect(self.start_rec_record)
        self.button_interface.btn_start_record.clicked.connect(self.start_record)
        self.button_interface.btn_stop_record.clicked.connect(self.stop_record)
        
        self.button_interface.btn_play_record.clicked.connect(self.play_record)
        self.button_interface.btn_save_record_path.clicked.connect(self.open_save_record_path)

        self.button_interface.save_record.stateChanged.connect(self.save_record_changed)
        self.button_interface.translate_to_mainlang.stateChanged.connect(self.translate_to_mainlang_changed)

    def start_rec_stream(self):
        if self.rec_stream_started:
            self.warning_message(self.tr("注意"), self.tr("实时识别已启动"))
            return
        if self.rec_record_started:
            self.warning_message(self.tr("注意"), self.tr("正在识别录音，请等待识别录音结束"))
            return
        
        model = self.button_interface.model_select.currentText()
        model_info = Globals.rec_models[model]
        if not model_info.get('support_stream'):
            self.error_message(self.tr("错误"), self.tr("当前模型不支持实时识别"))
            return
        lang = self.button_interface.lang_select.currentText()
        if model not in self.rec_model_inited_lst:
            self.load_model(model, lang)
            self.rec_stream_started = True
        else:
            self.status_bar.set_state(f"{self.tr('正在启动实时识别: ')} {model}")
            self.rec_stream_started = True

    def stop_rec_stream(self):
        if not self.rec_stream_started:
            self.warning_message(self.tr("注意"), self.tr("实时识别未启动"))
            return
        self.rec_stream_started = False
    def rec_stream_callback(self):
        pass
    
    def start_rec_record(self):
        if self.rec_record_started:
            self.warning_message(self.tr("注意"), self.tr("正在识别录音中..."))
            return
        if self.rec_stream_started:
            self.warning_message(self.tr("注意"), self.tr("实时识别已启动，请先停止实时识别"))
            return
        if self.audio_file is None:
            self.warning_message(self.tr("注意"), self.tr("需要先选择音频文件"))
            return
        model = self.button_interface.model_select.currentText()
        model_info = Globals.rec_models[model]
        

    def load_model(self, model_name, lang):
        self.status_bar.set_state(f"{self.tr('正在加载模型: ')} {model_name}")
        def callback(): 
            self.hide_status.emit((call, f"{self.tr('模型加载成功: ')}{model_name}", self.tr("模型初始化完成，开始实时识别")))
        call = self.show_loading_status(f"{self.tr("初始化模型: ")}{model_name}", self.tr("正在加载模型，请稍候..."))
        # 测试用
        # 退出动画使用了QTimer, 不能将回调在主线程外进行，这里使用信号传递执行回调操作
        call_delay(2, callback)

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, self.tr("选择音频文件"), "", self.tr("音频文件 (*.wav *.mp3)"))
        self.audio_file = file_path
        if file_path:
            self.status_bar.set_now_record(Path(file_path).name)
            if self.player is not None:
                self.player.player.setSource(QUrl.fromLocalFile(file_path))
    def open_save_record_path(self):
        file_path = QFileDialog.getExistingDirectory(self, self.tr("选择保存录音路径"), "")
        if file_path:
            self.save_path = file_path
    
    def start_record(self):
        if self.rec_record_started:
            self.warning_message(self.tr("注意"), self.tr("正在识别录音中..."))
            return
        if self.rec_stream_started:
            self.warning_message(self.tr("注意"), self.tr("实时识别已启动，请先停止实时识别"))
            return
        if self.save_path is None:
            self.warning_message(self.tr("注意"), self.tr("需要先选择保存路径"))
            return
        self.status_bar.set_state(f"{self.tr('正在录音')}")
        self.record_started = True
        self.record = Record()
        self.record.start(_join(self.save_path, datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".wav"))
    
    def stop_record(self):
        if not self.record_started:
            self.warning_message(self.tr("注意"), self.tr("录音未开始"))
            return
        self.status_bar.set_state(f"{self.tr('正在停止录音')}")
        self.record_started = False
        self.record.stop()
        self.status_bar.resume_state()

    
    def play_record(self):
        print('play_record')
        if self.subplayer is None:
            self.player = SubMediaPlayer(self) if self.subplayer is None else self.player
            self.player.resize(self.width(), 200)
            if self.audio_file is None:
                self.warning_message(self.tr("注意"), self.tr("需要先选择音频文件"))
            else:
                self.player.player.setSource(QUrl.fromLocalFile(self.audio_file))
                self.player.player.play()
            
            self.subplayer = SubWidget(self.player, self)
            self.player.close_button.clicked.connect(self.subplayer.close_with_animation)
            self.subplayer.move(self.rect().bottomLeft() - self.subplayer.rect().bottomLeft())
            self.subplayer.show()
        elif not self.subplayer.isVisible():
            self.subplayer.move(self.rect().bottomLeft() - self.subplayer.rect().bottomLeft())
            self.subplayer.show()
    def resizeEvent(self, event):
        # and self.subplayer.pos().y() - self.subplayer.height() == 0
        if self.subplayer and self.subplayer.isVisible():
            self.subplayer.move(self.rect().bottomLeft() - self.subplayer.rect().bottomLeft())
            self.subplayer.resize_all(self.width(), 200)
        super().resizeEvent(event)
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = event.globalPos() - self.frameGeometry().topLeft()
            # close_sub = not ((self.subplayer is None or not self.subplayer.isVisible()) and self.subplayer.rect().contains(event.pos()))
            event.accept()
            # if close_sub:
            #     self.subplayer.close_with_animation()
            #     self.setMinimumWidth(0)

    def save_record_changed(self, state):
        pass
    def translate_to_mainlang_changed(self, state):
        pass
    
    def show_loading_status(self, text, desc):
        def callback(text, desc):
            self.stateTooltip.setTitle(text)
            self.stateTooltip.setContent(desc)
            self.stateTooltip.setState(True)
            self.stateTooltip = None
        self.stateTooltip = StateToolTip(
            text, desc, self.window()
        )
        self.stateTooltip.move(self.stateTooltip.getSuitablePos())
        self.stateTooltip.show()
        return callback
    def hide_loading_status(self, r):
        callback, text, desc = r
        callback(text, desc)
    
    
    def error_message(self, title, message):
        InfoBar.error(
            title=title,
            content=message,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=-1,    # won't disappear automatically
            parent=self
        )
    def warning_message(self, title, message):
        InfoBar.warning(
            title=title,
            content=message,
            orient=Qt.Horizontal,
            isClosable=False,   # disable close button
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=self
        )

if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = SpeechRecInterface()
    w.show()
    sys.exit(app.exec())