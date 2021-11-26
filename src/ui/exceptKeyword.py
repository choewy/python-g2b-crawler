from PyQt5.QtWidgets import *
from src import json
from src.ui.message import Message


class ExceptKeyword(QWidget):
    def __init__(self, window):
        QWidget.__init__(self)
        self.window = window

        # 행 추가 / 저장 버튼
        self.btnAdd = QPushButton()
        self.btnAdd.setText("추가")
        self.btnAdd.clicked.connect(self.btnClickEvent)
        self.btnSave = QPushButton()
        self.btnSave.setText("저장")
        self.btnSave.clicked.connect(self.btnClickEvent)
        h_layout_btn = QHBoxLayout()
        h_layout_btn.addWidget(self.btnAdd)
        h_layout_btn.addWidget(self.btnSave)
        self.groupBtn = QGroupBox()
        self.groupBtn.setLayout(h_layout_btn)
        
        # 테이블
        self.tbl = QTableWidget()
        self.setTbl()

        layout = QVBoxLayout()
        layout.addWidget(self.groupBtn)
        layout.addWidget(self.tbl)

        self.setLayout(layout)

    def btnClickEvent(self):
        btn = self.sender()

        if btn.text() == "추가":
            row = self.tbl.rowCount()
            self.tbl.insertRow(row)
            widget = QLineEdit()
            self.tbl.setCellWidget(row, 0, widget)
            btn = QPushButton("삭제")
            btn.setFixedWidth(60)
            btn.clicked.connect(self.btnClickEvent)
            self.tbl.setCellWidget(row, 1, btn)

        elif btn.text() == "삭제":
            row = self.tbl.currentRow()
            self.tbl.removeRow(row)

        elif btn.text() == "저장":
            old = json.get_except_keywords()
            new = []
            for row in range(self.tbl.rowCount()):
                keyword = self.tbl.cellWidget(row, 0).text()
                if keyword:
                    new.append(keyword)
            if old != new:
                json.set_except_keywords(new)
                Message("저장되었습니다.").exec_()

    def setTbl(self):
        columns = ["제외어", ""]
        keywords = json.get_except_keywords()

        self.tbl.clear()
        self.tbl.setRowCount(0)
        self.tbl.setColumnCount(len(columns))
        self.tbl.setHorizontalHeaderLabels(columns)

        for row, keyword in enumerate(keywords):
            self.tbl.insertRow(row)
            widget = QLineEdit(keyword)
            self.tbl.setCellWidget(row, 0, widget)
            btn = QPushButton("삭제")
            btn.setFixedWidth(60)
            btn.clicked.connect(self.btnClickEvent)
            self.tbl.setCellWidget(row, 1, btn)

        self.tbl.resizeColumnsToContents()
        self.tbl.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
