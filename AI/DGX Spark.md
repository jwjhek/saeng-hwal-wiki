---
publish: true
draft: false
depth: article
aliases:
  - NVIDIA DGX Spark
  - Project DIGITS
  - GB10
  - 디지츠
---

# DGX Spark

> **분류:** AI · [[생활위키 목차]]

**NVIDIA DGX Spark**는 책상 위에 두는 **개인용 AI 컴퓨터**다. 예전 코드명 **Project DIGITS**.  
안에 **GB10 Grace Blackwell Superchip**(Arm CPU + Blackwell GPU, 메모리 공유)이 들어가고, NVIDIA는 이걸 로컬에서 **큰 모델 추론·미세조정·에이전트**를 돌리는 상자로 안내한다.

공식 제품: [https://www.nvidia.com/en-us/products/workstations/dgx-spark/](https://www.nvidia.com/en-us/products/workstations/dgx-spark/)  
하드웨어 가이드: [https://docs.nvidia.com/dgx/dgx-spark/hardware.html](https://docs.nvidia.com/dgx/dgx-spark/hardware.html)  
발표: [NVIDIA 뉴스룸 (2025-03)](https://nvidianews.nvidia.com/news/nvidia-announces-dgx-spark-and-dgx-station-personal-ai-computers)

확인일: 2026-08-18  
스펙·가격·파트너 SKU는 **NVIDIA·판매처**가 우선이다. 이 글의 숫자는 고정 견적이 아니다.

관련: [[Ollama]] · [[현존 AI 비교]] · [[클라우드 AWS GCP Azure]]

---

## 1. 개요

| 항목 | 설명 |
|------|------|
| **무엇** | 소형 데스크톱 **AI 워크스테이션**. 데이터센터 DGX 랙이 아니라 **책상 박스** |
| **칩** | NVIDIA **GB10** — Grace(Arm) CPU + Blackwell GPU, NVLink-C2C로 **CPU·GPU 메모리를 같이 봄** |
| **메모리** | **128 GB** LPDDR5x **통합**(VRAM 24 GB + 시스템 램이 따로 나뉜 일반 PC와 다름) |
| **OS** | **NVIDIA DGX OS** (Ubuntu 계열 안내) → 바탕 개념은 [[Ubuntu]]·[[리눅스]] |
| **무엇이 아님** | 게임용 조립 PC, x86 윈도우 워크스테이션, 랙형 **DGX** 서버, **DGX Station**(한 체급 위) |

```text
로컬에서 큰 모델을 돌리고 싶다
 ├─ 이미 GPU 있는 PC → [[Ollama]] 등으로 먼저 실험
 ├─ 클라우드 GPU 빌려 쓰기 → [[클라우드 AWS GCP Azure]]
 ├─ 책상 위 NVIDIA 전용 박스 → DGX Spark (이 글)
 └─ 팀 단위 초대형 데스크톱 → DGX Station (별 제품)
```

크기는 대략 **150 × 150 × 50.5 mm**, 무게 **1.2 kg** 안내. 콘솔만 한 발자국이다.

---

## 2. 쓰는 이유

- **VRAM이 모자란 모델**을 한 대에 올려 보고 싶을 때. 공식은 단일 기기 **최대 약 200B(2천억) 파라미터** 추론, 두 대를 ConnectX-7로 묶으면 **약 405B(4천억)**까지라는 안내가 있다. `B` 읽는 법은 [[파라미터 수]]. **양자화·구현·실제 속도**는 모델마다 다르다.
- 데이터가 **밖으로 나가면 안 되는** 프로토타입. 클라우드 토큰과 역할이 다르다 → [[OpenAI Platform]]·[[Ollama]] `:cloud`와 구분.
- 전력·소음이 랙 서버보다 **책상 쪽**. GB10 TDP **140 W**, 외부 어댑터 **240 W** 안내.
- 나중에 DGX Cloud·가속 클라우드로 **코드를 거의 안 바꾸고** 옮긴다는 NVIDIA 스택 안내 (NIM·CUDA-X 등). 전제는 **그 스택을 쓰는 워크플로**.

일반 RTX 한 장 + [[Ollama]]로 작은·중간 모델이 충분하면 Spark가 **필수는 아니다.**

---

## 3. 스펙 (공식 안내 요약)

확인일 기준 제품·사용자 가이드에 나오는 값이다. SKU(저장 1 TB / 4 TB 등)는 판매처마다 다를 수 있다.

| 항목 | 안내 |
|------|------|
| **아키텍처** | NVIDIA Grace Blackwell |
| **GPU** | Blackwell, Tensor 5세대, RT 4세대. CUDA 코어는 가이드에 **6144**로 적힌 문서가 있음 |
| **CPU** | Arm **20코어** — Cortex-X925 10 + Cortex-A725 10 |
| **AI 연산 표기** | 최대 **1 PFLOP FP4**(희소성 포함) / **1000 TOPS**급 마케팅 숫자. 실사용 BF16·FP8과는 **단위가 다름** |
| **메모리** | 128 GB LPDDR5x, 256-bit, 대역 **273 GB/s** |
| **저장** | NVMe M.2, 자체 암호화. **1 TB 또는 4 TB** 안내 |
| **네트워크** | 10 GbE(RJ-45), **ConnectX-7 200 Gbps**, Wi-Fi 7, Bluetooth 5.4 |
| **입출력** | USB-C 4, HDMI 2.1a, USB-C DisplayPort 알트모드(최대 3) |
| **영상** | NVENC 1 / NVDEC 1 |
| **전원** | 외부 240 W, GB10 TDP 140 W |

**대역 273 GB/s**는 통합 128 GB로 **모델을 넣는 용량**과, HBM 데이터센터 GPU의 **토큰 속도**를 한 줄에 비교하면 안 된다. 큰 모델이 **들어간다**와 **빠르게 나온다**는 별 문제다.

---

## 4. 소프트웨어

| 층 | 메모 |
|----|------|
| **DGX OS** | NVIDIA가 맞춘 리눅스. 일반 윈도우 설치 대상이 아님 |
| **CUDA · 프레임워크** | PyTorch, TensorRT-LLM 등 **aarch64 + CUDA** 빌드. x86 휠을 그대로 복사하면 실패하기 쉬움 |
| **엔터프라이즈 스택** | NIM 마이크로서비스, NVIDIA AI Enterprise 안내는 **라이선스·지원 계약**이 붙는 경우가 있음 |
| **로컬 챗 런타임** | [[Ollama]] 등 오픈 웨이트 실행기는 **Arm 지원·이미지 태그**를 문서에서 확인 |

**Arm**이라 윈도우용 설치 파일, 많은 **x86 Docker 이미지**는 바로 안 돈다. 컨테이너는 [[Docker 사용법]] + **리눅스/ARM64** 전제.

---

## 5. 다른 것과 비교

| | DGX Spark | DGX Station | 일반 NVIDIA GPU PC | 클라우드 GPU |
|--|-----------|-------------|-------------------|--------------|
| **자리** | 책상 소형 박스 | 대형 데스크톱(타워) | 조립·브랜드 워크스테이션 | 빌려 쓰는 인스턴스 |
| **칩 예** | GB10 | GB300 Grace Blackwell Ultra 등 | RTX·데이터센터 GPU (x86이 흔함) | A100/H100 등 세대는 상품명 |
| **메모리 감각** | 통합 128 GB | 수백 GB 통합(제품 세대별) | VRAM이 보통 수십 GB | 시간당 과금, 큰 VRAM 가능 |
| **전력** | 200 W대 어댑터 | 킬로와트급 안내가 흔함 | 카드+파워에 따라 | 데이터센터 |
| **잘 맞는 일** | 개인 프로토타입·로컬 에이전트 | 팀 학습·초대형 추론 | 게임+학습 겸용, 기존 x86 툴 | 가끔 큰 학습, 탄력 |

파트너 상자(예: ASUS Ascent GX10 등)는 **같은 GB10 계열**을 OEM이 만든 제품이다. 보증·포트·가격은 **그 브랜드 페이지**.

판매·예약은 NVIDIA Founders와 ASUS·Dell·HP·Lenovo 등 **시스템 빌더** 안내가 있었다. **재고·국내 유통은 판매처**.

---

## 6. 고를 때 체크

| 질문 | 보면 좋은 것 |
|------|----------------|
| **이미 GPU PC가 있나** | 7B~32B는 [[Ollama]]로 충분한 경우가 많음 |
| **윈도우 앱·x86 도구가 필수인가** | Spark는 **Arm 리눅스**. 듀얼 PC가 필요할 수 있음 |
| **학습(파인튜닝) 규모** | 공식도 추론 쪽이 강조. 큰 학습은 Station·클라우드가 맞는 경우가 많음 |
| **두 대 연결** | ConnectX-7·케이블·설정. “405B”는 **구성·모델 전제** |
| **값** | 달러 정가는 **수시 변경**(메모리 수급 보도도 있었음). 전기·지원·소프트웨어 라이선스를 같이 본다 |
| **소음·온도** | 가이드 동작 온도 **5~30 °C**대. 여름 밀폐 책상은 확인 |

구매 권유가 아니다. 견적·통관·A/S는 **판매자·NVIDIA 지원**.

---

## 7. 확인 방법

1. [DGX Spark 제품 페이지](https://www.nvidia.com/en-us/products/workstations/dgx-spark/) — 표 스펙  
2. [DGX Spark User Guide](https://docs.nvidia.com/dgx/dgx-spark/) — 하드웨어·OS  
3. [지원](https://www.nvidia.com/en-us/support/dgx-spark/)  
4. 로컬 실행 개념 → [[Ollama]] · 모델 비교 → [[현존 AI 비교]]  
5. 클라우드 대안 → [[클라우드 AWS GCP Azure]] · [[OpenAI Platform]]

---

## 면책

> **면책**
> - **특정 모델·판매처·구독 권유가 아니다.**
> - PFLOP·파라미터 상한·가격은 **마케팅·SKU·개정**에 따라 바뀐다. 공식 표가 우선이다.
> - Arm·드라이버·모델 라이선스는 **이용자 책임**. 이 글이 우회·무단 클러스터 구성을 안내하지 않는다.

---

## 관련

- [[Ollama]]
- [[파라미터 수]]
- [[현존 AI 비교]]
- [[OpenAI Platform]]
- [[클라우드 AWS GCP Azure]]
- [[Docker 사용법]]
- [[Ubuntu]]
