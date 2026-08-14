---
publish: true
draft: false
depth: article
aliases:
  - 올라마
  - ollama.com
---

# Ollama

> **분류:** AI · [[생활위키 목차]]

**Ollama**는 오픈 웨이트 LLM을 **이 컴퓨터(또는 공식 클라우드)** 에서 돌리는 런타임이다. ChatGPT 같은 **챗 구독 제품이 아니고**, Llama·Gemma·Qwen 같은 **모델 파일도 아니다.** 모델을 받아 대화하고, 로컬 [[API]]로 앱에 붙이는 쪽에 가깝다.

공식: [https://ollama.com](https://ollama.com)  
문서: [https://docs.ollama.com](https://docs.ollama.com)  
모델 목록: [https://ollama.com/search](https://ollama.com/search)  
코드(MIT): [https://github.com/ollama/ollama](https://github.com/ollama/ollama)

확인일: 2026-08-14  
모델명·명령·클라우드 요금은 **사이트·문서**가 우선이다.

관련: [[현존 AI 비교]] · [[OpenAI Platform]] · [[API]] · [[VS Code 추천 확장]]

---

## 1. 개요

| 항목 | 설명 |
|------|------|
| **무엇** | 로컬(기본) · 공식 클라우드로 **오픈 모델을 실행**하는 도구. CLI + REST |
| **OS** | Windows · macOS · Linux. Docker 이미지도 있음 → [[Docker 사용법]] |
| **엔진** | 뒤에 llama.cpp · (Apple 등) MLX 안내. 사용자는 `ollama run`만 보는 경우가 많음 |
| **무엇이 아님** | ChatGPT 계정, [[OpenAI Platform]] 키, [[Cursor 사용법]] 구독, 모델 가중치 그 자체 |

```text
ollama.com 에서 설치
 ↓
ollama  (메뉴) 또는  ollama run 모델이름
 ↓
터미널 채팅  /  localhost API  /  에디터·에이전트 연결
```

[[현존 AI 비교]]의 오픈 웨이트를 **직접 돌릴 때** 자주 고른다. 클라우드 챗보다 품질·속도는 기기(RAM·VRAM)에 달렸다.

같은 축: LM Studio, 직접 llama.cpp. 이 글이 우열을 정하지 않는다.

---

## 2. 로컬과 클라우드

문서 기준 **두 갈래**가 있다. “Ollama = 무조건 오프라인·비학습”이 **아니다.**

| | **로컬** | **Ollama 클라우드** |
|--|----------|---------------------|
| 실행 | 이 PC. 기본 API `http://localhost:11434` | 공식 호스트. 문서 예: `https://ollama.com/api` |
| 모델 | 디스크에 받음 (`ollama pull`) | 큰 모델을 **다운로드 없이** 쓰는 태그 안내 (`이름:cloud` 등) |
| 데이터 | 요청이 이 기기에 머무는 쪽에 가깝다 | 사업자 약관·지역(미국·유럽·싱가포르 등 안내) |
| 통신 | 꺼 두면 오프라인 | 네트워크 필요 |

민감 코드를 **밖으로 안 보내려면** 로컬 모델만 쓰고, `:cloud`·ollama.com API를 쓰지 않는다. 회사 정책이 있으면 그걸 따른다.

---

## 3. 설치 · 자주 쓰는 명령

[https://ollama.com](https://ollama.com) 에서 OS별 설치. Windows는 설치 후 트레이에 상주하는 안내가 흔하다. 터미널:

```text
ollama                 대화형 메뉴 (모델 실행·도구 연결)
ollama run 모델이름    받아서 채팅. 끝은 /bye
ollama pull 모델이름   받기만
ollama list            받은 목록
ollama rm 모델이름     삭제 (용량이 큼)
```

모델 이름은 라이브러리가 수시로 바뀐다. 퀵스타트 예(`gemma4` 등)를 이 글에 고정하지 않는다. [검색](https://ollama.com/search)에서 **파라미터 수·용량·라이선스**를 본다.

작은 모델은 CPU로도 돌아가지만 느리다. 큰 모델은 **VRAM·RAM이 부족하면** 스왑·실패. 숫자 한도는 기기·양자화마다 다르다.

---

## 4. API · 앱에 붙이기

Ollama가 떠 있으면 로컬 REST가 열린다. 기본:

`http://localhost:11434/api`

문서 예(모델 이름은 그때 목록):

```text
curl http://localhost:11434/api/generate -d "{\"model\": \"모델이름\", \"prompt\": \"...\"}"
```

OpenAI 모양 `/v1/chat/completions` 호환 안내도 있다. 앱·라이브러리가 **OpenAI 클라이언트 + base URL만 바꿈**으로 붙는 경우가 많다. 키·스키마 차이는 [[OpenAI Platform]] 문서와 **완전히 같지 않음**.

공식 라이브러리: Python · JavaScript (문서). 문법·venv는 [[파이썬 개발 툴]] · [[Python 학습과 패키지]].

에디터: [[VS Code 추천 확장]]의 **Continue**가 로컬 Ollama를 고르는 예가 흔함. Cursor는 **제품이 로컬 엔드포인트를 받는지** 그 문서를 본다.

에이전트 도구([[MCP]]·Claude Code 등)를 Ollama 메뉴에서 띄운다는 퀵스타트 안내가 있다. 모델이 약하면 도구 호출이 흔들린다.

---

## 5. 모델 · Modelfile · 라이선스

| 항목 | 메모 |
|------|------|
| **라이브러리** | 채팅·코딩·비전·임베딩 등이 섞여 있다. 태그가 용량·양자화를 가리키는 경우가 많음 |
| **Modelfile** | `FROM`에 기본 모델을 두고 시스템 프롬프트·파라미터를 얹는 레시피. 문서는 `/modelfile` |
| **Ollama 코드** | MIT |
| **모델 가중치** | Llama 커뮤니티 라이선스 등 **모델마다** 다름. 상업·재배포는 그 문구 |

“오픈”이 **아무 용도나 무료**는 아니다.

---

## 6. Docker · 네트워크

공식 이미지 `ollama/ollama` → [[Docker 사용법]]. GPU 통과는 드라이버·런타임이 맞아야 한다.

기본은 **이 PC의 localhost**. 포트를 다른 기기에 열어 두면, 인증이 약하다는 이야기가 많다. 집 공유기·회사망에 그냥 노출하지 않는다. 이 글이 원격 공개 절차를 적지 않는다.

---

## 7. ChatGPT · Cursor와

구매 권유가 아니다.

| | Ollama | [[OpenAI Platform]] / 챗GPT | [[Cursor 사용법]] |
|--|--------|------------------------------|-------------------|
| 자리 | 모델 **실행기** | 호스티드 모델 API·구독 UI | 코드 에이전트 IDE |
| 값 | 전기·디스크·(클라우드면) 그 요금 | 토큰·구독 | 에디터 구독 |
| 품질 | 고른 모델·GPU | 프론티어가 기본 | 연결한 모델 |
| 비밀 | 로컬이면 기기 안. 클라우드는 약관 | 제공자 정책 | 제품 정책 |

로컬 7B~30B급은 일상 초안·실험에 쓰고, 어려운 추론·최신 지식은 검색·호스티드 모델과 나누는 집이 많다 → [[현존 AI 비교]] §6.

---

## 8. 정리

| 항목 | 한 줄 |
|------|--------|
| 정의 | 오픈 모델을 로컬(또는 공식 클라우드)에서 돌리는 런타임 |
| 설치 | [https://ollama.com](https://ollama.com) |
| 대화 | `ollama run 모델이름` |
| API | 로컬 `localhost:11434`. 개념은 [[API]] |
| 에디터 | Continue 등 → [[VS Code 추천 확장]] |
| 도구 | [[MCP]]는 별 규격. 모델 실행과 겹치지 않음 |

---

## 면책

> **면책**
> - **설치·특정 모델·클라우드 요금제 권유가 아니다.**
> - 출력은 환각이 있다. 의료·법률·보안 설정은 **전문가·공식 문서**.
> - `:cloud`·ollama.com API는 **로컬 비공개가 아니다.**
> - 모델 라이선스·GPU 드라이버·열린 포트는 **이용자 책임**. 이 글이 침투·무단 공개를 안내하지 않는다.

---

## 관련

- [[생활위키 목차]]
- [[현존 AI 비교]]
- [[OpenAI Platform]]
- [[API]]
- [[VS Code 추천 확장]]
- [[Cursor 사용법]]
- [[Docker 사용법]]
