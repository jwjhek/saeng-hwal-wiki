---
publish: true
draft: false
---

# Spring과 Spring Boot 학습

> **분류:** 개발 › 프레임워크·DB · [[생활위키 목차]]

Java 백엔드의 사실상 표준인 **Spring**과, 그걸 쉽게 기동·구성하게 해 주는 **Spring Boot**를 학습용으로 정리한다. 
공공의 [[전자정부프레임워크]]도 결국 Spring 위에 표준을 얹은 것이다.

공식:

- Spring: [https://spring.io](https://spring.io) 
- Guides: [https://spring.io/guides](https://spring.io/guides) 
- Boot Reference: 버전별 docs.spring.io 

확인일: 2026-08-13 
버전은 빨리 바뀐다. **개념은 동일**하고, 패키지(`jakarta.*`)·Boot major만 사업에 맞추면 된다.

---

## 1. Spring과 Spring Boot는 뭐가 다르나

| | Spring Framework | Spring Boot |
|--|------------------|-------------|
| 정체 | DI·AOP·MVC·트랜잭션 등 **핵심 프레임워크** | Spring을 **제품처럼** 포장한 실행·구성 계층 |
| 설정 | XML / Java Config를 직접 많이 짬 | starter + 자동구성(`auto-configuration`) |
| 서버 | 외부 Tomcat 등에 war 배포가 전통적 | 내장 서버로 `jar` 실행이 기본 |
| 비유 | 엔진·부품 | 조립된 자동차 + 키만 꽂으면 시동 |

```text
당신의 코드
 ↑
Spring Boot (starter, 자동구성, Actuator…)
 ↑
Spring Framework (IoC, MVC, Tx, Security…)
 ↑
JDK + (Jakarta) Servlet / JPA …
```

**학습 순서**: Boot만 만지작거리기 전에 **IoC·빈·DI**를 짧게라도 이해한다. 
Boot는 “설정을 줄여 주는 도구”이지, Spring 개념을 없애 주지 않는다.

### 체감

| 일 | Spring만 (전통) | Spring Boot |
|----|-----------------|-------------|
| 의존성 | 버전을 **하나하나** 맞춤 | `spring-boot-starter-web` 한 줄에 웹 묶음 |
| 톰캣 | 서버에 **따로 설치**하고 war 배포가 많았음 | **내장** 톰캣. `java -jar` 로 실행이 기본 |
| XML | `web.xml`·스프링 XML이 길었음 | `application.yml` + 애너테이션이 흔함 |
| 「빈」 | 직접 등록을 많이 함 | 클래스패스 보고 **자동 구성**. 필요할 때만 덮어씀 |

지금 신규 학습·대부분의 신규 서비스는 **Boot를 쓴다.** 그래도 `@Service`, 트랜잭션, MVC는 **Spring Framework 개념**이다.  
공공 [[전자정부프레임워크]]도 Spring 위이고, 최근 가이드는 Boot 쪽으로 온다.

### 버전 (2026)

| 조합 | 비고 |
|------|------|
| Spring Framework 6 + Boot 3.x | Jakarta(`jakarta.*`), Java 17+. 현장에 아직 많음 |
| Spring Framework 7 + Boot 4.x | 신규·업그레이드 방향. OSS 지원 주기 짧으니 패치 버전 추적 |
| eGovFrame 5.0 | Spring 6대·Jakarta 기준 가이드 — [[전자정부프레임워크]] |

신규 개인 학습: **Java 17 또는 21 + 현재 안정 Boot**로 start.spring.io에서 시작하면 된다. 
회사·공공은 **지정 버전**을 따른다.

---

## 2. 선수 지식

이 정도는 있는 편이 좋다. 부족하면 [[Java 언어 학습]]부터.

- Java OOP, 인터페이스, 예외, 컬렉션
- HTTP / JSON 기초
- SQL 기초 (JOIN, 트랜잭션) — [[SQL 학습]]
- Maven 또는 Gradle로 의존성 추가 — [[Maven과 Gradle]]

있으면 가속:

- 애너테이션, 스트림, Optional/Record
- 디자인 패턴: DI는 **의존성 역전(DIP)** 과 맞닿아 있음 → [[디자인 패턴]]

환경: [[VS Code 사용법]] / IntelliJ / [[Cursor 사용법]] + JDK.

---

## 3. Spring 핵심 — IoC와 DI

### 3.1 IoC (Inversion of Control)

객체를 `new`로 서로 만들고 엮는 대신, **컨테이너(ApplicationContext)** 가 객체 생성·조립·생명주기를 관리한다.

### 3.2 DI (Dependency Injection)

필요한 협력 객체를 생성자가 주입받는다 (권장).

```java
@Service
public class OrderService {
 private final OrderRepository repo;

 public OrderService(OrderRepository repo) { // 생성자 주입
 this.repo = repo;
 }
}
```

| 주입 방식 | 평가 |
|-----------|------|
| 생성자 | 불변, 테스트 쉬움, 권장 |
| setter | 선택 의존에 |
| 필드 `@Autowired` | 간편하지만 테스트·불변에 불리 → 지양 추세 |

### 3.3 Bean

스프링이 관리하는 객체. 
등록: `@Component` / `@Service` / `@Repository` / `@Controller` / `@Configuration` + `@Bean`

스코프: 기본 **singleton** (컨테이너당 하나). 
요청마다 새로면 `prototype` 등 (웹에서는 프록시 이슈 주의).

### 3.4 컨테이너가 하는 일

1. 컴포넌트 스캔 
2. 빈 생성·의존 주입 
3. `@PostConstruct` 등 초기화 
4. AOP 프록시 적용 (트랜잭션 등) 
5. 종료 시 destroy 

---

## 4. AOP와 트랜잭션

### AOP (관점 지향)

로깅, 트랜잭션, 보안처럼 **업무 코드 옆에 반복되는 횡단 관심사**를 분리.

실무에서 가장 많이 쓰는 결과물:

```java
@Transactional
public void placeOrder(...) { ... }
```

### `@Transactional` 주의

- **public** 메서드에 적용되는 것이 기본 프록시 방식 
- **같은 클래스 내부 호출**(`this.method()`)은 프록시를 안 타서 트랜잭션이 안 붙을 수 있음 
- checked 예외는 기본이 롤백 안 함 (`rollbackFor` 확인) 
- 읽기 전용은 `readOnly = true`로 힌트 

---

## 5. 웹 — Spring MVC · REST

원격 호출·키·상태 코드 개념은 [[API]]. 아래는 Spring으로 **만드는** 쪽이다.

### 요청 흐름

```text
HTTP → DispatcherServlet
 → HandlerMapping → Controller
 → Service → Repository
 → View 또는 JSON 응답
```

### 컨트롤러 예

```java
@RestController
@RequestMapping("/api/orders")
public class OrderController {
 private final OrderService service;

 public OrderController(OrderService service) {
 this.service = service;
 }

 @GetMapping("/{id}")
 public OrderResponse get(@PathVariable Long id) {
 return service.get(id);
 }

 @PostMapping
 public ResponseEntity<OrderResponse> create(@RequestBody @Valid CreateOrderRequest req) {
 return ResponseEntity.ok(service.create(req));
 }
}
```

| 애너테이션 | 역할 |
|------------|------|
| `@RestController` | `@Controller` + `@ResponseBody` |
| `@RequestMapping` | URL·메서드 매핑 |
| `@PathVariable` / `@RequestParam` | 경로·쿼리 |
| `@RequestBody` | JSON → 객체 |
| `@Valid` | Bean Validation |

예외는 `@ControllerAdvice` + `@ExceptionHandler`로 공통 JSON 에러 응답을 만든다.

전통 MVC(JSP/Thymeleaf)는 서버 사이드 렌더링. 
현대 API 서버는 `@RestController` + SPA([[전자정부프레임워크]] 현장도 분리 증가).

---

## 6. 데이터 접근 — JDBC · JPA · MyBatis

Java에서 DB를 만지는 **바닥은 JDBC**다. JPA와 MyBatis는 그 위에 올린 **다른 스타일**이다.  
**둘 다 배워야 하는 게 아니다.** 팀 표준 하나를 먼저 판다.

```text
앱 코드
 ↓
JPA (객체 ↔ 표)    또는    MyBatis (SQL을 내가 씀)
 ↓
JDBC
 ↓
DB ([[SQL 학습]] · [[Oracle DB와 튜닝]])
```

| 방식 | 한 줄 | 언제 |
|------|------|------|
| **JDBC** (`JdbcTemplate`) | SQL을 문자열로 실행 | 소규모·학습·특수 쿼리 |
| **JPA** (+ Hibernate 등) | **객체(엔티티)** 를 저장하면 SQL을 **프레임워크가 만듦** | CRUD·연관 관계가 많을 때 |
| **Spring Data JPA** | JPA 위에 **저장소 인터페이스**만 선언 | Boot에서 JPA 쓸 때 기본에 가까움 |
| **MyBatis** | **SQL을 XML(또는 애너테이션)에 직접** 적고 결과만 객체에 꽂음 | 공공·복잡 SQL·튜닝이 잦을 때 — [[전자정부프레임워크]] |

### 6.1 JDBC가 뭔가

Java 표준 **DB 연결 API**. `Connection` → `PreparedStatement` → 결과 행.  
반복 코드가 많아서 Spring은 `JdbcTemplate`으로 줄인다.  
JPA·MyBatis도 **결국 JDBC로 SQL을 보낸다.**

### 6.2 JPA가 뭔가

**JPA**(Jakarta Persistence API, 옛 이름 Java Persistence API)는 **자바 객체와 테이블을 맞추는 표준**이다.  
구현체는 현장이 **Hibernate**인 경우가 많다. 「JPA 쓴다」≈ 보통 **Hibernate로 그 표준을 쓴다.**

**ORM**(객체-관계 매핑)과 **같은 종류**다. Django ORM·SQLAlchemy가 Python에서 하는 일을, Java에서는 JPA(+ Hibernate)가 한다.  
JPA는 ORM **제품 이름**이 아니라 **자바 표준 API**이고, Hibernate가 그 구현이다.

#### Hibernate

**Hibernate**는 Java **ORM 라이브러리**다. JPA 표준보다 **먼저** 나왔고, 지금은 그 표준을 **구현**하는 제품으로 쓰인다.

```text
Spring Data JPA    ← findByName 같은 저장소 (Boot에서 자주)
        ↑
JPA 표준           ← @Entity, EntityManager 규격
        ↑
Hibernate          ← SQL을 만들고 실행 (현장 기본)
        ↑
JDBC → DB
```

EclipseLink 등 다른 JPA 구현도 있으나, Boot `starter-data-jpa`의 **기본은 Hibernate**다.  
`ddl-auto`, 방언(dialect), 2차 캐시 같은 설정 이름은 Hibernate에서 온 것이 많다.

학습은 「Hibernate API를 따로」보다 **JPA 애너테이션 + Spring Data**로 시작하고, 로그에 찍히는 SQL이 Hibernate가 만든 것이라고 보면 된다.

| 용어 | 의미 |
|------|------|
| **엔티티** (`@Entity`) | 표 한 행에 대응하는 **자바 클래스** |
| **영속성 컨텍스트** | 엔티티를 모아 두고, 커밋 때 INSERT/UPDATE를 **모아 실행** |
| **ORM** | Object-Relational Mapping — 객체 ↔ 관계형 표 |

```java
@Entity
public class Member {
  @Id @GeneratedValue
  private Long id;
  private String name;
}

public interface MemberRepository extends JpaRepository<Member, Long> {
  List<Member> findByName(String name);  // 메서드 이름으로 조회 SQL 생성
}
```

`findByName`처럼 **메서드 이름·애너테이션**으로 쿼리를 만드는 층이 **Spring Data JPA**다. JPA 표준만으로도 `EntityManager`를 쓸 수 있다.

| 잘 맞음 | 주의 |
|---------|------|
| 회원·주문처럼 **표와 객체가 비슷** | **N+1** — 목록 후 연관 객체를 한 건씩 또 조회 |
| 트랜잭션 안에서 객체만 고쳐도 UPDATE | **지연 로딩**을 트랜잭션 **밖**에서 치면 오류 |
| 연관(`@ManyToOne` 등) | 엔티티를 API JSON에 **그대로 노출**하지 말 것 (DTO) |
| `jpql` / `QueryDSL`로 조회 | 복잡한 리포트 SQL은 **버거울** 수 있음 → MyBatis·네이티브 쿼리 |

SQL·인덱스가 느리면 실행 계획은 [[SQL 실행 계획]], 튜닝은 [[Oracle DB와 튜닝]].

### 6.3 MyBatis가 뭔가

**SQL 매퍼.** 내가 적은 `SELECT`/`INSERT`를 **메서드에 연결**하고, 결과 행을 객체 필드에 넣는다.  
ORM처럼 객체를 저장한다고 INSERT가 **자동으로 만들어지지는 않는다.** (생성기·플러그인은 별도)

```xml
<!-- mapper XML 예 -->
<select id="findByName" resultType="Member">
  SELECT id, name
    FROM member
   WHERE name = #{name}
</select>
```

```java
@Mapper
public interface MemberMapper {
  List<Member> findByName(String name);
}
```

| 잘 맞음 | 주의 |
|---------|------|
| **조인·힌트·페이징**을 SQL로 정확히 통제 | XML이 늘면 **중복·오타** |
| 공공 eGov, 레거시 오라클 조회 | 동적 SQL(`<if>`)이 복잡해지기 쉬움 |
| DBA와 **실행 계획**을 같이 볼 때 | 객체 그래프(연관 로딩)는 JPA만큼 **자동이 아님** |

예전 이름 **iBatis**의 후신이다. 문서·구글에 iBatis가 나와도 같은 계열로 보면 된다.

### 6.4 무엇으로 고르나

| 상황 | 자주 가는 쪽 |
|------|----------------|
| Boot 개인 학습·CRUD API | **Spring Data JPA** |
| 전자정부·복잡 SELECT·힌트 | **MyBatis** |
| 둘 다 있는 회사 | 도메인 CRUD는 JPA, **리포트·배치 SQL**은 MyBatis — **한 쿼리에 둘을 섞어 배우지 않기** |
| SQL을 아직 모름 | [[SQL 학습]] 먼저. 매퍼·ORM은 SQL을 **숨기지 못한다** |

「JPA가 상위 기술, MyBatis가 구식」이 **아니다.** **누가 SQL을 쓰느냐**가 다를 뿐이다.

SQL·인덱스 문제는 [[SQL 학습]] 다음 [[Oracle DB와 튜닝]]으로 이어진다.

---

## 7. Spring Boot — 쓰는 이유

Boot가 대신 해 주는 것:

1. **starter**로 의존성 묶음 (`spring-boot-starter-web` 등) 
2. **자동 구성** — 클래스패스 보고 DataSource, DispatcherServlet 등을 기본 세팅 
3. **내장 Tomcat(또는 다른 서버)** — `main` 한 번으로 실행 
4. **`application.yml` / `.properties`** — 외부화 설정 
5. **Actuator** — 헬스·메트릭 (운영) 
6. **테스트** — `@SpringBootTest`, MockMvc, Testcontainers 연계 

### 최소 기동

```java
@SpringBootApplication
public class DemoApplication {
 public static void main(String[] args) {
 SpringApplication.run(DemoApplication.class, args);
 }
}
```

`@SpringBootApplication` ≈ `@Configuration` + `@EnableAutoConfiguration` + `@ComponentScan`

### 설정 예 (`application.yml`)

```yaml
server:
 port: 8080
spring:
 datasource:
 url: jdbc:h2:mem:test
 username: sa
 password:
 jpa:
 hibernate:
 ddl-auto: update
```

프로필: `application-local.yml` + `spring.profiles.active=local`

### starter만 알아도 절반

| starter | 용도 |
|---------|------|
| `spring-boot-starter-web` | MVC REST |
| `spring-boot-starter-data-jpa` | JPA |
| `spring-boot-starter-validation` | `@Valid` |
| `spring-boot-starter-security` | 보안 |
| `spring-boot-starter-actuator` | 모니터링 |
| `spring-boot-starter-test` | 테스트 |

[start.spring.io](https://start.spring.io)에서 체크박스로 프로젝트를 받는 것이 입문에 가장 빠르다.

---

## 8. 설정·프로파일·비밀

- 코드에 비밀번호 하드코딩 금지 
- 로컬: yml, 운영: 환경변수 / Secret Manager 
- `spring.config.import` / Vault 등은 팀 표준 
- `@ConfigurationProperties`로 타입 세이프 설정 객체 

자동구성이 맘에 안 들면:

- `application.yml`로 커스터마이즈 
- `@SpringBootApplication(exclude = …)` 
- 필요 시 명시 `@Bean`으로 덮어쓰기 

“Boot가 마법으로 망가뜨렸다”의 대부분은 **의존성·설정 키 오타·프로필 미스**다. 
기동 로그의 `CONDITIONS EVALUATION REPORT` (debug)를 보면 자동구성 여부를 추적할 수 있다.

---

## 9. 보안 맛보기 (Spring Security)

입문 최소:

1. `starter-security` 추가 → 기본 모든 URL 인증 
2. SecurityFilterChain 빈으로 URL 허용/인증 규칙 
3. 비밀번호는 반드시 인코딩 (BCrypt 등) 
4. CSRF: 폼 vs Stateless API(JWT) 전략이 다름 

인증·인가를 대충 끄고 배포하지 말 것. 공공은 별도 보안 가이드·공통모듈이 있다.

---

## 10. 테스트

| 종류 | 애너테이션·도구 |
|------|------------------|
| 단위 | JUnit 5, Mockito — 서비스만 |
| 웹 슬라이스 | `@WebMvcTest` + MockMvc |
| 통합 | `@SpringBootTest` |
| DB | `@DataJpaTest`, Testcontainers |

테스트 없이 `@Transactional`·예외 처리를 믿으면 회귀가 바로 난다.

---

## 11. 추천 학습 로드맵

### 1단계 — 핵심 (1~2주)

1. IoC / DI / Bean 
2. `@SpringBootApplication`으로 Hello API 
3. Controller → Service → (메모리) Repository 
4. DTO + Validation 
5. 전역 예외 처리 

실습: 할 일(Todo) CRUD REST API

### 2단계 — 데이터 (1~2주)

1. H2 또는 로컬 DB 연결 
2. JPA **또는** MyBatis 중 하나 
3. `@Transactional` 시나리오 (성공/롤백) 
4. 간단한 연관관계 또는 JOIN 쿼리 

실습: 회원·주문(또는 게시글·댓글)

### 3단계 — 실무 인접 (2~4주)

1. 프로필·설정 외부화 
2. Spring Security 기초 또는 API Key 
3. Actuator + 로그 포맷 
4. 페이징·검색 
5. 통합 테스트 

### 4단계 — 심화 (필요 시)

- AOP 직접, 이벤트(`ApplicationEvent`) 
- 캐시, 비동기(`@Async`), 스케줄 
- Spring Data REST / QueryDSL 
- WebFlux (리액티브 — 팀 필요할 때만) 
- 클라우드·MSA (Gateway, Config) — Boot 다음에 

### 하지 말 것 (초반)

- 처음부터 MSA·Kafka·MSA 만능 
- JPA+MyBatis+JdbcTemplate 동시 학습 
- 레거시 XML만 잔뜩 보는 것 (개념 이해 후 레거시) 

---

## 12. 전자정부프레임워크와의 관계

```text
eGovFrame = Spring(+MyBatis 등) + 공공 표준 템플릿·공통컴포넌트·점검
```

| Spring 학습 | eGov에서 |
|-------------|---------|
| Controller/Service/DAO | 동일 레이어, 패키지·접두어 관례 |
| DI·Tx | 그대로 사용 |
| Boot 자동구성 | 버전·템플릿에 따라 XML/Boot 혼재 |
| Security | 사이트 공통·보안 모듈과 맞춰야 함 |

Spring을 알면 eGov 코드가 읽힌다. 
eGov만 복사하면 Spring을 몰라도 “동작은” 하지만 **튜닝·장애·업그레이드**에서 막힌다.

상세: [[전자정부프레임워크]]

---

## 13. 자주 하는 실수

| 실수 | 결과 |
|------|------|
| 필드 주입 + 순환 참조 | 기동 실패·설계 냄새 |
| 엔티티 직접 반환 | 지연로딩 예외·보안 누수 |
| 트랜잭션 없는 여러 쓰기 | 부분 커밋 |
| `FetchType.EAGER` 남발 | 성능 저하 |
| 예외를 삼키기 | 롤백 안 됨, 원인 은폐 |
| 프로덕션에 `ddl-auto=update` | 사고 위험 |
| 모든 걸 God Service 하나 | 테스트 불가 |

---

## 14. 미니 실습 커리큘럼 (주차별)

**Week 1** 
start.spring.io → web + validation → Todo API → curl/Postman

**Week 2** 
JPA 또는 MyBatis 연결 → DB 저장 → 예외·검증 메시지 정리

**Week 3** 
페이징·검색·DTO 분리 → `@ControllerAdvice` → 테스트 몇 개

**Week 4** 
프로필·Actuator → (선택) Security → README에 API 명세

막히면 [[Cursor 사용법]]으로 코드 설명을 묻되, **생성 코드를 읽고 DI 흐름을 손으로 그려 보라.**

긴 레퍼런스 PDF는 [[NotebookLM 사용법]]에 넣어도 좋다.

---

## 15. 치트시트

```text
빈 등록 @Component @Service @Repository @Controller @Bean
주입 생성자 권장
웹 @RestController @GetMapping @PostMapping
검증 @Valid @NotNull …
트랜잭션 @Transactional
설정 application.yml , @ConfigurationProperties
부트 진입 @SpringBootApplication
테스트 @SpringBootTest @WebMvcTest @DataJpaTest
```

---

## 16. Django와 (한 장)

Python **Django**는 Boot처럼 **웹을 빨리 올리는 쪽**이지만, **언어·기본 묶음**이 다르다. 표는 [[Django Flask FastAPI 학습]] §2.1.

한 줄: Boot는 Java **부품을 자동으로 조립**, Django는 Python **배터리 포함 풀스택**. 공공 SI는 Boot, 관리 화면·CMS 성격은 Django가 자주 맞다.

---

## 관련

- [[전자정부프레임워크]]
- [[Django Flask FastAPI 학습]] · [[API]]
- [[Java 언어 학습]] · [[JDK]]
- [[SQL 학습]]
- [[디자인 패턴]]
- [[Oracle DB와 튜닝]]
- [[Docker 사용법]]
- [[쿠버네티스]]
- [[생활위키 목차]]
- [[Cursor 사용법]]
- [[VS Code 사용법]]
- [[NotebookLM 사용법]]
