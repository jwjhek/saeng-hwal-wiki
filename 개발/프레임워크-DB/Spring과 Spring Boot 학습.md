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

확인일: 2026-08-06 
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
- SQL 기초 (JOIN, 트랜잭션 개념)
- Maven 또는 Gradle로 의존성 추가

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

## 6. 데이터 접근

선택지가 여러 개다. **하나만 먼저** 판다.

| 방식 | 특징 | 언제 |
|------|------|------|
| **Spring JDBC** | SQL 직접, 단순 | 소규모·학습 |
| **MyBatis** | SQL을 XML/애너테이션으로 명시 | 공공·복잡 SQL — eGov 다수 |
| **Spring Data JPA** | 메서드 이름·Entity로 매핑 | CRUD 빠른 개발 |
| jOOQ 등 | 타입 세이프 SQL | 팀 표준일 때 |

### JPA

```java
@Entity
public class Member {
 @Id @GeneratedValue
 private Long id;
 private String name;
}

public interface MemberRepository extends JpaRepository<Member, Long> {
 List<Member> findByName(String name);
}
```

주의: N+1, 지연로딩·트랜잭션 범위, 엔티티를 그대로 API에 노출하지 않기 (DTO 권장).

SQL·인덱스 문제는 [[Oracle DB와 튜닝]]으로 이어진다.

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

## 관련

- [[전자정부프레임워크]]
- [[Django Flask FastAPI 학습]]
- [[Java 언어 학습]]
- [[디자인 패턴]]
- [[Oracle DB와 튜닝]]
- [[Docker 사용법]]
- [[쿠버네티스]]
- [[생활위키 목차]]
- [[Cursor 사용법]]
- [[VS Code 사용법]]
- [[NotebookLM 사용법]]
