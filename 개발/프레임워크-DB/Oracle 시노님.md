---
publish: true
draft: false
depth: article
aliases:
  - Oracle Synonym
  - SYNONYM
  - 동의어
---

# Oracle 시노님

> **분류:** 개발 › 프레임워크·DB · [[생활위키 목차]]

**Oracle 시노님**(synonym)은 **다른 스키마 객체**를 가리키는 **별칭(이름)** 이다. 
SQL에서 `OWNER.TABLE` 대신 **짧은 이름**으로 테이블·뷰·시퀀스·프로시저 등을 부를 수 있다.

**뷰(view)** 와 달리 **데이터를 저장하지 않고**, 이름만 **리다이렉트**한다. 
공공·SI·[[전자정부프레임워크]] Oracle 사업에서 **스키마 분리·앱 계정 단순화**에 자주 쓴다.

공식: [Database Administrator's Guide — Synonyms](https://docs.oracle.com/en/database/oracle/oracle-database/)  
확인일: 2026-08-11

관련: [[Oracle DB와 튜닝]] · [[Oracle 힌트]] · [[DBeaver 사용법]] · [[전자정부프레임워크]]

---

## 1. 개요

| 항목 | 설명 |
|------|------|
| 무엇 | 객체에 대한 **대체 이름** (포인터) |
| 대상 | **TABLE**, **VIEW**, **SEQUENCE**, **PROCEDURE**, **FUNCTION**, **PACKAGE**, **MATERIALIZED VIEW** 등 |
| 종류 | **Private**(개인) · **PUBLIC**(전역) |
| 소유 | 시노님 **자체**가 스키마 객체. `CREATE SYNONYM` 권한 필요 |
| vs 뷰 | 뷰 = **쿼리 정의 + (간접) 데이터 접근**. 시노님 = **이름만** 다른 객체로 연결 |

```text
앱 SQL:  SELECT * FROM EMP;
              ↓ (시노님 EMP)
실제:    HR.EMPLOYEES
```

---

## 2. Private vs PUBLIC

| | **Private synonym** | **PUBLIC synonym** |
|--|---------------------|---------------------|
| 가시성 | **만든 사용자** + 권한 있는 사용자 | **모든** 사용자 (대상에 SELECT 등 권한 있을 때) |
| 이름 충돌 | 스키마마다 같은 이름 가능 | **DB 전체에서 이름 유일** |
| 생성 | `CREATE SYNONYM` | `CREATE PUBLIC SYNONYM` + **`CREATE PUBLIC SYNONYM`** 권한 |
| 위험 | 상대적으로 단순 | **이름 가로채기**·오래된 public synonym 잔존 |

해석 순서(같은 이름이 있을 때): **현재 사용자 private synonym** → **public synonym** → **로컬 객체** (버전·설정은 문서 확인).

---

## 3. CREATE · REPLACE · DROP

### 3.1 Private synonym

```sql
-- HR.EMPLOYEES 를 내 스키마에서 EMP 로
CREATE SYNONYM emp FOR hr.employees;

CREATE OR REPLACE SYNONYM emp FOR hr.employees;

DROP SYNONYM emp;
-- 다른 사람 소유: DROP SYNONYM hr.emp;
```

### 3.2 Public synonym

```sql
CREATE PUBLIC SYNONYM emp FOR hr.employees;

CREATE OR REPLACE PUBLIC SYNONYM emp FOR hr.employees;

DROP PUBLIC SYNONYM emp;
```

| 옵션 | 설명 |
|------|------|
| **OR REPLACE** | 있으면 **교체**. 없으면 생성 |
| **FOR** | `스키마.객체` 또는 **같은 스키마** 객체명 |
| **링크** | DB Link 객체: `CREATE SYNONYM remote_emp FOR emp@link_db;` |

### 3.3 권한

| 작업 | 필요 권한 (예) |
|------|----------------|
| Private synonym 생성 | 대상 객체에 대한 **적절한 권한** + `CREATE SYNONYM` |
| Public synonym 생성 | 위 + **`CREATE PUBLIC SYNONYM`** (보통 DBA) |
| 다른 사용자 synonym 삭제 | **`DROP ANY SYNONYM`** 등 |

대상 테이블에 **SELECT** 권한이 없으면 시노님을 만들어도 **조회 불가**다.

---

## 4. 이름 해석·조회

### 4.1 앱에서 보이는 이름

```sql
-- APP_USER 로 접속했을 때
SELECT * FROM dept;   -- APP_USER.DEPT (synonym) → OPS.DEPT (table)
```

[[DBeaver 사용법]] — 스키마 트리에서 **Synonyms** 노드로 확인.

### 4.2 데이터 딕셔너리

```sql
-- 내 시노님
SELECT synonym_name, table_owner, table_name, db_link
  FROM user_synonyms
 ORDER BY synonym_name;

-- DBA (권한 있을 때)
SELECT owner, synonym_name, table_owner, table_name
  FROM dba_synonyms
 WHERE synonym_name = 'EMP';

-- Public 만
SELECT synonym_name, table_owner, table_name
  FROM all_synonyms
 WHERE owner = 'PUBLIC';
```

| 뷰 | 설명 |
|----|------|
| **USER_SYNONYMS** | 내 private synonym |
| **ALL_SYNONYMS** | 접근 가능한 synonym (public 포함) |
| **DBA_SYNONYMS** | 인스턴스 전체 (DBA) |

`TABLE_OWNER` / `TABLE_NAME` 이 **실제 객체**다. `DB_LINK` 가 있으면 **원격** 대상.

---

## 5. 뷰와 비교

|               | **Synonym**            | **View**               |
| ------------- | ---------------------- | ---------------------- |
| 정의            | **이름 → 객체** 매핑         | **SELECT 쿼리** 정의       |
| 데이터           | 없음                     | **기본 테이블** 데이터를 쿼리로 노출 |
| 컬럼 제한         | 없음 (대상 그대로)            | **컬럼·조건** 가릴 수 있음      |
| [[Oracle 힌트]] | 대상 테이블·뷰에 따라 **간접** 영향 | 뷰 **정의 SQL**에 힌트 가능    |
| 용도            | **스키마 숨기기**·이름 통일      | **보안·단순화·집계**          |

둘 다 쓸 수 있다: `CREATE SYNONYM v_emp FOR hr.v_emp_summary;`

---

## 6. [[전자정부프레임워크]]·SI 패턴

| 패턴 | 설명 |
|------|------|
| **스키마 분리** | 업무 데이터 `OPS` / 앱 계정 `APP` — APP에는 **synonym만** |
| **Public synonym** | 레거시·공통 코드 테이블을 **짧은 이름**으로 — **이름 충돌** 주의 |
| **환경 이전** | DEV synonym → 운영 **스키마명** 다르면 **재생성** 스크립트 필요 |
| **MyBatis** | `FROM COMTNUSER` — 실제는 synonym → `COM.USR_TBL` |
| **Tibero·호환 DB** | `CREATE SYNONYM` 문법 **유사**. 이관 시 **PUBLIC**·권한 재점검 |

DB 튜닝 시 `USER_SYNONYMS` 로 **실제 테이블**을 찾은 뒤 [[Oracle DB와 튜닝]] 절차를 탄다. 
시노님 때문에 **잘못된 스키마**를 튜닝하는 실수를 줄인다.

---

## 7. 주의·실수

| 주제 | 설명 |
|------|------|
| **Broken synonym** | 대상 테이블 **삭제·이름 변경** → 시노님만 남음. 조회 시 **ORA-** 오류 |
| **Public 남용** | 같은 이름을 여러 팀이 기대 → **예측 불가** |
| **권한** | 시노님 있어도 **대상 GRANT** 없으면 실패 |
| **DDL** | `DROP TABLE` 시 synonym **자동 삭제 안 됨** — **고아 synonym** 정리 |
| **DB Link** | 링크 끊기면 synonym **유효하지 않음** |

```sql
-- 대상 확인 (예: invalid 여부는 all_objects 등과 조합)
SELECT s.synonym_name, s.table_owner, s.table_name, o.status
  FROM user_synonyms s
  LEFT JOIN all_objects o
    ON o.owner = s.table_owner AND o.object_name = s.table_name;
```

---

## 8. 실전 체크

- [ ] SQL의 테이블명이 **로컬 테이블**인지 **synonym**인지 `USER_SYNONYMS` 로 확인했는가  
- [ ] Public synonym **이름 충돌**·레거시 잔존을 점검했는가  
- [ ] 앱 계정에는 **synonym + 최소 GRANT** 만 두는 설계인가  
- [ ] 이관·스키마 변경 시 **CREATE OR REPLACE SYNONYM** 스크립트가 있는가  
- [ ] 튜닝·[[Oracle 힌트]] 적용 시 **실제 owner.table** 을 짚었는가  

---

## 면책

> **면책**  
> 권한·뷰 이름·PUBLIC 정책은 **조직·버전**마다 다르다. 운영 synonym·PUBLIC 변경은 **변경관리·롤백** 후에.  
> 이 글은 **객체 개념·SQL 예시**이며 특정 스키마 설계를 권하지 않는다.

---

## 관련

- [[Oracle DB와 튜닝]]
- [[Oracle 힌트]]
- [[DBeaver 사용법]]
- [[전자정부프레임워크]]
- [[Spring과 Spring Boot 학습]]
- [[생활위키 목차]]
