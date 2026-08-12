---
publish: true
draft: false
---

# VS Code 추천 확장

> **분류:** 작성·지식 › 에디터·IDE · [[생활위키 목차]]

기본 조작은 [[VS Code 사용법]]. 여기서는 **실제로 깔아 볼 만한 확장**만 용도별로 정리한다. 
마켓플레이스에서 이름·게시자(Publisher)로 검색한다. (`Ctrl` + `Shift` + `X`)

확인일: 2026-08-06 
확장 ID·인기는 바뀔 수 있다. **공식·최근 업데이트·별점**을 본다.

---

## 0. 고르는 원칙

1. **필요한 언어·작업만** — 팩을 잔뜩 깔면 시작·검색이 느려진다. 
2. Microsoft / 언어 공식 확장을 우선. 
3. 같은 역할 확장은 **하나**만 (포맷터·테마 중복 주의). 
4. 느리면 확장 절반 disable → 이분 탐색. 
5. Cursor를 쓰면 AI 확장은 겹칠 수 있다 → [[Cursor 사용법]].

설치 후 Settings Sync를 켜 두면 PC 간 목록이 맞는다.

---

## 1. 거의 공통으로 쓸 만한 것

| 확장 (검색어) | 용도 |
|---------------|------|
| **Korean Language Pack** (MS) | UI 한글 |
| **GitLens** | 라인 blame, 커밋 히스토리, 작성자 힌트 |
| **Git Graph** | 브랜치·커밋을 그래프로 보기 |
| **Error Lens** | 에러·경고를 코드 줄 옆에 바로 표시 |
| **Path Intellisense** | 파일 경로 자동완성 |
| **EditorConfig** | `.editorconfig` 탭/개행 통일 |
| **TODO Highlight** / **Todo Tree** | `TODO`·`FIXME` 하이라이트·목록 |
| **indent-rainbow** | 들여쓰기 단계 색 (선택) |
| **Bookmarks** | 파일 안 북마크 점프 (선택) |

GitLens는 무료 범위만으로도 충분하다. 유료 기능은 무시해도 된다.

---

## 2. 코드 품질·포맷

| 확장 | 용도 |
|------|------|
| **Prettier** | JS/TS/JSON/MD 등 포맷 (팀 합의 시) |
| **ESLint** | JS/TS 린트 |
| **Pretty TypeScript Errors** | TS 에러 메시지 읽기 쉽게 (TS 쓸 때) |
| **Code Spell Checker** | 영문 오타 (코드·주석). 한글 프로젝트는 예외 단어 등록 |

저장 시 포맷:

```json
{
 "editor.formatOnSave": true,
 "editor.defaultFormatter": "esbenp.prettier-vscode"
}
```

언어마다 기본 포맷터가 다르면 `[java]` 등 언어별 설정으로 나눈다.

---

## 3. 언어별 (이 위키 스택 기준)

### Java · Spring · eGov

| 확장 | 용도 |
|------|------|
| **Extension Pack for Java** (MS) | 언어 지원·디버그·Maven/Gradle 묶음 |
| **Spring Boot Extension Pack** (VMware) | Boot 프로젝트·실행·심볼 |
| **Gradle for Java** | Gradle 빌드 (팩에 포함되는 경우 많음) |
| **Community Server Connectors** / Tomcat 관련 | 내장 톰캣 배포 시 (필요하면) |

공공·이클립스 비중이 크면 IDE는 [[Eclipse 사용법]]도 병행. VS Code는 가벼운 편집·리뷰용으로 쓰는 팀이 많다. 
학습: [[Java 언어 학습]], [[Spring과 Spring Boot 학습]], [[전자정부프레임워크]]

### Python

| 확장 | 용도 |
|------|------|
| **Python** (MS) | 인터프리터·디버그·lint 연동 |
| **Pylance** | 타입·자동완성 (보통 Python과 함께) |
| **Python Debugger** | 디버그 (최근 분리된 경우) |
| **Jupyter** | 노트북 `.ipynb` |

venv 선택: 상태바 인터프리터 클릭. → [[Python 학습과 패키지]]

### C / C++

요약만. 설치·설정·디버그는 **§12. C/C++ 확장** 참고.

| 확장 | ID·용도 |
|------|---------|
| **C/C++** (MS) | `ms-vscode.cpptools` — IntelliSense·디버그 |
| **C/C++ Extension Pack** | 위 + CMake Tools 등 묶음 |
| **CMake Tools** | CMake 프로젝트 |

→ [[C언어와 포인터]]

### 웹 (HTML/CSS/JS)

| 확장 | 용도 |
|------|------|
| **ESLint** + **Prettier** | 위 §2 |
| **Live Server** | 정적 HTML 미리보기·자동 새로고침 |
| **Auto Rename Tag** | HTML/XML 태그 쌍 이름 동시 수정 |
| **CSS Peek** | 클래스 정의로 점프 (선택) |

### 데이터·SQL

| 확장 | 용도 |
|------|------|
| **SQLTools** + 드라이버 | DB 접속·쿼리 (가벼운 용). 본격 GUI는 [[DBeaver 사용법]] |
| **Database Client** 계열 | GUI에 가깝게 볼 때 (취향) |

Oracle 튜닝 개념은 [[Oracle DB와 튜닝]]. 확장은 “접속 도구”일 뿐 튜닝을 대신하지 않는다.

---

## 4. Docker · 원격 · 인프라

| 확장 | 용도 |
|------|------|
| **Docker** (MS) | 이미지·컨테이너·Compose 탐색 |
| **Dev Containers** | 컨테이너 안 개발 환경 |
| **Remote - SSH** | 원격 서버에 VS Code로 붙기 |
| **Remote - WSL** | Windows에서 WSL 폴더를 네이티브처럼 |
| **Kubernetes** (MS) | 클러스터·리소스 탐색 (선택) |
| **YAML** (Red Hat) | k8s·Compose YAML 스키마·자동완성 |
| **Even Better TOML** | `Cargo.toml` 등 (필요 시) |

→ [[Docker 사용법]], [[쿠버네티스]], [[윈도우 사용법]](WSL)

---

## 5. 마크다운 · 이 위키

| 확장 | 용도 |
|------|------|
| **Markdown All in One** | 목차·단축키·목록 편집 |
| **markdownlint** | MD 스타일·깨진 링크 |
| **Markdown Preview Enhanced** | 미리보기 강화 (무거우면 All in One만) |
| **Paste Image** | 클립보드 이미지를 폴더에 저장·링크 |

Obsidian vault를 열 때: 편집은 VS Code, `[[위키링크]]`·그래프는 [[Obsidian 사용법]]이 유리하다. 
공개 여부는 vault 루트 `공개 규칙.md`(사이트 비공개).

---

## 6. 화면·생산성 (취향)

| 확장 | 용도 |
|------|------|
| **Material Icon Theme** / **vscode-icons** | 파일 아이콘 |
| **One Dark Pro** 등 | 색 테마 (하나만) |
| **Peacock** | 창/워크스페이스마다 테두리 색 (여러 창 구분) |
| **Project Manager** | 최근 프로젝트 즐겨찾기 |
| **Partial Diff** / 내장 diff | 선택 영역 비교 — 폴더 전체는 [[WinMerge 사용법]] |
| **REST Client** 또는 **Thunder Client** | `.http`로 API 호출 (Postman 대체) |
| **Draw.io Integration** | 다이어그램 (선택) |

테마·아이콘은 취향이라 **추천이 곧 정답은 아니다**.

---

## 7. 쓰지 않거나 신중히

| 종류 | 이유 |
|------|------|
| 거대 “Extension Pack” 남발 | 안 쓰는 언어까지 로드 |
| 유명도만 높은 구형 확장 | 업데이트 중단·보안 |
| 동일 역할 중복 (포맷터 2개) | 저장할 때마다 충돌 |
| 피싱성 유사 이름 | 게시자·설치 수 확인 |
| 브라우저 자동화·크롤러 계열 | 권한·정책 이슈 가능 |

AI 코딩은 **§10 Copilot · §11 Continue**. Cursor와 구독·단축키가 겹치면 하나만 켠다.

---

## 8. 추천 최소 세트 (예시)

일상·위키 + 가벼운 개발만 한다면:

1. Korean Language Pack 
2. GitLens 
3. Error Lens 
4. Markdown All in One 
5. (Python이면) Python + Pylance 
6. (Java면) Extension Pack for Java 
7. (C/C++이면) C/C++ Extension Pack — §12 
8. (AI면) Copilot **또는** Continue 중 하나 — §10·§11 
9. (컨테이너면) Docker + YAML 
10. Prettier 또는 언어 공식 포맷터 

이후 필요할 때만 추가.

---

## 9. 설치·백업 팁

```text
확장 뷰 → 검색 → Install
프로필/Settings Sync로 다른 PC에 복제
```

명령 팔레트:

- `Extensions: Show Recommended Extensions` — 워크스페이스 추천 
- 팀 공유: `.vscode/extensions.json`의 `recommendations`

```json
{
 "recommendations": [
 "ms-vscode.cpptools",
 "ms-vscode.cmake-tools",
 "GitHub.copilot",
 "Continue.continue"
 ]
}
```

ID는 확장 페이지 “Unique Identifier”를 복사한다. Copilot·Continue를 **동시에 추천할 필요는 없다** — 팀 표준 하나만.

---

## 10. GitHub Copilot

전용 정리: [[GitHub Copilot]] (Microsoft Copilot과 구분).

게시자: **GitHub**. 대표 확장:

| 확장 | ID | 역할 |
|------|-----|------|
| **GitHub Copilot** | `GitHub.copilot` | 인라인 완성(회색 제안) |
| **GitHub Copilot Chat** | `GitHub.copilot-chat` | 사이드바·인라인 채팅 (최근엔 묶이거나 함께 설치) |

유료 구독(개인·학생·회사)이 필요하다. 요금·정책은 [GitHub Copilot](https://github.com/features/copilot) 확인.

### 무엇을 잘하나

- 커서 위치·주석·함수 시그니처를 보고 **다음 줄·블록 제안**
- 채팅으로 설명·리팩터·테스트 초안
- 슬래시 명령·에이전트형 기능은 버전에 따라 추가됨

### 기본 조작 (Windows, 바뀔 수 있음)

| 동작 | 설명 |
|------|------|
| 제안 수락 | `Tab` |
| 제안 거부 | `Esc` |
| 다음/이전 제안 | `Alt` + `]` / `Alt` + `[` (환경에 따라) |
| 채팅 열기 | 명령 팔레트 `Chat` / 사이드바 Copilot 아이콘 |
| 인라인 채팅 | `Ctrl` + `I` 부근 (키맵 확인) |

단축키는 `Ctrl` + `K`, `Ctrl` + `S`에서 “Copilot”으로 검색해 본인 환경에 맞춘다.

### 설정·습관

1. GitHub 계정으로 로그인·구독 활성화 
2. 회사 코드는 **조직 Copilot 정책·허용 저장소** 확인 
3. 제안은 **읽고 수락** — 컴파일·테스트 전제 
4. 시크릿·API 키·개인정보를 프롬프트/파일에 두지 않기 
5. [[Cursor 사용법]]과 **동시 사용 시** 완성 팝업이 이중으로 뜨면 한쪽 disable 

### VS Code vs Cursor

| | Copilot (VS Code) | Cursor |
|--|-------------------|--------|
| 기반 | VS Code + 확장 | VS Code 포크 + 내장 AI |
| 과금 | GitHub 구독 | Cursor 구독 |
| 에이전트 | Chat/에이전트(버전별) | Agent가 제품 핵심 |

이미 Cursor만 쓰면 Copilot 확장은 보통 불필요하다.

---

## 11. Continue

게시자·검색: **Continue** (`Continue.continue`). 
오픈소스에 가까운 **자체 모델 연결형** AI 코딩 확장이다. Copilot처럼 “GitHub 고정 모델”이 아니라, **로컬·API 키로 모델/제공자를 고르는** 쪽이 핵심이다.

문서: [https://continue.dev](https://continue.dev)

### Copilot과 차이

| | Continue | GitHub Copilot |
|--|----------|----------------|
| 모델 | 설정으로 OpenAI·Anthropic·로컬(Ollama 등) 등 | GitHub이 제공하는 모델 중심 |
| 과금 | 확장 자체보다 **모델 API·로컬 GPU** 비용 | Copilot 구독 |
| 데이터 | 키·프록시·로컬에 따라 통제 여지 | GitHub/정책 범위 |
| UX | 사이드바 채팅·인라인 편집·컨텍스트 @ | 인라인 완성 + Chat |

“회사 코드를 외부 구독 AI에 덜 보내고, 로컬 모델을 쓰고 싶다” → Continue 검토. 
“설치 후 바로 완성 품질만” → Copilot이 단순할 때가 많다.

### 설치·첫 설정

1. 확장 `Continue` 설치 
2. 사이드바 Continue 아이콘 → 모델/제공자 설정 
3. API 키는 **User secrets·Continue 설정**에만 (Git 커밋 금지) 
4. 로컬이면 Ollama 등 실행 후 모델명 연결 

설정 파일 위치는 버전마다 `~/.continue/config.json`(또는 yaml) 형태가 흔하다. UI 마법사가 있으면 그걸 우선.

### 쓰는 흐름

- **채팅**: 코드 설명, 리팩터 제안, 에러 해석 
- **Edit / 인라인**: 선택 영역을 지시문으로 수정 
- **@파일·@폴더**: 컨텍스트로 코드 첨부 (Continu 쪽 `@` 문법 — UI 힌트 따름) 
- 탭 완성 계열이 있으면 Copilot과 **동시에 켜지 말 것**

### 주의

1. API 키 유출·프롬프트에 시크릿 포함 금지 
2. 로컬 모델은 **품질·속도·VRAM** 편차가 큼 
3. 에이전트가 파일을 직접 고치면 diff를 반드시 리뷰 
4. 팀 표준이 Copilot이면 Continue는 개인 프로필에서만 

---

## 12. C/C++ 확장 (Microsoft)

C/C++ 개발의 기본 축은 Microsoft **C/C++** 확장이다.

| 항목 | 내용 |
|------|------|
| 검색 이름 | `C/C++` |
| ID | `ms-vscode.cpptools` |
| 묶음 | **C/C++ Extension Pack** (`ms-vscode.cpptools-extension-pack`) — CMake Tools, Themes 등 포함되는 구성 |

관련:

| 확장 | 용도 |
|------|------|
| **CMake Tools** | `CMakeLists.txt` 구성·빌드·디버그 타깃 |
| **C/C++ Themes** | 문법 강조 테마 (팩에 포함되기도) |
| **Makefile Tools** | Makefile 프로젝트 (선택) |

언어·포인터 개념: [[C언어와 포인터]]

### Windows에서 컴파일러

확장만으로는 **컴파일러가 없다**. 예:

- **MSVC** — Visual Studio Build Tools 
- **MinGW-w64** / MSYS2 
- **WSL** 안 `gcc`/`clang` + [[윈도우 사용법]]·Remote WSL 

명령 팔레트: `C/C++: Edit Configurations (UI)` 또는 `c_cpp_properties.json`으로 includePath·compilerPath 지정.

`.vscode/c_cpp_properties.json` 예:

```json
{
 "configurations": [
 {
 "name": "Win32",
 "compilerPath": "C:/mingw64/bin/g++.exe",
 "intelliSenseMode": "windows-gcc-x64",
 "cStandard": "c17",
 "cppStandard": "c++17",
 "includePath": ["${workspaceFolder}/**"]
 }
 ],
 "version": 4
}
```

경로는 본인 PC에 맞게. IntelliSense가 빨간 줄이어도 **실제 빌드 설정과 따로**일 수 있다.

### 빌드·실행

- 단순: `tasks.json`으로 `gcc main.c -o main` 후 실행 
- CMake: CMake Tools로 Configure → Build → Debug 
- F5 디버그: `launch.json`에서 `cppdbg` 또는 `cppvsdbg`(MSVC)

### IntelliSense가 이상할 때

1. `compilerPath`가 실제 컴파일러를 가리키는지 
2. 헤더 includePath (라이브러리·서브모듈) 
3. 명령 팔레트 `C/C++: Reset IntelliSense Database` 
4. 대형 모노레포는 파일 제외·제한 

### 디버그

브레이크포인트 → F5. 
Watch·Call Stack·메모리(주소)는 포인터 학습([[C언어와 포인터]])과 함께 보면 이해가 빠르다.

### 추천 조합

```text
C/C++ Extension Pack
 + (CMake면) CMake Tools 확인
 + Error Lens
 + (선택) GitLens
 + (선택) Copilot 또는 Continue — 완성은 AI, 빨간 줄·디버그는 cpptools
```

---

## 관련

- [[VS Code 사용법]]
- [[Cursor 사용법]]
- [[C언어와 포인터]]
- [[생활위키 목차]]
- [[DBeaver 사용법]]
- [[Docker 사용법]]
- [[Oracle DB와 튜닝]]
- [[Java 언어 학습]]
- [[Python 학습과 패키지]]
- [[현존 AI 비교]]
