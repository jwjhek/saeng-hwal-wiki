---
publish: true
draft: false
---

# GitHub

> **분류:** 개발 › 인프라 · [[생활위키 목차]]

[GitHub](https://github.com)은 Git 원격 저장소를 호스팅하고, **Pull Request·Issues·Actions·Pages** 등으로 협업·자동화를 붙인 서비스다. 
버전 관리 **명령·개념**은 [[Git 사용법]], 비슷한 제품(MR·셀프호스트)은 [[GitLab]].

공식: [https://github.com](https://github.com) 
문서: [https://docs.github.com](https://docs.github.com)

확인일: 2026-08-07

관련: [[Git 사용법]] · [[GitLab]] · [[Cursor 사용법]] · [[VS Code 추천 확장]]

---

## 1. 개요

| 항목 | 설명 |
|------|------|
| 핵심 | Git **원격** + 웹 협업 |
| 단위 | Repository(저장소), Organization(조직) |
| 공개 | **Public** / **Private** |
| 리뷰 | **Pull Request(PR)** 로 브랜치 병합 제안 |
| 자동화 | **Actions**(CI/CD 워크플로) |
| 정적 사이트 | **Pages** (이 생활위키 배포에 쓰이기도 함) |
| AI | Copilot 등은 [[VS Code 추천 확장]] · 별도 구독 |

```text
로컬 Git 커밋
 ↓ push
GitHub 저장소
 ↓ PR
리뷰·Checks(Actions)
 ↓ merge
main (등 기본 브랜치)
```

---

## 2. Git과의 관계

| | [[Git 사용법\|Git]] | GitHub |
|--|---------------------|--------|
| 어디 | 내 PC(및 모든 원격) | github.com(및 Enterprise) |
| 필수? | 버전 관리의 본체 | 원격·협업에 자주 쓰는 **한 곳** |
| 없어도 | 로컬 이력만으로 가능 | Git 없이 “GitHub만”은 의미 없음 |

SSH 키 또는 HTTPS + Personal Access Token(PAT)·자격 증명으로 `git push`한다. 
계정 **2FA** 권장.

---

## 3. 저장소 · 첫 push

1. New repository — 이름, Public/Private, README·`.gitignore` 여부 
2. 로컬에서:

```powershell
git remote add origin https://github.com/사용자/저장소.git
git push -u origin main
```

또는 빈 원격만 만들고 로컬 `git init` 후 연결. 
**GitHub CLI**(`gh`)로 생성·PR도 가능하다.

| 설정 | 설명 |
|------|------|
| Default branch | 보통 `main` |
| Branch protection | force push·직접 커밋 제한, PR 필수 |
| Collaborators / Teams | 권한 |
| Secrets | Actions용 비밀. 코드에 하드코딩 금지 |

---

## 4. Pull Request (PR)

| 단계 | 설명 |
|------|------|
| 브랜치 | `feature/...`에서 작업·push |
| PR 생성 | base(`main`) ← compare(기능 브랜치) |
| 설명 | 무엇을·왜·테스트 방법 |
| 리뷰 | Approve / Request changes |
| Checks | Actions·봇 통과 여부가 막히기도 함 |
| Merge | Create a merge commit / Squash / Rebase — **팀 규칙** |

Issue로 할 일을 적고 PR에 `Fixes #번호`를 넣는 흐름이 흔하다.

---

## 5. Actions · Pages · 기타

| 기능 | 설명 |
|------|------|
| Actions | `.github/workflows/*.yml` — 테스트·빌드·배포 |
| Pages | 정적 사이트 호스팅. 이 vault는 [[Quartz]] 빌드 → Actions 배포 |
| Packages | 컨테이너·라이브러리 패키지 호스팅 |
| Codespaces | 클라우드 개발 환경 |
| Dependabot | 의존성·보안 업데이트 PR |
| Security | secret scanning, Dependabot alerts 등 |

워크플로에 쓰는 토큰·클라우드 키는 **Settings → Secrets**에만.

---

## 6. [[GitLab]]과 고를 때

| | GitHub | GitLab |
|--|--------|--------|
| 강점 | 오픈소스·커뮤니티·Actions·Copilot 생태계 | MR+내장 CI, **셀프호스트**, DevOps 일체형 |
| PR 이름 | Pull Request | Merge Request |
| CI | Actions | GitLab CI/CD (`.gitlab-ci.yml`) |
| 회사 | GitHub.com / Enterprise | gitlab.com / Self-managed |

둘 다 원격은 [[Git 사용법]]과 같다. 이 위키·많은 개인 프로젝트는 GitHub Pages 경로가 흔하다.

---

## 7. 보안 · Public 주의

| 주의 | 왜 |
|------|-----|
| `.env`·키·비밀번호 커밋 | Public이면 즉시 유출. Private도 협업자·유출 위험 |
| `publish: false` 노트 | 사이트에는 안 나가도 **GitHub 소스에는 보일 수 있음** |
| force push to main | 이력·협업 파괴 |
| 낯선 Actions 마켓플레이스 | 써드파티 액션 신뢰·핀 버전 |
| 피싱 | 가짜 GitHub 로그인·악의적 OAuth |

실수로 올린 비밀은 **폐기(로테이션)** 가 먼저다.

---

## 8. 실전 체크

- [ ] [[Git 사용법]]으로 로컬 커밋이 되는가 
- [ ] remote·SSH/HTTPS 인증 
- [ ] Public/Private·`.gitignore` 
- [ ] PR로 병합하는가 (혼자여도 습관에 유용) 
- [ ] Actions Secrets에만 비밀 
- [ ] 대안·회사 표준이 [[GitLab]]인지 확인 

---

## 9. 정리

GitHub는 Git 저장소를 **호스팅하고 PR·Actions·Pages로 확장**한 협업 플랫폼이다. 
매일 흐름은 clone/push + PR이고, 개념 뼈대는 [[Git 사용법]], 비교는 [[GitLab]]이다.

---

## 면책

> **면책** 
> 제품·요금·UI·정책은 자주 바뀐다. **공식 문서·설정 화면**이 우선. 
> Public 저장소는 누구나 클론·열람할 수 있다. 비밀·개인정보를 올리지 말 것. 
> 이 글은 가입·유료 플랜 권유가 아니다.

---

## 관련

- [[생활위키 목차]]
- [[Git 사용법]]
- [[GitLab]]
- [[VS Code 사용법]]
- [[VS Code 추천 확장]]
- [[Cursor 사용법]]
- [[Quartz]]
- [[Docker 사용법]]
- [[Playwright]]
- [[쿠버네티스]]
