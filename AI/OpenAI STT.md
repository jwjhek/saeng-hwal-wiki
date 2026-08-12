---
publish: true
draft: false
depth: article
aliases:
  - OpenAI 음성 전사
  - Whisper API
---

# OpenAI STT

> **분류:** AI · [[생활위키 목차]]

**OpenAI STT**(Speech-to-Text, 음성→텍스트)는 [[OpenAI Platform]] API로 **녹음 파일·실시간 오디오**를 **텍스트 전사**하는 기능이다. 
예전에는 **Whisper** 모델이 중심이었고, 지금은 **`gpt-transcribe`** 계열이 일반 전사의 **권장** 모델이다.

공식: [Speech-to-text 가이드](https://developers.openai.com/api/docs/guides/speech-to-text)  
API: `POST /v1/audio/transcriptions`

확인일: 2026-08-12  
모델 ID·요금·지원 포맷은 **자주 바뀐다** — [Models](https://developers.openai.com/api/docs/models) · 대시보드가 최종본.

관련: [[OpenAI Platform]] · [[Python 학습과 패키지]] · [[현존 AI 비교]] · [[위키 쇼츠 자동 제작]](TTS·자막)

---

## 1. 개요

| 용어 | 의미 |
|------|------|
| **STT** | Speech-to-Text — 말을 글자로 |
| **전사(transcription)** | 원어 그대로 텍스트로 옮김 |
| **번역(translation)** | API에서는 주로 **영어로** 옮김 (`whisper-1` + `/translations`) |
| **화자 분리(diarization)** | 누가 언제 말했는지 **화자 라벨** 붙임 |

```text
[마이크·회의 녹음·팟캐스트 mp3]
        ↓ 업로드 또는 실시간 스트림
[OpenAI STT 모델]
        ↓
[텍스트] · (선택) 화자·타임스탬프
        ↓
요약·검색·자막·RAG·회의록
```

**ChatGPT 앱**에서 음성 대화·전사를 쓰는 것과 **Platform API STT**는 **계정·과금·제어**가 다르다. 앱에 API 권한이 자동으로 붙지 않는다 → [[OpenAI Platform]].

---

## 2. 언제 쓰나

| 상황 | OpenAI STT |
|------|------------|
| 회의·인터뷰 **녹음 파일**을 글로 | 파일 전사 |
| 콜센터·고객 통화 **기록** | `gpt-transcribe` + (필요 시) diarize |
| **실시간 자막**·라이브 캡션 백엔드 | Realtime + `gpt-live-transcribe` |
| 팟캐스트·강의 **자막** 제작 | whisper-1 타임스탬프 또는 후처리 |
| 다국어 오디오 → **영어**만 필요 | `/translations` + `whisper-1` |

OS 기본 **라이브 캡션**·무료 로컬 Whisper는 비용·개인정보 측면에서 대안이다 → [[라이브 캡션]].

---

## 3. 모델 선택

**완료된 녹음**은 보통 **`gpt-transcribe`**부터 쓴다. 특수 요건이 있을 때만 아래로 분기한다.

| 모델 | 용도 | 비고 |
|------|------|------|
| **`gpt-transcribe`** | **일반 전사**(권장) | 원어 유지, `prompt`·`keywords`·`languages` |
| **`gpt-4o-transcribe`** | 고정확도 전사 | 문서·마이그레이션 경로에 남아 있는 이름 |
| **`gpt-4o-mini-transcribe`** | 저비용·대량 | 정확도·비용 트레이드오프 |
| **`gpt-4o-transcribe-diarize`** | **화자 분리** | `diarized_json`, 30초 초과 시 `chunking_strategy` |
| **`whisper-1`** | 레거시·**타임스탬프**·**SRT/VTT**·**영어 번역** | 신규 일반 전사는 `gpt-transcribe` 우선 |
| **`gpt-live-transcribe`** | **실시간** 스트리밍 전사 | Realtime API 세션 |

```text
녹음 파일이 이미 있음?
  ├─ 화자 구분 필요 → gpt-4o-transcribe-diarize
  ├─ 자막용 단어·구간 시간 필요 → whisper-1 (timestamp_granularities)
  ├─ 다른 언어 → 영어 번역만 → /translations + whisper-1
  └─ 그 외 일반 전사 → gpt-transcribe

마이크·통화가 계속 들어옴?
  └─ Realtime transcription + gpt-live-transcribe
```

모델 이름은 세대마다 바뀐다. 배포 전 **Playground·소량 테스트**로 WER(오인식률)을 본다.

---

## 4. 파일 전사 — 빠른 시작

### 4.1 제한

| 항목 | 일반적 한도 |
|------|-------------|
| 파일 크기 | **25 MB** (초과 시 압축·분할) |
| 형식 | mp3, mp4, mpeg, mpga, m4a, wav, webm |
| 인증 | `Authorization: Bearer <API_KEY>` |

### 4.2 Python 예

```python
from openai import OpenAI

client = OpenAI()  # OPENAI_API_KEY 환경변수

with open("meeting.wav", "rb") as f:
    result = client.audio.transcriptions.create(
        model="gpt-transcribe",
        file=f,
    )

print(result.text)
```

### 4.3 cURL 예

```bash
curl https://api.openai.com/v1/audio/transcriptions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F file="@audio.mp3" \
  -F model="gpt-transcribe"
```

응답에 **감지된 언어**(`languages`)가 JSON으로 올 수 있다. 신뢰할 수 없으면 빈 배열일 수 있다.

---

## 5. 정확도 높이기 — 맥락·키워드

`gpt-transcribe`는 **도메인 용어**를 넣을 때 아래 필드가 도움이 된다.

| 필드 | 역할 |
|------|------|
| **`prompt`** | 통화·회의 **상황** 설명 (예: “프리미엄 요금제 상담”) |
| **`keywords`** | 반드시 맞추고 싶은 **고유명·약어** 목록 |
| **`languages`** | 예상 **언어 코드** 배열 (다국어 혼합) |

```python
transcription = client.audio.transcriptions.create(
    model="gpt-transcribe",
    file=open("call.wav", "rb"),
    prompt="고객 지원 통화, 계정 AC-42, 요금제 문의",
    extra_body={
        "keywords": ["AC-42", "프리미엄", "청구"],
        "languages": ["ko", "en"],
    },
)
```

`whisper-1`의 짧은 **prompt**(224 토큰)보다 **제어가 넓은** 편이다. 다만 **말한 내용을 바꾸지 않는지** 샘플로 검증한다.

---

## 6. 화자 분리 (diarization)

회의록에서 **누가 말했는지** 필요하면 `gpt-4o-transcribe-diarize`를 쓴다. **일반 전사용이 아니다.**

| 옵션 | 설명 |
|------|------|
| `response_format="diarized_json"` | 화자·시작·끝 구간 메타데이터 |
| `chunking_strategy="auto"` | **30초 초과** 녹음에 필요 |
| `known_speaker_names` + 참조 클립 | 알려진 화자 매핑 (Cookbook 예시) |

Realtime 세션에서는 **화자 분리 미지원** — 파일 API 전용.

---

## 7. 스트리밍·실시간

### 7.1 파일 스트리밍

**이미 끝난 파일**도 처리하면서 **부분 텍스트**를 받을 수 있다 (`transcript.text.delta` 등).  
마이크 실시간과는 **다른 경로**다.

### 7.2 Realtime 전사

**마이크·통화·미디어 스트림**이 **계속 들어올 때**는 [Realtime transcription](https://developers.openai.com/api/docs/guides/realtime-transcription) 가이드를 본다.

| | 파일 전사 | Realtime |
|--|-----------|----------|
| 입력 | 완료된 mp3·wav 등 | WebSocket·WebRTC 스트림 |
| 모델 | `gpt-transcribe` 등 | **`gpt-live-transcribe`** |
| 지연 | 배치·스트리밍 처리 | **저지연** |

음성 **에이전트**(말하고 듣고 답하기)는 Realtime API 전체 문서와 겹친다.

---

## 8. Whisper(`whisper-1`) — 아직 쓰는 경우

| 기능 | whisper-1 |
|------|-----------|
| **`/v1/audio/translations`** | 다른 언어 오디오 → **영어** 텍스트만 |
| **타임스탬프** | `timestamp_granularities[]` — 자막·편집 |
| **자막 포맷** | srt, vtt 등 (모델별 지원은 문서 확인) |
| **레거시 코드** | 기존 파이프라인 유지 |

신규 **일반 전사**는 `whisper-1` 대신 **`gpt-transcribe`**로 옮기는 것이 공식 권장 방향이다.  
마이그레이션: [Whisper → GPT-Transcribe](https://developers.openai.com/cookbook/examples/migrating_from_whisper_to_gpt_transcribe)

---

## 9. TTS와 짝

| | STT (이 글) | TTS |
|--|-------------|-----|
| 방향 | 음성 → 텍스트 | 텍스트 → 음성 |
| OpenAI | `/audio/transcriptions` | `/audio/speech` |
| 이 vault 예 | 회의록·자막 원문 | [[위키 쇼츠 자동 제작]] — edge-tts 등 |

전사본을 LLM에 넣어 **요약·액션 아이템**을 뽑는 패턴이 흔하다 → [[OpenAI Platform]] Responses API.

---

## 10. 보안·개인정보

| 주의 | |
|------|--|
| **API 키** | 서버·환경 변수만 — git·프론트 금지 ([[OpenAI Platform]] §4) |
| **녹음 내용** | 통화·의료·금융 — **동의·보관 정책** 확인 |
| **로그** | 플랫폼·자체 서버에 원본 오디오·전사문 남기지 않기 |
| **환각** | STT도 고유명·숫자 **오인식** 가능 — 중요 필드는 사람 검수 |

---

## 11. 비용·한도

- **오디오 길이·모델·스트리밍**에 따라 과금 (토큰과 **별도** 요금표인 경우 많음)  
- 대시보드 **Usage**에서 확인  
- 긴 회의는 **압축·분할** 후 배치 — 25 MB·타임아웃 주의  

정확한 단가는 [Pricing](https://openai.com/api/pricing/) · 모델 페이지.

---

## 12. 실무 팁

1. **짧은 샘플**로 모델·`keywords` 튜닝 후 전체 파일 투입  
2. 노이즈·다중 화자면 **마이크·녹음 품질**이 API보다 먼저  
3. 자막은 전사 → **타임코드** → SRT 편집기 ([[CapCut 사용법]])  
4. 한국어 회의는 `languages: ["ko"]` 힌트 + 고유명 `keywords`  
5. Whisper 레거시는 **기능 하나씩** `gpt-transcribe`로 이전 계획  
6. 실시간·파일·diarize를 **한 요청에 섞지 말고** 경로 분리  

---

## 13. 정리

1. OpenAI STT = Platform **음성→텍스트** API.  
2. **완료된 녹음** → `gpt-transcribe`가 기본.  
3. **화자 분리** → `gpt-4o-transcribe-diarize`.  
4. **실시간** → Realtime + `gpt-live-transcribe`.  
5. **영어 번역·레거시 자막** → `whisper-1` + 해당 엔드포인트.  
6. 키·개인정보·오인식은 **직접 검수**.

---

## 면책

> **면책**  
> API 사용·요금·데이터 처리 정책은 **OpenAI 약관·조직 설정**을 따른다.  
> 의료·법률 기록은 **전문가 검수**가 필요하다. 이 글은 **개발 학습용**이며 특정 상품 가입을 권하지 않는다.

---

## 관련

- [[OpenAI Platform]] — API 키·빌링·Realtime
- [[현존 AI 비교]] — ChatGPT 앱 vs API, 환각
- [[Python 학습과 패키지]] — SDK·venv
- [[위키 쇼츠 자동 제작]] — TTS·자막 파이프라인 (역방향은 STT)
- [[CapCut 사용법]] — 자막 편집
- [[라이브 캡션]] — OS 내장 실시간 자막
- [[NotebookLM 사용법]] — 전사문·문서 기반 Q&A
- [[생활위키 목차]]
