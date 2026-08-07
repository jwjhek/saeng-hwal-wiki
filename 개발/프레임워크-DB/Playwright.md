---
publish: true
draft: false
---

# Playwright

> **분류:** 개발 › 프레임워크·DB · [[생활위키 목차]]

**Playwright**는 브라우저를 **자동으로 조작**해 E2E(종단) 테스트·스크래핑·UI 검증에 쓰는 도구다.  
Microsoft가 주도하는 오픈소스이며, Chromium·Firefox·WebKit을 **하나의 API**로 다룬다.

공식: [https://playwright.dev](https://playwright.dev)

> **면책**  
> 사이트 이용약관·robots·개인정보·저작권을 위반하는 자동 수집·공격에 쓰지 않는다.  
> 이 글은 학습용이며, CI·버전별 CLI는 공식 문서가 우선이다.

확인일: 2026-08-07

관련 언어: [[Python 학습과 패키지]] · [[Java 언어 학습]] (Java 바인딩) · JS/TS는 Node 생태계

---

## 1. 한눈에

| 항목 | 내용 |
|------|------|
| 무엇 | 브라우저 자동화 + 테스트 러너 |
| 지원 브라우저 | Chromium, Firefox, WebKit (Safari 엔진 계열) |
| 언어 | **TypeScript/JavaScript**가 주류. Python, Java, .NET 바인딩 |
| Selenium과 | 대기·선택자·추적(trace)·코드젠 등이 **현대 E2E**에 맞춰져 있다는 평가가 많음 |
| Cypress와 | 멀티 브라우저·멀티 탭/출처 시나리오에서 Playwright를 고르는 팀이 있음 |

로컬에서 “클릭·입력·로그인 후 화면 확인”을 **반복 가능한 스크립트**로 남길 때 쓴다.

---

## 2. 왜 쓰나

| 목적 | 예 |
|------|-----|
| E2E 테스트 | 회원가입 → 로그인 → 결제 버튼까지 회귀 |
| 스모크 | 배포 후 주요 URL·로그인 동작 |
| 개발 보조 | UI 동작 재현, 버그 리포트용 녹화 |
| 제한적 자동화 | 사내 도구나 **허용된** 관리 화면 반복 작업 |

웹앱이 [[Spring과 Spring Boot 학습]]·프론트 조합이든, 정적 사이트든 **브라우저로 보이는 것**이 대상이다.

---

## 3. 핵심 개념

```text
브라우저 (Browser)
    └── 컨텍스트 (BrowserContext)  ← 쿠키·스토리지가 격리된 프로필 감각
            └── 페이지 (Page)      ← 탭 하나
                    └── 로케이터 (Locator) ← 버튼·입력창 찾는 손
```

| 용어 | 감각 |
|------|------|
| **Browser** | Chromium 등 프로세스 |
| **Context** | 독립 세션(쿠키 분리). 테스트마다 새로 만들면 격리가 쉬움 |
| **Page** | 탭 |
| **Locator** | `getByRole`, `getByText`, `getByTestId` 등 — **역할·접근성** 우선이 권장 |
| **auto-wait** | 클릭 전 보일 때까지 알아서 기다리는 편 |
| **Trace / Video** | 실패 시 재생·디버깅 |

선택자는 CSS만으로도 가능하지만, `getByRole('button', { name: '저장' })`처럼 쓰면 UI 문구·접근성과 맞추기 좋다.

---

## 4. 설치·첫 실행 (JS/TS 감각)

Node가 있는 환경에서 (버전은 공식 권장 확인):

```bash
npm init playwright@latest
# 또는 기존 프로젝트
npm i -D @playwright/test
npx playwright install
```

`npx playwright install`이 **브라우저 바이너리**를 받는다. CI에서도 이 단계가 필요하다.

최소 테스트 예 (개념):

```ts
import { test, expect } from '@playwright/test'

test('홈에 제목이 있다', async ({ page }) => {
  await page.goto('https://example.com')
  await expect(page).toHaveTitle(/Example/)
})
```

실행:

```bash
npx playwright test
npx playwright test --ui          # UI 모드
npx playwright codegen https://example.com   # 조작 녹화 → 코드
```

**codegen**: 직접 클릭해 보며 코드를 뽑을 때 유용. 그대로 커밋하기보다 **로케이터를 다듬는** 편이 유지보수에 낫다.

### Python 쪽

```bash
pip install playwright
playwright install
```

API 모양이 비슷하고, pytest 플러그인(`pytest-playwright`)을 쓰는 경우가 많다 → [[Python 학습과 패키지]].

---

## 5. 실무에서 자주 쓰는 것

| 기능 | 용도 |
|------|------|
| `expect(locator).toBeVisible()` 등 | 화면 상태 **검증** |
| 스크린샷·비디오 | 실패 아티팩트 |
| Trace viewer | `npx playwright show-trace` — 타임라인으로 디버깅 |
| 프로젝트·브라우저 매트릭스 | `playwright.config`에서 chromium/firefox/webkit |
| 스토리지 스테이트 | 로그인 한 번 → 상태 저장 → 다른 테스트에서 재사용 |
| APIRequest | UI 없이 API만 치거나 UI와 섞기 |
| 인증·2FA | 테스트 전용 계정·스테이지 환경. 실 OTP 우회는 정책 내로 |

CI: [[GitHub]] Actions 등에서 `npx playwright install --with-deps` 패턴이 공식 문서에 있다. [[GitLab]] CI도 동일하게 Job 스크립트에 넣으면 된다.
[[Docker 사용법]] 이미지로 브라우저 의존성을 고정하기도 한다.

---

## 6. 로케이터·안정성 팁

1. **테스트 전용 `data-testid`** 를 프론트와 약속하면 문구 변경에 강함  
2. `text=정확한문구`만 의존하면 i18n·카피에 깨지기 쉬움  
3. 네트워크 대기: `page.waitForURL`, response 대기 — `waitForTimeout` 남용 금지  
4. 플레이크(가끔 실패): 병렬·애니메이션·AB 테스트 원인 분리  
5. 시크릿·실서버 비밀번호를 저장소에 넣지 않음 → `private/`·CI 시크릿  

---

## 7. Selenium·Cypress와 고를 때 (감각)

| | Playwright | Selenium | Cypress |
|--|------------|----------|---------|
| 대기 | auto-wait가 강한 편 | 명시적 대기 코드가 많아지기 쉬움 | 대기 편함, 구조가 다름 |
| 브라우저 | Chromium/FF/WebKit | 드라이버 생태계 넓음 | Chromium 계열 중심 역사 |
| 언어 | JS/TS·Python·Java·.NET | 다언어 | 주로 JS |
| 멀티 탭·멀티 출처 | 상대적으로 다루기 쉽다는 평 | 가능 | 제약이 있던 시기·패턴 차이 |

팀에 이미 Selenium 자산이 많으면 이전이 비용이다. **신규 E2E**면 Playwright를 후보에 두는 팀이 늘었다.

---

## 8. 하지 말 것

- 약관 금지 사이트 대량 스크래핑·우회 로그인  
- 실사용자 계정으로 파괴적 테스트  
- 프로덕션에서 부하·결제 실결제 남발  
- 실패를 `force: true` 클릭으로만 덮기  

---

## 9. 실전 체크

- [ ] `playwright install`로 브라우저 설치  
- [ ] codegen으로 초안 → 로케이터 정리  
- [ ] `getByRole` / test id 우선  
- [ ] 실패 시 trace·스크린샷 켜 두기  
- [ ] CI에 브라우저·의존성 포함  
- [ ] 스테이징 URL·테스트 계정만 사용  

---

## 10. 정리

Playwright는 **멀티 브라우저 E2E·자동화**를 한 API로 다루는 도구다.  
설치 → codegen/테스트 작성 → locator·trace로 안정화 → CI 순이 기본 흐름이다.

---

## 관련

- [[생활위키 목차]]
- [[Python 학습과 패키지]]
- [[Java 언어 학습]]
- [[Spring과 Spring Boot 학습]] — 웹앱 E2E 대상 예
- [[Docker 사용법]]
- [[쿠버네티스]]
- [[GitHub]]
- [[GitLab]]
- [[Cursor 사용법]] — 테스트 코드 작성 보조
- [[VS Code 사용법]]
