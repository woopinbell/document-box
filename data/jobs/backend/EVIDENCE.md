# Backend 지원 증거 matrix

공고의 요구사항을 42·Backend release에서 재현 가능한 근거로 연결합니다. Foundations V2,
Reliability V2, Risk correctness와 Orchestration은 고정된 release ref를 사용합니다. 공개 URL을
영구 증거처럼 적지 않습니다. 공식 28개 프로젝트의 private 상태를 전수 확인했으며, 필요할 때만
release tag가 고정된 저장소를 선택적으로 초대하고 learning branch보다 `main`의 source·test·운영
문서를 먼저 보여 줍니다.

## release surface

| 저장소·release | 확인 가능한 근거 | 과장하면 안 되는 범위 |
| --- | --- | --- |
| `backend-foundations-training` / `foundations-v2` (`770d7ea`, learning `f3ff558`) | Spring HTTP·validation·JPA·transaction·security와 JVM/Go 비교, standalone·Compose 검증 | 상용 트래픽이나 팀 개발 경험이 아닙니다. |
| `backend-delivery-training` / `delivery-v1` | executable artifact, runtime config, migration, health/readiness, structured log, CI·runbook | Kubernetes나 production on-call 경험으로 확대하지 않습니다. |
| `backend-reliability-training` / `reliability-v2` (`b0aad3c`, learning `634f9c2`) | idempotency, lock/race, cursor, token bucket, cache, outbox, retry, tracing, saga와 failure injection | 특정 회사의 장애 대응 실적으로 쓰지 않습니다. |
| Shared·Wallet·Odds·Betting·Settlement·Gateway·Admin release | Money/odds schema, double-entry wallet, odds, bet, settlement, gateway와 admin 경계 | 실제 베팅 사용자·금액·규제 시스템이 아닙니다. |
| `sportsbook-risk-service` / `risk-v1` (`76c822b`, learning `d262f52`) | 99 correctness tests, atomic snapshot, fail-closed decision과 정적/package gate | 1,000 RPS qualification은 RED입니다. `p99 < 30 ms`, drops 0 또는 production SLO를 주장하지 않습니다. |
| `sportsbook-orchestration` / `orchestration-v1` (`564a83a`, learning `9d5fa54`) | 9개 release 고정 manifest, JWT 401, Risk fail-closed, WON 1/LOST 2, payout/forfeit, `locked=0`, replay exact-state와 cold E2E 144/0 | Risk의 독립 1,000 RPS qualification이나 production traffic 근거로 확대하지 않습니다. |
| Central `backend-distributed-incident` | evidence·falsifier·rollback·reconciliation을 답지 없이 작성하는 독립 평가 | 평가 starter를 제품 구현이나 정답 corpus로 소개하지 않습니다. |

## 요구사항 → 제출 근거

| 공고 요구사항 | 앞에 둘 근거 | 설명할 결정·검증 | 남은 gap |
| --- | --- | --- | --- |
| Java·Spring·JPA·RDBMS | Foundations → Reliability | transaction boundary, validation/auth 실패 분리, lock·idempotency와 focused test | 회사 codebase 유지보수 경험은 없습니다. |
| Redis·rate limit·cache | Reliability + Risk | token bucket, snapshot consistency, fail-closed decision과 RED 성능 근거의 latency 분해 | 1,000 RPS SLO 인증, managed Redis 운영과 cluster failover는 직접 경험이 아닙니다. |
| event·Kafka·outbox | Betting + Settlement + Shared | DB commit과 publication 경계, partition/replay/DLQ, duplicate settlement test | production broker 운영이나 대규모 lag 대응을 주장하지 않습니다. |
| 결제·정산·돈 불변식 | Wallet + Betting + Settlement | minor unit, double-entry, lock/release, payout/forfeit와 reconciliation | 실제 금융 규제·PG 연동 경험은 없습니다. |
| Docker·배포·readiness | Delivery + Orchestration + 42 Container Stack | immutable artifact, config/migration 순서, cold start, readiness와 deterministic E2E | Kubernetes·Terraform 실무가 필요한 공고에는 별도 gap입니다. |
| 장애 분석·관측성 | Reliability + Orchestration + distributed incident | evidence와 falsifier, timeout/retry, rollback, metrics/log trace와 recovery plan | on-call·사용자 영향·MTTR 수치를 만들지 않습니다. |
| Node·TypeScript 인접군 | Pong·Frontend Reliability + Sportsbook 계약 설계 | TypeScript API/state, shared schema, async failure와 test | Node backend를 Java/Spring 실무와 같은 깊이라고 주장하지 않습니다. |
| CS·Linux·network | 42 Thread/IRC/Small Shell/Web Boundary | process/thread/fd, nonblocking I/O, TCP/HTTP boundary와 실제 검증 | 현대 C++ 또는 Linux fleet 운영 경력은 아닙니다. |

## 공고별 최소 packet

| 공고 | 우선 제시 | 보조 | 면접에서 먼저 밝힐 gap |
| --- | --- | --- | --- |
| 포스타입 | Foundations·Reliability | Sportsbook + 42 Web/Network | AWS 운영과 실제 수백만 요청 경험 없음 |
| 아드리엘 | Reliability + Orchestration | Pong·Frontend Reliability | 영어 협업, Node production과 외부 광고 API 경험 없음 |
| 데이콘 | Pong + Orchestration | Frontend Reliability + Delivery | 2년 실무, LLM pipeline과 AWS 운영 경험 없음 |
| 이팝소프트 | Sportsbook + Reliability | Delivery + Pong | 유료 서비스·대규모 트래픽·Terraform 운영 경험 없음 |

## 제출 gate

1. 선택한 release의 main/tag 일치와 fresh-clone 검증 결과를 다시 확인합니다.
2. 공고별로 2~3개 저장소만 고르고 `문제 → 설계 결정 → 검증 명령 → 결과` 한 줄씩 준비합니다.
3. repository invitation은 요청받은 reviewer에게 필요한 저장소만 최소 기간으로 제공합니다. Learning
   답지·문제지는 source 설명이 필요한 경우에만 추가로 엽니다.
4. 이력서와 면접에서 개인 학습 release, 실제 실무와 production 운영을 명시적으로 구분합니다.
5. 회사 평균·백분위 proxy 후보는 기본연봉 4,000만원 이상을 확인하기 전 과제나 개인정보 제출 범위를
   확대하지 않습니다.
6. 지원 버튼과 고용형태가 바뀌거나 선택한 주장에 필요한 release gate가 red이면 packet을 중단합니다.
   Risk의 1,000 RPS 성능 근거가 필요한 공고에는 현재 release를 성능 인증으로 사용하지 않습니다.
