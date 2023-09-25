from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QKeyEvent, QPixmap
from TabsControl import TabController

class TabbedBrowser(QMainWindow): #Класс управляет всеми вкладками
    def __init__(self):
        super().__init__()

        #Подуключаем вкладки и открываем домашнюю
        self.tab_widget = TabController.TabsController()
        self.tab_widget.homeTab()

        tabsCounter = self.tab_widget.count()

        #Добавляем кнопку, для создания новых вкладок
        self.tab_widget.addNewTab = QToolButton()
        addIcon = QPixmap('style/icons/add.png')
        scaledaddIcon = addIcon.scaled(QSize(13,13))
        self.tab_widget.addNewTab.setIcon(QIcon(scaledaddIcon))
        self.tab_widget.addNewTab.clicked.connect(self.tab_widget.newTab)
        self.tab_widget.addNewTab.setStyleSheet(
            '''border: none;
            color: black;
            margin-left: -4px;
            margin-right: 2px;
            '''
        )
        self.tab_widget.insertTab(tabsCounter, QWidget(), "")
        self.tab_widget.tabBar().setTabButton(
            tabsCounter, QTabBar.ButtonPosition.RightSide, self.tab_widget.addNewTab #Полдний индекс для кнопки
        )


        #Добавляем кнопку домашней вкладки\
        self.tab_widget.home = QToolButton()
        homeIcon = QPixmap('style/icons/home.png')
        scaledHomeIcon = homeIcon.scaled(QSize(13,13))
        self.tab_widget.home.setIcon(QIcon(scaledHomeIcon))
        self.tab_widget.home.clicked.connect(self.tab_widget.toHome)
        self.tab_widget.home.setStyleSheet(
            '''border: none;
            color: black;
            margin-left: -4px;
            margin-right: 2px;''')
        self.tab_widget.tabBar().setTabButton(
            0, QTabBar.ButtonPosition.RightSide, self.tab_widget.home) #0 индекс для домашней вкладки


        #Контейнер длля tab_widget
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.tab_widget)
        central_widget.setLayout(layout)
        layout.setContentsMargins(0, 4, 0, 0)

        # Настройка окна
        self.setWindowTitle("Tabbed Browser")
        self.setCentralWidget(central_widget)
        screen = QApplication.primaryScreen()
        screen_size = screen.size()
        window_width = screen_size.width()
        window_height = screen_size.height()
        self.setGeometry(window_width // 7, window_height // 7, int(window_width * 0.7), int(window_height * 0.7))  # Окно размером 70% от экрана, распологается посередине

        #Подключаем стили
        with open('style/css/draggableBrowser.css', 'r') as style:
            self.setStyleSheet(style.read())




    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
        if event.modifiers() == Qt.KeyboardModifier.AltModifier and event.key() == Qt.Key.Key_Q: #Создание окна на HomeTab
            self.tab_widget.addCube()
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_T: #Создание newTab
            self.tab_widget.newTab()







