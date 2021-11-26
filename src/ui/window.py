from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow
from datetime import datetime, timedelta
from src.ui.tabWidget import TabWidget


class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setWindowTitle("나라장터 입찰정보 수집 프로그램")
        self.setWindowIcon(QIcon("images/icon_0.png"))

        self.today = datetime.now()

        if self.today.weekday() == 0:
            self.yesterday = self.today + timedelta(days=-3)

        elif self.today.weekday() == 6:
            self.yesterday = self.today + timedelta(days=-2)

        else:
            self.yesterday = self.today + timedelta(days=-1)

        self.setCentralWidget(TabWidget(self))

