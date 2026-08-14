---
publish: true
draft: false
depth: article
aliases:
  - Java Development Kit
  - OpenJDK
  - JAVA_HOME
---

# JDK

> **분류:** 개발 › 언어 · [[생활위키 목차]]

**JDK**(Java Development Kit)는 Java를 **컴파일·실행·디버그**할 때 쓰는 개발 키트다. 문법·OOP는 [[Java 언어 학습]], 웹은 [[Spring과 Spring Boot 학습]]을 본다. 이 글은 **무엇·어느 배포·어느 버전·어디에 설치**만 정리한다.

파이썬은 인터프리터·venv·IDE가 흩어져 있다 → [[파이썬 개발 툴]].

확인일: 2026-08-14  
버전·지원 종료일은 **벤더 로드맵**이 우선이다. 회사 PC는 반입·라이선스 정책을 먼저 본다.

공식·배포:

- OpenJDK 프로젝트: [https://openjdk.org](https://openjdk.org)
- Eclipse Temurin (Adoptium): [https://adoptium.net](https://adoptium.net)
- Oracle Java SE 로드맵: [https://www.oracle.com/java/technologies/java-se-support-roadmap.html](https://www.oracle.com/java/technologies/java-se-support-roadmap.html)

관련: [[Java 언어 학습]] · [[Maven과 Gradle]] · [[Spring과 Spring Boot 학습]] · [[Eclipse 사용법]]

---

## 1. 개요

| 항목 | 설명 |
|------|------|
| **무엇** | `javac`(컴파일), `java`(실행), 표준 라이브러리, 진단 도구 묶음 |
| **무엇이 아님** | 언어 교재, Spring, 안드로이드 스튜디오 대체 |
| **결과물** | `.java` → `.class`(바이트코드). JVM이 해석·JIT |
| **설치 단위** | 보통 **메이저 번호 하나**(17·21·25…)를 폴더 하나에 |

```text
.java
  → javac (JDK)
  → .class
  → java / JVM (HotSpot 등)
  → 실행
```

같은 바이트코드를 여러 OS의 JVM에서 돌린다는 말이 **WORA**다. 전제는 **클래스 파일 버전 ≤ 실행 JDK**다. 21로 컴파일한 것을 11 JVM에 올리면 실패한다.

---

## 2. JDK · JRE · JVM

| 이름 | 역할 |
|------|------|
| **JVM** | 바이트코드를 실행하는 가상 머신 (힙·GC·JIT) |
| **JRE** | 실행만 (JVM + 라이브러리). Java 11 이후 **단독 JRE 배포는 거의 사라짐** |
| **JDK** | JRE + `javac`·`jar`·`jlink`·`jshell` 등 **개발 도구** |

지금은 **JDK를 깔고 실행도 JDK로** 하는 구성이 기본이다. 「JRE만 깔면 된다」는 옛 안내가 아직 웹에 남아 있다.

IDE가 내장한 런타임(예: Android Studio의 JBR, 일부 Eclipse)과 **터미널 `java`** 가 다른 경우가 많다. 에러가 나면 **어느 java인지**부터 본다.

---

## 3. OpenJDK와 배포본

**OpenJDK**는 스펙·소스의 중심이다. 손에 받는 설치 파일은 **빌드 벤더**가 다르다.

| 배포 | 메모 |
|------|------|
| **Eclipse Temurin** (Adoptium) | 학습·개인·많은 CI에서 **무난한 기본**. GPL + Classpath Exception |
| **Oracle JDK** | 공식 벤더. **라이선스(NFTC·OTN 등)가 버전·날짜마다 다름**. 회사는 구매·법무 |
| **Amazon Corretto** | AWS와 같이 쓰는 팀이 많음 |
| **Microsoft Build of OpenJDK** | Azure·Windows 안내와 같이 나오는 경우 |
| **Azul Zulu** · **BellSoft Liberica** | 장기 지원·특수 패키지(데스크톱 등) |
| **GraalVM** | 같은 Java라도 **네이티브 이미지** 등 목적이 다름. 입문 JDK 대체가 아님 |

「Java를 깔았다」만으로는 **몇 번인지·어느 벤더인지**가 안 나온다. `java -version` 한 줄에 vendor·버전을 같이 적는다.

소스 호환은 OpenJDK 계열이 같다. **지원 기간·보안 패치·라이선스**가 벤더 차이다.

---

## 4. 버전과 LTS

대략 **6개월**마다 메이저가 나온다. **LTS**(장기 지원)만 현장에서 오래 고정한다.

확인일 기준 흔히 보는 LTS:

| 버전 | 메모 |
|------|------|
| **8** | 레거시. 람다. **신규 학습·신규 사업은 피함** |
| **11** | 옛 LTS. 아직 유지보수 코드에 남음 |
| **17** | 모듈 이후 현장 LTS로 오래 쓰임. 지원은 벤더마다 종료 시점이 다름 |
| **21** | 가상 스레드 등. 2026년에도 **현역 LTS** |
| **25** | 2025-09 GA. **최신 LTS**. 신규·학습 기본으로 무난 |
| **26** | 2026-03 기능 릴리스. LTS가 아님. 6개월 주기로 따라갈 때만 |

비-LTS(12~16, 18~20, 22~24, 26…)는 **미리보기 문법을 잠깐 볼 때** 쓰고, 서비스 JDK로는 LTS를 고른다.

고를 때:

| 상황 | 방향 |
|------|------|
| 혼자 문법·Spring 입문 | **25** (또는 팀이 쓰는 LTS) |
| 회사·공공 사업 | **RFP·개발환경이 적은 번호** ([[전자정부프레임워크]]는 17·21이 안내된 적 있음) |
| 오래된 라이브러리 | 먼저 **그 라이브러리가 지원하는 최대 JDK** |
| CI·운영 | 로컬과 **같은 메이저·가능하면 같은 벤더** |

문법 예시는 [[Java 언어 학습]]이 **17+** 기준으로 적혀 있다. 8/11만 되는 코드와는 `var`·record·텍스트 블록이 갈린다.

---

## 5. 설치와 확인

Windows 개인 PC 예 (메뉴·패키지 ID는 시점에 따라 다름):

1. [Adoptium](https://adoptium.net)에서 **Temurin JDK** LTS 설치 프로그램  
2. 설치 화면에서 **JAVA_HOME**, **PATH에 `java` 추가**를 켠다  
3. **새** 터미널에서 확인  

```text
java -version
javac -version
where java
```

`java`만 되고 `javac`가 없으면 **JRE만 잡혔거나 PATH가 꼬인** 상태다.

다른 경로:

| 방법 | 메모 |
|------|------|
| `winget search temurin` | Windows 패키지 관리. ID는 검색 결과를 따른다 |
| **SDKMAN** | macOS·Linux에서 버전 여러 개 |
| 회사 포털·개발환경 ZIP | 전자정부·SI는 **지정 JDK**가 있는 경우가 많음 — 개인 Temurin과 섞지 말 것 |
| IDE 설치 마법사 | [[Eclipse 사용법]]·IntelliJ가 JDK를 같이 받기도 함. 터미널과 **별개**일 수 있음 |

Linux는 배포판 `apt`의 `openjdk-*-jdk`도 쓰인다. 패키지 메이저가 오래된지 `java -version`으로 확인한다.

---

## 6. JAVA_HOME · PATH · 여러 버전

| 변수 | 역할 |
|------|------|
| **JAVA_HOME** | JDK **루트** 폴더. Maven·Gradle·Tomcat·일부 IDE가 봄 |
| **PATH** | `java`·`javac`가 있는 `bin` |

`JAVA_HOME`은 `bin`이 **아니라** 그 위(`...\jdk-25.x.y`)다. `bin`을 JAVA_HOME에 넣으면 도구가 실패한다.

여러 메이저를 같이 두는 것은 흔하다. 그때:

- 터미널 PATH가 **의도한 버전**인지  
- IDE **Project SDK / Installed JREs**가 같은지  
- Maven `maven.compiler.release` · Gradle toolchain이 **더 높은 버전을 요구**하지 않는지  

Windows에서 설치 직후 옛 터미널은 PATH를 모를 수 있다. **창을 닫고** 다시 연다.

---

## 7. 자주 쓰는 명령

입문은 아래면 충분하다. 세부 옵션은 `명령 -help`.

| 명령 | 하는 일 |
|------|---------|
| `java` | 클래스·JAR 실행. `-version` |
| `javac` | 소스 컴파일 |
| `jar` | JAR 묶기·풀기 |
| `jshell` | REPL. 한 줄 실험 |
| `jdeps` | 의존·모듈 분석 |
| `jlink` | 필요한 모듈만 넣은 **작은 런타임** |
| `jpackage` | 설치 패키지 (데스크톱) |
| `jcmd` · `jfr` | 실행 중 JVM 진단 — [[Java 언어 학습]] JVM 절 |

일상 프로젝트는 **Maven / Gradle**이 `javac`를 대신 돌린다. 그래도 JDK는 필요하다.

```text
javac Hello.java
java Hello
```

파일명·`public class` 이름은 같아야 한다 → [[Java 언어 학습]] §2.

---

## 8. IDE·빌드·컨테이너

| 도구 | JDK와의 관계 |
|------|----------------|
| [[Eclipse 사용법]] | Installed JREs · Compiler compliance를 **프로젝트 번호**에 맞춤 |
| [[VS Code 사용법]] | Extension Pack for Java. `java.configuration.runtimes` |
| [[Cursor 사용법]] | VS Code와 같은 확장을 쓰는 경우가 많음. **에이전트가 보는 터미널 JDK**를 맞출 것 |
| IntelliJ | Project SDK. IDE 부팅 JDK와 프로젝트 JDK를 혼동하지 말 것 |
| Maven·Gradle | Wrapper + (선택) toolchain. CI 이미지의 JDK와 맞추기 |
| [[Docker 사용법]] | `eclipse-temurin` 등 **이미지 태그 = 메이저**. 로컬 25 / 이미지 17이면 재현이 안 됨 |
| [[SQL Developer 사용법]] | **번들 JDK** 또는 설치된 JDK 경로. 개발 JDK와 달라도 됨 |
| [[DBeaver 사용법]] | 최근 배포는 런타임을 **포함하는** 경우가 많음 |
| [[안드로이드]] 앱 | Android Studio **내장 JDK**. 폰 OS와 별개. 언어는 Kotlin 비중, JVM 기초는 [[Java 언어 학습]] |

전자정부 개발환경은 **지정 Eclipse + 지정 JDK**를 같이 받는 경우가 많다 → [[전자정부프레임워크]].

---

## 9. 정리

| 항목 | 한 줄 |
|------|--------|
| 정의 | Java **개발 키트** (컴파일 + 실행 + 도구) |
| 개인 기본 | Temurin **LTS** (확인일 기준 **25** 무난) |
| 회사 | 사업이 적은 버전 + 라이선스 |
| 확인 | `java -version` · `javac -version` · `where java` |
| 다음 | [[Java 언어 학습]] → [[Maven과 Gradle]] → [[디자인 패턴]] → [[Spring과 Spring Boot 학습]] |

---

## 면책

> **면책**
> - **특정 벤더·유료 구독 권유가 아니다.**
> - 메이저 번호·보안 업데이트·라이선스 문구는 **Oracle·Adoptium·클라우드 벤더**가 바꾼다. 설치 페이지·로드맵이 우선이다.
> - 회사·공공 PC는 **반입 정책·지정 개발환경**을 개인 설치보다 앞에 둔다.
> - 이 글의 명령은 **로컬 개발 확인**용이다.

---

## 관련

- [[생활위키 목차]]
- [[Java 언어 학습]]
- [[Spring과 Spring Boot 학습]]
- [[전자정부프레임워크]]
- [[Eclipse 사용법]]
- [[Maven과 Gradle]]
- [[안드로이드]]
