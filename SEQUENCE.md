# SEQUENCE.md — 학습 프로젝트 진행 (모듈 + 경로 선택)

> 자기완결 문서. 단일 고정 순서가 아니라 **독립 모듈(구획)을 목표에 맞게 켜고 끄는** 구조다.
> (구 `SEQUENCE_NOT_USE.md`는 구시대 유물 — 무시.)
> 전제: `notes/` 완성 (19개 프로젝트 139개 대장 가이드 + reference-impl). 이제 정하는 것은 **"어떤 모듈을, 어떤 순서로 켜는가"**.
> **기본 추천 경로 = A (JVM 취업 최단)** — 1차 커리어 타겟(해외 베팅사 JVM 백엔드, 6개월)에 맞춘 최단 경로. 정통 CS 완주를 원하면 **경로 B**(구 단일순서 그대로 보존).
>
> **실행 방법은 짝 문서 [LEARNING.md](LEARNING.md) 참조.** 이 문서는 *무엇을/어떤 순서로*만 다루고, 각 프로젝트를 **실제로 어떻게 도는가**(노트 정독 → reference-impl → 커밋 재구성 → L3 복기)는 LEARNING.md가 담당한다.

---

## 0. 원칙

1. **언어/프레임워크 우선**: 툴(Docker·Make·ESLint…)은 구현하며 익힌다. 언어/프레임워크는 코드를 쓰기 전에 알아야 하므로, 모듈의 뼈대는 언어/프레임워크 습득이다.
2. **대장이 모듈을 연다**: 한 스택의 "대장 노트"(가장 깊은 가이드)를 가진 프로젝트가 그 모듈의 **대장**이고 스캐폴딩이 가장 두껍다. 모듈은 대장으로 시작, 곁가지(같은 스택을 얕게 재사용)는 뒤.
3. **순서 결정은 두 층**: ① **글로벌** = "어떤 모듈을 켤지"(경로 선택). ② **로컬** = 모듈 안의 진행 순서(대장-first vs 곁가지 워밍업). 글로벌에서 난이도 걱정을 없애고, 어려운 점프(특히 C++ 98→17→20)는 로컬에서 흡수한다.
4. **생략 가능**: 모듈은 목표에 불필요하면 끈다(아래 "생략 가능" 열). **진입 선행만 지키면** 자유롭게 조합한다.

---

## 1. 모듈 카탈로그

| 모듈 | 대장 (+곁가지) | 핵심 습득 | 진입 선행 | 생략 가능 조건 | 캡스톤 경로 |
|---|---|---|---|---|---|
| **M0 작업규율** | linux-admin | Git·Conventional Commits·Markdown | — | Git·CLI 이미 능숙 | 권장 |
| **JVM 백엔드** ★ | backend-foundations (+backend-reliability) | Java 21·Spring Boot·MVC·Validation·Security·Test·JPA·Redis·동시성 (+Go·Kotlin DSL) | M0 | (1차 타겟이면 생략 불가) | **필수** |
| **인프라/운영** | container-stack (+network-routing-notes) | Docker·Compose·Nginx·POSIX shell (+서브넷/라우팅) | — (M0 권장) | 컨테이너 배포를 안 다룰 때 | **필수(Docker)** |
| **C 트랙** | small-shell (+format-printer·signal-message-bus·thread-dining·stack-sort) | C·프로세스/메모리·시그널/IPC·pthread 동시성·알고리즘 (+Python) | M0 권장 | 저수준/시스템 프로그래밍이 목표에 불필요 | ✗ |
| **C++ 트랙** | stl-container (+ray-scene-tracer) | C++98·템플릿·allocator·iterator·예외안전 (+그래픽스 연습) | C 트랙(언어 기초) | C++가 불필요 | ✗ |
| **시스템 서버** | game-server-reliability-training (+irc-relay-server·game-server-foundations-training) | C++17/20·Boost.Asio·소켓(epoll/kqueue)·C#/.NET·ASP.NET Core | C++ 트랙 | 고성능 C++ 서버·.NET이 불필요 | ✗* |
| **Node/TS 백엔드** | **pong-pong**(공개·입문 대장) (+grounded-travel·chatbot-evaluation) | TypeScript·Node·Fastify·WebSocket·PostgreSQL(풀스택) | M0 | JVM이 1차 → 생략 가능 (단 grounded의 **TS는 프론트의 선행**) | △ |
| **프론트엔드** | **portfolio-site**(공개·자족 입문 대장) (+frontend-reliability-training·frontend-foundations-training) | Next.js·React·Tailwind v4 (+React 심화: RSC·Router·Query·테스트) | TS | 백엔드 전용 목표(단 portfolio는 공개 필수) | ✗ |
| **모바일** | mobile-reliability-training (+mobile-foundations-training) | Kotlin·Jetpack Compose·Coroutines/Flow·Hilt·Retrofit/OkHttp·Room·WebSocket/STOMP·JWT refresh | M0 (Kotlin은 JVM과 시너지·강제 아님) | 모바일이 목표에 불필요 | sportsbook 모바일 클라이언트 |
| **캡스톤** | sportsbook | 코어=종합 적용(기존 139개 재사용) + **분산/운영 스택 신규**(Tier-1 노트 8개 → `sportsbook/orchestration/notes/`) | **JVM 백엔드 + 인프라** | — | — |

\* 시스템 서버의 **동시성 개념**은 캡스톤에 유용하나, 캡스톤의 동시성은 JVM 백엔드(backend-reliability)가 직접 커버하므로 critical path는 아니다.

**대장 정의와 입문 진입점**: `대장`은 그 스택의 **공개 대표 산출물 + 가장 두꺼운 통합**이다(반드시 가장 먼저 하는 프로젝트는 아니다). 신입 입문은 각 대장의 `docs/notes/systems/<x>.md`로 들어간다. 대장이 입문을 자족하지 못하는 스택은 **경유지**를 따른다:

| 스택 | 입문 진입점 | 비고 |
|---|---|---|
| C++ 트랙 | `stl-container/docs/notes/systems/cpp.md` | 자족(OOP·참조·RAII 온램프) → `notes/cpp98.md` 심화 |
| Node/TS | `pong-pong/docs/notes/systems/node-typescript.md` | 자족. grounded는 TS언어·프론트 선행 곁가지 |
| 프론트 | `portfolio-site/docs/notes/systems/react.md` | 자족(front-* 미이수 기준). React 심화는 frontend-reliability 곁가지 |
| 시스템 서버 | **경유지: irc-relay-server** `docs/notes/systems/cpp.md` | 대장 game-server-reliability는 C++20 심화. game-server 입문 진입은 보류 |

---

## 2. 의존성 — 강한 사슬은 2개뿐

대부분의 모듈은 M0에만 매달린 독립체다. 진짜 강제 사슬은 두 줄:

```
M0 ──┬───────────────────────────────────► (거의 모든 모듈의 권장 선행)
     │
     ├─ [사슬 1]  C 트랙 ─► C++ 트랙 ─► 시스템 서버
     ├─ [사슬 2]  Node/TS(grounded) ─► 프론트엔드
     ├─ [사슬 3]  모바일 foundations ─► 모바일 reliability
     ├─ JVM 백엔드        (M0만)
     ├─ 인프라/운영        (독립; M0 권장)
     └─ Node/TS 백엔드     (M0만)

캡스톤(sportsbook) ◄── JVM 백엔드  +  인프라/운영      (타이트하게 좁힌 선행)
sportsbook 모바일 클라이언트 ◄── 모바일 페어  +  sportsbook 백엔드(=위 캡스톤)
```

좁힌 의존(구 문서의 느슨한 선행 정리):
- ~~container-stack ← small-shell~~ : Docker/Compose는 C 셸 구현이 필요 없다. POSIX shell은 가볍게 익히면 됨.
- ~~sportsbook ← pong-pong~~ : 캡스톤의 PostgreSQL은 JVM 모듈의 **Spring Data JPA**로 충당된다. pong-pong은 PostgreSQL "대장 노트" 보유처일 뿐, JVM 캡스톤의 필수 선행은 아님.

---

## 3. 경로 프리셋

모듈을 의존성 안에서 조합한 것. 기본은 A.

### A. JVM 취업 최단 ★기본 (목표 직결)
`M0 → JVM 백엔드 → 인프라/운영 → 캡스톤`
- 프로젝트: **linux-admin → backend-foundations → backend-reliability → container-stack → sportsbook** (network-routing-notes는 선택).
- C/C++/시스템/Node/프론트 **전부 생략**. PostgreSQL은 JPA로. ~5개로 1차 타겟 + 캡스톤 도달.

### B. 정통 CS 완주 (구 단일순서 — 보존)
모듈 전체를 사슬 순서대로:
`M0 → C 트랙 → C++ 트랙 → 시스템 서버 → 인프라 → JVM → Node/TS → 프론트 → 캡스톤`

| # | 프로젝트 | 모듈 | 새로 배우는 핵심 | 선행 |
|---|---|---|---|---|
| 0 | linux-admin | M0 | Git/Commits/Markdown | — |
| 1 | small-shell | C | **C 언어**(프로세스/메모리/파서) | 0 |
| 2 | format-printer | C | 가변인자, ar | 1 |
| 3 | signal-message-bus | C | POSIX 시그널/IPC | 1 |
| 4 | thread-dining | C | pthread 동시성 | 1 |
| 5 | stack-sort | C | 알고리즘 + **Python** | 1 |
| 6 | stl-container | C++ | **C++98**(템플릿/자료구조) | 1 |
| 7 | ray-scene-tracer | C++ | (C++ 그래픽스 연습) | 6 |
| 8 | game-server-reliability-training | 시스템 서버 | **C++20 + C#/.NET** + Boost.Asio/ASP.NET | 6 |
| 9 | irc-relay-server | 시스템 서버 | **C++17** + 소켓(epoll/kqueue) | 6 |
| 10 | game-server-foundations-training | 시스템 서버 | C++20/C# 입문 | 9 (경사) / 8·9 (대장-first) |
| 11 | container-stack | 인프라 | **Docker/Compose** + POSIX shell | — |
| 12 | network-routing-notes | 인프라 | (서브넷/라우팅) | — |
| 13 | backend-foundations-training | JVM | **Java 21 + Spring Boot** | 0 |
| 14 | backend-reliability-training | JVM | Spring 신뢰성 + **Go** + Kotlin DSL | 13 |
| 15 | grounded-travel | Node/TS | **TypeScript**(+Fastify/Leaflet) | 0 |
| 16 | chatbot-evaluation | Node/TS | **Fastify** + SQLite | 15 |
| 17 | pong-pong | Node/TS | **PostgreSQL** + WebSocket(풀스택) | 15 |
| 18 | frontend-foundations-training | 프론트 | Zustand + React 기초 | 15 |
| 19 | frontend-reliability-training | 프론트 | **React** 심화 + RSC/Query/테스트 | 18 |
| 20 | portfolio-site | 프론트 | **Next.js** + Tailwind | 19 |
| 21 | sportsbook | 캡스톤 | (종합 적용) | 13·14·11 |

### C. 백엔드 풀폭 (JVM + Node 두 생태계)
`M0 → JVM 백엔드 → Node/TS 백엔드 → 인프라 → 캡스톤`
- DB 두 계열(Spring JPA ↔ raw PostgreSQL/SQLite)·서버 두 런타임을 모두. 프론트는 선택.

### D. 풀스택 1인개발 (산출물 먼저)
`M0 → TS(grounded-travel) → 프론트엔드 → JVM 백엔드 → 인프라 → 캡스톤`
- 웹 산출물을 빨리 만들고 싶을 때. Node 백엔드(chatbot·pong)는 선택.

### E. JVM 백엔드 + 모바일 (해외·다양성)
`A 경로(M0 → JVM → 인프라 → sportsbook) → 모바일 foundations → 모바일 reliability → sportsbook 모바일 클라이언트`
- 1차 타겟(해외 베팅 JVM)을 끝낸 뒤 같은 시스템에 네이티브 Android 클라이언트를 얹는다. Kotlin이 JVM 자산을
  복리로 쓰고(모바일 + Kotlin-백엔드), 캡스톤이 백엔드+게이트웨이+모바일을 하나의 시스템 서사로 묶는다.
  플랫폼 결정 근거·레포 상세: [mobile-track.md](mobile-track.md).

### F. 42 주도 + 백/프론트 병렬 (폭·동시진행) ※유일한 병렬 프리셋
선형인 A~E와 달리 **세 레인을 동시에** 굴린다 — 42/CS를 스파인(페이스 주도)으로, BACK·FRONT를 병렬 레인으로.
```
M0(linux-admin = 42 첫 과제 = 공통 게이트)
├─ 스파인 42/CS : small-shell → [C 곁가지] → stl-container → ray → irc → game-server-*
├─ 레인 BACK(JVM): backend-foundations → backend-reliability → container-stack → sportsbook
└─ 레인 FRONT    : grounded-travel(TS) → frontend-foundations → frontend-reliability → portfolio-site
```
- **게이트는 M0 하나.** 그 위로 세 레인은 서로 하드 의존이 없다(§2). 유일한 교차 선행: **FRONT는 grounded TS가 선행**(사슬 2)이라 grounded-travel을 FRONT 레인 맨 앞에 둔다(Node 백엔드 chatbot·pong은 선택, 생략 가능).
- **§0.4의 자유 조합**으로 성립하는 구성이다(모듈·의존 모델 불변). 기본 A보다 폭은 넓고 인지 부하는 크다 — 심화 peak(stl-container·game-server-reliability·backend-reliability·frontend-reliability)를 같은 시기에 겹치지 않게 **분산**한다.
- 동시 진행 캘린더(레인별 phase 배치·peak 분산표)·생략 옵션 정본: [parallel-track.md](parallel-track.md).

---

## 4. 모듈 상세 — 가이드 읽기 순서 (선행 블록 내부 순서)

노트는 **선행 학습 자료**다(가이드 = 개념 → 본 프로젝트 코드 분석 → 미니프로젝트 → 심화). 각 프로젝트는 그 `notes/`를 아래 순서로 **정독(스택 습득) → 짝 reference-impl로 손에 익힘 → 본 프로젝트 코드 직접 작성/복기**. 곁가지는 공유 스택을 재기술하지 않으니 자기 가이드만 빠르게.

> 표기: `` `A` → `B` `` = A 먼저. 그룹 라벨(언어/빌드/코어/…/보조)은 묶음이고 그룹 간에도 좌→우. **보조**는 후순위/선택. 파일명 자체는 알파벳순이라 디스크 정렬과 이 순서는 무관 — **이 순서를 따른다.**

### M0 작업규율
- **linux-admin** (대장): `git-cli` → `conventional-commits` → `markdown`

### C 트랙
경사 대안: format-printer(가벼움) 워밍업 → small-shell. 대장-first면 small-shell 정면돌파. 떼어쓰기: Python만 → stack-sort 단독.
- **small-shell** (대장): `c-language` → `gnu-readline`
- **format-printer**: `ar` → `c-test-harness`
- **signal-message-bus**: `posix-signal`
- **thread-dining**: `posix-pthread` → `posix-time-io` → `awk`(로그 검증 도구·보조)
- **stack-sort** (Python 대장): `python`

### C++ 트랙
대장-first: stl-container부터 시작한다(유일한 C++ 언어 진입 노트 `cpp.md`→`cpp98.md` 보유). ray-scene-tracer는 노트 없는 핸즈온이라 그 뒤.
- **stl-container** (대장): `cpp98`
- **ray-scene-tracer**: (노트 없음 — C++ 핸즈온 연습)

### 시스템 서버
C++ 점프 경사 대안: irc-relay(C++17) → game-server-foundations(입문) → game-server-reliability(심화). 대장-first면 reliability부터.
- **game-server-reliability** (대장·가장 두꺼움): 언어 `cpp20` → `csharp-dotnet8` · C++빌드 `cpp-compiler` → `cmake` → `cmake-fetchcontent` · .NET빌드 `dotnet-cli` → `msbuild` → `nuget` · 라이브러리 `boost-asio` → `spdlog` → `aspnet-core` · 추상화 `ms-di-abstractions` → `ms-logging-abstractions` · C++테스트 `googletest` → `ctest` → `sanitizers` · .NET테스트 `xunit` → `fluentassertions` · CI `github-actions`
- **irc-relay-server** (C++17 대장): `cpp17` → `posix-bsd-sockets` → `gnu-make` → `e2e-smoke-harness`
- **game-server-foundations**: `system-threading-channels` → `coverlet`(커버리지·보조)

### 인프라/운영
- **container-stack** (대장): 셸기반 `posix-shell` → `apt` → `curl` → `gosu` · 컨테이너 `docker` → `dockerfile` → `yaml` → `docker-compose` · 웹서버 `nginx-config` → `openssl` → `cgi-fcgi` → `php-fpm-pool` → `wordpress` → `wp-cli` · DB `mariadb-install-db` → `mariadb-config` → `mysqladmin`
- **network-routing-notes**: (노트 없음 — 서브넷/라우팅 개념·짧음)

### JVM 백엔드 ★
대장이 무겁다 → Spring 코어·웹·테스트 먼저, Security·Testcontainers는 2회독.
- **backend-foundations** (대장): 언어 `java-21` → `jdk-21` · 빌드 `gradle` → `spring-boot-gradle-plugin` · 코어 `spring-boot` → `jakarta-servlet-api` → `spring-web-mvc` · 기능 `spring-boot-starter-validation` → `spring-boot-starter-security` → `spring-data-commons-pagination` · 테스트 `spring-test` → `junit5` → `mockito` → `spring-security-test` → `testcontainers` · 보조 `go-toolchain` → `internal-go-cli-checkdocs`
- **backend-reliability** (곁가지): 빌드 `gradle-kotlin-dsl` · 영속성 `jakarta-persistence` → `spring-data-jpa` → `h2-database` → `spring-transaction` · 캐시 `redis` → `spring-data-redis` · 로깅 `slf4j` · 테스트 `assertj` · Go `go-language` → `go-net-http`

### Node/TS 백엔드
떼어쓰기: TS만 필요(프론트 선행) → grounded-travel만.
- **grounded-travel** (TS 대장): 언어 `typescript` → `zod` · 빌드 `tsc-project-references` → `vite` → `vitejs-plugin-react` · 연동 `ollama` → `overpass-api` · 지도UI `leaflet` → `react-leaflet` → `lucide-react`
- **chatbot-evaluation** (Fastify/SQLite 대장): 패키지 `pnpm` · 서버 `fastify` → `fastify-multipart` · DB `sql-sqlite` → `better-sqlite3` · 보조 `nanoid` → `html`
- **pong-pong** (PostgreSQL/WS 대장·풀스택): 런타임 `nodejs` → `tsx` · 서버 `fastify-cors` → `fastify-cookie` → `fastify-websocket` → `ws` · DB `postgresql` → `pg` → `kysely` · 배포 `caddy` · 테스트 `smoke-scripts` → `playwright`

### 프론트엔드
경사 대안: frontend-foundations(Zustand 워밍업) → reliability → portfolio. 대장-first면 reliability부터.
- **frontend-reliability** (React 대장): 언어 `javascript-esm` · 코어 `react` → `react-server-components` → `react-router-dom` · 데이터 `tanstack-react-query` → `msw` · 폼 `react-hook-form` → `hookform-resolvers` · 테스트 `vitest` → `testing-library` → `jsdom` → `jest-axe` · 도구 `eslint` → `typescript-eslint` → `storybook` · 스크립팅 `nodejs-scripting` → `repo-guard-scripts`(보조)
- **frontend-foundations** (Zustand 대장): `zustand`
- **portfolio-site** (Next.js 대장): 패키지/언어 `npm` → `tsx-jsx` → `json` · 프레임워크 `nextjs` · 빌드 `webpack` · 스타일 `postcss` → `tailwindcss-v4` → `css-tailwind-v4-directive` · 자원 `simple-icons`

### 모바일
대장-first면 mobile-reliability부터 가능하나, Kotlin/Compose가 처음이면 mobile-foundations 워밍업 권장. 입문 진입점 = mobile-foundations `notes/kotlin.md`(자족 언어 온램프). 상세 설계: [mobile-track.md](mobile-track.md).
- **mobile-foundations** (입문 대장·곁가지): 언어 `kotlin` · 플랫폼 `android-sdk` → `jetpack-compose` → `compose-navigation` → `viewmodel-stateflow` · 비동기 `kotlin-coroutines` · 연동 `retrofit-okhttp` → `room` · DI `hilt` · 스타일 `material3` · 테스트 `junit-mockk` → `compose-ui-test` · 빌드 `gradle-android-kts`
- **mobile-reliability** (대장·가장 두꺼움): 동시성 `kotlin-flow` → `structured-concurrency` · 영속/오프라인 `room-offline-first` → `workmanager` → `paging3` · 보안 `datastore-security` · 실시간 `okhttp-websocket-stomp` → `retry-backoff` · 인증 `jwt-auth-interceptor` → `problem-detail-mapping` · 성능 `compose-performance` · 테스트 `turbine` → `mockwebserver` → `espresso` → `screenshot-testing` → `hilt-testing`
- **sportsbook/mobile-client** (캡스톤): 종합 적용(페어 notes 재사용) + 신규 `stomp-over-spring-broker` · `oauth2-refresh-against-gateway`

---

## 5. 스택별 대장 (참조표)

트랙 진입 시 이 표의 대장부터.

| 스택 | 대장 (대장 노트 보유) | 곁가지(재사용) |
|---|---|---|
| C | small-shell | format-printer, signal-message-bus, thread-dining, stack-sort |
| C++98 | stl-container | ray-scene-tracer |
| C++17 | irc-relay-server | ray-scene-tracer |
| C++20 | game-server-reliability-training | game-server-foundations-training |
| C#/.NET | game-server-reliability-training | game-server-foundations-training |
| Python | stack-sort | (각 프로젝트 테스트 러너) |
| Java/Spring | backend-foundations-training | backend-reliability-training |
| Go | backend-reliability-training | backend-foundations-training |
| Kotlin DSL(Gradle) | backend-reliability-training | (Gradle 사용처) |
| TypeScript | grounded-travel | chatbot-evaluation, pong-pong, portfolio-site, frontend-* |
| JavaScript ESM | frontend-reliability-training | (각종 .mjs 스크립트) |
| React | frontend-reliability-training | frontend-foundations, portfolio, grounded-travel, pong-pong |
| Next.js | portfolio-site | frontend-foundations, frontend-reliability, pong-pong |
| Fastify | chatbot-evaluation | grounded-travel, pong-pong |
| PostgreSQL | pong-pong | backend-foundations/reliability |
| SQLite | chatbot-evaluation | grounded-travel |
| Docker/Compose | container-stack | chatbot, grounded, pong |
| POSIX shell | container-stack | small-shell·irc-relay 등 테스트 |
| Kotlin | mobile-foundations-training | mobile-reliability-training, sportsbook/mobile-client |
| Jetpack Compose | mobile-foundations-training | mobile-reliability-training |
| Android SDK | mobile-foundations-training | mobile-reliability-training |
| Coroutines/Flow | mobile-reliability-training | mobile-foundations-training |
| Room/오프라인 | mobile-reliability-training | mobile-foundations-training |
| WebSocket/STOMP(client) | mobile-reliability-training | sportsbook/mobile-client |
| Git/Markdown | linux-admin | 전 프로젝트 |

---

## 6. 캡스톤 진입 체크 (sportsbook)

JVM 백엔드(backend-foundations·reliability) + 인프라(container-stack) 완료 시 진입이 자연스럽다. 각 서비스의 in-process Spring 코어(web·JPA·Redis·validation·security 기본·test)는 **기존 139개 노트 재사용**으로 충당된다 — 그만큼은 "종합 적용".

단, sportsbook을 분산 시스템으로 만드는 **횡단 계층(분산/이벤트/운영/복원력)은 신규 학습**이며 139개에 없다. 이를 위한 **Tier-1 노트 8개**를 `sportsbook/orchestration/notes/`에 별도 작성했다 (9개 레포 공통 횡단 스택이라 서비스별 분산 대신 시스템 레포에 중앙집중; 각 가이드는 기존 4부 포맷 + 실행 가능 reference-impl). 권장 읽기 순서(빌드→이벤트→데이터→복원력→보안→게이트웨이→관측성):

`maven` → `spring-kafka` → `avro` → `flyway` → `resilience4j`(+bucket4j) → `spring-cloud-gateway` → `oauth2-resource-server` → `observability`

(Node·프론트·C/C++ 계열은 캡스톤의 선행이 아님 — 필요 폭에 따라 켜는 enrichment.)

---

## 7. 모바일 캡스톤 진입 체크 (sportsbook/mobile-client)

모바일 페어(mobile-foundations·mobile-reliability) + sportsbook 백엔드(§6 캡스톤) 완료 시 진입한다. 앱의 in-app 계층(Compose·Flow·Room·DI·테스트)은 **모바일 페어 노트 재사용**으로 충당된다("종합 적용"). 신규 학습은 **살아있는 분산 백엔드와의 클라이언트 통합** 2축 — gateway STOMP 브로커 구독/재연결과 RS256 JWT refresh — 이며, 캡스톤 신규 노트 `stomp-over-spring-broker`·`oauth2-refresh-against-gateway`(+선택 `idempotent-bet-contract`)로 다룬다.

소비할 API 표면(`/api/v1/*` REST + `/ws/v1/*` STOMP)·도메인 모델(shared-protocol 재기술)·출구 기준은 [mobile-track.md](mobile-track.md) §5에 정본으로 있다. (모바일 페어·C/C++/Node 계열은 sportsbook 백엔드 캡스톤(§6)의 선행이 아니다 — 모바일 클라이언트는 백엔드 완성 후 얹는 별도 캡스톤이다.)
