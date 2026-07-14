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

## 2026-07-14 원격 release·학습 사이클 종료 상태

다음 SHA는 source/learning 분리와 원격 공개가 끝난 뒤 실제 원격 ref를 다시 읽고 fresh clone에서
검증한 값입니다. Release 열은 `annotated tag object → peeled source commit` 순서입니다.

| 저장소 | `main` | release | `learning/<release>` | fresh-clone 검증 |
| --- | --- | --- | --- | --- |
| `backend-foundations-training` | `189f49548edea71eb17fc92acf3059daa089d6f3` | `foundations-v1`: `46171d1254335c1398f5c23d87a122c2e2bb2048` → `189f49548edea71eb17fc92acf3059daa089d6f3` | `d7f50a1e08c08892c5af8704971fe6b15091acc5` | Make, JVM/Go, reference 17개, Compose와 문서 gate green |
| `backend-delivery-training` | `66b095b7bf34a114b99f14ea80bd75763ef60eed` | `delivery-v1`: `60d0f8dc26b6ca36e176fc3a315da1884096942b` → `66b095b7bf34a114b99f14ea80bd75763ef60eed` | `bf1a84e6eecd4544676a71ea7143b01a01b18a4d` | Make, JVM/Go, image, Compose와 branch-aware 문서 gate green |
| `backend-reliability-training` | `a28ad09ceea9bc28a1321601ff4202816ac00775` | `reliability-v1`: `7902d50106b40c1673a09f44f43c1c9a53b15eea` → `a28ad09ceea9bc28a1321601ff4202816ac00775` | `c4b34b46e3024f4f9ccef8b3c884184763622680` | Make, JVM/Go, reference 11개, Testcontainers와 Compose green |
| `sportsbook/shared-protocol` | `e0754c3a68ddce4f9ddef00e3dfb26b3ce53adbb` | `shared-v1`: `bd3ab9cb9df9ddce51aecd32008b8844781a184c` → `e0754c3a68ddce4f9ddef00e3dfb26b3ce53adbb` | `415bd8165e66fe8a83a32b4855f43038577a6eac` | 89 tests, Spotless, Checkstyle와 package green |
| `sportsbook/wallet-service` | `04c0c9706ed16ae6ba763aadd02d8eddd6bde536` | `wallet-v1.0.1`: `836c6b6823ae09ceca3ee7b0974f7752f08ef3f9` → `04c0c9706ed16ae6ba763aadd02d8eddd6bde536` | `dacb59158a50897c4de93ff780663862ce0ab407` | single shared 0.2 Maven 저장소에서 49 tests와 전체 verify green |
| `sportsbook/odds-feed-service` | `72316d951cc7e289ba2da04ef441ae94474c5009` | `odds-v1`: `763408693cf5277a3975dc56edeebb554237dfea` → `72316d951cc7e289ba2da04ef441ae94474c5009` | `be22dd966b7105023df38ff111c734dbd74b73d9` | 72 tests, 독립 endpoint 부하 gate 5/5와 전체 verify green |
| `sportsbook/betting-service` | `a4009f118b77f6739b591a3c2f87dcfd98c03c21` | `betting-v1`: `978da92ea9cafa5297fb3fdfa0eb7ee88f9680b0` → `a4009f118b77f6739b591a3c2f87dcfd98c03c21` | `4384d307461be43d3ae4761a8de60615a2594336` | 130 tests와 placement/reconciliation 10회 반복, 전체 verify green |
| `sportsbook/settlement-service` | `b117d7f71540f3bbd0586a07205634b0a7bf6a28` | `settlement-v1`: `ec83a25fe46716df48b2ac4922d269299febc780` → `b117d7f71540f3bbd0586a07205634b0a7bf6a28` | `a23f46df36b99ac4a016d8f2950ac4dd7f3af61e` | 80 tests, WON/LOST 10,000건 3회와 전체 verify green |
| `sportsbook/gateway` | `e955ee6ecf0e6b63d31bacfefc8657ff72271b8e` | `gateway-v1`: `ad65e266880ff10dd3ed6f9c5e406fe6fdb02713` → `e955ee6ecf0e6b63d31bacfefc8657ff72271b8e` | `912d87afc12516313f8ce320581fde77c8f89a60` | 22 tests와 전체 verify green |
| `sportsbook/admin-api` | `1c39c9cab5830214d5a99c20419e1f940ec6eeb2` | `admin-v1`: `51eb82ce43d2a9877cf15329c3daf6125aac306a` → `1c39c9cab5830214d5a99c20419e1f940ec6eeb2` | `26e58686b8d4f1bb45ef19ef5c5b492f540c2c88` | 28 tests와 전체 verify green |

위 10개 저장소는 독립 source release 단위로 green입니다. 기존 corpus는 byte-for-byte 보존했고, 현재
source graph용 corpus는 각 immutable learning branch에 추가했습니다. 공개 후 임시 archive와 중복
feature branch를 제거했고, 장기 ref는 `main`과 검증된 release별 immutable learning branch로
제한했습니다.

다음 두 저장소는 release가 아니라 재현 가치가 있는 **진단 상태**만 보존합니다. Diagnostic 열은
`annotated tag object → peeled candidate commit` 순서입니다.

| 저장소 | 원격 `main` | diagnostic | release 차단 근거 |
| --- | --- | --- | --- |
| `sportsbook/risk-service` | `db45a5611a2ac4554a78adbed759500af30d85c7` | `diagnostic-atomic-snapshot-v1-red`: `88da276f887292619500228c91e7f2fc8049c10b` → `49c6ec9e023ad0c831de563869b0c22ae46ffeee`<br>`diagnostic-codex-5.6-red`: `51707bec5cf5c6a7bb7ea750f95688f2247f1e2e` → `eca275e3de27222ee774b61c55d07c955a11694d` | fresh clone 정확성 98 tests·정적 검사·package는 green. 59,993 요청에서 errors 0%, checks 100%, p50 0.802 ms, p95 14.079 ms였지만 p99 64.654 ms와 drops 8로 최종 gate red. 요청당 EVALSHA 2회와 Kafka Stable·metadata error 0은 확인 |
| `sportsbook/orchestration` | `00581a4714ea167a7925da1e720792793a66fc5e` | `legacy-orchestration-v1-candidate`: `d470a54a076d82f2d20361bf344a82f9440bf79c` → `ec24b487e438db382a94832b168746eb83d200d9`<br>`diagnostic-codex-5.6-red`: `09d6127c6def47cb16c9775bb3da5aa1f684ceab` → `5767b959248da79104e47977d91a76c8fb95246c` | Risk release 부재와 historical manifest의 `PENDING` 때문에 strict cold E2E를 실행하지 않음. 비-release 후보의 실제 reference 검증은 37/37 green |

독립 release는 전체 12개 중 10개, Sportsbook은 9개 중 7개가 green입니다. Diagnostic과 legacy
candidate tag는 비-release이며 완료 수에 포함하지 않습니다. `risk-v1`, `orchestration-v1`,
`sportsbook-v1`은 만들지 않았고 service-tag 기반 strict cold E2E도 실행하지 않았습니다. Backend의
개발·정확성·성능 진단 **학습 사이클은 종료**했지만, Sportsbook 통합 release와 답지 없는 독립
mastery 평가는 **미완료**입니다.

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
Backend 트랙의 release 조건을 충족합니다. 현재 Training 3개와 Sportsbook source release 7개는
green이지만, Risk production release, Orchestration strict cold E2E와 `sportsbook-v1`이 없으므로 이
조건을 충족하지 않았습니다. 상태는 **학습 사이클 종료 · 통합 release 미완료**입니다.
