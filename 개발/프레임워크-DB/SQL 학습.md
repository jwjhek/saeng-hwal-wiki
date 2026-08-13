---
publish: true
draft: false
depth: article
aliases:
  - SQL
  - 에스큐엘
  - Structured Query Language
---

# SQL 학습

> **분류:** 개발 › 프레임워크·DB · [[생활위키 목차]]

**SQL**(Structured Query Language)은 관계형 데이터베이스에서 **조회·추가·수정·삭제·구조 정의**를 하는 언어다.  
백엔드([[Spring과 Spring Boot 학습]]·[[Django Flask FastAPI 학습]]), 리포트, 데이터 확인에 공통으로 쓰인다.

이 글은 **표준에 가까운 문법**과 **조인·서브쿼리** 쓰는 법을 정리한다.  
Oracle·PostgreSQL·MySQL·SQL Server는 **방언**이 있어, 함수·페이징·일부 키워드가 다르다.  
튜닝·실행 계획은 [[SQL 실행 계획]] · [[Oracle DB와 튜닝]] · [[Oracle 힌트]].

확인일: 2026-08-13

도구: [[DBeaver 사용법]] · [[SQL Developer 사용법]]

---

## 0. 학습 지도

```text
SELECT · WHERE · ORDER BY · 페이징
 → 함수 · NULL · CASE
 → GROUP BY · HAVING
 → JOIN (내부·외부·자기)
 → 서브쿼리 · WITH(CTE)
 → UNION · 창 함수
 → INSERT/UPDATE/DELETE · 트랜잭션
 → CREATE TABLE · 키 · 인덱스 · 뷰 (맛보기)
```

문법만 외우지 말고, **작은 표 두 개를 만들고 직접 실행**한다.  
운영 DB에 연습 DML을 넣지 않는다.

---

## 1. 무엇인가

| 항목 | 설명 |
|------|------|
| **관계형** | 데이터를 **표(테이블)** 로 두고, 행·열·키로 연결 |
| **선언형** | 「어떻게 읽나」보다 **무엇을 원하는지**를 씀 — 실행 순서는 엔진이 정함 |
| **방언** | 표준 SQL + 제품별 확장. 이 글은 공통을 우선하고, 차이는 **표시** |
| **대소문자** | 키워드는 관례상 대문자. 식별자는 DB·따옴표 설정에 따름 |

| 묶음 | 하는 일 | 예 |
|------|---------|-----|
| **DQL** | 조회 | `SELECT` |
| **DML** | 행 변경 | `INSERT` `UPDATE` `DELETE` |
| **DDL** | 구조 | `CREATE` `ALTER` `DROP` |
| **DCL** | 권한 | `GRANT` `REVOKE` |
| **TCL** | 트랜잭션 | `COMMIT` `ROLLBACK` |

---

## 2. 예제 표 (이 글 공통)

이후 예는 이 두 표를 가정한다.

**dept (부서)**

| dept_id | dept_name |
|---------|-----------|
| 10 | 개발 |
| 20 | 영업 |
| 30 | 인사 |

**emp (사원)**

| emp_id | name | dept_id | salary | hire_date |
|--------|------|---------|--------|-----------|
| 1 | 김개발 | 10 | 400 | 2020-01-01 |
| 2 | 이영업 | 20 | 350 | 2021-03-01 |
| 3 | 박개발 | 10 | 450 | 2019-06-01 |
| 4 | 최프리 | NULL | 300 | 2022-09-01 |

`dept_id`가 비어 있는 행은 **부서 없는 사원**(외부 조인 연습용).

---

## 3. SELECT 기본

```sql
SELECT emp_id, name, salary
FROM emp;
```

| 절 | 역할 |
|----|------|
| `SELECT` | 어떤 **열** (또는 식) |
| `FROM` | 어떤 **표** |
| `*` | 모든 열 — 탐색용. 운영 조회는 **열 이름을 적는** 편이 안전 |

```sql
SELECT name AS 이름, salary * 12 AS 연봉
FROM emp;
```

`AS`는 별칭. 생략해도 되지만, 식을 쓰면 별칭이 읽기 쉽다.

```sql
SELECT DISTINCT dept_id FROM emp;
```

`DISTINCT`는 **중복 행 제거**. 열이 여러 개면 **조합**이 유일해야 한 줄로 남는다.

---

## 4. 필터 · 정렬 · 행 제한

```sql
SELECT name, salary
FROM emp
WHERE salary >= 350
  AND dept_id = 10
ORDER BY salary DESC, name ASC;
```

| 연산 | 예 |
|------|-----|
| 비교 | `=`, `<>`, `<`, `>=` |
| 논리 | `AND` `OR` `NOT` — `OR`는 괄호로 묶기 |
| 목록 | `dept_id IN (10, 20)` |
| 구간 | `salary BETWEEN 300 AND 400` (양 끝 **포함**) |
| 패턴 | `name LIKE '김%'` (`%` 여러 글자, `_` 한 글자) |
| 빈 값 | `dept_id IS NULL` / `IS NOT NULL` — **`= NULL`은 쓰지 않음** |

`WHERE`는 **행을 남길지**. `SELECT` 별칭은 보통 `WHERE`에서 **못 씀** (엔진마다 예외).

### 4.1 상위 N행 (방언)

같은 뜻, 문법이 다름.

| 제품 | 예 |
|------|-----|
| 표준·Oracle 12c+ · PostgreSQL | `FETCH FIRST 10 ROWS ONLY` |
| MySQL | `LIMIT 10` |
| SQL Server | `SELECT TOP 10 ...` |
| 구 Oracle | `WHERE ROWNUM <= 10` (정렬과 **순서 주의**) |

정렬 후 자르려면 **`ORDER BY`가 먼저** 적용되게 쓴다. Oracle 옛 `ROWNUM`은 서브쿼리로 감싸는 패턴이 흔하다.

```sql
SELECT name, salary
FROM emp
ORDER BY salary DESC
FETCH FIRST 3 ROWS ONLY;
```

---

## 5. NULL · 함수 · CASE

`NULL`은 「값 없음」이다. `NULL`과 어떤 연산을 해도 결과는 `NULL`인 경우가 많다.

| 목적 | 공통에 가까운 것 | Oracle에서 자주 봄 |
|------|-----------------|-------------------|
| 빈 값 대체 | `COALESCE(dept_id, 0)` | `NVL(dept_id, 0)` |
| 조건 식 | `CASE WHEN ... THEN ... ELSE ... END` | 같음. `DECODE`도 있음 |
| 문자열 붙임 | `CONCAT`, `\|\|` | `\|\|` |
| 날짜 | 제품마다 **크게 다름** | `TO_DATE`, `TO_CHAR` |

```sql
SELECT name,
       CASE
         WHEN salary >= 400 THEN '상위'
         WHEN salary >= 350 THEN '중간'
         ELSE '그 외'
       END AS grade
FROM emp;
```

문자열 비교·정렬은 **콜레이션·문자셋**에 따라 달라질 수 있다.

---

## 6. 집계 — GROUP BY · HAVING

한 줄로 **여러 행을 요약**한다.

```sql
SELECT dept_id,
       COUNT(*) AS cnt,
       AVG(salary) AS avg_sal,
       MAX(salary) AS max_sal
FROM emp
WHERE salary IS NOT NULL
GROUP BY dept_id
HAVING COUNT(*) >= 1
ORDER BY dept_id;
```

| 함수 | 의미 | NULL |
|------|------|------|
| `COUNT(*)` | 행 수 | 행이면 셈 |
| `COUNT(dept_id)` | 그 열이 **NULL이 아닌** 행 |
| `SUM` `AVG` `MIN` `MAX` | 합·평균·최소·최대 | 보통 NULL 제외 |

```text
FROM → WHERE (행 필터)
 → GROUP BY (그룹)
 → HAVING (그룹 필터)
 → SELECT
 → ORDER BY
```

**규칙:** `SELECT`에 집계가 아닌 열을 넣으면 **`GROUP BY`에도 넣는다.**  
`WHERE`는 그룹 **전**, `HAVING`은 그룹 **후** (`COUNT(*)` 조건을 `WHERE`에 두면 안 됨).

---

## 7. 조인 (JOIN)

두 표의 행을 **키로 붙인다.** 실무 조회 대부분의 핵심이다.

```text
emp.dept_id  ───  dept.dept_id
```

### 7.1 INNER JOIN (내부)

**양쪽 다 맞는 행만.** 부서 없는 `최프리`는 빠진다.

```sql
SELECT e.name, d.dept_name, e.salary
FROM emp e
INNER JOIN dept d ON e.dept_id = d.dept_id;
```

`INNER`는 생략하는 경우가 많다 (`JOIN`만 써도 내부 조인).

옛 방식(비권장에 가까움):

```sql
SELECT e.name, d.dept_name
FROM emp e, dept d
WHERE e.dept_id = d.dept_id;
```

조건이 빠지면 **곱집합**이 나와 행이 폭증한다. **`ON`/`USING`을 쓰는 JOIN 문법**을 권한다.

### 7.2 LEFT / RIGHT / FULL (외부)

| 종류 | 남기는 쪽 |
|------|-----------|
| `LEFT JOIN` | 왼쪽 표 **모든 행**. 오른쪽 없으면 열은 NULL |
| `RIGHT JOIN` | 오른쪽 기준 (왼쪽을 기준으로 `LEFT` 쓰는 편이 읽기 쉬움) |
| `FULL OUTER JOIN` | 양쪽 다. MySQL은 오래 **미지원** → `UNION`으로 흉내 |

```sql
SELECT e.name, d.dept_name
FROM emp e
LEFT JOIN dept d ON e.dept_id = d.dept_id;
```

`최프리`는 `dept_name`이 NULL인 채로 남는다.

**함정:** `LEFT JOIN` 뒤에 오른쪽 표 조건을 `WHERE d.dept_id = 10`처럼 쓰면, NULL 행이 떨어져 **내부 조인처럼** 된다.  
오른쪽 필터는 `ON`에 두거나, 「내부 조인이 맞는지」를 먼저 정한다.

### 7.3 CROSS JOIN

조건 없이 모든 조합. 의도적으로 쓸 때만.

```sql
SELECT e.name, d.dept_name
FROM emp e
CROSS JOIN dept d;
```

### 7.4 자기 조인 (같은 표 두 번)

상사·계층처럼 **한 표를 별칭 두 개**로 붙인다.

```sql
-- emp에 manager_id가 있다고 가정
SELECT e.name AS 사원, m.name AS 상사
FROM emp e
LEFT JOIN emp m ON e.manager_id = m.emp_id;
```

### 7.5 조인 여러 개

```sql
SELECT ...
FROM a
JOIN b ON a.id = b.a_id
JOIN c ON b.id = c.b_id
LEFT JOIN d ON c.id = d.c_id;
```

**키를 명확히.** 이름이 같은 열은 `e.dept_id`처럼 **표 별칭**을 붙인다.

---

## 8. 서브쿼리

쿼리 **안에 쿼리**. 괄호로 묶는다.

### 8.1 스칼라 (값이 하나)

```sql
SELECT name, salary,
       (SELECT AVG(salary) FROM emp) AS avg_all
FROM emp;
```

행마다 바깥 평균을 붙인다. 결과가 **2행 이상이면 오류**인 제품이 많다.

### 8.2 IN / NOT IN

```sql
SELECT name
FROM emp
WHERE dept_id IN (SELECT dept_id FROM dept WHERE dept_name = '개발');
```

`NOT IN` 서브쿼리에 **NULL이 있으면** 전체가 비는 제품이 있다 → `NOT EXISTS`가 안전한 경우가 많음.

### 8.3 EXISTS (상관)

바깥 행과 **연결되어** 안쪽을 본다. 「있느냐」만 보면 될 때 유리한 경우가 많다.

```sql
SELECT d.dept_name
FROM dept d
WHERE EXISTS (
  SELECT 1
  FROM emp e
  WHERE e.dept_id = d.dept_id
    AND e.salary >= 400
);
```

`SELECT 1`은 「존재 여부」만 쓴다는 뜻. 안쪽 열 값은 보통 안 쓴다.

상관 서브쿼리는 바깥 행 수만큼 안쪽이 돌 수 있어, **조인·EXISTS·IN** 중 실행 계획을 보고 고른다 → [[SQL 실행 계획]] · [[Oracle DB와 튜닝]].

### 8.4 FROM 절 인라인 뷰

```sql
SELECT x.dept_id, x.avg_sal
FROM (
  SELECT dept_id, AVG(salary) AS avg_sal
  FROM emp
  GROUP BY dept_id
) x
WHERE x.avg_sal >= 350;
```

집계한 뒤에 다시 거를 때. Oracle에서 페이징·ROWNUM 패턴에도 자주 쓴다.

### 8.5 서브쿼리로 갱신 (맛보기)

```sql
UPDATE emp
SET salary = salary + 10
WHERE dept_id = (SELECT dept_id FROM dept WHERE dept_name = '개발');
```

서브쿼리가 **한 값**이어야 `=`가 성립. 여러 부서면 `IN`.

---

## 9. WITH (공통 테이블 식, CTE)

서브쿼리에 **이름**을 붙인다. 같은 묶음을 여러 번 쓸 때 읽기 좋다.

```sql
WITH dept_avg AS (
  SELECT dept_id, AVG(salary) AS avg_sal
  FROM emp
  GROUP BY dept_id
)
SELECT e.name, e.salary, a.avg_sal
FROM emp e
JOIN dept_avg a ON e.dept_id = a.dept_id
WHERE e.salary >= a.avg_sal;
```

재귀 `WITH`는 계층(조직도)에 쓰인다. 문법은 제품마다 조금 다르다.

---

## 10. 집합 연산

위아래로 **결과 집합을 합치거나 뺀다.** 열 개수·타입이 맞아야 한다.

| 연산 | 의미 | 중복 |
|------|------|------|
| `UNION` | 합집합 | 제거 |
| `UNION ALL` | 합치기 | **유지** (보통 더 빠름) |
| `INTERSECT` | 교집합 | Oracle·PostgreSQL 등 |
| `EXCEPT` / `MINUS` | 차집합 | SQL Server `EXCEPT`, Oracle `MINUS` |

```sql
SELECT dept_id FROM emp
UNION ALL
SELECT dept_id FROM dept;
```

`ORDER BY`는 **맨 마지막**에 한 번.

---

## 11. 창 함수 (WINDOW)

집계처럼 계산하되, **행을 접지 않고** 옆에 붙인다. `GROUP BY`와 역할이 다르다.

```sql
SELECT name, dept_id, salary,
       AVG(salary) OVER (PARTITION BY dept_id) AS dept_avg,
       ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rn
FROM emp;
```

| 함수 | 쓰임 |
|------|------|
| `ROW_NUMBER()` | 그룹 안 순번 (중복 없이) |
| `RANK()` / `DENSE_RANK()` | 순위 (동점 처리가 다름) |
| `SUM() OVER (...)` | 누적·그룹 합을 행마다 |
| `LAG` / `LEAD` | 이전·다음 행 |

「부서별 급여 1등만」은 창 함수 후 `WHERE rn = 1` (인라인 뷰·CTE로 감싸기).

구버전·일부 엔진은 창 함수가 약하다. 그때는 서브쿼리로 대체한다.

---

## 12. INSERT · UPDATE · DELETE

```sql
INSERT INTO emp (emp_id, name, dept_id, salary, hire_date)
VALUES (5, '정신규', 20, 320, DATE '2024-01-01');

INSERT INTO emp (emp_id, name, dept_id, salary, hire_date)
SELECT 6, name, 10, salary, hire_date
FROM emp
WHERE emp_id = 1;
```

날짜 리터럴은 `DATE '2024-01-01'`(표준에 가까움) / Oracle `TO_DATE(...)` / MySQL `'2024-01-01'` 등.

```sql
UPDATE emp
SET salary = salary + 20
WHERE dept_id = 20;

DELETE FROM emp
WHERE emp_id = 5;
```

**`WHERE` 없는 `UPDATE`/`DELETE`는 표 전체**다. 실행 전 `SELECT`로 대상 행을 확인한다.

---

## 13. 트랜잭션

여러 DML을 **전부 반영하거나 전부 취소**.

```sql
BEGIN;          -- PostgreSQL 등. Oracle은 보통 자동으로 트랜잭션 시작
UPDATE emp SET salary = salary - 10 WHERE emp_id = 1;
UPDATE emp SET salary = salary + 10 WHERE emp_id = 2;
COMMIT;         -- 확정
-- ROLLBACK;    -- 취소
```

| 개념 | 설명 |
|------|------|
| `COMMIT` | 확정. 다른 세션에 보임 (격리 수준에 따름) |
| `ROLLBACK` | 되돌림 |
| `SAVEPOINT` | 중간 지점만 되돌리기 |

[[DBeaver 사용법]]의 **Auto-commit**이 켜져 있으면 문장마다 커밋된다. 연습·운영 모두 **의도를 확인하고** 끈다.

격리 수준(더티 리드 등)은 DB마다 기본값이 다르다. 「동시에 두 사람이 같은 행」이면 잠금·오류가 날 수 있다.

---

## 14. DDL 맛보기 (표·키·인덱스)

```sql
CREATE TABLE dept (
  dept_id   INTEGER PRIMARY KEY,
  dept_name VARCHAR(40) NOT NULL
);

CREATE TABLE emp (
  emp_id    INTEGER PRIMARY KEY,
  name      VARCHAR(40) NOT NULL,
  dept_id   INTEGER REFERENCES dept (dept_id),
  salary    INTEGER,
  hire_date DATE
);

CREATE INDEX idx_emp_dept ON emp (dept_id);
```

| 개념 | 역할 |
|------|------|
| **PRIMARY KEY** | 행 식별. NULL 불가·유일 |
| **FOREIGN KEY** | 다른 표의 키를 가리킴. 조인의 **의미** |
| **INDEX** | 찾기 빠르게. 쓰기 비용↑. 남발 금지 — [[Oracle DB와 튜닝]] |
| `VARCHAR` / `VARCHAR2` | 문자열. Oracle은 `VARCHAR2`가 흔함 |
| `INTEGER` / `NUMBER` | 숫자 타입 이름이 제품마다 다름 |

`DROP TABLE emp;` 은 **구조와 데이터 삭제**. 되돌리기 어렵다.

---

## 15. 뷰

자주 쓰는 `SELECT`에 이름. 권한·복잡도 숨김에 쓴다.

```sql
CREATE VIEW v_emp_dept AS
SELECT e.emp_id, e.name, d.dept_name, e.salary
FROM emp e
LEFT JOIN dept d ON e.dept_id = d.dept_id;

SELECT * FROM v_emp_dept WHERE salary >= 400;
```

뷰를 갱신할 수 있는지는 **정의·키·제품**에 따라 갈린다. 복잡한 조인 뷰는 조회 전용으로 보는 편이 안전하다.

[[Oracle 시노님]]은 **별칭(다른 스키마 객체 이름)** 이지 뷰와 다르다.

---

## 16. 조인 vs 서브쿼리 (언제)

정답은 하나 없고, **읽기 + [[SQL 실행 계획]]**으로 고른다.

| 상황 | 자주 쓰는 쪽 |
|------|----------------|
| 여러 열을 한 결과로 | **JOIN** |
| 「이 조건의 부서에 속한 사원」 | `IN` 서브쿼리 또는 JOIN |
| 「그런 행이 **있기만** 하면」 | `EXISTS` |
| 집계한 뒤 다시 비교 | CTE·인라인 뷰·창 함수 |
| 상관 서브쿼리가 느림 | JOIN으로 바꿔 비교 |

같은 결과가 나와도 **비용이 다를 수 있다.** 느리면 힌트부터가 아니라 **조건·인덱스·조인 키**를 본다.

---

## 17. 흔한 실수

| 실수 | 고치기 |
|------|--------|
| `WHERE col = NULL` | `IS NULL` |
| `LEFT JOIN` + 오른쪽 `WHERE` | 내부 조인이 됨. `ON` 또는 의도 확인 |
| `GROUP BY` 빠진 열 | `SELECT`의 비집계 열을 그룹에 |
| 콤마 조인에 `WHERE` 누락 | 행 폭증 — `JOIN ... ON` |
| `NOT IN (NULL 포함)` | 빈 결과 — `NOT EXISTS` |
| `SELECT *` 운영 API | 열 고정, 불필요 I/O |
| `DELETE`/`UPDATE`에 `WHERE` 없음 | 먼저 `SELECT` |
| 문자열에 숫자 비교 암묵 변환 | 인덱스 못 탐. 타입 맞추기 |

---

## 18. 실습 체크

작은 표로 아래를 **직접 실행**해 본다.

- [ ] 급여 350 이상, 급여 내림차순  
- [ ] 부서명과 사원명 **내부 조인** / **왼쪽 조인** 결과 차이 (최프리)  
- [ ] 부서별 인원·평균 급여  
- [ ] 평균보다 급여 높은 사원 (서브쿼리 또는 CTE)  
- [ ] 부서별 급여 순번 (`ROW_NUMBER` 또는 서브쿼리)  
- [ ] 트랜잭션: 두 `UPDATE` 후 `ROLLBACK` 되는지  

그다음: [[SQL 실행 계획]]으로 플랜을 보고, [[Oracle DB와 튜닝]]에서 인덱스.

---

## 19. 정리

| 항목 | 한 줄 |
|------|--------|
| 조회 | `SELECT` → `FROM` → `JOIN` → `WHERE` → `GROUP BY` → `HAVING` → `ORDER BY` |
| 조인 | 키로 붙임. 외부 조인은 NULL 행. `ON`과 `WHERE`를 섞지 않기 |
| 서브쿼리 | 값·목록·존재·인라인 뷰. 상관은 계획 확인 |
| 집계 vs 창 | 접기 vs 행 유지 |
| 변경 | `WHERE` 확인, 트랜잭션, 운영에서 Auto-commit 주의 |

문법 뼈대 다음에 **실행 계획**이 실무다.

---

## 면책

> **면책**  
> 교육용 요약이며 **특정 DB 매뉴얼·운영 절차가 아니다.**  
> 키워드·함수·페이징·트랜잭션 기본값은 **제품·버전**마다 다르다. 공식 문서와 실행으로 확인한다.  
> 운영 데이터에 연습 DML·DDL을 실행하지 않는다.

---

## 관련

- [[생활위키 목차]]
- [[DBeaver 사용법]]
- [[SQL Developer 사용법]]
- [[SQL 실행 계획]]
- [[Oracle DB와 튜닝]]
- [[Oracle 힌트]]
- [[Oracle 시노님]]
- [[Spring과 Spring Boot 학습]]
- [[Java 언어 학습]]
