# 개발일지

## 2021-03-02

- 기능 정의 및 로직 설계
- 의존성 패키지 설치

```
$ pip install pandas==1.0.5
$ pip install openpyxl
$ pip install pyqt5==5.15.0
$ pip install pyinstaller==3.6
$ pip install selenium==3.141.0
```

---

## 2021-03-05

- window 화면 구현
- widget 탭 구현(입찰공고, 사전규격 구분)
- 키워드 관리 widget 구현(검색어, 제외어 관리)
- 다중 쓰레드를 사용한 입찰공고, 사전규격 정보 수집 기능 구현
- 단, 사전규격 정보 수집 중 가격 정보에 해당하는 element는 검토 필요
- 입찰 공고 정보 수집 중 가격 정보에 해당하는 element는 규칙 찾아야 함

---

## 2021-03-06

- 조달청 시스템 점검으로 인한 작업 불가능 ( ~ 2021.03.07(일) 20시까지 )

---

## 2021-03-08

- 검색 키워드별 수집되는 입찰공고 및 사전규격 결과에 `tb_inner` 수량 파악 후 규칙 파악
- 결과 : 입찰 공고에서 해당 코드 제거 (규칙성이 없으므로 적용 불가능)
- 성능 검사 : 하루 기준 입찰 공고 시 약 600초, 사전 규격 시 약 750초 소요
- 버전 : 1.0.2 빌드

```
$ pyinstaller -w --icon="venv/icon.ico" -p "venv/_dllFiles" crawler.py
```

---

## 2021-03-09

- 버전 : 1.0.3
- `command` 숨김 처리

```python
self.process = subprocess.Popen(
    cmd, env=self.env,
    close_fds=platform.system() != 'Windows',
    stdout=self.log_file,
    stderr=self.log_file,
    stdin=PIPE,
    creationflags=0x08000000
)
```

---

## 2021-11-24

- 종속성 이슈 해결(참고: [stackoverflow](https://stackoverflow.com/questions/68118223/import-error-when-using-pandas-for-fsspec-in-python))

- querySelector 사용 불가능 이슈 해결 (원인 : chromedriver 최신버전 설치)

```commandline
Missing optional dependency 'fsspec'. Use pip or conda to install fsspec.
```

```commandline
$ pip3.7 install fsspec
$ pip3.7 install tox tox-conda
```

---

## 2021-11-25

- 조달청 SSL 적용으로 인한 프로토콜 변경 (기존 : http => 변경 : https)
- webdriver-manager 모듈 설치 및 적용 (최신 버전 자동 업데이트)

```
$ pip3.7 install webdriver-manager
```

```python
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()

'''
driver = webdriver.Chrome(
    executable_path="driver/chromedriver.exe",
    options=options,
    service_args=["hide_console"]
)
'''

# 크롬 드라이버 관리자 : 2021-11-26
driver = webdriver.Chrome(
    ChromeDriverManager().install(),
    options=options,
    service_args=["hide_console"]
)
```

---

## 2021-11-26

- 버전 : 1.0.4(`/json`, `/images/` 폴더 포함시켜야 함)
- `pyinstaller` 빌드 후 엑셀 파일을 출력하는 부분에서 의존성 이슈 발생

```commandline
missing optional dependency 'fsspec'...
```

- 빌드 시 `hidden-import`를 해줌으로써 해결 가능

```commandline
$ pyinstaller --hidden-import fsspec -w --icon=images/icon.ico crawler.py
```

