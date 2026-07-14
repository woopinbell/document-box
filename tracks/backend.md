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

## 2026-07-14 원격 release·학습 상태

다음 SHA는 source/learning 분리와 원격 게시가 끝난 뒤 실제 원격 ref를 다시 읽고 fresh clone에서
검증한 값입니다. Release 열은 `annotated tag object → peeled source commit` 순서입니다.

| 저장소 | `main` | release | `learning/<release>` | fresh-clone 검증 |
| --- | --- | --- | --- | --- |
| `backend-foundations-training` | `770d7ea217d5d53d1cb5e0aa8e5cf822fa4d8532` | `foundations-v2`: `5e7f089f7bc7ec60cb14f9010b3561f263f9b06f` → `770d7ea217d5d53d1cb5e0aa8e5cf822fa4d8532` | `f3ff5588485497150dbd382eb709777cf84de8f1` | 통합 `make check`, JVM/Go, standalone reference 17개, Compose와 문서 gate green |
| `backend-delivery-training` | `66b095b7bf34a114b99f14ea80bd75763ef60eed` | `delivery-v1`: `60d0f8dc26b6ca36e176fc3a315da1884096942b` → `66b095b7bf34a114b99f14ea80bd75763ef60eed` | `bf1a84e6eecd4544676a71ea7143b01a01b18a4d` | Make, JVM/Go, image, Compose와 branch-aware 문서 gate green |
| `backend-reliability-training` | `b0aad3cd7f74f98e9ab1c3b2a88b0f302bccc9fc` | `reliability-v2`: `159548ce66a01ca9fda47464872b82568966b904` → `b0aad3cd7f74f98e9ab1c3b2a88b0f302bccc9fc` | `634f9c27776ce10ccf9fe52d885d831abce4c0e2` | 통합 `make check`, JVM/Go, reference 11개, Testcontainers와 Compose green |
| `sportsbook/shared-protocol` | `e0754c3a68ddce4f9ddef00e3dfb26b3ce53adbb` | `shared-v1`: `bd3ab9cb9df9ddce51aecd32008b8844781a184c` → `e0754c3a68ddce4f9ddef00e3dfb26b3ce53adbb` | `415bd8165e66fe8a83a32b4855f43038577a6eac` | 89 tests, Spotless, Checkstyle와 package green |
| `sportsbook/wallet-service` | `04c0c9706ed16ae6ba763aadd02d8eddd6bde536` | `wallet-v1.0.1`: `836c6b6823ae09ceca3ee7b0974f7752f08ef3f9` → `04c0c9706ed16ae6ba763aadd02d8eddd6bde536` | `dacb59158a50897c4de93ff780663862ce0ab407` | single shared 0.2 Maven 저장소에서 62 tests와 전체 verify green |
| `sportsbook/odds-feed-service` | `72316d951cc7e289ba2da04ef441ae94474c5009` | `odds-v1`: `763408693cf5277a3975dc56edeebb554237dfea` → `72316d951cc7e289ba2da04ef441ae94474c5009` | `be22dd966b7105023df38ff111c734dbd74b73d9` | 72 tests와 publisher 111,982 events/s 검증 green. 독립 HTTP 부하 5/5는 주장하지 않음 |
| `sportsbook/betting-service` | `a4009f118b77f6739b591a3c2f87dcfd98c03c21` | `betting-v1`: `978da92ea9cafa5297fb3fdfa0eb7ee88f9680b0` → `a4009f118b77f6739b591a3c2f87dcfd98c03c21` | `4384d307461be43d3ae4761a8de60615a2594336` | 130 tests와 전체 verify green |
| `sportsbook/settlement-service` | `b117d7f71540f3bbd0586a07205634b0a7bf6a28` | `settlement-v1`: `ec83a25fe46716df48b2ac4922d269299febc780` → `b117d7f71540f3bbd0586a07205634b0a7bf6a28` | `a23f46df36b99ac4a016d8f2950ac4dd7f3af61e` | 80 tests와 replay focused 41 tests green. WON/LOST 10,000건 3회는 주장하지 않음 |
| `sportsbook/gateway` | `e955ee6ecf0e6b63d31bacfefc8657ff72271b8e` | `gateway-v1`: `ad65e266880ff10dd3ed6f9c5e406fe6fdb02713` → `e955ee6ecf0e6b63d31bacfefc8657ff72271b8e` | `912d87afc12516313f8ce320581fde77c8f89a60` | 22 tests와 전체 verify green |
| `sportsbook/admin-api` | `1c39c9cab5830214d5a99c20419e1f940ec6eeb2` | `admin-v1`: `51eb82ce43d2a9877cf15329c3daf6125aac306a` → `1c39c9cab5830214d5a99c20419e1f940ec6eeb2` | `26e58686b8d4f1bb45ef19ef5c5b492f540c2c88` | 28 tests와 전체 verify green |
| `sportsbook/risk-service` | `76c822b69bc816bad333479dfee79dcf3d19212b` | `risk-v1`: `12ae029455dacf1b73f10c64622d977d1b691544` → `76c822b69bc816bad333479dfee79dcf3d19212b` | `d262f52ccc845cef5f0912326cd90f69ce04697e` | 99 correctness tests·정적 검사·package green. 1,000 RPS 성능 qualification은 RED이므로 SLO 인증을 주장하지 않음 |
| `sportsbook/orchestration` | `564a83a57bd834870303688adb96450639c13bd2` | `orchestration-v1`: `51f8698a2123e9b5ce8052edad42a17405e8b3bb` → `564a83a57bd834870303688adb96450639c13bd2`<br>`sportsbook-v1`: `cfcde39f193dea8a92d30c64f96d9b13202d09bd` → 같은 source | `9d5fa541b765bb569c68d90444ef051bc63111b1` | manifest 9/9 post-tag, strict cold E2E 144 pass/0 fail, fresh-clone graph·learning gate green |

위 12개 저장소는 명시한 범위의 독립 source release 단위로 green입니다. 기존 corpus는 byte-for-byte 보존했고, 현재
source graph용 corpus는 각 immutable learning branch에 추가했습니다. 게시 후 임시 archive와 중복
feature branch를 제거했고, 장기 ref는 `main`과 검증된 release별 immutable learning branch로
제한했습니다.

Risk의 `risk-v1`은 correctness와 학습 surface를 고정한 release입니다. 그러나 1,000 RPS에서
`p99 < 30 ms`, errors 0, drops 0을 동시에 만족하는 성능 qualification은 반복 실행에서 RED였으므로,
이 release에 production SLO나 1,000 RPS 인증을 붙이지 않습니다. 기존 diagnostic tag는 실패 근거로
보존합니다.

Orchestration의 이전 main은 `pre-orchestration-v1` tag object
`2e794312c3c85b3f03ed7cc6fd66dca6f9acbfa6`에서
`00581a4714ea167a7925da1e720792793a66fc5e`로 peel되어 보존됩니다. 기존
`legacy-orchestration-v1-candidate`와 `diagnostic-codex-5.6-red`도 실패·전환 근거로 유지하되 release
완료 수에는 포함하지 않습니다. 독립 release 12/12와 Sportsbook 9/9가 green이며, 답지 없는 독립
incident 평가와 회상 checkpoint를 통과하는 curriculum mastery는 별도입니다.

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

세 훈련 저장소를 순서대로 완료하고 Sportsbook 9개 저장소가 통합 동작해야 합니다. 원격 main,
annotated release tag, 단일 immutable learning branch와 fresh-clone gate를 모두 통과하면 프로젝트
release 과정이 완료됩니다. 현재 Training 3개와 Sportsbook 9개 모두 원격 release·learning ref와
fresh-clone gate가 green이므로 Backend 프로젝트 release 과정은 완료됐습니다.

프로젝트 release 완료와 curriculum mastery는 별도입니다. 돈, 멱등, transaction/outbox와 saga를
코드 없이 설명하고 장애 시 보상·중복·정합성 경계를 방어한 뒤, Central Notes의 답지 없는 분산
incident 평가와 완료 직후·7일·30일 회상 checkpoint까지 통과해야 curriculum mastery가 완료됩니다.
Risk의 correctness release는 이 학습 경로에 사용할 수 있지만, 별도 1,000 RPS 성능 qualification은
RED이며 production SLO 근거로 사용할 수 없습니다.

## 완주 후 지원 데이터

트랙 완료와 채용 공고의 활성 상태를 섞지 않습니다. 정규직, 보상 하한 또는 검증 가능한 proxy를
통과한 현재 공고와 제출 근거는 [`../data/jobs/backend/`](../data/jobs/backend/)에서 확인하고 실제
제출 직전에 원문과 지원 버튼을 다시 엽니다. 공식 27개 프로젝트의 private 전환과 원격 전수 audit는
green이며, repository는 필요한 reviewer에게만 선택적으로 초대합니다.
