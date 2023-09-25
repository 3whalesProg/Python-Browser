from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from WebView import browser

class DraggableWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cube_size_width = 470
        self.cube_size_height = 600
        self.setFixedSize(self.cube_size_width, self.cube_size_height)
        self.right_mouse_pressed = False
        self.pressed = False
        self.offset = None

    def mousePressEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.pressed = True
            self.offset = event.pos()
            self.raise_()
        elif event.button() == Qt.MouseButton.RightButton:
            self.right_mouse_pressed = True
            self.right_mouse_start_pos = event.position()
            self.right_mouse_start_size_width = self.cube_size_width
            self.right_mouse_start_size_height = self.cube_size_height

    def mouseMoveEvent(self, event):
        if self.pressed:
            new_pos = self.mapToParent(event.pos() - self.offset)
            self.move(new_pos)
        elif self.right_mouse_pressed:
            delta_width = event.position().x() - self.right_mouse_start_pos.x()
            delta_height = event.position().y() -self.right_mouse_start_pos.y()
            self.cube_size_width = max(20, self.right_mouse_start_size_width + delta_width)
            self.cube_size_height = max(20, self.right_mouse_start_size_height + delta_height)
            self.setFixedSize(int(self.cube_size_width), int(self.cube_size_height))

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.pressed = None
            self.offset = None
        if event.button() == Qt.MouseButton.RightButton:
            self.right_mouse_pressed = False
            self.offset = None


class DraggbleWebEngine(QVBoxLayout):
    def __init__(self, parent):
        super().__init__()
        self.box = parent
        self.close_but = QPushButton('закрыть')
        self.close_but.clicked.connect(self.remove_widget)
        self.webview_drag = browser.BrowserView()
        self.addWidget(self.close_but)
        self.addWidget(self.webview_drag)

    def remove_widget(self):
        self.webview_drag.close()
        self.box.move(-1000000,-1000000)
