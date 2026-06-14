# parallel-track.md — 42 주도 + 백/프론트 병렬 실행 캘린더 (경로 F 정본)

[SEQUENCE.md](SEQUENCE.md) **경로 F**의 짝 문서다. SEQUENCE가 *무엇을·어떤 순서로*(모듈·의존)를
정의한다면, 이 문서는 *세 레인을 캘린더에서 어떻게 동시에 굴리는가*(실행·배치·peak 분산)를 다룬다.
모듈·의존 모델은 SEQUENCE가 정본이며 여기서 재정의하지 않는다 — 충돌 시 SEQUENCE가 우선.

## 1. 전제 (게이트와 불변 규칙)

- **M0(linux-admin = 42 첫 과제)이 유일한 공통 게이트.** 이것만 끝나면 세 레인이 풀린다.
- **세 레인은 서로 하드 의존이 없다**(SEQUENCE §2). 유일한 교차 선행 하나: **FRONT는 grounded TS가
  선행**(사슬 2) → grounded-travel을 FRONT 레인 맨 앞에 둔다.
- **sportsbook 캡스톤은 JVM(backend-foundations+reliability) + 인프라(container-stack) 완료 후**
  진입(SEQUENCE §6). 이 둘만 끝나면 어느 phase든 배치 가능 — 일정의 주된 *slack 항목*이다.
- **peak 분산 규칙: 한 phase에 ★(심화 봉우리)는 최대 1개.** ★ = stl-container(C++ 점프)·
  game-server-reliability(C++20/시스템)·backend-reliability(분산 신뢰성)·frontend-reliability(RSC/Query/테스트).

## 2. 레인 정의 (★ = 심화 peak)

- **스파인 42/CS** (페이스 주도, 내부 순차): small-shell → [C 곁가지: format-printer·signal-message-bus·
  thread-dining·stack-sort] → **stl-container ★** → ray-scene-tracer → irc-relay-server →
  game-server-foundations → **game-server-reliability ★**
- **레인 BACK(JVM)**: backend-foundations → **backend-reliability ★** → container-stack(인프라) → sportsbook(캡스톤)
- **레인 FRONT(TS→React)**: grounded-travel(TS 게이트) → frontend-foundations → **frontend-reliability ★** → portfolio-site

## 3. 동시 진행표

각 phase = "그 phase의 가장 무거운 레인 항목을 끝내는 데 걸리는 시간"(절대 주(週) 아님 — §6 참조).
★는 phase 2·3·4·6에 하나씩 분산 — 절대 겹치지 않는다.

| Phase | 스파인 42/CS | 레인 BACK(JVM) | 레인 FRONT(TS→React) | 이 phase의 ★ |
|---|---|---|---|---|
| 0 게이트 | **linux-admin** (M0) | — | — | — |
| 1 기초 | small-shell (C 대장) | backend-foundations | — (대기) | — |
| 2 | C 곁가지 4종 [가벼움] | **backend-reliability ★** | grounded-travel (TS) | BACK |
| 3 | **stl-container ★** (C++ 점프) | container-stack [인프라] | frontend-foundations [가벼움] | 스파인 |
| 4 | ray-scene-tracer [C++ 적용] | sportsbook 착수 | **frontend-reliability ★** | FRONT |
| 5 | irc-relay → game-server-foundations | sportsbook 계속 | portfolio-site | — |
| 6 | **game-server-reliability ★** | sportsbook 마감 | (마감·폴리시) | 스파인 |

선행 검증: backend-reliability(P2)←foundations(P1) · stl-container(P3)←small-shell의 C 기초(P1) ·
sportsbook(P4~)←JVM(P1~2)+container-stack(P3) · frontend(P3~)←grounded TS(P2). 전부 충족.

## 4. 부하 메모 (정직)

- **P1은 의도적으로 2레인**(FRONT를 P2로 미룸): small-shell(C)+backend-foundations(Spring)만으로도
  기초 2개가 무겁다. 버거우면 backend-foundations 착수를 P1 후반으로 늦춰 겹침을 줄인다.
- **P2**: 스파인이 가벼운 C 곁가지 구간이라 BACK의 ★(backend-reliability)를 여기서 소화한다.
- **P3**: 스파인 ★(stl-container) 구간 → BACK·FRONT는 가벼운 항목(인프라·React 기초)만.
- **P4~6이 가장 붐빈다**(sportsbook 3 phase + 스파인 시스템 램프). sportsbook은 *신규 학습*이 아니라
  *종합 적용*(기존 노트 재사용)이라 ★ 레인과 병행이 그나마 견딘다. 그래도 무거우면 — sportsbook은
  P3 이후 아무 때나 배치 가능한 slack 항목이므로 **스파인 시스템(P5~6)을 먼저 닫고 sportsbook을
  뒤로 미는** 변형이 가장 안전하다.

## 5. 생략·축소 옵션

- **Node 백엔드(chatbot-evaluation·pong-pong)**: JVM이 back 타겟이면 선택 — 생략하거나 맨 뒤 append.
  grounded-travel은 FRONT의 TS 게이트라 생략 불가.
- **C 곁가지**: 시간 압박 시 stack-sort(Python·알고리즘)만 남기고 축소 가능(SEQUENCE §4 "떼어쓰기").
- **AI 트랙**: 이 캘린더 밖. 별도 사슬(stack-sort Python → ai-foundations → ai-reliability →
  ai-capstone, plan-box 정본)이라 경로 F 완주 뒤 enrichment로 얹는다.

## 6. phase → 주(週) 매핑

phase 길이는 사용자 속도(velocity)에 달려 고정하지 않는다. 실제로 한 phase를 돌려 본 뒤 그 소요를
기준으로 다음 phase를 잡고, [quality-ledger](../plan-box/quality-ledger.md) 식으로 진도를 기록한다.
peak가 겹치지 않는 한, phase 안에서 레인 항목의 착수 시점은 자유롭게 흔들어도 된다.

## 참조

- 모듈·의존·대장: [SEQUENCE.md](SEQUENCE.md)(경로 F 포함) · 실행 루프(레포 도는 법): [LEARNING.md](LEARNING.md) ·
  스택별 입문 진입점: SEQUENCE §1·§5. (이 문서는 캘린더만; 그 외는 위 정본을 따른다.)
