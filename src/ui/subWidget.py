import os
import pandas as pd
from datetime import date
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from src.threading import Threading
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import *
from src.ui.message import Message
from src import json


dict_browser = {
    "숨김": False,
    "표시(브라우저 클릭 시 검색이 종료됩니다.)": True
}

dict_task_type = {
    "전체": "taskClCdsA",
    "물품": "taskClCds1",
    "공사": "taskClCds3",
    "용역": "taskClCds5",
    "외자": "taskClCds2",
}


def __selector(element):
    return Select(element)


def __input(element, keyword):
    element.clear()
    element.send_keys(keyword)


def crawling(browser, taskTypes, dateFrom, dateTo):
    try:
        search_keywords = json.get_search_keywords()
        except_keywords = json.get_except_keywords()

        url = "https://www.g2b.go.kr:8081/ep/preparation/prestd/preStdSrch.do?taskClCd=1"

        options = webdriver.ChromeOptions()

        if not browser:
            options.add_argument("disable_gpu")
            options.add_argument("headless")
        options.add_argument("window-size=1920x1080")

        """
        driver = webdriver.Chrome(
            executable_path="driver/chromedriver.exe",
            options=options,
            service_args=["hide_console"]
        )
        """

        # 크롬 드라이버 관리자 : 2021-11-26
        driver = webdriver.Chrome(
            ChromeDriverManager().install(),
            options=options,
            service_args=["hide_console"]
        )
        driver.get(url=url)

        for task_type in taskTypes:
            driver.find_element_by_id(task_type).click()

        __selector(driver.find_element_by_id(
            "recordCountPerPage"
        )).select_by_value(
            "100"
        )
        __input(
            driver.find_element_by_id("fromRcptDt"),
            dateFrom
        )
        __input(
            driver.find_element_by_id("toRcptDt"),
            dateTo
        )

        results = []
        keywords = []

        for keyword in search_keywords:
            __input(driver.find_element_by_id("prodNm"), keyword)
            driver.find_element_by_class_name("btn_mdl").click()

            div_len = len(driver.find_element_by_class_name(
                "results"
            ).find_elements_by_tag_name(
                'div'
            ))

            result = []

            div_cnt = 0
            enter_flag = 1

            for idx in range(div_len):
                div = driver.find_element_by_class_name(
                    "results"
                ).find_elements_by_tag_name(
                    'div'
                )[idx]

                if div.text != "검색조건":
                    result.append(div.text)

                    if enter_flag == 2:
                        div_cnt += 1

                        a = div.find_element_by_tag_name('a')
                        a.click()

                        price = driver.find_elements_by_class_name("tb_inner")[3].text
                        result.append(price)

                        driver.find_element_by_class_name(
                            "button3"
                        ).find_element_by_class_name(
                            "btn_mdl"
                        ).click()

                    enter_flag = enter_flag + 1 if enter_flag < 7 else 1

            results += [result[0 + col * 8:(col + 1) * 8] for col in range(div_cnt)]
            keywords += [keyword for _ in range(div_cnt)]

            driver.find_element_by_class_name(
                "button4"
            ).find_element_by_class_name(
                "btn_mdl"
            ).click()

        driver.quit()

        columns = [
            "순번",
            "등록번호",
            "배정예산액",
            "참조번호",
            "품명(사업명)",
            "수요기관",
            "사전규격공개일시",
            "업체등록의견수"
        ]

        results = pd.DataFrame(data=results, columns=columns)
        results["검색어"] = keywords
        
        columns.insert(1, "검색어")
        
        for keyword in except_keywords:
            results = results[results["참조번호"].str.contains(keyword) == False]
            results = results[results["품명(사업명)"].str.contains(keyword) == False]
            results = results[results["수요기관"].str.contains(keyword) == False]

        results["순번"] = [x+1 for x in range(len(results))]
        results = results[columns[:-1]]

        path = os.path.expanduser("~").replace("\\", "//")
        path = f"{path}/desktop/[나라장터-사전규격]-{date.today().strftime('%Y-%m-%d')}.xlsx"
        results.to_excel(path, sheet_name="사전규격", index=False)

        return 0

    except Exception as e:
        return str(e)


class SubWidget(QWidget):
    def __init__(self, window):
        QWidget.__init__(self)

        # 클래스 변수 초기화
        self.window = window
        self.browser = False
        self.searchType = "bidSearchType1"
        self.taskTypes = ["taskClCdsA"]

        # 브라우저 숨김/표시 버튼
        self.radioHide = QRadioButton("숨김")
        self.radioHide.setChecked(True)
        self.radioHide.clicked.connect(self.radioClickEvent)
        self.radioShow = QRadioButton("표시(브라우저 클릭 시 검색이 종료됩니다.)")
        self.radioShow.clicked.connect(self.radioClickEvent)
        h_layout_radio_browser = QHBoxLayout()
        h_layout_radio_browser.addWidget(self.radioHide)
        h_layout_radio_browser.addWidget(self.radioShow)
        self.groupRadioBrowser = QGroupBox()
        self.groupRadioBrowser.setLayout(h_layout_radio_browser)

        # 검색유형 입찰공고/개찰결과/최종낙찰자 버튼
        self.radioType1 = QRadioButton()
        self.radioType1.setText("입찰공고")
        self.radioType1.setChecked(True)
        self.radioType1.clicked.connect(self.radioClickEvent)
        self.radioType2 = QRadioButton()
        self.radioType2.setText("개찰결과")
        self.radioType2.clicked.connect(self.radioClickEvent)
        self.radioType3 = QRadioButton()
        self.radioType3.setText("최종낙찰자")
        self.radioType3.clicked.connect(self.radioClickEvent)
        h_layout_radio_type = QHBoxLayout()
        h_layout_radio_type.addWidget(self.radioType1)
        h_layout_radio_type.addWidget(self.radioType2)
        h_layout_radio_type.addWidget(self.radioType3)
        self.groupRadioType = QGroupBox()
        self.groupRadioType.setLayout(h_layout_radio_type)

        # 업무 전체/물품/공사/용역/리스/외자/비축/기타/민간 버튼
        self.checkTask1 = QCheckBox()
        self.checkTask1.setText("전체")
        self.checkTask1.setChecked(True)
        self.checkTask1.clicked.connect(self.checkClickEvent)
        self.checkTask2 = QCheckBox()
        self.checkTask2.setText("물품")
        self.checkTask2.setChecked(True)
        self.checkTask2.clicked.connect(self.checkClickEvent)
        self.checkTask3 = QCheckBox()
        self.checkTask3.setText("공사")
        self.checkTask3.setChecked(True)
        self.checkTask3.clicked.connect(self.checkClickEvent)
        self.checkTask4 = QCheckBox()
        self.checkTask4.setText("용역")
        self.checkTask4.setChecked(True)
        self.checkTask4.clicked.connect(self.checkClickEvent)
        self.checkTask5 = QCheckBox()
        self.checkTask5.setText("외자")
        self.checkTask5.setChecked(True)
        self.checkTask5.clicked.connect(self.checkClickEvent)
        h_layout_check_task = QHBoxLayout()
        h_layout_check_task.addWidget(self.checkTask1)
        h_layout_check_task.addWidget(self.checkTask2)
        h_layout_check_task.addWidget(self.checkTask3)
        h_layout_check_task.addWidget(self.checkTask4)
        h_layout_check_task.addWidget(self.checkTask5)
        self.groupCheckTask = QGroupBox()
        self.groupCheckTask.setLayout(h_layout_check_task)

        # 검색일자
        today = self.window.today
        yesterday = self.window.yesterday
        self.dateFrom = QDateEdit()
        self.dateFrom.setMaximumDate(QDate(today.year, today.month, today.day))
        self.dateFrom.setDate(QDate(yesterday.year, yesterday.month, yesterday.day))
        self.dateFrom.setCurrentSectionIndex(2)
        self.labelDate = QLabel()
        self.labelDate.setText("~")
        self.labelDate.setAlignment(Qt.AlignCenter)
        self.labelDate.setFixedWidth(30)
        self.dateTo = QDateEdit()
        self.dateTo.setMinimumDate(QDate(yesterday.year, yesterday.month, yesterday.day))
        self.dateTo.setDate(QDate.currentDate())
        self.dateTo.setCurrentSectionIndex(2)
        h_layout_date = QHBoxLayout()
        h_layout_date.addWidget(self.dateFrom)
        h_layout_date.addWidget(self.labelDate)
        h_layout_date.addWidget(self.dateTo)
        self.groupDate = QGroupBox()
        self.groupDate.setLayout(h_layout_date)

        # 로딩 이미지/로딩 라벨/실행 버튼
        self.movieCube = QMovie("images/Loading_0.gif")
        self.movieCube.start()
        self.movieCube.stop()
        self.labelMovie = QLabel()
        self.labelMovie.setMovie(self.movieCube)
        self.labelMovie.setFixedWidth(25)
        self.btnRun = QPushButton("실행")
        self.btnRun.setFixedWidth(120)
        self.btnRun.setShortcut("return")
        self.btnRun.clicked.connect(self.btnClickEvent)
        h_layout_btn = QHBoxLayout()
        h_layout_btn.addWidget(self.labelMovie)
        h_layout_btn.addWidget(self.btnRun)
        self.groupBtn = QGroupBox()
        self.groupBtn.setLayout(h_layout_btn)

        # 전체 레이아웃
        layout = QVBoxLayout()
        layout.addWidget(self.groupRadioBrowser)
        layout.addWidget(QLabel())
        layout.addWidget(self.groupCheckTask)
        layout.addWidget(self.groupDate)
        layout.addWidget(self.groupBtn)

        self.setLayout(layout)

    @property
    def message(self):
        return Message("")

    def btnClickEvent(self):
        btn = self.sender()
        if btn.text() == "실행":
            self.movieCube.start()

            date_to = self.dateTo.date()
            date_to = date(date_to.year(), date_to.month(), date_to.day()).strftime("%Y/%m/%d")

            date_from = self.dateFrom.date()
            date_from = date(date_from.year(), date_from.month(), date_from.day()).strftime("%Y/%m/%d")

            Threading(
                self.btnRun, self.movieCube, self.message, crawling,
                [self.browser, self.taskTypes, date_from, date_to]
            )

    def radioClickEvent(self):
        radio = self.sender()
        if radio.text() in ["숨김", "표시(브라우저 클릭 시 검색이 종료됩니다.)"]:
            self.browser = dict_browser[radio.text()]

    def checkClickEvent(self, value):
        check = self.sender()

        if check.text() == "전체":
            if value:
                self.checkTask2.setChecked(True)
                self.checkTask3.setChecked(True)
                self.checkTask4.setChecked(True)
                self.checkTask5.setChecked(True)
                self.taskTypes = [dict_task_type[check.text()]]

            else:
                self.checkTask2.setChecked(False)
                self.checkTask3.setChecked(False)
                self.checkTask4.setChecked(False)
                self.checkTask5.setChecked(False)
                self.taskTypes = []

        elif check.text() != "전체":
            check_boxes = [
                self.checkTask2,
                self.checkTask3,
                self.checkTask4,
                self.checkTask5
            ]

            all_check = [check_box.isChecked() for check_box in check_boxes]

            if value:
                self.taskTypes.append(dict_task_type[check.text()])

                if sum(all_check) == len(check_boxes):
                    self.checkTask1.setChecked(True)
                    self.taskTypes = [dict_task_type["전체"]]

            else:
                self.checkTask1.setChecked(False)
                self.taskTypes = []
                for check_box in check_boxes:
                    if check_box.isChecked():
                        self.taskTypes.append(dict_task_type[check_box.text()])
