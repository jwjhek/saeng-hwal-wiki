---
publish: true
draft: false
---

# Oracle DB와 튜닝

> **분류:** 개발 › 프레임워크·DB · [[생활위키 목차]]

Oracle Database의 기본 구조와, 느려졌을 때 **근거 있게** 튜닝하는 방법을 정리한다. 
버전은 19c / 21c / 23ai 등이 현장에 혼재한다. 메뉴·뷰 이름은 버전에 따라 조금 다를 수 있다.

공식 문서: [Oracle Database Documentation](https://docs.oracle.com/en/database/oracle/oracle-database/)

확인일: 2026-08-06 
※ 운영 DB 파라미터·인덱스 변경은 **변경 관리·백업·테스트** 후에. 이 글은 학습·점검용이다.

---

## 1. Oracle이 뭔지 (한 장)

Oracle은 **관계형 DBMS**다. SQL로 데이터를 넣고·읽고·트랜잭션으로 일관성을 지킨다.

| 개념 | 의미 |
|------|------|
| Instance | 메모리(SGA/PGA) + 백그라운드 프로세스. “살아 있는 DB 엔진” |
| Database | 디스크 위의 데이터파일·컨트롤파일·리두 등 물리 파일 집합 |
| Tablespace | 논리 저장 공간. 테이블·인덱스가 여기에 들어감 |
| Schema | 사용자 소유의 객체 묶음 (테이블, 뷰, 프로시저…) |
| Synonym | 다른 스키마 객체 **별칭** — [[Oracle 시노님]] |
| SID / Service | 접속 식별. 요즘은 서비스명 접속이 일반적 |
| Listener | 클라이언트 접속을 받아 인스턴스로 넘김 |

접속 예 (환경마다 다름):

```text
sqlplus user/pass@//host:1521/ORCLPDB1
```

도구: SQL*Plus, SQLcl, [[SQL Developer 사용법]], 모니터링은 OEM/Cloud Control 등.

---

## 2. 아키텍처 핵심 (튜닝에 필요한 만큼)

### 2.1 메모리

| 영역 | 역할 |
|------|------|
| SGA | 인스턴스 공유 메모리. Buffer Cache, Shared Pool, Redo Log Buffer 등 |
| Buffer Cache | 디스크 블록을 메모리에 캐시. 히트율이 낮으면 물리 I/O↑ |
| Shared Pool | SQL 커서, 딕셔너리 캐시. 파싱·하드파스와 관련 |
| PGA | 세션·정렬·해시 조인 등 프로세스별 메모리 |
| Redo Log Buffer | 변경 로그를 리두로 쓰기 전 버퍼 |

`MEMORY_TARGET` / `SGA_TARGET` / `PGA_AGGREGATE_TARGET` 등으로 크기를 관리한다. 
**무작정 키우기 전에** AWR에서 어디가 병목인지 본다.

### 2.2 프로세스 (이름만)

- DBWn: Dirty 버퍼를 데이터파일로 
- LGWR: 리두를 로그 파일로 (커밋 성능과 직결) 
- CKPT, SMON, PMON, ARCn 등 

### 2.3 읽기 경로

```text
SQL → 파싱(공유 커서?) → 실행 계획 → Buffer Cache 조회
 ↓ miss
 디스크 물리 읽기
```

튜닝의 많은 부분은 **불필요한 논리/물리 읽기(Buffer Gets / Disk Reads) 줄이기**다.

---

## 3. 성능이 나쁘다는 신호를 나누기

느리다 ≠ 전부 DB 잘못.

| 증상 | 의심 |
|------|------|
| 특정 화면·리포트만 느림 | SQL / 실행계획 / 인덱스 |
| 특정 시간대만 느림 | 배치, 통계 수집, 백업, peak 락 |
| 전체가 CPU 100% | SQL 비효율, 병렬도, 앱 연결 폭주 |
| I/O wait 우세 | Full scan, 스토리지, temp |
| 커밋·INSERT만 느림 | Redo/undo, 커밋 빈도, 로그 동기화 |
| 앱은 느린데 DB wait 거의 없음 | 앱 서버, 네트워크, 락은 앱 단, 원격 호출 |

**측정 없이 인덱스부터 추가하지 않는다.**

---

## 4. 튜닝 방법론 — 위에서 아래로

실무에서 안전한 순서:

```text
1) 체감 구간 확정 (언제, 어떤 업무, 얼마나)
2) AWR / ASH / ADDM으로 DB Time·Wait·Top SQL 확인
3) 문제 SQL의 실행계획·통계·바인드 확인
4) 최소 변경으로 개선 (SQL → 인덱스/통계 → 계획 고정 → 인프라)
5) 전후 지표 비교 (Elapsed, Buffer Gets, 실행 횟수)
```

한 줄 원칙:

> **DB Time → Wait Class/Event → Top SQL → Plan → 조치**

---

## 5. 진단 도구

### 5.1 AWR (Automatic Workload Repository)

주기적으로 스냅샷을 남겨 **과거 구간** 리포트를 만든다. (Diagnostics Pack 라이선스 주의)

보는 포인트:

- **DB Time / DB CPU** — 부하 크기 
- **Top 5 Timed Events** — 뭐를 기다리거나 CPU를 쓰는지 
- **Load Profile** — 초당 논리읽기, 물리읽기, 파스, 트랜잭션 
- **Top SQL** — Elapsed, CPU, Gets, Reads, Executions 여러 축으로 
- **PGA / SGA / Tablespace I/O**

문제 시각의 스냅샷 구간과, 평소 같은 요일·시간 **베이스라인**을 비교하면 원인 감이 온다.

생성 예 (권한·환경에 따라):

```sql
-- 스냅샷 ID 확인 후
SELECT * FROM TABLE(
 DBMS_WORKLOAD_REPOSITORY.AWR_REPORT_HTML(
 l_dbid, l_inst, start_snap, end_snap
)
);
```

Enterprise Manager에서도 클릭으로 생성 가능하다.

### 5.2 ASH (Active Session History)

약 1초마다 활성 세션을 샘플링. **지금 느릴 때** 또는 AWR보다 짧은 구간에 강하다.

```sql
-- 개념 예시: 최근 대기/SQL 분포 (환경에 맞게 수정)
SELECT NVL(event, 'ON CPU') event, COUNT(*) samples
FROM v$active_session_history
WHERE sample_time > SYSDATE - (10/1440)
GROUP BY NVL(event, 'ON CPU')
ORDER BY samples DESC;
```

### 5.3 ADDM

AWR을 바탕으로 자동 진단·권고. 출발점으로 좋지만, **앱 설계·커밋 패턴**까지는 못 보는 경우가 많다. 권고를 그대로 운영 반영하지 말고 검증한다.

### 5.4 SQL 추적

특정 세션·SQL:

- `DBMS_MONITOR` / SQL Trace + `tkprof` 
- Real-Time SQL Monitoring (`V$SQL_MONITOR`, OEM) — 오래 도는 쿼리 시각화 

### 5.5 실행계획 보기

```sql
EXPLAIN PLAN FOR
SELECT ... ;
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);

-- 실제 실행 후 커서 기준
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY_CURSOR(NULL, NULL, 'ALLSTATS LAST'));
```

`A-Rows` vs `E-Rows` 괴리가 크면 **통계·카디널리티** 문제 가능성이 크다.

---

## 6. Wait Event로 원인 가르기

| Wait / 상태 | 흔히 의미 | 다음에 볼 것 |
|-------------|-----------|--------------|
| ON CPU | 계산·논리적 일 | Top SQL Buffer Gets, 비효율 조인 |
| db file sequential read | 단일 블록(인덱스 타고 테이블 등) | SQL, 인덱스 설계, 캐시 |
| db file scattered read | 멀티블록 = Full scan 성격 | Full table scan이 필요한지, 병렬 |
| log file sync | 커밋 시 LGWR 대기 | 커밋 빈도, 스토리지 로그 지연 |
| enq: TX row lock | 행 락 경합 | 앱 트랜잭션 길이, 인덱스 없는 FK |
| library cache / shared pool | 파스·커서 경합 | 리터럴 SQL, 커서 공유 |
| direct path read/write temp | 정렬·해시가 디스크로 | PGA, SQL 정렬량 |
| gc* (RAC) | 노드 간 블록 전송 | RAC 핫블록, 파티션·앱 친화성 |

Wait만 보고 파라미터를 막 건드리지 말고, **그 wait를 유발한 SQL_ID**를 찾는다.

---

## 7. SQL 튜닝 (효과가 가장 큰 영역)

### 7.1 자주 있는 원인

1. **통계 정보 오래됨 / 잘못됨** → 옵티마이저가 나쁜 플랜 
2. **인덱스 부재·과다·잘못된 컬럼 순서** 
3. **암시적 형변환** (`WHERE char_col = 123`) → 인덱스 비효율 
4. **함수로 컬럼 감싸기** (`WHERE TRUNC(dt) = ...`) 
5. **선택도 낮은 조건만으로 Full scan** 
6. **NESTED LOOPS + 큰 드라이브** / 잘못된 조인 순서 
7. **바인드 피킹**으로 가끔 플랜이 엇나감 
8. **행마다 커밋**하는 배치 

### 7.2 인덱스

| 상황 | 방향 |
|------|------|
| 고선택도 조건 + 자주 조회 | B-Tree 인덱스 검토 |
| 여러 컬럼 조건 | 결합 인덱스, **등호 조건 컬럼을 앞쪽**에 |
| 광범위 범위 검색·집계 | Full scan이 나을 수도. 인덱스≠만능 |
| 과다 인덱스 | DML 느려짐. 안 쓰는 인덱스 정리 |
| FK 컬럼 | 자식 테이블 FK에 인덱스 없으면 부모 DELETE/UPDATE 시 락·Full scan |

생성은 운영 시간에 `ONLINE` 옵션 등을 검토하고, 애플리케이션 회귀 테스트를 한다.

### 7.3 통계

```sql
EXEC DBMS_STATS.GATHER_TABLE_STATS('HR', 'EMPLOYEES', cascade=>TRUE);
-- 스키마/DB 단위 정책은 유지보수 윈도우에 맞춤
```

- 대량 적재 직후 통계 미수집 → 플랜 붕괴 흔함 
- 히스토그램·incremental stats는 대용량·파티션에서 중요 
- `GATHER_STATS_JOB` / Auto stats 설정을 파악해 둘 것 

### 7.4 SQL 작성 습관

- 리터럴 남발보다 **바인드 변수** (파스·공유 풀) 
- `SELECT *` 지양, 필요한 컬럼만 
- 존재 여부만 볼 때 불필요한 정렬·대량 fetch 줄이기 
- 페이지네이션은 버전·패턴에 맞는 방식 (`FETCH FIRST`, 키셋 등) 
- 뷰·인라인 뷰가 옵티마이저를 혼란시키면 단순화 

### 7.5 SQL Tuning Advisor / SQL Profile / Baseline / 힌트

- **SQL Tuning Advisor**: 인덱스·통계·SQL Profile 권고 
- **SQL Profile**: 옵티마이저에 보정 정보 (라이선스·검증 필요) 
- **SQL Plan Baseline**: 검증된 플랜만 사용 → **업그레이드·통계 후 플랜 회귀 방지**에 강함 
- **옵티마이저 힌트** (`/*+ ... */`): SQL 안에서 플랜을 **강하게** 유도 — **남용 금지**, 상세 [[Oracle 힌트]]

23ai 계열에서는 Real-Time SQL Plan Management 등 자동 회귀 대응이 강화되는 추세다. 버전 문서를 확인한다.

---

## 8. 인스턴스·스토리지 쪽 튜닝

SQL이 괜찮은데도 느리면:

| 영역 | 점검 |
|------|------|
| CPU | AAS(평균 활성 세션) vs 코어 수. 과다면 SQL·병렬·앱 동시성 |
| Buffer Cache | 물리 읽기 비율, keep/recycle은 신중히 |
| Redo / Undo | 로그 스위치 빈도, undo 확장, long transaction |
| Temp | 대량 정렬·해시. PGA 부족 신호 |
| 테이블스페이스 | I/O hotspot, 자동 확장 잦은지 |
| 네트워크 | 앱과 DB 왕복, array fetch size |
| RAC | gc wait, 서비스 분리, 핫 블록 |

파라미터 예 (이름만 — 값 복붙 금지):

- `SESSIONS`, `PROCESSES` 
- `OPEN_CURSORS` 
- `PARALLEL_*` 
- `OPTIMIZER_FEATURES_ENABLE` (업그레이드 시 플랜 영향) 

**감으로 `*_CACHE`만 키우는 튜닝은 실패율이 높다.**

---

## 9. 애플리케이션·설계 튜닝 (DBA만의 일이 아님)

| 패턴 | 문제 | 개선 |
|------|------|------|
| N+1 쿼리 | 루프마다 SELECT | 조인·IN·배치 |
| 행 단위 커밋 | log file sync 폭주 | 100~1000행 단위 커밋 등 |
| 넓은 트랜잭션 | 락·undo | 짧게, 순서 일관 |
| 시퀀스+트리거 과다 | 경합 | 캐시 시퀀스, 설계 단순화 |
| 핫 테이블 | 동시 UPDATE | 파티션, 큐, 아키텍처 변경 |
| 연결 누수 | 세션 고갈 | 풀 설정, 타임아웃 |

“DB 튜닝”으로 보이지만 **앱 수정이 정답**인 경우가 절반 이상이다.

---

## 10. 실전 체크리스트

문제 발생 시:

1. [ ] 사용자·화면·시간대를 기록 
2. [ ] 지금이면 ASH / SQL Monitor, 과거면 AWR 
3. [ ] Top Timed Event가 CPU인지 I/O인지 락인지 
4. [ ] Top SQL의 SQL_ID → 텍스트·플랜 
5. [ ] `gets_per_exec`, `elapsed_per_exec`로 “한 번이 무거운지 / 너무 자주인지” 
6. [ ] 통계 수집 시점·데이터 급증 여부 
7. [ ] 최근 배포·인덱스·파라미터·업그레이드 
8. [ ] 조치 후 AWR/실행시간으로 전후 비교 

평소 예방:

1. [ ] 피크 시간 AWR 베이스라인 보관 
2. [ ] 통계 정책·윈도우 문서화 
3. [ ] 중요 SQL Plan Baseline 
4. [ ] 배치 커밋·동시성 가이드를 개발 표준에 
5. [ ] 용량·Temp·Redo 모니터링 알람 

---

## 11. 하면 안 되는 것

- 원인 SQL 없이 인덱스 난사 
- 운영에서 검증 없는 힌트 남발 (`/*+ PARALLEL(256) */` 등) → [[Oracle 힌트]]
- 통계를 잠그거나 fake로 방치 
- 라이선스 없는 Diagnostic/Tuning Pack 기능 무단 사용 
- 피크 시간에 대형 `GATHER` + 풀 스캔 분석 
- “예전에 이렇게 해서 고쳤다”만 반복 (워크로드가 바뀜) 

---

## 12. 용어 빠른 사전

| 용어 | 뜻 |
|------|-----|
| Hard parse | SQL을 새로 최적화. CPU·공유 풀 부담 |
| Soft parse | 기존 커서 재사용 |
| Buffer get | 논리 읽기 (메모리 블록 접근) |
| Cardinality | 예상 행 수. 틀리면 플랜이 망가짐 |
| Selectivity | 조건이 걸러내는 비율 |
| Bind peeking | 첫 바인드 값으로 플랜 결정 |
| Latch / Mutex | 메모리 구조 보호용 내부 락 |
| AAS | Average Active Sessions. 부하의 체감 척도 |

---

## 13. 학습·다음 단계

1. AWR 리포트 한 장을 Top Event → Top SQL 순으로 읽어 보기 
2. 느린 SQL 하나에 `DISPLAY_CURSOR`로 플랜 해석 
3. 개발 DB에서 통계·인덱스 전후 비교 
4. 공식: *Database Performance Tuning Guide*, *SQL Tuning Guide* 
5. 사내 표준(커밋, 스키마 변경, 힌트 금지 목록) 확인 — 힌트·시노님: [[Oracle 힌트]] · [[Oracle 시노님]]

로컬에서 SQL만 다듬을 때는 [[Notepad++ 사용법]], [[VS Code 사용법]], [[Cursor 사용법]]으로 스크립트를 관리하면 편하다. 
긴 매뉴얼 PDF는 [[NotebookLM 사용법]]에 넣어 소화해도 좋다.

---

## 관련

- [[생활위키 목차]]
- [[DBeaver 사용법]] — SQL 실행·스키마 탐색 GUI
- [[Oracle 힌트]] — `/*+ ... */`, 플랜·Baseline
- [[Oracle 시노님]] — private/public synonym, 이름 해석
- [[Cursor 사용법]]
- [[NotebookLM 사용법]]
- [[현존 AI 비교]]
