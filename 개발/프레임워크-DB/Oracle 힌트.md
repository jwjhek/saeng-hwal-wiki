---
publish: true
draft: false
depth: article
aliases:
  - Oracle Hint
  - SQL 힌트
---

# Oracle 힌트

> **분류:** 개발 › 프레임워크·DB · [[생활위키 목차]]

**Oracle 힌트**(hint)는 SQL 문 안에 넣어 **옵티마이저**에게 “이렇게 실행해 달라”고 **권고**하는 주석이다. 
`/*+ ... */` 형태로 **SELECT·INSERT·UPDATE·DELETE·MERGE** 등에 붙인다.

힌트는 **실행 계획**을 바꿀 수 있지만, 데이터·통계·버전이 바뀌면 **역효과**가 나기 쉽다. 
근본 튜닝 순서는 [[Oracle DB와 튜닝]]을 먼저 본다.

공식: [SQL Tuning Guide — Optimizer Hints](https://docs.oracle.com/en/database/oracle/oracle-database/)  
확인일: 2026-08-11

관련: [[Oracle DB와 튜닝]] · [[Oracle 시노님]] · [[DBeaver 사용법]] · [[전자정부프레임워크]]

---

## 1. 개요

| 항목 | 설명 |
|------|------|
| 무엇 | 옵티마이저 **실행 계획**에 영향을 주는 **SQL 주석** |
| 문법 | `/*+ 힌트이름(인자) ... */` — **`+` 바로 뒤**에 공백 없이 |
| 위치 | 보통 **SELECT** 직후 첫 키워드 앞 (`SELECT /*+ ... */`) |
| 대상 | **접근 경로**(인덱스·풀스캔), **조인 순서·방법**, **병렬** 등 |
| 한계 | 잘못 쓰면 **느려지거나** 다른 환경에서 **깨짐**. “영구 패치” 대용 아님 |

```text
SQL 작성 → 파싱 → 옵티마이저가 후보 플랜 평가 → 실행 계획
                    ↑
              힌트가 후보·선택에 개입
```

힌트 없이 **통계·SQL·인덱스**를 고치는 것이 기본이다. 힌트는 **검증된 예외**에 가깝다.

---

## 2. 문법·붙이는 위치

### 2.1 기본 형태

```sql
SELECT /*+ INDEX(e emp_pk) */
       e.empno, e.ename
  FROM employees e
 WHERE e.empno = :id;
```

| 주의 | 설명 |
|------|------|
| `/*+` | 일반 주석 `/*` 와 다름. **`+` 필수** |
| 별칭 | 힌트 안 테이블 이름은 SQL **별칭(alias)** 과 맞춤 |
| 무시 | 문법 오류·지원 안 하는 힌트·버전 차이 → **조용히 무시**될 수 있음 |
| 확인 | `DBMS_XPLAN` 으로 **힌트가 반영됐는지** 반드시 본다 |

### 2.2 힌트 블록 위치 (흔한 패턴)

```sql
-- SELECT
SELECT /*+ FULL(t) */ ...

-- 서브쿼리 (해당 블록에만)
SELECT *
  FROM (SELECT /*+ INDEX(d dept_idx) */ ... FROM dept d) v;

-- DELETE / UPDATE (버전·문맥에 따라)
DELETE /*+ INDEX(e emp_pk) */ FROM employees e WHERE ...
```

애플리케이션·MyBatis XML에 힌트를 **하드코딩**하면 배포·버전 관리 부담이 커진다.

---

## 3. 자주 쓰는 힌트 (표)

| 힌트 | 의미 (요약) | 예 |
|------|-------------|-----|
| **INDEX** | 해당 인덱스 사용 권고 | `INDEX(t idx_name)` |
| **FULL** | **풀 테이블 스캔** 권고 | `FULL(t)` |
| **NO_INDEX** | 인덱스 사용 억제 | `NO_INDEX(t idx_name)` |
| **USE_NL** | **Nested Loops** 조인 | `USE_NL(a b)` |
| **USE_HASH** | **Hash** 조인 | `USE_HASH(a b)` |
| **USE_MERGE** | **Sort-Merge** 조인 | `USE_MERGE(a b)` |
| **LEADING** | **조인 순서** (왼쪽부터 드라이빙) | `LEADING(a b c)` |
| **ORDERED** | FROM 절 순서대로 조인 | `ORDERED` |
| **PARALLEL** | **병렬** 실행 | `PARALLEL(t, 4)` |
| **FIRST_ROWS(n)** | **처음 n행** 빨리 (OLTP) | `FIRST_ROWS(10)` |
| **ALL_ROWS** | **전체 결과** 처리에 유리 (배치) | `ALL_ROWS` |

정확한 인자·조합은 **버전별 문서**가 최종본이다.

---

## 4. 예시 SQL

### 4.1 인덱스 vs 풀 스캔

```sql
-- 인덱스 타기를 기대할 때 (통계·선택도 맞을 때만)
SELECT /*+ INDEX(o order_pk) */
       o.order_id, o.status
  FROM orders o
 WHERE o.order_id = :id;

-- 대량 스캔이 맞을 때 (소량 인덱스 랜덤 I/O보다 나을 수 있음)
SELECT /*+ FULL(l) */
       COUNT(*)
  FROM log_table l
 WHERE l.log_date >= TRUNC(SYSDATE) - 7;
```

### 4.2 조인

```sql
SELECT /*+ LEADING(d e) USE_NL(e) INDEX(e emp_dept_idx) */
       d.deptno, e.empno
  FROM dept d, employees e
 WHERE d.deptno = e.deptno;
```

`LEADING` 과 `USE_NL` 을 **함께** 쓰는 경우가 많다. 플랜이 기대와 다르면 **별칭·조인 그래프**를 다시 본다.

### 4.3 PARALLEL (주의)

```sql
SELECT /*+ PARALLEL(t, 8) FULL(t) */
       ...
  FROM big_fact t
 WHERE ...
```

| 위험 | 설명 |
|------|------|
| CPU·I/O 폭주 | `PARALLEL(256)` 같은 **과다** 설정은 다른 세션을 **밀어냄** |
| OLTP | 짧은 트랜잭션에 병렬 힌트 → **오히려 느림** |
| 운영 정책 | 많은 사이트가 **힌트 병렬 금지** |

[[Oracle DB와 튜닝]] §11 — 검증 없는 `PARALLEL` 남발 금지.

---

## 5. 실행 계획과 확인

힌트를 넣었다고 **반영됐다고 가정하지 않는다.**

```sql
EXPLAIN PLAN FOR
SELECT /*+ INDEX(e emp_pk) */ e.empno FROM employees e WHERE e.empno = 1;

SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY(NULL, NULL, 'BASIC +NOTE'));
```

실행 후:

```sql
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY_CURSOR(NULL, NULL, 'ALLSTATS LAST'));
```

| 볼 것 | 설명 |
|-------|------|
| **NOTE** | 힌트 **무시·병합** 메시지 |
| **Operation** | INDEX RANGE SCAN vs TABLE ACCESS FULL |
| **A-Rows vs E-Rows** | 통계·힌트 불일치 신호 ([[Oracle DB와 튜닝]] §5.5) |

[[DBeaver 사용법]] — Explain·실행 계획 뷰로 같은 내용을 GUI에서 볼 수 있다.

---

## 6. 쓸 때 · 피할 때

### 6.1 힌트를 검토할 만한 때

| 상황 | 설명 |
|------|------|
| 통계·인덱스·SQL은 맞는데 **가끔** 플랜만 틀어짐 | 바인드 피킹· skew |
| **단기 응급** | 배포 전 AWR로 원인 SQL 확인 후 **테스트 DB**에서만 |
| SQL Plan Baseline·Profile과 **함께** 표준화 | 힌트만 영구 박아 두기보다 **Baseline** 검토 |

### 6.2 피해야 할 때

| 상황 | 설명 |
|------|------|
| 원인 SQL·통계 **미확인** | 인덱스·힌트 **난사** |
| 앱 전역에 **복붙** | 환경·데이터량 바뀌면 **회귀** |
| 업그레이드 직전 **무검증** | 옵티마이저 개선으로 힌트가 **독**이 됨 |
| 라이선스 없이 **Tuning Pack** 기능만 믿기 | Advisor·Profile은 정책 확인 |

---

## 7. SQL Plan Baseline과 관계

[[Oracle DB와 튜닝]] §7.5 — **SQL Plan Baseline** 은 “검증된 플랜만 쓰게” 고정하는 쪽이다.

| | 힌트 (SQL 안) | SQL Plan Baseline |
|--|---------------|-------------------|
| 위치 | 애플리케이션 SQL·뷰 | DB 메타데이터 (`DBA_SQL_PLAN_BASELINES` 등) |
| 변경 | 배포·소스 수정 | DBA·도구로 **플랜 수집·고정** |
| 용도 | **임시**·특정 SQL 한정 | **플랜 회귀 방지**·업그레이드 대비 |
| 관리 | 코드에 흩어짐 | **중앙** 관리 가능 |

힌트로 맞춘 플랜을 Baseline으로 **캡처**해 두고, 장기적으로는 **힌트 제거 + Baseline** 또는 **SQL·통계 개선**으로 가는 팀도 많다.

---

## 8. 현장·[[전자정부프레임워크]] 맥락

| 패턴 | 설명 |
|------|------|
| MyBatis XML | `<select>` 안에 `/*+ ... */` **직접** — 변경 이력·코드 리뷰 필수 |
| 공통 SQL | 힌트 **금지 목록**·승인 절차가 있는 사업 많음 |
| 패키지·뷰 | 뷰 정의에 힌트 → **모든** 조회에 영향 |
| Tibero 등 | Oracle 호환 DB는 **힌트 문법이 비슷**하지만 **100% 동일 아님** |

성능 이슈는 [[Oracle DB와 튜닝]] 순서(**AWR → SQL → 플랜 → 인덱스/통계**)를 따르고, 힌트는 **최후 수단**에 가깝게 둔다.

---

## 9. 실전 체크

- [ ] 힌트 **철자·별칭·인덱스명**이 SQL과 일치하는가  
- [ ] `DISPLAY_CURSOR` / Explain으로 **반영 여부**를 봤는가  
- [ ] **전후** Elapsed·Buffer Gets를 [[Oracle DB와 튜닝]]처럼 비교했는가  
- [ ] 운영 반영 전 **테스트·변경관리**를 거쳤는가  
- [ ] Baseline·Profile 대안을 검토했는가  

---

## 면책

> **면책**  
> 힌트 이름·동작·무시 조건은 **Oracle 버전**마다 다르다. 공식 *SQL Tuning Guide*가 우선.  
> 운영 DB에 힌트·병렬·Baseline 변경은 **백업·롤백·부하 테스트** 후에. 이 글은 **학습·점검용**이며 특정 SQL 패치를 권하지 않는다.

---

## 관련

- [[Oracle DB와 튜닝]]
- [[Oracle 시노님]]
- [[DBeaver 사용법]]
- [[전자정부프레임워크]]
- [[Spring과 Spring Boot 학습]]
- [[생활위키 목차]]
