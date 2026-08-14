---
publish: true
draft: false
depth: article
aliases:
  - Model Context Protocol
  - 모델 컨텍스트 프로토콜
  - MCP 서버
---

# MCP

> **분류:** AI · [[생활위키 목차]]

**MCP**(Model Context Protocol)는 AI 앱이 **외부 도구·데이터**에 붙는 **공개 표준**이다. 공식은 USB-C에 비유한다. 충전기마다 다른 단자가 아니라, **한 규격으로 여러 기기**를 꽂는 쪽에 가깝다.

챗창에 파일을 붙이는 것과 달리, 서버가 **도구(tools)·자료(resources)·프롬프트 틀**을 정해 두고, 호스트(Cursor·Claude·ChatGPT 등)가 그걸 호출한다. HTTP [[API]]와 겹치지만, **사람용 REST**가 아니라 **LLM 에이전트가 쓰기 위한 계약**이다.

공식: [https://modelcontextprotocol.io](https://modelcontextprotocol.io)  
스펙: [https://modelcontextprotocol.io/specification/latest](https://modelcontextprotocol.io/specification/latest)  
Cursor: [https://cursor.com/docs/mcp](https://cursor.com/docs/mcp)

확인일: 2026-08-14  
개정·전송 방식·호스트 UI는 **공식 스펙·쓰는 앱 문서**가 우선이다.

관련: [[API]] · [[Cursor 사용법]] · [[Cursor 스킬 설정]] · [[OpenAI Platform]]

---

## 1. 개요

| 항목 | 설명 |
|------|------|
| **무엇** | AI 앱 ↔ 외부 시스템 **도구·맥락**을 주고받는 프로토콜 |
| **누가 만들었나** | Anthropic이 연 뒤 **공개 표준**으로 여러 제품이 붙음 |
| **메시지** | 대개 **JSON-RPC 2.0** |
| **비유** | 언어 서버의 Language Server Protocol(LSP)이 IDE에 언어를 붙이듯, MCP는 AI에 **도구**를 붙임 |
| **무엇이 아님** | 모델 그 자체, 채팅 구독, [[Cursor 스킬 설정]]의 `SKILL.md`, 일반 REST [[API]] 대체품 |

```text
호스트 (Cursor · Claude · ChatGPT …)
  ├─ 클라이언트 A ── 서버 A (로컬 프로세스, stdio)
  └─ 클라이언트 B ── 서버 B (원격 HTTP)
         ↓
도구 호출 · 자료 읽기 · (선택) 프롬프트 틀
```

[[현존 AI 비교]]의 **에이전트**가 터미널·브라우저를 쓰는 것과 같은 축이다. MCP는 그 연결을 **제품마다 다른 플러그인**이 아니라 **같은 규격**으로 맞춘다.

---

## 2. 호스트 · 클라이언트 · 서버

말은 헷갈리기 쉽다. **서버가 AI가 아니다.**

| 역할 | 하는 일 | 예 |
|------|---------|-----|
| **호스트** | AI 앱. 연결을 고르고, 모델에게 도구를 보여 줌 | Cursor, VS Code, Claude Desktop |
| **클라이언트** | 호스트 안 **한 서버당 하나**인 연결 쪽 | Cursor가 레드마인 서버에 붙는 통로 |
| **서버** | 도구·자료를 **제공하는 프로그램** | 이슈 트래커, 브라우저, DB, 캘린더 |

로컬 서버는 같은 PC에서 프로세스로 뜨는 경우가 많고, 원격 서버는 **HTTP**로 붙는다. 공식 전송 예: **stdio**(표준 입출력), **Streamable HTTP**.

2026년 스펙 개정(예: `2026-07-28`)은 **요청마다 버전·능력을 실어 상태를 덜 붙이는** 쪽으로 가는 안내가 있다. 쓰는 Cursor·SDK가 **어느 개정**을 말하는지는 그 문서.

---

## 3. 서버가 여는 것

| 종류 | 한 줄 |
|------|--------|
| **Tools** | 모델이 **실행**할 수 있는 동작. 검색, 이슈 만들기, 페이지 열기 |
| **Resources** | 읽기용 **맥락**. 파일·레코드·문서 URI |
| **Prompts** | 자주 쓰는 **대화 틀**. 호스트가 메뉴로 보여 주기도 함 |

호스트는 목록을 받은 뒤, 사용자가 동의한 범위에서 도구를 부른다. **승인 없이 뭐든 실행**한다고 단정하지 말 것. Cursor는 채팅 중 도구 호출을 보여 주는 편이다.

확장(Tasks, MCP Apps 등)은 스펙이 **선택**으로 붙는 안내가 있다. 필수가 아니다.

---

## 4. [[API]] · 스킬 · 규칙과

| | MCP | REST [[API]] | [[Cursor 스킬 설정]] · 규칙 |
|--|-----|--------------|------------------------------|
| 상대 | AI 호스트 | 앱·서버·curl | 같은 Cursor 안의 절차·제약 |
| 계약 | 도구 스키마 + JSON-RPC | URL·메서드·JSON | `SKILL.md` · `.cursor/rules` |
| 키 | 서버·OAuth·환경 변수 | 헤더·토큰 | 보통 없음 |
| 자리 | “이 서비스에 **손을 뻗게**” | “이 엔드포인트를 **호출**” | “이 일을 **이렇게** 하라” |

[[OpenAI Platform]]의 function calling·Responses 도구와 **목적이 비슷**하다. MCP는 **호스트가 여러 서버**를 같은 방식으로 꽂게 한다. 모델 API 키와 MCP 서버 토큰은 **별개**인 경우가 많다 → [[Bitwarden 사용법]].

[[바이브 코딩]]으로 검수 없이 도구를 승인하면, 권한이 큰 서버일수록 피해가 커진다.

---

## 5. Cursor에서

[[Cursor 사용법]] 호스트 기준(메뉴 이름은 버전이 바꿈):

| 경로 | 설명 |
|------|------|
| **UI** | 설정 · Customize · Tools & MCP. 마켓에서 한 번에 넣는 안내가 있음 |
| **프로젝트** | `.cursor/mcp.json` — 이 저장소. 팀에 공유할 때 |
| **개인** | `~/.cursor/mcp.json` — 모든 워크스페이스. Windows는 사용자 폴더 아래 `.cursor` |
| **이름 겹침** | 같은 서버 이름이 있으면 **프로젝트 쪽이 우선**이라는 안내 |

로컬은 `command`+`args`(실행 파일·npx 등), 원격은 `url`(필요하면 헤더). 키·토큰은 **파일에 박지 말고** 환경 변수·비밀 저장. Git에 `mcp.json`을 올릴 거면 **비밀을 빼는지** 본다.

```json
{
  "mcpServers": {
    "example-local": {
      "command": "npx",
      "args": ["-y", "package-name"]
    },
    "example-remote": {
      "url": "https://mcp.example.com"
    }
  }
}
```

위는 **모양만**. 패키지명·주소·인증은 그 서버 문서. `API_KEY` 실값을 채팅·커밋에 붙이지 말 것.

켠 뒤 에이전트가 도구를 안 쓰면: 서버가 **연결됨**(초록 표시 등)인지, 창을 다시 열었는지, 도구 승인란을 본다. UI는 [Cursor MCP 문서](https://cursor.com/docs/mcp)가 맞다.

이슈 트래커를 붙이는 예는 [[레드마인]]. **회사 정책·권한**이 프로토콜보다 앞선다.

---

## 6. 고를 때 · 주의

| 습관 | 왜 |
|------|-----|
| **출처** | 아무 서버나 실행하면 그 프로세스 권한만큼 손이 간다 |
| **최소 권한** | 읽기만 필요한데 쓰기·삭제 도구를 열지 않기 |
| **승인** | 채팅에 뜬 도구 호출을 **읽고** 수락 |
| **비밀** | 토큰은 [[Bitwarden 사용법]]. 로그·스크린샷에 헤더가 남을 수 있음 |
| **회사** | 사내 MCP·데이터 반출은 보안 팀 문서 |

스펙·SDK(Python·TypeScript 등)로 **서버를 직접 만드는** 자리는 이 글 밖이다. 시작은 [modelcontextprotocol.io](https://modelcontextprotocol.io)의 서버·클라이언트 가이드.

---

## 7. 정리

| 항목 | 한 줄 |
|------|--------|
| 정의 | AI가 외부 도구·자료를 쓰는 **공개 프로토콜** |
| 공식 | [https://modelcontextprotocol.io](https://modelcontextprotocol.io) |
| 호스트 | Cursor · Claude · ChatGPT · VS Code 등. **제품마다 켜는 법** |
| REST | [[API]]는 앱끼리. MCP는 **에이전트용 플러그 규격** |
| 절차 문서 | [[Cursor 스킬 설정]] · 규칙. MCP와 **겹치지 않음** |
| 키 | [[Bitwarden 사용법]] · Git에 실값 금지 |

---

## 면책

> **면책**
> - **특정 서버·마켓 설치 권유가 아니다.**
> - 스펙 개정·전송·OAuth·호스트 UI는 **공식 문서**가 바꾼다.
> - 서버는 실행 권한만큼 파일·계정·네트워크에 닿을 수 있다. 이 글이 보안 심사를 하지 않는다.
> - 타인 시스템 **무단 접속·우회**를 안내하지 않는다. 토큰 탈취·공격 절차는 다루지 않는다.

---

## 관련

- [[생활위키 목차]]
- [[API]]
- [[Cursor 사용법]]
- [[Cursor 스킬 설정]]
- [[OpenAI Platform]]
- [[현존 AI 비교]]
- [[Bitwarden 사용법]]
