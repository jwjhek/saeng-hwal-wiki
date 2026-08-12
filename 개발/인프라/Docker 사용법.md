---
publish: true
draft: false
---

# Docker 사용법

> **분류:** 개발 › 인프라 · [[생활위키 목차]]

Docker는 앱과 실행에 필요한 환경(라이브러리·설정)을 **이미지**로 묶고, **컨테이너**로 동일하게 돌리게 해 주는 도구다. 
“내 PC에선 되는데 서버에선 안 돼”를 줄이는 게 핵심이다.

공식: [https://www.docker.com](https://www.docker.com) 
문서: [https://docs.docker.com](https://docs.docker.com)

확인일: 2026-08-06 
Windows에서는 보통 **Docker Desktop** + (권장) **WSL2** 백엔드.

---

## 1. 쓰는 이유

| 문제 | Docker로 |
|------|----------|
| 개발자마다 Java/Node/DB 버전 다름 | 같은 이미지로 맞춤 |
| 로컬에 DB·Redis 설치 부담 | `docker run` / Compose로 띄움 |
| 배포 환경 재현 | 이미지 태그를 서버에 그대로 |
| 마이크로서비스 여러 개 | 네트워크로 컨테이너 연결 |

가상머신(VM)과 비교:

```text
VM = 하드웨어 가상화 + 게스트 OS 통째
컨테이너 = 호스트 커널 공유 + 프로세스 격리 (더 가볍고 빠름)
```

---

## 2. 핵심 용어

| 용어 | 의미 |
|------|------|
| **이미지 (Image)** | 읽기 전용 템플릿. 계층(layer)으로 구성 |
| **컨테이너 (Container)** | 이미지로 만든 실행 중인(또는 중지된) 인스턴스 |
| **Dockerfile** | 이미지를 만드는 레시피 |
| **레지스트리** | 이미지 저장소 (Docker Hub, GHCR, 사내 Harbor 등) |
| **태그** | `nginx:1.27`, `myapp:1.0.3` — 버전 이름 |
| **볼륨 (Volume)** | 컨테이너를 지워도 남길 데이터 |
| **네트워크** | 컨테이너끼리 이름으로 통신 |
| **Compose** | 여러 컨테이너를 YAML 한 파일로 정의·실행 |

```text
Dockerfile → docker build → Image → docker run → Container
 ↑
 docker pull (레지스트리)
```

---

## 3. 설치 (Windows)

1. [Docker Desktop](https://www.docker.com/products/docker-desktop/) 설치 
2. **WSL2** 엔진 사용 권장 (설정에서 확인) 
3. 설치 후 터미널:

```powershell
docker version
docker run hello-world
```

요구: 가상화(BIOS), WSL2, 충분한 RAM. 
회사 PC는 라이선스·보안 정책을 확인한다.

Linux/macOS는 네이티브 또는 Desktop. 명령은 대체로 같다.

---

## 4. 일상 명령어

### 이미지

```bash
docker pull nginx:alpine # 받기
docker images # 목록 (또는 docker image ls)
docker rmi nginx:alpine # 삭제
docker build -t myapp:1.0 . # Dockerfile로 빌드
```

### 컨테이너

```bash
docker run -d --name web -p 8080:80 nginx:alpine
# -d 백그라운드, -p 호스트:컨테이너 포트, --name 이름

docker ps # 실행 중
docker ps -a # 중지 포함
docker logs -f web # 로그
docker exec -it web sh # 컨테이너 안 셸 (bash 없으면 sh)
docker stop web
docker start web
docker rm web # 삭제 (중지 후)
docker rm -f web # 강제
```

### 정리

```bash
docker system df # 용량
docker system prune # 안 쓰는 것 정리 (주의)
docker volume prune
```

---

## 5. Dockerfile 기초

```dockerfile
# 예: 간단한 Python API
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

| 지시어 | 역할 |
|--------|------|
| `FROM` | 베이스 이미지 |
| `WORKDIR` | 작업 디렉터리 |
| `COPY` / `ADD` | 파일 복사 (`COPY` 권장) |
| `RUN` | 빌드 중 명령 (패키지 설치) |
| `ENV` | 환경변수 |
| `EXPOSE` | 문서용 포트 표시 (실제 공개는 `-p`) |
| `CMD` / `ENTRYPOINT` | 컨테이너 시작 명령 |

빌드:

```bash
docker build -t myapi:1.0 .
docker run --rm -p 8000:8000 myapi:1.0
```

### 잘 쓰는 습관

1. **작은 베이스** (`-slim`, `-alpine`) — 단, alpine은 libc 이슈 있을 수 있음 
2. **레이어 캐시**: 자주 안 바뀌는 `requirements.txt`를 코드보다 먼저 COPY 
3. **`.dockerignore`**: `.git`, `.venv`, `__pycache__`, `node_modules` 
4. **root 비권장**: 가능하면 비root USER 
5. **시크릿을 이미지에 넣지 말 것** — 빌드 인자·레이어에 남음 
6. 멀티 스테이지 빌드: 빌드 도구와 런타임을 분리해 최종 이미지 축소 

```dockerfile
FROM golang:1.22 AS build
WORKDIR /src
COPY . .
RUN CGO_ENABLED=0 go build -o /out/app

FROM gcr.io/distroless/static
COPY --from=build /out/app /app
ENTRYPOINT ["/app"]
```

---

## 6. 볼륨·포트·환경변수

### 포트

```bash
docker run -p 5432:5432 postgres:16
# 호스트 5432 → 컨테이너 5432
```

### 환경변수

```bash
docker run -e POSTGRES_PASSWORD=secret postgres:16
# 또는 --env-file .env
```

### 볼륨 (데이터 유지)

```bash
docker volume create pgdata
docker run -d --name pg \
 -e POSTGRES_PASSWORD=secret \
 -v pgdata:/var/lib/postgresql/data \
 postgres:16
```

바인드 마운트 (호스트 폴더):

```bash
docker run -v ${PWD}:/app -w /app node:22 npm test
```

Windows 경로·권한은 WSL 쪽 프로젝트 경로(`\\wsl$\...` / WSL 터미널)가 덜 까다로운 경우가 많다.

---

## 7. Docker Compose

여러 서비스(앱 + DB + Redis)를 한번에.

`compose.yaml` (또는 `docker-compose.yml`):

```yaml
services:
 db:
 image: postgres:16-alpine
 environment:
 POSTGRES_PASSWORD: secret
 POSTGRES_DB: app
 volumes:
 - pgdata:/var/lib/postgresql/data
 ports:
 - "5432:5432"

 api:
 build: .
 ports:
 - "8000:8000"
 environment:
 DATABASE_URL: postgres://postgres:secret@db:5432/app
 depends_on:
 - db

volumes:
 pgdata:
```

```bash
docker compose up -d # 빌드+백그라운드
docker compose ps
docker compose logs -f api
docker compose down # 중지·네트워크 제거
docker compose down -v # 볼륨까지 삭제 (데이터 삭제 주의)
```

같은 Compose 네트워크 안에서는 서비스 이름(`db`)이 호스트명이 된다.

---

## 8. 네트워크

```bash
docker network ls
docker network create appnet
docker run -d --name redis --network appnet redis:alpine
docker run -it --network appnet nicolaka/netshoot ping redis
```

Compose는 프로젝트용 네트워크를 자동 생성한다. 
`localhost`는 **컨테이너 자신**이다. 호스트의 DB에 붙을 때는 `host.docker.internal`(Desktop) 등을 쓴다.

---

## 9. 개발 워크플로 예

### DB만 컨테이너

앱은 로컬 IDEA/VS Code, DB만 Docker:

```bash
docker compose up -d db
# localhost:5432 로 접속
```

### 풀 스택 Compose

프론트·API·DB 전부 Compose. 팀원에게 `docker compose up`만 안내.

### 앱 이미지 배포

```bash
docker build -t ghcr.io/org/myapi:1.0.3 .
docker push ghcr.io/org/myapi:1.0.3
# 서버에서 pull && run 또는 k8s/compose
```

CI에서 빌드·스캔(Trivy 등)·푸시가 일반적이다.

---

## 10. Spring · Python과의 연결

| 스택 | 전형 |
|------|------|
| [[Spring과 Spring Boot 학습\|Spring Boot]] | `Dockerfile` + jre 슬림, Compose에 Oracle/Postgres |
| [[Python 학습과 패키지\|Python]] / FastAPI | slim 이미지 + `requirements.txt`, Compose에 DB |
| [[전자정부프레임워크\|eGov]] | 로컬 WAS·DB를 Compose로 맞춰 버전 통일 |
| [[Oracle DB와 튜닝\|Oracle]] | 공식/커뮤니티 이미지를 쓸지는 라이선스·리소스 확인 |

개발은 [[Cursor 사용법\|Cursor]] / [[VS Code 사용법\|VS Code]]의 Dev Containers로 “폴더 = 컨테이너” 개발도 가능.

---

## 11. 보안·운영 체크

1. **latest 태그 의존 말기** — 재현 가능한 버전 핀 
2. 이미지·의존성 **CVE 스캔** 
3. 컨테이너에 SSH·불필요 포트를 열지 않기 
4. 시크릿은 환경변수·비밀 관리자 (이미지·git 금지) 
5. 읽기 전용 루트 파일시스템, drop capabilities (심화) 
6. 로그는 stdout → 수집 스택으로 
7. 헬스체크: `HEALTHCHECK` 또는 Compose `healthcheck` 
8. 프로덕션 오케스트레이션은 **Kubernetes / Swarm / Nomad** 등으로 넘어가는 경우가 많음 (Docker는 빌드·런타임 단위) → [[쿠버네티스]]

---

## 12. 자주 하는 실수

| 실수 | 결과 / 대안 |
|------|-------------|
| 데이터 볼륨 없이 DB 사용 | `docker rm` 시 데이터 증발 |
| `-p` 없이 포트 기대 | 호스트에서 접속 안 됨 |
| 컨테이너 안 `localhost`로 형제 DB | 서비스 이름 사용 |
| 거대 컨텍스트 빌드 | `.dockerignore` |
| Windows 경로 마운트 이슈 | WSL2 파일시스템에서 작업 |
| root + 취약 베이스 | 슬림·비root·패치 |
| 한 컨테이너에 웹+DB+SSH 전부 | 프로세스 하나(또는 역할 하나) 권장 |

---

## 13. 치트시트

```bash
docker run -d --name N -p H:C -e K=V -v VOL:/path IMAGE
docker build -t NAME:TAG .
docker compose up -d --build
docker compose down
docker logs -f N
docker exec -it N sh
docker system prune
```

```dockerfile
FROM … WORKDIR … COPY … RUN …
ENV … EXPOSE … USER … CMD …
```

---

## 14. 학습 순서

1. `hello-world`, `nginx` run · 포트 매핑 
2. `exec`로 들어가 보기 · logs 
3. Dockerfile로 자기 앱 이미지화 
4. Compose로 앱+DB 
5. 볼륨·네트워크·`.dockerignore` 
6. (다음) 멀티 스테이지, CI 푸시, [[쿠버네티스]] 입문 

---

## 관련

- [[생활위키 목차]]
- [[쿠버네티스]]
- [[클라우드 AWS GCP Azure]]
- [[Git 사용법]]
- [[GitHub]]
- [[GitLab]]
- [[Python 학습과 패키지]]
- [[Spring과 Spring Boot 학습]]
- [[Oracle DB와 튜닝]]
- [[DBeaver 사용법]] — 컨테이너 DB에 GUI 접속
- [[VS Code 사용법]]
- [[Cursor 사용법]]
