from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve

class SubWidget(QWidget):
    def __init__(self, widget, parent=None):
        super().__init__(parent)
        self.resize(widget.size())
        self.setFixedHeight(widget.height())
        
        self.view = widget
        self.vbox_layout = QVBoxLayout(self)
        self.vbox_layout.addWidget(self.view)

        self.show_animation = QPropertyAnimation(self, b"pos")
        self.show_animation.setDuration(300)
        self.show_animation.setEasingCurve(QEasingCurve.OutQuad)

        self.hide_animation = QPropertyAnimation(self, b"pos")
        self.hide_animation.setDuration(150)
        self.hide_animation.setEasingCurve(QEasingCurve.InQuad)

    def showEvent(self, event):
        self.show_animation.setStartValue(self.pos() + self.parent().rect().bottomLeft())
        self.show_animation.setEndValue(self.pos())
        self.show_animation.start()
        super().showEvent(event)

    def close_with_animation(self):
        self.hide_animation.setStartValue(self.pos())
        self.hide_animation.setEndValue(self.pos() + self.parent().rect().bottomLeft())
        self.hide_animation.finished.connect(self.close)
        self.hide_animation.start()
    
    def resize_all(self, width, height):
        self.view.resize(width, height)
        self.resize(width, height)

    # def mousePressEvent(self, event):
    #     if event.button() == Qt.LeftButton:
    #         self.drag_start_position = event.globalPos() - self.frameGeometry().topLeft()
    #         event.accept()

    # def mouseMoveEvent(self, event):
    #     if event.buttons() == Qt.LeftButton:
    #         new_pos = event.globalPos() - self.drag_start_position
    #         # 限制子窗口的位置在主窗口内
    #         if new_pos.x() < 0:
    #             new_pos.setX(0)
    #         elif new_pos.x() + self.width() > self.parent().width():
    #             new_pos.setX(self.parent().width() - self.width())
    #         if new_pos.y() < 0:
    #             new_pos.setY(0)
    #         elif new_pos.y() + self.height() > self.parent().height():
    #             new_pos.setY(self.parent().height() - self.height())
    #         self.move(new_pos)
    #         event.accept()


