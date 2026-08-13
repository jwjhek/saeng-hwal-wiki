---
publish: true
draft: false
depth: article
---

# Django Flask FastAPI 학습

> **분류:** 개발 › 프레임워크·DB · [[생활위키 목차]]

Python으로 **웹 사이트·REST API**를 만들 때 가장 많이 고르는 프레임워크가 **Django**, **Flask**, **FastAPI**다. 
세 개 모두 Python이지만 **철학·규모·실행 방식**이 달라서, 프로젝트 성격에 맞게 고르는 편이 낫다.

선수: [[Python 학습과 패키지]] — venv·pip·타입 힌트·HTTP 기초.  
Java 쪽과 비교하면 [[Spring과 Spring Boot 학습]].

공식:

- Django: [https://www.djangoproject.com](https://www.djangoproject.com)
- Flask: [https://flask.palletsprojects.com](https://flask.palletsprojects.com)
- FastAPI: [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com)

확인일: 2026-08-13  
예시는 **Python 3.10+** 기준이다. 버전·패키지 이름은 배포에 따라 조금 다를 수 있다.

---

## 1. 개요

| 프레임워크 | 한 줄 | 비유 |
|------------|------|------|
| **Django** | **풀스택** — ORM·관리자·인증·템플릿이 **한 세트** | Spring Boot + JPA + Thymeleaf + Admin에 가깝게 묶인 느낌 |
| **Flask** | **마이크로** — 라우팅·요청 처리 **골격**만, 나머지는 직접 고름 | Spring MVC 일부만 가져온 뒤 확장으로 조립 |
| **FastAPI** | **API 전용** — 타입 힌트·**OpenAPI**·비동기에 최적화 | JSON API·마이크로서비스·문서 자동 생성에 강함 |

```text
[클라이언트] 브라우저 / 앱 / 다른 서버
      ↓ HTTP
[Python 웹 프레임워크] Django / Flask / FastAPI
      ↓
[비즈니스 로직] 뷰·서비스·의존성
      ↓
[저장소] ORM·SQL·Redis·파일 …
```

---

## 2. 요약 비교

| 항목 | Django | Flask | FastAPI |
|------|--------|-------|---------|
| **규모** | 대형·풀스택 | 소형·마이크로 | 중형·API 중심 |
| **학습 곡선** | 규칙·구조가 많음 | 낮음, 대신 조립 책임 큼 | 중간 — 타입 힌트·async 익숙하면 빠름 |
| **ORM** | **내장**(Django ORM) | 없음 — SQLAlchemy 등 선택 | 없음 — SQLAlchemy 등 선택 |
| **관리자 UI** | **내장** Admin | 없음 | 없음 |
| **템플릿·SSR** | **내장** | Jinja2(기본) | 보통 JSON만 — 프론트 분리 |
| **API 문서** | DRF·수동·서드파티 | Swagger 플러그인 | **OpenAPI·Swagger UI 자동** |
| **비동기** | 3.x+ 점진 지원 | 제한적 | **ASGI·async 기본** |
| **실행** | WSGI/ASGI | WSGI(기본) | **ASGI**(uvicorn 등) |
| **적합** | CMS·관리 시스템·팀 규모 큰 웹 | 소규모·프로토타입·유연 조립 | REST·마이크로서비스·고성능 API |

「무조건 FastAPI」가 아니다. **서버 렌더링 HTML·관리 화면**이 크면 Django, **가볍게 한 파일**이면 Flask, **타입 안전 API**면 FastAPI가 자주 나온다.

### 2.1 Spring Boot와

둘 다 **웹 앱·API를 빨리 올리는 풀에 가까운 쪽**이다. 언어·생태계가 다르다.

| 항목 | Spring Boot | Django |
|------|-------------|--------|
| **언어** | Java (Kotlin도) | Python |
| **철학** | 의존성 주입·계층(컨트롤러·서비스·리포지토리). Boot가 **자동 구성** | **배터리 포함** — 모델·관리자·인증·템플릿이 한 세트 |
| **데이터** | JPA/Hibernate·MyBatis 등 **선택** | **내장 ORM** + 마이그레이션 |
| **화면** | Thymeleaf·별도 프론트. API면 JSON | **템플릿 내장**. Admin UI **기본** |
| **실행** | 내장 Tomcat 등, `jar` | `runserver` / gunicorn 등 |
| **현장** | 공공·대기업 Java SI ([[전자정부프레임워크]]) | 스타트업·CMS·Python 팀, 관리 화면이 클 때 |
| **성능·타입** | 정적 타입·JVM. 기동은 상대적으로 무거움 | 동적 타입. 기동·프로토타입은 가벼운 편 |
| **가까운 짝** | Boot ≈ Django보다 **조립형**. JPA+시큐리티+MVC를 직접 붙임 | Django ≈ Boot+JPA+화면+Admin을 **처음부터 묶은** 느낌 |

같은 「사이트 하나」라도 Java 공고·전자정부는 **Spring Boot**, Python·관리자 페이지 빨리면 **Django**가 자주 나온다.  
API만 작고 빠르게면 Python은 FastAPI, Java는 Boot + Web 만으로도 간다.

상세: [[Spring과 Spring Boot 학습]]

---

## 3. 공통 개념 — WSGI와 ASGI

| | WSGI | ASGI |
|--|------|------|
| 역할 | 동기 HTTP 앱 **표준 인터페이스** | **비동기**·WebSocket·HTTP/2 지원 |
| 대표 서버 | gunicorn, uwsgi | **uvicorn**, hypercorn |
| 프레임워크 | Flask(기본), Django(전통) | **FastAPI**, Django 4+ ASGI |

로컬 개발:

```bash
# Flask
flask --app app run

# Django
python manage.py runserver

# FastAPI
uvicorn main:app --reload
```

운영은 보통 **리버스 프록시**(nginx 등) 뒤에 WSGI/ASGI 워커를 둔다 → [[Docker 사용법]].

---

## 4. Django

### 4.1 철학

**「배터리 포함」** — URL·뷰·모델·마이그레이션·관리자·인증·세션·폼·캐시 등을 **프로젝트 구조 안에** 정해 준다. 
규칙이 많아서 **팀·장기 유지보수**에 유리한 경우가 많다.

### 4.2 구조 (MVT)

| 계층 | Django 이름 | 역할 |
|------|-------------|------|
| URL | `urls.py` | 경로 → 뷰 연결 |
| 로직 | **View** | 요청 처리 |
| 데이터 | **Model** | ORM — DB 테이블 매핑 |
| 화면 | **Template** | HTML 렌더링 |

Spring MVC의 Controller·Entity·View와 **대응** 관계로 보면 이해가 빠르다.

### 4.3 시작하기

```bash
python -m venv .venv
.venv\Scripts\activate
pip install django
django-admin startproject mysite
cd mysite
python manage.py startapp polls
python manage.py migrate
python manage.py runserver
```

`settings.py` — DB·앱 등록·미들웨어·보안. **한 파일에 설정이 모이는** 편이라 처음엔 길어 보인다.

### 4.4 강점·주의

| 강점 | 주의 |
|------|------|
| **Admin** — 모델 등록만으로 CRUD 화면 | 프레임워크 **관습**에 맞춰야 함 |
| **ORM·마이그레이션** 일체화 | 단순 API만 필요하면 **무겁게** 느껴질 수 있음 |
| 인증·권한·세션 **내장** | 비동기·초고속 API는 Flask/FastAPI 대비 선택지가 다름 |
| **Django REST framework(DRF)** — API 확장 | DRF는 **별도 학습** 곡선 |

REST API만 필요하고 Admin이 필요 없으면 **FastAPI**를 같이 검토한다.

---

## 5. Flask

### 5.1 철학

**마이크로 프레임워크** — 라우팅·요청·응답 **최소 코어**. 
DB·인증·폼·마이그레이션은 **Flask-SQLAlchemy**, **Flask-Login**, **Flask-Migrate** 등 **확장**으로 붙인다.

### 5.2 구조

```text
app.py (또는 factory)
 ├── @app.route / Blueprint
 ├── 뷰 함수
 └── (선택) SQLAlchemy, Jinja2 템플릿
```

**Blueprint** — URL·뷰를 **모듈별로 분리**(Spring의 `@RequestMapping` 묶음과 비슷한 역할).

### 5.3 최소 예

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/items/<int:item_id>")
def read_item(item_id: int):
    return jsonify({"id": item_id})
```

```bash
pip install flask
flask --app app run --debug
```

### 5.4 강점·주의

| 강점 | 주의 |
|------|------|
| **가볍고 자유도** 높음 | 구조를 **팀이 직접** 정해야 함 |
| 한 파일 프로토타입에 최적 | 커지면 **폴더·패턴** 없으면 스파게티 |
| 확장 생태계 풍부 | 확장 조합마다 **버전 호환** 확인 |
| WSGI 배포 경험 많음 | 대규모 **비동기 I/O**는 FastAPI 쪽이 유리한 경우 많음 |

「Flask로 시작 → 규모 커지면 Django로 이전」보다, 처음부터 **요구사항**으로 고르는 편이 낫다.

---

## 6. FastAPI

### 6.1 철학

**타입 힌트 기반 API** — Pydantic으로 **요청·응답 검증**, **OpenAPI(Swagger)** 스키마·UI **자동 생성**. 
**Starlette** + **uvicorn**(ASGI) 위에서 동작한다.

### 6.2 구조

```text
main.py
 ├── FastAPI() 앱
 ├── 경로 함수 (@app.get / post …)
 ├── Pydantic BaseModel (스키마)
 └── Depends() — 의존성 주입
```

`Depends()`는 Spring의 **생성자 주입·@Autowired**와 비슷한 **의존성 주입** 패턴이다.

### 6.3 최소 예

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"id": item_id}

@app.post("/items")
async def create_item(item: Item):
    return item
```

```bash
pip install "fastapi[standard]"
uvicorn main:app --reload
```

브라우저에서 `/docs` — **Swagger UI**, `/redoc` — ReDoc.

### 6.4 강점·주의

| 강점 | 주의 |
|------|------|
| **자동 API 문서** | HTML **서버 렌더링**은 주 목적이 아님 |
| 타입·검증·에디터 지원 좋음 | `async`·이벤트 루프 이해 필요할 때 있음 |
| 성능·동시성에 유리한 편 | ORM은 **SQLAlchemy** 등 **별도** 선택 |
| 프론트 분리(SPA·모바일)와 궁합 | Admin·CMS는 Django 대비 직접 만들거나 서드파티 |

[[Python 학습과 패키지]] §17과 같은 예시다. 여기서는 **프레임워크 선택·구조**까지 확장한다.

---

## 7. 무엇을 고를까

| 상황 | 추천 방향 |
|------|-----------|
| **관리자·게시판·사내 업무 웹** + ORM·권한 일체 | **Django** |
| **소규모 API·스크립트 확장·학습용** 한 파일 | **Flask** |
| **REST·OpenAPI·모바일 백엔드·마이크로서비스** | **FastAPI** |
| 팀이 **Java Spring**에 익숙, 엔터프라이즈 규칙 | Django 또는 [[Spring과 Spring Boot 학습]] |
| **프론트는 React/Vue**, 백은 JSON만 | **FastAPI** (또는 Django + DRF) |
| **레거시 WSGI** 호스팅만 가능 | Flask·Django 우선 검토 |

혼합도 흔하다: **Django(메인 웹) + FastAPI(고속 API 서비스)** 를 서비스별로 나누기.

---

## 8. 학습 순서 (4주 예)

**Week 1 — 공통**  
[[Python 학습과 패키지]] 복습 — venv, pip, HTTP, JSON, 타입 힌트.  
curl·브라우저로 GET/POST 확인.

**Week 2 — Flask**  
라우팅·Blueprint·Jinja2 또는 JSON API 하나.  
Flask-SQLAlchemy로 SQLite CRUD.

**Week 3 — FastAPI**  
Pydantic 모델·`Depends`·`/docs` 확인.  
uvicorn으로 배포 구조 익히기.

**Week 4 — Django**  
`startproject` → Model → migrate → Admin 등록 → 간단 뷰.  
(시간 있으면 DRF로 API 한 엔드포인트)

막히면 [[Cursor 사용법]]·[[VS Code 사용법]]으로 코드 설명을 묻되, **요청이 어느 파일을 타는지** 직접 따라가 본다.

---

## 9. 자주 쓰는 패키지

| 목적 | Django | Flask | FastAPI |
|------|--------|-------|---------|
| ORM | 내장 ORM | Flask-SQLAlchemy | SQLAlchemy 2.x |
| API | djangorestframework | flask-restx 등 | (내장 스타일) |
| 인증 | 내장 + allauth 등 | Flask-Login | OAuth2·JWT 라이브러리 |
| 테스트 | `TestCase` | pytest + client | `TestClient` |
| 배포 | gunicorn + nginx | gunicorn | uvicorn + nginx |

DB 튜닝·Oracle은 [[Oracle DB와 튜닝]] · [[DBeaver 사용법]]. 컨테이너는 [[Docker 사용법]].

---

## 10. 흔한 실수

| 실수 | 현실 |
|------|------|
| FastAPI만 배워 Django Admin 기대 | Admin은 **Django 전용** |
| Flask에 모든 걸 한 파일 | Blueprint·팩토리 패턴으로 **분리** |
| `runserver`/`--reload`를 운영에 | 개발 전용 — **gunicorn/uvicorn** 워커 |
| 타입 힌트 없이 FastAPI | 검증·문서 이점이 **줄어듦** |
| ORM N+1·마이그레이션 무시 | Django·SQLAlchemy 모두 **쿼리·스키마** 점검 필요 |
| 시크릿 키·DB URL을 Git에 | 환경 변수·`.env`(gitignore) — [[Git 사용법]] |

---

## 11. 정리

1. **Django** = 풀스택·Admin·ORM·팀 규칙.  
2. **Flask** = 가벼운 골격·자유 조립·프로토타입.  
3. **FastAPI** = 타입·OpenAPI·비동기 API.  
4. 실행은 **WSGI(Flask·Django)** vs **ASGI(FastAPI)** 구분.  
5. 선수는 [[Python 학습과 패키지]], Java 비교는 [[Spring과 Spring Boot 학습]].

---

## 면책

> **면책**  
> 학습·기술 선택 참고용이다. **프레임워크·보안·배포 표준**은 팀·프로젝트·규제에 따른다.  
> 버전·패키지 API는 공식 문서가 최종본이다.

---

## 관련

- [[Python 학습과 패키지]] — 언어·venv·웹 패키지 표
- [[Spring과 Spring Boot 학습]] — Java 웹과 역할 비교
- [[전자정부프레임워크]] — 공공 Java 웹 (Python과 별축)
- [[Docker 사용법]] — 컨테이너 배포
- [[Git 사용법]] — 버전 관리·비밀 제외
- [[Playwright]] — E2E (API와 별도)
- [[VS Code 사용법]] · [[Cursor 사용법]]
- [[생활위키 목차]]
