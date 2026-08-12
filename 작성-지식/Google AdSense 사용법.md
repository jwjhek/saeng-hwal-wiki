---
publish: true
draft: false
depth: article
aliases:
  - Google AdSense
---

# Google AdSense 사용법

> **분류:** 작성·지식 › 노트·지식 · [[생활위키 목차]]

**Google AdSense**는 웹사이트·블로그에 **Google 광고**를 붙여 수익을 나누는 프로그램이다. 
[[Quartz 사용법]]로 빌드한 **GitHub Pages** 정적 사이트에 연결할 때 필요한 **일반 절차**를 정리한다.

공식: [https://www.google.com/adsense](https://www.google.com/adsense)

확인일: 2026-08-11

---

## 1. 개요

| 항목 | 설명 |
|------|------|
| 무엇 | 방문자에게 맞춤 광고를 보여 주고, 클릭·노출에 따라 **수익**을 정산 |
| 대상 | 운영자가 소유한 **콘텐츠 사이트** (위키·블로그·정보 글 등) |
| 전제 | Google 계정, **사이트 소유 확인**, 콘텐츠·정책 검토 통과 |
| 정적 사이트 | Quartz 등 SSG + GitHub Pages **프로젝트 경로** 또는 **루트 도메인** |

AdSense는 **편집기가 아니다.** 글은 [[Obsidian 사용법]]·[[Cursor 사용법]]에서 쓰고, 광고 코드·`ads.txt`는 **빌드·배포 설정**에 넣는다.

---

## 2. GitHub Pages 주소 구조

GitHub Pages는 **두 종류**가 있다.

| 종류 | 저장소 이름 | 공개 URL |
|------|-------------|----------|
| **사용자 사이트** | `username.github.io` | `https://username.github.io/` |
| **프로젝트 사이트** | 임의 이름 (예: `my-wiki`) | `https://username.github.io/repo-name/` |

AdSense **사이트 추가** 화면은 **최상위 도메인**만 받는다.  
`/repo-name/`처럼 **경로가 붙은 URL**은 거부되는 경우가 많다.

위키만 **프로젝트 Pages**로 올려 두면 `https://username.github.io` 는 **404**가 나고, AdSense 등록이 막힐 수 있다.

### 흔한 구성 (프로젝트 경로 + 루트)

| 역할 | 저장소 예 | URL 예 |
|------|-----------|--------|
| **본문 사이트** | `my-wiki` | `https://username.github.io/my-wiki/` |
| **루트 도메인** | `username.github.io` (별도) | `https://username.github.io/` |

**해결:** `username.github.io` 이름의 저장소를 만들어 루트를 살린다. 루트 `index.html`은 본문으로 **안내·리다이렉트**만 한다.

```text
[AdSense 등록] username.github.io (루트)
 ↓ ads.txt · 검증 스크립트
[username.github.io 저장소] index.html → 본문으로 이동
 ↓
[my-wiki] Quartz 빌드 → /my-wiki/ 에 글·광고 스크립트
```

**대안:** 위키를 **사용자 사이트** 저장소(`username.github.io`)에 직접 배포하면 `baseUrl`을 `username.github.io`만 쓰고 루트 이중 구조가 필요 없다.  
**또 다른 대안:** **커스텀 도메인**(`example.com`)을 Pages에 연결해 AdSense에 그 도메인을 등록한다.

---

## 3. 가입·사이트 등록 순서

1. [AdSense](https://www.google.com/adsense)에서 Google 계정으로 **시작하기**
2. **사이트**에 등록할 **루트 도메인** 입력 (`https://`·끝 슬래시·하위 경로 없이. 예: `username.github.io` 또는 `example.com`)
3. **소유권 확인** — 아래 §4·§5
4. **동의 메시지(CMP)** — 유럽·영국·스위스 방문자용 쿠키 동의 (§7)
5. **검토 요청** — Google이 콘텐츠·정책 검토 (수일~수주)

승인 전에는 광고가 안 나오거나 제한될 수 있다. 메뉴·문구는 AdSense UI가 바뀔 수 있으니 **화면 안내**를 따른다.

---

## 4. ads.txt

광고 사기 방지용 **공인 판매자 목록**이다. AdSense가 `ads.txt`로 사이트와 **pub-ID**를 맞춘다.

**AdSense에 등록한 도메인 루트**에 있어야 한다.

```text
https://username.github.io/ads.txt
```

프로젝트 경로로 본문을 서비스할 때는 **같은 내용**을 하위 경로에도 둘 수 있다.

```text
https://username.github.io/repo-name/ads.txt
```

| 위치 | 넣는 곳 (예) |
|------|----------------|
| 루트 | `username.github.io` 저장소의 `ads.txt` |
| Quartz 빌드 | vault 루트 `ads.txt` 또는 CI에서 `public/ads.txt` 생성 |

형식 (한 줄):

```text
google.com, pub-XXXXXXXXXXXXXXXX, DIRECT, f08c47fec0942fa0
```

`pub-` 값은 AdSense **계정 → 설정**에서 확인한다. 사이트에 올리는 값은 **공개 정보**이지만, **민감 계정 정보**(비밀번호·결제)와 혼동하지 않는다. 루트·빌드·스크립트의 pub-ID가 **같은지** 맞춘다.

---

## 5. 사이트 소유권 확인 (애드센스 코드)

AdSense가 주는 **스크립트**를 사이트 `<head>` 안에 넣는다.

```html
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX"
     crossorigin="anonymous"></script>
```

메타 태그를 함께 쓰는 경우:

```html
<meta name="google-adsense-account" content="ca-pub-XXXXXXXXXXXXXXXX">
```

### 어디에 넣나

| 배포 형태      | 위치                                                              |
| ---------- | --------------------------------------------------------------- |
| 루트 정적 HTML | `index.html`의 `<head>`                                          |
| Quartz     | `quartz/components/Head.tsx` 등 **모든 공개 페이지** `<head>`를 만드는 컴포넌트 |

```text
push main → GitHub Actions → Pages 배포 후 AdSense에서 「코드를 삽입했습니다」→ 확인
```

배포 직후 캐시 때문에 실패할 수 있다. 1~2분 뒤 다시 시도한다.

---

## 6. GitHub Actions (Quartz 배포 예)

`.github/workflows/deploy.yml`에서 흔히 하는 일:

```text
quartz build -d .
 ↓
public/ads.txt 생성 (pub-ID 한 줄)
 ↓
GitHub Pages artifact → deploy
```

루트 `username.github.io` 저장소와 본문 저장소가 **다르면** 각각 push가 필요하다.

---

## 7. 동의 메시지 (CMP)

가입·설정 중 **「사이트에 사용할 동의 메시지 만들기」** 화면이 나온다.

| 내용 | 설명 |
|------|------|
| 목적 | 유럽경제지역(EEA)·영국·스위스 사용자에게 **쿠키·광고 동의** 받기 |
| Google CMP | AdSense가 **동의 배너**를 자동으로 붙임 |
| 선택 | **2버튼**(동의 + 옵션 관리)이 단순. 3버튼은 「동의하지 않음」이 더 분명 |
| 나중에 | 「나중에 알림」 가능하나, 승인 전에 막히는 경우가 있어 **제출**을 권장 |

한국 위주 사이트라도 AdSense를 쓰면 이 단계를 **건너뛰지 않는 편**이 안전하다.

---

## 8. 승인·운영 시 참고

| 항목 | 참고 |
|------|------|
| 콘텐츠 | **원문 정보** 위주. 복사·자동 생성만 있는 페이지는 거절되기 쉽다 |
| 개인정보 처리방침 | 수익화·쿠키 안내가 있는 **공개 페이지** URL 제출이 필요한 경우가 많다 |
| 트래픽 | 방문·체류가 너무 적으면 승인이 늦어지거나 어려울 수 있다 |
| 정책 | [AdSense 프로그램 정책](https://support.google.com/adsense/answer/48182) 위반 시 계정 제한 |
| 수익 | 승인 후에도 금액은 트래픽·주제·시즌에 따라 크게 다름 |

광고 **단위(블록)** 는 승인 이후 AdSense 대시보드에서 만든다. Quartz에 슬롯을 넣으려면 레이아웃 컴포넌트·SCSS 수정이 필요할 수 있다.

---

## 9. 자주 하는 문제

| 증상                       | 확인                                                                |
| ------------------------ | ----------------------------------------------------------------- |
| 사이트 URL 거부               | **루트 도메인**만 입력. `/repo-name/`은 사이트 URL 칸에 넣지 않음                   |
| `username.github.io` 404 | `username.github.io` **저장소**·Pages **main** 배포·`index.html`       |
| 소유권 확인 실패                | 등록 도메인(루트)의 `<head>`에 스크립트·**배포 완료** 후 재시도                        |
| ads.txt 오류               | 등록 도메인 루트의 `/ads.txt`가 열리는지, pub-ID 오타                            |
| 본문만 수정했는데 루트 검증 실패       | 검증 대상이 **루트**이면 루트 저장소도 수정·push                                   |
| 링크·OG 깨짐                 | `quartz.config.yaml`의 `baseUrl`이 실제 Pages URL과 일치 ([[Quartz 사용법]] §5) |
| 승인 대기만 길음                | 콘텐츠·정책·트래픽. **개인정보 처리방침**·소개 페이지 보강                               |

---

## 10. 정리

| 항목 | 내용 |
|------|------|
| AdSense 사이트 URL | **루트 도메인** (`username.github.io` 또는 커스텀 도메인) |
| 프로젝트 Pages | 본문은 `/repo-name/`, 등록은 **루트** — 이중 구조면 루트 저장소 별도 |
| ads.txt | 등록 도메인 루트 + (선택) 빌드 산출물 |
| 검증 코드 | 루트 HTML 또는 Quartz `Head` 컴포넌트 `<head>` |
| CMP | Google CMP **2버튼** 제출 권장 |

커스텀 도메인을 쓰면 AdSense·북마크·`baseUrl` 관리가 단순해진다.

---

## 면책

> **면책**  
> AdSense **승인·수익·정책**은 Google이 결정한다. 이 글은 **일반 절차 안내**이며 보장이 아니다.  
> `pub-` ID는 사이트에 공개되는 경우가 많다. 계정 비밀번호·결제 정보는 **저장소에 넣지 않는다**.  
> 메뉴·검증·CMP는 **버전마다 다르다.** [AdSense 고객센터](https://support.google.com/adsense)를 본다.

---

## 관련

- [[Quartz 사용법]]
- [[GitHub]]
- [[Git 사용법]]
- [[Obsidian 사용법]]
- [[생활위키 목차]]
