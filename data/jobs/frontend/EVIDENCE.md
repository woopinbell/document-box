# Frontend 지원 증거 matrix

보상 하한 또는 조건부 보상 proxy를 통과한 정규직 공고의 요구사항을 기존 release에서 확인 가능한
증거로 연결하고, 현재 입증하지 못한 내용을 분리합니다. 2026-07-14 read-only remote/fresh-clone
감사 결과를 기준으로 합니다.

## 접근 상태와 release

| 저장소 | 기준 ref | 기록 시 접근 상태·최종 gate | 안전하게 주장할 수 있는 범위 |
|---|---|---|---|
| `frontend-delivery-training` | `delivery-v1` = main `95c4d9e` | 비공개 | Next delivery, asset pipeline, SEO·sitemap·robots, build와 Chromium E2E |
| `cloud-launch-training` | `cloud-launch-v1.0.1` = main `480e18b` | 비공개, fresh unit 15·emulator/config 6·production build·3-engine E2E 30·corpus object 8 green | Firebase claim·Firestore Rules·trusted Functions core·Cloudflare perimeter의 local 검증 경계 |
| `frontend-reliability-training` | `reliability-v1` = main `1988796` | 비공개 | React/Vite와 Next, TanStack Query·Zustand, async rollback, 접근성, unit/build/Playwright 6 smoke |
| `portfolio-site` | `portfolio-v3` = main `3f90d20` (`template-v3` = `82df0f2`) | 비공개, fresh lint/typecheck·unit 38·두 build·E2E 27 pass/1 expected skip green | Next content/schema/render 경계, 5개 design, route/query/native-details hydration/visual E2E 계약 |
| `web-boundary-inspector` | `codex-5.6` = main `237834c` | 비공개 | HTTP trace 3, event/fetch/history/cache/cookie/CORS/CSP browser 계약 |
| `pong-pong` | `codex-5.6` = main `b949bbe` | 비공개 | Next/React/Fastify/WS/Postgres, 서버 권위 게임 루프, auth/session과 shared schema |
| `irc-relay-server` | `codex-5.6` = main `6c76d84` | 비공개 | C++17 nonblocking socket, kqueue/epoll, partial frame/write, backpressure와 TCP smoke |

공식 42·Frontend 저장소 16개는 원격 ref audit 뒤 모두 private로 확인했습니다. 필요한 저장소만
private invitation 대상으로 사용합니다.
Learning branch는 답지·문제지의 근거이며 repository invitation의 첫 surface로 사용하지 않습니다.
Release tag 또는 main의 source·test·설계 문서를 먼저 연결합니다.

## 요구사항 → 증거

| 요구사항 | 주 증거 | 제출 문구의 경계 |
|---|---|---|
| React·Next·TypeScript·Vite | Frontend Delivery·Reliability, Portfolio | 개인 release에서 구현·검증했다고 씁니다 |
| TanStack Query·Zustand·비동기 정합성 | Reliability의 stale response, optimistic rollback과 mutation identity test | 실제 사용자 규모나 제품 KPI를 붙이지 않습니다 |
| 접근성·디자인 시스템 | Reliability의 modal/focus/axe와 design-state, Portfolio의 ARIA·reduced-motion E2E | 실제 디자이너 협업으로 표현하지 않습니다 |
| SEO·asset·release | Delivery의 image pipeline, metadata, sitemap/robots와 production build | Search Console 운영 실적은 아직 없습니다 |
| Managed BaaS·edge 권한 | Cloud Launch의 Auth claim, Firestore Rules emulator와 Cloudflare example config | Firebase/Cloudflare 실제 배포, AWS/GCP 운영·실트래픽 경험이라고 주장하지 않습니다 |
| Browser·HTTP·security | Web Boundary의 request correlation, proxy sanitization, event loop, Fetch abort, CORS/CSP | Release 게시 시 request 3/3·Chromium/Firefox/WebKit 21/21을 통과했습니다. 이번 지원 감사 재현은 설치된 request 3/3·Chromium 7/7까지만 확인했으므로 Firefox/WebKit은 제출 전에 다시 실행합니다. |
| 실시간·전체 구조 | Pong의 서버 권위 WS schema와 game loop, IRC의 실제 TCP smoke | Pong을 transaction-safe 또는 production OAuth 운영으로 표현하지 않습니다 |
| Linux·container | IRC, Container Stack, Linux Admin | Linux Admin은 documentation-first이며 실제 서버 운영 경력이 아닙니다 |
| C/C++·CS | IRC, STL Container, Thread Dining, Stack Sort, Small Shell | STL은 C++98 기반기이며 현대 C++ production 증거가 아닙니다 |

공개 접근을 제출 근거로 약속하지 않습니다. 코드 검토가 필요하면 Portfolio V3 publication commit,
route·presentation·native-details hydration characterization,
Playwright 계약, content schema와 five-design registry가 있는 `portfolio-site`를 우선 제한
초대합니다.

## 직무별 최소 packet

| 직무군 | 앞에 둘 증거 | 보조 증거 | 남은 gap |
|---|---|---|---|
| ESTgames·게임 웹 | Pong + IRC | STL·Thread·Stack + Portfolio | 게임 관심 설명, DB 기본기와 명절상여를 제외한 기본연봉 4,000만원 확인. Pong DB transaction은 주장 금지 |
| 위시스트·파트리지·더스윙 | Web Boundary + Reliability | Portfolio + Pong | 실제 media scale·WebGL·monitoring 운영과 조직 협업 경험은 분리하고 기본연봉 확인 |
| 토기·아하랩스·알로카도스 | Delivery + Reliability | Portfolio + Web Boundary | 실제 사용자 운영·타 직무 협업으로 과장하지 않기, 기본연봉 확인 |
| 코너스톤·옵스테크 | Pong + Reliability | Container Stack + Web Boundary | Python·Java·SQL·SI 경험을 Frontend release로 대체하지 않기 |
| 이너버즈·미리디·선데이띵커 | Pong + Reliability | Delivery + Container Stack | DB·AWS·제품 운영을 production 경력으로 쓰지 않고 직무 범위와 기본연봉 확인 |
| 데일리페이·메디스태프·사각·웨이센 | Reliability + Portfolio | Delivery + Web Boundary | 공고의 실무 연차와 개인 release를 구분하고 동등역량 인정 여부·기본연봉 확인 |
| 밀리만 Application | Reliability + STL·Thread | IRC + Portfolio | Electron·Nest·분산처리의 직접 구현 gap, 기본연봉 확인 |
| 채널톡 Software Engineer | 42 CS + Web Boundary | Reliability + Pong·IRC | 관련 전공 조건, PS/live coding, Frontend 배치 불확실성과 기본연봉 확인 |
| 셀타스퀘어·아키스케치·에이블리 | Reliability + Web Boundary | Portfolio + Pong | WebGL 직접 프로젝트는 현재 gap이며 보유했다고 주장하지 않고, 2년 실무·대규모 제품 경험으로 확대하지 않기 |
| 아우토크립트 | Web Boundary + IRC·STL | Reliability + Portfolio | cyber-security domain은 학습 근거와 제품 경험을 분리하고 기본연봉 확인 |
| 3년 동등역량 상향군 | Reliability + Portfolio | Delivery + Web Boundary + 직무별 42 release | 재현 가능한 CI 결과와 깊이 있는 설명이 없으면 동등역량을 주장하지 않고 기본연봉 확인 |
| Robert Walters Fullstack | Reliability + Portfolio | Delivery + Web Boundary + Container Stack | 복잡한 서비스 로직 유지보수, server·AWS 운영을 실무 경력으로 과장하지 않는 설명 |

## 현재 제출 중단 gate

아래가 모두 끝나기 전에는 `ready-to-submit`으로 올리지 않습니다.

1. 일부 42 release commit이 2026-07-17~21로 기록되어 있으므로 해당 날짜 전에는 그 history를
   채용 근거로 제시하지 않습니다.
2. Delivery, Reliability, Web Boundary와 직무별 필수 42 저장소 중 필요한 것만 reviewer에게 제한
   초대합니다.
3. Portfolio에 실제 연락처, profile asset, live deployment URL과 Delivery·Reliability·Web Boundary
   case study를 연결합니다. 현재는 placeholder, contact disabled, `case-study-only` 상태입니다.
4. 초대받은 reviewer가 확인할 수 있는 CI에서 lint/typecheck/unit/build/E2E green run을 만듭니다.
   로컬 green을 원격 CI로 바꾸어 쓰지 않습니다.
5. Web Boundary의 Firefox·WebKit browser binary를 설치하고 21/21을 다시 실행합니다.
6. Portfolio V3의 fresh hydration·visual E2E 27 pass/1 expected skip 근거를 보존하고, 지원 직전 선택한
   직무별 저장소 gate를 다시 실행합니다.
7. 이력서에는 문제 → 결정 → 검증 → 결과를 적되, 실무·프로덕션 트래픽·팀 KPI·운영 경력으로
   과장하지 않습니다.
8. 보상 proxy 후보는 recruiter screen에서 기본연봉 4,000만원 이상을 확인하고, 해외 full-time은
   employee/EOR인지 확인합니다. 조건을 충족하지 않으면 packet에서 제거합니다.

Repository invitation, Portfolio content publication과 CI 추가는 각각 별도 운영·release 작업입니다.
이 문서는 그 변경을 승인하거나 대신하지 않습니다.
