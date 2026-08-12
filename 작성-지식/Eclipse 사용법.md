---
publish: true
draft: false
---

# Eclipse 사용법

> **분류:** 작성·지식 › 에디터·IDE · [[생활위키 목차]]

Eclipse는 Java 등 JVM 언어 개발에 널리 쓰이는 **IDE(통합 개발 환경)** 다. 
국내 공공·SI에서는 [[전자정부프레임워크]] 개발환경의 기본으로 자주 등장한다.

다운로드: [https://www.eclipse.org/downloads/](https://www.eclipse.org/downloads/) 
패키지: **Eclipse IDE for Enterprise Java and Web Developers** (웹·EE 할 때 추천)

확인일: 2026-08-06 
메뉴 이름은 버전(2024-03, 2025-03 등)·한글 언어팩에 따라 조금 다를 수 있다.

---

## 1. Eclipse가 하는 일

- 프로젝트·소스 편집, 자동완성, 리팩터 
- 컴파일·실행·디버그 
- Maven/Gradle 연동 
- 서버(Tomcat 등)에 배포·실행 
- Git, 플러그인으로 기능 확장 

[[VS Code 사용법\|VS Code]] / [[Cursor 사용법\|Cursor]]보다 **Java EE·이클립스 플러그인 생태계·eGov 템플릿**에 강하고, 
가벼운 편집·AI 에이전트는 Cursor 쪽이 편한 경우가 많다. **병행**해도 된다.

---

## 2. 설치·첫 실행

1. JDK 설치 (프로젝트 버전에 맞춤 — eGov 5.0 개발환경은 JDK 21 등) 
2. Eclipse 패키지 ZIP 또는 설치 프로그램 
3. 실행 → **Workspace** 폴더 지정 (프로젝트들이 모이는 루트) 
4. 필요 시 Marketplace / eGov 개발환경 플러그인 설치 

팁:

- 워크스페이스는 프로젝트마다 나누거나, 회사/개인으로 분리 
- `eclipse.ini`에서 `-Xmx`로 힙을 키우면 대형 프로젝트에서 버벅임이 줄어듦 
- 한글 메뉴: Language Pack 또는 한글 배포본 

---

## 3. 화면 구성

```text
┌ 메뉴·툴바 ─────────────────────────────────────┐
│ Package Explorer │ 에디터 탭들 │ Outline 등 │
│ (또는 Project) │ │ │
├──────────────────┴──────────────┴────────────┤
│ Console / Problems / Servers / Git 등 뷰 │
└──────────────────────────────────────────────┘
```

| 뷰 | 용도 |
|----|------|
| **Package Explorer** | 소스 패키지 중심 트리 |
| **Project Explorer** | 파일·리소스 전체 |
| **Outline** | 클래스 멤버 목록 |
| **Problems** | 컴파일 오류·경고 |
| **Console** | 실행 로그 |
| **Servers** | Tomcat 등 서버 등록·배포 |
| **Progress** | 빌드·다운로드 진행 |

뷰가 사라지면: `Window` → `Show View` → `Other…` 
원배치: `Window` → `Perspective` → `Reset Perspective`

**Perspective**: Java, Debug, Java EE 등 화면 배치 프리셋. 오른쪽 위 아이콘으로 전환.

---

## 4. 프로젝트 만들기·가져오기

### 새로 만들기

1. `File` → `New` → `Java Project` 또는 `Maven Project` / `Dynamic Web Project` 
2. JRE·프로젝트명 설정 
3. 소스 폴더 `src` (Maven이면 `src/main/java`) 

### 기존 프로젝트

- `File` → `Import` → `Existing Projects into Workspace` 
- Maven: `Import` → `Existing Maven Projects` (`pom.xml` 선택) 
- eGov: 포털·가이드의 **프로젝트 생성 마법사/템플릿** 사용 

프로젝트가 빨간 X면: JDK 버전, Maven Update, 빌드 경로를 확인.

---

## 5. 필수 단축키 (Windows)

| 동작 | 단축키 |
|------|--------|
| 빠른 실행 (Quick Access) | `Ctrl` + `3` |
| 퀵 아웃라인 | `Ctrl` + `O` |
| 타입 열기 | `Ctrl` + `Shift` + `T` |
| 리소스(파일) 열기 | `Ctrl` + `Shift` + `R` |
| 빠른 수정 (Quick Fix) | `Ctrl` + `1` |
| 자동완성 | `Ctrl` + `Space` |
| 포맷 | `Ctrl` + `Shift` + `F` |
| import 정리 | `Ctrl` + `Shift` + `O` |
| 실행 | `Ctrl` + `F11` |
| 디버그 | `F11` |
| 한 줄 삭제 | `Ctrl` + `D` |
| 줄 복사 | `Ctrl` + `Alt` + `↓` |
| 주석 토글 | `Ctrl` + `/` |
| 찾기 | `Ctrl` + `F` |
| 파일 내 검색 | `Ctrl` + `H` (Search) |
| 선언으로 이동 | `F3` |
| 호출 계층 | `Ctrl` + `Alt` + `H` |
| 이름 바꾸기(리팩터) | `Alt` + `Shift` + `R` |
| 추출 메서드 | `Alt` + `Shift` + `M` |

단축키 전체: `Window` → `Preferences` → `General` → `Keys`

---

## 6. 코딩 워크플로

1. 클래스 작성 → 저장 시 자동 빌드 (`Project` → `Build Automatically` 권장) 
2. `Problems`에 에러 없으면 `Run As` → `Java Application` 
3. main 없는 웹은 Server에 Add and Run 
4. 자주 쓰는 import·포맷은 저장 액션으로:

`Preferences` → `Java` → `Editor` → `Save Actions` 
→ format, organize imports 체크

### 코드 템플릿

`sysout` + `Ctrl` + `Space` → `System.out.println` 
템플릿 편집: `Preferences` → `Java` → `Editor` → `Templates`

---

## 7. 디버깅

1. 줄 번호 왼쪽 더블클릭 → **Breakpoint** 
2. `Debug As` → Java Application / Debug on Server 
3. Perspective가 Debug로 전환 
4. `F5` Step Into, `F6` Step Over, `F7` Step Return, `F8` Resume 
5. **Variables** / **Expressions** 로 값 확인 

팁: 조건 브레이크포인트(우클릭 → Breakpoint Properties), Hot Code Replace는 제한적으로 동작.

---

## 8. Maven · 빌드

- 프로젝트 우클릭 → `Maven` → `Update Project…` (`Alt` + `F5`) 
- `Run As` → `Maven build…` → goals: `clean install` 
- `pom.xml` 의존성 오류 → 로컬 `.m2` 손상·저장소 URL·JDK 수준 확인 

Gradle은 Buildship 플러그인. eGov는 Maven이 많은 편.

---

## 9. 서버(Tomcat) 연동

1. `Window` → `Show View` → `Servers` 
2. `No servers` → Tomcat 버전 선택 → 로컬 설치 경로 
3. 프로젝트 우클릭 → `Run As` → `Run on Server` 
4. `web.xml` / context path / 포트(8080) 확인 

포트 충돌 시 Server Overview에서 포트 변경. 
모듈이 안 뜨면 Project Facets·Dynamic Web Module 버전을 점검.

---

## 10. Git

- `Window` → `Perspective` → `Git` 
또는 프로젝트 우클릭 → `Team` → `Share Project` / `Commit` 
- 내장 Git 또는 EGit 

대형 저장소는 SourceTree·CLI와 병행해도 된다.

---

## 11. 설정해 두면 좋은 것

| 항목 | 경로 |
|------|-----------|
| 워크스페이스 인코딩 UTF-8 | Preferences → General → Workspace |
| 에디터 탭 크기 4 | General → Editors → Text Editors |
| JDK 설치 경로 | Java → Installed JREs |
| Compiler compliance | Java → Compiler (프로젝트와 일치) |
| 폰트 | General → Appearance → Colors and Fonts |
| 자동 모듈패스/클래스패스 | Maven이 관리하게 두기 |

프로젝트별 JDK: 프로젝트 우클릭 → `Properties` → `Java Build Path` / `Java Compiler`

---

## 12. 전자정부프레임워크와 함께

[[전자정부프레임워크]] 개발환경은 전통적으로 Eclipse + 구현 도구(플러그인)다.

1. 포털에서 **지정 버전** 개발환경·가이드 확인 
2. 권장 Eclipse·JDK 맞추기 
3. eGov 플러그인·템플릿으로 프로젝트 생성 
4. `context-*.xml` / Java Config · Maven parent 
5. 로컬 WAS 또는 내장 톰캣으로 기동 

최근에는 VS Code 확장·IntelliJ 가이드도 있으나, **현장 표준이 Eclipse면 Eclipse에 맞추는 것**이 협업에 유리하다.

관련: [[Spring과 Spring Boot 학습]], [[Java 언어 학습]]

---

## 13. 문제 빠른 대처

| 증상 | 시도 |
|------|------|
| 프로젝트 전부 에러 | Project → Clean, Maven Update |
| 한글 깨짐 | UTF-8, 파일 Properties → Resource encoding |
| 실행은 되는데 예전 클래스 | Clean 후 재빌드, 서버 Clean |
| Tomcat 기동 실패 | 포트, JDK, 모듈 배포 목록 |
| 자동완성 안 됨 | 포커스 Java 에디터, `Ctrl`+`Space`, Content Assist 설정 |
| 느림 | `-Xmx` 증가, 불필요 플러그인 제거, 인덱스 재구축 |
| Workspace 손상 | 새 워크스페이스에 Import |

---

## 14. VS Code / IntelliJ / Cursor와 비교

| | Eclipse | IntelliJ | VS Code/Cursor |
|--|---------|----------|----------------|
| 공공 eGov | 매우 흔함 | 가능(가이드) | 확장으로 가능 |
| Java EE·서버 뷰 | 강함 | 강함 | 설정 더 필요 |
| 무게 | 중간~무거움 | 무거움 | 가벼움 |
| AI | 플러그인 의존 | 자체 AI | Cursor 강점 |

학습·개인: Cursor로 Java를 익혀도 되고, **회사 표준이 Eclipse면** 단축키·Perspective·Servers만 익히면 충분하다.

---

## 15. 추천 학습 순서

1. Workspace · Perspective · Package Explorer 
2. Java Project 실행 · 단축키 `Ctrl`+`Shift`+`T/R`, `Ctrl`+`1` 
3. 디버그 브레이크포인트 
4. Maven Import · Update 
5. Tomcat Run on Server 
6. (필요 시) eGov 템플릿 

---

## 관련

- [[생활위키 목차]]
- [[전자정부프레임워크]]
- [[Java 언어 학습]]
- [[Spring과 Spring Boot 학습]]
- [[VS Code 사용법]]
- [[Cursor 사용법]]
- [[Docker 사용법]]
