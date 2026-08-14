---
publish: true
draft: false
---

# Git 사용법

> **분류:** 개발 › 인프라 · [[생활위키 목차]]

**Git**은 파일 변경을 **커밋(스냅샷)** 으로 쌓아 두는 **분산 버전 관리** 도구다. 
로컬만으로도 동작하고, 원격 저장소는 [[GitHub]]·[[GitLab]] 등이 맡는다.

공식: [https://git-scm.com](https://git-scm.com) 
문서: [https://git-scm.com/doc](https://git-scm.com/doc)

확인일: 2026-08-07

관련: [[GitHub]] · [[GitLab]] · [[VS Code 사용법]] · [[Cursor 사용법]] · [[WinMerge 사용법]]

---

## 1. 개요

| 항목 | 설명 |
|------|------|
| 하는 일 | “언제 무엇이 바뀌었는지”를 커밋으로 기록·되돌리기·협업 |
| 로컬 | PC의 `.git` 폴더가 저장소 |
| 원격 | [[GitHub]]·[[GitLab]] 등에 `push` / `pull` |
| UI | 터미널, 또는 [[VS Code 사용법]]·[[Cursor 사용법]] 소스 제어 |

```text
작업 폴더 (수정)
 ↓ git add
스테이징 (올릴 조각)
 ↓ git commit
로컬 이력
 ↓ git push
원격 ([[GitHub]] / [[GitLab]])
```

---

## 2. 설치 · 최초 설정

| OS | 설명 |
|----|------|
| Windows | [git-scm.com](https://git-scm.com) 설치. Git Bash·자격 증명 관리자 포함되는 경우가 많음 |
| macOS | Xcode CLT 또는 공식 설치 |
| Linux | 배포판 패키지 (`git`) |
| Android | [[Termux 사용법]] — `pkg install git` |

```powershell
git config --global user.name "이름"
git config --global user.email "이메일@example.com"
git config --global init.defaultBranch main
git --version
```

이메일은 [[GitHub]]/[[GitLab]] 계정과 맞추면 커밋 작성자 연결이 쉽다. 
`--global`은 사용자 전체, 저장소만이면 그 폴더에서 `--global` 없이.

---

## 3. 핵심 용어

| 말 | 설명 |
|----|------|
| 저장소(repo) | `.git`이 있는 프로젝트 |
| 커밋 | 시점 스냅샷 + 메시지 |
| 브랜치 | 갈라진 작업 줄. 기본 이름이 흔히 `main` |
| 스테이징 | 다음 커밋에 **넣을** 변경만 골라 둠 |
| 원격(remote) | 보통 `origin` → GitHub/GitLab URL |
| clone | 원격 전체를 로컬로 복사 |
| fork | (호스팅) 남의 원격 복사본을 **내 계정**에 만듦 |
| merge / rebase | 브랜치를 합치는 방식 (팀 규칙) |
| .gitignore | 추적하지 않을 경로 (node_modules, .env, `private/` 등) |

---

## 4. 매일 쓰는 명령

### 새 저장소

```powershell
cd 프로젝트폴더
git init
```

또는 원격에서:

```powershell
git clone https://github.com/조직/저장소.git
cd 저장소
```

### 상태 · 차이

```powershell
git status
git diff
git diff --staged
git log --oneline -10
```

### 커밋

```powershell
git add 파일명
git add .
git commit -m "변경 이유를 짧게"
```

메시지를 “뭐가 바뀌었나”보다 **왜**에 가깝게 쓰면 이력이 읽기 쉽다. 
에디터 UI: [[VS Code 사용법]] §8.

### 원격과 동기

```powershell
git remote -v
git push -u origin main
git pull
git fetch
```

`pull` ≈ `fetch` + 병합(설정에 따라 rebase). 충돌 나면 파일을 고치고 다시 커밋/계속.

### 브랜치

```powershell
git branch
git switch -c feature/로그인
git switch main
git merge feature/로그인
```

옛 명령 `git checkout -b`도 많이 보인다. 새 습관은 `switch`/`restore` 쪽.

---

## 5. 되돌리기 (조심해서)

| 상황 | 자주 쓰는 것 | 주의 |
|------|----------------|------|
| 아직 add 전 수정 버리기 | `git restore 파일` | 내용 사라짐 |
| add 취소 | `git restore --staged 파일` | 작업 내용은 남음 |
| 마지막 커밋 메시지만 | `git commit --amend` | **이미 push한 커밋은** 팀과 합의 없이 amend·force 금지 |
| 커밋은 남기고 취소 커밋 | `git revert` | 공유 이력에 안전 쪽 |
| 로컬에서만 과거로 | `reset` | 공유 브랜치에 hard reset 위험 |

확실치 않으면 **새 브랜치에 복사**하거나 스태시 전에 백업한다.

```powershell
git stash
git stash pop
```

---

## 6. .gitignore · 비밀

```gitignore
.env
*.pem
node_modules/
private/
.DS_Store
```

한 번 커밋된 비밀은 **이력에 남을 수 있다.** 유출 시 키 교체·이력 정리(고급)·호스팅 지원을 본다. 
민감 폴더는 `private/`·`publish: false`로 사이트 공개 범위와 맞춘다.

---

## 7. 충돌

```text
<<<<<< HEAD
내 쪽
======
상대 쪽
>>>>>> branch
```

1. 파일을 열어 올바른 내용으로 합친다 
2. `git add` 
3. merge면 `git commit`, rebase면 `git rebase --continue` 

폴더 단위 비교는 [[WinMerge 사용법]]도 보조로 쓴다.

---

## 8. GUI · 호스팅과 역할

| 도구 | 역할 |
|------|------|
| Git (이 글) | 로컬 이력·브랜치·명령 |
| [[GitHub]] | 원격·PR·Actions·Pages 등 |
| [[GitLab]] | 원격·MR·CI/CD·셀프호스트 강점 |
| VS Code / Cursor | 스테이징·diff·커밋 UI |
| GitLens 등 | blame·그래프 ([[VS Code 추천 확장]]) |

“GitHub에 올린다” = 대개 **Git 커밋 후 push**. 호스팅만 바꾸고 Git 개념은 같다.

---

## 9. 실전 체크

- [ ] `user.name` / `user.email` 설정 
- [ ] `.gitignore`에 비밀·빌드 산출물 
- [ ] 커밋 전 `status`·`diff` 
- [ ] `main`에 직접 강제 push하지 않음 (팀 규칙) 
- [ ] 원격은 [[GitHub]] 또는 [[GitLab]] 중 어디에 둘지 정함 

---

## 10. 정리

Git은 **로컬 커밋 이력**이 본체이고, [[GitHub]]·[[GitLab]]은 그걸 **공유·리뷰·CI**하는 원격이다. 
매일은 `status` → `add` → `commit` → `push`/`pull`이면 대부분 충분하다.

---

## 면책

> **면책** 
> 학습용이다. 회사 브랜치·권한·훅 규칙은 **팀 문서**가 우선. 
> `push --force`·이력 재작성은 **공유 브랜치에서 위험**하다. 
> 비밀(.env, 키, 비밀번호)을 커밋하지 않는다.

---

## 관련

- [[생활위키 목차]]
- [[GitHub]]
- [[GitLab]]
- [[VS Code 사용법]]
- [[VS Code 추천 확장]]
- [[Cursor 사용법]]
- [[WinMerge 사용법]]
- [[Docker 사용법]]
- [[Playwright]]
- [[Obsidian 사용법]]
