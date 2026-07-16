# Frontend 확장 트랙

42 통합 incident의 즉시 checkpoint 뒤 선택하는 확장 트랙이다. 아래 순서를 유지한다.

```text
Foundations → Delivery → Cloud → Reliability → unfamiliar-API transfer
→ Portfolio → Web production regression → 회상 → 완료
```

시작 전에 `make preflight TRACK=frontend`를 실행한다. `learning/*`는 읽기 전용이고 release tag는
baseline에만 사용한다. 실제 구현은 [Basis 안내의 우선순위](README.md#basis-안내의-우선순위)에
따라 practice 또는 current ledger crosswalk에서 해소한 historical parent의 `study/*` branch에
둔다. 아래 카드의 “현재 practice의 full 부모 commit”도 이 해소 규칙을 줄여 쓴 표현이다. 대표
항목의 결정 규칙과 선택 심화의 경계는
[공식 수행 범위](README.md#공식-수행-범위)를 따른다. Portfolio의 통합 content
publication 과제만 neutral template tag에서 시작한다.

42를 이미 직접 구현했고 지원 자료를 먼저 준비해야 한다면
[Frontend 지원 준비 브리지](frontend-fast-track.md#route-frontend-application-bridge)를 선택할 수 있다.
Foundations 4개 review, Reliability 4개 hands-on과 Portfolio 병행 범위를 정확히 제한한 경로이며
`grants_mastery=false`다. 지원 gate 뒤에는 이 문서의
[Delivery 카드](#stage-frontend-delivery-training)로 복귀한다. 아래 정규 카드와 prev/next 순서는
그대로 유지된다.

<a id="stage-frontend-foundations-training"></a>
## 1. frontend-foundations-training

- 이전 gate: [42 통합 incident](42.md#stage-42-incident)의 자동·사람 gate와 즉시 회상 통과.
- 저장소·ref: [`frontend-foundations-training`](https://github.com/woopinbell/frontend-foundations-training), release `foundations-v1.0.1`, learning `learning/foundations-v1.0.1`.
- Central 상세 목록: [frontend-foundations-training 전체 읽기 순서](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-frontend-foundations-training). 이 목록이 language·React·build·state·test 선수 범위를 확정한다.
- 빠른 노트: [Frontend Language and Runtime](https://github.com/woopinbell/central-notes/blob/main/frontend-react/README.md#language-and-runtime), [React, Build, Routing](https://github.com/woopinbell/central-notes/blob/main/frontend-react/README.md#react-build-routing).
- 수행 범위: [대표 practice 한 개와 카드 전체 gate](README.md#공식-수행-범위). 나머지는 선택 심화다.
- 프로젝트 노트: [current learning index](https://github.com/woopinbell/frontend-foundations-training/blob/learning/foundations-v1.0.1/docs/README.md)에서 notes를 읽고 practice로 이동한다.
- Clean release gate: annotated release의 별도 clean worktree에서 Node/pnpm과 browser를 확인하고 `make check-repo && make build && make test-e2e`를 기록한다.
- 문제지: [current practice ledger](https://github.com/woopinbell/frontend-foundations-training/blob/learning/foundations-v1.0.1/docs/practice-foundations-v1.0.1/README.md).
- 구현: 현재 practice의 full `부모 commit`에서 `study/frontend-foundations-<ID>`를 만들고 route, server/client boundary, form/data/UI state 실패를 원장에 남긴다.
- 답지 개방: 자기 구현·expected/actual·검증 근거 뒤 [answer ledger](https://github.com/woopinbell/frontend-foundations-training/blob/learning/foundations-v1.0.1/docs/commits-foundations-v1.0.1/README.md)를 연다.
- Historical 무자료 gate: 현재 practice 파일이 명시한 시작 tree의 새 branch에서 그 파일의 구현 범위와 당시 검증 계약만 통과한다.
- 연결 설명: 선택한 UI 변경이 current release의 route·server/client·form·data/UI state 경계로 이어지는 근거를 설명한다.
- 다음: [frontend-delivery-training](#stage-frontend-delivery-training).

<a id="stage-frontend-delivery-training"></a>
## 2. frontend-delivery-training

- 이전 gate: Foundations 무자료 gate와 App Router/data contract 설명 완료.
- 저장소·ref: [`frontend-delivery-training`](https://github.com/woopinbell/frontend-delivery-training), release `delivery-v1.0.1`, learning `learning/delivery-v1.0.1`.
- Central 상세 목록: [frontend-delivery-training 전체 읽기 순서](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-frontend-delivery-training). 이 목록이 Central과 프로젝트 delivery 노트 범위를 확정한다.
- 빠른 노트: [Frontend Delivery](https://github.com/woopinbell/central-notes/blob/main/frontend-react/README.md#delivery).
- 수행 범위: [대표 practice 한 개와 카드 전체 gate](README.md#공식-수행-범위). 나머지는 선택 심화다.
- 프로젝트 노트: [current learning index](https://github.com/woopinbell/frontend-delivery-training/blob/learning/delivery-v1.0.1/docs/README.md).
- Clean release gate: annotated release의 별도 clean worktree에서 Node/pnpm, image와 Chromium 도구를 확인하고 `make check`를 기록한다. 실제 DNS/Search Console 변경은 하지 않는다.
- 문제지: [current practice ledger](https://github.com/woopinbell/frontend-delivery-training/blob/learning/delivery-v1.0.1/docs/practice-delivery-v1.0.1/README.md).
- 구현: 현재 practice의 full `부모 commit`에서 `study/frontend-delivery-<ID>`를 만들고 route·asset budget·SEO/build 실패와 release checklist를 남긴다.
- 답지 개방: 공개 surface와 검증 근거가 생긴 뒤 [answer ledger](https://github.com/woopinbell/frontend-delivery-training/blob/learning/delivery-v1.0.1/docs/commits-delivery-v1.0.1/README.md)를 연다.
- Historical 무자료 gate: 현재 practice 파일이 명시한 시작 tree의 새 branch에서 그 파일의 구현 범위와 당시 검증 계약만 통과한다.
- 연결 설명: 선택한 delivery 변경이 current release의 route·asset budget·SEO·build·release checklist로 이어지는 근거를 설명한다.
- 다음: [cloud-launch-training](#stage-cloud-launch-training).

<a id="stage-cloud-launch-training"></a>
## 3. cloud-launch-training

- 이전 gate: Delivery의 deployable artifact·SEO·release surface 완료.
- 저장소·ref: [`cloud-launch-training`](https://github.com/woopinbell/cloud-launch-training), release `cloud-launch-v1.0.1`, learning `learning/cloud-launch-v1.0.1`.
- Central 상세 목록: [cloud-launch-training 전체 읽기 순서](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-cloud-launch-training). 이 목록이 request lifecycle·browser security·Next·Playwright와 프로젝트 Cloud 노트 범위를 확정한다.
- 빠른 노트: [Request lifecycle](https://github.com/woopinbell/central-notes/blob/main/web-foundations/request-lifecycle.md), [Browser runtime·security](https://github.com/woopinbell/central-notes/blob/main/web-foundations/browser-runtime-security.md).
- 수행 범위: [대표 practice 한 개와 카드 전체 gate](README.md#공식-수행-범위). 나머지는 선택 심화다.
- 프로젝트 노트: [current learning index](https://github.com/woopinbell/cloud-launch-training/blob/learning/cloud-launch-v1.0.1/docs/README.md).
- Clean release gate: annotated release의 별도 clean worktree에서 Node/pnpm, Java, Firebase Emulator와 세 browser를 확인하고 `make check`를 기록한다. 실제 credential·비용·DNS는 필수 gate가 아니다.
- 문제지: [current practice ledger](https://github.com/woopinbell/cloud-launch-training/blob/learning/cloud-launch-v1.0.1/docs/practice/README.md).
- 구현: 현재 practice의 full `부모 commit`에서 `study/cloud-launch-<ID>`를 만들고 Rules allow/deny, Functions trust, Cloudflare perimeter 실패를 남긴다.
- 답지 개방: emulator와 config 증거가 생긴 뒤 [answer ledger](https://github.com/woopinbell/cloud-launch-training/blob/learning/cloud-launch-v1.0.1/docs/commits/README.md)를 연다.
- Historical 무자료 gate: 현재 practice 파일이 명시한 시작 tree의 새 branch에서 그 파일의 구현 범위와 당시 검증 계약만 통과한다.
- 연결 설명: 선택한 Cloud 변경이 current release의 Rules·Functions·Cloudflare trust boundary로 이어지는 근거와 client claim/authority 차이를 설명한다.
- 다음: [frontend-reliability-training](#stage-frontend-reliability-training).

<a id="stage-frontend-reliability-training"></a>
## 4. frontend-reliability-training

- 이전 gate: managed BaaS·Rules·edge perimeter trust boundary 완료.
- 저장소·ref: [`frontend-reliability-training`](https://github.com/woopinbell/frontend-reliability-training), release `reliability-v1.0.1`, learning `learning/reliability-v1.0.1`.
- Central 상세 목록: [frontend-reliability-training 전체 읽기 순서](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-frontend-reliability-training). 이 목록이 RSC·router·query·form·a11y·test·quality 범위를 확정한다.
- 빠른 노트: [Frontend Testing and Quality](https://github.com/woopinbell/central-notes/blob/main/frontend-react/README.md#testing-and-quality).
- 수행 범위: [대표 practice 한 개와 카드 전체 gate](README.md#공식-수행-범위). 나머지는 선택 심화다.
- 프로젝트 노트: [current learning index](https://github.com/woopinbell/frontend-reliability-training/blob/learning/reliability-v1.0.1/docs/README.md).
- Clean release gate: annotated release의 별도 clean worktree에서 Node/pnpm과 Playwright를 확인하고 `make lint && make typecheck && make test && make build && make test-e2e`를 기록한다.
- 문제지: [current practice ledger](https://github.com/woopinbell/frontend-reliability-training/blob/learning/reliability-v1.0.1/docs/practice-reliability-v1.0.1/README.md).
- 구현: 현재 practice의 full `부모 commit`에서 `study/frontend-reliability-<ID>`를 만들고 stale response, rollback, URL state, focus/reconnect 실패를 남긴다.
- 답지 개방: deterministic failing test와 자기 수정 뒤 [answer ledger](https://github.com/woopinbell/frontend-reliability-training/blob/learning/reliability-v1.0.1/docs/commits-reliability-v1.0.1/README.md)를 연다.
- Historical 무자료 gate: 현재 practice 파일이 명시한 시작 tree의 새 branch에서 그 파일의 구현 범위와 당시 검증 계약만 통과한다.
- 연결 설명: 선택한 reliability 변경이 current release의 stale response·rollback·URL state·focus/reconnect 경계로 이어지는 근거를 설명한다.
- 다음: [unfamiliar-API transfer](#stage-frontend-transfer).

<a id="stage-frontend-transfer"></a>
## 5. unfamiliar-API transfer 평가

- 이전 gate: Reliability의 async/state/accessibility 실패 모드 무자료 재구현 완료.
- 평가: [answerless Frontend transfer](https://github.com/woopinbell/central-notes/blob/main/assessments/frontend-transfer/README.md).
- 환경·baseline: 평가 디렉터리에서 `npm ci`, `npx playwright install chromium firefox webkit`, `npm run check`, `npm run test:starter-red`를 실행한다. starter의 21개 assertion red가 정상이다.
- 구현: source·답지 없이 별도 복사본에서 URL source-of-truth, validation, abort/stale response, optimistic rollback, loading/error/empty와 focus/ARIA를 구현한다.
- 실패 artifact: browser·test title·마지막 URL·request/DOM budget과 수정 근거를 진행 원장에 남긴다.
- 완료 gate: Chromium·Firefox·WebKit acceptance와 사람 rubric을 통과한다. 정답 구현은 Central에 commit하지 않는다.
- 회상: [Frontend transfer clock](https://github.com/woopinbell/central-notes/blob/main/assessments/recall-checkpoints.md#frontend-transfer-clock)을 시작한다.
- 다음: 즉시 회상 뒤 [portfolio-site](#stage-portfolio-site); 7일·30일 회상은 병행한다.

<a id="stage-portfolio-site"></a>
## 6. portfolio-site

- 이전 gate: unfamiliar-API transfer의 세 browser gate와 즉시 회상 완료.
- 저장소·ref: [`portfolio-site`](https://github.com/woopinbell/portfolio-site), neutral `template-v3.0.1`, deployable release `portfolio-v3.0.1` (`== main`), learning `learning/portfolio-v3.0.1`.
- Central 상세 목록: [portfolio-site 전체 읽기 순서](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-portfolio-site). 이 목록이 production CSS·asset·build 선수 범위를 확정한다.
- 빠른 노트: [Frontend CSS and Build](https://github.com/woopinbell/central-notes/blob/main/frontend-react/README.md#css-and-build), [Testing and Quality](https://github.com/woopinbell/central-notes/blob/main/frontend-react/README.md#testing-and-quality).
- 수행 범위: [대표 practice 한 개와 카드 전체 gate](README.md#공식-수행-범위). 나머지는 선택 심화다.
- 프로젝트 노트: 별도 notes가 없으므로 Central 선수 노트 뒤 바로 current practice로 이동한다.
- Clean release gate: annotated release의 별도 clean worktree에서 Node/npm과 Playwright로 `npm run lint`, `npm run typecheck`, `npm test`, `npm run build`, `npm run test:e2e`를 기록한다.
- 문제지: [current practice ledger](https://github.com/woopinbell/portfolio-site/blob/learning/portfolio-v3.0.1/docs/practice-portfolio-v3.0.1/README.md).
- 구현: 개별 commit practice는 그 파일의 full `부모 commit`에서 시작한다. 통합 content publication 과제만 개인 content가 아닌 neutral tag에서 `git switch -c study/portfolio template-v3.0.1`로 시작해 content/schema/render, five-design, responsive/accessibility 실패를 남긴다.
- 답지 개방: neutral template 검증과 자기 publication diff 뒤 [answer ledger](https://github.com/woopinbell/portfolio-site/blob/learning/portfolio-v3.0.1/docs/commits-portfolio-v3.0.1/README.md)를 연다.
- Historical 무자료 gate: 현재 practice 파일이 명시한 시작 tree의 새 branch에서 그 파일의 구현 범위와 당시 검증 계약만 통과한다. 통합 content publication이면 지정된 neutral template가 시작 tree다.
- 연결 설명: 선택한 publication 변경이 current release의 neutral/content topology·allowlist·responsive/accessibility 경계로 이어지는 근거를 설명한다.
- 다음: [Web production regression](#stage-web-production-regression).

<a id="stage-web-production-regression"></a>
## 7. Web production regression 평가

- 이전 gate: Portfolio neutral/content topology와 browser gate 완료.
- 평가: [answerless Web production regression](https://github.com/woopinbell/central-notes/blob/main/assessments/web-production-regression/README.md).
- 시작: 답지와 이전 제출을 닫고 starter·contract·evidence fixture만 사용한다.
- 실행: bundle/network/main-thread/render와 DNS/TLS/proxy/header, XSS·CSRF·CORS·CSP를 하나의 causal chain으로 진단한다.
- 실패 artifact: 측정 → 원인 격리 → 최소 변경 → 검증 → rollback 결과와 외부 review evidence를 남긴다.
- 완료 gate: checker, 사람 rubric, 실제 수정·staged deployment 폐루프와 외부 review를 모두 통과한다.
- 회상: [Web production regression clock](https://github.com/woopinbell/central-notes/blob/main/assessments/recall-checkpoints.md#web-production-regression-clock)을 시작한다. transfer clock과 날짜를 합치지 않는다.
- 다음: 두 평가의 7일·30일 checkpoint 뒤 [Frontend 완료](#stage-frontend-complete).

<a id="stage-frontend-complete"></a>
## Frontend 완료

다음 artifact가 모두 개인 진행 원장에 있으면 Frontend curriculum mastery를 확정한다.

- 5개 프로젝트의 baseline, 대표 practice ID·선택 근거, 실패 근거, answer 확인 시각, 무자료 재구현과 최종 gate
- unfamiliar-API transfer와 Web production regression의 자동·사람 gate
- 서로 독립적인 두 회상 clock의 완료 직후·7일·30일 결과
- 병행한 42 incident 회상 clock의 30일 checkpoint
- Portfolio의 neutral template와 개인 publication을 구분한 검증 결과

취업 지원 자료를 고를 때만 [Frontend 공고 데이터](../data/jobs/frontend/)로 이동한다. 공고 데이터는
학습 완료 gate가 아니며 제출 직전에 원문을 다시 확인한다.

[전체 지도](README.md#분기와-완료)로 돌아가 Backend를 선택하거나 과정을 종료한다.
