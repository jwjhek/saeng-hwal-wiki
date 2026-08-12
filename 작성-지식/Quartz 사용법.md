---
publish: true
draft: false
aliases:
  - Quartz
---

# Quartz 사용법

> **분류:** 작성·지식 › 노트·지식 · [[생활위키 목차]]

**Quartz**는 마크다운 노트(특히 **Obsidian** vault)를 **정적 웹사이트**로 빌드하는 도구다. 
공개 위키는 Obsidian으로 글을 쓰고, Quartz로 **`publish: true`만 골라** [GitHub Pages](https://pages.github.com)에 올릴 수 있다.

공식: [https://quartz.jzhao.xyz](https://quartz.jzhao.xyz)  
프로젝트 예: `quartz.config.yaml` · `npm run preview:wiki` · `.github/workflows/deploy.yml`

확인일: 2026-08-11

관련: [[Obsidian 사용법]] · [[공개 규칙]] · [[GitHub]] · [[Cursor 사용법]]

---

## 1. 개요

| 항목 | 설명 |
|------|------|
| 무엇 | **SSG**(정적 사이트 생성기). `.md` → HTML·CSS·JS 묶음 |
| 만든 이유 | 디지털 가든·위키·노트를 **웹에 공개** (서버 없이 호스팅 가능) |
| Obsidian | `[[위키링크]]`, callout, mermaid 등 **OFM** 지원 플러그인 사용 |
| 예시 프로젝트 | vault **루트**가 콘텐츠 (`npx quartz build -d .`) |
| 공개 정책 | **ExplicitPublish** — `publish: true`인 글만 사이트에 포함 |

Quartz는 **편집기가 아니다.** 글은 [[Obsidian 사용법]]·[[Cursor 사용법]]에서 쓰고, Quartz는 **빌드·배포** 담당이다.

---

## 2. 프로젝트 구성 예

```text
[작성] Obsidian / Cursor → .md (분류 폴더)
 ↓ frontmatter publish: true/false
[빌드] Quartz (로컬 preview 또는 GitHub Actions)
 ↓ public/
[호스팅] GitHub Pages (baseUrl 설정)
 ↓
읽는 사람 — 검색·그래프·다크모드 사이트
```

| 층 | 도구·경로 |
|----|-----------|
| 로컬 위키 | Obsidian vault = `생활위키/` 폴더 |
| 비공개 메모 | `private/` (gitignore), `publish: false` |
| 사이트 홈 | `index.md` |
| 목차 | `생활위키 목차.md` |
| 작성자 메타 | `공개 규칙.md` (**사이트 비공개**, `publish: false`) |
| 설정 | `quartz.config.yaml` |
| 산출물 | `public/` (빌드 결과, 배포용) |

상세 공개 절차·민감 정보 기준은 vault 루트 **`공개 규칙.md`** (웹에 안 올림). 이 글은 **Quartz 개념·빌드** 위주다.

---

## 3. 다른 방식과 비교

| | Quartz + Obsidian | Obsidian Publish | Notion 공개 |
|--|-------------------|------------------|-------------|
| 파일 소유 | 로컬 **.md** | Obsidian 클라우드 | Notion 서버 |
| 비용 | 호스팅만 (Pages 무료 등) | 유료 구독 | 플랜에 따름 |
| 위키링크 | `[[파일명]]` 네이티브 | Obsidian 전용 | Notion 링크 |
| 선별 공개 | `publish: true` | 노트별 설정 | 페이지 권한 |
| 커스터마 | `quartz.config.yaml`·플러그인 | 테마 제한적 | Notion UI 고정 |
| 이 위키 | **채택** | 미사용 | [[Notion 사용법]] 별도 |

[[GitHub]] **Pages** + Actions로 push 시 자동 배포하는 구성이 흔하다.

---

## 4. 빌드가 하는 일

1. vault에서 `.md` 수집 (`ignorePatterns`로 `templates/`·`private/`·엔진 파일 제외)  
2. **필터** — `remove-draft`, **explicit-publish** (`publish: true`만)  
3. **변환** — Obsidian 마크다운·GFM·LaTeX·mermaid 등  
4. **링크** — `[[위키링크]]`를 HTML 경로로 (`shortest` 해상도)  
5. **페이지 생성** — 글·폴더·태그·그래프·검색 인덱스  
6. **출력** — `public/`에 정적 파일  

사이트는 **SPA**(단일 페이지 앱) 옵션이 켜져 있어 페이지 이동이 빠른 편이다 (`enableSPA: true`).

---

## 5. 핵심 설정 (`quartz.config.yaml`)

| 항목 | 프로젝트 예 |
|------|-------------|
| `pageTitle` | 사이트 제목 |
| `locale` | `ko-KR` |
| `baseUrl` | GitHub Pages 경로 (`username.github.io/repo-name`, `https://` 없이) |
| `ignorePatterns` | `private`, `templates`, `.obsidian`, `node_modules`, `**/*.md` 제외한 비마크다운 등 |
| `theme` | 글꼴·라이트/다크 색 |
| `plugins` | OFM, 검색, 그래프, 목차, 백링크, RSS 등 |

`baseUrl`이 실제 Pages 주소와 다르면 **내부 링크·OG 이미지·sitemap**이 깨질 수 있다. 저장소 이름·Pages 설정을 바꿨으면 **함께** 수정한다.

---

## 6. 공개·비공개 (frontmatter)

```yaml
---
publish: true   # 사이트에 포함
draft: false    # true면 remove-draft로 제외
---
```

| 값 | Quartz 동작 |
|----|-------------|
| `publish: true` | **ExplicitPublish** 통과 → 사이트 노출 |
| `publish` 없음 / `false` | vault·Git에는 있을 수 있으나 **사이트 미포함** |
| `draft: true` | 빌드 제외 |

**주의:** GitHub 저장소가 **public**이면 `publish: false` 글도 **Git에는 보인다.** 비밀은 `private/`(gitignore) 또는 **private repo**.  
암호 걸기는 `encrypted-pages` 플러그인으로 가능하나, 예시 프로젝트에서는 일반 글을 `publish`로 나눈다.

템플릿: `templates/노트-공개.md`, `templates/노트-비공개.md`

---

## 7. 로컬 미리보기·빌드

Node **22+**, npm **10.9+** (`package.json` engines).

```bash
npm ci
npx quartz plugin install
npm run preview:wiki
```

| 스크립트 | 설명 |
|----------|------|
| `npm run preview:wiki` | `quartz build --serve -d .` — 로컬 서버 + 핫 리로드 |
| `npm run build:wiki` | `quartz build -d .` → `public/`만 생성 |

Windows에서 `quartz` 실행 권한 이슈가 있으면 `node ./quartz/bootstrap-cli.mjs build -d .` (CI와 동일).

미리보기에서 **깨진 위키링크·제목·목차**를 확인한 뒤 push하는 편이 안전하다.

---

## 8. GitHub Actions 배포

`.github/workflows/deploy.yml` 요약:

```text
push main (또는 workflow_dispatch)
 ↓ checkout (fetch-depth: 0 — 날짜·git 플러그인용)
 ↓ npm ci · plugin install
 ↓ quartz build -d .
 ↓ public/ → GitHub Pages artifact
 ↓ deploy-pages
```

- `publish: true`만 사이트에 들어간다 (워크플로 주석과 동일).  
- 플러그인 캐시: `.quartz/plugins`, `quartz.lock.json`  
- 배포 URL은 저장소 **Settings → Pages**와 `baseUrl` 일치 확인  

[[Git 사용법]]으로 `main`에 push하면 자동 배포되는 **CI/CD** 한 축이다.

---

## 9. 켜져 있는 기능 (요약)

예시 `quartz.config.yaml` 기준, 읽는 사람이 쓰는 UI:

| 기능 | 플러그인·설정 |
|------|----------------|
| `[[위키링크]]` | obsidian-flavored-markdown, crawl-links |
| Callout·하이라이트 | OFM |
| Mermaid | OFM |
| 검색 | search |
| 그래프 | graph |
| 백링크 | backlinks |
| 목차(우측) | table-of-contents |
| 다크모드·리더 모드 | darkmode, reader-mode |
| 탐색기(좌측) | explorer |
| RSS·sitemap | content-index |
| 수정일 | created-modified-date |
| 별칭 URL | alias-redirects (`aliases` frontmatter) |

댓글(giscus)은 **비활성**. 필요 시 플러그인 설정 후 활성화.

---

## 10. 폴더·파일 규칙

| 경로 | 빌드 |
|------|------|
| `PC-OS/`, `생활-건강/` 등 **분류 폴더**의 `.md` | `publish: true`면 포함 |
| `templates/` | **제외** |
| `private/` | **제외** + gitignore |
| `quartz/`, `node_modules/` | 엔진·의존성, 콘텐츠 아님 |
| `index.md` | 사이트 홈 |

`[[위키링크]]`는 **파일명** 기준이라 폴더가 달라도 연결된다 ([[Obsidian 사용법]]과 동일).

---

## 11. 자주 하는 문제

| 증상 | 확인 |
|------|------|
| 글이 사이트에 안 보임 | `publish: true`? `draft: false`? |
| 링크 404 | 대상 글도 `publish: true`? 파일명·별칭 오타? |
| 스타일·경로 깨짐 | `baseUrl`이 Pages URL과 일치? |
| 로컬만 되고 CI 실패 | Node 버전, `npm ci`, `plugin install` |
| 비밀 글이 웹에 노출 | `publish: false`만으로는 **public repo Git에 노출** — `private/` 사용 |
| 한글 경로·Windows | UTF-8 저장, 경로는 vault 루트 기준 `-d .` |

Quartz 엔진 자체를 수정할 때는 upstream([jackyzha0/quartz](https://github.com/jackyzha0/quartz))과 diff를 관리한다. 일반 글 작성만 할 때는 **설정·frontmatter**만 보면 된다.

---

## 12. 작성 루틴 (Quartz 관점)

1. [[Cursor 사용법]] 또는 Obsidian으로 분류 폴더에 `.md` 작성  
2. 상단 `publish`·`draft` 결정 ([[공개 규칙]] 내용은 로컬 `공개 규칙.md`)  
3. `npm run preview:wiki`로 링크·제목 확인  
4. [[Git 사용법]] commit → `main` push → Actions 배포  
5. [[생활위키 목차]]에 한 줄 추가  

---

## 13. 정리

| 항목 | 한 줄 |
|------|--------|
| 정의 | Obsidian형 마크다운 → **정적 위키 사이트** 생성기 |
| 예시 프로젝트 | 루트가 콘텐츠, **`publish: true`만 공개** |
| 로컬 | `npm run preview:wiki` |
| 배포 | GitHub Actions → **Pages** |
| 편집 | Quartz가 아니라 **Obsidian·Cursor** |

---

## 면책

> **면책**  
> Quartz·플러그인·Node 요구 사항은 **버전마다 다르다.** 공식 문서·`package.json` engines를 본다.  
> `publish: false`도 **public Git**에 올라가면 저장소에서 읽힐 수 있다.  
> 이 글은 프로젝트 구성 예시이며, 다른 Quartz 프로젝트와 1:1 같지 않을 수 있다.

---

## 관련

- [[생활위키 목차]]
- [[Obsidian 사용법]]
- [[Cursor 사용법]]
- [[GitHub]]
- [[Git 사용법]]
- [[Google AdSense 사용법]]
- [[Notion 사용법]]
- [[VS Code 사용법]]
