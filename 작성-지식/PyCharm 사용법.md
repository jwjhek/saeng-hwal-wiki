---
publish: true
draft: false
depth: article
aliases:
  - PyCharm
  - JetBrains PyCharm
---

# PyCharm 사용법

> **분류:** 작성·지식 › 에디터·IDE · [[생활위키 목차]]

**PyCharm**은 JetBrains의 **Python 전용 IDE**다. 편집·실행·디버그·테스트·가상환경이 한 창에 붙어 있다. 문법은 [[Python 학습과 패키지]], 웹은 [[Django Flask FastAPI 학습]]을 본다. 파이썬 도구 전체 지도는 [[파이썬 개발 툴]]. 이 글은 **설치·인터프리터·무료/Pro·다른 에디터와의 자리**만 정리한다.

제품: [https://www.jetbrains.com/pycharm/](https://www.jetbrains.com/pycharm/)  
도움말: [https://www.jetbrains.com/help/pycharm/](https://www.jetbrains.com/help/pycharm/)

확인일: 2026-08-14  
메뉴·단축키·무료 범위는 **버전(2025.3 이후 통합 제품)** 마다 조금 다를 수 있다.

관련: [[파이썬 개발 툴]] · [[Python 학습과 패키지]] · [[VS Code 사용법]] · [[Cursor 사용법]]

---

## 1. 개요

| 항목 | 설명 |
|------|------|
| **무엇** | Python 코드용 통합 개발 환경 (IntelliJ 플랫폼) |
| **무엇이 아님** | 언어 교재, [[Jupyter 노트북]]만 쓰는 클라우드 사이트, Java eGov IDE([[Eclipse 사용법]]) |
| **형제** | IntelliJ IDEA(Java 중심), DataGrip(DB), Android Studio도 같은 계열 UI |
| **Windows** | 아래 단축키는 `Ctrl` 기준. macOS는 대개 `Cmd` |

```text
폴더(프로젝트)
  → 인터프리터 (venv · conda · uv · 시스템 Python)
  → 편집 · 실행 · 디버그 · pytest
  → Git · 터미널
```

가벼운 스크립트·위키 편집은 [[VS Code 사용법]] / [[Cursor 사용법]]이 가벼운 경우가 많다. **큰 Python 저장소·리팩터·디버그**는 PyCharm이 편한 사람이 많다. **병행**해도 된다.

---

## 2. 무료 핵심과 Pro

예전에는 **Community / Professional** 설치 파일이 둘이었다. **2025.1부터 설치본이 하나**(unified)다.

| | **핵심 (무료로 남는 쪽)** | **Pro 구독** |
|--|---------------------------|--------------|
| 편집·실행·디버그 | Python 인스펙션, 리팩터, pytest | 같음 + 웹·원격이 두꺼움 |
| Jupyter | **기본 노트북** 실행·편집 (통합 이후 핵심에 포함) → [[Jupyter 노트북]] | 원격 노트북, SQL 셀 등 **고급** |
| 웹 | 일반 Python 파일 | **Django·Flask·FastAPI** 안내·엔드포인트 탐색 등 |
| DB | 없음에 가까움 → [[DBeaver 사용법]] | DataGrip 엔진 **내장** |
| 원격 | 로컬이 기본 | SSH·[[Docker 사용법]]·WSL 인터프리터 등 |

설치하면 **Pro 체험(약 30일)** 이 붙는 안내가 흔하다. 끝나면 핵심만 쓰거나 구독한다. **구독 권유가 아니다.** 회사 PC는 **지정 라이선스·반입**이 우선.

웹에 남은 「Community 설치 vs Professional 설치」글은 **옛 파일 이름**일 수 있다. 지금 받는 화면의 **무료/Pro 구분**을 본다.

---

## 3. 설치·첫 실행

1. 공식 사이트 또는 **JetBrains Toolbox**로 설치. Toolbox는 버전 여러 개를 같이 두기 쉽다.  
   Toolbox: [https://www.jetbrains.com/toolbox-app/](https://www.jetbrains.com/toolbox-app/)  
2. `winget search pycharm` 도 있다. **패키지 ID는 검색 결과**를 따른다.  
3. 실행 → **프로젝트 폴더**를 연다 (`Open`). 빈 폴더면 `New Project`.  
4. **Python 인터프리터**를 고른다. 이게 안 맞으면 빨간 물결·실행 실패의 대부분이다.

회사 PC: 오프라인 설치·프록시·Toolbox 금지 여부를 먼저 본다.

프로젝트 루트에 `.idea/` 가 생긴다. **팀 공유 여부는 팀 규칙**. 개인 경로·키는 Git에 넣지 않는다 → [[Git 사용법]].

---

## 4. 인터프리터 · 가상환경

Python은 **환경마다 패키지가 다르다**. IDE가 보는 인터프리터 ≠ 터미널 `python` 인 경우가 많다.

| 방식 | 언제 |
|------|------|
| **venv** | 학습·대부분의 앱. [[Python 학습과 패키지]] 기본 |
| **conda** | 데이터·과학, 바이너리 의존 |
| **uv** | 2025.3 전후, 시스템에 `uv`가 있으면 마법사가 **기본으로 권하는** 경우 |
| 시스템 Python | 연습만. 패키지를 전역에 쌓지 말 것 |

설정 위치(이름 검색): `Settings` → `Python Interpreter`  
상태바 오른쪽의 인터프리터 이름 클릭으로도 바뀐다.

확인:

- 터미널 패널에서 `python -c "import sys; print(sys.executable)"`  
- 실행 구성(Run Configuration)의 interpreter가 **같은 경로**인지  

패키지는 IDE 터미널에서 `pip` / `uv` / `conda`로 깔거나, 인터프리터 화면의 패키지 목록을 쓴다. **프로젝트 venv 밖**에 깔면 「터미널에선 되는데 IDE에선 모듈 없음」이 난다.

---

## 5. 실행 · 디버그 · 테스트

| 동작 | 흔한 방법 |
|------|-----------|
| 현재 파일 실행 | `Shift + F10` 또는 거터(줄번호 옆) 초록 화살표 |
| 디버그 | 줄 번호 클릭으로 **중단점** → `Shift + F9` |
| 실행 구성 | 오른쪽 위 드롭다운. 스크립트·모듈·pytest·Django `manage.py` 등 |
| 테스트 | `pytest` 파일·함수 옆 아이콘. 통과/실패가 **테스트 도구 창** |

`main` 가드:

```python
if __name__ == "__main__":
    ...
```

FastAPI·Flask는 **uvicorn / flask run** 구성을 쓰거나 터미널에서 띄운다. Pro면 프레임워크 실행 구성이 더 친절한 경우가 많다 → [[Django Flask FastAPI 학습]].

디버그는 `print` 남발보다 **중단점 + Variables**가 빠르다.

---

## 6. 자주 쓰는 단축키

명령이 기억 안 나면 `Ctrl + Shift + A` (**Find Action**)에 한글·영어 키워드를 친다. `Double Shift`는 **전체 검색**(파일·클래스·액션).

| 키 | 하는 일 |
|----|---------|
| `Ctrl + Shift + N` | 파일 이름으로 열기 |
| `Ctrl + Shift + F` | 폴더 안 문자열 검색 |
| `Ctrl + B` | 정의로 이동 |
| `Alt + Enter` | 빠른 수정(인텐션) |
| `Ctrl + /` | 줄 주석 |
| `Ctrl + Alt + L` | 서식 (키 충돌 시 Settings에서 확인) |
| `Ctrl + Shift + F12` | 도구 창 숨김/복원 (코드만 보기) |
| `Alt + F12` | 터미널 |

키맵을 **VS Code**로 바꿀 수 있다. 팀 온보딩·Cursor와 손을 맞출 때 쓴다. JetBrains 기본에 익숙해지면 블로그 단축키가 바로 맞다.

---

## 7. Git · 비밀 · AI

| 항목 | 메모 |
|------|------|
| Git | 왼쪽 **Git** 도구 창. 커밋 전 diff. 원리는 [[Git 사용법]] |
| `.env` · 키 | 실행 구성 환경 변수 또는 로컬 파일. **저장소·채팅에 붙이지 말 것** → [[API]] · [[Bitwarden 사용법]] |
| JetBrains AI | 제품 안 어시스턴트·크레딧. [[Cursor 사용법]]·[[GitHub Copilot 사용법]]과 **구독이 별개** |
| 위키 `.md` | 마크다운 위키는 Cursor/VS Code가 폴더 편집에 맞음 |

「AI가 없는 함수를 만들어 준다」는 [[바이브 코딩]]의 환각과 같다. 실행·테스트로 확인한다.

---

## 8. 다른 도구와 비교

구매 권유가 아니다.

| | PyCharm | [[VS Code 사용법]] / [[Cursor 사용법]] | [[Eclipse 사용법]] |
|--|---------|----------------------------------------|-------------------|
| 주 언어 | **Python** | 다언어. 확장을 붙임 | **Java**·eGov |
| Python DX | 인터프리터·리팩터가 **기본이 두꺼움** | Python·Pylance 확장 → [[VS Code 추천 확장]] | 주력이 아님 |
| AI 에이전트 | JetBrains AI (별도) | Cursor가 **에이전트**에 강함 | 플러그인 |
| 무게 | 무거움 | 가벼움 | 중간~무거움 |
| 이런 일 | Python 앱 | 위키·다언어·에이전트 | 공공 Java |

IntelliJ IDEA에 Python 플러그인을 얹는 구성은 **Java가 본업**일 때 흔하다. Python만 하면 PyCharm이 메뉴가 짧다.

DB만 보면 Pro 내장 vs [[DBeaver 사용법]]. 둘 다 쓰는 사람도 있다.

---

## 9. 막히면

| 증상 | 먼저 |
|------|------|
| `No module named …` | 인터프리터가 프로젝트 venv인지, 패키지를 **그 환경에** 깔았는지 |
| 실행은 되는데 터미널과 다름 | Run Configuration interpreter ≠ 터미널 `python` |
| 디버그가 안 붙음 | 중단점이 **실제로 실행되는 파일**인지, 원격/Docker면 Pro·경로 매핑 |
| 느림 | 제외 폴더(`venv`, `.git`, `node_modules`), 메모리, 플러그인 |
| 한글 경로 | 프로젝트·venv를 **ASCII에 가까운 경로**에 두는 편이 사고가 적다 |
| 체험 종료 후 메뉴가 없음 | 그 기능이 **Pro**인지. 핵심만 쓰거나 구독. 공식 비교표 |

인덱스가 이상하면 `File` → `Invalidate Caches` (저장 후). 자주 쓰지 말 것.

---

## 10. 정리

| 항목 | 한 줄 |
|------|--------|
| 정의 | JetBrains **Python IDE** |
| 라이선스 | 통합 설치. **핵심 무료** + **Pro** (웹·DB·원격 등) |
| 첫 단추 | 프로젝트 폴더 + **인터프리터 = venv** |
| 언어 | [[Python 학습과 패키지]] |
| 웹 | [[Django Flask FastAPI 학습]] |
| 가벼운 편집 | [[VS Code 사용법]] · [[Cursor 사용법]] |

---

## 면책

> **면책**
> - **유료 구독·특정 라이선스 권유가 아니다.**
> - 무료 범위·Pro 기능·가격·체험 일수는 **JetBrains가 바꾼다.** 설치 화면·[공식 도움말](https://www.jetbrains.com/help/pycharm/unified-pycharm.html)이 우선이다.
> - 회사·학교 PC는 **지정 IDE·라이선스·반입 정책**을 개인 설치보다 앞에 둔다.
> - 크랙·라이선스 우회는 다루지 않는다.

---

## 관련

- [[생활위키 목차]]
- [[파이썬 개발 툴]]
- [[Python 학습과 패키지]] · [[Jupyter 노트북]]
- [[Django Flask FastAPI 학습]]
- [[VS Code 사용법]]
- [[Cursor 사용법]]
- [[Eclipse 사용법]]
