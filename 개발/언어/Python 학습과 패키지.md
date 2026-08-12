---
publish: true
draft: false
---

# Python 학습과 주요 패키지

> **분류:** 개발 › 언어 · [[생활위키 목차]]

Python은 **문법이 단순하고 생태계가 넓은** 언어다. 
스크립트·자동화·데이터 분석·웹·AI([[현존 AI 비교]]의 API 클라이언트)까지 한 언어로 붙이기 쉽다.

공식: [https://www.python.org](https://www.python.org) 
문서: [https://docs.python.org](https://docs.python.org)

확인일: 2026-08-06 
예시는 **Python 3.10+** 기준이다. 3.8 이하·Python 2는 신규 학습에서 제외한다.

---

## 0. 학습 지도

```text
기초 문법·자료구조·함수·모듈
중급 OOP·예외·가상환경(venv·conda)·패키징
실무 pathlib·typing·테스트·비동기
패키지 데이터 / 웹 / 자동화 / AI
연계 Cursor·VS Code로 편집, NotebookLM으로 긴 문서 소화
```

도구: [[VS Code 사용법]] / [[Cursor 사용법]] + Python 확장, 터미널.

---

# Part 1 — 언어 기초

## 1. 설치와 실행

- Windows: python.org 설치 시 **Add to PATH** 체크, 또는 `winget install Python.Python.3.12` 등 
- 확인: `python --version` / `py -3 --version` 
- REPL: `python` 
- 파일 실행: `python app.py` 

패키지 관리: **pip** (기본), 프로젝트는 **venv**로 격리.  
데이터·과학·바이너리 의존이 많으면 **Anaconda / Miniconda (`conda`)** 도 자주 쓴다 → [[#8.1 Anaconda·Miniconda·conda]].

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
python -m pip install --upgrade pip
```

## 2. 문법 핵심

```python
# 변수·타입 (동적, 다만 type hint 권장)
name: str = "kim"
age: int = 30
pi: float = 3.14
ok: bool = True

# 제어
if age >= 18:
 print("adult")
elif age > 0:
 print("minor")
else:
 print("?")

for i in range(3):
 print(i)

while ok:
 break
```

- 들여쓰기 = 블록 (스페이스 4칸 관례) 
- 주석 `#`, docstring `"""..."""` 

## 3. 자료구조

| 타입 | 특징 | 예 |
|------|------|-----|
| `list` | 가변 순서 | `[1, 2]` |
| `tuple` | 불변 순서 | `(1, 2)` |
| `dict` | 키-값 | `{"a": 1}` |
| `set` | 중복 없음 | `{1, 2}` |
| `str` | 불변 문자열 | `"hi"` |

```python
nums = [1, 2, 3]
nums.append(4)
person = {"name": "kim", "age": 30}
print(person["name"], person.get("email", ""))

# 언패킹
a, b = (10, 20)
*rest, last = [1, 2, 3, 4]
```

컴프리헨션:

```python
squares = [x * x for x in range(5) if x % 2 == 0]
mapping = {x: x * x for x in range(3)}
```

## 4. 함수

```python
def add(a: int, b: int = 0) -> int:
 """합을 반환한다."""
 return a + b

def f(*args, **kwargs):
 ...

# 람다 (짧은 익명)
sorted(items, key=lambda x: x["score"], reverse=True)
```

- 기본 인수는 **불변 값**만 (list/dict를 기본값으로 두지 말 것) 
- `*args`, `**kwargs` 
- 타입 힌트는 실행을 안 바꾸지만, 가독성·도구(mypy/pyright)에 유리 

## 5. 모듈·패키지

```text
mypkg/
 __init__.py
 util.py
main.py
```

```python
from mypkg.util import helper
import json
from pathlib import Path
```

표준 라이브러리 자주 쓰는 것:

| 모듈 | 용도 |
|------|------|
| `pathlib` | 경로 |
| `json` | JSON |
| `re` | 정규식 |
| `datetime` | 날짜 |
| `collections` | deque, Counter, defaultdict |
| `itertools` | 이터레이터 도구 |
| `functools` | lru_cache, partial |
| `subprocess` | 외부 명령 |
| `logging` | 로그 (`print` 대신) |
| `argparse` / `typer`(외부) | CLI |
| `unittest` / `pytest`(외부) | 테스트 |
| `asyncio` | 비동기 |

## 6. 클래스 (OOP)

```python
class User:
 def __init__(self, name: str) -> None:
 self.name = name

 def greet(self) -> str:
 return f"hi {self.name}"

class Admin(User):
 def greet(self) -> str:
 return f"admin:{self.name}"
```

- `@dataclass` (3.7+): 데이터 담는 클래스 자동 생성 
- `@staticmethod` / `@classmethod` 
- 프로퍼티 `@property` 
- 다중 상속은 믹스인 정도로만 

```python
from dataclasses import dataclass

@dataclass
class Point:
 x: float
 y: float
```

## 7. 예외

```python
try:
 n = int("x")
except ValueError as e:
 logging.exception("parse fail: %s", e)
finally:
 ...

# 직접 정의
class NotFoundError(Exception):
 pass
```

컨텍스트 매니저:

```python
with open("a.txt", encoding="utf-8") as f:
 text = f.read()

with Path("a.txt").open(encoding="utf-8") as f:
 ...
```

경로·파일은 **`pathlib.Path`** 를 기본으로.

## 8. 가상환경·의존성

### 8.1 Anaconda·Miniconda·conda

**Anaconda**는 데이터 분석·과학 쪽에서 많이 쓰는 **배포판**이다.  
Python + **conda** 패키지 관리자 + (풀 설치 시) Jupyter·pandas 등 묶음이 함께 온다.

| 이름 | 내용 |
|------|------|
| **Anaconda Distribution** | 용량 큰 **풀 세트**. 처음 깔아 두면 분석 패키지가 많이 포함됨 |
| **Miniconda** | Python + **conda만** 최소 설치. 필요한 패키지만 직접 추가 (추천되는 경우가 많음) |
| **Miniforge / Mambaforge** 등 | conda-forge 중심의 경량 배포 (커뮤니티). `mamba`는 conda와 비슷하고 더 빠른 해결기로 알려짐 |
| **conda** | 환경 생성·패키지 설치 명령 (`conda create`, `conda install`) |
| **Anaconda Navigator** | GUI로 환경·Jupyter 실행 (풀 Anaconda에 포함되는 경우) |

공식: [https://www.anaconda.com](https://www.anaconda.com) · conda 문서: [https://docs.conda.io](https://docs.conda.io)

**언제 conda / Anaconda 쪽을 보나**

- numpy·scipy·pytorch 등 **바이너리·드라이버** 의존이 복잡할 때  
- 팀·강의·논문 재현이 **conda env** 기준일 때  
- Windows에서 과학 스택 설치가 pip만으로 자주 깨질 때  

**언제 pip + venv가 나은가**

- 웹·스크립트·일반 앱, `requirements.txt`만으로 충분한 프로젝트  
- Docker·CI가 pip 전제일 때  
- IDE·배포 파이프라인이 venv 기준일 때  

둘을 **같은 프로젝트에서 섞어 쓰면** 경로가 꼬이기 쉽다.  
한 프로젝트는 **venv+pip** 또는 **conda env** 중 하나로 통일한다.

#### conda 기본 흐름

```bash
# 환경 만들기 (Python 버전 지정 예)
conda create -n myenv python=3.12

# 활성화 (Anaconda Prompt / conda init 한 터미널)
conda activate myenv

# 패키지 설치 (채널은 defaults / conda-forge 등)
conda install pandas numpy jupyterlab
# 또는 conda-forge
conda install -c conda-forge pandas

# 목록·내보내기·재현
conda list
conda env export > environment.yml
conda env create -f environment.yml

# 비활성화·삭제
conda deactivate
conda env remove -n myenv
```

팁:

- Windows에서는 **Anaconda Prompt** 또는 `conda init powershell` 후 새 터미널을 연다.  
- VS Code / Cursor에서 인터프리터를 **해당 conda env**로 고른다 ([[VS Code 사용법]]).  
- conda 환경 안에 `pip install`도 가능하지만, **가능하면 conda로 맞추고**, 섞을 때는 순서를 문서화한다.  
- `base` 환경에 전부 설치하지 말고 **프로젝트별 env**를 만든다.  
- 용량·업데이트가 부담이면 **Miniconda**부터.

### 8.2 pip + venv (기본)

```bash
python -m venv .venv
.venv\Scripts\activate
pip install requests pandas
pip freeze > requirements.txt
pip install -r requirements.txt
```

### 8.3 도구 비교

| 도구 | 역할 |
|------|------|
| **pip + venv** | 기본, 어디에나 |
| **uv** | 빠른 pip/venv 대체 (인기↑) |
| **Poetry** / **PDM** | 의존성·빌드 메타데이터 |
| **conda** (Anaconda/Miniconda) | 데이터·과학·바이너리 의존, 환경 YAML 재현 |

프로젝트마다 가상환경을 새로 만드는 습관이 사고를 줄인다.

---

# Part 2 — 중급·실무 포인트

## 9. 이터러블·제너레이터

```python
def countdown(n: int):
 while n > 0:
 yield n
 n -= 1

for x in countdown(3):
 print(x)
```

대용량은 리스트에 다 올리지 말고 제너레이터·스트리밍.

## 10. 타입 힌트 확장

```python
from typing import Optional, Iterable
# 3.10+
def find(name: str) -> str | None:
 ...
```

`list[str]`, `dict[str, int]` (3.9+). 
프로토콜·TypedDict는 API 경계에 유용.

## 11. 비동기 (asyncio)

```python
import asyncio
import aiohttp # 외부

async def fetch(url: str) -> str:
 await asyncio.sleep(0.1)
 return url

async def main():
 await asyncio.gather(fetch("a"), fetch("b"))

asyncio.run(main())
```

I/O 대기가 많을 때. CPU 뭉텅이는 멀티프로세싱·별도 워커.

## 12. 테스트

```bash
pip install pytest
pytest -q
```

```python
def test_add():
 assert add(1, 2) == 3
```

## 13. 코딩 습관

| 권장 | 비권장 |
|------|--------|
| venv + requirements (또는 conda env + environment.yml) | 글로벌 pip·conda **base**에 전부 설치 |
| `logging` | 운영에서 `print`만 |
| `Path` | 문자열 경로 하드코딩 |
| 명시 인코딩 `utf-8` | 기본 인코딩 의존 (Windows) |
| 작은 함수·모듈 | 2000줄 스크립트 하나 |
| 시크릿은 환경변수 | 코드에 API 키 |

스타일: [PEP 8](https://peps.python.org/pep-0008/), 포매터 **Ruff** / Black, import 정렬.

---

# Part 3 — 주요 패키지

용도별로 **자주 쓰는 것**만. 설치는 `pip install 패키지명`.

## 14. 데이터 분석·수치

| 패키지 | 한 줄 |
|--------|------|
| **NumPy** | 다차원 배열·수치 연산의 기반 |
| **Pandas** | 표(DataFrame) 처리, CSV/엑셀, 그룹·조인 |
| **SciPy** | 과학·통계·최적화 알고리즘 |
| **Polars** | 빠른 DataFrame (Rust 기반, 대용량에 인기) |

```python
import pandas as pd

df = pd.read_csv("data.csv")
print(df.head())
print(df.groupby("city")["sales"].sum())
```

## 15. 시각화

| 패키지 | 한 줄 |
|--------|------|
| **Matplotlib** | 기본 플롯 |
| **Seaborn** | 통계 그래프 (Matplotlib 위) |
| **Plotly** | 인터랙티브 차트 |

## 16. 머신러닝·AI

| 패키지 | 한 줄 |
|--------|------|
| **scikit-learn** | 고전 ML (분류·회귀·클러스터링) |
| **PyTorch** | 딥러닝 연구·실무 강세 |
| **TensorFlow / Keras** | 딥러닝 또 다른 축 |
| **transformers** (Hugging Face) | 사전학습 NLP·비전 모델 |
| **openai** / 각 클라우드 SDK | LLM API 호출 |
| **langchain** / **llama-index** 등 | RAG·에이전트 오케스트레이션 (버전 변화 빠름) |

학습·실험은 Jupyter와 함께 쓰는 경우가 많다 (`jupyter`, `ipython`).

## 17. 웹·API

| 패키지 | 한 줄 |
|--------|------|
| **requests** | 동기 HTTP 클라이언트 (입문 필수) |
| **httpx** | 동기·비동기 HTTP |
| **Flask** | 가벼운 웹/API |
| **FastAPI** | 타입힌트 기반 API, OpenAPI 자동, 속도·DX 좋음 |
| **Django** | 풀스택·관리자·ORM 포함 대형 웹 |
| **Starlette** / **uvicorn** | ASGI·FastAPI 하단 |

```python
import requests
r = requests.get("https://httpbin.org/get", timeout=10)
r.raise_for_status()
data = r.json()
```

```python
# FastAPI
from fastapi import FastAPI
app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: int):
 return {"id": item_id}
```

Java/Spring 쪽과 역할이 겹치면 [[Spring과 Spring Boot 학습]]과 비교해 보면 된다 (정적타입·엔터프라이즈 vs 빠른 프로토타입).

## 18. 자동화·스크래핑·파일

| 패키지 | 한 줄 |
|--------|------|
| **BeautifulSoup** (`bs4`) | HTML 파싱 |
| **Scrapy** | 대규모 크롤링 프레임워크 |
| **Selenium** / **Playwright** | 브라우저 자동화 |
| **openpyxl** / **xlsxwriter** | 엑셀 |
| **python-docx** | 워드 |
| **Pillow (PIL)** | 이미지 |
| **PyPDF2** / **pypdf** | PDF |
| **rich** | 터미널 예쁜 출력 |
| **tqdm** | 진행률 바 |
| **click** / **typer** | CLI |

웹 스크래핑은 **이용약관·robots·저작권·개인정보**를 지킨다.

## 19. DB·저장

| 패키지 | 한 줄 |
|--------|------|
| **sqlite3** | 표준 라이브러리 내장 DB |
| **SQLAlchemy** | ORM·SQL 툴킷 |
| **psycopg** / **psycopg2** | PostgreSQL |
| **oracledb** (구 cx_Oracle) | Oracle — [[Oracle DB와 튜닝]]과 연계 |
| **pymysql** / **mysqlclient** | MySQL |
| **redis** | Redis 클라이언트 |
| **pymongo** | MongoDB |

## 20. 품질·도구

| 패키지/도구 | 한 줄 |
|-------------|------|
| **pytest** | 테스트 |
| **Ruff** | 린트+포맷 빠름 |
| **mypy** / **pyright** | 정적 타입 검사 |
| **black** | 포매터 (Ruff로 대체하는 팀↑) |
| **pre-commit** | 커밋 전 훅 |
| **python-dotenv** | `.env` 로드 |

## 21. 패키지 고르는

```text
표 데이터 빨리 → pandas (또는 polars)
숫자·행렬 → numpy
HTTP 한두 번 → requests
API 서버 새로 → FastAPI
전통 풀스택 웹 → Django
브라우저 클릭 자동화 → Playwright
LLM API → 공식 SDK + 필요 시 오케스트레이션 라이브러리
엑셀 보고 → pandas + openpyxl
```

의존성은 **필요할 때만**. `requirements.txt`가 수백 개면 설치·보안 감사 비용이 커진다.

---

# Part 3 — 로드맵

## 22. 주차별 제안

**1주** — 문법, list/dict, 함수, venv(또는 conda env), `pathlib`, `requests`로 API 하나 호출 

**2주** — 클래스, 예외, pytest, CSV 읽기 (`csv` 또는 pandas) 

**3주** — pandas 기초 집계 + matplotlib 그래프 하나 

**4주** — FastAPI로 CRUD 뼈대 또는 업무 폴더 자동화 스크립트 

**이후** — DB(SQLAlchemy), 비동기, ML 입문(sklearn), AI API 

## 23. Java와 비교

| | Python | Java ([[Java 언어 학습]]) |
|--|--------|---------------------------|
| 타입 | 동적 + 힌트 | 정적 강제 |
| 배포 | 스크립트·venv | JVM·빌드 산출물 |
| 웹 | FastAPI/Django | Spring |
| 공공 SI | 자동화·분석·AI에 많음 | eGov·기간계에 많음 |
| 속도 | 대체로 느림 (병목은 C확장·벡터화로) | 대체로 빠름 |

둘 다 할 줄 알면 **분석·자동화는 Python, 대형 백엔드는 Java/Spring** 조합이 흔하다.

## 24. 체크리스트

- [ ] venv 활성화 후 pip 설치 (또는 conda env + `conda install`)  
- [ ] Anaconda를 쓰면 **base에 몰아넣지 않고** 프로젝트 env를 쓰는지  
- [ ] `if __name__ == "__main__":` 진입점 
- [ ] 파일은 UTF-8 
- [ ] 예외·로그 
- [ ] requirements / `environment.yml` 고정 
- [ ] 시크릿 미포함 
- [ ] 타입 힌트를 함수 시그니처에 

---

## 관련

- [[생활위키 목차]]
- [[Java 언어 학습]]
- [[Spring과 Spring Boot 학습]]
- [[Oracle DB와 튜닝]]
- [[현존 AI 비교]]
- [[Cursor 사용법]]
- [[VS Code 사용법]]
- [[NotebookLM 사용법]]
