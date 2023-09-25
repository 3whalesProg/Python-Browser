from PyQt6.QtWidgets import QSizePolicy, QVBoxLayout, QWidget
from PyQt6.QtCore import QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
from WebView import url

class BrowserView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.webview = QWebEngineView(self)
        self.navigation_widget = url.UrlNavigationWidget(self.webview)
        self.webview.setUrl(QUrl('http://google.com'))
        self.webview.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.layout.addWidget(self.navigation_widget)
        self.layout.addWidget(self.webview)
        self.layout.setContentsMargins(0, 0, 0, 0)