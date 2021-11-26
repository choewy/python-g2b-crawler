import threading
from time import sleep
from src.ui.message import Message


class Threading:
    def __init__(self, btn, movie, message, func, args):
        self.btn = btn
        self.movie = movie
        self.message = message
        self.func = func
        self.args = args

        self.state = 1

        self.thread_crawling = threading.Thread(target=self.__start, args=[self.func])
        self.thread_seconds = threading.Thread(target=self.__seconds, args=())

        self.thread_crawling.daemon = True
        self.thread_crawling.start()

        self.thread_seconds.daemon = True
        self.thread_seconds.start()

    def __start(self, func):
        self.btn.setEnabled(False)

        if len(self.args) == 5:
            self.state = func(self.args[0], self.args[1], self.args[2], self.args[3], self.args[4])
        else:
            self.state = func(self.args[0], self.args[1], self.args[2], self.args[3])

    def __end(self):
        self.movie.stop()
        self.btn.setText("실행")
        self.btn.setEnabled(True)

    def __seconds(self):
        sec = 1
        while self.state:
            self.btn.setText(f"수집 중...({sec}초)")
            sleep(1)
            sec += 1

            if self.state == 1:
                continue
            else:
                break

        self.__end()

        if self.state == 0:
            self.message.setText("수집이 완료되었습니다.")
        else:
            self.message.setText(self.state)

        self.message.exec_()


