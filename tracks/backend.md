# Backend 확장 트랙

42 통합 incident의 즉시 checkpoint 뒤 선택하는 JVM 중심 확장 트랙이다. Training 3개 뒤
Sportsbook의 9개 독립 저장소를 순서대로 진행한다.

```text
Foundations → Delivery → Reliability
→ Shared → Wallet → Risk → Odds → Betting → Settlement → Gateway → Admin → Orchestration
→ distributed incident → 회상 → 완료
```

시작 전에 `make preflight TRACK=backend`를 실행한다. `learning/*`는 읽기 전용이고 release tag는
baseline에만 사용한다. 실제 구현은 대표 practice 파일의 full 부모 commit에서 만든 `study/*`
branch에 둔다. 대표 항목의 결정 규칙과 선택 심화의 경계는
[공식 수행 범위](README.md#공식-수행-범위)를 따른다. Spring main track을 먼저
수행하고 Go 비교 구현은 같은 계약을 압축해 재확인하는 용도로 사용한다.

<a id="stage-backend-foundations-training"></a>
## 1. backend-foundations-training

- 이전 gate: [42 통합 incident](42.md#stage-42-incident)의 자동·사람 gate와 즉시 회상 통과.
- 저장소·ref: [`backend-foundations-training`](https://github.com/woopinbell/backend-foundations-training), release `foundations-v2.0.1`, learning `learning/foundations-v2.0.1`.
- Central 상세 목록: [backend-foundations-training 전체 읽기 순서](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-backend-foundations-training). 이 목록이 Java·Spring·persistence·security·test·Go 선수 범위를 확정한다.
- 빠른 노트: [Java/JDK/Build](https://github.com/woopinbell/central-notes/blob/main/java-spring/README.md#java-jdk-build), [Servlet/Spring Boot/MVC](https://github.com/woopinbell/central-notes/blob/main/java-spring/README.md#servlet-spring-boot-mvc).
- 수행 범위: [대표 practice 한 개와 카드 전체 gate](README.md#공식-수행-범위). 나머지는 선택 심화다.
- 프로젝트 노트: [current learning index](https://github.com/woopinbell/backend-foundations-training/blob/learning/foundations-v2.0.1/docs/README.md)에서 notes를 읽고 practice로 이동한다.
- Clean release gate: annotated release의 별도 clean worktree에서 Java 21, Maven, Go와 Docker를 확인하고 `make check`를 기록한다. Docker 불가 시 환경 제한과 통과한 하위 gate를 분리한다.
- 문제지: [current practice ledger](https://github.com/woopinbell/backend-foundations-training/blob/learning/foundations-v2.0.1/docs/practice-foundations-v2.0.1/README.md).
- 구현: 현재 practice의 full `부모 commit`에서 `study/backend-foundations-<ID>`를 만들고 request, validation, transaction, persistence와 auth 실패를 남긴다.
- 답지 개방: failing test와 자기 수정 근거 뒤 [answer ledger](https://github.com/woopinbell/backend-foundations-training/blob/learning/foundations-v2.0.1/docs/commits-foundations-v2.0.1/README.md)를 연다.
- Historical 무자료 gate: 현재 practice 파일이 명시한 시작 tree의 새 branch에서 그 파일의 구현 범위와 당시 검증 계약만 통과한다.
- 연결 설명: 선택한 foundation 변경이 current release의 request·validation·transaction·persistence·auth와 Spring/Go 비교 경계로 이어지는 근거를 설명한다.
- 다음: [backend-delivery-training](#stage-backend-delivery-training).

<a id="stage-backend-delivery-training"></a>
## 2. backend-delivery-training

- 이전 gate: HTTP→validation→transaction→response와 Go 비교 gate 완료.
- 저장소·ref: [`backend-delivery-training`](https://github.com/woopinbell/backend-delivery-training), release `delivery-v1.0.1`, learning `learning/delivery-v1.0.1`.
- Central 상세 목록: [backend-delivery-training 전체 읽기 순서](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-backend-delivery-training). 이 목록이 build·container·Flyway와 프로젝트 delivery 노트 범위를 확정한다.
- 빠른 노트: [Java Build](https://github.com/woopinbell/central-notes/blob/main/java-spring/README.md#java-jdk-build), [Container/Infra 읽는 순서](https://github.com/woopinbell/central-notes/blob/main/container-infra/README.md#읽는-순서).
- 수행 범위: [대표 practice 한 개와 카드 전체 gate](README.md#공식-수행-범위). 나머지는 선택 심화다.
- 프로젝트 노트: [current learning index](https://github.com/woopinbell/backend-delivery-training/blob/learning/delivery-v1.0.1/docs/README.md).
- Clean release gate: annotated release의 별도 clean worktree에서 Java/Maven, Go와 Docker로 `make test && make build-spring && make build-go && make check-docs`; 가능하면 image/Compose gate를 기록한다.
- 문제지: [current practice ledger](https://github.com/woopinbell/backend-delivery-training/blob/learning/delivery-v1.0.1/docs/practice-delivery-v1.0.1/README.md).
- 구현: 현재 practice의 full `부모 commit`에서 `study/backend-delivery-<ID>`를 만들고 artifact, runtime config, migration, health와 log 실패를 남긴다.
- 답지 개방: prod-like 실행·진단 근거 뒤 [answer ledger](https://github.com/woopinbell/backend-delivery-training/blob/learning/delivery-v1.0.1/docs/commits-delivery-v1.0.1/README.md)를 연다.
- Historical 무자료 gate: 현재 practice 파일이 명시한 시작 tree의 새 branch에서 그 파일의 구현 범위와 당시 검증 계약만 통과한다.
- 연결 설명: 선택한 delivery 변경이 current release의 artifact·runtime config·migration·health·log 경계로 이어지는 근거를 설명한다.
- 다음: [backend-reliability-training](#stage-backend-reliability-training).

<a id="stage-backend-reliability-training"></a>
## 3. backend-reliability-training

- 이전 gate: immutable artifact·runtime config·migration·readiness 경계 완료.
- 저장소·ref: [`backend-reliability-training`](https://github.com/woopinbell/backend-reliability-training), release `reliability-v2.0.1`, learning `learning/reliability-v2.0.1`.
- Central 상세 목록: [backend-reliability-training 전체 읽기 순서](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-backend-reliability-training). 이 목록이 transaction·idempotency·Redis·test 선수 범위를 확정한다.
- 빠른 노트: [Persistence, Transaction, Reliability, Redis](https://github.com/woopinbell/central-notes/blob/main/java-spring/README.md#persistence-transaction-reliability-redis), [Test](https://github.com/woopinbell/central-notes/blob/main/java-spring/README.md#test).
- 수행 범위: [대표 practice 한 개와 카드 전체 gate](README.md#공식-수행-범위). 나머지는 선택 심화다.
- 프로젝트 노트: [current learning index](https://github.com/woopinbell/backend-reliability-training/blob/learning/reliability-v2.0.1/docs/README.md).
- Clean release gate: annotated release의 별도 clean worktree에서 Java/Maven, Go와 Docker/Testcontainers로 `make check`를 기록한다.
- 문제지: [current practice ledger](https://github.com/woopinbell/backend-reliability-training/blob/learning/reliability-v2.0.1/docs/practice-reliability-v2.0.1/README.md).
- 구현: 현재 practice의 full `부모 commit`에서 `study/backend-reliability-<ID>`를 만들고 idempotency, lock, outbox, retry, cache, compensation 실패를 남긴다.
- 답지 개방: deterministic failing test와 state transition 근거 뒤 [answer ledger](https://github.com/woopinbell/backend-reliability-training/blob/learning/reliability-v2.0.1/docs/commits-reliability-v2.0.1/README.md)를 연다.
- Historical 무자료 gate: 현재 practice 파일이 명시한 시작 tree의 새 branch에서 그 파일의 구현 범위와 당시 검증 계약만 통과한다.
- 연결 설명: 선택한 failure pattern이 current release의 idempotency·transaction race·outbox·cache/rate-limit 경계로 이어지는 근거를 설명한다.
- 다음: [sportsbook-shared-protocol](#stage-sportsbook-shared-protocol).

<a id="stage-sportsbook-shared-protocol"></a>
## 4. sportsbook-shared-protocol

- 이전 gate: reliability 결정 패턴의 무자료 재구현 완료.
- 저장소·ref: [`sportsbook-shared-protocol`](https://github.com/woopinbell/sportsbook-shared-protocol), release `shared-v1.0.1`, learning `learning/shared-v1.0.1`.
- Central 상세 목록: [sportsbook-shared-protocol 전체 읽기 순서](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-sportsbook-shared-protocol). 이 단계에서 새로 읽을 노트와 다시 볼 범위를 따른다.
- 빠른 노트: [Java/Spring Persistence·Reliability](https://github.com/woopinbell/central-notes/blob/main/java-spring/README.md#persistence-transaction-reliability-redis).
- 수행 범위: [대표 practice 한 개와 카드 전체 gate](README.md#공식-수행-범위). 나머지는 선택 심화다.
- 프로젝트 노트: 별도 notes가 없으므로 Central 선수 노트 뒤 바로 current practice로 이동한다.
- Clean release gate: annotated release의 별도 clean worktree에서 Java/Maven으로 `./mvnw verify`를 실행해 schema·compatibility 결과를 기록한다.
- 문제지: [current practice ledger](https://github.com/woopinbell/sportsbook-shared-protocol/blob/learning/shared-v1.0.1/docs/practice-shared-v1.0.1/README.md).
- 구현: 현재 practice의 full `부모 commit`에서 `study/shared-protocol-<ID>`를 만들고 event/error contract와 compatibility 실패를 남긴다.
- 답지 개방: consumer 관점의 breakage 증거 뒤 [answer ledger](https://github.com/woopinbell/sportsbook-shared-protocol/blob/learning/shared-v1.0.1/docs/commits-shared-v1.0.1/README.md)를 연다.
- Historical 무자료 gate: 현재 practice 파일이 명시한 시작 tree의 새 branch에서 그 파일의 구현 범위와 당시 검증 계약만 통과한다.
- 연결 설명: 선택한 contract 변경이 current release의 schema·error·event compatibility와 downstream 경계로 이어지는 근거를 설명한다.
- 다음: [sportsbook-wallet-service](#stage-sportsbook-wallet-service).

<a id="stage-sportsbook-wallet-service"></a>
## 5. sportsbook-wallet-service

- 이전 gate: shared schema와 error/event compatibility 완료.
- 저장소·ref: [`sportsbook-wallet-service`](https://github.com/woopinbell/sportsbook-wallet-service), release `wallet-v1.0.2`, learning `learning/wallet-v1.0.2`.
- Central 상세 목록: [sportsbook-wallet-service 전체 읽기 순서](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-sportsbook-wallet-service). 이 단계에서 새로 읽을 노트와 다시 볼 범위를 따른다.
- 빠른 노트: [Transaction·Redis](https://github.com/woopinbell/central-notes/blob/main/java-spring/README.md#persistence-transaction-reliability-redis).
- 수행 범위: [대표 practice 한 개와 카드 전체 gate](README.md#공식-수행-범위). 나머지는 선택 심화다.
- 프로젝트 노트: [current learning index](https://github.com/woopinbell/sportsbook-wallet-service/blob/learning/wallet-v1.0.2/docs/README.md).
- Clean release gate: annotated release의 별도 clean worktree에서 Java/Maven과 필요한 PostgreSQL/Redis로 `./mvnw verify`를 기록한다.
- 문제지: [current practice ledger](https://github.com/woopinbell/sportsbook-wallet-service/blob/learning/wallet-v1.0.2/docs/practice-wallet-v1.0.2/README.md).
- 구현: 현재 practice의 full `부모 commit`에서 `study/wallet-<ID>`를 만들고 balance/lock/idempotency/ledger 실패와 전후 상태를 남긴다.
- 답지 개방: 중복 차감 반증과 transaction 증거 뒤 [answer ledger](https://github.com/woopinbell/sportsbook-wallet-service/blob/learning/wallet-v1.0.2/docs/commits-wallet-v1.0.2/README.md)를 연다.
- Historical 무자료 gate: 현재 practice 파일이 명시한 시작 tree의 새 branch에서 그 파일의 구현 범위와 당시 검증 계약만 통과한다.
- 연결 설명: 선택한 money transition이 current release의 balance·lock·idempotency·ledger 불변식으로 이어지는 근거를 설명한다.
- 다음: [sportsbook-risk-service](#stage-sportsbook-risk-service).

<a id="stage-sportsbook-risk-service"></a>
## 6. sportsbook-risk-service

- 이전 gate: wallet money/lock/idempotency 불변식 완료.
- 저장소·ref: [`sportsbook-risk-service`](https://github.com/woopinbell/sportsbook-risk-service), release `risk-v1.0.1`, learning `learning/risk-v1.0.1`.
- Central 상세 목록: [sportsbook-risk-service 전체 읽기 순서](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-sportsbook-risk-service). 이 단계에서 새로 읽을 노트와 다시 볼 범위를 따른다.
- 빠른 노트: [Transaction·rate limit·Redis](https://github.com/woopinbell/central-notes/blob/main/java-spring/README.md#persistence-transaction-reliability-redis).
- 수행 범위: [대표 practice 한 개와 카드 전체 gate](README.md#공식-수행-범위). 나머지는 선택 심화다.
- 프로젝트 노트: [current learning index](https://github.com/woopinbell/sportsbook-risk-service/blob/learning/risk-v1.0.1/docs/README.md).
- Clean release gate: annotated release의 별도 clean worktree에서 Java/Maven, Redis와 Docker 환경으로 `./mvnw verify` correctness 결과를 기록한다.
- 문제지: [current practice ledger](https://github.com/woopinbell/sportsbook-risk-service/blob/learning/risk-v1.0.1/docs/practice-risk-v1.0.1/README.md).
- 구현: 현재 practice의 full `부모 commit`에서 `study/risk-<ID>`를 만들고 limit snapshot, replay, fail-closed와 decision 실패를 남긴다.
- 답지 개방: correctness 반증 근거 뒤 [answer ledger](https://github.com/woopinbell/sportsbook-risk-service/blob/learning/risk-v1.0.1/docs/commits-risk-v1.0.1/README.md)를 연다.
- Historical 무자료 gate: 현재 practice 파일이 명시한 시작 tree의 새 branch에서 그 파일의 구현 범위와 당시 검증 계약만 통과한다.
- 연결 설명: 선택한 decision 변경이 current release의 limit snapshot·replay·fail-closed·Redis atomicity로 이어지는 근거를 설명한다. 별도 1,000 RPS `p99 < 30 ms`, errors=0, drops=0 qualification은 RED이므로 성공 사례로 주장하지 않는다.
- 다음: [sportsbook-odds-feed-service](#stage-sportsbook-odds-feed-service).

<a id="stage-sportsbook-odds-feed-service"></a>
## 7. sportsbook-odds-feed-service

- 이전 gate: Risk correctness와 성능 proof gap 분리 완료.
- 저장소·ref: [`sportsbook-odds-feed-service`](https://github.com/woopinbell/sportsbook-odds-feed-service), release `odds-v1.0.1`, learning `learning/odds-v1.0.1`.
- Central 상세 목록: [sportsbook-odds-feed-service 전체 읽기 순서](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-sportsbook-odds-feed-service). 이 단계에서 새로 읽을 노트와 다시 볼 범위를 따른다.
- 빠른 노트: [Spring Kafka](https://github.com/woopinbell/sportsbook-orchestration/blob/learning/orchestration-v1/notes/spring-kafka.md), [Avro](https://github.com/woopinbell/sportsbook-orchestration/blob/learning/orchestration-v1/notes/avro.md). Kafka·Avro의 정본은 Sportsbook 원본 notes다.
- 수행 범위: [대표 practice 한 개와 카드 전체 gate](README.md#공식-수행-범위). 나머지는 선택 심화다.
- 프로젝트 노트: [current learning index](https://github.com/woopinbell/sportsbook-odds-feed-service/blob/learning/odds-v1.0.1/docs/README.md).
- Clean release gate: annotated release의 별도 clean worktree에서 Java/Maven과 필요한 broker 환경으로 `./mvnw verify`를 기록한다.
- 문제지: [current practice ledger](https://github.com/woopinbell/sportsbook-odds-feed-service/blob/learning/odds-v1.0.1/docs/practice-odds-v1.0.1/README.md).
- 구현: 현재 practice의 full `부모 commit`에서 `study/odds-<ID>`를 만들고 feed normalization, ordering, publish/replay 실패를 남긴다.
- 답지 개방: input/event evidence 뒤 [answer ledger](https://github.com/woopinbell/sportsbook-odds-feed-service/blob/learning/odds-v1.0.1/docs/commits-odds-v1.0.1/README.md)를 연다.
- Historical 무자료 gate: 현재 practice 파일이 명시한 시작 tree의 새 branch에서 그 파일의 구현 범위와 당시 검증 계약만 통과한다.
- 연결 설명: 선택한 feed 변경이 current release의 normalization·ordering·publish·replay 경계로 이어지는 근거를 설명한다.
- 다음: [sportsbook-betting-service](#stage-sportsbook-betting-service).

<a id="stage-sportsbook-betting-service"></a>
## 8. sportsbook-betting-service

- 이전 gate: odds normalization·ordering·delivery 경계 완료.
- 저장소·ref: [`sportsbook-betting-service`](https://github.com/woopinbell/sportsbook-betting-service), release `betting-v1.0.1`, learning `learning/betting-v1.0.1`.
- Central 상세 목록: [sportsbook-betting-service 전체 읽기 순서](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-sportsbook-betting-service). 이 단계에서 새로 읽을 노트와 다시 볼 범위를 따른다.
- 빠른 노트: [Transaction·outbox·reliability](https://github.com/woopinbell/central-notes/blob/main/java-spring/README.md#persistence-transaction-reliability-redis).
- 수행 범위: [대표 practice 한 개와 카드 전체 gate](README.md#공식-수행-범위). 나머지는 선택 심화다.
- 프로젝트 노트: [current learning index](https://github.com/woopinbell/sportsbook-betting-service/blob/learning/betting-v1.0.1/docs/README.md).
- Clean release gate: annotated release의 별도 clean worktree에서 Java/Maven과 downstream stub/infra로 `./mvnw verify`를 기록한다.
- 문제지: [current practice ledger](https://github.com/woopinbell/sportsbook-betting-service/blob/learning/betting-v1.0.1/docs/practice-betting-v1.0.1/README.md).
- 구현: 현재 practice의 full `부모 commit`에서 `study/betting-<ID>`를 만들고 actor, idempotency, risk/wallet coordination, outbox 실패와 downstream effect를 남긴다.
- 답지 개방: 단일 수락·단일 차감 반증 계획 뒤 [answer ledger](https://github.com/woopinbell/sportsbook-betting-service/blob/learning/betting-v1.0.1/docs/commits-betting-v1.0.1/README.md)를 연다.
- Historical 무자료 gate: 현재 practice 파일이 명시한 시작 tree의 새 branch에서 그 파일의 구현 범위와 당시 검증 계약만 통과한다.
- 연결 설명: 선택한 placement 변경이 current release의 actor·idempotency·risk/wallet coordination·outbox 경계로 이어지는 근거를 설명하고 미증명 처리량을 성공으로 쓰지 않는다.
- 다음: [sportsbook-settlement-service](#stage-sportsbook-settlement-service).

<a id="stage-sportsbook-settlement-service"></a>
## 9. sportsbook-settlement-service

- 이전 gate: bet placement의 authority·downstream effect·outbox 경계 완료.
- 저장소·ref: [`sportsbook-settlement-service`](https://github.com/woopinbell/sportsbook-settlement-service), release `settlement-v1.0.1`, learning `learning/settlement-v1.0.1`.
- Central 상세 목록: [sportsbook-settlement-service 전체 읽기 순서](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-sportsbook-settlement-service). 이 단계에서 새로 읽을 노트와 다시 볼 범위를 따른다.
- 빠른 노트: [Transaction·outbox·replay](https://github.com/woopinbell/central-notes/blob/main/java-spring/README.md#persistence-transaction-reliability-redis).
- 수행 범위: [대표 practice 한 개와 카드 전체 gate](README.md#공식-수행-범위). 나머지는 선택 심화다.
- 프로젝트 노트: [current learning index](https://github.com/woopinbell/sportsbook-settlement-service/blob/learning/settlement-v1.0.1/docs/README.md).
- Clean release gate: annotated release의 별도 clean worktree에서 Java/Maven과 필요한 DB/broker로 `./mvnw verify`를 기록한다.
- 문제지: [current practice ledger](https://github.com/woopinbell/sportsbook-settlement-service/blob/learning/settlement-v1.0.1/docs/practice-settlement-v1.0.1/README.md).
- 구현: 현재 practice의 full `부모 commit`에서 `study/settlement-<ID>`를 만들고 terminal result, durable claim, wallet effect, outbox/replay 실패를 남긴다.
- 답지 개방: WON/LOST/duplicate/replay 증거 뒤 [answer ledger](https://github.com/woopinbell/sportsbook-settlement-service/blob/learning/settlement-v1.0.1/docs/commits-settlement-v1.0.1/README.md)를 연다.
- Historical 무자료 gate: 현재 practice 파일이 명시한 시작 tree의 새 branch에서 그 파일의 구현 범위와 당시 검증 계약만 통과한다.
- 연결 설명: 선택한 settlement 변경이 current release의 terminal result·durable claim·wallet effect·outbox/replay 경계로 이어지는 근거를 설명하고 처리량 proof gap을 분리한다.
- 다음: [sportsbook-gateway](#stage-sportsbook-gateway).

<a id="stage-sportsbook-gateway"></a>
## 10. sportsbook-gateway

- 이전 gate: settlement terminal state·wallet effect·reconciliation 경계 완료.
- 저장소·ref: [`sportsbook-gateway`](https://github.com/woopinbell/sportsbook-gateway), release `gateway-v1.0.1`, learning `learning/gateway-v1.0.1`.
- Central 상세 목록: [sportsbook-gateway 전체 읽기 순서](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-sportsbook-gateway). 이 단계에서 새로 읽을 노트와 다시 볼 범위를 따른다.
- 빠른 노트: [Spring MVC·Security 진입](https://github.com/woopinbell/central-notes/blob/main/java-spring/README.md#servlet-spring-boot-mvc).
- 수행 범위: [대표 practice 한 개와 카드 전체 gate](README.md#공식-수행-범위). 나머지는 선택 심화다.
- 프로젝트 노트: [current learning index](https://github.com/woopinbell/sportsbook-gateway/blob/learning/gateway-v1.0.1/docs/README.md).
- Clean release gate: annotated release의 별도 clean worktree에서 Java/Maven과 HTTP/STOMP 환경으로 `./mvnw verify`를 기록한다.
- 문제지: [current practice ledger](https://github.com/woopinbell/sportsbook-gateway/blob/learning/gateway-v1.0.1/docs/practice-gateway-v1.0.1/README.md).
- 구현: 현재 practice의 full `부모 commit`에서 `study/gateway-<ID>`를 만들고 JWT, trusted identity, proxy와 fan-out 실패를 남긴다.
- 답지 개방: request/response/STOMP와 identity 전파 증거 뒤 [answer ledger](https://github.com/woopinbell/sportsbook-gateway/blob/learning/gateway-v1.0.1/docs/commits-gateway-v1.0.1/README.md)를 연다.
- Historical 무자료 gate: 현재 practice 파일이 명시한 시작 tree의 새 branch에서 그 파일의 구현 범위와 당시 검증 계약만 통과한다.
- 연결 설명: 선택한 gateway 변경이 current release의 JWT·trusted identity·proxy·fan-out 경계로 이어지는 근거를 설명한다.
- 다음: [sportsbook-admin-api](#stage-sportsbook-admin-api).

<a id="stage-sportsbook-admin-api"></a>
## 11. sportsbook-admin-api

- 이전 gate: 단일 외부 진입점의 authn/identity/proxy/fan-out 경계 완료.
- 저장소·ref: [`sportsbook-admin-api`](https://github.com/woopinbell/sportsbook-admin-api), release `admin-v1.0.1`, learning `learning/admin-v1.0.1`.
- Central 상세 목록: [sportsbook-admin-api 전체 읽기 순서](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-sportsbook-admin-api). 이 단계에서 새로 읽을 노트와 다시 볼 범위를 따른다.
- 빠른 노트: [Spring MVC·Security](https://github.com/woopinbell/central-notes/blob/main/java-spring/README.md#servlet-spring-boot-mvc), [Test](https://github.com/woopinbell/central-notes/blob/main/java-spring/README.md#test).
- 수행 범위: [대표 practice 한 개와 카드 전체 gate](README.md#공식-수행-범위). 나머지는 선택 심화다.
- 프로젝트 노트: [current learning index](https://github.com/woopinbell/sportsbook-admin-api/blob/learning/admin-v1.0.1/docs/README.md).
- Clean release gate: annotated release의 별도 clean worktree에서 Java/Maven으로 `./mvnw verify`를 기록한다.
- 문제지: [current practice ledger](https://github.com/woopinbell/sportsbook-admin-api/blob/learning/admin-v1.0.1/docs/practice-admin-v1.0.1/README.md).
- 구현: 현재 practice의 full `부모 commit`에서 `study/admin-<ID>`를 만들고 JWT/RBAC, audit, read model과 downstream 실패를 남긴다.
- 답지 개방: 허용/거부 요청과 audit evidence 뒤 [answer ledger](https://github.com/woopinbell/sportsbook-admin-api/blob/learning/admin-v1.0.1/docs/commits-admin-v1.0.1/README.md)를 연다.
- Historical 무자료 gate: 현재 practice 파일이 명시한 시작 tree의 새 branch에서 그 파일의 구현 범위와 당시 검증 계약만 통과한다.
- 연결 설명: 선택한 admin 변경이 current release의 JWT/RBAC·audit·read model·downstream 경계로 이어지는 근거를 설명한다.
- 다음: [sportsbook-orchestration](#stage-sportsbook-orchestration).

<a id="stage-sportsbook-orchestration"></a>
## 12. sportsbook-orchestration

- 이전 gate: Shared부터 Admin까지 8개 독립 release의 무자료 gate 완료.
- 저장소·ref: [`sportsbook-orchestration`](https://github.com/woopinbell/sportsbook-orchestration), release `orchestration-v1` (`sportsbook-v1` alias), learning `learning/orchestration-v1`.
- Central 상세 목록: [sportsbook-orchestration 전체 읽기 순서](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-sportsbook-orchestration). 이 단계에서 새로 읽을 노트와 다시 볼 범위를 따른다.
- 빠른 노트: [Java/Spring 전체 index](https://github.com/woopinbell/central-notes/blob/main/java-spring/README.md#읽는-순서), [Container/Infra](https://github.com/woopinbell/central-notes/blob/main/container-infra/README.md#읽는-순서).
- 수행 범위: [대표 practice 한 개와 카드 전체 gate](README.md#공식-수행-범위). 나머지는 선택 심화다.
- 프로젝트 노트: [current learning index](https://github.com/woopinbell/sportsbook-orchestration/blob/learning/orchestration-v1/docs/README.md).
- Clean release gate: annotated release의 별도 clean workspace에서 9개 repository의 manifest release, Java/Maven, Docker/Compose를 준비하고 `scripts/validate-release-manifest.sh`, `scripts/build-all.sh`, `e2e/run-e2e.sh`를 기록한다.
- 문제지: [current practice ledger](https://github.com/woopinbell/sportsbook-orchestration/blob/learning/orchestration-v1/docs/practice-orchestration-v1/README.md).
- 구현: 현재 practice의 full `부모 commit`에서 `study/orchestration-<ID>`를 만들고 401/JWT, Risk fail-closed, WON/LOST, locked balance, payout/forfeit, replay/readiness 실패를 남긴다.
- 답지 개방: detached release build와 cold E2E evidence 뒤 [answer ledger](https://github.com/woopinbell/sportsbook-orchestration/blob/learning/orchestration-v1/docs/commits-orchestration-v1/README.md)를 연다.
- Historical 무자료 gate: 현재 practice 파일이 명시한 시작 tree의 새 branch에서 그 파일의 구현 범위와 당시 검증 계약만 통과한다.
- 연결 설명: 선택한 orchestration 변경이 current release의 manifest·detached build·401/JWT·Risk fail-closed·settlement·replay/readiness 통합 경계로 이어지는 근거를 설명한다.
- 다음: [Backend distributed incident](#stage-backend-incident).

<a id="stage-backend-incident"></a>
## 13. Backend distributed incident 평가

- 이전 gate: Training 3개와 Sportsbook 9개 무자료 gate·완료 artifact 기록.
- 평가: [answerless Backend distributed incident](https://github.com/woopinbell/central-notes/blob/main/assessments/backend-distributed-incident/README.md).
- 시작: project answers와 이전 제출을 닫고 starter·contract·evidence fixture만 사용한다.
- 실행: transaction/idempotency, Redis cache/rate limit, Kafka outbox/replay, settlement partial failure와 reconciliation을 authority·delivery 경계로 분리한다.
- 실패 artifact: evidence, 가설, falsifier, read-only probe, rollback과 repair gate를 진행 원장에 남긴다.
- 완료 gate: 자동 checker와 사람 rubric을 모두 통과한다. 정답/gold report는 Central에 commit하지 않는다.
- 회상: [Backend incident clock](https://github.com/woopinbell/central-notes/blob/main/assessments/recall-checkpoints.md#backend-distributed-incident-clock)의 즉시·7일·30일 checkpoint를 수행한다.
- 다음: 30일 checkpoint 뒤 [Backend 완료](#stage-backend-complete).

<a id="stage-backend-complete"></a>
## Backend 완료

다음 artifact가 모두 개인 진행 원장에 있으면 Backend curriculum mastery를 확정한다.

- 12개 프로젝트의 baseline, 대표 practice ID·선택 근거, 실패 근거, answer 확인 시각, 무자료 재구현과 최종 gate
- Backend distributed incident의 checker·사람 rubric 결과
- 완료 직후·7일·30일 무자료 회상 결과
- 병행한 42 incident 회상 clock의 30일 checkpoint
- Risk correctness와 미통과 1,000 RPS/p99 qualification을 구분한 설명
- Orchestration manifest와 cold E2E의 재현 가능한 evidence

취업 지원 자료를 고를 때만 [Backend 공고 데이터](../data/jobs/backend/)로 이동한다. 공고 데이터는
학습 완료 gate가 아니며 제출 직전에 원문을 다시 확인한다.

[전체 지도](README.md#분기와-완료)로 돌아가 Frontend를 선택하거나 과정을 종료한다.
