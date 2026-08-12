---
publish: true
draft: false
---

# OpenAI Platform

> **분류:** AI · [[생활위키 목차]]

[OpenAI Platform](https://platform.openai.com/)은 **개발자용 OpenAI API·대시보드**다. 
브라우저에서 채팅하는 [ChatGPT](https://chatgpt.com) 소비자 앱과 **계정·요금·용도가 다르다**.

| | Platform (API) | ChatGPT 앱 |
|--|----------------|------------|
| 주소 | [platform.openai.com](https://platform.openai.com/) | chatgpt.com |
| 쓰는 사람 | 앱·서버에 모델 붙이는 개발자 | 일반 사용자 |
| 과금 | 사용량(토큰·도구 호출 등) | Plus/Pro 등 구독 |
| 핵심 | API 키, 프로젝트, Playground, 사용량 | 채팅 UI, GPTs 등 |

문서 허브(개발자 문서): [https://developers.openai.com/api/docs](https://developers.openai.com/api/docs) 
모델·엔드포인트는 자주 바뀌므로 **공식 문서·대시보드가 최신**이다.

확인일: 2026-08-06 
관련: [[현존 AI 비교]], [[Python 학습과 패키지]], [[Cursor 사용법]]

---

## 1. Platform에서 할 수 있는 일

1. **API 키 발급·관리** — 서버에서 모델 호출 
2. **조직(Organization) / 프로젝트** — 팀·환경별 키·한도·감사 
3. **Playground** — 프롬프트·모델을 UI로 시험 후 코드로 가져가기 
4. **사용량·빌링** — 크레딧, 한도, 인보이스 
5. **모델·기능 탐색** — 텍스트, 이미지, 음성, 임베딩, 도구·에이전트 

API로 만드는 것 예:

- 사내 챗봇, 문서 요약, 분류·추출(Structured Outputs) 
- 코딩 도우미, RAG(파일 검색·자체 벡터 DB) 
- 음성(Realtime), 이미지 생성·분석 
- Agents SDK로 도구 호출·멀티스텝 워크플로 

ChatGPT 구독만으로는 **Platform API 호출 권한이 자동으로 생기지 않는다**. API는 Platform에서 결제·키를 별도로 연다.

---

## 2. 시작 흐름

1. [platform.openai.com](https://platform.openai.com/) 로그인 (OpenAI 계정) 
2. **Billing**에 결제 수단·사용 한도 설정 (미결제면 키가 막히거나 한도가 0인 경우 많음) 
3. **API keys**에서 키 생성 → **한 번만** 전체 문자열 복사 
4. 환경변수로 저장 (코드·git·프론트에 넣지 말 것)

```bash
# Windows PowerShell 예 (현재 세션)
$env:OPENAI_API_KEY = "sk-..."
```

5. 공식 문서 [Quickstart](https://developers.openai.com/api/docs/quickstart) 따라 첫 요청 
6. Playground에서 프롬프트를 다듬은 뒤 SDK로 이식 

### cURL (문서 예시 형태)

```bash
curl https://api.openai.com/v1/responses \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer $OPENAI_API_KEY" \
 -d "{\"model\": \"gpt-5.6\", \"input\": \"한 줄로 자기소개 해 줘\"}"
```

모델 ID·엔드포인트 경로는 **문서의 현재 권장 API**를 따른다. 
예전 튜토리얼의 `/v1/chat/completions`만 보는 글이 많지만, 플랫폼은 **Responses API** 등으로 이주·병행하는 추세다.

---

## 3. 대시보드 주요 메뉴 (이름·배치는 바뀔 수 있음)

| 영역 | 용도 |
|------|------|
| **API keys** | 프로젝트별 시크릿 키 발급·폐기 |
| **Usage** | 토큰·비용·요청 수 |
| **Billing / Limits** | 결제, 월 한도, 알림 |
| **Playground** | 채팅·완성 실험, 파라미터 조절 |
| **Organization / Projects** | 팀, 환경(dev/prod) 분리 |
| **Docs / Cookbook** | 가이드·예제 (developers.openai.com) |

여러 조직에 속하면 요청 헤더로 org·project를 지정할 수 있다 (`OpenAI-Organization`, `OpenAI-Project`).

---

## 4. 인증·보안

```text
Authorization: Bearer <API_KEY>
```

| 규칙 | 이유 |
|------|------|
| **서버에만** 키 두기 | 브라우저·모바일 앱에 넣으면 탈취 |
| git에 커밋 금지 | `.env`는 gitignore, 유출 시 즉시 revoke |
| 최소 권한·프로젝트 분리 | 유출 피해 범위 축소 |
| 정기 로테이션 | 직원 퇴사·유출 대응 |
| Admin 키 ≠ 앱 키 | 관리 API와 런타임 키 분리 |

키 유출 시: Platform에서 키 삭제 → 사용량 이상 여부 확인 → 새 키 발급.

Python 예 ([[Python 학습과 패키지]]):

```python
import os
from openai import OpenAI

client = OpenAI() # OPENAI_API_KEY 환경변수 사용

response = client.responses.create(
 model="gpt-5.6",
 input="한 줄로 자기소개 해 줘",
)
print(response.output_text)
```

(구 Chat Completions 예제 `chat.completions.create`도 레거시 코드에 많다. 신규는 문서의 Responses 권장을 따른다.)

---

## 5. API 표면 (무엇을 고르나)

공식 개요 기준:

| 경로 | 언제 |
|------|------|
| **Responses API** | 텍스트·도구·멀티모달·상태 있는 상호작용의 기본 축으로 권장되는 경우가 많음 |
| **Realtime API** | 저지연 음성·실시간 세션 (WebRTC/WebSocket 등) |
| **Administration** | 사용자·초대·프로젝트·키·감사 로그 (Admin 자격) |
| **Agents SDK** | 도구·핸드오프·승인·트레이싱이 있는 에이전트 오케스트레이션 |
| Legacy (Chat Completions, Assistants 등) | 기존 코드 유지·마이그레이션 대상. 신규는 문서의 “현재 권장” 확인 |

기능 키워드:

- **Structured Outputs** — JSON 스키마에 맞춘 응답 
- **Tools** — 웹 검색, 파일 검색, 함수 호출, 코드 실행 등 
- **Embeddings** — 검색·RAG용 벡터 
- **Images / Audio / Vision** — 생성·분석·음성 ([[OpenAI STT]] — 전사)

세부 스키마는 [API Reference](https://developers.openai.com/api/reference/overview/)를 본다.

---

## 6. 모델 고르기 

Frontier 라인은 세대마다 이름이 바뀐다. 2026년 문서 기준 예:

| 역할 | 예 (문서상) |
|------|-------------|
| 고난도 추론·코딩 | GPT-5.6 **Sol** (`gpt-5.6-sol`, 별칭 `gpt-5.6`이 Sol로 라우팅되는 경우) |
| 성능·비용 균형 | GPT-5.6 **Terra** |
| 대량·저비용 | GPT-5.6 **Luna** |

선택 팁:

1. Playground·소량 트래픽으로 **품질 먼저** 확인 
2. 그다음 한 단계 저렴한 모델로 A/B 
3. 프롬프트 캐싱·입출력 토큰을 Usage에서 관찰 
4. 코딩 IDE([[Cursor 사용법]])는 Platform 키가 아니라 **Cursor 구독·자체 라우팅**일 수 있음 — 혼동하지 말 것 

Deprecated 모델은 문서의 “Deprecated models”를 보고 이전한다.

---

## 7. Playground 활용

1. 시스템/개발자 지시 + 사용자 메시지 실험 
2. temperature, 토큰 한도, 도구 on/off 
3. 맘에 드는 설정을 **코드 스니펫으로보내** SDK에 반영 
4. 운영 전 반드시 서버에서 동일 모델 ID로 재현 

Playground 사용량도 **API와 같이 과금**되는 경우가 많다 (계정·정책 확인).

---

## 8. 요금·한도

- **토큰** 단위 과금 (입력·출력 단가 다름, 모델마다 다름) 
- 도구·검색·음성 등은 **별도 요금**이 붙을 수 있음 
- **Rate limit** (RPM/TPM) — 티어·결제 이력에 따라 상승 
- 월 **usage limit**을 낮게 잡아 폭주·유출 피해를 제한하는 것을 추천 

정확한 단가: Platform의 Pricing / 모델 카드. 
견적 시 “하루 N요청 × 평균 입출력 토큰”으로 대략 계산한다.

---

## 9. ChatGPT·다른 제품과의 관계

```text
ChatGPT 앱 ── 사람용 UI (구독)
Platform API ── 앱·서버 연동 (종량)
Azure OpenAI ── 기업·규정·리전 (Microsoft 계약, 엔드포인트·배포명 다름) → [[클라우드 AWS GCP Azure]]
Cursor 등 IDE ── 자체 과금/모델 라우팅 (Platform 키와 별개인 경우 많음)
```

- 같은 OpenAI 모델 가문이라도 **엔드포인트·약관·데이터 처리**가 제품마다 다를 수 있다. 
- API 데이터 사용 정책(학습 여부 등)은 Platform의 **How we use your data / 기업 약관**을 확인. 
- 국내 공공·금융은 외부 LLM API 반출 규정을 먼저 본다.

---

## 10. 최소 실습 체크리스트

- [ ] Platform 가입 · Billing 설정 
- [ ] API 키 발급 · 환경변수 
- [ ] `curl` 또는 SDK로 Responses(또는 문서 권장 API) 1회 성공 
- [ ] Playground에서 한국어 요약 프롬프트 시험 
- [ ] Usage에서 토큰·비용 확인 
- [ ] `.gitignore`에 `.env` 
- [ ] (앱 만들 때) 키를 프론트에 노출하지 않음 

Python:

```bash
pip install openai
```

Node:

```bash
npm install openai
```

공식 라이브러리 목록은 문서 Libraries 페이지.

---

## 11. 운영 시 주의

1. 프롬프트·사용자 입력을 로그에 무분별 저장 → 개인정보·비밀 
2. 환각 — 검색·Structured Output·사람 검수 ([[현존 AI 비교]]) 
3. 재시도·타임아웃·idempotency (결제·티켓 발급 등과 연결 시) 
4. 모델 업그레이드 시 회귀 테스트 
5. Assistants 등 legacy에 묶인 코드는 마이그레이션 계획 

---

## 12. 공식 링크

| 링크 | 내용 |
|------|------|
| [platform.openai.com](https://platform.openai.com/) | 대시보드·키·빌링·Playground |
| [API Docs](https://developers.openai.com/api/docs) | 가이드·퀵스타트 |
| [API Reference](https://developers.openai.com/api/reference/overview/) | 엔드포인트 스키마 |
| [Models](https://developers.openai.com/api/docs/models) | 모델 목록·비교 |

---

## 관련

- [[현존 AI 비교]]
- [[OpenAI STT]]
- [[클라우드 AWS GCP Azure]]
- [[Python 학습과 패키지]]
- [[Cursor 사용법]]
- [[NotebookLM 사용법]]
- [[생활위키 목차]]
