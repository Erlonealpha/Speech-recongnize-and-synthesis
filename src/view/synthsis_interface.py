from PySide6.QtCore import Qt, QUrl, QPropertyAnimation, QRect, Signal, Slot
from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QGridLayout, QHBoxLayout, QTableWidgetItem, QFileDialog
# from PySide6.QtGui import QPalette, QColor

from qfluentwidgets import  BodyLabel, PushButton, ScrollArea, ComboBox, StrongBodyLabel, CheckBox, \
                            PlainTextEdit, TableWidget, InfoBar, InfoBarPosition, TransparentToolButton, \
                            FluentIcon
from qfluentwidgets.multimedia import StandardMediaPlayBar

from .overlay_interface import SubWidget
from pyperclip import copy as perclip_copy
from components.globals import Globals
from recongnize.api import SpeechRecognition

class SubMediaPlayer(StandardMediaPlayBar):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.close_button = TransparentToolButton(FluentIcon.CLOSE, self)
        self.buttonLayout.addWidget(self.close_button)
        
        self.resize(self.parent().width(), 200)
        
class TextToolBar(QWidget):
    def __init__(self, text_edit: PlainTextEdit, parent=None):
        super().__init__(parent)
        self.text_edit = text_edit
        self.hbox_layout = QHBoxLayout(self)
        self.setFixedHeight(50)
        
        self.btn_copy = PushButton("复制")
        self.btn_clear = PushButton("清空")
        
        self.hbox_layout.addWidget(self.btn_copy, 1, Qt.AlignmentFlag.AlignLeft)
        self.hbox_layout.addWidget(self.btn_clear, 1, Qt.AlignmentFlag.AlignRight)
        
        self.connect_btns()
    def connect_btns(self):
        self.btn_copy.clicked.connect(self.copy_text)
        self.btn_clear.clicked.connect(self.clear_text)
    def copy_text(self):
        print('copy_text')
        perclip_copy(self.text_edit.toPlainText())
    def clear_text(self):
        print('clear_text')
        self.text_edit.clear()
        
class TextInput(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.text_edit = PlainTextEdit(self)
        self.toolbar = TextToolBar(self.text_edit, self)

        self.vbox_layout = QVBoxLayout(self)
        self.vbox_layout.addWidget(self.toolbar)
        self.vbox_layout.addWidget(self.text_edit)
        self.text_edit.setPlaceholderText(self.tr("请输入文本"))
        
class TableFrame(TableWidget):
    def __init__(self, headers, table_data, parent=None):
        super().__init__(parent)

        self.verticalHeader().hide()
        self.setBorderRadius(8)
        self.setBorderVisible(True)

        self.setColumnCount(len(headers))
        self.setRowCount(len(table_data))
        self.setHorizontalHeaderLabels(headers)

        for i, data in enumerate(table_data):
            for j in range(len(data)):
                self.setItem(i, j, QTableWidgetItem(data[j]))
                
        self.resizeColumnsToContents()
        
class TableWidgetF(QFrame):
    def __init__(self, headers, table_data, parent=None):
        super().__init__(parent)
        self.setObjectName('tableWidgetF')
        self.resize(self.parent().width(), 650)
        self.setFixedHeight(650)
        
        self.model = None
        
        self.vbox_layout = QVBoxLayout(self)
        self.close_button = TransparentToolButton(FluentIcon.CLOSE, self)
        self.table_widget = TableFrame(headers, table_data, self)
        self.vbox_layout.addWidget(self.close_button, 0, Qt.AlignmentFlag.AlignRight)
        self.vbox_layout.addWidget(self.table_widget)
    
        self.setStyleSheet('''QFrame {
                background-color: rgb(250, 250, 250);
                border-radius: 8px;
                border: 1px solid rgb(220, 220, 220);
            }''')
        
class ButtonInterface(QWidget):
    """ Tab interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # self.tabCount = 1

        # self.tabBar = TabBar(self)
        # self.stackedWidget = QStackedWidget(self)
        self.tabView = QWidget(self)
        self.controlPanel = QFrame(self)

        self.btn_start = PushButton(self.tr("开始语音合成"), self)
        self.btn_play = PushButton(self.tr("播放录音"), self)

        self.model_selectLabel = BodyLabel(self.tr("模型选择"), self)
        self.model_select = ComboBox(self)
        self.voice_selectLabel = BodyLabel(self.tr("音色选择"), self)
        self.voice_select = ComboBox(self)
        
        self.btn_save_path = PushButton(self.tr("选择保存音频文件路径"), self)
        self.btn_open_table = PushButton(self.tr("打开模型音色详情表格(如有)"), self)
        
        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout(self.tabView)
        self.panelLayout = QVBoxLayout(self.controlPanel)

        self.__initWidget()

    def __initWidget(self):
        self.initLayout()

        self.model_select.addItems(list(Globals.synth_models))
        model = self.model_select.currentText()
        models = list(Globals.synth_models.get(model, {}).get('models'))
        if models is not None:
            self.voice_select.addItems([x[1] for x in models[1:]])
        else:
            self.voice_select.addItems(["中文", "英语", "日语"])
        
        self.controlPanel.setObjectName('controlPanel')

    def initLayout(self):
        self.setFixedHeight(240)
        self.controlPanel.setFixedWidth(260)
        self.hBoxLayout.addWidget(self.tabView, 1)
        self.hBoxLayout.addWidget(self.controlPanel, 0, Qt.AlignRight)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.vBoxLayout.addWidget(self.btn_start)
        self.vBoxLayout.addWidget(self.btn_play)
        self.vBoxLayout.setContentsMargins(24, 36, 12, 36)

        self.panelLayout.setSpacing(8)
        self.panelLayout.setContentsMargins(14, 16, 14, 14)
        self.panelLayout.setAlignment(Qt.AlignTop)

        self.panelLayout.addWidget(self.model_selectLabel)
        self.panelLayout.addWidget(self.model_select)
        self.panelLayout.addWidget(self.voice_selectLabel)
        self.panelLayout.addWidget(self.voice_select)
        self.panelLayout.addWidget(self.btn_save_path)
        self.panelLayout.addWidget(self.btn_open_table)
        self.panelLayout.addSpacing(4)

class SynthsisInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('synthsisInterface')
        
        self.table_frame: TableWidgetF = None
        self.subview: SubWidget = None
        self.subplayer: SubWidget = None
        self.player: SubMediaPlayer = None
        self.time_stamps_dic = {}
        
        self.is_synthesis = False
        self.save_folder = None
        self.now_audio_path = None
        
        self.vbox_layout = QVBoxLayout(self)
        self.strongLabel = StrongBodyLabel("语音合成", self)
        self.label = BodyLabel("speech synthesis", self)
        self.button_interface = ButtonInterface(self)
        self.text_input = TextInput(self)
        
        self.vbox_layout.addWidget(self.strongLabel)
        self.vbox_layout.addWidget(self.label)
        self.vbox_layout.addWidget(self.button_interface)
        self.vbox_layout.addWidget(self.text_input)
        
        self._connect_btns()
        
    def _connect_btns(self):
        self.button_interface.btn_start.clicked.connect(self.start_synthesis)
        self.button_interface.btn_play.clicked.connect(self.play_audio)
        self.button_interface.btn_save_path.clicked.connect(self.select_save_path)
        self.button_interface.btn_open_table.clicked.connect(self.show_table)
        
    def start_synthesis(self):
        def callback(audio_path, time_stamps):
            self.is_synthesis = False
            self.time_stamps_dic[audio_path] = time_stamps
            self.load_audio(audio_path)
            
        if self.save_folder is None:
            self.error_message(self.tr("错误"), self.tr("请先选择保存音频文件路径"))
            return
        if self.is_synthesis:
            self.error_message(self.tr("错误"), self.tr("正在合成语音，请等待"))
            return
        text = self.text_input.text_edit.toPlainText()
        if text == '':
            self.warning_message(self.tr("警告"), self.tr("请输入文本"))
            return
        
        self.is_synthesis = True
        
        model = self.get_model_select()
        voice = self.get_voice_select()
        
        SpeechRecognition.tts(text, model, voice, callback, folder=self.save_folder)
    
    def load_audio(self, audio_path):
        self.now_audio_path = audio_path
        if self.player is not None:
            self.player.player.stop()
            self.player.player.setSource(QUrl.fromLocalFile(audio_path))
        
    def play_audio(self):
        if self.subplayer is None:
            self.player = SubMediaPlayer(self) if self.subplayer is None else self.player
            # self.player.resize(self.width(), 200)
            if self.now_audio_path is None:
                self.warning_message(self.tr("注意"), self.tr("需要先选择音频文件"))
            else:
                self.player.player.setSource(QUrl.fromLocalFile(self.now_audio_path))
                self.player.player.play()
            
            self.subplayer = SubWidget(self.player, self)
            self.player.close_button.clicked.connect(self.subplayer.close_with_animation)
            self.subplayer.move(self.rect().bottomLeft() - self.subplayer.rect().bottomLeft())
            self.subplayer.show()
        elif not self.subplayer.isVisible():
            self.subplayer.move(self.rect().bottomLeft() - self.subplayer.rect().bottomLeft())
            self.subplayer.show()
        
    def select_save_path(self):
        self.save_folder = QFileDialog.getExistingDirectory(self, self.tr("选择保存音频文件路径"), "./", QFileDialog.ShowDirsOnly)
    
    def show_table(self):
        model = self.get_model_select()
        try:
            no_same = self.table_frame.model != model # check if the table is the same as the current model
        except AttributeError:
            no_same = True
        if self.table_frame is None or no_same:
            table = Globals.synth_models[model].get('models')
            if table is None:
                self.warning_message(self.tr("模型音色详情表格"), self.tr("该模型暂无音色详情表格"))
                return
            headers = table[0]
            table_data = table[1:]
            self.table_frame = TableWidgetF(headers, table_data, self)
            self.table_frame.model = model
        if self.subview is None or no_same:
            self.subview = SubWidget(self.table_frame, self)
            self.table_frame.close_button.clicked.connect(self.subview.close_with_animation)
            self.subview.move(self.rect().bottomLeft() - self.subview.rect().bottomLeft())
            self.subview.show()
        elif not self.subview.isVisible():
            self.subview.move(self.rect().bottomLeft() - self.subview.rect().bottomLeft())
            self.subview.show()
    def resizeEvent(self, event):
        # and self.subview.pos().y() - self.subview.height() == 0
        if self.subview and self.subview.isVisible():
            self.subview.move(self.rect().bottomLeft() - self.subview.rect().bottomLeft())
            self.subview.resize_all(self.width(), self.subview.height())
        super().resizeEvent(event)

    def get_model_select(self):
        return self.button_interface.model_select.currentText()
    def get_voice_select(self):
        return self.button_interface.voice_select.currentText()
    
    
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
    w = SynthsisInterface()
    w.show()
    sys.exit(app.exec())
    