from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *


class Message(QDialog):
    def __init__(self, text):
        QDialog.__init__(self)
        self.setWindowTitle("알림")
        self.setWindowIcon(QIcon("images/icon_0.png"))
        self.labelText = QLabel(text)
        self.labelText.setAlignment(Qt.AlignCenter)
        self.btnClose = QPushButton("닫기")
        self.btnClose.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(self.labelText)
        layout.addWidget(self.btnClose)

        self.setLayout(layout)

    def setText(self, text):
        self.labelText.setText(text)
