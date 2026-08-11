---
publish: true
draft: false
---

# Microsoft Copilot

> **분류:** AI · [[생활위키 목차]]

**Microsoft Copilot**은 마이크로소프트의 대화형·업무용 AI 브랜드다.  
코딩 IDE용 **GitHub Copilot**과는 **제품·구독·쓰는 곳이 다르다** → [[GitHub Copilot]].

확인일: 2026-08-10  
요금·메뉴·모델명은 자주 바뀐다. [copilot.microsoft.com](https://www.copilot.microsoft.com) · [Microsoft 지원](https://support.microsoft.com) · 로그인 계정이 최종이다.

큰 지도: [[현존 AI 비교]] · 웹 Office와 초안 팁: [[Microsoft Copilot과 무료 Office]]

---

## 1. 개요 — “코파일럿”이 여러 개다

| 이름 | 어디에 | 무엇을 |
|------|--------|--------|
| **Microsoft Copilot** (소비자) | 웹, Edge, Windows, 모바일 앱 | 질문·초안·요약·이미지 등 일반 비서 |
| **Microsoft 365 안 Copilot** | Word·Excel·Outlook 등 (구독·계정에 따라) | 문서·메일·시트 **안에서** 초안·수식·요약 |
| **Microsoft 365 Copilot** (추가 라이선스) | 회사·유료 좌석 | 조직 데이터·고급 에이전트 등. 무료 챗과 **다른 층** |
| **GitHub Copilot** | VS Code·JetBrains 등 | **코드** 완성·채팅 → [[GitHub Copilot]] |

같은 아이콘·이름이라도 **개인 Microsoft 계정 vs 회사 계정**, **무료 vs M365 구독 vs 추가 라이선스**에 따라 메뉴가 갈린다.

```text
일상 질문·초안 ────── 소비자 Microsoft Copilot (웹/앱)
Office 파일 작업 ──── 웹/데스크톱 Office + (있으면) 앱 안 Copilot
회사 데이터·규정 ──── 회사 배포 M365 Copilot (IT 정책)
코드 ─────────────── GitHub Copilot / Cursor 등 (별도)
```

---

## 2. 소비자 Microsoft Copilot

### 2.1 들어가기

| 경로 | 메모 |
|------|------|
| 웹 | [https://www.copilot.microsoft.com](https://www.copilot.microsoft.com) |
| Edge | 사이드바·주소창 Copilot (버전·지역에 따라) |
| Windows | 작업 표시줄·Win+C 등 (OS·빌드에 따라) |
| 모바일 | Microsoft Copilot / Microsoft 365 앱 |

Microsoft 계정으로 로그인하면 기록이 묶이고, 기능·한도가 달라질 수 있다.

### 2.2 잘 맞는 일

- 글·메일·발표 개요 **초안**
- 긴 글 **요약·번역·쉬운 말**로 바꾸기
- 아이디어·비교표·체크리스트 잡기
- (지원 시) 이미지 생성·설명
- Edge에서 **지금 보는 페이지**를 물어보기

### 2.3 조심할 일

- 사실·숫자·법률·의료·금융은 **재확인**
- 회사 기밀·개인정보를 소비자 Copilot에 넣지 않기
- “docx 정품을 공짜로 준다”가 아니라, 보통은 **초안 + 웹 Office** 조합 → [[Microsoft Copilot과 무료 Office]]

---

## 3. Office·Microsoft 365와의 관계

| 층 | 내용 |
|----|------|
| 계정만 | [microsoft365.com](https://www.microsoft365.com)에서 **웹** Word·Excel·PPT 사용 가능 (한도·기능은 계정별) |
| M365 Personal/Family 등 | 데스크톱 앱·OneDrive 용량·(시기별) 앱 안 AI |
| M365 Copilot 추가 | 기업용 고급. IT·구매 부서가 좌석을 줌 |

실무 팁: **초안은 Copilot 웹/앱 → 붙여넣기는 Office 웹**이 안전한 경우가 많다.  
파일은 대개 **OneDrive** → [[웹 드라이브 비교]].

상세 흐름·오해 정리: [[Microsoft Copilot과 무료 Office]].

---

## 4. Windows·Edge에서

| 환경 | 쓰는 법 |
|------|---------|
| **Edge** | 페이지 요약, 선택 텍스트 질문, 사이드바 채팅 |
| **Windows** | 시스템 Copilot 진입점(있으면). [[윈도우 사용법]]과 함께 계정·개인정보 설정 확인 |
| **그림판 등** | 버전·지역에 따라 Image Creator 등 → [[그림판 사용법]] |

OS에 붙어 있어도 **라이선스·지역·업데이트**에 따라 안 보일 수 있다.

---

## 5. GitHub Copilot과 비교

| | Microsoft Copilot | [[GitHub Copilot]] |
|--|-------------------|-------------------|
| 회사 축 | Microsoft | GitHub (Microsoft 계열이나 **제품 분리**) |
| 주 무대 | 웹·Office·Windows·일반 질문 | VS Code·IDE·저장소 코드 |
| 결과물 | 글·표·요약·이미지 등 | 코드 제안·채팅·PR 보조 |
| 구독 | Microsoft 계정 / M365 / 추가 라이선스 | GitHub Copilot 구독(개인·학생·조직) |
| 이 위키 | 이 글 · [[Microsoft Copilot과 무료 Office]] | [[GitHub Copilot]] · [[VS Code 추천 확장]] |

“코파일럿 켰는데 코드 완성이 없다” → 대개 **MS Copilot만** 켠 상태다. 코딩은 [[GitHub Copilot]] 또는 [[Cursor 사용법]].

---

## 6. 다른 AI와 고를 때

| 목적 | 후보 |
|------|------|
| Office·Windows·Edge와 한몸 | Microsoft Copilot |
| 만능 챗·플러그인 생태계 | ChatGPT 등 → [[현존 AI 비교]] |
| 구글 문서·Gmail | Gemini |
| 에디터에서 저장소 수정 | Cursor · GitHub Copilot |

---

## 7. 체크리스트

- [ ] 지금 쓰는 것이 **소비자 / M365 앱 안 / 회사 추가 라이선스** 중 무엇인지  
- [ ] 개인 계정과 회사 계정을 섞어 쓰지 않는지  
- [ ] 기밀·주민번호·카드 정보를 넣지 않는지  
- [ ] 코딩이 목표면 [[GitHub Copilot]]을 보는지  
- [ ] Office 파일은 [[Microsoft Copilot과 무료 Office]] 흐름을 아는지  

---

## 면책

> **면책**  
> 제품·요금·기능·정책은 바뀐다. 가입·구매 권유가 아니다.  
> 생성 내용은 오류가 있을 수 있다. 업무·학습의 최종 책임은 사용자에게 있다.

---

## 관련

- [[생활위키 목차]]
- [[GitHub Copilot]]
- [[Microsoft Copilot과 무료 Office]]
- [[현존 AI 비교]]
- [[웹 드라이브 비교]]
- [[윈도우 사용법]]
- [[크롬]] · Edge는 Windows·MS 계정과 함께 쓰는 경우가 많음
- [[Cursor 사용법]] — 코딩 에디터(별개)
