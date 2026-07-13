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

## 2026-07-13 원격 release 상태

다음 SHA는 source/learning 분리와 원격 공개가 끝난 뒤 실제 원격 ref를 다시 읽고 fresh clone에서
검증한 값입니다. Release 열은 `annotated tag object → peeled source commit` 순서입니다.

| 저장소 | `main` | release | `learning/<release>` | fresh-clone 검증 |
| --- | --- | --- | --- | --- |
| `backend-foundations-training` | `189f49548edea71eb17fc92acf3059daa089d6f3` | `foundations-v1`: `46171d1254335c1398f5c23d87a122c2e2bb2048` → `189f49548edea71eb17fc92acf3059daa089d6f3` | `d7f50a1e08c08892c5af8704971fe6b15091acc5` | Make, JVM/Go, reference 17개, Compose와 문서 gate green |
| `backend-delivery-training` | `66b095b7bf34a114b99f14ea80bd75763ef60eed` | `delivery-v1`: `60d0f8dc26b6ca36e176fc3a315da1884096942b` → `66b095b7bf34a114b99f14ea80bd75763ef60eed` | `bf1a84e6eecd4544676a71ea7143b01a01b18a4d` | Make, JVM/Go, image, Compose와 branch-aware 문서 gate green |
| `backend-reliability-training` | `a28ad09ceea9bc28a1321601ff4202816ac00775` | `reliability-v1`: `7902d50106b40c1673a09f44f43c1c9a53b15eea` → `a28ad09ceea9bc28a1321601ff4202816ac00775` | `c4b34b46e3024f4f9ccef8b3c884184763622680` | Make, JVM/Go, reference 11개, Testcontainers와 Compose green |
| `sportsbook/shared-protocol` | `e0754c3a68ddce4f9ddef00e3dfb26b3ce53adbb` | `shared-v1`: `bd3ab9cb9df9ddce51aecd32008b8844781a184c` → `e0754c3a68ddce4f9ddef00e3dfb26b3ce53adbb` | `415bd8165e66fe8a83a32b4855f43038577a6eac` | 89 tests, Spotless, Checkstyle와 package green |
| `sportsbook/wallet-service` | `0f28d668856d702c1bcea90e1a42bd43871c0a9f` | `wallet-v1`: `89afc07a1886426ce8d68bdae3c99f650fbf98b7` → `0f28d668856d702c1bcea90e1a42bd43871c0a9f` | `009de12feb4dc99410dddb08469d9261e4a3ffcf` | single shared 0.2 Maven 저장소에서 49 tests와 전체 verify green |
| `sportsbook/betting-service` | `a4009f118b77f6739b591a3c2f87dcfd98c03c21` | `betting-v1`: `978da92ea9cafa5297fb3fdfa0eb7ee88f9680b0` → `a4009f118b77f6739b591a3c2f87dcfd98c03c21` | `4384d307461be43d3ae4761a8de60615a2594336` | 130 tests와 placement/reconciliation 10회 반복, 전체 verify green |
| `sportsbook/gateway` | `e955ee6ecf0e6b63d31bacfefc8657ff72271b8e` | `gateway-v1`: `ad65e266880ff10dd3ed6f9c5e406fe6fdb02713` → `e955ee6ecf0e6b63d31bacfefc8657ff72271b8e` | `912d87afc12516313f8ce320581fde77c8f89a60` | 22 tests와 전체 verify green |
| `sportsbook/admin-api` | `1c39c9cab5830214d5a99c20419e1f940ec6eeb2` | `admin-v1`: `51eb82ce43d2a9877cf15329c3daf6125aac306a` → `1c39c9cab5830214d5a99c20419e1f940ec6eeb2` | `26e58686b8d4f1bb45ef19ef5c5b492f540c2c88` | 28 tests와 전체 verify green |

위 여덟 저장소는 source release 단위로 green입니다. 기존 corpus는 byte-for-byte 보존했고, 현재
source graph용 corpus는 각 immutable learning branch에 추가했습니다. 공개 후 임시 archive와 중복
feature branch를 제거해 장기 branch는 `main`과 해당 `learning/<release>`만 남겼습니다.

다음 네 저장소는 release가 아니라 재현 가치가 있는 **진단 상태**만 보존합니다. Diagnostic 열은
`annotated tag object → peeled candidate commit` 순서입니다.

| 저장소 | 원격 `main` | diagnostic | release 차단 근거 |
| --- | --- | --- | --- |
| `sportsbook/risk-service` | `db45a5611a2ac4554a78adbed759500af30d85c7` | `diagnostic-codex-5.6-red`: `51707bec5cf5c6a7bb7ea750f95688f2247f1e2e` → `eca275e3de27222ee774b61c55d07c955a11694d` | 1,000 RPS 반복 gate가 2/5만 green이고 허용된 단일 tuning이 모두 실패 |
| `sportsbook/odds-feed-service` | `c0f46ab38335218ea441cc01c13ab1c5b2493caa` | `diagnostic-codex-5.6-red`: `8a541f7fa667610e4700e8368f47693bd1e219a4` → `155f91de0c97d986561f89017e1e6d04ae6f57d8` | events p99 62.39ms, odds p99 90.49ms로 latency gate red |
| `sportsbook/settlement-service` | `42bc2d88a28c571e0af263ab02fd27523be70538` | `diagnostic-codex-5.6-red`: `7e12e80eb8c310f33a088d41cb4c67331f3a7e22` → `3e157ab491e22a203ec12300b63b275c8c835d6e` | WON/LOST 10,000건 성능 gate 30회가 모두 10초 기준 red |
| `sportsbook/orchestration` | `00581a4714ea167a7925da1e720792793a66fc5e` | `diagnostic-codex-5.6-red`: `09d6127c6def47cb16c9775bb3da5aa1f684ceab` → `5767b959248da79104e47977d91a76c8fb95246c` | orphan locked debit 증거가 남고, 최신 strict cold E2E는 첫 bet의 risk 호출 timeout으로 HTTP 500·exit 1 |

`diagnostic-codex-5.6-red`는 비-release tag이며 완료 수에 포함하지 않습니다. 모든 저장소를 fresh
clone한 뒤 개별 gate와 orchestration strict cold E2E의 인증·WON/LOST·잔액·locked 불변식이 함께
green이어야만 Sportsbook과 Backend 트랙을 완료로 바꿀 수 있습니다. 현재는 `sportsbook-v1` tag를
만들지 않았고 **Sportsbook과 Backend 트랙 모두 미완료**입니다.

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
Backend 트랙 완료입니다. 현재 Training 3개와 Sportsbook source release 5개는 green이지만, Red 4개와
strict cold E2E가 남아 있으므로 이 완료 조건을 충족하지 않았습니다.
