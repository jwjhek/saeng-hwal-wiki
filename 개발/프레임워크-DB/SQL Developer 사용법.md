---
publish: true
draft: false
aliases:
  - SQL Developer
---

# SQL Developer 사용법

> **분류:** 개발 › 프레임워크·DB · [[생활위키 목차]]

**Oracle SQL Developer**는 Oracle이 배포하는 **무료 GUI 클라이언트**다. 
SQL 실행·스키마 탐색·실행 계획·데이터보내기·간단한 PL/SQL 디버깅까지 Oracle 작업을 한 화면에서 한다.

공식: [Oracle SQL Developer](https://www.oracle.com/database/sqldeveloper/)  
다운로드: [SQL Developer Downloads](https://www.oracle.com/tools/downloads/sqldev-downloads.html)

확인일: 2026-08-12  
메뉴·단축키는 **버전**(23.x·24.x 등)에 따라 조금 다를 수 있다.

관련: [[SQL 학습]] · [[Oracle DB와 튜닝]] · [[Oracle 힌트]] · [[Oracle 시노님]] · 다 DB 클라이언트: [[DBeaver 사용법]]

---

## 1. 쓰는 이유

| 상황 | SQL Developer |
|------|---------------|
| Oracle 전용 기능 | 실행 계획·Autotrace·AWR 리포트 뷰어·Data Pump 마법사 |
| 사내 표준 | DBA·운영이 SQL Developer 접속 정보를 기준으로 줄 때 |
| SQL*Plus 대체 | 워크시트·결과 그리드·자동 완성 |
| 스키마 탐색 | 연결 트리에서 테이블·뷰·패키지·동의어([[Oracle 시노님]]) |
| 학습·튜닝 | [[Oracle DB와 튜닝]] 점검을 GUI로 따라가기 |

[[DBeaver 사용법]]은 **여러 DBMS**를 한 툴로 다루기 좋고, SQL Developer는 **Oracle에 최적화**된 기능이 많다. 
회사에서 둘 다 쓰는 경우도 흔하다.

---

## 2. 설치

### 2.1 Windows

1. Oracle 다운로드 페이지에서 **Windows 64-bit with JDK included**(또는 JDK 별도) 선택  
2. Zip이면 원하는 폴더에 풀고 `sqldeveloper.exe` 실행  
3. 첫 실행 시 **JDK 경로**를 묻으면 번들 JDK 또는 설치된 [[JDK]] 지정  

설치형·Zip형은 배포에 따라 다르다. **회사 PC**는 보안 정책·프록시·Oracle 계정 로그인 필요 여부를 확인한다.

### 2.2 macOS·Linux

공식 패키지 또는 Zip. macOS는 Gatekeeper 경고가 뜨면 시스템 설정에서 허용.

### 2.3 업그레이드

기존 `sqldeveloper` 폴더를 새 버전으로 **교체**하거나 별도 경로에 두고 연결 설정을 옮긴다. 
`~/.sqldeveloper` 또는 사용자 홈 아래에 접속 정보·환경설정이 저장되는 경우가 많다.

---

## 3. 접속(연결) 만들기

1. 왼쪽 **Connections** 패널에서 **+** (새 연결)  
2. **Name**: `DEV_HR`, `PROD_READ`처럼 환경이 보이게  
3. **Username / Password**  
4. **Connection Type** 선택 후 나머지 입력  
5. **Test** → **Save** → **Connect**

### 3.1 Basic

| 항목 | 예 |
|------|-----|
| Hostname | DB 서버 IP·호스트명 |
| Port | `1521` (환경마다 다름) |
| Service name | `ORCLPDB1` (권장) |
| SID | 레거시 환경만 — Service와 혼동 주의 |

### 3.2 TNS

로컬 `tnsnames.ora`를 쓰는 환경. **Net Service Name** 목록에서 고른다. 
사내 표준 TNS 파일 경로를 DBA에게 받는다.

### 3.3 Cloud Wallet (ATP·ADW 등)

Oracle Cloud Autonomous DB는 **Wallet Zip**을 받아 연결한다.

1. Cloud 콘솔에서 Wallet 다운로드  
2. 연결 유형 **Cloud Wallet**  
3. Zip 경로·Wallet 비밀번호 지정  
4. Service 목록에서 `…_high` / `…_medium` / `…_low` 선택  

TLS·인증서가 Wallet에 포함된다. [[DBeaver 사용법]] Oracle 접속에도 같은 Wallet을 쓸 수 있다.

### 3.4 보안 습관

- 운영 DB는 **읽기 전용 계정**·별도 연결 이름  
- 암호를 스크립트·Git에 넣지 않는다  
- VPN·SSH 터널·방화벽 화이트리스트는 환경별로 DBA·인프라와 맞춘다  

---

## 4. 화면 구조

```text
┌─────────────────┬────────────────────────────┐
│ Connections     │ SQL Worksheet / 결과 탭    │
│ (스키마 트리)   │ Script Output · DBMS Output│
│ Reports         │ 실행 계획 · Autotrace      │
└─────────────────┴────────────────────────────┘
```

| 영역 | 하는 일 |
|------|---------|
| **Connections** | 연결·테이블·뷰·인덱스·프로시저·동의어 탐색 |
| **SQL Worksheet** | SQL·PL/SQL 작성·실행 |
| **Query Result** | SELECT 결과 그리드 |
| **Script Output** | `DBMS_OUTPUT`, 스크립트 메시지 |
| **Reports** | 사전 정의·사용자 리포트 |
| **DBA** (메뉴) | 세션·스토리지·백업 등 — 권한·에디션에 따라 |

테이블·뷰를 펼치면 **Data**·**SQL**·**Constraints** 등 하위 탭으로 메타데이터를 본다.

---

## 5. SQL 워크시트 — 실행 방식

같은 SQL이라도 **실행 단축키**에 따라 동작이 다르다. 헷갈리기 쉬운 부분이다.

| 단축키 | 동작 | 언제 쓰나 |
|--------|------|-----------|
| **`Ctrl` + `Enter`** | **커서 위치 문장 하나** 실행 (Run Statement) | SELECT·단일 DML·EXPLAIN |
| **`F5`** | **워크시트 전체**를 스크립트로 실행 (Run Script) | 여러 문장·PL/SQL 블록·`@script.sql` |
| **`F9`** | (버전에 따라) PL/SQL 실행·디버그 진입 | 패키지·프로시저 테스트 |

- `SELECT`만 보면 **`Ctrl` + `Enter`**가 일상적이다.  
- `BEGIN … END;`·여러 `INSERT`·DDL 묶음은 **`F5`**.  
- **`F5`**는 결과가 **Script Output** 쪽에 쌓이고, **`Ctrl` + `Enter`**는 **Query Result** 탭이 뜬다.

### 5.1 자주 쓰는 편집·탐색

| 단축키 | 동작 |
|--------|------|
| **`Ctrl` + `Space`** | 자동 완성 |
| **`Ctrl` + `/`** | 한 줄 주석 |
| **`Shift` + `F4`** | 객체 설명 (Describe) — 테이블명에 커서 두고 |
| **`Ctrl` + `Shift` + `O`** | SQL History |
| **`Ctrl` + `H`** | 찾기·바꾸기 |

단축키는 `Tools` → `Preferences` → `Shortcut Keys`에서 검색·변경한다.

---

## 6. 실행 계획·튜닝

느린 SQL은 [[SQL 실행 계획]]으로 플랜을 꺼내고, [[Oracle DB와 튜닝]] 흐름으로 원인을 가른다.

| 방법 | 설명 |
|------|------|
| **Explain Plan** (`Ctrl` + `F10` 또는 툴바) | 예상 계획. 실제 실행 없이 플랜만 |
| **Autotrace** | 실행 후 통계·계획 요약 (SQL*Plus `SET AUTOTRACE`에 가깝게) |
| **SQL Tuning Advisor** | (라이선스·권한 해당 시) 권고안 생성 |

워크시트에서 문장 선택 → **Explain Plan** → **Plan** 탭에서 단계별 Cost·Rows·Operation을 읽는다. 
힌트를 넣을 때는 [[Oracle 힌트]]와 사내 규정을 함께 본다.

```sql
-- 예: 바인드 변수 (워크시트)
VARIABLE v_id NUMBER;
EXEC :v_id := 100;
SELECT * FROM employees WHERE employee_id = :v_id;
```

---

## 7. DBMS_OUTPUT·디버깅

PL/SQL에서 `DBMS_OUTPUT.PUT_LINE`을 쓰면 **Script Output** 또는 **DBMS Output** 패널을 연다.

1. `View` → `Dbms Output` (또는 하단 탭)  
2. 녹색 **+** 로 현재 연결에 Output 활성화  
3. `SET SERVEROUTPUT ON` (스크립트 실행 시) 후 `BEGIN … END;`를 **F5**로 실행  

**디버그**: 연결된 프로시저·함수에서 우클릭 **Debug** (권한·컴파일 옵션 필요). 
브레이크포인트·Step Over로 값을 본다.

---

## 8. 데이터·스키마 작업

| 작업 | 경로 (대략) |
|------|-------------|
| 테이블 데이터 보기 | 연결 트리 → Tables → 테이블 → **Data** 탭 |
| 행 편집 | Data 탭에서 직접 수정 후 Commit (Auto-commit 설정에 따름) |
| DDL 보기 | 테이블 우클릭 → **SQL** 또는 **Quick DDL** |
| CSV·Excel보내기 | 결과 그리드 우클릭 → **Export** |
| CSV·스프레드시트 가져오기 | 테이블 우클릭 → **Import Data** |
| 객체 생성 마법사 | 테이블·뷰·시퀀스 등 우클릭 **Create** |

대량 이관은 **Data Pump** 마법사(`Tools` → `Database Migration` / Export·Import)를 쓰거나 운영 표준 배치를 따른다. 
운영 테이블 **직접 편집**은 트랜잭션·감사 정책을 확인한다.

---

## 9. 커밋·Auto-commit

SQL Developer도 **자동 커밋** 설정이 있다.

| 설정 | 의미 |
|------|------|
| Auto-commit **켜짐** | DML 실행 후 즉시 COMMIT — 실수 시 롤백 불가 |
| Auto-commit **꺼짐** | 명시적 **Commit**·**Rollback** 버튼(툴바)으로 확정 |

운영·공유 DB 연결은 **Auto-commit Off** + 연결 이름에 `PROD` 표기를 권장한다. 
[[DBeaver 사용법]] §8과 같은 습관이다.

---

## 10. SQL*Plus·SQLcl과

| | SQL Developer | SQL*Plus / SQLcl |
|--|---------------|-------------------|
| UI | GUI·그리드 | 터미널 |
| 스크립트·CI | 가능하나 무거움 | **배치·자동화**에 유리 |
| 실행 계획 | 클릭·탭 | `EXPLAIN PLAN`, `AUTOTRACE` |
| 사내 표준 | 개발·DBA 데스크톱 | 서버·배포 스크립트 |

같은 `user/pass@//host:1521/service` 문자열을 공유할 수 있다. 
서버에서는 `sqlplus`, 로컬 분석에서는 SQL Developer가 흔한 조합이다.

---

## 11. [[DBeaver 사용법]]과 비교

|           | SQL Developer              | DBeaver CE                       |
| --------- | -------------------------- | -------------------------------- |
| DBMS      | **Oracle 중심** (다른 DB는 제한적) | Oracle·PostgreSQL·MySQL 등 **다중** |
| 가격        | 무료 (SQL Developer)         | CE 무료                            |
| Oracle 특화 | AWR 뷰·Data Pump·PL/SQL 디버그 | 기본 실행 계획·드라이버                    |
| 회사에서      | Oracle SI·공공·금융 표준인 경우 많음  | 팀마다 혼용                           |

접속 정보만 맞으면 **둘 다** 같은 DB에 붙을 수 있다. 
Oracle 튜닝·리포트는 SQL Developer, 여러 DB를 오가며 조회는 DBeaver — 이렇게 나누는 경우도 있다.

---

## 12. 자주 겪는 문제

| 증상 | 시도 |
|------|------|
| **ORA-12514**·리스너 | Service name / SID, 호스트·포트, `tnsnames.ora` |
| **ORA-28040**·인증 | DB·클라이언트 버전, `sqlnet.ora` 협상 설정 |
| Wallet 연결 실패 | Zip 경로·Wallet 비밀번호·서비스명(`_high` 등) |
| 한글 깨짐 | DB 문자셋·NLS_LANG·폰트 |
| F5와 Ctrl+Enter 혼동 | §5 — 스크립트 vs 한 문장 |
| 결과가 안 보임 | Query Result 탭·Script Output·DBMS Output 확인 |
| 느린 페치 | `Tools` → `Preferences` → **Database** → Advanced — **Fetch Size** |
| 권한 오류 | 롤·시스템 권한 — DBA에 요청 |

---

## 13. 체크리스트

- [ ] JDK 포함 배포본 또는 JDK 경로 지정  
- [ ] DEV / PROD 연결 **이름 분리**  
- [ ] 운영 연결 **Auto-commit Off**  
- [ ] **`Ctrl` + `Enter`** vs **`F5`** 구분  
- [ ] Explain Plan으로 느린 SQL 1건 읽어 보기 → [[Oracle DB와 튜닝]]  
- [ ] Export 전 **개인정보·마스킹** 확인  
- [ ] 접속 정보·Wallet을 Git·위키에 올리지 않기  

---

## 면책

> **면책**  
> 일반 학습·업무 참고용이다. **운영 DB 변경·라이선스**(Diagnostic/Tuning Pack 등)는 사내 정책·DBA 승인을 따른다.  
> 메뉴·버전·단축키는 Oracle 배포에 따라 다르다. 최종 확인은 [Oracle SQL Developer Documentation](https://docs.oracle.com/en/database/oracle/sql-developer/)이다.

---

## 관련

- [[생활위키 목차]]
- [[SQL 학습]]
- [[SQL 실행 계획]]
- [[Oracle DB와 튜닝]] — AWR·실행 계획·인덱스
- [[Oracle 힌트]] — 옵티마이저 힌트
- [[Oracle 시노님]] — 스키마 별칭
- [[DBeaver 사용법]] — 다중 DB 클라이언트
- [[전자정부프레임워크]] — 공공 SI에서 Oracle·SQL Developer 조합이 흔함
- [[VS Code 사용법]] — 스크립트 파일 관리·가벼운 편집
