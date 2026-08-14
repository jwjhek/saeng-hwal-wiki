---
publish: true
draft: false
---

# GitLab

> **분류:** 개발 › 인프라 · [[생활위키 목차]]

[GitLab](https://gitlab.com)은 Git 원격 호스팅에 **Merge Request·내장 CI/CD·이슈·패키지** 등을 묶은 DevOps 플랫폼이다. 
saas(gitlab.com)와 **셀프호스트(Self-managed)** 둘 다 쓰인다. 
Git 명령은 [[Git 사용법]], 비슷한 호스팅·PR 문화는 [[GitHub]].

공식: [https://gitlab.com](https://gitlab.com) 
문서: [https://docs.gitlab.com](https://docs.gitlab.com)

확인일: 2026-08-07

관련: [[Git 사용법]] · [[GitHub]] · [[Docker 사용법]] · [[쿠버네티스]]

---

## 1. 개요

| 항목 | 설명 |
|------|------|
| 핵심 | Git **원격** + MR + **CI/CD가 제품 안에** |
| 배포 형태 | gitlab.com / Self-managed (직접 설치) |
| 리뷰 | **Merge Request(MR)** ≈ GitHub의 PR |
| 자동화 | `.gitlab-ci.yml` + **Runner** |
| 그룹 | Group / Subgroup으로 권한·프로젝트 묶기 |

```text
로컬 Git
 ↓ push
GitLab 프로젝트
 ↓ Merge Request
리뷰 · Pipeline(CI)
 ↓ merge
기본 브랜치
```

---

## 2. Git · [[GitHub]]와 관계

| | [[Git 사용법\|Git]] | GitLab | [[GitHub]] |
|--|---------------------|--------|------------|
| 역할 | 이력·브랜치 | 원격+DevOps | 원격+협업/Actions |
| 리뷰 이름 | — | Merge Request | Pull Request |
| CI | — | 내장 CI/CD | Actions |
| 셀프호스트 | — | **강점으로 자주 언급** | Enterprise(별 제품) |

원격 URL만 바꾸면 같은 로컬 저장소를 옮길 수 있다(이력·권한·이슈는 별도 이전).

```powershell
git remote add origin https://gitlab.com/그룹/프로젝트.git
git push -u origin main
```

---

## 3. 프로젝트 · 권한

| 개념 | 설명 |
|------|------|
| Project | 저장소 + 이슈 + CI + 위키 등 |
| Group | 여러 프로젝트·멤버 역할 |
| Visibility | Private / Internal / Public (인스턴스 설정에 따라) |
| Protected branches | main 등에 push·merge 제한 |
| Deploy keys / Access tokens | 자동화·읽기전용 배포 |

회사 GitLab은 **SSO·승인 MR·필수 파이프라인**이 켜져 있는 경우가 많다.

---

## 4. Merge Request (MR)

| 단계 | 설명 |
|------|------|
| 브랜치 push | 웹에서 Create merge request 제안이 뜸 |
| 설명·체크리스트 | 템플릿을 쓰는 조직이 많음 |
| Approvals | 승인 수·코드오너 |
| Pipeline | CI 실패 시 merge 막기 설정 가능 |
| Merge methods | merge commit / fast-forward / squash 등 |

GitHub PR과 **역할이 같고 이름·버튼만 다른** 경우가 많다.

---

## 5. CI/CD 

루트(또는 설정한 경로)의 `.gitlab-ci.yml`:

```yaml
# 개념 예시 — 문법·이미지는 공식 문서 확인
stages:
 - test
 - build

unit:
 stage: test
 image: node:20
 script:
 - npm ci
 - npm test
```

| 말 | 설명 |
|----|------|
| Pipeline | 한 번의 push/MR에 대한 전체 실행 |
| Job | 단계 안의 개별 작업 |
| Runner | Job를 실행하는 에이전트 (공유/전용) |
| CI/CD Variables | 비밀·환경값. Masked·Protected 옵션 |
| Environments | staging/production 배포 추적 |
| Container Registry | 이미지 보관 → [[Docker 사용법]]과 연결 |

러너·도커 소켓·권한은 **보안 설정**을 팀 가이드에 따른다. 
Kubernetes 배포·GitOps는 [[쿠버네티스]]와 겹친다.

---

## 6. [[GitHub]]와 고를 때

| 상황 | 기울기 |
|------|-------------|
| 오픈소스·공개 협업·Actions 예시가 많음 | [[GitHub]] |
| 사내 일체형(이슈+CI+패키지+보안 스캔) | GitLab이 이미 표준인 회사 많음 |
| 직접 서버에 올리고 데이터 주권 | GitLab Self-managed |
| Pages·정적 위키형 개인 사이트 | GitHub Pages 사례가 흔함 (GitLab Pages도 있음) |

개인이 둘 다 쓰는 경우: 오픈소스는 GitHub, 회사는 GitLab — **Git 조작은 동일**.

---

## 7. 보안 주의

| 주의 | 왜 |
|------|-----|
| CI Variable에 비밀 | 로그에 찍히지 않게 Masked, 스크립트 echo 금지 |
| Public Job 로그 | 토큰·URL 유출 |
| `git push --force` to main | Protected branch로 막는 편 |
| 셀프호스트 업데이트 | 보안 패치·러너 격리 |
| `.env` 커밋 | [[Git 사용법]]과 동일 |

---

## 8. 실전 체크

- [ ] [[Git 사용법]] 로컬 커밋·remote 
- [ ] 인스턴스(URL)·그룹·프로젝트 권한 
- [ ] MR로 병합 · Protected branch 
- [ ] `.gitlab-ci.yml`·Runner 상태 
- [ ] Variables에만 비밀 
- [ ] 외부 공개/오픈소스는 [[GitHub]]와 역할 분리했는지 

---

## 9. 정리

GitLab은 Git 원격에 **MR과 내장 CI/CD**를 붙인 플랫폼이고, 셀프호스트가 강점인 경우가 많다. 
손의 명령은 [[Git 사용법]], PR 문화 비교는 [[GitHub]]를 보면 된다.

---

## 면책

> **면책** 
> 에디션(Free/Premium/Ultimate)·UI·CI 문법은 버전마다 다르다. **공식 문서·회사 인스턴스 안내**가 우선. 
> Public 프로젝트·러너·변수에 비밀을 넣지 말 것. 
> 가입·유료 플랜 권유가 아니다.

---

## 관련

- [[생활위키 목차]]
- [[Git 사용법]]
- [[GitHub]]
- [[레드마인]]
- [[Docker 사용법]]
- [[쿠버네티스]]
- [[Playwright]]
- [[VS Code 사용법]]
- [[Cursor 사용법]]
