# Backend 트랙

HTTP/JPA 기본기에서 배포 표면, 신뢰성 결정 패턴과 분산 Sportsbook까지 이어지는 JVM 중심
트랙입니다. 42의 `container-stack` 지식은 선행으로 재사용하지만 Backend 프로젝트 목록에는 넣지
않습니다.

```text
backend-foundations-training
→ backend-delivery-training
→ backend-reliability-training
→ sportsbook
```

## 공통 진행 방식

- 각 저장소의 `main`은 실행 가능한 source/config/test와 release 문서를 소유합니다.
- 해당 release의 `learning/<release>`에서 notes, answers, practices를 순서대로 읽습니다.
- Spring main track을 먼저 완성하고 Go sub-track에서 같은 계약을 압축 비교합니다.
- 돈, transaction, idempotency, outbox와 concurrency 같은 L3만 백지에서 재구성합니다.
- Ref와 corpus 규칙은 [`../commit-policy.md`](../commit-policy.md)와
  [`../docs-commit-note.md`](../docs-commit-note.md)를 따릅니다.

## 1. `backend-foundations-training`

Java 21와 Spring Boot의 요청 → 검증 → transaction → response 기본기를 exercise로 익힙니다.

- 범위: HTTP JSON, CRUD, validation, JPA, relation, test slice, session/Security, pagination,
  multipart, PostgreSQL bridge와 작은 background job
- 비교: Go 표준 library로 HTTP, state와 validation 경계를 다시 확인
- L3: transaction boundary, idempotent create, CRUD 상태 소유권, validation/auth 실패 분리
- 검증: `make test`, `make test-spring`, `make test-go`, `make check-docs`와 focused exercise test
- 완료: transaction과 session/security 경계를 설명하고 전체 gate 통과

## 2. `backend-delivery-training`

구현된 API를 외부 환경에 전달할 수 있는 artifact와 운영 기준선으로 닫습니다.

- 범위: executable jar, Docker image, runtime config/profile, PostgreSQL Compose와 migration,
  health/readiness, structured log, CI와 runbook
- 비교: Go delivery probe로 image, env와 health surface를 작은 runtime에서 재확인
- L3: build artifact와 runtime config 분리, immutable image, migration 순서, liveness/readiness 경계
- 검증: `make test`, Spring/Go test, docs check, image build와 가능한 환경의 Compose 기동
- 완료: README만으로 prod-like service를 시작·진단할 수 있고 health/CI gate 통과

Delivery는 reliability 패턴 과정이나 Kubernetes 운영 과정이 아닙니다. 배포 가능한 서비스의 최소
납품 표면만 소유합니다.

## 3. `backend-reliability-training`

HTTP controller보다 service 계층의 실패 모드와 상태 전이를 회귀 test로 고정합니다.

- 범위: idempotency key, transaction race, cursor pagination, token bucket, retry queue, cache
  invalidation, outbox, authorization, upload safety, tracing, failure injection과 saga
- 비교: Go 표준 library로 rate limit, worker pool, timeout과 최소 idempotency를 재구성
- L3: duplicate suppression, pessimistic locking, atomic outbox, retry transition, cache coherence,
  compensation과 fail-open/closed
- 검증: `make test`, Spring/Go focused test와 필요한 Testcontainers PostgreSQL scenario
- 완료: idempotency, race, outbox와 compensation을 백지에서 설명하고 deterministic gate 통과

## 4. `sportsbook/`

Sportsbook은 상위 단일 저장소가 아니라 다음 **9개 독립 Git 저장소**를 담는 Backend 캡스톤입니다.
각 하위 저장소를 별도 작업·commit·검증 단위로 취급합니다.

```text
1. shared-protocol
2. wallet-service
3. risk-service
4. odds-feed-service
5. betting-service
6. settlement-service
7. gateway
8. admin-api
9. orchestration
```

### 하위 순서와 책임

1. **shared-protocol**: Avro event, Money/Odds/ID value object와 공통 enum
2. **wallet-service**: double-entry ledger와 idempotent debit/credit/forfeit
3. **risk-service**: user/market limit, pattern decision과 critical-path latency budget
4. **odds-feed-service**: odds ingress, Kafka publish와 Redis write-through
5. **betting-service**: slip validation → risk/wallet 동기 호출 → transaction outbox
6. **settlement-service**: result consumer, WON/LOST/PUSH/VOID, saga, DLQ와 payout/forfeit
7. **gateway**: JWT, rate limit, public route와 realtime perimeter
8. **admin-api**: void/refund/limit/market-close와 audit를 사용자 perimeter에서 분리
9. **orchestration**: Compose, build staging, E2E, chaos와 observability overlay

`sportsbook/mobile-client`는 이 트랙에서 제외합니다.

### Capstone L3

- minor-unit/BigDecimal과 double-entry ledger 불변식
- Idempotency-Key와 transaction race
- 상태 변경과 event publication의 atomic outbox
- synchronous bet acceptance와 asynchronous settlement saga의 경계
- Kafka partition key, DLQ, retry와 single-broker replication 함정
- gateway/admin blast-radius 분리, circuit breaker와 rate-limit failure policy

### 검증

각 저장소의 unit/integration gate를 먼저 통과한 뒤 orchestration에서 실행합니다.

```bash
./scripts/build-all.sh
docker compose up -d --wait postgres kafka redis
docker compose up -d
bash e2e/run-e2e.sh
```

단독 green을 통합 green으로 간주하지 않습니다. Shared protocol packaging, infrastructure config,
service contract와 end-to-end payout/forfeit를 별도로 확인합니다.

## 트랙 완료

세 훈련 저장소를 순서대로 완료하고 Sportsbook 9개 저장소가 통합 동작해야 합니다. 돈, 멱등,
transaction/outbox와 saga를 코드 없이 설명하고 장애 시 보상·중복·정합성 경계를 방어할 수 있으면
Backend 트랙 완료입니다.
