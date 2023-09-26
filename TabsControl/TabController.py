from TabsControl import draggbleItems
from PyQt6.QtWidgets import QTabWidget, QWidget, QVBoxLayout
from WebView import browser
class TabsController(QTabWidget):
    def __init__(self):
        super().__init__()
        self.opened = 0 #счетчик открытых вкладок на HomeTab
        self.newTab()
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.closeTab) #Реагируем на закрытие вкладки
        self.currentChanged.connect(self.tabChanged)  # Реагируем на изменение вкладки


    #---------------Функции для работы с обычными вкладками---------------
    def tabChanged(self, index):
        if self.count()-1 == index: #Кнопка addNewTab реализована как вкладка, так что при нажатии на неё функция возвращает новую вкладку
            self.newTab()
    def closeTab(self, index):
        self.removeTab(index)
        self.setCurrentIndex(self.count()-2) #переключение на предыдущую вкладку

    def newTab(self):   #Добавление новой вкладки с браузером
        new_tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        web_view = browser.BrowserView()
        layout.addWidget(web_view)
        new_tab.setLayout(layout)
        self.insertTab(self.count()-1, new_tab, "Новая вкладка")
        self.setCurrentIndex(self.count()-2) #Что бы вкладка отображалась за addNewTab

    #-------------Функции для работы с Home Tab------------------

    def toHome(self):
        self.setCurrentIndex(0)
    def homeTab(self):
        self.home_tab = QWidget()
        self.insertTab(self.count()-1, self.home_tab, '')
        self.setCurrentIndex(self.count() - 1)

    def addCube(self): #Создание нового окна с браузером
        self.setCurrentIndex(1)
        self.webWindow = draggbleItems.DraggableWidget(self.home_tab)
        self.webWindow.setLayout(draggbleItems.DraggbleWebEngine(self.webWindow))
        self.setCurrentIndex(0)

