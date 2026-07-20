# Backend 학습 경로

42 통합 평가를 마친 뒤 시작하는 JVM 중심 트랙이다. Training 3개를 먼저 끝내고 Sportsbook 9개
저장소를 순서대로 진행한다.

```text
기초 → 배포 → 안정성
→ 공통 규약 → 지갑 → 위험 판단 → 배당 수신 → 베팅 → 정산 → 게이트웨이 → 관리자 → 통합 실행
→ 분산 장애 평가 → 복습 → 완료
```

먼저 `make preflight TRACK=backend`를 실행한다. 공통 진행법과 연습문제 선택법은
[학습 시작](README.md), Git 세부 절차는 [기술 안내](TECHNICAL_GUIDE.md)를 따른다. Spring 구현을 먼저
학습하고 Go 구현은 같은 계약을 더 작은 코드로 다시 확인할 때 사용한다.

<a id="stage-backend-foundations-training"></a>
## B1. backend-foundations-training

- **시작 조건:** [42 통합 평가](42.md#stage-42-incident)를 통과하고 완료 직후 복습을 기록한다.
- **먼저 읽을 것:** [Backend 기초 읽는 순서](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-backend-foundations-training)의 Java·Spring·DB·security·test·Go 범위를 읽는다.
- **저장소와 학습 자료:** [`backend-foundations-training`](https://github.com/woopinbell/backend-foundations-training), annotated 완성본 `foundations-v2.0.1`, 독자의 유일한 집필 branch `learning/current`; [학습 자료 목차](https://github.com/woopinbell/backend-foundations-training/blob/learning/current/docs/README.md), [연습문제 목록](https://github.com/woopinbell/backend-foundations-training/blob/learning/current/docs/practice/README.md), [해설 목록](https://github.com/woopinbell/backend-foundations-training/blob/learning/current/docs/commits/README.md).
- **직접 해볼 것:** [필수 학습 범위](README.md#공식-수행-범위)에 따라 문제 한 개를 고른다. 지정된 시작 커밋에 `study/backend-foundations-<ID>`를 만들고 request, validation, transaction, persistence와 인증 실패를 기록한다. 실패 test를 만든 뒤 해설과 비교하고 다시 구현한다.
- **현재 완성본 확인:** 별도의 깨끗한 작업 공간에서 Java 21, Gradle, Go와 Docker를 확인하고 `make check`를 실행한다. Docker를 쓸 수 없으면 통과한 검사와 환경 제한을 나눠 기록한다.
- **완료 조건:** HTTP 입력이 validation·transaction·DB·인증을 거쳐 응답으로 돌아오는 흐름과 Spring·Go 차이를 설명한다.
- **다음 과제:** [B2. backend-delivery-training](#stage-backend-delivery-training).

<a id="stage-backend-delivery-training"></a>
## B2. backend-delivery-training

- **시작 조건:** [B1. Backend 기초](#stage-backend-foundations-training)를 완료한다.
- **먼저 읽을 것:** [Backend 배포 읽는 순서](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-backend-delivery-training)의 build·container·Flyway와 프로젝트 배포 노트를 읽는다.
- **저장소와 학습 자료:** [`backend-delivery-training`](https://github.com/woopinbell/backend-delivery-training), annotated 완성본 `delivery-v1.0.1`, 독자의 유일한 집필 branch `learning/current`; [학습 자료 목차](https://github.com/woopinbell/backend-delivery-training/blob/learning/current/docs/README.md), [연습문제 목록](https://github.com/woopinbell/backend-delivery-training/blob/learning/current/docs/practice/README.md), [해설 목록](https://github.com/woopinbell/backend-delivery-training/blob/learning/current/docs/commits/README.md).
- **직접 해볼 것:** [필수 학습 범위](README.md#공식-수행-범위)에 따라 문제 한 개를 고른다. 지정된 시작 커밋에 `study/backend-delivery-<ID>`를 만들고 build 산출물, 실행 설정, migration, health와 log 실패를 기록한다. 해설과 비교한 뒤 다시 구현한다.
- **현재 완성본 확인:** 별도의 깨끗한 작업 공간에서 `make test && make build-spring && make build-go && make check-docs`를 실행하고 가능한 환경에서는 image·Compose 검사도 수행한다.
- **완료 조건:** 같은 산출물을 설정만 바꿔 실행하는 방법과 migration·readiness·log 확인 순서를 설명한다.
- **다음 과제:** [B3. backend-reliability-training](#stage-backend-reliability-training).

<a id="stage-backend-reliability-training"></a>
## B3. backend-reliability-training

- **시작 조건:** [B2. Backend 배포](#stage-backend-delivery-training)를 완료한다.
- **먼저 읽을 것:** [Backend 안정성 읽는 순서](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-backend-reliability-training)의 transaction·idempotency·Redis·test 범위를 읽는다.
- **저장소와 학습 자료:** [`backend-reliability-training`](https://github.com/woopinbell/backend-reliability-training), annotated 완성본 `reliability-v2.0.1`, 유일한 읽기 전용 자료 `learning/current`; [학습 자료 목차](https://github.com/woopinbell/backend-reliability-training/blob/learning/current/docs/README.md), [연습문제 목록](https://github.com/woopinbell/backend-reliability-training/blob/learning/current/docs/practice/README.md), [해설 목록](https://github.com/woopinbell/backend-reliability-training/blob/learning/current/docs/commits/README.md).
- **직접 해볼 것:** [필수 학습 범위](README.md#공식-수행-범위)에 따라 문제 한 개를 고른다. 지정된 시작 커밋에 `study/backend-reliability-<ID>`를 만들고 중복 요청, lock, outbox, retry, cache와 보상 실패를 재현한다. 결정적인 실패 test를 만든 뒤 해설과 비교하고 다시 구현한다.
- **현재 완성본 확인:** 별도의 깨끗한 작업 공간에서 Java 21·Gradle 8.10.2, Go와 Docker·Testcontainers를 확인하고 `make check`와 `make check-runtime`을 실행한다.
- **완료 조건:** transaction 경합, idempotency, outbox, cache와 rate limit의 상태 변화와 권위 경계를 설명한다.
- **다음 과제:** [B4. sportsbook-shared-protocol](#stage-sportsbook-shared-protocol).

<a id="stage-sportsbook-shared-protocol"></a>
## B4. sportsbook-shared-protocol

- **시작 조건:** [B3. Backend 안정성](#stage-backend-reliability-training)을 완료한다.
- **먼저 읽을 것:** [공통 규약 읽는 순서](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-sportsbook-shared-protocol)에서 새로 읽을 범위와 다시 볼 범위를 확인한다.
- **저장소와 학습 자료:** [`sportsbook-shared-protocol`](https://github.com/woopinbell/sportsbook-shared-protocol), 완성본 `shared-v1.0.1`, 읽기 전용 자료 `learning/shared-v1.0.1`; [연습문제 목록](https://github.com/woopinbell/sportsbook-shared-protocol/blob/learning/shared-v1.0.1/docs/practice-shared-v1.0.1/README.md), [해설 목록](https://github.com/woopinbell/sportsbook-shared-protocol/blob/learning/shared-v1.0.1/docs/commits-shared-v1.0.1/README.md).
- **직접 해볼 것:** [필수 학습 범위](README.md#공식-수행-범위)에 따라 문제 한 개를 고른다. 지정된 시작 커밋에 `study/shared-protocol-<ID>`를 만들고 event·error 규약과 호환성 실패를 consumer 관점에서 기록한다. 해설과 비교한 뒤 다시 구현한다.
- **현재 완성본 확인:** 별도의 깨끗한 작업 공간에서 Java·Maven으로 `./mvnw verify`를 실행해 schema와 호환성을 확인한다.
- **완료 조건:** schema·error·event 변경이 downstream을 깨뜨리는 경우와 호환 가능한 변경을 설명한다.
- **다음 과제:** [B5. sportsbook-wallet-service](#stage-sportsbook-wallet-service).

<a id="stage-sportsbook-wallet-service"></a>
## B5. sportsbook-wallet-service

- **시작 조건:** [B4. 공통 규약](#stage-sportsbook-shared-protocol)을 완료한다.
- **먼저 읽을 것:** [Wallet 읽는 순서](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-sportsbook-wallet-service)의 transaction·Redis 범위를 읽는다.
- **저장소와 학습 자료:** [`sportsbook-wallet-service`](https://github.com/woopinbell/sportsbook-wallet-service), 완성본 `wallet-v1.0.2`, 읽기 전용 자료 `learning/wallet-v1.0.2`; [학습 자료 목차](https://github.com/woopinbell/sportsbook-wallet-service/blob/learning/wallet-v1.0.2/docs/README.md), [연습문제 목록](https://github.com/woopinbell/sportsbook-wallet-service/blob/learning/wallet-v1.0.2/docs/practice-wallet-v1.0.2/README.md), [해설 목록](https://github.com/woopinbell/sportsbook-wallet-service/blob/learning/wallet-v1.0.2/docs/commits-wallet-v1.0.2/README.md).
- **직접 해볼 것:** [필수 학습 범위](README.md#공식-수행-범위)에 따라 문제 한 개를 고른다. 지정된 시작 커밋에 `study/wallet-<ID>`를 만들고 balance, lock, idempotency와 금액 기록 실패의 전후 상태를 남긴다. 중복 차감이 없음을 확인한 뒤 해설과 비교하고 다시 구현한다.
- **현재 완성본 확인:** 별도의 깨끗한 작업 공간에서 Java·Maven과 필요한 PostgreSQL·Redis로 `./mvnw verify`를 실행한다.
- **완료 조건:** 잔액·잠금·중복 방지·금액 기록의 불변식을 상태 전이로 설명한다.
- **다음 과제:** [B6. sportsbook-risk-service](#stage-sportsbook-risk-service).

<a id="stage-sportsbook-risk-service"></a>
## B6. sportsbook-risk-service

- **시작 조건:** [B5. Wallet](#stage-sportsbook-wallet-service)을 완료한다.
- **먼저 읽을 것:** [Risk 읽는 순서](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-sportsbook-risk-service)의 transaction·rate limit·Redis 범위를 읽는다.
- **저장소와 학습 자료:** [`sportsbook-risk-service`](https://github.com/woopinbell/sportsbook-risk-service), 완성본 `risk-v1.0.2`, 읽기 전용 자료 `learning/risk-v1.0.2`; [학습 자료 목차](https://github.com/woopinbell/sportsbook-risk-service/blob/learning/risk-v1.0.2/docs/README.md), [연습문제 목록](https://github.com/woopinbell/sportsbook-risk-service/blob/learning/risk-v1.0.2/docs/practice-risk-v1.0.2/README.md), [해설 목록](https://github.com/woopinbell/sportsbook-risk-service/blob/learning/risk-v1.0.2/docs/commits-risk-v1.0.2/README.md).
- **직접 해볼 것:** [필수 학습 범위](README.md#공식-수행-범위)에 따라 문제 한 개를 고른다. 지정된 시작 커밋에 `study/risk-<ID>`를 만들고 limit snapshot, replay, fail-closed와 판단 실패를 기록한다. 정확성을 반증해 본 뒤 해설과 비교하고 다시 구현한다.
- **현재 완성본 확인:** 별도의 깨끗한 작업 공간에서 Java·Maven, Redis와 Docker로 `./mvnw verify`를 실행한다.
- **완료 조건:** 판단 시점의 limit, replay와 Redis 원자성을 설명한다. 1,000 RPS `p99 < 30 ms`, errors=0, drops=0 성능 검사는 아직 RED이므로 통과했다고 기록하지 않는다.
- **다음 과제:** [B7. sportsbook-odds-feed-service](#stage-sportsbook-odds-feed-service).

<a id="stage-sportsbook-odds-feed-service"></a>
## B7. sportsbook-odds-feed-service

- **시작 조건:** [B6. Risk](#stage-sportsbook-risk-service)의 정확성 검사와 성능 미통과 상태를 구분해 기록한다.
- **먼저 읽을 것:** [Odds 읽는 순서](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-sportsbook-odds-feed-service), [Spring Kafka](https://github.com/woopinbell/sportsbook-orchestration/blob/learning/orchestration-v1/notes/spring-kafka.md), [Avro](https://github.com/woopinbell/sportsbook-orchestration/blob/learning/orchestration-v1/notes/avro.md)를 읽는다. Kafka·Avro의 정본은 Sportsbook 원본 notes다.
- **저장소와 학습 자료:** [`sportsbook-odds-feed-service`](https://github.com/woopinbell/sportsbook-odds-feed-service), 완성본 `odds-v1.0.1`, 읽기 전용 자료 `learning/odds-v1.0.1`; [학습 자료 목차](https://github.com/woopinbell/sportsbook-odds-feed-service/blob/learning/odds-v1.0.1/docs/README.md), [연습문제 목록](https://github.com/woopinbell/sportsbook-odds-feed-service/blob/learning/odds-v1.0.1/docs/practice-odds-v1.0.1/README.md), [해설 목록](https://github.com/woopinbell/sportsbook-odds-feed-service/blob/learning/odds-v1.0.1/docs/commits-odds-v1.0.1/README.md).
- **직접 해볼 것:** [필수 학습 범위](README.md#공식-수행-범위)에 따라 문제 한 개를 고른다. 지정된 시작 커밋에 `study/odds-<ID>`를 만들고 feed 정규화, 순서, publish와 replay 실패를 input·event 증거로 남긴다. 해설과 비교한 뒤 다시 구현한다.
- **현재 완성본 확인:** 별도의 깨끗한 작업 공간에서 Java·Maven과 필요한 broker로 `./mvnw verify`를 실행한다.
- **완료 조건:** 외부 feed가 정규화되고 순서를 유지하며 event로 재전송되는 경계를 설명한다.
- **다음 과제:** [B8. sportsbook-betting-service](#stage-sportsbook-betting-service).

<a id="stage-sportsbook-betting-service"></a>
## B8. sportsbook-betting-service

- **시작 조건:** [B7. Odds](#stage-sportsbook-odds-feed-service)를 완료한다.
- **먼저 읽을 것:** [Betting 읽는 순서](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-sportsbook-betting-service)의 transaction·outbox·reliability 범위를 읽는다.
- **저장소와 학습 자료:** [`sportsbook-betting-service`](https://github.com/woopinbell/sportsbook-betting-service), 완성본 `betting-v1.0.1`, 읽기 전용 자료 `learning/betting-v1.0.1`; [학습 자료 목차](https://github.com/woopinbell/sportsbook-betting-service/blob/learning/betting-v1.0.1/docs/README.md), [연습문제 목록](https://github.com/woopinbell/sportsbook-betting-service/blob/learning/betting-v1.0.1/docs/practice-betting-v1.0.1/README.md), [해설 목록](https://github.com/woopinbell/sportsbook-betting-service/blob/learning/betting-v1.0.1/docs/commits-betting-v1.0.1/README.md).
- **직접 해볼 것:** [필수 학습 범위](README.md#공식-수행-범위)에 따라 문제 한 개를 고른다. 지정된 시작 커밋에 `study/betting-<ID>`를 만들고 요청자, 중복 방지, Risk·Wallet 협력과 outbox 실패를 기록한다. 한 번만 수락·차감되는지 확인한 뒤 해설과 비교하고 다시 구현한다.
- **현재 완성본 확인:** 별도의 깨끗한 작업 공간에서 Java·Maven과 downstream stub·infra로 `./mvnw verify`를 실행한다.
- **완료 조건:** 베팅 요청의 권위와 Risk·Wallet·outbox 사이의 실패 경계를 설명하고 미검증 처리량을 성공으로 쓰지 않는다.
- **다음 과제:** [B9. sportsbook-settlement-service](#stage-sportsbook-settlement-service).

<a id="stage-sportsbook-settlement-service"></a>
## B9. sportsbook-settlement-service

- **시작 조건:** [B8. Betting](#stage-sportsbook-betting-service)을 완료한다.
- **먼저 읽을 것:** [Settlement 읽는 순서](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-sportsbook-settlement-service)의 transaction·outbox·replay 범위를 읽는다.
- **저장소와 학습 자료:** [`sportsbook-settlement-service`](https://github.com/woopinbell/sportsbook-settlement-service), 완성본 `settlement-v1.0.1`, 읽기 전용 자료 `learning/settlement-v1.0.1`; [학습 자료 목차](https://github.com/woopinbell/sportsbook-settlement-service/blob/learning/settlement-v1.0.1/docs/README.md), [연습문제 목록](https://github.com/woopinbell/sportsbook-settlement-service/blob/learning/settlement-v1.0.1/docs/practice-settlement-v1.0.1/README.md), [해설 목록](https://github.com/woopinbell/sportsbook-settlement-service/blob/learning/settlement-v1.0.1/docs/commits-settlement-v1.0.1/README.md).
- **직접 해볼 것:** [필수 학습 범위](README.md#공식-수행-범위)에 따라 문제 한 개를 고른다. 지정된 시작 커밋에 `study/settlement-<ID>`를 만들고 최종 결과, durable claim, Wallet 반영, outbox와 replay 실패를 기록한다. 중복·재처리 결과를 확인한 뒤 해설과 비교하고 다시 구현한다.
- **현재 완성본 확인:** 별도의 깨끗한 작업 공간에서 Java·Maven과 필요한 DB·broker로 `./mvnw verify`를 실행한다.
- **완료 조건:** WON·LOST 최종 상태, Wallet 반영과 재처리의 권위를 설명하고 처리량 미검증 상태를 분리한다.
- **다음 과제:** [B10. sportsbook-gateway](#stage-sportsbook-gateway).

<a id="stage-sportsbook-gateway"></a>
## B10. sportsbook-gateway

- **시작 조건:** [B9. Settlement](#stage-sportsbook-settlement-service)를 완료한다.
- **먼저 읽을 것:** [Gateway 읽는 순서](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-sportsbook-gateway)의 Spring MVC·Security 범위를 읽는다.
- **저장소와 학습 자료:** [`sportsbook-gateway`](https://github.com/woopinbell/sportsbook-gateway), 완성본 `gateway-v1.0.1`, 읽기 전용 자료 `learning/gateway-v1.0.1`; [학습 자료 목차](https://github.com/woopinbell/sportsbook-gateway/blob/learning/gateway-v1.0.1/docs/README.md), [연습문제 목록](https://github.com/woopinbell/sportsbook-gateway/blob/learning/gateway-v1.0.1/docs/practice-gateway-v1.0.1/README.md), [해설 목록](https://github.com/woopinbell/sportsbook-gateway/blob/learning/gateway-v1.0.1/docs/commits-gateway-v1.0.1/README.md).
- **직접 해볼 것:** [필수 학습 범위](README.md#공식-수행-범위)에 따라 문제 한 개를 고른다. 지정된 시작 커밋에 `study/gateway-<ID>`를 만들고 JWT, 신뢰할 identity, proxy와 fan-out 실패를 request·response·STOMP로 기록한다. 해설과 비교한 뒤 다시 구현한다.
- **현재 완성본 확인:** 별도의 깨끗한 작업 공간에서 Java·Maven과 HTTP·STOMP 환경으로 `./mvnw verify`를 실행한다.
- **완료 조건:** 외부 요청의 identity가 내부 서비스와 구독자에게 전달되는 신뢰 경계를 설명한다.
- **다음 과제:** [B11. sportsbook-admin-api](#stage-sportsbook-admin-api).

<a id="stage-sportsbook-admin-api"></a>
## B11. sportsbook-admin-api

- **시작 조건:** [B10. Gateway](#stage-sportsbook-gateway)를 완료한다.
- **먼저 읽을 것:** [Admin 읽는 순서](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-sportsbook-admin-api)의 Spring MVC·Security·test 범위를 읽는다.
- **저장소와 학습 자료:** [`sportsbook-admin-api`](https://github.com/woopinbell/sportsbook-admin-api), 완성본 `admin-v1.0.1`, 읽기 전용 자료 `learning/admin-v1.0.1`; [학습 자료 목차](https://github.com/woopinbell/sportsbook-admin-api/blob/learning/admin-v1.0.1/docs/README.md), [연습문제 목록](https://github.com/woopinbell/sportsbook-admin-api/blob/learning/admin-v1.0.1/docs/practice-admin-v1.0.1/README.md), [해설 목록](https://github.com/woopinbell/sportsbook-admin-api/blob/learning/admin-v1.0.1/docs/commits-admin-v1.0.1/README.md).
- **직접 해볼 것:** [필수 학습 범위](README.md#공식-수행-범위)에 따라 문제 한 개를 고른다. 지정된 시작 커밋에 `study/admin-<ID>`를 만들고 JWT·RBAC, audit, read model과 downstream 실패를 허용·거부 요청으로 기록한다. 해설과 비교한 뒤 다시 구현한다.
- **현재 완성본 확인:** 별도의 깨끗한 작업 공간에서 Java·Maven으로 `./mvnw verify`를 실행한다.
- **완료 조건:** 누가 어떤 관리 동작을 할 수 있는지와 audit·read model의 책임을 설명한다.
- **다음 과제:** [B12. sportsbook-orchestration](#stage-sportsbook-orchestration).

<a id="stage-sportsbook-orchestration"></a>
## B12. sportsbook-orchestration

- **시작 조건:** [B4](#stage-sportsbook-shared-protocol)부터 [B11](#stage-sportsbook-admin-api)까지 모든 독립 저장소를 완료한다.
- **먼저 읽을 것:** [통합 실행 읽는 순서](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-sportsbook-orchestration)의 Java·Spring 전체 색인과 Container·Infra 범위를 읽는다.
- **저장소와 학습 자료:** [`sportsbook-orchestration`](https://github.com/woopinbell/sportsbook-orchestration), 완성본 `orchestration-v1` (`sportsbook-v1` 별칭), 읽기 전용 자료 `learning/orchestration-v1`; [학습 자료 목차](https://github.com/woopinbell/sportsbook-orchestration/blob/learning/orchestration-v1/docs/README.md), [연습문제 목록](https://github.com/woopinbell/sportsbook-orchestration/blob/learning/orchestration-v1/docs/practice-orchestration-v1/README.md), [해설 목록](https://github.com/woopinbell/sportsbook-orchestration/blob/learning/orchestration-v1/docs/commits-orchestration-v1/README.md).
- **직접 해볼 것:** [필수 학습 범위](README.md#공식-수행-범위)에 따라 문제 한 개를 고른다. 지정된 시작 커밋에 `study/orchestration-<ID>`를 만들고 401·JWT, Risk fail-closed, WON·LOST, locked balance, payout·forfeit, replay와 readiness 실패를 기록한다. 해설과 비교한 뒤 다시 구현한다.
- **현재 완성본 확인:** 별도의 깨끗한 작업 공간에서 9개 저장소의 manifest와 Java·Maven, Docker·Compose를 준비하고 `scripts/validate-release-manifest.sh`, `scripts/build-all.sh`, `e2e/run-e2e.sh`를 실행한다.
- **완료 조건:** 고정 release build부터 인증·위험 판단·베팅·정산·재처리·readiness까지 전체 흐름을 설명한다.
- **다음 과제:** [B13. 분산 장애 평가](#stage-backend-incident).

<a id="stage-backend-incident"></a>
## B13. 분산 장애 평가

- **시작 조건:** Training 3개와 Sportsbook 9개 프로젝트를 모두 완료한다.
- **먼저 읽을 것:** [답지 없는 Backend 분산 장애 평가](https://github.com/woopinbell/central-notes/blob/main/assessments/backend-distributed-incident/README.md)의 contract와 금지 사항을 읽는다.
- **저장소와 학습 자료:** 별도 해설은 없다. starter·contract·evidence fixture만 사용한다.
- **직접 해볼 것:** 답지와 이전 제출을 닫고 transaction·idempotency, Redis, Kafka outbox·replay와 정산 부분 실패를 권위와 전달 문제로 나눠 진단한다.
- **현재 완성본 확인:** evidence, 가설, 반증, 읽기 전용 조사, rollback과 복구 기록이 같은 incident 실행을 가리키는지 확인한다.
- **완료 조건:** 자동 검사와 사람 평가를 통과하고 가설·반증·읽기 전용 조사·rollback·복구 결과를 남긴다. 완료 직후·7일·30일 복습을 수행한다.
- **다음 과제:** 30일 복습 뒤 [Backend 완료](#stage-backend-complete).

<a id="stage-backend-complete"></a>
## Backend 완료

다음 기록이 모두 있으면 완료다.

- 12개 프로젝트의 선택 문제, 실제 실패, 해설 확인 시각, 다시 구현한 결과와 현재 완성본 검사
- 분산 장애 평가의 자동·사람 검사
- 완료 직후·7일·30일 복습과 42 통합 평가의 30일 복습
- Risk 정확성과 미통과 성능 목표를 구분한 설명
- Orchestration manifest와 처음부터 다시 실행한 E2E 결과

취업 지원 자료가 필요할 때만 [Backend 공고 데이터](../data/jobs/backend/)를 사용한다. 공고 데이터는
학습 완료 조건이 아니며 지원 직전에 원문을 다시 확인한다.

[전체 학습 시작](README.md#트랙-선택)으로 돌아가 Frontend를 선택하거나 과정을 종료한다.
