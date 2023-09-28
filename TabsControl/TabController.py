from TabsControl import draggbleItems
from PyQt6.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QToolButton
from WebView import browser
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
class TabsController(QTabWidget):
    def __init__(self):
        super().__init__()
        self.newTab()
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.closeTab) #Реагируем на закрытие вкладки
        self.currentChanged.connect(self.tabChanged)  # Реагируем на изменение вкладки




    #---------------Функции для работы с обычными вкладками---------------
    def tabChanged(self, index):
        if self.count()-1 == index: #Кнопка addNewTab реализована как вкладка, так что при нажатии на неё функция возвращает новую вкладку
            self.newTab()
    def closeTab(self, index):
        self.setCurrentIndex(0)
        #self.setCurrentIndex(self.count() - 2) #переключение на предыдущую вкладку
        self.removeTab(index)
        self.setCurrentIndex(self.count() - 2)


    def newTab(self):   #Добавление новой вкладки с браузером
        self.new_tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        web_view = browser.BrowserView()
        layout.addWidget(web_view)
        self.new_tab.setLayout(layout)
        self.insertTab(self.count()-1, self.new_tab, "Новая вкладка")
        self.setCurrentIndex(self.count()-2) #Что бы вкладка отображалась за addNewTab

    #-------------Функции для работы с Home Tab------------------

    def toHome(self):
        self.setCurrentIndex(0)
    def homeTab(self):
        self.home_tab = QWidget()
        layout = QVBoxLayout()
        self.home_tab.setLayout(layout)

        self.insertTab(self.count()-1, self.home_tab, '')
        self.setCurrentIndex(self.count() - 1)


    def addWindow(self): #Создание нового окна с браузером
        currenWidget = self.currentWidget()
        currentIndex = self.currentIndex()
        if currentIndex == 0:
            self.setCurrentIndex(1)
            self.webWindow2 = draggbleItems.DraggableWidget(currenWidget)
            self.webWindow2.setLayout(draggbleItems.DraggbleWebEngine(self.webWindow2))
            self.setCurrentIndex(currentIndex)
        else:
            self.setCurrentIndex(0)
            self.webWindow2 = draggbleItems.DraggableWidget(currenWidget)
            self.webWindow2.setLayout(draggbleItems.DraggbleWebEngine(self.webWindow2))
            self.setCurrentIndex(currentIndex)


