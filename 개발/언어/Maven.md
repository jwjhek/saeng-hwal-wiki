---
publish: true
draft: false
depth: article
aliases:
  - Apache Maven
  - pom.xml
  - mvn
  - 메이븐
---

# Maven

> **분류:** 개발 › 언어 · [[생활위키 목차]]

**Maven**(Apache Maven)은 JVM 프로젝트의 **빌드·의존성** 도구다. 설정은 **`pom.xml`**(Project Object Model)이고, **라이프사이클 단계**를 순서대로 돈다.

비교·고르는 기준은 [[Maven과 Gradle]], 다른 축은 [[Gradle]], JDK는 [[JDK]].

공식: [https://maven.apache.org](https://maven.apache.org)

확인일: 2026-08-14  
3.9대가 현장에 많다. 4.x 여부는 **공식 다운로드·릴리스 노트**를 본다. 프로젝트는 **Maven Wrapper**가 가리키는 버전이 맞다.

관련: [[Maven과 Gradle]] · [[Gradle]] · [[JDK]]

---

## 1. 개요

| 항목 | 설명 |
|------|------|
| **무엇** | 좌표로 라이브러리를 받고, 컴파일·테스트·jar/war를 만드는 도구 |
| **설정** | 모듈 루트의 `pom.xml` |
| **관례** | `src/main/java`, `src/test/java` — 경로를 거의 안 적는다 |
| **실행** | Wrapper `./mvnw` (Windows `mvnw.cmd`). 전역 `mvn`만 쓰지 않는 편이 안전 |
| **산출** | `target/` |

```text
pom.xml (좌표·플러그인·모듈)
        ↓
validate → compile → test → package → verify → install → deploy
        ↓
target/*.jar  (또는 war)
```

Spring Boot는 [start.spring.io](https://start.spring.io)에서 Maven을 고르면 `pom.xml` + Wrapper가 같이 나온다.

---

## 2. 쓰는 이유

- **선언이 비슷하다.** 다른 팀 POM을 읽기 쉽다.
- **단계 이름이 고정**이라 CI에 `clean verify`처럼 적기 수월하다.
- 공공 [[전자정부프레임워크]]·[[Eclipse 사용법]] 예제가 Maven인 경우가 많다.
- Central·회사 Nexus에 **같은 좌표 체계**로 올린다.

커스텀 태스크가 많거나 Android면 [[Gradle]] 쪽이 맞는 경우가 많다.

---

## 3. 좌표·저장소

의존성 한 줄은 **세 조각**이다.

```text
groupId : artifactId : version
예: org.springframework.boot : spring-boot-starter-web : (Boot가 정한 버전)
```

| 용어 | 의미 |
|------|------|
| **groupId** | 조직·패키지 앞부분 (`org.example`) |
| **artifactId** | 그 조직 안의 프로젝트 이름 |
| **version** | `1.2.3`, `1.2.3-SNAPSHOT` |
| **scope** | `compile`(기본), `provided`(서블릿처럼 런타임 컨테이너 제공), `runtime`, `test` |

다운로드는 기본이 **Maven Central**. 회사는 `settings.xml` 또는 POM `<repositories>`로 **내부 저장소**를 가리킨다.

Spring Boot는 `<parent>` 또는 BOM으로 **starter 버전을 한곳에서** 맞춘다. 숫자를 POM마다 흩뿌리지 않는 편이 안전하다.

---

## 4. pom.xml 뼈대

최소 골격만 본다. 버전은 문서·Boot parent가 정한다.

```xml
<project>
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.example</groupId>
  <artifactId>demo</artifactId>
  <version>0.0.1-SNAPSHOT</version>
  <packaging>jar</packaging>
  <dependencies>
    <!-- dependency 블록 -->
  </dependencies>
</project>
```

| 태그 | 역할 |
|------|------|
| `<parent>` | Boot·eGov처럼 **부모 POM**에서 플러그인·의존 버전을 받음 |
| `<properties>` | Java 버전, 인코딩, 라이브러리 버전 변수 |
| `<dependencyManagement>` | 멀티모듈에서 **버전만** 중앙 관리 (쓰는 쪽은 version 생략) |
| `<modules>` | 하위 모듈 목록 |
| `<build><plugins>` | compiler, surefire(테스트), Spring Boot 패키징 등 |

인코딩은 UTF-8, 소스/타깃은 **팀이 쓰는 JDK**와 맞춘다 → [[JDK]].

---

## 5. 라이프사이클·명령

기본 라이프사이클(앞 단계가 같이 도는 편):

| 단계 | 하는 일 |
|------|---------|
| `compile` | 메인 소스 컴파일 |
| `test` | 테스트 컴파일·실행 (JUnit 등) |
| `package` | jar/war |
| `verify` | 패키지 이후 검사(통합 테스트 플러그인이 있으면) |
| `install` | 로컬 `~/.m2/repository`에 넣음 (다른 로컬 모듈이 참조) |
| `deploy` | 원격 저장소에 배포 (권한·CI) |

`clean`은 **별도 라이프사이클**이다. `clean package`처럼 붙여 쓴다.

자주 쓰는 명령:

```bash
./mvnw clean test
./mvnw package
./mvnw install
./mvnw dependency:tree
```

플러그인 골(goal)은 `플러그인이름:골` 형식이다. `dependency:tree`가 그 예다.

---

## 6. Wrapper

저장소에 보통 있다.

```text
mvnw
mvnw.cmd
.mvn/wrapper/maven-wrapper.properties
```

`maven-wrapper.properties`의 `distributionUrl`이 **이 프로젝트가 쓰는 Maven 버전**이다. CI도 `./mvnw`를 호출하면 전역 설치와 안 싸운다.

Git에는 Wrapper와 `pom.xml`을 올리고, `target/`은 `.gitignore`다 → [[Git 사용법]].

---

## 7. 멀티 모듈

부모 POM + `<modules>`로 하위 프로젝트를 나눈다. 공통 라이브러리 모듈을 `install`하거나 같은 리액터에서 참조한다.

현장에서는 **BOM·parent 버전**이 어긋나면 “로컬에선 되고 CI에서 실패”가 난다. 부모와 자식의 Java 버전·인코딩을 먼저 본다.

---

## 8. 흔한 함정

| 증상 | 먼저 볼 것 |
|------|------------|
| 컴파일은 되는데 IDE가 빨갛다 | Eclipse **Maven Update**, IntelliJ **Reload Maven**. JDK가 POM과 같은지 |
| 의존을 못 받음 | 회사 프록시·Nexus URL, `~/.m2/settings.xml`, VPN |
| 테스트만 스킵하고 패키징 | `-DskipTests` / `-Dmaven.test.skip` 차이를 알고 쓸 것. CI 기본은 테스트를 돌리는 편 |
| SNAPSHOT이 안 바뀜 | 로컬 `~/.m2`에 오래된 SNAPSHOT. `-U`로 업데이트하거나 해당 폴더 삭제 |
| `target`을 커밋함 | 바이너리다. gitignore |
| pom과 Gradle 공존 | 한 모듈에 빌드 도구 **하나** |

키·비밀번호를 `pom.xml`에 적지 않는다. 서버 비밀번호는 `settings.xml`(로컬) 또는 CI 비밀 변수.

---

## 9. 확인 방법

1. 공식 문서 — [Maven Guides](https://maven.apache.org/guides/)  
2. 프로젝트 `./mvnw -v` — Maven·Java 버전  
3. Spring이면 start.spring.io가 만든 POM + [[Spring과 Spring Boot 학습]]  
4. 공공이면 포털 지정 parent → [[전자정부프레임워크]]

---

## 면책

> **면책**
> - **특정 IDE·저장소 제품 권유가 아니다.**
> - 플러그인·라이프사이클·Central 정책은 **개정**된다. Wrapper와 공식 가이드가 우선이다.
> - `deploy`·회사 Nexus는 **권한·보안 정책**을 따른다.

---

## 관련

- [[생활위키 목차]]
- [[Maven과 Gradle]]
- [[Gradle]]
- [[JDK]]
- [[Spring과 Spring Boot 학습]]
- [[전자정부프레임워크]]
- [[Eclipse 사용법]]
