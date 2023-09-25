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

        self.new1 = draggbleItems.DraggableWidget(self.home_tab)
        self.new1.move(-100000,-100000)

        self.new2 = draggbleItems.DraggableWidget(self.home_tab)
        self.new2.move(-100000, -100000)

        self.new3 = draggbleItems.DraggableWidget(self.home_tab)
        self.new3.move(-100000, -100000)

        self.new4 = draggbleItems.DraggableWidget(self.home_tab)
        self.new4.move(-100000, -100000)

        self.new5 = draggbleItems.DraggableWidget(self.home_tab)
        self.new5.move(-100000, -100000)

        self.insertTab(self.count()-1, self.home_tab, '')
        self.setCurrentIndex(self.count() - 1)
    def addCube(self):
        print(self.new1.pos())
        if self.opened == 0:
            self.opened += 1
            self.new1.move(0,0)

            self.new1.setLayout(draggbleItems.DraggbleWebEngine(self.new1))
            print(self.opened)
            return 0
        if self.opened == 1:
            self.opened += 1
            self.new2.move(0,0)
            self.new2.setLayout(draggbleItems.DraggbleWebEngine(self.new2))
            print(self.opened)
            return 0
        if self.opened == 2:
            self.opened += 1
            self.new3.move(0,0)

            self.new3.setLayout(draggbleItems.DraggbleWebEngine(self.new3))
            print(self.opened)
            return 0
        if self.opened == 3:
            self.opened += 1
            self.new4.move(0,0)
            self.new4.setLayout(draggbleItems.DraggbleWebEngine(self.new4))
            print(self.opened)
            return 0
        if self.opened == 4:
            self.opened += 1
            self.new5.move(0,0)
            self.new5.setLayout(draggbleItems.DraggbleWebEngine(self.new5))
            print(self.opened)
            return 0
        else: print('Нельзя открыть больше одной вкладки'); return 0
