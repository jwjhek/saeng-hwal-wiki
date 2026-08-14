---
publish: true
draft: false
depth: article
aliases:
  - 퍼블릭 클라우드
  - AWS
  - GCP
  - Azure
---

# 클라우드 AWS GCP Azure

> **분류:** 개발 › 인프라 · [[생활위키 목차]]

**퍼블릭 클라우드**는 인터넷으로 빌려 쓰는 **서버·스토리지·DB·네트워크**다. 
대표 **3사**는 **AWS**(Amazon Web Services), **Microsoft Azure**, **GCP**(Google Cloud Platform)다.

일상의 **OneDrive·Google Drive** 같은 **파일 동기화**와는 겹치는 말이지만, 이 글은 **개발·운영 인프라**(VM·컨테이너·DB·API 호스팅) 쪽을 본다. 소비자 드라이브는 [[웹 드라이브 비교]].

확인일: 2026-08-12  
서비스 이름·요금·리전은 **수시로 바뀐다** — 각 공식 사이트가 최종본.

공식:

- AWS: [https://aws.amazon.com](https://aws.amazon.com)
- Azure: [https://azure.microsoft.com](https://azure.microsoft.com)
- GCP: [https://cloud.google.com](https://cloud.google.com)

관련: [[Docker 사용법]] · [[쿠버네티스]] · [[GitHub]] · [[ISMS-P]]

---

## 1. 개요

```text
[온프레미스] 회사 IDC에 서버·스토리지 직접 구매·운영
        ↓
[퍼블릭 클라우드] AWS·Azure·GCP에 VM·DB·스토리지를 분 단위·월 단위로 사용
        ↓
[컨테이너·K8s] 같은 클라우드 위에 Docker·쿠버네티스 올림
```

| 계층 | 의미 | 예 |
|------|------|-----|
| **IaaS** | 가상 서버·디스크·네트워크 | EC2, Azure VM, Compute Engine |
| **PaaS** | 앱만 올리고 OS·런타임은 플랫폼이 | App Service, Cloud Run, Elastic Beanstalk |
| **SaaS** | 완성된 앱 구독 | M365, Gmail — 이 글 범위 밖 |

**멀티 클라우드** — 한 조직이 AWS와 Azure를 같이 쓰기도 한다. **벤더 종속**을 줄이려는 전략과 **관리 복잡도**가 트레이드오프다.

---

## 2. 요약 비교

| | **AWS** | **Azure** | **GCP** |
|--|---------|-----------|---------|
| **운영** | Amazon | Microsoft | Google |
| **시장·생태** | 서비스 **종류·문서·사례**가 가장 넓은 편 | **Microsoft·Windows·AD·Office** 조직에 강함 | **데이터·AI·BigQuery·K8s 원조** 이미지 |
| **콘솔** | AWS Management Console | Azure Portal | Google Cloud Console |
| **CLI** | `aws` | `az` | `gcloud` |
| **기본 리전 예** | `ap-northeast-2`(서울) | `koreacentral` | `asia-northeast3`(서울) |
| **무료 체험** | Free Tier·크레딧 (조건별) | 무료 계정·크레딧 | Free Trial·Always Free 일부 |
| **한국 공공·SI** | 많이 씀 | M365·AD 연계 많음 | 분석·AI 프로젝트 |

「어느 게 무조건 1등」보다 **조직에 이미 있는 계약·기술 스택**이 선택에 크게 작용한다.

---

## 3. 서비스 대응 표

같은 역할, **이름만 다름**. 면접·아키텍처 그림에서 자주 나온다.

| 역할 | AWS | Azure | GCP |
|------|-----|-------|-----|
| **가상 서버** | EC2 | Virtual Machines | Compute Engine |
| **관리형 K8s** | **EKS** | **AKS** | **GKE** |
| **컨테이너(서버리스)** | Fargate | Container Apps | **Cloud Run** |
| **서버리스 함수** | **Lambda** | Azure Functions | Cloud Functions |
| **객체 스토리지** | **S3** | Blob Storage | Cloud Storage |
| **블록 디스크** | EBS | Managed Disks | Persistent Disk |
| **관계형 DB** | **RDS** | Azure SQL / Database for PostgreSQL | Cloud SQL |
| **NoSQL** | DynamoDB | Cosmos DB | Firestore / Bigtable |
| **메시지 큐** | SQS | Service Bus / Queue Storage | Pub/Sub |
| **CDN** | CloudFront | Azure CDN / Front Door | Cloud CDN |
| **DNS** | Route 53 | Azure DNS | Cloud DNS |
| **신원·권한** | **IAM** | Microsoft Entra ID + RBAC | IAM |
| **비밀 관리** | Secrets Manager | Key Vault | Secret Manager |
| **로그·모니터** | CloudWatch | Azure Monitor | Cloud Logging / Monitoring |
| **데이터 웨어하우스** | Redshift | Synapse | **BigQuery** |
| **정적 웹·CDN** | S3 + CloudFront | Static Web Apps + CDN | Firebase Hosting 등 |

[[쿠버네티스]]를 배우면 **EKS·AKS·GKE**가 같은 개념의 **관리형 클러스터**다.

---

## 4. AWS (Amazon Web Services)

### 4.1 특징

- **서비스 수·레퍼런스**가 많다. 튜토리얼·자격증(AWS Certified) 생태계가 크다.
- 글로벌 **리전·가용 영역(AZ)** 이 넓다.
- 스타트업부터 대기업까지 **범용** 인프라의 기본 이미지.

### 4.2 자주 쓰는 조합

```text
EC2 (또는 ECS/EKS) + RDS + S3 + CloudFront + IAM
```

- **S3** — 백업·정적 파일·로그 아카이브  
- **Lambda** — 이벤트·짧은 배치·API Gateway와 API  
- **VPC** — 사설 네트워크·서브넷·보안 그룹  

SSH 접속 사용자명은 AMI마다 다르다 (`ec2-user`, `ubuntu` 등) → [[PuTTY 사용법]].

### 4.3 주의

- IAM 정책·버킷 **퍼블릭 노출** 사고가 잦다 — 최소 권한·블록 퍼블릭 액세스.  
- 요금 항목이 많아 **Cost Explorer**·예산 알람을 초기에 켠다.

---

## 5. Azure (Microsoft Azure)

### 5.1 특징

- **Active Directory(Entra ID)·Office 365·Windows Server** 와 **단일 계정·하이브리드** 연동이 강점.
- **.NET·Windows** 워크로드, 기업 SSO가 이미 Microsoft면 진입 장벽이 낮다.
- **Azure OpenAI Service** — OpenAI 모델을 **Azure 계약·리전·규정** 안에서 쓰는 경로 → [[OpenAI Platform]]과 **엔드포인트·키가 다름**.

### 5.2 자주 쓰는 조합

```text
App Service / AKS + Azure SQL + Blob Storage + Key Vault
```

- **Resource Group** — 리소스를 묶는 논리 단위 (태그·권한·삭제 범위)  
- **Azure DevOps** — CI/CD (GitHub Actions와 병행도 흔함)  

### 5.3 주의

- 포털 메뉴·이름이 **자주 개편**된다. 공식 문서 버전을 맞춘다.  
- 하이브리드(온프레 + Azure)는 **ExpressRoute·VPN** 설계가 필요할 수 있다.

---

## 6. GCP (Google Cloud Platform)

### 6.1 특징

- **Kubernetes(GKE)·컨테이너·데이터 분석(BigQuery)** 에 강한 이미지.
- Google Workspace·Analytics·YouTube 등과 **데이터 파이프라인** 연계 사례.
- **Cloud Run** — 컨테이너를 서버 관리 거의 없이 HTTP로 — 프로토타입에 빠른 편.

### 6.2 자주 쓰는 조합

```text
GKE (또는 Cloud Run) + Cloud SQL + Cloud Storage + IAM
```

- **BigQuery** — 서버리스 DW·로그·BI  
- **Vertex AI** — Google 쪽 ML·생성형 플랫폼 (OpenAI API와 별 제품)  

### 6.3 주의

- 프로젝트·폴더·조직 **계층**을 처음에 정리하지 않으면 권한이 꼬이기 쉽다.  
- AWS 대비 한국 SI 레퍼런스는 조직마다 다르다 — 팀 경험을 본다.

---

## 7. 국내·기타

| 제공자 | 메모 |
|--------|------|
| **Naver Cloud Platform(NCP)** | 국내 리전·공공·게임·SI에서 종종 |
| **Kakao i Cloud** | 카카오 계열·국내 규제 |
| **Oracle Cloud(OCI)** | Oracle DB 워크로드·특가 마케팅 |
| **Alibaba Cloud** | 아시아·중국 연계 |

법·개인정보 **국내 저장** 요건이 있으면 **리전·계약·ISMS**를 같이 본다 → [[ISMS-P]].

---

## 8. 이 위키에서 이어지는 글

| 목적 | 흔한 경로 |
|------|-----------|
| **정적 위키** | [[GitHub]] Pages (클라우드 VM 없이) — [[Quartz 사용법]] |
| **컨테이너 앱** | 로컬 [[Docker 사용법]] → 이미지를 ECR/ACR/GCR에 push → EKS/AKS/GKE |
| **CI/CD** | [[GitHub]] Actions가 세 클라우드에 **배포** |
| **DB 튜닝** | RDS·Cloud SQL·Azure SQL 위 Oracle/PostgreSQL — [[Oracle DB와 튜닝]] |
| **AI API** | OpenAI Platform 직접 vs **Azure OpenAI** |

「클라우드 = AWS」만 알아도 되지만, **M365 회사**는 Azure, **데이터·GKE** 팀은 GCP를 만날 수 있다.

---

## 9. 고르는 기준

| 상황 | 힌트 |
|------|------|
| 팀이 **이미 AWS** 표준 | EC2·EKS·RDS 축 유지 |
| **AD·M365·.NET** 중심 | Azure 우선 검토 |
| **K8s·BigQuery·Cloud Run** | GCP 검토 |
| **OpenAI를 기업 계약**으로 | Azure OpenAI vs OpenAI Platform 비교 |
| **개인·소규모** | GitHub Pages·Railway 등 **관리형 PaaS**도 후보 — VM 풀셋업은 나중에 |
| **규제·공공** | 지정 클라우드·국내 리전·[[ISMS-P]] 요구 |

---

## 10. 시작 순서 (공통)

1. **계정** 생성 — 결제 수단·**예산 알람** 설정  
2. **리전** 선택 — `서울`/`koreacentral`/`asia-northeast3` 등 **지연·규정**  
3. **IAM** — 루트 계정 일상 사용 금지, **역할·최소 권한** 사용자  
4. **VPC/VNet** — 공인 IP·보안 그룹·SSH 키  
5. **VM 1대** 또는 **관리형 K8s** 체험  
6. [[Docker 사용법]] 이미지 배포 → 로드밸런서·도메인  

무료 티어는 **기간·용량·서비스 제한**이 있다. 방치된 VM·공인 IP가 **요금 폭탄**의 흔한 원인이다.

---

## 11. 비용·보안

| 주제 | 팁 |
|------|-----|
| **과금** | 컴퓨트·스토리지·전송(egress)·API 호출이 **따로** 잡힌다 |
| **예산** | Billing Alert·태그로 팀·프로젝트 분리 |
| **키** | Access Key를 git·프론트에 넣지 않음 — [[GitHub]] Secrets |
| **네트워크** | 0.0.0.0/0 SSH·DB 포트 개방 금지 |
| **백업** | 스냅샷·다중 AZ — 클라우드 ≠ 자동 백업 |
| **인증** | [[ISMS-P]]·개인정보 처리 시 **접근 로그·암호화** 요구 |

---

## 12. 흔한 실수

| 실수 | 현실 |
|------|------|
| 루트 계정으로 매일 작업 | IAM 사용자·역할 분리 |
| 리전 잘못 선택 | 서울 사용자인데 미국 리전만 생성 |
| 보안 그룹 전체 개방 | IP·포트 최소화 |
| 학습 VM 방치 | 종료·스냅샷 삭제·예산 알람 |
| S3/Blob **퍼블릭** 설정 | 민감 데이터 유출 |
| 클라우드 = 백업 완료 | 3-2-1·오프라인 복사는 별도 ([[웹 드라이브 비교]] §백업) |

---

## 13. 정리

1. **AWS·Azure·GCP** = 퍼블릭 **IaaS/PaaS** 3강.  
2. **EC2 / VM / Compute Engine**, **EKS / AKS / GKE**, **S3 / Blob / GCS** 식으로 **역할은 같고 이름만 다름**.  
3. **Azure**는 Microsoft 스택, **GCP**는 데이터·K8s, **AWS**는 범용·레퍼런스 많음.  
4. [[Docker 사용법]]·[[쿠버네티스]]·[[GitHub]] Actions와 **바로 이어진다**.  
5. 소비자 **드라이브**와 구분 — [[웹 드라이브 비교]].

---

## 면책

> **면책**  
> 요금·리전·규정·무료 티어는 **제공자 약관**이 최종본이다.  
> 이 글은 **기술 학습·선택 참고**이며 특정 클라우드 가입·이전을 권하지 않는다.  
> 공공·금융·의료는 **별도 컴플라이언스** 검토가 필요하다.

---

## 관련

- [[Docker 사용법]] — 이미지·컨테이너
- [[쿠버네티스]] — EKS·AKS·GKE
- [[GitHub]] — Actions·Pages·Codespaces
- [[GitLab]] — 셀프호스트·MR·CI
- [[ISMS-P]] — 인증·관리체계
- [[OpenAI Platform]] · [[OpenAI STT]] — Azure OpenAI와 구분
- [[웹 드라이브 비교]] — 소비자 클라우드 드라이브
- [[전자정부프레임워크]] — 공공 SI (온프레·클라우드 혼재)
- [[PuTTY 사용법]] — VM SSH
- [[생활위키 목차]]
