# STUDY.md — 레포 학습, 실전 요약

> 이것만 읽고 시작해도 되는 압축판. 규칙이 더 궁금하면 [LEARNING.md](LEARNING.md)(정본),
> 순서는 [SEQUENCE.md](SEQUENCE.md). 충돌하면 그쪽이 이긴다.

전제 두 줄:
- 레포 = **직접 다시 만들면서 배우는** 구현 단위다. 읽기만 하면 남는 게 없다.
- 문서 = 선수지식 계층이다. 루트 `notes/`(선행 교과서) → `docs/practice/`(빈칸 문제) →
  `docs/notes/`(막힐 때 용어집) → `docs/commits/`(답+이유. **마지막에 펼친다**).

## 공통 루프 — 어느 레포든 이 6단계

1. SEQUENCE에서 다음 레포를 고른다(기본 = 경로 A: JVM 최단).
2. 루트 `notes/<stack>.md`를 읽는다. **처음 보는 스택만 1부(개념)부터 깊게**, 아는 스택이면
   2부(본 코드 분석)만. `reference-impl/`이 있으면 빌드해서 한 번 만져본다.
3. `docs/practice/NNN.md`를 번호順으로: 개요·계약·책임 줄만 읽고 **답지 덮고 직접 구현한다.**
4. 문제지 `## 검증`의 명령을 실제로 돌린다. 그다음 `git show <커밋>`(또는 답지)과 diff —
   내 결정이 다르면 *왜* 다른지 따진다. 여기가 학습의 본체다.
5. 답지 끝 **L3 항목을 백지에서 말로 설명**해 본다. 안 되면 그 커밋은 안 끝난 거다.
6. 레포를 닫을 때 [INTERVIEW.md](INTERVIEW.md)에서 그 레포 L3 줄들을 한 번 더 훑는다.

막히는 순서: `docs/notes/` 용어집 → 답지의 **해당 `###` 한 절만** → 그래도면 답지 전체.

## 묶음별 차이 — 방법과 집중점

| 묶음 | 재구성 단위 | 검증 | 집중할 것 | 함정·예외 |
|---|---|---|---|---|
| **C** (small-shell·format-printer·signal-message-bus·thread-dining) | 커밋(작다) | `make test` + 수동 시나리오 | **소유권**("누가 할당하고 누가 닫나"를 소리 내 말하기), fd·프로세스·시그널 안전 | stack-sort는 알고리즘 — 독립 적용기(Python)로 출력 검증하는 법 자체가 배울 거리 |
| **C++** (stl-container·irc-relay-server) | 커밋 | stl=std와 행동 대조, irc=`make test` 스모크 | stl: 예외 안전·iterator 무효화. irc: 이벤트 루프·부분 프레임 — **상태 전이를 그림으로** | ray-scene-tracer는 핸즈온(노트 없음) — 체크섬 결정성만 확인하며 따라 만든다 |
| **시스템서버** (gsf·gsr) | 과제 1커밋 = 1모델 | **테스트가 채점기** | 경계·불변식(틱 루프, 레지스트리 lock 경계, 하트비트) | 방법이 다르다: **테스트를 먼저 읽고** 구현한다(문제지보다 테스트가 더 정확한 명세) |
| **인프라** (container-stack·linux-admin·network-routing-notes) | 절차·정책 | cs=정적 검증기, la=실제 VM, nrn=손계산 | 구현이 아니라 **왜 이 정책인가**(헬스체크 체인, secret 분리, sudo/SSH 경계) | 이 묶음은 코드 재구성보다 "백지에서 구조도+정책 근거" 재현이 목표 |
| **웹 training** (ffd·frt) | 과제 triplet(모델→구현→테스트) | 테스트 채점기 + `check:repo` | **frt가 본대**: 실패 모드(스테일 응답, 낙관적 업데이트 롤백, 에러 경계, RSC 경계) | ffd의 카탈로그-범프류 반복 커밋은 묶어서 빠르게 — 전부 같은 무게로 돌지 말 것 |
| **제품형 TS** (grounded-travel·chatbot-evaluation·pong-pong·portfolio-site) | 기능 단위 커밋 | `pnpm dev`/`npm run dev` **실행하며** + 테스트 | 공유 계약(schemas)이 중심 — 화면↔코드 왕복. pong은 서버 권위 모델 | pong 85커밋 전부 재구성은 과투자 — L3 붙은 커밋만 깊게, 나머지는 답지 통독 |
| **Java/Spring** (bf·br → sportsbook 9) | bf/br=과제, sportsbook=기능 커밋 | 테스트 채점기 / `mvn test`(또는 `./mvnw`) | **돈·멱등·트랜잭션·outbox** — 이 코퍼스의 심장. 답지의 "왜" 절을 빼먹지 말 것 | sportsbook은 **순서 고정**: shared-protocol → betting → wallet → risk·odds-feed → settlement → gateway·admin → orchestration. 노트는 orchestration/notes에 중앙화 — 서비스 들어가기 전 해당 노트 1편 선행. 통합 검증은 Docker 필요(없으면 단위까지만 하고 e2e는 답지로) |
| **모바일** (mf·mr·mobile-client) | 과제/기능 커밋 | JVM 단위 테스트(코덱 등)만 SDK 없이 가능 | 상태 소유(ViewModel·StateFlow), single-flight refresh, 오프라인 우선 | SDK 없는 머신에선 빌드 불가 — 코드 리딩+JVM 테스트로 돌고, 빌드 검증은 SDK 환경에서 |
| **AI** (af·ar → ai-capstone 5) | 과제/기능 커밋 | 전부 **오프라인·결정적**(포트 주입) — 어디서든 실행됨 | grounding 게이트, step-cap, 평가 3층(결정·judge·회귀), 멱등 키=의도의 함수 | capstone 순서: shared-contracts → rag-agent → reliability-gateway → eval-gate → orchestration |

## 깊이 조절 — 전부 같은 깊이로 돌지 마라

- **과투자할 곳은 L3 주제뿐**: 동시성·트랜잭션·멱등·돈 계산·실패 모드. 나머지는 L2(펼쳐서 설명)·
  L1(읽고 파악)로 끝낸다. 어떤 커밋이 어느 급인지는 답지 끝에 다 적혀 있다.
- 시간이 없으면: 경로 A 레포만 돌고 + [INTERVIEW.md](INTERVIEW.md) Part 1을 백지 연습.
- 일부 답지에 `## 알려진 소스 결함` 절이 있다 — 재구성 전에 그것부터 본다(원본의 함정 안내).
