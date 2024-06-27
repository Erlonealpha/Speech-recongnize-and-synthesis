from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel

from qfluentwidgets import FluentIcon as FLI, ExpandLayout, ScrollArea


class SettingInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget() # 滚动区域窗口
        self.expandLayout = ExpandLayout(self.scrollWidget) # 展开布局
        
        self.settingLabel = QLabel("Settings", self.scrollWidget)
        self._init_widgets()

    
    def _init_widgets(self):
        # self.resize(800, 600)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName('settingInterface')
        
        self.scrollWidget.setObjectName('scrollWidget')
        self.settingLabel.setObjectName('settingLabel')
        
        self._init_layout() # 初始化布局
        self._connect_SignalToSlot() # 连接信号与槽
    
    def _init_layout(self):
        ...
        # self.settingLabel.move(36, 30)
    def _connect_SignalToSlot(self):
        ...