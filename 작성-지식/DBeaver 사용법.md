---
publish: true
draft: false
---

# DBeaver 사용법

> **분류:** 작성·지식 › 에디터·IDE · [[생활위키 목차]]

DBeaver는 **여러 DBMS를 한 UI에서** 다루는 데이터베이스 클라이언트다.  
Oracle·PostgreSQL·MySQL·SQL Server·SQLite 등에 접속해 SQL 실행·스키마 탐색·데이터 편집·내보내기를 한다.

커뮤니티 에디션(CE)은 무료 오픈소스 비중이 크고, 기업용(EE/Lite 등)은 유료 기능이 있다.  
이 글은 **DBeaver Community** 감각 위주.

공식: [https://dbeaver.io](https://dbeaver.io)  
다운로드: [https://dbeaver.io/download/](https://dbeaver.io/download/)

확인일: 2026-08-07  
UI 메뉴 이름은 버전에 따라 조금 다를 수 있다.

관련 DB 학습: [[Oracle DB와 튜닝]] · 에디터: [[VS Code 사용법]] (SQLTools는 가벼운 대안)

---

## 1. 왜 쓰나

| 상황 | DBeaver |
|------|---------|
| DB마다 전용 툴이 다름 | 접속만 바꾸면 같은 습관 |
| 스키마·테이블 클릭 탐색 | 트리 + 데이터 그리드 |
| SQL 작성·실행·결과 비교 | SQL 에디터·여러 탭 |
| CSV/Excel 뽑기 | Export 마법사 |
| ER 다이어그램 | 자동 생성(버전·드라이버에 따라) |

SQL*Plus·sqlcl만으로도 되지만, **조회·조인 결과 확인·메타데이터**는 GUI가 빠른 경우가 많다.  
무거운 IDE(DataGrip) 대용으로 CE를 쓰는 사람이 많다.

---

## 2. 설치 (Windows)

1. 공식에서 **Windows Installer** (또는 Zip)  
2. 실행 후 워크스페이스(설정·접속 정보 저장 위치) 지정  
3. 첫 실행 시 샘플·팁 창은 취향껏  

JDK: 최근 배포본은 런타임을 포함하는 경우가 많다.  
회사 PC는 반입 정책·프록시를 확인한다.

macOS/Linux도 공식 패키지. 원격은 SSH 터널·클라우드 SQL과 조합.

---

## 3. 접속 만들기

1. 데이터베이스 아이콘 **새 연결** (플러그 모양)  
2. DBMS 선택 (Oracle, PostgreSQL, …)  
3. 호스트·포트·DB/서비스명·사용자·암호  
4. **드라이버 다운로드** 안내가 뜨면 허용 (최초 1회)  
5. **연결 테스트** → 완료  

### Oracle 예 (감각)

| 항목 | 예 |
|------|-----|
| Host | DB 서버 |
| Port | `1521` (환경마다) |
| Database/Service | 서비스명 또는 SID (라디오 구분) |
| User / Password | 계정 |

TNS·지갑(Wallet)·SSL은 연결 설정 탭·드라이버 속성에서.  
사내 표준이 SQL Developer면 접속 문자열을 그대로 옮겨 본다. → [[Oracle DB와 튜닝]]

### 보안

- 암호를 OS 자격 증명 저장소에 둘지 선택  
- 운영 DB는 **읽기 전용 계정** 권장  
- 연결 정보는 Git에 커밋하지 말 것 (`.dbeaver` 폴더 주의)

---

## 4. 화면 구조

```text
┌─────────────┬──────────────────────────┐
│ 데이터베이스 │  SQL 에디터 / 데이터 탭  │
│ 네비게이터   │  결과 그리드             │
│ (연결·스키마)│  실행 로그               │
└─────────────┴──────────────────────────┘
```

| 영역 | 하는 일 |
|------|---------|
| **Navigator** | 연결·스키마·테이블·뷰·프로시저 |
| **SQL Editor** | 스크립트 작성·실행 |
| **Data** | 테이블 내용 그리드 조회·편집 |
| **Output / Log** | 메시지·실행 시간 |

테이블 더블클릭 → 데이터, 우클릭 → 보기 SQL·내보내기·ER 등.

---

## 5. SQL 실행

1. `SQL 편집기` → 새 스크립트 (또는 `Ctrl` + `]`)  
2. 상단에서 **어느 연결/스키마**인지 확인  
3. 실행:  
   - 현재 문장 / 스크립트 전체 (툴바 재생 버튼)  
   - 단축키는 `Ctrl` + `Enter` 계열이 흔함 (키맵·버전 확인)  

팁:

- 여러 문장은 `;` 또는 Oracle이면 `/` 습관에 맞춤  
- **바인드 변수**·파라미터 프롬프트 지원  
- 결과 탭을 여러 개 두고 비교  
- 실행 계획: DBMS별 `Explain` 메뉴 (Oracle이면 실행 계획 뷰)

실수로 `UPDATE`/`DELETE` 없이 WHERE — 운영에선 읽기 계정·트랜잭션 확인.

---

## 6. 데이터 보기·편집

- 필터·정렬·행 수 제한(페이지)으로 대용량 조심  
- 셀 편집 후 **저장** — Auto-commit이 꺼져 있으면 **Commit**까지 해야 DB에 반영  
- 대용량 SELECT는 클라이언트·네트워크를 죽일 수 있다 → `ROWNUM`/`FETCH FIRST`·샘플  

트랜잭션 모드는 아래 §7.

---

## 7. Auto-commit 해제 (Manual commit)

**Auto-commit On**이면 `UPDATE`/`DELETE`/`INSERT`·그리드 저장이 **문장마다 바로 확정**되고 Rollback이 어렵다.  
운영·실습 모두 **끄고(Manual commit)** Commit/Rollback을 직접 누르는 습관을 권장한다.

공식 문서: [Transaction mode](https://dbeaver.com/docs/dbeaver/Auto-and-Manual-Commit-Modes/)

### 7.1 지금 세션에서만 끄기 (빠른 방법)

SQL 에디터 또는 데이터 에디터 **툴바**에서:

1. **Auto** / **Auto-commit** 표시를 찾는다 (연결·트랜잭션 관련 드롭다운)  
2. **Manual commit**(수동 커밋)으로 바꾼다  
3. 이후 변경은 **Commit**으로 확정, **Rollback**으로 취소  

주의: 툴바에서만 바꾼 값은 **재접속·재시작 후 기본값으로 돌아갈 수** 있다.  
항상 끄려면 §7.2처럼 **연결 설정에 저장**한다.

### 7.2 연결마다 기본값을 Manual로 (권장·영구)

1. Database Navigator에서 해당 연결 **우클릭**  
2. **Edit Connection**(연결 편집)  
3. **Connection settings** → **Initialization**(초기화)  
4. 트랜잭션/Auto-commit 관련 항목에서  
   - **Manual commit** 선택  
   - 또는 Auto-commit 체크 **해제** (UI 문구는 버전마다 `Auto-commit` / `Default` / `Manual commit` 등)  
5. **OK** 후 **재접속**  

`Default`로 두면 **Connection type**(개발/테스트/운영)의 기본값을 따른다 → §7.3.

같은 화면의 **Transactions** 쪽에서 Smart commit 등을 더 다듬을 수 있다.

| 옵션 (감각) | 의미 |
|-------------|------|
| Smart commit | 데이터 변경 SQL 전에 Manual로 넘기는 안전 모드 |
| Return to auto-commit… | 커밋/롤백 후 다시 Auto로 (Smart와 함께) |
| Idle transaction 종료 | 오래 방치한 트랜잭션 자동 정리 |

운영 연결은 Smart만 믿기보다 **처음부터 Manual**이 단순하다.

### 7.3 Connection type으로 운영만 기본 Manual

DBeaver 기본:

| Connection type | Auto-commit 기본 (대략) |
|-----------------|-------------------------|
| Development / Test | On |
| **Production** | **Off (Manual)** |

설정:

1. 연결 편집 → **General** 등에서 Connection type을 **Production**으로  
2. 또는 `Window` → `Preferences` → `Connections` → `Connection types`에서  
   - Production: **Auto-commit by default** 꺼짐 확인  
   - Development: 필요 시 여기도 끄기  

운영 DB 연결은 이름에 `PROD` + type **Production**을 같이 쓰면 실수가 줄어든다.

### 7.4 Manual일 때 하는 일

```text
SQL 실행 또는 그리드 수정
        ↓
아직 DB에 확정 안 됨 (세션 트랜잭션)
        ↓
Commit  → 확정
Rollback → 취소
```

- 툴바 **Commit** / **Rollback**  
- 커밋 안 하고 연결 끊으면 DBMS·설정에 따라 롤백되는 경우가 많음 (방심 금지)  
- SELECT만 할 때도 Manual이면 문제 없는 편. 잠금·롱 트랜잭션만 주의  

### 7.5 안 꺼지거나 다시 Auto로 돌아갈 때

1. 연결 **Initialization**에 Manual이 저장됐는지 확인 (§7.2)  
2. Connection type이 Development라 기본 Auto인지 확인  
3. 툴바만 바꾼 뒤 재접속하지 않았는지  
4. 스크립트 창에서 **다른 DB/연결로 바꾸면** 모드가 꼬인다는 이슈 보고가 있음 → 창을 닫고 해당 연결로 새 SQL 에디터  
5. DBeaver 버전 업데이트 노트·이슈 확인  

---

## 8. 내보내기·가져오기

우클릭 테이블/결과 → **Export data**

| 형식 | 용도 |
|------|------|
| CSV / Excel | 분석·공유 |
| SQL INSERT | 이관·백업 감각 |
| JSON / XML | 연동 |

Import로 CSV를 테이블에 넣을 수 있다. 문자셋(UTF-8)·날짜 포맷을 맞춘다.  
운영 적재는 전용 ETL·SQL*Loader가 더 안전한 경우가 많다.

---

## 9. ER 다이어그램·메타데이터

- 테이블/스키마 → **다이어그램 보기** (버전에 따라 View diagram)  
- FK가 정의돼 있어야 관계가 예쁘게 나옴  
- DDL 추출: 객체 우클릭 → DDL 생성 → 파일로 저장  

문서화·인수인계용으로 ER+DDL을 위키에 붙일 때 유용 ([[Obsidian 사용법]]).

---

## 10. 자주 쓰는 설정

| 목적 | 어디 |
|------|------|
| 결과 행 수·페치 크기 | Preferences → Editors / Data Editor |
| SQL 포맷 | 에디터 우클릭 Format 또는 설정 |
| 다크 테마 | Appearance |
| **Auto-commit 해제** | §7 (연결 Initialization / Connection type) |
| SSH 터널 | 연결 → SSH 탭 (DB가 VPN 뒤에 있을 때) |

한국어 UI: 설치·언어팩 여부는 버전마다. 영문 UI여도 SQL은 동일.

---

## 11. Community vs 유료

| | Community (CE) | Enterprise 등 |
|--|----------------|---------------|
| 가격 | 무료 | 구독 |
| 기본 SQL·다중 DB | ○ | ○ |
| 고급 관리·클라우드·일부 NoSQL·지원 | 제한 | 확장 |

개인·학습·대부분 개발 조회는 CE로 충분한 경우가 많다.  
회사 표준 툴이 있으면 그걸 우선.

---

## 12. 다른 툴과 비교

| 툴 | 감각 |
|----|------|
| **DBeaver CE** | 무료·다 DB·만능에 가깝다 |
| **SQL Developer** | Oracle 특화 |
| **DataGrip** | 유료·완성도·리팩터 |
| **VS Code SQLTools** | 에디터 안에서 가볍게 ([[VS Code 추천 확장]]) |
| **Excel + ODBC** | 분석용, 스키마 관리엔 부적합 |
| **psql / sqlplus** | 스크립트·자동화·CI |

---

## 13. 문제 빠른 대처

| 증상 | 시도 |
|------|------|
| 드라이버 오류 | 연결 편집 → Download/Update driver |
| Oracle 서비스명/SID 혼동 | 연결 타입 전환 후 재테스트 |
| 한글 깨짐 | 연결 속성 문자셋, 클라이언트 NLS_LANG |
| 느린 결과 | 페치 크기↓, WHERE·인덱스, 행 제한 |
| 권한 오류 | 계정 롤·테이블스페이스 — DBA에 확인 |
| SSL/방화벽 | SSH 터널·VPN·화이트리스트 |
| Auto-commit이 다시 켜짐 | §7.5 |

---

## 14. 체크리스트

- [ ] CE 설치·워크스페이스 경로  
- [ ] 개발/운영 연결 분리 (이름에 `DEV`/`PROD`)  
- [ ] **운영·중요 연결 Auto-commit Off** (연결 설정에 저장)  
- [ ] Manual일 때 Commit/Rollback 위치 확인  
- [ ] 자주 쓰는 SQL을 스크립트/프로젝트로 저장  
- [ ] Export 전 개인정보·마스킹 확인  
- [ ] (Oracle) 실행 계획·AWR은 [[Oracle DB와 튜닝]]과 역할 분담  

---

## 관련

- [[생활위키 목차]]
- [[Oracle DB와 튜닝]]
- [[VS Code 사용법]]
- [[VS Code 추천 확장]]
- [[Docker 사용법]] — 로컬 DB 컨테이너와 접속
- [[윈도우 사용법]]
- [[공개 규칙]]
