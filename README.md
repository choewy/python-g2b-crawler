# crwaler

---

## 1. 개요

>   (1) Title
>   - 나라장터 입찰정보 수집 프로그램

>   (2) Description
>   - UI를 통해 입찰공고 및 사전규격에 해당하는 설정하여 검색어에 해당하는 검색 결과 중 제외어에 해당하는 내용을 삭제 후 엑셀 파일로 출력하는 프로그램

>   (3) Version
> 
>   - 1.0.1(삭제)
>
>   - 1.0.2(삭제)
> 
>   - 1.0.3(현재) : 전체적인 UI 구성 변경 및 오류 수정

>   (4) Lib
>   
>   - `$ pip install pandas==1.0.5`
> 
>   - `$ pip install openpyxl`
> 
>   - `$ pip install pyqt5==5.15.0`
> 
>   - `$ pip install pyinstaller==3.6`
> 
>   - `$ pip install selenium==3.141.0`

>   (5) Build
> 
>   - `$ pyinstaller -w --icon="venv/icon.ico" -p "venv/_dllFiles" crawler.py`

---

## 2. 작업이력

### 2.1.  2021-03-05(금)

>   (1) 윈도우 화면 구성
> 
>   - 전체적인 화면 구성

>   (2) 위젯 탭 구성
>
>   - 입찰공고 및 사전규격 검색을 위한 UI 구성

>   (3) 키워드 관리 탭 구성
> 
>   - 검색어 및 제외어 입력/수정/삭제를 위한 UI 구성

>   (4) 검색 기능 구현
>
>   - 다중 쓰레드를 사용한 사전규격 정보 수집 기능 구현 
> 
>   - 다중 쓰레드를 사용한 입찰공고 정보 수집 기능 구현
> 
>   - 단, 사전규격 정보 수집 중 가격 정보에 해당하는 Element는 검토가 필요하며, 입찰 공고 정보 수집 중 가격 정보에 해당하는 Element는 규칙을 찾아내야 함.

### 2.2. 2021-03-06(토) ~ 07(일)

>   (1) 시스템 점검으로 인한 작업 불가능
> 
>   - 점검 기간 : 2021.03.05(금) 20:00 ~ 2021.03.07(일) 20:00

### 2.3. 2021-03-08(월)

>   (1) Element 검토
> 
>   - 검색 키워드별 수집되는 사전규격 및 입찰공고 정보에 해당하는 `tb_inner`의 수량 파악 후 규칙 검토
>
>   - 검토 결과 : 입찰공고에서의 코드 제거(적용 불가능)
>
>   (2) 전체 기능 검토
> 
>   - 입찰공고 시 약 600초, 사전규격 시 약 750초

### 2.4. 2021-03-09(화)

>   (1) Build : 1.0.3 버전 Build 및 Github Commit
> 
>   (2) Command 숨김처리
> 
>   - `\venv\Lib\site-packages\selenium\webdriver\common\service.py`
> 
>   - 속성(`creationflags=0x08000000`) 추가
> 
> ```python
> self.process = subprocess.Popen(cmd, env=self.env,
>                                 close_fds=platform.system() != 'Windows',
>                                 stdout=self.log_file,
>                                 stderr=self.log_file,
>                                 stdin=PIPE,
>                                 creationflags=0x08000000)
> ```
