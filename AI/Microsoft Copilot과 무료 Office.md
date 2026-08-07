---
publish: true
draft: false
---

# Microsoft Copilot과 무료 Office 팁

> **분류:** AI · [[생활위키 목차]]

“코파일럿 쓰니까 워드·엑셀을 공짜로 쓰는 것 같다”는 체감은, 보통 **무료 Microsoft 계정 + 웹 Office + (선택) Copilot으로 초안**이 겹친 결과다.  
제품·요금·기능은 자주 바뀌니, 로그인 화면·[Microsoft 지원](https://support.microsoft.com)이 최종이다.

> **면책**  
> 가입·결제 권유가 아니다. 회사·학교 계정은 **IT 정책**이 우선이다.  
> “완전 공짜 데스크톱 Office 영구판”과는 다르다.

확인일: 2026-08-06

관련 AI 큰 그림: [[현존 AI 비교]] · 코딩용은 [[VS Code 추천 확장]]의 GitHub Copilot(별개 제품).

---

## 1. 이름을 먼저 구분

| 이름 | 대략 |
|------|------|
| **Microsoft Copilot (소비자·무료 챗)** | [copilot.microsoft.com](https://www.copilot.microsoft.com), Edge, Windows, 모바일 앱 — 질문·초안·이미지 등 |
| **Microsoft 365 웹/앱의 Office** | Word·Excel·PowerPoint를 **브라우저**에서 (계정만으로도 기본 사용 가능) |
| **Microsoft 365 Personal/Family 등 구독** | 데스크톱 앱 설치·OneDrive 용량·Copilot이 앱 안에 더 깊이 붙는 경우 |
| **Microsoft 365 Copilot (유료 추가 라이선스)** | 회사 데이터·고급 에이전트 등. “챗 공짜”와 다름 |
| **GitHub Copilot** | VS Code 코딩 AI — 이 글 범위 밖 |

“MS 코파일럿”만으로는 위가 한꺼번에 불린다. **어느 로그인·어느 URL**인지 보면 헷갈림이 줄어든다.

---

## 2. 공짜에 가까운 Office — 웹에서 쓰기

### 2.1 핵심 팁

1. Microsoft 계정(또는 학교·회사 계정)으로 로그인  
2. [https://www.microsoft365.com](https://www.microsoft365.com) 또는 [https://www.office.com](https://www.office.com)  
3. **Word / Excel / PowerPoint / OneNote** 웹 앱 실행  
4. 파일은 보통 **OneDrive**에 저장  

데스크톱 설치판(영구·정품 박스)을 해적판으로 구하라는 뜻이 **아니다**.  
공식 경로의 **웹 버전**은 개인 계정으로도 문서 작성·편집·공유가 된다.  
고급 매크로·일부 데스크톱 전용 기능·용량·동시 편집 한도는 구독·계정 종류에 따라 막힐 수 있다.

### 2.2 웹으로 충분한 경우

- 이력서·보고서·간단한 표·발표 초안  
- 폰·PC 가리지 않고 OneDrive만 있으면 이어서 작업  
- “설치는 싫은데 호환 확장자(docx/xlsx/pptx)는 필요”  

부족한 경우: 무거운 서식, VBA, 고급 데이터 모델, 오프라인 중심 작업 → 구독·데스크톱 검토.

### 2.3 Windows에 보이는 “Office”

윈도우 초기 앱·Microsoft 365 앱은 **로그인하면 웹·클라우드와 이어지는** 형태가 많다.  
“이미 깔려 있으니 평생 무료 정품”이 아니라, **계정·라이선스 상태**를 앱 계정 메뉴에서 확인한다. → [[윈도우 사용법]]

---

## 3. 무료 Copilot으로 Office를 “공짜처럼” 쓰는 흐름

### 3.1 초안은 Copilot, 파일은 Office 웹

```text
copilot.microsoft.com (또는 Edge Copilot)
        ↓  프롬프트로 글·표·개요 생성
복사 또는 다듬기
        ↓
microsoft365.com 에서 Word/Excel/PPT 새 문서
        ↓
OneDrive 저장 · 공유 링크
```

팁:

- “docx로 만들어줘”보다 **구조화된 마크다운·표**를 받은 뒤 웹 Word에 붙여넣기가 안전한 경우가 많다.  
- 숫자·인용·법률·의료는 **반드시 재확인**.  
- 회사 기밀은 소비자 Copilot에 넣지 않는다.

### 3.2 Microsoft 365 Copilot 앱 · Word/Excel/PPT Agent

최근에는 Copilot(또는 Microsoft 365 Copilot 앱) 안에서  
**Word / Excel / PowerPoint Agent(도구)** 로 “설명만 하면 파일 생성 → OneDrive 저장” 흐름이 있다.

| 포인트 | 내용 |
|--------|------|
| 어디서 | Copilot 챗의 Agents / Tools 메뉴 등 (UI 이름 변경 가능) |
| 결과물 | OneDrive의 docx·xlsx·pptx |
| 자격 | 공식 안내상 **Microsoft 365 Personal / Family / Premium** 등 적격 구독자 중심인 경우가 많음. **완전 무료 계정만으로 항상 되는 기능이 아닐 수 있음** |
| Copilot 추가 라이선스 | “에이전트로 파일 만들기”와 “회사 데이터 연동 풀 Copilot”은 별개 층 |

체감 팁: 앱·웹에 Agent가 보이면 써 보고, 안 보이면 **웹 Office + 무료 Copilot 초안**으로 같은 목적을 달성한다.

### 3.3 Edge + Copilot

Edge에서 웹페이지 요약·글 다듬기 → 결과를 Office 웹에 붙여넣기.  
PDF·긴 공지 URL을 열어 두고 “요약해 표로” 시킨 뒤 Excel 웹에 옮기는 식.

---

## 4. 구독·학생·회사에서 “더 공짜에 가까워지는” 경우

| 경로 | 메모 |
|------|------|
| **학교 메일** | 많은 학교가 Microsoft 365 교육용 제공 → 웹·데스크톱·OneDrive. 포털·학생지원 확인 |
| **회사 계정** | 회사가 라이선스·Copilot Chat 포함 여부를 정함. 개인 구독과 섞어 쓰지 말 것 |
| **M365 Personal/Family** | 데스크톱 앱 + (시기별) 앱 안 Copilot·AI 크레딧. “완전 무료”는 아님 |
| **프로모션** | 신규·카드·통신사 번들 — 기간 한정. 자동 갱신 체크 |

“친구가 공짜래” = 학교·회사·이벤트인 경우가 많다. 본인 계정 구독 상태를 Microsoft 계정·서비스 페이지에서 본다.

---

## 5. 무료 Copilot vs 유료 Microsoft 365 Copilot

| | 무료·소비자 Copilot | M365 안 Copilot Chat (적격 구독) | M365 Copilot 추가 라이선스 |
|--|---------------------|----------------------------------|----------------------------|
| 접근 | 웹·앱·Edge 등 | Word 등 옆 챗(계정·플랜별) | IT가 할당 |
| 강점 | 웹 검색·일상 초안 | 열린 문서 맥락에서 질문 | 조직 데이터·고급 에이전트 |
| Office 파일 | 초안→수동 붙여넣기 또는 Agent(조건) | 앱 안에서 생성·수정 비중↑ | 업무 통합 |

같은 “Copilot” 아이콘이라도 **로그인 계정(개인/회사)** 에 따라 메뉴가 달라진다.

---

## 6. 실전 팁 모음

1. **파일 저장 위치** — OneDrive `문서` 정리. 데스크톱에만 두면 기기 고장 시 증발.  
2. **버전 기록** — OneDrive 웹에서 이전 버전 복구 가능한지 알아 두기.  
3. **공유** — 링크 권한(보기/편집)·만료. 회사 파일은 개인 OneDrive로 빼지 않기.  
4. **한글** — 웹 Office도 한글 잘 되지만, 폰트·쪽 나눔은 데스크톱과 조금 다를 수 있음.  
5. **오프라인** — 웹은 망 필요. 비행기 모드 작업이면 구독 데스크톱·로컬 저장 검토.  
6. **갤럭시** — Microsoft 365 / Copilot 앱으로 폰에서 이어서 편집 ([[갤럭시 폰과 워치 사용법]]).  
7. **크롬에서도** — Office는 브라우저 가리지 않는 편. Edge 전용 기능만 Edge ([[크롬]]).  
8. **AI 한도** — 개인 구독의 AI 크레딧·일일 한도가 있으면 고용량 작업은 나눠서.  
9. **생성물 검증** — 표 합계·날짜·고유명사 재계산.  
10. **대안** — Google 문서, 한글(웹), 로컬 오픈소스 오피스 등. 이 위키는 MD면 [[Obsidian 사용법]]·[[VS Code 사용법]].

---

## 7. 자주 하는 오해

| 오해 | 보완 |
|------|------|
| Copilot = Office 정품 평생 무료 | 웹·구독·라이선스가 층층이 |
| 설치 안 해도 모든 데스크톱 기능 | 웹은 기능 일부(서브셋) |
| 회사 파일을 개인 Copilot에 넣어도 됨 | 보안·규정 위반 가능 |
| GitHub Copilot과 동일 | 코딩 vs 일반·Office |
| Agent가 안 보이면 고장 | 지역·언어·구독·롤아웃 차 |

---

## 8. 체크리스트

- [ ] Microsoft 계정으로 microsoft365.com 접속·Word 새 문서 확인  
- [ ] OneDrive 용량·중요 폴더  
- [ ] 무료 Copilot으로 초안 → 웹 Office 붙여넣기 한 번 연습  
- [ ] (해당 시) 학교·회사 포털 라이선스 확인  
- [ ] 구독 자동 갱신·결제 수단 점검  
- [ ] 기밀 데이터는 소비자 AI에 미입력  

---

## 관련

- [[생활위키 목차]]
- [[웹 드라이브 비교]]
- [[윈도우 사용법]]
- [[현존 AI 비교]]
- [[크롬]]
- [[갤럭시 폰과 워치 사용법]]
- [[VS Code 추천 확장]] — GitHub Copilot
- [[공개 규칙]]
