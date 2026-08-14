---
publish: true
draft: false
---

# Java 언어 학습

> **분류:** 개발 › 언어 · [[생활위키 목차]]

Java는 **객체지향 + JVM** 위에서 동작하는 정적 타입 언어다. 
백엔드([[Spring과 Spring Boot 학습]]), 공공([[전자정부프레임워크]]), Android(최근은 Kotlin 비중↑) 등에 쓰인다.  
설치·LTS·JAVA_HOME은 [[JDK]].

공식·학습:

- [Oracle Java Documentation](https://docs.oracle.com/en/java/) 
- [OpenJDK](https://openjdk.org/) 

확인일: 2026-08-06 
문법 예시는 **Java 17+**으로 적되, 구버전(8/11)과 다른 점은 표시한다. 현장 LTS는 11·17·21이 흔하고, 신규는 21/25도 늘어난다.

---

## 0. 학습 지도

```text
기초 타입·연산·제어문·배열·메서드·클래스
중급 상속·인터페이스·예외·컬렉션·제네릭·I/O
실무 스트림·동시성·JVM·모듈·신문법(Record…)
연계 Spring / JDBC·JPA / 테스트
```

하루에 문법만 암기하지 말고, **작은 프로그램을 직접 컴파일·실행**하는 편이 빠르다. 
도구: [[JDK]] + [[VS Code 사용법]] / IntelliJ / [[Cursor 사용법]]

---

# Part 1 — 기초

## 1. Java가 실행되는 방식

```text
.java (소스) → javac → .class (바이트코드) → JVM이 해석/JIT 컴파일 → 실행
```

- **WORA**: Write Once, Run Anywhere (같은 바이트코드를 여러 OS JVM에서) 
- **[[JDK]]**: 개발 도구 (`javac`, 라이브러리). 배포·LTS·`JAVA_HOME`은 그 글 
- **JRE**: 실행만 (요즘 JDK에 포함되는 배포가 일반적) 

```bash
javac Hello.java
java Hello
```

빌드 도구(Maven/Gradle)를 쓰면 위 과정을 자동화한다.

## 2. 프로그램 골격

```java
public class Hello {
 public static void main(String[] args) {
 System.out.println("Hello");
 }
}
```

- `public class` 이름 = 파일명 (`Hello.java`) 
- 진입점: `public static void main(String[] args)` 
- 패키지: `package com.example;` — 디렉터리 구조와 일치 

## 3. 타입

### 원시 타입 (primitive)

| 타입 | 크기 | 예 |
|------|-----------|-----|
| `byte` | 1바이트 | 파일·버퍼 |
| `short` | 2 | 거의 안 씀 |
| `int` | 4 | 기본 정수 |
| `long` | 8 | `100L` |
| `float` | 4 | `1.0f` |
| `double` | 8 | 기본 실수 |
| `char` | 2 (UTF-16 코드유닛) | `'A'` |
| `boolean` | true/false | |

### 참조 타입

클래스, 배열, 인터페이스, enum… — 변수는 **객체의 주소(참조)** 를 담는다.

```java
String a = "hi"; // 참조
String b = a; // 같은 대상을 가리킬 수 있음
int x = 10; // 값 자체
```

`null`: 참조가 아무 객체도 가리키지 않음 → NPE 주의.

### 박싱

`int` ↔ `Integer` 자동 박싱/언박싱. 
컬렉션은 원시 타입을 못 담아 `List<Integer>`를 쓴다. 루프에서 박싱 남발은 성능 비용.

## 4. 연산·제어문

- 산술: `+ - * / %` 
- 비교·논리: `== != < > && || !` 
- 참조 동등: `==`는 주소, 문자열 내용 비교는 **`equals`** 
- `if / else`, `switch` (Java 14+ 화살표·yield 가능) 
- `for`, 향상 for, `while`, `do-while` 
- `break` / `continue` 

```java
String day = "MON";
switch (day) {
 case "MON", "TUE" -> System.out.println("weekday");
 default -> System.out.println("other");
}
```

## 5. 배열

```java
int[] a = new int[3];
int[] b = {1, 2, 3};
for (int n : b) { ... }
```

길이는 `arr.length`. 다차원: `int[][] m`.

## 6. 메서드

```java
public static int add(int a, int b) {
 return a + b;
}
```

- 오버로딩: 같은 이름, 다른 파라미터 목록 
- `varargs`: `void log(String... msgs)` 
- 반환 없으면 `void` 

## 7. 클래스와 객체

```java
public class User {
 private final String name; // 필드
 public User(String name) { // 생성자
 this.name = name;
 }
 public String getName() { // 메서드
 return name;
 }
}
```

| 개념 | 의미 |
|------|------|
| 필드 | 상태 |
| 생성자 | 초기화 |
| 메서드 | 행동 |
| `this` | 자기 자신 |
| `static` | 인스턴스 없이 클래스에 속함 |
| 접근제어 | `private` `package` `protected` `public` |

캡슐화: 필드는 private, 필요 시 getter/setter (불변이면 setter 없음이 나음).

---

# Part 2 — 중급 (객체지향·핵심 API)

## 8. 상속과 다형성

```java
public class Animal {
 public void speak() { System.out.println("..."); }
}
public class Dog extends Animal {
 @Override
 public void speak() { System.out.println("멍"); }
}
Animal a = new Dog(); // 업캐스트
a.speak(); // 멍 — 동적 바인딩
```

- 단일 클래스 상속 (`extends` 하나) 
- `super`로 부모 생성자/메서드 
- `abstract class`: 인스턴스화 불가, 추상 메서드 가능 
- `final` 클래스/메서드: 상속·오버라이드 금지 

**구성(has-a)을 상속(is-a)보다 우선**하는 편이 설계가 안전한 경우가 많다.

## 9. 인터페이스

```java
public interface Payment {
 void pay(int amount);
 default void log() { System.out.println("pay"); } // default 메서드
}
```

- 다중 구현 가능 (`implements A, B`) 
- Java 8+: `default` / `static` 메서드 
- 함수형 인터페이스: 추상 메서드 1개 → 람다 대상 (`@FunctionalInterface`) 

## 10. 예외

```text
Throwable
├── Error (시스템 — 보통 앱이 복구 안 함)
└── Exception
 ├── RuntimeException (unchecked — NPE, IAE…)
 └── 그 외 checked (IOException… — 선언/처리 강제)
```

```java
try {
 Files.readString(path);
} catch (IOException e) {
 throw new IllegalStateException("read fail", e); // 원인 보존
} finally {
 // 정리
}
```

- try-with-resources: `try (var in = …) { }` → AutoCloseable 자동 close 
- 예외를 삼키지(`catch` 빈칸) 말 것 
- 비즈니스 예외는 unchecked로 설계하는 팀도 많음 (Spring과 잘 맞음) 

## 11. 문자열·공통 유틸

- `String` 불변. `+` 반복은 `StringBuilder` 
- `equals` / `hashCode` 계약 — HashMap 키에 필수 
- `Objects.equals`, `Objects.requireNonNull` 
- `Optional<T>`: null 대신 “값 없을 수 있음” — 필드보다 **반환 타입**에 적합 

```java
Optional<User> find(long id);
user.orElseThrow(() -> new NoSuchElementException());
```

## 12. 컬렉션

```text
Collection
├── List ArrayList, LinkedList
├── Set HashSet, LinkedHashSet, TreeSet
└── Queue ArrayDeque, PriorityQueue
Map (별계열) HashMap, LinkedHashMap, TreeMap, ConcurrentHashMap
```

| 구현 | 특징 |
|------|------|
| `ArrayList` | 랜덤 접근 빠름, 기본 List |
| `HashMap` | 키-값, 순서 없음 (Java 이후 일부 순서 특성이 있어도 의존 말 것) |
| `LinkedHashMap` | 삽입 순서 |
| `TreeMap/Set` | 정렬, Comparable/Comparator |
| `ArrayDeque` | 스택·큐 |

```java
List<String> list = new ArrayList<>();
Map<String, Integer> map = new HashMap<>();
for (var e : map.entrySet()) { ... }
```

동시성: `ConcurrentHashMap`, `CopyOnWriteArrayList` 등 — 일반 List를 멀티스레드로 공유하지 말 것.

## 13. 제네릭

```java
public class Box<T> {
 private T value;
 public void set(T value) { this.value = value; }
 public T get() { return value; }
}
```

- 타입 소거(erasure): 런타임에 `T` 정보는 대부분 사라짐 
- 와일드카드: `List<? extends Number>` (생산자), `List<? super Integer>` (소비자) — PECS 
- 제한: `T extends Comparable<T>` 

원시 타입 `List` (제네릭 없이)는 쓰지 말 것.

## 14. enum

```java
public enum Status {
 READY, RUN, DONE;
}
```

필드·메서드·생성자를 가질 수 있어 **상수 그룹 + 행위**에 적합. `switch`와 잘 맞음.

## 15. I/O · NIO.2

```java
String text = Files.readString(Path.of("a.txt")); // Java 11+
Files.writeString(path, text);
try (var lines = Files.lines(path)) {
 lines.filter(s -> !s.isBlank()).forEach(System.out::println);
}
```

- `java.io` 전통 스트림 
- `java.nio.file.Files` / `Path` 권장 
- 문자 인코딩: `StandardCharsets.UTF_8` 명시 

---

# Part 3 — 중상급 (모던 Java · 실무)

## 16. 람다와 스트림

```java
list.stream()
 .filter(s -> s.length() > 3)
 .map(String::toUpperCase)
 .sorted()
 .toList(); // Java 16+ (불변 리스트)
```

| 개념 | 예 |
|------|-----|
| Predicate | `x -> x > 0` |
| Function | `s -> s.length()` |
| Consumer | `System.out::println` |
| Supplier | `() -> new Token()` |
| 메서드 참조 | `User::getName`, `ArrayList::new` |

주의:

- 스트림은 **한 번만** 소비 
- 부작용(외부 변수 mutate) 최소화 
- 병렬 스트림(`parallelStream`)은 과제·오버헤드 이해하고 사용 
- 복잡한 로직은 가독성을 위해 일반 for가 나을 수 있음 

## 17. 날짜·시간 (java.time)

`Date` / `Calendar` 대신:

- `LocalDate`, `LocalDateTime`, `Instant` 
- `ZonedDateTime`, `Duration`, `Period` 
- 포맷: `DateTimeFormatter` 

타임존·서머타임 버그는 `LocalDateTime`만으로 서버 시각을 표현할 때 자주 난다. 저장은 `Instant` UTC가 안전한 경우가 많다.

## 18. 예외·리소스 · record · sealed (신문법)

### Record (Java 16+)

```java
public record Point(int x, int y) {}
```

불변 데이터 운반. equals/hashCode/toString 자동. DTO에 적합.

### Sealed class (Java 17+)

```java
public sealed interface Shape permits Circle, Rect {}
```

하위 타입을 제한 → switch 패턴매칭과 함께 도메인 모델링.

### Pattern matching

```java
if (obj instanceof String s) {
 System.out.println(s.length());
}
```

`switch` 패턴(버전별 확대)으로 타입 분기 단순화.

### Text block (Java 15+)

```java
String json = """
 {"a": 1}
 """;
```

### var (Java 10+)

지역 변수 타입 추론. 필드·파라미터에는 못 씀. 남발 시 가독성↓.

## 19. 동시성

```java
ExecutorService pool = Executors.newFixedThreadPool(4);
Future<Integer> f = pool.submit(() -> compute());
int v = f.get();
pool.shutdown();
```

| 도구 | 용도 |
|------|------|
| `Thread` / `Runnable` | 기초 |
| `ExecutorService` | 스레드 풀 |
| `synchronized` / `ReentrantLock` | 상호 배제 |
| `volatile` | 가시성 (원자 복합연산은 아님) |
| `AtomicInteger` 등 | 락 없는 카운터 |
| `CompletableFuture` | 비동기 파이프라인 |
| Virtual Threads (21+) | 대량 블로킹 I/O에 경량 스레드 |

규칙:

- 공유 가변 상태를 줄인다 
- 데드락: 락 순서 일관 
- UI/요청 스레드에서 긴 작업 금지 → 풀로 

Spring `@Async`·리액티브는 이 개념 위에 있다.

## 20. JVM

| 영역 | 의미 |
|------|------|
| Heap | 객체. GC 대상 |
| Stack | 호출·로컬 변수 (스레드별) |
| Metaspace | 클래스 메타데이터 |
| GC | 가비지 컬렉션 — STW·할당량 튜닝은 운영 이슈 |

툴: `jcmd`, `jfr`, 힙덤프, GC 로그. 
`OutOfMemoryError`, 메모리 누수(캐시에 무한 put)를 의한다.

컴파일: javac → 바이트코드, HotSpot JIT가 hot method를 네이티브로.

## 21. 모듈 (JPMS) — 알아두기

`module-info.java`로 패키지 공개 범위를 제한. 
앱 서버·Spring 쪽은 **아직 classpath 중심**인 경우도 많으나, JDK 자체는 모듈화되어 있다. 입문 필수까지는 아님.

## 22. 애너테이션·리플렉션

```java
@Deprecated
@Override
@SuppressWarnings("unchecked")
```

커스텀 애너테이션 + 리플렉션은 프레임워크(Spring)의 기반. 
직접 `Class.forName`·setAccessible은 보안·성능·모듈 벽 때문에 신중히.

---

# Part 4 — 실무 습관 · 심화 주제

## 23. equals / hashCode / Comparable

```java
@Override
public boolean equals(Object o) { ... }
@Override
public int hashCode() { ... }
```

Record는 자동. 클래스 직접 쓸 때 IDE 생성 또는 Objects.hash. 
정렬: `Comparable` 자연 순서, `Comparator` 외부 전략.

## 24. 불변·방어적 복사

- 가능하면 불변 객체 (record, final 필드) 
- 컬렉션 노출 시 `List.copyOf` / unmodifiable 
- 생성자에서 널·범위 검증 

## 25. 제네릭·와일드카드 심화 포인트

- `List<String>`은 `List<Object>`의 서브타입이 **아님** (불공변) 
- 배열은 공변 → 런타임 ArrayStoreException 위험 → 컬렉션 권장 
- 헬퍼 메서드에 `<T>` 선언 

## 26. 성능 (성급한 최적화 금지)

1. 알고리즘·DB 쿼리가 대개 병목 ([[Oracle DB와 튜닝]]) 
2. 불필요 박싱, 스트림 남발, 로그 문자열 조립 
3. `+`로 거대한 문자열 루프 
4. 프로파일러 없이 감으로 synchronized 제거하지 말 것 

## 27. 테스트

- JUnit 5: `@Test`, `@ParameterizedTest` 
- AssertJ / Hamcrest 
- Mockito로 의존 대체 
- 단위(순수 로직) vs 통합(스프링 컨텍스트) 

## 28. 빌드 · 의존성

```text
Maven pom.xml / Gradle build.gradle
```

- 의존성 버전·BOM 
- `src/main/java`, `src/test/java` 
- 패키지 네이밍: `com.company.project` 

---

# Part 5 — 로드맵 · 체크리스트

## 29. 단계별 로드맵

**기초 (1~2주)** 
타입, 제어문, 배열, 클래스, 메서드, 패키지, main 실행

**중급 (2~4주)** 
상속·인터페이스·예외·컬렉션·제네릭·enum·파일 I/O 
실습: 콘솔 게시판, 단어 통계

**모던 Java (2주)** 
람다·스트림·java.time·Optional·record 
실습: CSV 읽어 집계

**설계 (병행 권장)** 
[[디자인 패턴]] — Strategy·Factory·Builder 등

**동시성·JVM (필요 시)** 
Executor, Future, 동시 컬렉션, 가상 스레드 맛보기

**프레임워크 진입** 
[[Spring과 Spring Boot 학습]] → JDBC/JPA → [[전자정부프레임워크]]

## 30. 스스로 점검 리스트

기초

- [ ] `==` vs `equals` 
- [ ] static vs instance 
- [ ] 배열과 List 차이 
- [ ] checked vs unchecked 

중급

- [ ] 오버라이드와 `@Override` 
- [ ] HashMap에 커스텀 키 넣을 때 hashCode 
- [ ] try-with-resources 
- [ ] 제네릭으로 타입 안전한 API 

심화

- [ ] 스트림으로 그룹핑(`Collectors.groupingBy`) 
- [ ] 스레드 안전하게 카운터 증가 
- [ ] record로 DTO 설계 
- [ ] NPE 없는 API (Optional·검증) 

## 31. 피해야 할 습관

| 습관 | 이유 |
|------|------|
| 모든 것을 static | 테스트·교체 불가 |
| 예외 삼키기 | 장애 은폐 |
| raw type (`List`) | 타입 안전 붕괴 |
| public 필드 | 캡슐화 파괴 |
| `Date` 신규 코드 | java.time 사용 |
| `System.out`만으로 운영 로그 | 로거 사용 |
| null 범벅 도메인 | Optional·실패 타입·검증 |

---

## 32. 다른 문서와 연결

| 다음 | 문서 |
|------|------|
| 설계·패턴 | [[디자인 패턴]] |
| 웹·DI·Boot | [[Spring과 Spring Boot 학습]] |
| 공공 표준 | [[전자정부프레임워크]] |
| SQL·성능 | [[Oracle DB와 튜닝]] |
| 에디터 | [[VS Code 사용법]], [[Cursor 사용법]] |
| 긴 스펙 PDF | [[NotebookLM 사용법]] |

---

## 관련

- [[생활위키 목차]]
- [[JDK]]
- [[디자인 패턴]]
- [[Spring과 Spring Boot 학습]]
- [[전자정부프레임워크]]
- [[Oracle DB와 튜닝]]
- [[Cursor 사용법]]
