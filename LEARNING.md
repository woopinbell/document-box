# LEARNING.md — 학습 실행 가이드 (각 프로젝트를 실제로 어떻게 도는가)

> 자기완결 문서. **[SEQUENCE.md](SEQUENCE.md)의 짝**이다.
> - `SEQUENCE.md` = **무엇을, 어떤 순서로** 켜는가 (글로벌 라우팅 + 모듈 내부 읽기 순서).
> - `LEARNING.md` = **각 단위를 어떻게 도는가** (로컬 실행: 노트 정독 → reference-impl → 커밋 재구성 → 복기 → 회고).
>
> SEQUENCE에서 경로를 골랐다면(기본 = 경로 A), **이 문서의 보편 루프(§3)로 그 경로의 프로젝트를 하나씩 돈다.** 방법은 경로와 무관하며, 본 문서는 기본 경로 A(`linux-admin → backend-foundations → backend-reliability → container-stack → sportsbook`)를 관통 예시로 쓴다.
>
> 전제: `notes/`(19개 프로젝트 139개 대장 가이드 + reference-impl)와 `docs/commits/`(커밋별 문서 + L3/L2/L1 색인)는 이미 작성돼 있다. 이 문서는 그것들을 **재작성하지 않고 활용하는 방법**만 고정한다.

---

## 0. 이 문서의 위치 — SEQUENCE 연동 지도

| 필요한 판단 | SEQUENCE (무엇/순서) | LEARNING (어떻게) |
|---|---|---|
| 어떤 프로젝트를 할까 | §1 모듈 카탈로그 · §3 경로 프리셋 | — |
| 이 프로젝트가 여는 스택·대장은? | §1, §5 스택별 대장 | §3 Step 0 |
| 노트를 어떤 순서로 읽나 | §4 가이드 읽기 순서 | §3 Step 1 |
| 노트·커밋·복기를 실제로 어떻게 | — | **§3 보편 루프** |
| 모듈마다 루프가 어떻게 바뀌나 | §1 (생략 가능/선행) | §4 모듈별 변주 |
| 캡스톤은 어떻게 | §6 캡스톤 진입 체크 | §5 캡스톤 운영 |

한 줄 요약: **SEQUENCE에서 "다음 프로젝트"를 정하고 → 여기 §3 루프로 돌리고 → §6 기준으로 닫는다.**

---

## 1. 학습 철학 — 3원칙

이 3원칙이 본 문서 모든 절차의 근거다. (그리고 이 철학은 이미 커밋 문서의 **L3/L2/L1**로 항목 단위 실체화돼 있다 — §2 참조.)

1. **재유도 > 암송.** 학습됐다는 테스트는 "코드를 떠올리나"가 아니라 **"빈 파일에서 같은 결정을 같은 이유로 다시 만들 수 있나"**다. 노트·커밋을 *다시 읽는* 것보다, 덮고 *재구성하다 막히는 곳만 펼치는* 것이 몇 배 강하다.
2. **빈도가 자동화를 깎는다.** 외우려 하지 마라. 자동화(0초 인출)는 노력의 대상이 아니라 *반복 사용의 결과*다. 네 일은 플래시카드가 아니라 **반복 인출 상황(=직접 만들기)을 세팅**하는 것.
3. **폭발 반경 큰 것만 과투자.** 동시성·트랜잭션·보안·돈 계산은 검색으로 못 빠져나온다(새벽 3시의 레이스 컨디션). 참조 없이 추론될 때까지 의도적으로 판다. 나머지는 빈도에 맡긴다.

보조: 사실이 아니라 **패턴(청크)**을 모은다("이건 생산자-소비자 문제네" 하면 해법 형태가 통째로 딸려오게). "찾아봐도 되는 것"은 내재화 말고 **색인만**(무엇이 존재하는지 알면 검색할 수 있다).

---

## 2. 한 프로젝트의 해부학 — 아티팩트 지도

학습 프로젝트 한 개는 보편적으로 이 구조다(캡스톤 sportsbook은 §5의 별구조).

```
<project>/
├─ notes/                     ← ① 스택 가이드 (선행 정독, 깊게)
│   ├─ <stack>.md  (4부 포맷)
│   └─ reference-impl/<stack>/ ← ② 짝 실행체
├─ src·spring-main·go-sub…    ← 본 프로젝트 코드 (정답지)
└─ docs/
    ├─ commits/  000.md…N.md  ← ③ 재구성 시퀀스 (각 끝에 L3/L2/L1)
    ├─ notes/    backend·systems·infra·reliability/  ← ④ 온디맨드 어휘 (얕게, 막힐 때만)
    └─ reflection/  failure-modes·change-cost·retrospective  ← ⑤ 회고
```

| # | 아티팩트 | 무엇 | 학습 모드 |
|---|---|---|---|
| ① | 루트 `notes/<stack>.md` | 스택 1개당 1노트. **4부 포맷**(Part1 개념·멘탈모델 → Part2 본 프로젝트 코드 분석 → Part3 학습용 미니프로젝트 → Part4 심화). C·Java·프론트 가로질러 균일. | **선행 정독.** 대장-first(SEQUENCE §5). |
| ② | `notes/reference-impl/<stack>/` | 노트와 짝으로 도는 실행 가능한 최소 구현체. | 빌드·실행하며 **손에 익힘**. |
| ③ | `docs/commits/000.md…N.md` | 비-merge 커밋 1개당 1문서. 번호=히스토리 위치(merge 경계 번호는 **결번**). | **재구성 시퀀스**(§3 Step 2). |
| — | 각 커밋 끝 `## 기억/설명 Level` | **L3/L2/L1 복기 색인.** 본문 요약이 아니라 우선순위 인덱스. 거의 모든 커밋 문서에 있음. | **복기 필터**(§3 Step 4). |
| ④ | `docs/notes/<cat>/` | 언어·프레임워크 **개념 어휘**(Spring MVC, JPA, mutex…). 일부 프로젝트만 보유. | **온디맨드.** 처음부터 읽지 말 것 — 커밋 따라가다 막힐 때만 꺼냄. |
| ⑤ | `docs/reflection/` | 회고·실패 시나리오·변경 비용 시뮬레이션. | 마무리 단계. |

**두 층 노트를 혼동하지 말 것.** ①루트 `notes/`는 *깊게 선행 정독*하는 스택 가이드, ④`docs/notes/`는 *얕게 온디맨드*로 꺼내는 어휘 노트다. 모드가 정반대다.

**L3/L2/L1 정의** (출처: 각 프로젝트 `docs/commits/README.md`, 원문 그대로):

- **L3 — 백지 설명 대상**: 문서 없이 구조·흐름·설계 결정·핵심 제약을 설명하거나 그릴 수 있어야 하는 항목.
- **L2 — 코드/문서 기반 설명 대상**: 소스나 커밋 문서를 보며 연결 관계·구현 흐름·예외 처리·책임 분리를 설명할 수 있어야 하는 항목.
- **L1 — 읽고 파악하면 충분한 대상**: 깊게 외우지 않고 필요할 때 문서·코드를 읽어 의도와 역할을 파악하면 되는 항목.
- **L0**: 포맷팅·단순 정리·자동 생성물. 보통 문서화하지 않음.

> **연결**: §1의 "재유도/빈도/폭발 반경"이 곧 L3(반드시 내재화)·L2(펼쳐서)·L1(찾아봐도 됨)이다. 즉 "암기냐 이해냐"는 전역으로 안 나뉘지만, **이 커밋의 이 항목**은 L 등급으로 국소적으로 나뉜다.

---

## 3. 보편 루프 (The Loop) — 프로젝트 1개 도는 법

문서의 심장. SEQUENCE에서 정한 "다음 프로젝트"에 대해 Step 0→5를 돈다.

### Step 0 — 진입 판별
SEQUENCE §1(모듈)·§5(스택별 대장)에서 이 프로젝트가 **여는 스택**과 **대장/곁가지** 여부를 확인한다. 대장이면 두껍게 정면, 곁가지면 자기 파트만 빠르게.

### Step 1 — 스택 선행 (notes 정독)
루트 `notes/`를 SEQUENCE §4의 순서대로, 대장-first로 **4부 정독**한다. 그다음 짝 `reference-impl/<stack>/`를 **빌드·실행**해 손에 익힌다. (곁가지는 공유 스택을 재기술하지 않으니 자기 노트만 빠르게.)

### Step 2 — 재구성 ★핵심
`docs/commits/`를 `000.md`부터 번호순으로(결번=merge, 건너뜀) 따라가되, **베끼지 말고 덮고 직접 만든다.** 커밋 리듬은 레포 형태에 따라 둘 중 하나다 — 커밋 문서 제목을 보면 바로 구분된다:

- **(2A) exercise형 — "…문제 계약 / 구현 / 테스트" triplet** (예: `backend-foundations-training`. 제목에 "문제 계약"이 보이면 이 형):
  1. **계약 문서**(문제 계약)를 읽는다.
  2. **여기서 멈추고 정답지를 덮는다. 계약만 보고 직접 구현한다.** ← 재유도 엔진.
  3. **구현 문서**를 펼쳐 내 코드와 diff한다. 다른 결정을 했으면 *왜* 다른지 따진다.
  4. **테스트 문서**로 검증 모델을 익힌다.

- **(2B) build형 — 순차 기능 커밋** (대부분: `small-shell`·`container-stack`·`irc-relay-server`·`pong-pong`·`stack-sort`·`linux-admin` 등. 제목이 기능/컴포넌트 이름):
  1. 커밋 문서의 **제목과 본문 첫머리(문제 정의)**만 읽어 *이번 증분의 목표*를 잡는다.
  2. **덮고**, 직전 상태에서 그 목표까지 **직접 구현**한다.
  3. 커밋 문서 본문·원본과 **대조**한다.

어느 형이든 `git show <커밋>` (또는 `git log --oneline`)으로 **원본 커밋 diff와 내 재구성을 대조**할 수 있다. 완성 레포 = 답안지, `commits/` = 풀이 순서, 너 = 답 보기 전에 직접 푸는 사람.

### Step 3 — 온디맨드 어휘
Step 2에서 어휘가 막히면 그때만 `docs/notes/`의 해당 개념 노트(또는 루트 notes의 Part 1)를 꺼내 읽고 → **커밋으로 복귀**. 처음부터 docs/notes를 통독하지 않는다.

### Step 4 — 복기 (L3/L2/L1 필터)
각 커밋 문서 끝 `## 기억/설명 Level`을 **공부 필터**로 쓴다(본문 요약 아님):
- **L3** → 문서 덮고 **백지 설명/작도**. 막히면 그 항목은 아직 안 된 것.
- **L2** → 소스·문서를 **펼쳐서** 연결·흐름·예외·책임 분리 설명.
- **L1** → 스킵(필요 시 재독).

### Step 5 — 회고·검증으로 닫기
`docs/reflection/`(failure-modes·change-cost·retrospective)을 읽거나 직접 채운다. 그리고 §6의 완료 기준(exercise Completion Criteria + `scripts/checkdocs` 등)으로 단위를 닫는다.

> **⛔ 안티패턴**: `000→N`을 소설처럼 읽고 코드를 베껴 쓰기. 수동 전사는 가장 약한 학습이며 §1의 재유도 원칙을 정면 위배한다. triplet/순차 구조는 *베끼지 못하게* 일부러 만든 것이다 — 반드시 **덮고 먼저 시도**한다.

---

## 4. 모듈별 변주 — SEQUENCE §1 모듈에 루프 맞추기

루프(§3)는 동일하고, 모듈마다 **무엇이 대장·어디가 L3(폭발 반경)·어떤 구조 변형**인지만 조정한다.

| 모듈 (SEQUENCE §1) | 대장 | 커밋 리듬 | 구조 변형 | L3 집중처(폭발 반경) |
|---|---|---|---|---|
| **M0 작업규율** | linux-admin | 순차(2B) | 표준 | 가벼움(Git 흐름·문서 검증) |
| **JVM 백엔드 ★** | backend-foundations(→reliability) | **triplet(2A)** | 표준(docs/notes 보유) | **트랜잭션·동시성·security** → 2회독 |
| **인프라/운영** | container-stack | 순차(2B) | 표준 | Compose 네트워킹·nginx·DB 초기화 |
| **C 트랙** | small-shell | 순차(2B) | **docs/notes 없음**(루트 notes+commits만) | **메모리·프로세스·시그널/IPC·pthread** |
| **C++ 트랙** | stl-container | 순차(2B) | ray-scene-tracer는 **reference-impl 없음**(핸즈온) | 템플릿·allocator·iterator·예외 안전 |
| **시스템 서버** | game-server-reliability | 순차(2B) | — | **소켓(epoll/kqueue)·동시성**; C++ 98→17→20 점프는 SEQUENCE 로컬 경사 대안 따름 |
| **Node/TS 백엔드** | grounded-travel | 순차(2B) | 표준 | TS 타입 경계·WebSocket·트랜잭션 |
| **프론트엔드** | frontend-reliability | **triplet(2A)** 경향 | 표준 | RSC 경계·데이터 패칭·상태 소유권 |
| **모바일** | mobile-reliability(→곁가지 foundations) | foundations=순차(2B)/reliability=**triplet(2A)** 경향 | 표준(docs/notes 보유) | **구조적 동시성·StateFlow 상태소유권·오프라인 캐시 정합성·토큰 refresh 레이스·WebSocket 재연결+멱등** |

> **docs/notes 없는 프로젝트**: format-printer · signal-message-bus · stack-sort · stl-container · game-server-foundations-training → §3 Step 3에서 루트 notes Part 1로 대체.
> **reference-impl 없는(핸즈온) 프로젝트**: network-routing-notes · ray-scene-tracer (SEQUENCE가 "노트 없음/얕음"으로 표기) → §3 Step 1을 개념 학습 + 직접 구현으로.
> **모바일 모듈 상세**: 스택·notes 목록·트랙·캡스톤 API 계약은 [mobile-track.md](mobile-track.md)에 정본으로 있다. foundations=앱빌드 기본기(순차 2B), reliability=신뢰성 대장(triplet 경향), 캡스톤(sportsbook/mobile-client)=§3 루프 + 종합 적용(페어 notes 재사용) + 신규 클라이언트 통합 노트 2~3개. (경로 E = SEQUENCE §3.)

### 경로 A 관통 예시 (각 단계에 §3 루프 적용)

1. **linux-admin** (M0): Step1 git-cli·commits·markdown 정독 → Step2 순차(2B)로 hardening·체크포인트 재구성 → Step4 L3 가볍게.
2. **backend-foundations** (JVM 대장): Step1 java-21→spring-boot→…→testcontainers 정독 + reference-impl → Step2 **triplet(2A)**: 계약 덮고 컨트롤러/서비스 직접 구현→대조→테스트 → Step4 트랜잭션·security L3 백지.
3. **backend-reliability** (JVM 곁가지): Step1 jpa·redis·go 노트만 빠르게 → Step2 triplet → Step4 동시성·롤백 경계 L3.
4. **container-stack** (인프라 대장): Step1 docker·compose·nginx 노트 + reference-impl 실행 → Step2 **순차(2B)**: 이미지·풀·DB 초기화 증분 직접 구성 → Step3 막히면 docs/notes.
5. **sportsbook** (캡스톤): §5로 진입.

---

## 5. 캡스톤 운영 — sportsbook (SEQUENCE §6 연동)

**진입 체크**: JVM 백엔드(backend-foundations·reliability) + 인프라(container-stack) 완료 시 자연스럽다.

sportsbook은 9개 레포(서비스 7 + gateway + orchestration)로, **두 갈래**로 돈다:

- **(A) 코어 = 종합 적용.** 각 서비스(`betting-service`·`wallet-service`·`settlement-service`·`risk-service`·`odds-feed-service`·`admin-api`·`shared-protocol`)는 자기 `docs/commits/`를 가진다 → **§3 루프 그대로** 재구성. in-process Spring 코어(web·JPA·Redis·validation·security 기본·test)는 **기존 139개 노트 재사용**으로 충당("종합 적용", 신규 학습 아님).
- **(B) 신규 = 분산·운영 스택.** sportsbook을 분산 시스템으로 만드는 횡단 계층은 139개에 없다. `sportsbook/orchestration/notes/`의 **Tier-1 노트 8개**(4부 포맷 + reference-impl)를 SEQUENCE §6 순서로 정독(=§3 Step 1):

  `maven → spring-kafka → avro → flyway → resilience4j(+bucket4j) → spring-cloud-gateway → oauth2-resource-server → observability`
  (빌드 → 이벤트 → 데이터 → 복원력 → 보안 → 게이트웨이 → 관측성)

**보조 자원**: `orchestration/docs/architecture/decisions`(ADR — 설계 결정 근거), `orchestration/chaos/`·`e2e/`·`observability/`(복원력·통합·관측 실습).

**출구**: 9개 레포 통합 동작 확인 → GitHub push (커리어 산출물).

---

## 6. 진행 추적 & 완료 기준

**한 단위(커밋/exercise)의 "완료" 정의** — 셋을 모두 만족:
1. 해당 exercise의 **Completion Criteria** 충족 (각 exercise README 기준).
2. **검증 스크립트 통과**: `scripts/checkdocs/`·`Makefile` 검증 명령·CI(있는 경우).
3. 그 단위의 **L3 항목 백지 설명 통과** (§3 Step 4).

**프로젝트의 "완료"**: 모든 비-merge 커밋을 §3 루프로 돌았고, 그 프로젝트의 L3 집합을 백지로 설명할 수 있다.

**경로 A 체크리스트 틀**:

```
[ ] M0  linux-admin            (Step1✓ Step2✓ L3✓)
[ ] JVM backend-foundations    (트랜잭션·security L3 백지 통과?)
[ ] JVM backend-reliability    (동시성·롤백 L3 백지 통과?)
[ ] INF container-stack        (Compose 기동·DB 초기화 재현?)
[ ] CAP sportsbook 코어(9서비스 §3) + Tier-1 8노트 + 9레포 통합·push
```

**면접 대비**: 전 프로젝트의 **L3 항목만 모아** 백지 설명 세트를 만든다. L3는 "문서 없이 설명·작도"가 기준이므로, 그 자체가 면접 답안의 골격이다. L2는 코드를 열고 설명하는 연습으로 보조. **산출물: [INTERVIEW.md](INTERVIEW.md)** (주제별 코어 세트 + 레포별 전체 L3 색인 — 답지 L3가 정본, 그 파일은 파생 색인).

---

> 요약 한 줄: **SEQUENCE에서 경로를 고르고(무엇/순서) → 각 프로젝트를 §3 루프로 돌리고(계약/목표 덮고 직접 재구성 → 막히면 온디맨드 → L3 백지 복기) → §6으로 닫는다.**
