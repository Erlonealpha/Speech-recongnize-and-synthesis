from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QStackedWidget, QVBoxLayout, QLabel

from qfluentwidgets import Pivot, FluentWindow, FluentIcon as FLI
from .recongnize_interface import SpeechRecInterface
from .setting_interface import SettingInterface

class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        self._init_window()

    def _init_window(self):
        self.setWindowTitle("语音助手")
        # self.setWindowIcon(FLI.MICROPHONE)
        
        
        # 移动到屏幕中心
        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        QApplication.processEvents()
        
        self._init_subinsterface()
        self.add_subinsterfaces()
        
        self.resize(1000, 800)
    def _init_subinsterface(self):
        self.recongnize_interface = SpeechRecInterface(self)
        self.setting_interface = SettingInterface(self)
    def add_subinsterfaces(self):
        self.addSubInterface(self.recongnize_interface, FLI.MICROPHONE, self.tr("语音识别"))
        
        self.navigationInterface.addSeparator()
        self.addSubInterface(self.setting_interface, FLI.SETTING, self.tr("设置"), Qt.AlignmentFlag.AlignBottom)
