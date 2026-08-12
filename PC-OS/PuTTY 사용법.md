---
publish: true
draft: false
depth: article
aliases:
  - putty
  - 푸티
  - PuTTY
---

# PuTTY 사용법

> **분류:** PC·OS · [[생활위키 목차]]

**PuTTY**는 **Windows**에서 **SSH**·Telnet·시리얼 등으로 **원격 터미널**에 접속하는 **무료 클라이언트**다. 
리눅스 서버·VPS·라즈베리파이·네트워크 장비에 **쉘**을 붙을 때 오래 쓰인 도구다.

공식: [https://www.putty.org](https://www.putty.org) (다운로드는 [PuTTY 다운로드 페이지](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html))  
확인일: 2026-08-12

관련: [[윈도우 사용법]] · [[리눅스 기본 명령어]] · [[리눅스]] · [[Git 사용법]] · [[DBeaver 사용법]]

---

## 1. 개요

| 항목 | 설명 |
|------|------|
| 무엇 | **SSH 클라이언트** + 터미널 창 (Windows용) |
| 요금 | **무료**·오픈 소스 (라이선스는 버전별 안내 확인) |
| 주 용도 | **원격 서버** 쉘, 장비 설정, 파일 전송(부속 도구) |
| 대안 | Windows **OpenSSH**(`ssh`), **Windows Terminal**, WSL `ssh`, [[VS Code 사용법]] Remote SSH |

```text
[Windows PC]  PuTTY  --SSH(보통 22번 포트)-->  [리눅스 서버 / VPS]
                      비밀번호 또는 SSH 키
```

서버에 붙은 뒤 명령은 [[리눅스 기본 명령어]]와 같다. PuTTY는 **접속 도구**일 뿐이다.

---

## 2. 언제 쓰나

| 상황 | PuTTY | 다른 선택 |
|------|-------|-----------|
| 회사·학교 PC에 **설치만** 허용 | 흔함 | |
| **간단히** IP·포트 넣고 접속 | 적합 | |
| 매일 개발·Git·여러 탭 | | **Windows Terminal** + `ssh` |
| 코드 편집까지 원격 | | VS Code **Remote SSH** |
| Android에서 SSH | | [[Termux 사용법]] |
| DB가 VPN·SSH 뒤 | PuTTY **터널** 또는 DBeaver SSH ([[DBeaver 사용법]]) |

Windows 10/11에는 **OpenSSH 클라이언트**를 켜 두고 `ssh user@host` 만 써도 되는 경우가 많다 ([[윈도우 사용법]]). 
PuTTY는 **GUI로 세션 저장**·**PPK 키**·**시리얼**이 익숙할 때 유리하다.

---

## 3. 설치

1. 공식 사이트에서 **Windows Installer**(`putty-64bit-*-installer.msi`) 또는 **포터블** `putty.exe` 받기  
2. **출처 확인** — 검색 광고·무료 설치기 사이트는 피하고 **공식 링크**만  
3. 설치 후 시작 메뉴 **PuTTY** 실행  

회사 PC는 **보안 정책**·관리자 승인이 필요할 수 있다.

---

## 4. SSH 접속 (처음)

### 4.1 기본 설정

| 필드 | 예 | 설명 |
|------|-----|------|
| **Host Name** | `203.0.113.10` 또는 `server.example.com` | 서버 주소 |
| **Port** | `22` | SSH 기본 포트 (바뀐 경우 관리자에게 확인) |
| **Connection type** | **SSH** | Telnet은 암호화 없음 — 가급적 SSH |

**Open** → 처음 접속 시 **호스트 키** 지문 확인 창이 뜬다.  
**신뢰할 수 있는 서버**일 때만 **Accept**한다. 중간자 공격 시 지문이 바뀐다.

### 4.2 로그인

- **login as:** `ubuntu`, `root`, `ec2-user` 등 (서버·클라우드마다 다름)  
- **Password:** 입력 시 **화면에 안 보임** — 정상  

접속 후 `pwd`, `ls` 등 [[리눅스 기본 명령어]]로 확인한다.

### 4.3 세션 저장

자주 쓰는 접속은 저장해 둔다.

1. Host·Port 입력  
2. **Saved Sessions**에 이름 (예: `my-vps`)  
3. **Save**  
4. 다음부터 목록에서 선택 → **Load** → **Open**

---

## 5. SSH 키 인증

비밀번호 대신 **키**로 로그인하는 경우가 많다 (VPS·Git 서버).

| 도구 | 역할 |
|------|------|
| **PuTTYgen** | 키 **생성**·변환. PuTTY 형식 **`.ppk`** |
| **Pageant** | 키를 메모리에 올려 **비밀번호 반복 입력** 줄임 |
| **PuTTY** | Connection → SSH → Auth → **Private key file** 에 `.ppk` 지정 |

### OpenSSH 키(`id_rsa`·`id_ed25519`)가 있을 때

1. **PuTTYgen** → **Conversions** → **Import key**  
2. `.ppk`로 **Save private key**  
3. PuTTY **Auth**에 그 `.ppk` 연결  

또는 Windows OpenSSH로 생성한 키를 그대로 쓰려면 **Windows Terminal**의 `ssh -i` 가 더 단순할 수 있다 ([[Git 사용법]] SSH).

**개인 키**는 USB·메일로 보내지 않는다. 서버에는 **공개키**만 등록한다.

---

## 6. 자주 쓰는 옵션

| 메뉴 | 설명 |
|------|------|
| **Connection → Seconds between keepalives** | `30` 등 — 유휴 **끊김** 방지 |
| **Window → Lines of scrollback** | 스크롤 **로그** 줄 수 늘리기 |
| **Terminal → Keyboard** | 백스페이스·홈/엔드 키 동작 |
| **Connection → Data → Auto-login username** | 사용자 이름 미리 넣기 (비밀번호는 자동 저장 안 됨) |
| **SSH → Tunnels** | **로컬 포트 포워딩** — DB·웹을 터널로 ([[DBeaver 사용법]]) |

옵션 바꾼 뒤 **Session**으로 돌아가 **Save**해야 세션에 남는다.

---

## 7. 부속 프로그램

| 프로그램 | 용도 |
|----------|------|
| **PSCP** | 명령줄 **파일 복사** (scp와 유사) |
| **PSFTP** | **SFTP** 대화형 파일 전송 |
| **Plink** | 스크립트·자동화용 SSH 명령 |
| **Pageant** | SSH 에이전트 |

GUI로 파일 옮기려면 **WinSCP**·**FileZilla**(SFTP)를 같이 쓰는 경우도 많다.

---

## 8. PuTTY vs Windows `ssh`

| | PuTTY | OpenSSH (`ssh` in PowerShell) |
|--|-------|-------------------------------|
| UI | **GUI** 세션 목록 | 명령줄 |
| 키 형식 | **`.ppk`** (변환 필요) | `~/.ssh/id_ed25519` 등 |
| 탭·테마 | PuTTY 창 각각 | **Windows Terminal** 탭 |
| 시리얼·레거시 | **지원** | 별도 도구 |
| 스크립트 | Plink | `ssh` 그대로 |

새 PC라면 **OpenSSH + Windows Terminal**을 먼저 켜 보고, 세션 GUI·PPK·시리얼이 필요하면 PuTTY를 병행한다.

---

## 9. 보안·주의

| 주제 | 설명 |
|------|------|
| **호스트 키** | 지문이 **갑자기 바뀌면** 접속 중단·관리자 확인 |
| **root 직접 로그인** | 서버 정책상 막혀 있을 수 있음 — 일반 계정 + `sudo` |
| **공용 PC** | 세션·키·클립보드에 **민감 정보** 남기지 않기 |
| **비밀번호 저장** | PuTTY는 기본적으로 비밀번호를 세션에 **안전 저장하지 않음** (별도 도구 주의) |
| **방화벽** | 집·회사·카페 Wi-Fi에서 **22번 포트** 막힐 수 있음 |

서버 측 보안은 [[ISMS-P]]·운영 정책과 별개로, 클라이언트는 **키 관리**가 핵심이다.

---

## 10. 실전 체크

- [ ] Host·Port·**SSH** 선택했는가  
- [ ] 첫 접속 **호스트 키**를 확인했는가  
- [ ] 키 로그인이면 **Auth**에 `.ppk`가 연결됐는가  
- [ ] 자주 쓰는 접속을 **Saved Sessions**에 저장했는가  
- [ ] 끊김이 잦으면 **keepalive**를 넣었는가  
- [ ] 접속 후 [[리눅스 기본 명령어]]·`exit`로 **종료**하는 습관  

---

## 면책

> **면책**  
> PuTTY 버전·메뉴 이름·다운로드 URL은 **업데이트**될 수 있다. 공식 사이트가 최종본.  
> 원격 서버 접속·`root`·방화벽 변경은 **권한·정책**을 따른다. 이 글은 도구 설명이며 특정 제품 설치를 권유하지 않는다.

---

## 관련

- [[생활위키 목차]]
- [[윈도우 사용법]]
- [[리눅스]]
- [[리눅스 기본 명령어]]
- [[Ubuntu]]
- [[Termux 사용법]]
- [[Git 사용법]]
- [[GitHub]]
- [[DBeaver 사용법]]
- [[VS Code 사용법]]
- [[ISMS-P]]
