---
publish: true
draft: false
---

# Cursor 스킬 설정

> **분류:** 작성·지식 › 에디터·IDE · [[생활위키 목차]]

Cursor **Agent Skills(스킬)** 는 에이전트에게 특정 작업 절차를 가르치는 `SKILL.md` 묶음이다.  
채팅·에이전트 기본 조작은 [[Cursor 사용법]], 항상 켜 두는 규칙은 [[#6. 규칙(Rules)과 스킬 차이|규칙]] 쪽을 본다.

제품·경로 UI는 버전에 따라 바뀔 수 있다. 확인일: 2026-08-07

관련: [[Cursor 사용법]] · [[VS Code 사용법]]

---

## 1. 한눈에

| 항목 | 감각 |
|------|------|
| 무엇 | 폴더 하나 + **`SKILL.md`** (필요 시 참고 문서·스크립트) |
| 하는 일 | PR 리뷰 방식, 커밋 메시지 형식, 위키 작성 절차 등 **반복 워크플로**를 에이전트에 주입 |
| 개인 | `~/.cursor/skills/스킬이름/` — 모든 프로젝트 |
| 프로젝트 | `.cursor/skills/스킬이름/` — 이 저장소를 쓰는 사람과 공유 |
| 넣지 말 것 | `~/.cursor/skills-cursor/` — **Cursor 내장 스킬** 영역. 사용자가 여기다 만들면 안 됨 |

```text
SKILL.md (이름·설명·절차)
    ↓ 에이전트가 필요할 때 읽음
특정 작업만 팀/개인 방식으로 수행
```

Windows 예: `C:\Users\사용자\.cursor\skills\my-skill\SKILL.md`

---

## 2. 규칙(Rules)과 스킬 차이

| | Rules (규칙) | Skills (스킬) |
|--|--------------|---------------|
| 느낌 | “이 프로젝트에서는 **항상** 이렇게” | “이 **종류의 일**을 할 때 이렇게” |
| 위치 예 | `.cursor/rules/`, 사용자 규칙, `AGENTS.md` | `.cursor/skills/`, `~/.cursor/skills/` |
| 예 | 한글로 쓰기, 커밋하지 말 것, 폴더 구조 | PDF 추출 절차, 쇼츠 대본 템플릿, 배포 체크리스트 |

둘 다 쓸 수 있다. 짧은 상시 제약은 규칙, **단계가 긴 절차**는 스킬이 맞다.  
[[Cursor 사용법]] § 규칙·MCP 언급과 같이 본다.

---

## 3. 폴더 구조

```text
skill-name/
├── SKILL.md          ← 필수
├── reference.md      ← 선택 (자세한 참고)
├── examples.md       ← 선택
└── scripts/          ← 선택 (헬퍼 스크립트)
```

- `SKILL.md`는 **대략 500줄 안**을 권장. 길면 `reference.md`로 나누기  
- 링크는 **한 단계**만 (SKILL → reference). 깊게 중첩하지 말 것  
- 스크립트 경로 예시는 `scripts/helper.py`처럼 **슬래시** 사용 (백슬래시 지양)

---

## 4. SKILL.md 작성법

### 4.1 Frontmatter

```markdown
---
name: wiki-shorts
description: >
  생활위키 글에서 YouTube Shorts 대본·체크리스트를 만든다.
  Use when the user asks for Shorts scripts from wiki notes.
disable-model-invocation: true
---
```

| 필드 | 규칙 |
|------|------|
| `name` | 소문자·숫자·하이픈, 최대 64자 |
| `description` | 비어 있으면 안 됨. **무엇을 + 언제** (최대 1024자) |
| `disable-model-invocation` | 기본으로 `true`면 **이름을 불렀을 때만** 로드. 생략하면 맥락으로 자동 호출될 수 있음 |

### 4.2 description 잘 쓰기

에이전트가 “이 스킬을 쓸지” 판단하는 핵심이다.

| 좋은 예 | 피하기 |
|---------|--------|
| 3인칭, 구체 동사·파일 종류 | “내가 도와줄게”, “문서를 돕습니다” |
| WHAT + WHEN | “유용한 도구입니다”만 |
| 트리거 단어 포함 (PDF, Shorts, 커밋…) | 모호한 `helper`, `utils` |

```yaml
# 예
description: >
  Generate descriptive commit messages from git diffs.
  Use when the user asks for commit messages or reviews staged changes.
```

### 4.3 본문

- 에이전트가 **이미 아는 일반론**은 줄이기  
- 체크리스트·템플릿·명령 예시를 구체로  
- 사용자가 **그대로 쓰라고 한 문장**은 바꿔 쓰지 말 것  

---

## 5. 만드는 순서 (설정 감각)

1. **목적** — 어떤 작업인가  
2. **위치** — 개인(`~/.cursor/skills`) vs 프로젝트(`.cursor/skills`)  
3. **트리거** — 언제 자동/수동으로 쓰게 할 것인가  
4. **폴더 + SKILL.md** 작성  
5. Cursor를 쓰며 “○○ 스킬로 …”라고 불러 보거나, 자동 호출이면 관련 요청으로 시험  

에이전트에게 “스킬 만들어줘”라고 하면, 위 정보를 물어본 뒤 파일을 만들어 주는 흐름이 흔하다.

---

## 6. 호출 · 사용

| 방식 | 감각 |
|------|------|
| 명시 | 채팅에 스킬 이름·경로·“○○ 스킬 따라” |
| 자동 | `disable-model-invocation`을 끄고 description이 요청과 맞을 때 (버전·설정에 따름) |
| 내장 | `skills-cursor` 아래 create-skill, create-rule 등은 Cursor가 관리 |

스킬이 안 먹으면: 경로·`name`·오타, 개인/프로젝트 위치, Cursor 재시작·최신 여부부터 본다.

---

## 7. 생활위키에 쓸 때 예

| 스킬 아이디어 | 내용 감각 |
|---------------|-----------|
| 위키 노트 | frontmatter `publish`, 분류 줄, 목차 한 줄 추가 |
| 쇼츠 대본 | [[위키 쇼츠 자동 제작]] 템플릿 |
| 쿠폰 점검 | [[최저가와 쿠폰]] 확인일·만료 행 정리 |

프로젝트 공통이면 `생활위키/.cursor/skills/` 에 두고 Git으로 공유할 수 있다.  
비밀·AdSense 키 등은 스킬에 **넣지 말 것**.

---

## 8. 안티패턴

| 피하기 | 대신 |
|--------|------|
| `skills-cursor`에 사용자 스킬 생성 | `skills` 또는 `.cursor/skills` |
| 이름 `helper`, `utils` | `processing-pdfs`처럼 구체적 |
| SKILL.md에 장문 백과 | 요약 + `reference.md` |
| 여러 라이브러리 나열만 | 기본 하나 + 예외 한 줄 |
| 날짜에 묶인 “2025년 이전 API” | 현재 방법 + deprecated 접기 |

---

## 9. 실전 체크

- [ ] 위치가 `skills` / `.cursor/skills` 인가 (`skills-cursor` 아님)  
- [ ] `name` · `description`(WHAT+WHEN, 3인칭)  
- [ ] 본문 짧고 절차·예시가 있는가  
- [ ] 규칙과 역할이 겹치면 나눴는가  
- [ ] 에이전트 기본 UI는 [[Cursor 사용법]]  

---

## 10. 정리

Cursor 스킬은 **`SKILL.md`로 에이전트에게 특수 절차를 심는 설정**이다.  
개인·프로젝트 폴더에 두고, 설명문과 짧은 체크리스트가 품질을 가른다.  
일상 편집은 [[Cursor 사용법]], 상시 제약은 규칙을 쓴다.

---

## 관련

- [[생활위키 목차]]
- [[Cursor 사용법]]
- [[VS Code 사용법]]
- [[VS Code 추천 확장]]
- [[위키 쇼츠 자동 제작]]
- [[최저가와 쿠폰]]
- [[Git 사용법]]
