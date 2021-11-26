from PyQt5.QtWidgets import *

from src.ui.exceptKeyword import ExceptKeyword
from src.ui.mainWidget import MainWidget
from src.ui.searchKeyword import SearchKeyword
from src.ui.subWidget import SubWidget


class TabWidget(QWidget):
    def __init__(self, window):
        QWidget.__init__(self)
        self.window = window

        self.tabWidgets = QTabWidget()
        self.tabWidgets.addTab(MainWidget(self.window), "입찰공고")
        self.tabWidgets.addTab(SubWidget(self.window), "사전규격")

        self.tabKeywords = QTabWidget()
        self.tabKeywords.addTab(SearchKeyword(self.window), "검색어")
        self.tabKeywords.addTab(ExceptKeyword(self.window), "제외어")

        layout = QHBoxLayout()
        layout.addWidget(self.tabWidgets, 6)
        layout.addWidget(self.tabKeywords, 4)

        self.setLayout(layout)
