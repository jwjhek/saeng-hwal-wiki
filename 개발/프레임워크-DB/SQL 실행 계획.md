---
publish: true
draft: false
depth: article
aliases:
  - 실행 계획
  - 실행계획
  - EXPLAIN PLAN
  - Explain Plan
---

# SQL 실행 계획

> **분류:** 개발 › 프레임워크·DB · [[생활위키 목차]]

**실행 계획**(execution plan)은 데이터베이스가 SQL을 **어떤 순서로, 어떤 방법으로** 처리할지(또는 했는지) 보여 주는 표다.  
느린 조회를 고칠 때 **감이 아니라 계획부터** 본다.

이 글은 **계획을 꺼내는 방법**과 **읽는 포인트**다.  
원인 가르기·인덱스 설계는 [[Oracle DB와 튜닝]], 계획을 억지로 바꿀 때는 [[Oracle 힌트]].

확인일: 2026-08-13

문법 뼈대: [[SQL 학습]] · 도구: [[SQL Developer 사용법]] · [[DBeaver 사용법]]

---

## 1. 개요

| 항목 | 설명 |
|------|------|
| **무엇** | 옵티마이저가 고른 **접근 경로·조인 방법·순서** |
| **예상 계획** | SQL을 **안 돌리거나** 가볍게만 보고, **추정** 비용·행 수 |
| **실제 계획** | SQL을 **실행한 뒤** 실제 행 수·시간·I/O |
| **누가 만드나** | 옵티마이저 (통계·힌트·인덱스·SQL 형태에 영향) |

```text
SQL
 ↓
옵티마이저 (통계·제약·힌트)
 ↓
실행 계획
 ↓
실행 (버퍼 캐시 · 디스크)
```

**예상만** 보면 빠르고 안전하다. **실제**를 봐야 카디널리티 오차가 드러난다.  
운영에서 무거운 `SELECT`를 실제 계획용으로 돌리면 **부하**가 된다 → 테스트 DB·조건 축소.

---

## 2. 예상 vs 실제

| | 예상 (Explain) | 실제 (실행 후) |
|--|----------------|----------------|
| **하는 일** | 계획만 세움 | 쿼리를 **실행**하고 통계를 붙임 |
| **볼 것** | Operation, 추정 Rows·Cost | **A-Rows**(실제 행), 시간, 버퍼 |
| **장점** | DML·대량 조회를 안 돌려도 됨 | 「추정과 현실이 다른지」 확인 |
| **단점** | 바인드·데이터 분포를 **빗나갈 수 있음** | 느린 SQL이면 **그만큼 기다림** |

Oracle에서 추정을 `E-Rows`, 실제를 `A-Rows`로 부르는 출력이 흔하다.  
둘의 차이가 크면 **통계 오래됨·바인드 피킹·치우친 데이터**를 의심한다.

---

## 3. Oracle에서 보기

현장·이 위키의 DB 글은 Oracle 비중이 크다. 권한은 `EXPLAIN`·딕셔너리 조회가 되는 **개발·튜닝 계정**이 필요하다.

### 3.1 EXPLAIN PLAN (예상)

```sql
EXPLAIN PLAN FOR
SELECT e.name, d.dept_name
  FROM emp e
  JOIN dept d ON e.dept_id = d.dept_id
 WHERE e.salary >= 350;

SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);
```

기본 출력 포맷을 조금 더 보려면:

```sql
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY(NULL, NULL, 'TYPICAL'));
-- 힌트 반영 여부: 'BASIC +NOTE'  ([[Oracle 힌트]] §5)
```

`EXPLAIN PLAN FOR`는 **그 SQL을 실행하지 않는다.** `INSERT`/`UPDATE`의 계획만 볼 때도 이 방식이 안전하다 (문장 자체는 실행 안 함).

### 3.2 DISPLAY_CURSOR (실제에 가깝게)

방금 세션에서 **실행한** 커서의 계획.

```sql
-- 1) 통계를 모으려면 (세션 또는 힌트)
ALTER SESSION SET STATISTICS_LEVEL = ALL;
-- 또는 SQL에 /*+ GATHER_PLAN_STATISTICS */

SELECT e.name, d.dept_name
  FROM emp e
  JOIN dept d ON e.dept_id = d.dept_id
 WHERE e.salary >= 350;

SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY_CURSOR(NULL, NULL, 'ALLSTATS LAST'));
```

| 인자 | 의미 |
|------|------|
| `NULL, NULL` | **바로 직전** SQL (세션 마지막 커서) |
| `'ALLSTATS LAST'` | 실제 행·시간 등. **LAST** = 마지막 실행 |
| `'ALLSTATS LAST +PEEKED_BINDS'` | 바인드 값까지 (버전·권한에 따름) |

다른 세션·공유 풀의 SQL이면 `SQL_ID`·`CHILD_NUMBER`를 넣는다.

```sql
SELECT * FROM TABLE(
  DBMS_XPLAN.DISPLAY_CURSOR('sql_id여기', 0, 'ALLSTATS LAST')
);
```

`V$SQL` / AWR에서 `SQL_ID`를 찾는 흐름은 [[Oracle DB와 튜닝]].

### 3.3 AUTOTRACE (SQL*Plus · SQLcl)

```sql
SET AUTOTRACE ON EXPLAIN
SELECT ... ;

SET AUTOTRACE ON STATISTICS
SELECT ... ;

SET AUTOTRACE OFF
```

`ON`은 계획+통계, `TRACEONLY`는 결과 행을 화면에 안 뿌리고 계획·통계만 (대량 조회 때).  
권한(`PLUSTRACE` 롤 등)이 없으면 실패한다.

### 3.4 GUI

| 도구 | 하는 법 |
|------|---------|
| [[SQL Developer 사용법]] | 문장 선택 → **Explain Plan** (`Ctrl` + `F10`) · **Autotrace** · Plan 탭 |
| [[DBeaver 사용법]] | SQL 편집기 → **실행 계획** (`Ctrl` + `Shift` + `E`) |
| OEM / Cloud Control | Real-Time SQL Monitoring, 실행 계획 그래픽 |

GUI는 **같은 계획의 그림**이다. 숫자 해석은 텍스트(`DBMS_XPLAN`)와 같다.

---

## 4. PostgreSQL

```sql
EXPLAIN
SELECT ... ;

EXPLAIN ANALYZE
SELECT ... ;

EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT ... ;
```

| | 설명 |
|--|------|
| `EXPLAIN` | 예상만 |
| `EXPLAIN ANALYZE` | **실제로 실행** + 실제 시간·행 |
| `BUFFERS` | 공유·로컬 버퍼 읽기 |

`ANALYZE`는 DML이면 **데이터까지 바뀐다.** `EXPLAIN ANALYZE UPDATE ...` 는 롤백하거나 테스트 DB에서만.

---

## 5. MySQL · MariaDB

```sql
EXPLAIN
SELECT ... ;

EXPLAIN FORMAT=TREE
SELECT ... ;

-- 8.0.18+ 등: 실제 실행 (버전 확인)
EXPLAIN ANALYZE
SELECT ... ;
```

옛 `EXPLAIN`은 **표 형태**(type, key, rows, Extra)다.  
`type`이 `ALL`이면 풀 스캔 성격, `ref`/`range`면 인덱스 접근에 가깝다.  
`Extra`의 `Using filesort` · `Using temporary` 는 정렬·임시표 신호.

---

## 6. SQL Server (방향만)

Management Studio에서 **실제 실행 계획 포함** 실행, 또는:

```sql
SET SHOWPLAN_TEXT ON;   -- 예상, 실행 안 함
SET STATISTICS IO ON;
SET STATISTICS TIME ON;
```

그래픽 계획의 두께·비용 %는 **상대값**이다. 한 노드 100%여도 전체가 가벼운 SQL일 수 있다.

---

## 7. 계획에서 볼 것

제품마다 이름만 조금 다르다. 의미는 통한다.

### 7.1 접근 방법

| 보이는 말 (Oracle 예) | 뜻 |
|----------------------|-----|
| **TABLE ACCESS FULL** | 표 전체 스캔 |
| **INDEX RANGE SCAN** | 인덱스 구간 |
| **INDEX UNIQUE SCAN** | 유일 인덱스 한 건 |
| **INDEX FULL SCAN** / **FAST FULL** | 인덱스 전체를 읽음 (표보다 나을 수도) |
| **TABLE ACCESS BY INDEX ROWID** | 인덱스로 위치 잡은 뒤 표 블록 |

「풀 스캔 = 무조건 나쁨」이 아니다. **많은 행**을 읽으면 풀 스캔이 맞을 수 있다.  
**적은 행**인데 풀 스캔이면 조건·인덱스·함수로 인덱스를 못 타는지를 본다 → [[SQL 학습]] 흔한 실수(타입 변환).

### 7.2 조인 방법

| 방법 | 흔한 장면 |
|------|-----------|
| **Nested Loops** | 한쪽이 작고, 안쪽을 인덱스로 반복 찾기 (OLTP) |
| **Hash Join** | 양쪽이 큰 등가 조인 (`=`) |
| **Merge Join** | 정렬된 두 집합을 맞추기 |

조인 **순서**(어느 표가 먼저)도 비용에 크게 영향. 힌트로 바꿀 때는 [[Oracle 힌트]] `LEADING` · `USE_NL` 등.

### 7.3 숫자

| 항목 | 읽는 법 |
|------|---------|
| **Cost** | 옵티마이저 **상대** 비용. 절대 ms가 아님. 계획 **안**에서 비교 |
| **E-Rows / rows** | **추정** 행 수 |
| **A-Rows** | **실제** 행 수 (실제 계획) |
| **Bytes** | 추정 데이터 양 |
| **Time** | 실제 계획에서 경과 (제품·옵션) |
| **Starts** | 그 단계가 **몇 번** 돌았는지 (NL 조인 안쪽) |

`E-Rows` 10인데 `A-Rows` 100만이면, 그 아래 단계가 **전부 빗나갈** 수 있다. **통계 수집**·표현식·바인드를 점검.

### 7.4 읽는 순서

트리는 **안쪽(자식)부터** 실행되는 그림이 많다. 텍스트 계획은 **들여쓰기**가 자식이다.

```text
SELECT
  HASH JOIN
    TABLE ACCESS FULL dept
    TABLE ACCESS FULL emp
```

여기서는 두 풀 스캔 후 해시 조인. `WHERE emp_id = :id`인데 풀 스캔이면 **조건이 계획에 반영됐는지**부터 본다.

---

## 8. GUI에서 헷갈리는 점

| 현상 | 정리 |
|------|------|
| Explain과 실행 후 계획이 **다름** | 바인드 피킹, 적응 계획, 실제 값 |
| 화면 Cost가 작은데 느림 | Cost ≠ 벽시계. Wait·네트워크·앱 반복 호출 |
| 그래픽만 보고 「풀 스캔 없애기」 | 대량 배치에선 풀 스캔이 정상일 수 있음 |
| 다른 환경과 계획이 다름 | 통계·데이터량·파라미터·버전·힌트 |

같은 SQL을 **바인드로 한 번**, **리터럴로 한 번** 찍어 보면 피킹 차이를 볼 수 있다.

---

## 9. 권한·주의

- `EXPLAIN` / `DBMS_XPLAN` / `V$SQL` 은 **권한**이 필요하다. 없으면 DBA·튜닝 롤을 요청한다.  
- **실제 계획** = 그 SQL이 **돈다.** 잠금·부하·DML 부작용을 생각한다.  
- PostgreSQL `EXPLAIN ANALYZE` + `UPDATE`/`DELETE`는 **데이터가 변한다.**  
- 실행 계획 출력에 **SQL 전문·바인드 값**이 남을 수 있다. 로그·티켓에 개인정보를 붙이지 않는다.  
- 운영에서 `STATISTICS_LEVEL=ALL`을 **인스턴스 전체**로 켜지 않는 편이 안전하다. 세션·힌트 단위.

---

## 10. 실전 체크

- [ ] 느린 SQL을 **예상 계획**으로 먼저 봄 (FULL vs INDEX, 조인 종류)  
- [ ] 필요하면 **테스트 DB**에서 실제 계획 (`A-Rows` / `EXPLAIN ANALYZE`)  
- [ ] `E-Rows`와 실제 행 수가 크게 다른지  
- [ ] 앱과 같은 **바인드**로 한 번 더  
- [ ] 고치기 전후 계획을 **저장**해 비교  
- [ ] 힌트를 넣었다면 NOTE에 **무시**가 있는지 — [[Oracle 힌트]]

---

## 11. 정리

| 항목 | 한 줄 |
|------|--------|
| 목적 | 옵티마이저가 **어떻게 읽는지**를 드러냄 |
| Oracle | `EXPLAIN PLAN` + `DBMS_XPLAN` / `DISPLAY_CURSOR` / GUI |
| 다른 DB | PostgreSQL `EXPLAIN ANALYZE`, MySQL `EXPLAIN` |
| 핵심 | 풀스캔·조인 방법, **추정 vs 실제 행 수** |
| 다음 | 통계·SQL·인덱스 ([[Oracle DB와 튜닝]]), 예외적으로 힌트 |

---

## 면책

> **면책**  
> 교육용 요약이다. 뷰 이름·권한·`EXPLAIN ANALYZE` 동작은 **제품·버전**마다 다르다.  
> 운영 DB에서 실제 계획을 뜰 때는 **부하·잠금·DML**을 확인한다. 튜닝 변경은 테스트 후.

---

## 관련

- [[생활위키 목차]]
- [[SQL 학습]]
- [[Oracle DB와 튜닝]]
- [[Oracle 힌트]]
- [[SQL Developer 사용법]]
- [[DBeaver 사용법]]
- [[Oracle 시노님]]
