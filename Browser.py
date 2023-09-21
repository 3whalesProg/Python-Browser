import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QIcon, QKeyEvent
from PyQt6.QtWebEngineWidgets import QWebEngineView

pink_theme = {
    'main': "#2d2d2d",
    'light': "#2d2d2d",
    'lighter': "#2d2d2d"
}

class DraggableWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cube_size_width = 470
        self.cube_size_height = 600
        self.setFixedSize(self.cube_size_width, self.cube_size_height)
        self.setStyleSheet("border: 1px solid #2d2d2d; border-radius: 10px")
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

class UrlNavigationWidget(QWidget):
    def __init__(self, browser_view):
        super().__init__()
        self.browser_view = browser_view

        layout = QHBoxLayout()

        self.url_edit = QLineEdit(self)
        self.url_edit.setStyleSheet(
            "QLineEdit {"
            f"   background-color: white;"
            "   color: black;"
            "   padding: 4px 8px;"
            "   border-radius: 5px;"
            "   width: 10px;"
            "   placeholder: 'Введите запрос для поиска или веб-адрес';"
            "   font-size: 14px;"
            "   border: None;"
            "}"
            "QLineEdit:hover {"
            f"   transition-delay: 5s; background-color: #f2f2f2;"
            "}"
            "QLineEdit:focus{"
            f"   transition-delay: 5s; background-color: white; border: None;"
            "}"
        )
        back_button = QPushButton()
        back_button.setIcon(QIcon(self.get_resized_icon('back.png', 12, 12)))

        back_button.clicked.connect(self.browser_view.back)
        forward_button = QPushButton()
        forward_button.setIcon(QIcon(self.get_resized_icon('foward.png', 12, 12)))
        forward_button.clicked.connect(self.browser_view.forward)
        reload_button = QPushButton()
        reload_button.setIcon(QIcon(self.get_resized_icon('reload.png', 12, 12)))
        reload_button.clicked.connect(self.browser_view.reload)
        self.url_edit.setPlaceholderText("Введите URL и нажмите Enter")
        self.url_edit.returnPressed.connect(self.load_url)
        layout.addWidget(back_button)
        layout.addWidget(forward_button)
        layout.addWidget(reload_button)
        layout.addWidget(self.url_edit)
        layout.setContentsMargins(0, 5, 0, 0)
        self.setStyleSheet(
            "QPushButton{"
            f"background-color: transparent;"
            "border-radius: 3px;"
            "width: 25px;"

            "height: 25px;"
            "border: None;"
            "}"
            "QPushButton:hover{"
            f"background-color: {pink_theme['main']};"
            "border: None;"
            "}"
            "QIcon{ width: 0px;"
            "color: white;}"
        )
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

class BrowserView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.webview = QWebEngineView(self)
        self.navigation_widget = UrlNavigationWidget(self.webview)
        self.webview.setUrl(QUrl('http://google.com'))
        self.webview.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.layout.addWidget(self.navigation_widget)
        self.layout.addWidget(self.webview)
        self.layout.setContentsMargins(0, 0, 0, 0)

class DraggbleWebEngine(QVBoxLayout):
    def __init__(self, parent):
        super().__init__()
        self.box = parent
        self.close_but = QPushButton('закрыть')
        self.close_but.clicked.connect(self.remove_widget)
        self.webview_drag = BrowserView()
        self.addWidget(self.close_but)
        self.addWidget(self.webview_drag)

    def remove_widget(self):
        self.webview_drag.close()
        self.box.move(-1000000,-1000000)

class TabbedBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.opened = 0
        self.setWindowTitle("Tabbed Browser")
        self.add = QPushButton('Добавить кубик')
        self.add.clicked.connect(self.addCube)

        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)


        #self.tab_widget.setMovable(True)
        self.tab_widget.more = QToolButton()
        self.tab_widget.more.setIcon(QIcon('add.png'))
        self.tab_widget.more.setStyleSheet(
            '''border: none;
            padding: 5px;
            color: black;

            hover{background-color:#2d2d2d;}'''
        )
        self.tab_widget.more.clicked.connect(self.addTab)

        self.tab_widget.setCornerWidget(
            self.tab_widget.more, Qt.Corner.TopRightCorner
        )
        self.tab_widget.tabCloseRequested.connect(self.closeTab)

        central_widget = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(self.tab_widget)
        #layout.addWidget(self.add)
        central_widget.setLayout(layout)
        layout.setContentsMargins(0, 4, 0, 0)

        self.tab_widget.setStyleSheet("QTabBar::tab {"
                                      f"background-color: rgb(3,6,21); color: white; padding: 4px 6px; margin-left: 5px; border-radius: 5px; "
                                      "}"
                                      #"QTabBar::tab:hover {background-color:rgb(240,170,199);}"
                                      "QTabBar::tab::selected {"
                                      f"background-color: rgb(72,77,101); color: White;"
                                      "}"
                                      #"QTabBar::tab:first-child { border: 3px solid red; }"
                                      "QTabBar{"
                                      "background-color: rgb(3,6,21);"
                                      "}"
                                      "QTabWidget::pane{"
                                      f"background-color: pink; top: 5px;"
                                      #f"background-image: url('wallpaper.jpg');"
                                      "}"
                                      "QTabBar::close-button {"
                                      "image: url('close.png');"
                                      "border-radius: 3px;"
                                      "}"
                                      "QTabBar::close-button:hover {"
                                      f"background-color: {pink_theme['main']};"
                                      "}"
                                      )

        self.setStyleSheet(
            "QMainWindow {"
            f"   background-color: rgb(3,6,21);"
            "}"
        )
        self.setCentralWidget(central_widget)
        screen = QApplication.primaryScreen()
        screen_size = screen.size()
        window_width = screen_size.width()
        window_height = screen_size.height()

        self.setGeometry(window_width // 7, window_height // 7, int(window_width * 0.7), int(window_height * 0.7))


        self.homeTab()
        self.addTab()

        self.tab_widget.tabBar().setTabButton(0, QTabBar.ButtonPosition.LeftSide, None)
        self.tab_widget.tabBar().setTabButton(0, QTabBar.ButtonPosition.RightSide, None)


    #def tabMoveable(self, index):
    #    # Make all tabs moveable except the first tab (index 0)
    #    return index != 0
#
    def closeTab(self, index):
        if index != 0:
            self.tab_widget.removeTab(index)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
        if event.modifiers() == Qt.KeyboardModifier.AltModifier and event.key() == Qt.Key.Key_Q:
            print('1')
            self.addCube()
        if event.modifiers() == Qt.KeyboardModifier.AltModifier and event.key() == Qt.Key.Key_E:
            self.addTab()



    def homeTab(self):
        self.home_tab = QWidget()
        #self.home_tab.setStyleSheet("background-image: url('wallpaper.jpg');")
        #self.home_tab.setWindowIcon(QIcon('logo.png'))
        #self.label = QLabel(self.home_tab)
        #self.label.setPixmap(QIcon("./logo.png").pixmap(24,24))
        self.new1 = DraggableWidget(self.home_tab)
        self.new1.move(-100000,-100000)

        self.new2 = DraggableWidget(self.home_tab)
        self.new2.move(-100000, -100000)

        self.new3 = DraggableWidget(self.home_tab)
        self.new3.move(-100000, -100000)

        self.new4 = DraggableWidget(self.home_tab)
        self.new4.move(-100000, -100000)

        self.new5 = DraggableWidget(self.home_tab)
        self.new5.move(-100000, -100000)
        self.tab_widget.addTab(self.home_tab, "home")
    def addCube(self):
        print(self.new1.pos())
        if self.opened == 0:
            self.opened += 1
            self.new1.move(0,0)

            self.new1.setLayout(DraggbleWebEngine(self.new1))
            print(self.opened)
            return 0
        if self.opened == 1:
            self.opened += 1
            self.new2.move(0,0)
            self.new2.setLayout(DraggbleWebEngine(self.new2))
            print(self.opened)
            return 0
        if self.opened == 2:
            self.opened += 1
            self.new3.move(0,0)

            self.new3.setLayout(DraggbleWebEngine(self.new3))
            print(self.opened)
            return 0
        if self.opened == 3:
            self.opened += 1
            self.new4.move(0,0)
            self.new4.setLayout(DraggbleWebEngine(self.new4))
            print(self.opened)
            return 0
        if self.opened == 4:
            self.opened += 1
            self.new5.move(0,0)
            self.new5.setLayout(DraggbleWebEngine(self.new5))
            print(self.opened)
            return 0
        else: print('Нельзя открыть больше одной вкладки'); return 0
    def addTab(self):
        new_tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        #web_view = QWebEngineView()
        web_view = BrowserView()
        layout.addWidget(web_view)
        new_tab.setLayout(layout)
        #print(random.randint(0,100))
        #self.tab_widget.setStyleSheet("QTabBar::tab {"
        #                              f"background-color: {pink_theme['main']}; color: black; padding: 5px 7px; border-bottom: 1px solid rgb(230,0,92); width:{random.randint(0,100)}px;"
        #                              "}")
        #web_view.webview.titleChanged.connect(self.some())
        self.tab_widget.addTab(new_tab, "Новая вкладка")


def main():
    app = QApplication(sys.argv)
    window = TabbedBrowser()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()