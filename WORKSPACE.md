# WORKSPACE.md — 레포체계 사용법 (전체 코퍼스 안내 정본)

`~/Desktop/seungwoo`는 여러 독립 레포로 된 **학습 포트폴리오 코퍼스**다. 각 레포는 한 스택(예: Spring ·
React · Android · RAG)을 **직접 재구성하며** 익힌 기록이고, 그 과정을 정해진 형태의 문서로 남긴다.
이 문서는 **이 워크스페이스에 처음 들어온 사람**이 전체 구조와 사용 동선을 한 번에 잡는 정본이다.
(룰·절차의 정본은 각 거버넌스 문서 — [README](README.md)의 카탈로그 참조.)

## 0. 한눈에 — 무엇이 어디에 있나

```
seungwoo/
├─ <독립 레포> × 25            각각이 작업·학습 단위 (자기 git 히스토리 + docs/commits 보유)
├─ sportsbook/   × 10 레포     캡스톤 폴더 — 하위 각각이 독립 레포 (분산 베팅 백엔드 + 모바일)
├─ ai-capstone/  × 5 레포      캡스톤 폴더 — RAG 에이전트 제품 (코어·게이트웨이·평가·계약)
├─ document-box/               허브: 거버넌스·교차 문서 (이 문서가 있는 곳, dual-form 대상 아님)
└─ plan-box/                   허브: 비-git 기획·원장 (TARGET, SEQUENCE-ai, quality-ledger 등)
```

- **작업·학습 단위 = 독립 git 레포 하나.** 정본 열거는 `find . -maxdepth 3 -name .git -type d`의
  부모다(캡스톤 폴더는 더 생길 수 있으므로 목록을 외우지 말고 find를 따른다).
- 아래 지도는 **2026-06-11 기준 스냅샷(40개)** — 빠른 조망용이며 find 결과가 항상 우선한다.

| 클러스터 | 레포 |
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

(★ = 그 스택의 "대장" — 가장 깊은 노트를 가진 진입 레포. 상세: [SEQUENCE.md](SEQUENCE.md) §1·§5.)

## 1. 레포 한 개의 구조 (어느 레포를 열든 같다)

```
<repo>/
├─ notes/                  ① 스택 가이드(깊은 선행 학습) + reference-impl/(짝 실행체)
├─ src · app · *-main …    본 프로젝트 코드 (정답 산출물)
└─ docs/
   ├─ commits/  NNN.md      ③ 답지: 커밋별 완성 코드 + 설계 이유
   ├─ practice/ NNN.md      ④ 문제지: 답지에서 코드 본문을 비운 연습용
   ├─ notes/                ② 온디맨드 어휘(얕은 개념 노트, 선택적)
   └─ reflection/           회고 · 실패 모드 · 변경 비용
```

예외 두 가지: **캡스톤 서비스 레포(sportsbook 하위)는 루트 `notes/`가 없다** — 횡단 스택 노트 8개가
`sportsbook/orchestration/notes/`에 중앙화돼 있고 코어 스택은 기존 노트를 재사용한다. **핸즈온 레포**
(ray-scene-tracer, network-routing-notes)는 설계상 노트가 없다. (정본: SEQUENCE §4·§6.)

## 2. 네 가지 문서 — 역할과 품질 기준

| 폴더 | 역할 | 품질 기준 | 읽는 법 |
|---|---|---|---|
| **`notes/<stack>.md`** | 스택 **교과서** (깊은 선행 정독) | **4부 포맷**: 개념·멘탈모델 → 본 프로젝트 코드 분석 → 학습용 미니프로젝트 → 심화. 스택 1개=1노트, 짝 `reference-impl/`는 빌드 가능 | 그 스택을 **처음 배운다면 여기부터** 깊게 |
| **`docs/commits/NNN.md`** (답지) | 커밋별 **완성 코드 + 왜** | 실제 git 커밋에 근거(추측 없음) · **완성 코드를 보여줌**(산문만 X) · 검증 명령 실행 가능 · 끝에 L3/L2/L1 색인 | 구현이 *어떤 순서로* 쌓였는지, 각 결정의 이유를 따라 읽기 |
| **`docs/practice/NNN.md`** (문제지) | 답지에서 **코드 본문을 비운** 연습 | 계약(시그니처·타입·구조)은 노출, 본문은 `// TODO: 책임`, 답지와 **같은 논리 단위** | **답지를 덮고** 직접 채운 뒤 답지와 대조(재유도 학습) |
| **`docs/notes/<cat>/`** | **얕은 개념 어휘** (온디맨드) | 카테고리별 짧은 노트, **선택적**(없는 레포 있음) | 커밋을 따라가다 **막힐 때만** 펼치는 용어 사전 |

### `notes/` 와 `docs/notes/` 는 다르다 (가장 헷갈리는 지점)

같은 주제(예: `docker`)가 양쪽에 있어도 **중복이 아니라 정반대 깊이**다: 루트 **`notes/`** = 깊게 선행
정독하는 **교과서**(4부), **`docs/notes/`** = 얕게, 막힐 때만 꺼내는 **곁노트(용어 사전)**. "더 최근 =
진짜"가 아니라 **역할이 다른 두 계층**이다.

### L3 / L2 / L1 — 답지 끝의 복기 색인

각 답지 끝에는 "이 커밋에서 무엇을 얼마나 내재화할지" 우선순위가 붙는다:

- **L3** — 문서 없이 **백지에서 설명·작도**할 핵심(폭발 반경 큰 것: 동시성·트랜잭션·보안·돈 계산).
- **L2** — 소스·문서를 **펼쳐서** 흐름·예외·책임 분리를 설명할 수 있으면 충분.
- **L1** — 필요할 때 **읽어 파악**하면 됨.

전 레포의 L3만 모은 면접용 색인이 [INTERVIEW.md](INTERVIEW.md)다.

### dual-form 한눈에

**답지(`docs/commits/`)가 정본**, **문제지(`docs/practice/`)는 파생**이다. 학습자는 문제지를 덮고 직접
풀어본 뒤 답지로 채점한다 — "다시 읽기"보다 **"다시 만들기"**. (실체 있는 코드 커밋만 문제지를 가진다;
마커·순수 문서·순수 타입 정의 커밋은 답지만 둔다.) 일부 답지에는 `## 알려진 소스 결함` 섹션이 있다 —
소스의 미수정 결함과 수정 방향을 기록한 것이니 재구현 시 그 지침을 따르라.

## 3. 사용 시나리오별 동선 (당신이 누구냐에 따라)

| 시나리오 | 동선 |
|---|---|
| **학습을 시작한다** | [SEQUENCE.md](SEQUENCE.md)에서 경로 선택(기본 = 경로 A: JVM 최단) → 각 레포를 [LEARNING.md](LEARNING.md) §3 루프로 돈다(노트 정독 → reference-impl → **답지 덮고 재구성** → L3 복기) |
| **면접을 준비한다** | [INTERVIEW.md](INTERVIEW.md) Part 1(주제별 코어)을 백지 설명 연습 → 막히면 포인터의 답지 복기 |
| **레포를 만들거나 문서를 보강한다** (작업 세션) | 루트 `CLAUDE.md`(AI 라우터) → [docs-commit-note.md](docs-commit-note.md)(빌드·파생 룰) + [commit-policy.md](commit-policy.md)(커밋 규율) |
| **검수한다** | 읽기전용 탐지·보고 = [AUDIT.md](AUDIT.md) / 탐지→수정→커밋 = [QUALITY.md](QUALITY.md). 진행 원장은 `plan-box/quality-ledger.md` |
| **모바일 트랙 설계를 본다** | [mobile-track.md](mobile-track.md) |
| **AI 트랙 기획을 본다** | `plan-box/`(TARGET.md · SEQUENCE-ai.md 등 — 비-git 허브) |

## 4. 불변 규칙 (요약 — 본문은 각 정본에)

- 독립 레포는 **자기 커밋 히스토리와 연동된 `docs/commits/`** 를 가져야 한다(없으면 위반).
- **추측·환각 금지** — 모든 문서 주장은 `git show`/실소스 근거. 근거가 없으면 멈추고 보고.
- 커밋: 영어 명령형 제목 + 한국어 `[근거]/[변경]/[검증]`, AI 트레일러 없음 (정본: commit-policy.md).
- 정본은 **한 곳**: 룰 본문은 document-box의 해당 문서에만 두고, 다른 곳에는 포인터만 둔다.
