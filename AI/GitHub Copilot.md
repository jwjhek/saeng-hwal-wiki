---
publish: true
draft: false
---

# GitHub Copilot

> **분류:** AI · [[생활위키 목차]]

**GitHub Copilot**은 GitHub이 제공하는 **코딩용 AI**다.  
에디터 안에서 코드를 **자동완성·채팅·설명·수정 제안**한다.  
일반 질문·Office용 **Microsoft Copilot**과는 이름이 비슷해도 **제품·구독이 다르다** → [[Microsoft Copilot]].

확인일: 2026-08-10  
요금·모델·단축키는 바뀐다. [GitHub Copilot](https://github.com/features/copilot) · VS Code 확장 문서가 우선.

큰 지도: [[현존 AI 비교]] · 확장 설치 목록: [[VS Code 추천 확장]] · 에디터 기본: [[VS Code 사용법]]

---

## 1. 개요

| 항목 | 내용 |
|------|------|
| 무엇 | IDE에 붙는 AI 코딩 어시스턴트 |
| 주 무대 | **VS Code**, Visual Studio, JetBrains 등 (지원 IDE는 시점별) |
| 계정 | **GitHub 계정** + Copilot 구독(개인·Pro·학생·조직 등) |
| 하는 일 | 회색 인라인 제안, 채팅, 선택 구간 설명·리팩터, (지원 시) PR·에이전트성 작업 |
| 아닌 것 | Word/엑셀 비서([[Microsoft Copilot]]), Cursor 전체 제품([[Cursor 사용법]]) |

```text
GitHub 로그인 · Copilot 구독 확인
        ↓
VS Code에 Copilot 확장 설치·권한
        ↓
코드 치다 보면 Tab으로 제안 수락
        ↓
채팅으로 “이 함수 설명해줘 / 테스트 짜줘”
        ↓
제안은 항상 읽고 · 빌드·테스트로 검증
```

---

## 2. Microsoft Copilot과 분류

| | [[GitHub Copilot]] | [[Microsoft Copilot]] |
|--|--------------------|------------------------|
| 브랜드 | GitHub Copilot | Microsoft Copilot |
| 목적 | **소프트웨어 작성** | 일반 비서·Office·Windows |
| 로그인 | GitHub | Microsoft (개인/회사) |
| 대표 UI | VS Code 인라인·Chat | copilot.microsoft.com, Edge, M365 |
| 이 위키에서 | 이 글 · [[VS Code 추천 확장]] §10 | [[Microsoft Copilot]] · [[Microsoft Copilot과 무료 Office]] |

둘 다 Microsoft 계열 이야기에 묶여 나오지만, **구독을 따로** 산다.  
Windows에 MS Copilot이 있어도 GitHub Copilot 완성이 자동으로 생기지는 않는다.

---

## 3. 구독·계정

| 종류 | 메모 |
|------|------|
| 개인 (Free/Pro 등) | 요금·요청 한도는 [features/copilot](https://github.com/features/copilot) 확인 |
| 학생·교사 | 교육 인증 시 혜택이 있는 경우가 많음 (자격·기간 확인) |
| 조직·Business/Enterprise | 회사가 좌석·허용 저장소·정책 제어 |

확인 순서:

1. github.com 로그인  
2. Settings → Copilot (메뉴 이름은 시점별)  
3. 활성 구독·정책 확인  
4. VS Code에서 같은 GitHub로 로그인  

회사 코드는 **조직이 Copilot을 허용한 저장소·정책**인지 먼저 본다.

---

## 4. VS Code에서 쓰기

### 4.1 설치

| 확장 | ID (대략) | 역할 |
|------|-----------|------|
| GitHub Copilot | `GitHub.copilot` | 인라인 완성 |
| GitHub Copilot Chat | `GitHub.copilot-chat` | 사이드바·인라인 채팅 (묶이거나 함께 설치되는 경우 많음) |

확장 마켓플레이스에서 설치 후 GitHub 로그인.  
목록·다른 AI 확장: [[VS Code 추천 확장]].

### 4.2 자주 쓰는 조작

| 동작 | 하는 일 |
|------|---------|
| 타이핑 중 회색 제안 | 다음 줄·블록 예측 |
| `Tab` | 제안 수락 (키는 설정에 따라) |
| 제안 거절 | `Esc` 등 |
| 채팅 열기 | 사이드바 Copilot / 명령 팔레트 `Chat` |
| 인라인 채팅 | 선택 후 채팅·`Ctrl+I` 계열(환경별) |

정확한 단축키: `Ctrl+K` `Ctrl+S`에서 “Copilot” 검색.

### 4.3 채팅으로 잘 되는 요청

- “이 함수가 하는 일 설명해줘”  
- “이 버그 재현 테스트 코드를 짜줘”  
- “이 파일을 TypeScript로 바꿔줘”  
- “PR 설명 초안”  

파일·선택 범위를 명시하면 품질이 올라간다. Cursor의 `@` 멘션과 비슷한 습관.

---

## 5. Cursor·Continue와 고를 때

| | GitHub Copilot | [[Cursor 사용법\|Cursor]] | Continue ([[VS Code 추천 확장]]) |
|--|----------------|---------------------------|----------------------------------|
| 형태 | VS Code **확장** | VS Code 포크 **에디터** | VS Code 확장 |
| 모델 | GitHub이 제공하는 쪽 | Cursor 구독·모델 선택 | API·로컬 모델을 사용자가 연결 |
| 에이전트 | 채팅·(시점별) 에이전트 기능 | Agent가 제품 핵심 | 설정에 따라 |
| 팀 | GitHub·조직 정책과 맞추기 쉬움 | 개인·팀 Cursor | 키·비용 직접 관리 |

- 이미 **Cursor만** 쓰면 Copilot 확장은 보통 겹친다 → 하나만.  
- “VS Code 유지 + GitHub 결제” → Copilot.  
- “모델·로컬을 직접” → Continue.

---

## 6. 잘 쓰는 습관

1. **제안은 읽고 수락** — 컴파일·린트·테스트를 통과하는지 확인  
2. **비밀을 프롬프트에 넣지 않기** — API 키·비밀번호·개인정보  
3. **라이선스·복제** — 공개 코드와 비슷한 조각이 나올 수 있음. 회사 정책·오픈소스 라이선스 확인  
4. **큰 리팩터는 단계로** — 한 번에 전 저장소보다 파일·함수 단위  
5. **리뷰는 사람** — Copilot은 리뷰어를 대체하지 않음  

---

## 7. GitHub.com 쪽

조직·저장소 설정에서 Copilot 관련 옵션(코딩·PR 요약 등)이 생길 수 있다.  
원격·PR 기본은 [[GitHub]]. Actions·Pages와는 별 구독이다.

---

## 8. 체크리스트

- [ ] GitHub에 Copilot 구독이 활성화돼 있는가  
- [ ] VS Code에 확장 설치·같은 계정 로그인  
- [ ] 인라인 제안이 보이는지 / 채팅이 열리는지  
- [ ] Cursor와 **동시 사용**하지 않는지 (원하면 하나만)  
- [ ] 회사 저장소 정책·비밀 정보를 지켰는지  
- [ ] MS Office용 AI가 필요하면 [[Microsoft Copilot]]을 보는지  

---

## 면책

> **면책**  
> 구독·기능·모델·정책은 바뀐다. 가입·구매 권유가 아니다.  
> 생성 코드는 버그·보안·라이선스 이슈가 있을 수 있다. 병합·배포 전 검증은 사용자 책임이다.

---

## 관련

- [[생활위키 목차]]
- [[Microsoft Copilot]]
- [[현존 AI 비교]]
- [[VS Code 사용법]]
- [[VS Code 추천 확장]]
- [[Cursor 사용법]]
- [[바이브 코딩]]
- [[GitHub]]
- [[Git 사용법]]
