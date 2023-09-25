from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QUrl

class UrlNavigationWidget(QWidget):
    def __init__(self, browser_view):
        super().__init__()
        self.browser_view = browser_view

        layout = QHBoxLayout()

        self.url_edit = QLineEdit(self)
        back_button = QPushButton()
        back_button.setIcon(QIcon(self.get_resized_icon('style/icons/back.png', 12, 12)))
        back_button.clicked.connect(self.browser_view.back)
        forward_button = QPushButton()
        forward_button.setIcon(QIcon(self.get_resized_icon('style/icons/foward.png', 12, 12)))
        forward_button.clicked.connect(self.browser_view.forward)
        reload_button = QPushButton()
        reload_button.setIcon(QIcon(self.get_resized_icon('style/icons/reload.png', 12, 12)))
        reload_button.clicked.connect(self.browser_view.reload)
        self.url_edit.setPlaceholderText("Введите URL и нажмите Enter")
        self.url_edit.returnPressed.connect(self.load_url)
        layout.addWidget(back_button)
        layout.addWidget(forward_button)
        layout.addWidget(reload_button)
        layout.addWidget(self.url_edit)
        layout.setContentsMargins(0, 5, 0, 0)
        self.setLayout(layout)

    def load_url(self):
        url = self.url_edit.text()
        if url.find('http') == 0:
            self.browser_view.load(QUrl(url))
        else:
            self.browser_view.load(QUrl('https://google.com/search?q=' + url))

    def get_resized_icon(self, icon_path, width, height):
        icon = QIcon(icon_path)
        pixmap = icon.pixmap(width, height)
        return pixmap
