# WORKSPACE.md — 코퍼스 사용 설명서 (처음 들어온 사람용 정본)

> **한 줄**: `~/Desktop/seungwoo`는 스택(Spring·React·Android·RAG…)을 **직접 재구성하며** 익힌
> ~40개 독립 레포의 학습 포트폴리오다. 각 레포는 그 과정을 정해진 형태의 문서로 남긴다.
>
> **처음이라면**: ① 이 문서로 *전체 지도*를 잡고 → ② 학습은 [STUDY.md](STUDY.md) **하나로 끝**(전
> 분야·순서·완주). 전체 문서 색인은 [README](README.md). (이 문서는 *지도와 동선*만 다룬다 — 룰 본문은
> 각 거버넌스 문서가 정본이다.)

## 0. 한눈에 — 무엇이 어디에 있나

레포 하나하나가 한 스택을 직접 재구성한 **독립 작업·학습 단위**이고, 세 개의 허브가 그것들을 감싼다.

```
seungwoo/
├─ <독립 레포> × ~25           각각이 작업·학습 단위 (자기 git 히스토리 + docs/)
├─ sportsbook/   × 10 레포      캡스톤 폴더 — 분산 베팅 백엔드 + 모바일 (하위 각각 독립 레포)
├─ ai-capstone/  × 5 레포       캡스톤 폴더 — RAG 에이전트 제품 (코어·게이트웨이·평가·계약)
├─ document-box/                허브: 거버넌스·학습 가이드 (이 문서가 사는 곳)
├─ plan-box/                    허브: 비-git 기획·원장 (TARGET·SEQUENCE-ai·quality-ledger)
└─ launch-box/                  허브: private git 출하·취업·운영 (SHIP·HIRE·ledger·ops-lab — 현 국면)
```

> **작업·학습 단위 = 독립 git 레포 하나.** 목록은 외우지 말고 `find . -maxdepth 3 -name .git`의
> 부모로 탐지한다(캡스톤·신규 제품 레포가 더 생긴다 — find가 항상 우선). 아래 클러스터 표는 빠른
> 조망용 스냅샷이다.

| 클러스터 | 레포 (★ = 그 스택의 대장 = 가장 깊은 노트를 가진 진입 레포) |
|---|---|
| C | small-shell★ · format-printer · signal-message-bus · thread-dining · stack-sort(Python) |
| C++ | stl-container★ · ray-scene-tracer · irc-relay-server(C++17) |
| 시스템 서버 | game-server-reliability-training★(C++20/C#) · game-server-foundations-training |
| 인프라 | container-stack★ · linux-admin · network-routing-notes |
| Node/TS | grounded-travel★(TS) · chatbot-evaluation · pong-pong(PostgreSQL/WS) |
| 프론트엔드 | frontend-reliability-training★(React) · frontend-foundations-training · portfolio-site(Next.js) |
| JVM 백엔드 ★주력 | backend-foundations-training★ · backend-reliability-training |
| 모바일 | mobile-reliability-training★ · mobile-foundations-training |
| AI | ai-foundations-training · ai-reliability-training |
| 캡스톤(백엔드) | sportsbook/: betting · wallet · settlement · risk · odds-feed · admin-api · shared-protocol · gateway · orchestration |
| 캡스톤(모바일) | sportsbook/mobile-client |
| 캡스톤(AI) | ai-capstone/: rag-agent · reliability-gateway · eval-gate · orchestration · shared-contracts |

(대장 진입점·스택별 상세: [SEQUENCE.md](SEQUENCE.md) §1·§5.)

## 1. 레포 한 개의 구조 (어느 레포를 열든 같다)

```
<repo>/
├─ docs/DESIGN.md          ⓪ 설계 의도 — 왜 이 레포·무엇을 만들기로 했나 (들어갈 때 먼저 1회)
├─ notes/                  ① 스택 가이드(깊은 선행 학습) + reference-impl/(짝 실행체)
├─ src · app · *-main …    본 프로젝트 코드 (정답 산출물)
└─ docs/
   ├─ commits/  NNN.md      ③ 답지: 커밋별 완성 코드 + 설계 이유 (끝에 L3/L2/L1)
   ├─ practice/ NNN.md      ④ 문제지: 답지에서 코드 본문을 비운 연습용
   ├─ notes/                ② 온디맨드 어휘(얕은 개념 노트, 선택적)
   └─ reflection/           회고 · 실패 모드 · 변경 비용
```

예외 둘: **캡스톤 서비스 레포(sportsbook 하위)는 루트 `notes/`가 없다** — 횡단 스택 노트 8개가
`sportsbook/orchestration/notes/`에 중앙화돼 있고 코어 스택은 기존 노트를 재사용한다. **핸즈온 레포**
(ray-scene-tracer · network-routing-notes)는 설계상 노트가 없다. (정본: SEQUENCE §4·§6.)

## 2. 레포의 문서들 — 역할과 읽는 법

들어가는 순서대로(설계 의도 → 스택 선행 → 직접 풀기 → 답 맞추기):

| 문서 | 역할 | 읽는 법 |
|---|---|---|
| **`docs/DESIGN.md`** | 이 레포가 **왜 존재하고 어떤 설계를 거쳤나** (목적·핵심 결정·의도적 비범위·구현 경로) | 레포 들어갈 때 **먼저 1회** — 무엇을·왜를 잡고 들어간다 |
| **`notes/<stack>.md`** | 스택 **교과서** (4부 포맷: 개념 → 본 코드 분석 → 미니프로젝트 → 심화. 짝 `reference-impl/`는 빌드 가능) | 그 스택을 **처음 배운다면 여기부터** 깊게 |
| **`docs/commits/NNN.md`** (답지) | 커밋별 **완성 코드 + 왜** (실제 git 커밋 근거, 끝에 L3/L2/L1 색인) | 구현이 *어떤 순서로* 쌓였나 — 직접 풀고 **마지막에** 펼친다 |
| **`docs/practice/NNN.md`** (문제지) | 답지에서 **코드 본문을 비운** 연습 (계약은 노출, 본문은 `// TODO: 책임`) | **답지를 덮고** 직접 채운 뒤 답지와 대조(재유도) |
| **`docs/notes/<cat>/`** | **얕은 개념 어휘** (온디맨드, 일부 레포만) | 커밋 따라가다 **막힐 때만** 펴는 용어 사전 |

**`notes/`와 `docs/notes/`를 혼동하지 마라 (가장 헷갈리는 지점).** 같은 주제(예: `docker`)가 양쪽에
있어도 중복이 아니라 **정반대 깊이**다: 루트 `notes/` = 깊게 선행 정독하는 **교과서**(4부), `docs/notes/`
= 얕게, 막힐 때만 꺼내는 **곁노트(용어 사전)**. "더 최근 = 진짜"가 아니라 *역할이 다른 두 계층*이다.

**L3 / L2 / L1 — 답지 끝의 복기 색인.** 각 답지 끝에 "이 커밋에서 무엇을 얼마나 내재화할지" 우선순위가 붙는다:

- **L3** — 문서 없이 **백지에서 설명·작도**할 핵심 (폭발 반경 큰 것: 동시성·트랜잭션·보안·돈 계산).
- **L2** — 소스·문서를 **펼쳐서** 흐름·예외·책임 분리를 설명할 수 있으면 충분.
- **L1** — 필요할 때 **읽어 파악**하면 됨.

전 레포의 L3만 모은 면접용 색인이 [INTERVIEW.md](INTERVIEW.md)다.

**dual-form 한눈에.** **답지(`docs/commits/`)가 정본**, **문제지(`docs/practice/`)는 파생**이다. 문제지를
덮고 직접 푼 뒤 답지로 채점한다 — *"다시 읽기"보다 "다시 만들기"*. (실체 있는 코드 커밋만 문제지를
가진다 — 마커·순수 문서·순수 타입 정의 커밋은 답지만 둔다.) 일부 답지의 `## 알려진 소스 결함` 절은
원본의 미수정 결함·수정 방향을 적은 것이니 재구현 때 그 지침을 따른다.

## 3. 사용 시나리오별 동선 (당신이 누구냐에 따라)

| 시나리오 | 동선 |
|---|---|
| **학습을 시작한다** | [STUDY.md](STUDY.md) **하나로 끝** — 왜·한 레포 도는 법·분야별·전체 순서(경로 A~F)·캡스톤·완주가 다 있다(구 SEQUENCE·LEARNING은 흡수된 동결 레거시) |
| **면접을 준비한다** | [INTERVIEW.md](INTERVIEW.md) Part 1(주제별 코어)을 백지 설명 연습 → 막히면 포인터의 답지 복기 |
| **레포를 만들거나 문서를 보강한다** (작업 세션) | 루트 `CLAUDE.md`(AI 라우터) → [docs-commit-note.md](docs-commit-note.md)(빌드·파생 룰) + [commit-policy.md](commit-policy.md)(커밋 규율) |
| **검수한다** | 읽기전용 탐지·보고 = [AUDIT.md](AUDIT.md) / 탐지→수정→커밋 = [QUALITY.md](QUALITY.md). 진행 원장 `plan-box/quality-ledger.md` |
| **모바일 트랙 설계를 본다** | [STUDY.md](STUDY.md) Part 4(모바일)·Part 6(캡스톤 API). 구 [mobile-track.md](mobile-track.md)는 동결 레거시 |
| **42 주도 + 백/프론트 병렬 진행 계획을 본다** | [STUDY.md](STUDY.md) Part 5 경로 F → 캘린더 [parallel-track.md](parallel-track.md) |
| **AI 트랙 기획을 본다** | `plan-box/`(TARGET.md · SEQUENCE-ai.md 등 — 비-git 허브) |

## 4. 불변 규칙 (요약 — 본문은 각 정본에)

- 독립 레포는 **자기 커밋 히스토리와 연동된 `docs/commits/`** 를 가져야 한다(없으면 위반).
- **추측·환각 금지** — 모든 문서 주장은 `git show`/실소스 근거. 근거가 없으면 멈추고 보고한다.
- 커밋: 영어 명령형 제목 + 한국어 `[근거]/[변경]/[검증]`, AI 트레일러 없음 (정본: commit-policy.md).
- 정본은 **한 곳**: 룰 본문은 document-box의 해당 문서에만 두고, 다른 곳에는 포인터만 둔다.
