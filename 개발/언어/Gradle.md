---
publish: true
draft: false
depth: article
aliases:
  - Gradle Build Tool
  - build.gradle
  - gradlew
  - 그레이들
---

# Gradle

> **분류:** 개발 › 언어 · [[생활위키 목차]]

**Gradle**은 JVM(그리고 Android) 프로젝트의 **빌드·의존성** 도구다. 설정은 **Groovy 또는 Kotlin DSL**이고, 일은 **태스크 그래프**로 연결한다.

비교는 [[Maven과 Gradle]], XML 축은 [[Maven]], JDK는 [[JDK]].

공식: [https://gradle.org](https://gradle.org)

확인일: 2026-08-14  
8.x·9.x 안내는 프로젝트 **Gradle Wrapper**와 [호환표](https://docs.gradle.org)가 우선이다. Android는 **Android Gradle Plugin** 버전이 따로 있다.

관련: [[Maven과 Gradle]] · [[Maven]] · [[JDK]]

---

## 1. 개요

| 항목 | 설명 |
|------|------|
| **무엇** | 스크립트로 태스크를 정의하고, 증분·캐시로 다시 빌드하는 도구 |
| **설정** | `build.gradle.kts`(Kotlin DSL) 또는 `build.gradle`(Groovy) |
| **프로젝트 목록** | `settings.gradle.kts` (또는 `.gradle`) |
| **관례** | Maven과 같이 `src/main/java` 를 많이 씀 |
| **실행** | Wrapper `./gradlew` (Windows `gradlew.bat`) |
| **산출** | `build/` . 캐시·데몬은 `.gradle/` |

```text
settings.gradle.kts  +  build.gradle.kts
        ↓
태스크 그래프 (compile → test → jar …)
        ↓
필요한 태스크만 · 안 바뀐 입력은 건너뜀
        ↓
build/libs/*.jar
```

Android Studio·[[안드로이드]] 앱은 **Gradle이 표준**이다. Spring Boot는 start.spring.io에서 Gradle(Kotlin/Groovy)을 고를 수 있다.

---

## 2. 쓰는 이유

- **증분 빌드·빌드 캐시·설정 캐시**로 큰 멀티모듈에서 재빌드가 짧은 경우가 많다.
- **태스크를 코드로** 붙이기 쉽다 (코드 생성, 커스텀 배포).
- Android Gradle Plugin, Kotlin 생태계 안내가 Gradle 쪽인 경우가 많다.
- `implementation` vs `api`로 **의존성이 밖으로 새는 범위**를 조절한다.

공공 템플릿·팀이 이미 `pom.xml`이면 [[Maven]]을 따른다.

---

## 3. Groovy DSL과 Kotlin DSL

| | `build.gradle` | `build.gradle.kts` |
|--|----------------|---------------------|
| 언어 | Groovy | Kotlin |
| 신규 | 레거시·예제 코드에 많음 | start.spring.io **Gradle - Kotlin**, Kotlin 가이드의 기본인 경우가 많음 |
| IDE | 동작함 | 자동완성이 나은 편이라는 체감이 흔함 |

한 프로젝트에서 **한 DSL만** 쓴다. `.gradle`과 `.kts`를 모듈마다 섞으면 온보딩이 아프다.

Kotlin DSL 의존성 한 줄 예 (버전은 플랫폼·카탈로그가 정함):

```kotlin
dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    testImplementation("org.springframework.boot:spring-boot-starter-test")
}
```

---

## 4. 의존성 configuration

Maven `scope`와 **이름이 다르다.**

| Gradle | 대략의 대응 | 메모 |
|--------|-------------|------|
| `implementation` | compile에 가깝지만 **소비자에게 안 새는** 편 | 앱 모듈 기본 |
| `api` | 라이브러리 모듈이 **컴파일 때 같이 노출** | 잘못 쓰면 의존 폭발 |
| `compileOnly` | provided에 가까움 | 애너테이션 프로세서·서블릿 API 등 |
| `runtimeOnly` | runtime | JDBC 드라이버 등 |
| `testImplementation` | test | JUnit |

버전 묶음은 `platform(...)` / `enforcedPlatform(...)`(Boot BOM) 또는 **Version Catalog** (`gradle/libs.versions.toml`)를 쓴다.

저장소는 `repositories { mavenCentral() }`가 기본. 회사는 `maven { url = ... }`로 미러.

---

## 5. 태스크·명령

Maven처럼 “package라고 하면 앞 단계가 자동”이 아니라, **태스크가 의존하는 태스크**만 돈다. `build`는 보통 테스트+jar를 묶은 관례 태스크다.

```bash
./gradlew tasks
./gradlew test
./gradlew build
./gradlew clean
./gradlew dependencies
./gradlew bootRun
```

`bootRun`은 Spring Boot 플러그인이 있을 때. 플러그인 없는 순수 Java는 `application` 플러그인의 `run` 등.

자세한 목록은 `./gradlew tasks --all` 또는 `./gradlew help --task test`.

---

## 6. Wrapper · 데몬

```text
gradlew
gradlew.bat
gradle/wrapper/gradle-wrapper.jar
gradle/wrapper/gradle-wrapper.properties
```

`distributionUrl`이 **이 저장소의 Gradle 버전**이다. Android는 AGP가 요구하는 Gradle 대역이 있다. 아무 최신이나 올리지 않는다.

**Daemon**은 백그라운드 JVM을 재사용한다. 로컬이 빠르고, CI에서는 `--no-daemon`을 쓰는 파이프라인도 있다. 팀 CI 문서를 본다.

Git에는 Wrapper를 올리고 `build/`, `.gradle/`은 ignore → [[Git 사용법]].

---

## 7. 증분·캐시

| 기능 | 요지 |
|------|------|
| **증분** | 입력(소스·클래스패스)이 같으면 태스크를 UP-TO-DATE |
| **빌드 캐시** | 다른 모듈·CI 에이전트와 산출물을 공유할 수 있음 (설정 필요) |
| **설정 캐시** | 설정 단계를 재사용해 시작이 짧아짐 (호환 안 되는 플러그인 주의) |

캐시가 꼬이면 `./gradlew clean`만으로 부족할 때가 있다. `--rerun-tasks` 또는 로컬 `.gradle` 캐시를 지우는 안내는 공식 Troubleshooting을 따른다.

---

## 8. 멀티 프로젝트

`settings.gradle.kts`에 `include("app", "core")`처럼 하위 프로젝트를 넣는다. 루트 `build.gradle.kts`에서 공통 플러그인·Java 버전을 맞추는 방식이 흔하다.

복합 빌드(`includeBuild`)는 별도 저장소를 한 그래프에 넣는 고급 기능이다. 입문 필수는 아니다.

---

## 9. 흔한 함정

| 증상 | 먼저 볼 것 |
|------|------------|
| IDE와 터미널 결과가 다름 | IDE Gradle JVM ≠ 터미널 `JAVA_HOME`. [[JDK]] 경로를 맞춤 |
| Android 빌드 실패 | AGP ↔ Gradle ↔ JDK **삼자 호환표** |
| 의존성이 너무 많음 | `api`를 `implementation`으로 줄일 수 있는지 |
| Windows에서 `gradlew` 권한 | `gradlew.bat` 또는 Git `core.autocrlf`. 실행 비트는 WSL |
| `build`를 커밋함 | gitignore |
| Groovy/Kotlin DSL 혼용 | 모듈마다 파일 종류를 통일 |
| 오프라인·회사망 | `mavenCentral()`이 막히면 미러. `--offline`은 캐시가 있을 때만 |

비밀은 `gradle.properties`(로컬, gitignore) 또는 CI 변수. `build.gradle.kts`에 토큰을 하드코딩하지 않는다.

---

## 10. 확인 방법

1. [Gradle User Manual](https://docs.gradle.org) — 해당 Wrapper 메이저  
2. `./gradlew -v` — Gradle·Kotlin DSL·JVM  
3. Android → Android Studio / AGP 릴리스 노트 · [[안드로이드]]  
4. Spring → start.spring.io의 Gradle - Kotlin · [[Spring과 Spring Boot 학습]]

---

## 면책

> **면책**
> - **Gradle 상용 제품·클라우드 빌드 구독 권유가 아니다.**
> - AGP·JDK·Gradle 조합은 **서로 버전이 묶여 있다.** 호환표를 이 글 숫자보다 앞에 둔다.
> - 캐시·데몬·병렬 옵션은 **CI 정책**에 맞춘다.

---

## 관련

- [[생활위키 목차]]
- [[Maven과 Gradle]]
- [[Maven]]
- [[JDK]]
- [[Spring과 Spring Boot 학습]]
- [[안드로이드]]
- [[Docker 사용법]]
