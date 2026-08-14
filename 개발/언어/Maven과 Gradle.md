---
publish: true
draft: false
depth: hub
aliases:
  - Maven vs Gradle
  - 메이븐과 그레이들
  - JVM 빌드 도구
---

# Maven과 Gradle

> **분류:** 개발 › 언어 · [[생활위키 목차]]

JVM 프로젝트에서 **의존성을 받고, 컴파일·테스트·패키징**하는 두 빌드 도구를 묶은 허브다. 본문은 각 글에 있다.

- [[Maven]] — `pom.xml`, 라이프사이클, Apache Maven  
- [[Gradle]] — `build.gradle` / `.kts`, 태스크 그래프  

문법은 [[Java 언어 학습]], 설치는 [[JDK]], 웹은 [[Spring과 Spring Boot 학습]], 공공은 [[전자정부프레임워크]].

확인일: 2026-08-14  
버전·플러그인 이름은 **Wrapper가 고정한 값**과 공식 문서가 우선이다.

관련: [[Maven]] · [[Gradle]] · [[JDK]]

---

## 1. 개요

둘 다 **라이브러리를 좌표로 받아** 클래스패스를 맞추고, `src/main/java` 관례로 **jar·war**를 만든다. 차이는 **설정을 어떻게 쓰느냐**와 **다시 빌드할 때 얼마나 건너뛰느냐**에 가깝다.

| | [[Maven]] | [[Gradle]] |
|--|-----------|------------|
| **무엇** | Apache 재단의 JVM 빌드 도구. XML 선언이 기본 | Gradle Inc의 빌드 도구. 스크립트(DSL)가 기본 |
| **설정** | `pom.xml` | `build.gradle` 또는 `build.gradle.kts` |
| **모델** | **라이프사이클 단계**(compile → test → package…) | **태스크 그래프**(필요한 일만 이어서 실행) |
| **명령 예** | `./mvnw clean test` | `./gradlew test` |
| **산출 폴더** | `target/` | `build/` |
| **Wrapper** | `mvnw` / `mvnw.cmd` | `gradlew` / `gradlew.bat` |
| **잘 맞는 곳** | 공공·SI, Eclipse, 팀 관례가 XML일 때 | Android, 큰 멀티모듈, 커스텀 태스크 |
| **신규 Spring** | start.spring.io에서 **선택 가능**. Java 기본값이 Maven인 화면이 많음 | Kotlin 프로젝트는 **Gradle Kotlin DSL** 안내가 흔함 |

```text
소스 + 좌표(group:name:version)
        ↓
   Maven 또는 Gradle
        ↓
컴파일 → 테스트 → jar/war
        ↓
IDE · CI · [[Docker 사용법]] 이미지
```

**둘을 한 모듈에 섞지 않는다.** `pom.xml`과 `build.gradle`이 같이 있으면 어느 쪽이 진짜인지 팀이 헷갈린다.

---

## 2. 같은 점

| 항목 | 내용 |
|------|------|
| **좌표** | `groupId` / `artifactId` / `version` (Gradle은 `group`·`name`·`version`) |
| **저장소** | Maven Central이 기본. 회사는 Nexus·Artifactory 미러가 많음 |
| **폴더 관례** | `src/main/java`, `src/main/resources`, `src/test/java` |
| **Wrapper** | 저장소에 스크립트를 넣어 **로컬에 도구를 안 깔아도** CI·동료가 같은 버전으로 빌드 |
| **BOM** | Spring Boot처럼 **버전 묶음**을 parent·platform으로 맞춤 |
| **플러그인** | 컴파일러·테스트·Spring Boot 패키징을 플러그인이 담당 |

파이썬의 pip·venv와 역할이 비슷하다. 그쪽은 [[파이썬 개발 툴]]·[[Python 학습과 패키지]].

---

## 3. 다른 점

| 축 | Maven | Gradle |
|----|--------|--------|
| **읽기** | XML이라 **도구·리뷰가 예측 가능**. 길어지기 쉬움 | Kotlin/Groovy라 **짧고 분기가 쉬움**. 팀 컨벤션이 없으면 제각각 |
| **실행** | 단계 이름을 부르면 **그 앞 단계까지** 같이 도는 편 | 태스크 의존만 탐. **증분·캐시·데몬**으로 재빌드가 빠른 경우가 많음 |
| **의존 범위** | `compile` / `provided` / `runtime` / `test` 등 **scope** | `implementation` / `api` / `compileOnly` / `testImplementation` 등 **configuration** |
| **멀티모듈** | `<modules>` + parent POM | `settings.gradle(.kts)` + `include` |
| **안드로이드** | 공식 앱 빌드의 주 경로가 아님 | **Android Gradle Plugin**이 표준 |
| **공공 템플릿** | eGov·Eclipse 예제가 **Maven인 경우가 많음** | 사업이 지정하면 그때. 개인이 먼저 바꾸지 말 것 |

「Gradle이 무조건 빠르다」는 **프로젝트 크기·캐시 히트·CI 콜드스타트**에 따라 갈린다. Maven도 3.9대와 이후 버전에서 체감이 다르다. **같은 머신에서 Wrapper로 재는 것**이 맞다.

---

## 4. 고를 때

| 상황 | 보통의 선택 |
|------|-------------|
| **회사·공공이 이미 Maven** | [[Maven]]. 혼자 Gradle로 바꾸지 않음 |
| **Android 앱** | [[Gradle]] |
| **Spring Boot 개인 학습** | 둘 다 됨. start.spring.io에서 고르고 **Wrapper를 커밋** |
| **Kotlin 위주** | Gradle **Kotlin DSL** 안내가 많음 |
| **커스텀 배포·코드 생성 태스크가 많음** | Gradle이 스크립트로 붙이기 수월한 편 |
| **XML·라이프사이클만 알고 시작** | Maven으로 관례를 익힌 뒤 Gradle을 봐도 됨 |

이직·오픈소스 읽기에는 **둘 다 명령 몇 개**가 필요하다. 개념은 이 허브, 파일·명령은 각 글.

---

## 5. 명령·파일 대응

| 하고 싶은 일 | Maven | Gradle |
|--------------|--------|--------|
| 테스트 | `./mvnw test` | `./gradlew test` |
| 패키징 | `./mvnw package` | `./gradlew build` |
| 로컬 저장소에 설치 | `./mvnw install` | `./gradlew publishToMavenLocal` (플러그인에 따라) |
| 의존성 트리 | `./mvnw dependency:tree` | `./gradlew dependencies` |
| 산출물 지움 | `./mvnw clean` | `./gradlew clean` |
| Git에 안 올리는 것 | `target/` | `build/`, `.gradle/` |

Windows는 `mvnw.cmd`, `gradlew.bat`. Git Bash·WSL은 `./mvnw`, `./gradlew`.

---

## 면책

> **면책**
> - **특정 도구 구독·전환 권유가 아니다.** 팀·RFP·안드로이드 공식 가이드가 우선이다.
> - 메이저 버전·플러그인·start.spring.io 기본값은 **자주 바뀐다.** Wrapper와 공식 문서가 최종본이다.
> - 이 글의 명령은 **로컬·CI 확인**용이다.

---

## 관련

- [[생활위키 목차]]
- [[Maven]]
- [[Gradle]]
- [[JDK]]
- [[Java 언어 학습]]
- [[Spring과 Spring Boot 학습]]
- [[전자정부프레임워크]]
