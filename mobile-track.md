# mobile-track.md — 모바일 트랙 기획 (3레포 설계 정본)

> 교차레포 문서. `SEQUENCE.md`(무엇을/순서)·`LEARNING.md`(어떻게)의 **모바일 모듈 상세 분기**다. 두 허브
> 문서는 모바일 모듈을 한 행으로 등록하고 상세는 이 문서를 가리킨다. 각 레포를 빌드할 세션은
> 루트 `CLAUDE.md` 표준 절차 + 이 문서의 해당 레포 절을 청사진으로 쓴다.
>
> **상태**: 기획 + 빈 골격 스캐폴드 완료. 코드·노트 본문·synthetic 커밋 히스토리·dual-form 문서는
> 아직 없음 — 레포별 빌드 세션이 채운다(한 레포 = 한 세션).

---

## 0. 무엇을 / 왜

프로그램은 도메인마다 `<도메인>-foundations-training`(가벼운 워밍업) + `<도메인>-reliability-training`
(가장 두꺼운 대장) **페어**를 가진다(backend·frontend·game-server). 캡스톤은 `sportsbook`. **모바일은
공백**이었다. 이 트랙은 그 공백을 **모바일 페어 2개 + 캡스톤 1개**로 메운다:

| 레포 | 역할 | 대장? | 규모(목표) |
|---|---|---|---|
| `mobile-foundations-training` | 앱빌드 기본기 워밍업 (frontend-foundations 대응) | 곁가지 | ~50–70 커밋 |
| `mobile-reliability-training` | 모바일 신뢰성 대장 (frontend-reliability 대응) | **대장** | ~90–120 커밋 |
| `sportsbook/mobile-client` | sportsbook 백엔드를 소비하는 네이티브 앱 (캡스톤) | — | ~40–60 커밋 |

## 1. 플랫폼 결정 — Android (Kotlin + Jetpack Compose)

사용자가 위임한 3기준(① 기존 seungwoo/ 자산 시너지=학습 용이성 ② 취업시장 다양성 ③ 해외취업 용이성)으로 판정.

- **① 시너지 — 압도적.** Kotlin은 JVM 언어. 사용자는 직전에 Java 21·Spring Boot·**Gradle Kotlin DSL**·
  JUnit5·Mockito를 완주했다. Kotlin 언어·Gradle 빌드·JUnit/MockK 테스트·Coroutines/Flow가 그대로 전이된다.
  캡스톤은 사용자가 **직접 설계한** Java/Spring 백엔드(REST + STOMP + RS256 JWT)와 **같은 도메인 모델**
  (Money/Odds/BetSlip)을 클라이언트 측에서 재기술한다 → 전이 최대. Flutter(Dart)·iOS(Swift)는 언어·빌드·
  테스트가 전부 콜드스타트이고 DTO 재사용이 0이다.
- **② 다양성 — 분산이 아니라 복리.** Kotlin 한 번의 투자가 **모바일 + Kotlin-백엔드**(Spring은 Kotlin
  1급 지원, 핀테크/베팅 해외 니치) 두 시장에 동시 적중한다. JVM 스파인을 *깊게* 하면서 플랫폼을 더한다.
  Flutter의 단일코드베이스 폭은 새 언어로 *발산*해 "해외 JVM 백엔드" 서사를 분절한다.
- **③ 해외취업 — 1순위 타겟과 정합.** SEQUENCE의 1차 타겟 = **해외 베팅사 JVM 백엔드**. 네이티브 Android
  베팅 클라이언트(실시간 odds WebSocket·보안 지갑·오프라인·멱등 베팅)는 **같은 고용주 카테고리**가 알아보는
  산출물이다. "해외 베팅: 백엔드 + 게이트웨이 + Android 클라이언트"라는 단일 시스템 서사가 가장 강하다.

**결론**: Android-Kotlin이 ①을 압도하고, 사용자 목표에서 ③ 우위이며, ②는 복리형 다양성. Flutter는 runner-up
(단일코드베이스 폭)이나 발산·콜드스타트로 탈락. iOS는 macOS/Xcode 종속 + 시너지 0으로 탈락.

**검증 비용 메모(AUDIT 연동)**: JUnit/MockK/**Robolectric** 단위테스트는 JVM에서 디바이스 없이 실행되어
AUDIT §3.4 "실제 실행" 게이트를 통과한다. Compose/Espresso **계측 테스트**는 에뮬레이터가 필요하므로 AUDIT의
**ENV-LIMIT**(Docker 미기동과 동급)으로 분류한다. 이 JVM-레벨 실행 가능성이 iOS 대비 Android의 실무 이점이다.

---

## 2. SEQUENCE / LEARNING에서의 위치

- **대장**: `mobile-reliability-training`(가장 두꺼운 통합). **곁가지/입문 진입점**: `mobile-foundations-training`
  (자족 입문 — `notes/kotlin.md`로 진입, frontend가 portfolio/foundations로 자족하는 것과 동형).
- **진입 선행**: M0(작업규율). Kotlin은 JVM 백엔드와 시너지지만 **강제 선행은 아님**(foundations의 `kotlin.md`가
  언어를 자족 온램프). 단 **캡스톤은 sportsbook 백엔드(JVM 캡스톤) 완료를 선행**으로 한다(소비 대상이라).
- **의존 사슬(SEQUENCE §2에 추가)**:
  ```
  [사슬 3]  모바일 foundations ─► 모바일 reliability
  sportsbook 모바일 클라이언트 ◄── 모바일 페어  +  sportsbook 백엔드(JVM 캡스톤)
  ```
- **경로 프리셋(SEQUENCE §3에 E 추가)** — **E. JVM 백엔드 + 모바일 (해외·다양성)**:
  `A 경로(M0→JVM→인프라→sportsbook) → 모바일 foundations → 모바일 reliability → sportsbook 모바일 클라이언트`.
- **스택별 대장(SEQUENCE §5)**: Kotlin·Jetpack Compose·Android·Coroutines/Flow → `mobile-reliability-training`
  (곁가지 `mobile-foundations-training`).
- **LEARNING §4 모듈별 변주 행**: 대장 mobile-reliability(→곁가지 foundations) · 커밋리듬 foundations=순차(2B)/
  reliability=triplet(2A) · 구조 표준(docs/notes 보유) · **L3 집중처 = 구조적 동시성·StateFlow 상태소유권·
  오프라인 캐시 정합성·토큰 refresh 레이스·WebSocket 재연결+멱등**.

---

## 3. 레포 1 — `mobile-foundations-training`

frontend-foundations(73커밋, "the preceding layer")의 모바일 대응. reliability 진입 전 정상적인 앱빌드 기본기.

- **스택**: Kotlin 언어 · Android SDK · Jetpack Compose · ViewModel/StateFlow · Compose Navigation ·
  Coroutines 기초 · Retrofit/OkHttp · Room 기초 · Hilt 기초 · Material 3 · JUnit5/MockK · Compose UI test ·
  Gradle(Kotlin DSL, Android).
- **`notes/<stack>.md`(4부 포맷) 순서**(=SEQUENCE §4 읽기 순서):
  `kotlin`(자족 언어 온램프·입문 진입점) → `android-sdk` → `jetpack-compose` → `compose-navigation` →
  `viewmodel-stateflow` → `kotlin-coroutines` → `retrofit-okhttp` → `room` → `hilt` → `material3` →
  `junit-mockk` → `compose-ui-test` → `gradle-android-kts`.
  각 노트는 짝 `notes/reference-impl/<stack>/`(빌드 가능한 최소 샘플).
- **커리큘럼 spine**(frontend-foundations 12스텝 대응): compose 기초 → 상태/이벤트 → 리스트/디테일/내비 →
  로컬저장(Room) → HTTP/JSON → API CRUD → 로딩·에러·빈상태 → 폼 검증 → 수동 세션/로그인 UI → 페이징 →
  이미지/파일 프리뷰. + 브랜치 미니 캡스톤(소형 앱 2–3개).
- **L3 집중처**: Compose 상태 소유권/recomposition, coroutine 생명주기(viewModelScope), Room 스키마.
- **커밋 리듬**: 순차(2B). **구조**: 표준(docs/notes 보유). 빌드 = `make`(gradlew 래핑) + `scripts/checkdocs`.

## 4. 레포 2 — `mobile-reliability-training` (대장)

frontend-reliability(114커밋, essential/advanced/sre/domain 트랙)의 모바일 대응. 모바일 신뢰성의 대장.

- **스택(심화)**: 구조적 동시성(Coroutines/Flow) · StateFlow/SharedFlow · Room 마이그레이션 + **offline-first** ·
  WorkManager(백그라운드 동기·재시도) · Paging 3 · DataStore + Android Keystore(토큰 보안) ·
  **WebSocket/STOMP 클라이언트**(OkHttp WebSocket / Krossbow) · 재시도·지수 백오프 ·
  **OAuth2/JWT refresh 인터셉터**(OkHttp Authenticator) · RFC 7807 에러 매핑 · 성능(recomposition·baseline
  profiles) · 테스트(Turbine·MockWebServer·Compose test·Espresso·MockK·스크린샷) · 관측성(Timber·StrictMode·ANR).
- **`notes/` 목록**(곁가지라 공유스택은 빠르게, 신뢰성 고유만 깊게):
  `kotlin-flow` · `structured-concurrency` · `room-offline-first` · `workmanager` · `paging3` ·
  `datastore-security` · `okhttp-websocket-stomp` · `retry-backoff` · `jwt-auth-interceptor` ·
  `problem-detail-mapping` · `compose-performance` · `turbine` · `mockwebserver` · `espresso` ·
  `screenshot-testing` · `hilt-testing`.
- **트랙**(frontend-reliability 대응 구조):
  - **essential**: 폼 검증 · async 상태(Flow) · 에러 경계 · 접근성 컴포넌트 · 페이징 · 낙관적 업데이트.
  - **advanced**: 오프라인 캐시(Room+WorkManager) · 실시간(WebSocket) · 디자인시스템 신뢰성 · 복합 필터 · 성능 예산.
  - **sre/resilience**: 카오스(네트워크 지연·손실 인터셉터) · 느린 API 경계 상태 · **토큰 refresh 레이스** ·
    **재연결 스톰** · trace·로깅.
  - **domain**: Compose 성능 예산 · 오프라인 전략 검증 · 대형 리스트 가상화 결함 탐지.
- **L3 집중처(폭발 반경 = "새벽 3시 레이스 컨디션"의 모바일판)**: 구조적 동시성/coroutine 취소 ·
  StateFlow 상태 소유권 · 오프라인 캐시 정합성 · 토큰 refresh/인증 레이스 · WebSocket 재연결 + 멱등.
- **커밋 리듬**: triplet(2A) 경향(frontend-reliability 동일) — 계약 덮고 직접 구현 → 대조 → 테스트. **구조**: 표준.

## 5. 레포 3 — `sportsbook/mobile-client` (캡스톤)

기존 sportsbook 백엔드(8/8 e2e 그린)를 소비하는 네이티브 Android 베팅 앱. sportsbook의 **10번째 독립
서브레포**. 코어 = **종합 적용**(페어 notes 재사용), 신규 = **살아있는 분산 백엔드와의 클라이언트 통합**.

**소비할 API 계약(검증된 실제 표면 — gateway `/api/v1/*`, `/ws/v1/*`):**

| 기능 | 엔드포인트 | 인증 | 신뢰성 포인트 |
|---|---|---|---|
| 이벤트 목록/상세 | `GET /api/v1/events`, `GET /api/v1/events/{eventId}` | 공개 | offline-first 캐시(Room), 페이징 |
| odds 조회 | `GET /api/v1/odds/{eventId}/{marketId}/{selectionId}` | 공개 | 캐시 + 실시간 갱신 병합 |
| 베팅 접수 | `POST /api/v1/bets` | JWT | **Idempotency-Key**, RFC 7807 매핑, 낙관적 UI + 롤백, "odds 변경→재확인" |
| 내 베팅 | `GET /api/v1/bets`, `GET /api/v1/bets/{betId}` | JWT | 페이징, 라이브 상태 갱신 |
| 지갑 잔고 | `GET /api/v1/wallet/balance` | JWT | 토큰 subject로 제약 |
| 실시간 odds | STOMP 핸드셰이크 `/ws/v1/odds` → 구독 `/topic/odds/{eventId}` | — | **재연결/백오프**, push lag 처리 |
| 베팅 상태 | STOMP 핸드셰이크 `/ws/v1/bets` → 구독 `/user/queue/bets`(userId=JWT sub) | JWT(CONNECT) | 라이브 정산(WON/LOST/VOID) 반영 |
| 인증 | RS256 JWT + refresh — **발급자는 시스템에 없음**(gateway는 검증만), login/refresh는 가정 seam | — | **OkHttp Authenticator 단일비행 refresh**, Keystore 보관 |

> 출처: `sportsbook/gateway`의 `routing/GatewayRoutes.java`(라우트) + `security/SecurityConfig.java`
> (공개 vs 인증 경로). 공개 = events/odds, 나머지는 JWT. gateway는 `X-User-*` 신뢰 헤더로 신원 전파.
>
> **STOMP 정합(빌드 세션 실소스 대조 — `sportsbook/mobile-client` ADR-0005, gateway `WebSocketStreamTest`):**
> `/ws/v1/odds`·`/ws/v1/bets`는 **핸드셰이크 엔드포인트**이고 실제 구독 목적지는
> `/topic/odds/{eventId}`(공개)·`/user/queue/bets`(인증 CONNECT, `convertAndSendToUser`로 JWT `sub`에 해소 —
> `{userId}`는 경로 파라미터가 아님). 또 시스템에 **토큰 발급자가 없어**(gateway=resource server 검증 전용)
> 클라의 login/refresh는 가정 seam이다. "이벤트의 market 목록" 엔드포인트도 없어 selection은 odds 스트림으로 발견.

- **도메인 모델**: `shared-protocol`의 Money / Odds / BetSlip / BetSelection / BetStatus / BetSlipType /
  MarketType / SettlementResult / ProblemDetail(RFC 7807) / ErrorCode 를 **Kotlin DTO로 재기술**
  (의존이 아니라 재기술 — 클라이언트는 JSON으로만 통신). 이미 설계해 본 모델이라 전이 최대.
- **캡스톤 신규 notes**(백엔드 `orchestration/notes` Tier-1 대응의 클라이언트 측, 2–3개):
  `stomp-over-spring-broker`(Spring STOMP 브로커 상대 클라이언트 구독/재연결) ·
  `oauth2-refresh-against-gateway`(게이트웨이 RS256 검증 + refresh 흐름) · (선택) `idempotent-bet-contract`.
  나머지 in-app 기능(Compose·Flow·Room·DI·테스트)은 페어 notes 재사용 = 종합 적용.
- **출구**: `sportsbook/orchestration`의 docker-compose로 백엔드 전 스택을 띄운 뒤, 앱이
  로그인 → 이벤트 브라우즈 → odds 실시간 → 베팅 접수 → 베팅 상태 라이브까지 동작. (선택) orchestration
  `e2e/`에 모바일 스모크 훅 추가.
- **ADR**: `docs/architecture/`에 클라이언트 결정 기록 — 오프라인 정책, 토큰 보관(Keystore vs EncryptedPrefs),
  WebSocket 재연결 전략, 멱등 베팅 키 생성.
- **커밋 리듬**: §3 보편 루프 그대로(서비스가 자기 `docs/commits/`를 가짐).

---

## 6. 빌드 세션 가이드 (각 레포를 나중에 어떻게 채우나)

CLAUDE.md "한 레포 = 한 세션". 각 레포 빌드 세션은:

1. 이 문서의 해당 절(스택·notes 목록·커리큘럼/트랙·L3)을 청사진으로 잡는다.
2. `notes/<stack>.md`를 4부 포맷으로 저작 + `reference-impl/` 작성(LEARNING §3 Step 1 대상).
3. 실제 Android 코드를 커리큘럼/트랙 순서로 구현하며 의미 있는 단위로 커밋(synthetic 타임라인).
4. 표준 절차로 `docs/commits/`(답지) 작성 → 실체 있는 커밋만 `docs/practice/` 파생(dual-form).
5. 검증: `make test`(JVM 단위), 계측 테스트는 ENV-LIMIT 명시. 통과 후 커밋·푸시(commit-policy).

**타임라인 배치**: synthetic 커밋 날짜는 기존 레포 window(≤2026-06-05) 이후 구간에, 모듈 의존
순서(foundations → reliability → 캡스톤)대로, 기존과 겹치지 않게(경계 분리) 둔다.

---

## 7. 관련 문서

[[SEQUENCE]] 모듈 카탈로그·경로·대장표 · [[LEARNING]] §4 모듈별 변주·보편 루프 ·
[[commit-policy]] 커밋·날짜 규율 · `sportsbook/gateway/README.md` API 표면 · `sportsbook/shared-protocol` 도메인 모델.
