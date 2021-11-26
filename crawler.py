from PyQt5.QtWidgets import QApplication
from sys import argv
from src.ui.window import Window


app = QApplication(argv)
window = Window()
window.show()
app.exec_()
