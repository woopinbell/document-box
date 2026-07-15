# Frontend 트랙

React/Next.js 구현 기본기에서 공개 납품, managed Cloud 경계, 실패 모드와 5-design Portfolio까지 이어지는 공식
Frontend 트랙입니다.

```text
frontend-foundations-training
→ frontend-delivery-training
→ cloud-launch-training
→ frontend-reliability-training
→ portfolio-site
```

별도 mobile 프로젝트는 이 공식 순서에 포함하지 않습니다.

## 공통 진행 방식

- `main`에서 실행 가능한 source/config/test, exercise 계약과 release 문서를 읽습니다.
- 해당 release의 immutable `learning/<release>`는 선택적 notes → answers → practices 순서로 게시합니다.
- 학습할 때는 공통 개념 또는 notes → practice → 실행/실패 → answer → 재구현 순서로 소비합니다.
- 문제지가 있으면 답지를 보기 전에 구현하고 실패 근거를 남긴 뒤 basis commit과 diff를 비교합니다.
- route, DOM, copy, CSS, asset, accessibility, RSC/hydration과 visual 결과를 공개 계약으로 봅니다.
- Ref와 corpus 규칙은 [`../commit-policy.md`](../commit-policy.md)와
  [`../docs-commit-note.md`](../docs-commit-note.md)를 따릅니다.

## 중앙 선수 학습과 mastery gate

Frontend에 진입하기 전에 [Web Foundations](https://github.com/woopinbell/central-notes/blob/main/web-foundations/README.md)의
IP/route/DNS, request lifecycle, HTML, CSS/rendering, browser runtime/security bridge를 완료하고,
[web-boundary-inspector](https://github.com/woopinbell/web-boundary-inspector)의 request/proxy 검사와
Chromium·Firefox·WebKit browser gate를 통과합니다. 공통 개념은 Central Notes에서 읽고 실행 가능한
release source와 재구현 corpus는 프로젝트의 `main`·`learning/codex-5.6`에서 사용합니다.
[42·Frontend capability matrix](https://github.com/woopinbell/central-notes/blob/main/CAPABILITY_MATRIX.md)에서
각 주제의 최초 노출과 직접 구현, 재사용, 독립 평가 연결을 확인합니다.

프로젝트 순서는 유지하면서 다음 평가를 삽입합니다.

- Frontend Reliability 완료 후:
  [unfamiliar-API transfer assessment](https://github.com/woopinbell/central-notes/blob/main/assessments/frontend-transfer/README.md)
- Portfolio 완료 후:
  [Web production regression assessment](https://github.com/woopinbell/central-notes/blob/main/assessments/web-production-regression/README.md)
- 각 평가 완료 직후와 7일·30일 후: 같은 rubric으로 무자료 전이와 지연 회상 checkpoint

이 gate는 이미 게시된 project release의 완료 판정을 바꾸지 않습니다. 이후 학습 실행에서 source를
처음 보는 조건에서도 URL state, async cancellation, rollback, 접근성과 browser 차이를 재구성하고,
성능·DNS/TLS/proxy·browser security evidence를 측정 → 원인 격리 → 최소 변경 → 검증 → rollback
폐루프로 닫을 수 있는지를 판정합니다. 실제 변경·staged deployment와 외부 review evidence가 없는
자동 checker 통과만으로는 Web production regression을 완료하지 않습니다.

## 1. `frontend-foundations-training`

Next.js App Router 단일 훈련 앱에서 정상적인 프론트 구현 기본기를 반복합니다.

- 범위: semantic page, component/props/state, controlled form, route, CRUD/storage, route handler,
  API fetching, loading/error/empty, Zod, session UI, pagination/filter와 upload preview
- 확장: board/commerce/task capstone과 RSC/cache/error/accessibility/optimistic bridge
- 실행 가능한 참고 구현: `notes/reference-impl/zustand`는 source `main`에 유지
- 현재 학습 ref: `learning/foundations-v1`
- L3: server/client boundary, serializable shared type, catalog source of truth, pagination bounds와
  storage lifecycle
- 검증: `make check-repo`, `make build`, production Playwright와 독립 Zustand package test/typecheck
- 완료: App Router 경계와 공유 data contract를 백지에서 설명하고 root/nested gate 통과

## 2. `frontend-delivery-training`

구현 기본기를 실제 외부 공개용 결과물로 넘기는 짧은 delivery bridge입니다.

- 범위: landing information architecture, capture/crop/blur/WebP pipeline, SEO metadata,
  sitemap/robots, Vercel/domain/Search Console release checklist
- Capstone: agency landing과 product/service landing
- 현재 학습 ref: `learning/delivery-v1`
- L3: page hierarchy, image quality/size budget, crawl/index surface, build와 deployment checklist 경계
- 검증: lint, typecheck, unit, exercise docs, production build와 Chromium E2E; learning에서는
  answer/practice pair gate 추가
- 완료: 외부 공개 가능한 route·asset·SEO surface가 build와 release checklist로 재현됨

Delivery는 새 product feature나 운영 side effect를 만드는 단계가 아닙니다. 실제 domain/DNS/Search
Console 변경은 별도 승인과 환경에서 수행합니다.

## 3. `cloud-launch-training`

Delivery 결과물을 managed BaaS와 edge perimeter 경계에서 검증하는 Cloud bridge입니다.

- 범위: Firebase Auth custom claim, Firestore owner/admin/server-owned 경계, fail-closed Rules,
  trusted Functions core, Cloudflare cache/WAF/rate-limit example과 다중 view
- 현재 source release: `cloud-launch-v1.0.1` = `main`
- 현재 학습 ref: `learning/cloud-launch-v1.0.1`
- L3: client claim과 Rules의 권한 source of truth, server-owned write, provider authorization과
  Cloudflare perimeter의 분리
- 검증: `make check`에서 metadata, unit 15, Firestore Emulator/config 6, production build와
  Chromium·Firefox·WebKit E2E 30 통과
- 학습 검증: `make check-learning`에서 answer/practice의 commit·tree·parent와 release 뒤
  notes → answers → practices path topology 통과
- 완료: local emulator의 allow/deny 증거와 실제 Firebase/Cloudflare 계정·배포 증거를 구분하고,
  pure Functions core를 배포된 trigger라고 과장하지 않음

기존 `cloud-launch-v1`과 `learning/cloud-launch-v1`은 immutable 과거 기록이며 현행 학습 진입점이
아닙니다. V1.0.1은 runtime 기능을 바꾸지 않고 v1 corpus의 source identity 오류를 교정합니다.
Cloud release는 실제 계정, DNS, credential, 비용 또는 production on-call을 증명하지 않습니다.
그 경험을 AWS·GCP 운영 경력이나 실트래픽 성과로 바꾸어 쓰지 않습니다.

## 4. `frontend-reliability-training`

React 19/Vite `react-main`과 Next.js App Router `next-sub`에서 실패 모드를 test로 봉인합니다.

- 범위: form/async/error boundary, accessible modal, URL table, optimistic rollback, i18n,
  virtualization, offline cache, design state, filtering, realtime ordering, performance budget와 RSC
- 현재 학습 ref: `learning/reliability-v1`
- L3: stale response, mutation identity/rollback, URL state ownership, local error/Suspense boundary,
  focus trap/restore, reconnect/dedup과 server/client serialization
- 검증: `pnpm check:repo`, lint, typecheck, React/Next unit, production build와 Playwright 6 smoke
- 완료: readiness timeout과 browser assertion, cache freshness, optimistic rollback과 RSC boundary를
  서로 다른 failure boundary로 설명하고 전체 gate 통과

Playwright는 필수 gate입니다. Lighthouse/Web Vitals 실측은 해당 browser 도구가 있는 환경의 보조
검사이며 Playwright를 대체하지 않습니다.

## 5. `portfolio-site`

공개 Portfolio와 학습 capstone을 하나로 통합한 최종 저장소입니다. 중립 reusable template와 개인
content publication을 분리하며 다음 5개 presentation system을 같은 validated content에서 렌더합니다.

1. **Design**: light product-oriented case study
2. **Classic**: dark terminal-led presentation
3. **Editorial**: asymmetric print folio, 기본 presentation
4. **Brutalist**: oversized modular grid와 hard contrast
5. **Cinematic**: image-led chapter와 restrained motion

### Release topology

- `template-vN`: profile/project/media를 제거한 중립 template
- `portfolio-vN == main`: content allowlist를 한 publication commit으로 적용한 deployable release
- `learning/portfolio-vN`: release별 전체 answers와 practices 두 commit
- 기존 `template-v1`·`portfolio-v1`·`learning/portfolio-v1`과 V2 ref는 immutable
- 현행 release: `template-v3` → `82df0f245e55120d87e45b3fe648ea6eee240f0e`,
  `portfolio-v3 == main` → `3f90d20cdc7a43b8af9e27414f3a58a2a70cf80e`
- 현행 학습 ref: `learning/portfolio-v3` → `7cfaae14b960cf5b89138660a2ebe8bf094db4af`

정확한 graph와 다음 release reset 방식은 `commit-policy.md`의 Portfolio topology를 따릅니다.

### Source 경계

- 공개 `portfolio.ts` façade는 유지하고 내부를 types/content/selectors/page-context로 분리
- 8개 App Router page의 request/searchParams → presentation/debug context → PageShell 흐름 통합
- `src/content/**`, `public/content/**`만 owner-controlled publication surface
- registry가 query와 navigation의 presentation 선택을 보존
- journey와 project link renderer의 중복을 공통 경계로 제거

### L3와 검증

- L3: content/schema/render 분리, template/content allowlist, five-design registry, static route context,
  stable query/href와 visual/accessibility 동일성
- 검증: `npm run lint`, `npm run typecheck`, `npm test`, `npm run build`, `npm run test:e2e`
- 다섯 design의 desktop/mobile visual snapshot, DOM·href·query·status, reduced-motion,
  hydration console/pageerror와 ARIA 결과를 함께 확인
- V3 fresh clone에서 neutral·personalized lint/typecheck, unit 38개, 두 build와 browser E2E
  27개 통과·의도된 1개 skip을 확인했으며 저장소는 private입니다.
- 완료: neutral template와 publication release 양쪽이 green이고 5개 design이 같은 content contract를
  보존하며 learning branch가 release에서 분리됨

## 트랙 완료

네 훈련 저장소를 순서대로 완료하고 `portfolio-site`의 template, deployable main, release tags와
learning branch를 검증합니다. RSC/state/data failure boundary와 content/template 경계를 백지에서
설명하고 5개 design을 실제 공개 가능한 상태로 검증하면 project release 과정이 완료됩니다. 중앙
unfamiliar-API assessment, Web production regression의 실제 운영·외부 review gate와 각 평가의
완료 직후·7일·30일 회상 checkpoint까지 통과하면 42·Frontend 범위의 curriculum mastery가
완료됩니다. Backend의 transaction, cache, queue와 distributed failure 평가는 완성된 Backend
트랙이 별도로 소유하며 Frontend mastery에 합산하지 않습니다.

## 완주 후 지원 데이터

트랙 완료 판정과 채용 공고의 활성 상태를 섞지 않습니다. 완주 후 정규직 여부와 보상 하한 또는
검증 가능한 보상 proxy를 통과한 현재 공고, 제출용 증거 조합은
[`../data/jobs/frontend/`](../data/jobs/frontend/)에서 확인하고, 실제 제출 직전에 회사 공식 페이지
또는 ATS를 다시 엽니다. 이 데이터는 Frontend 트랙의 학습 순서나 release 완료 판정을 변경하지 않습니다.
