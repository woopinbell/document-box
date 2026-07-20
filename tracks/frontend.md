# Frontend 학습 경로

42 통합 평가를 마친 뒤 시작한다. 이 트랙은 아래 순서를 지킨다.

```text
기초 → 배포 → Cloud → 안정성 → 낯선 API 평가
→ Portfolio → production 장애 평가 → 복습 → 완료
```

먼저 `make preflight TRACK=frontend`를 실행한다. 공통 진행법과 연습문제 선택법은
[학습 시작](README.md), Git 세부 절차는 [기술 안내](TECHNICAL_GUIDE.md)를 따른다.

이미 42를 구현했고 지원 준비가 급하면 [Frontend 지원 준비 경로](frontend-fast-track.md#route-frontend-application-bridge)를
사용할 수 있다. 이 경로는 Frontend 완료가 아니며 끝난 뒤 [배포 단계](#stage-frontend-delivery-training)로
돌아온다.

<a id="stage-frontend-foundations-training"></a>
## F1. frontend-foundations-training

- **시작 조건:** [42 통합 평가](42.md#stage-42-incident)를 통과하고 완료 직후 복습을 기록한다.
- **먼저 읽을 것:** [Frontend 기초 읽는 순서](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-frontend-foundations-training)의 language·React·build·state·test 범위를 읽는다.
- **저장소와 학습 자료:** [`frontend-foundations-training`](https://github.com/woopinbell/frontend-foundations-training), 완성본 `foundations-v1.0.1`, 읽기 전용 자료 `learning/current`; [학습 자료 목차](https://github.com/woopinbell/frontend-foundations-training/blob/learning/current/docs/README.md), [연습문제 목록](https://github.com/woopinbell/frontend-foundations-training/blob/learning/current/docs/practice/README.md), [해설 목록](https://github.com/woopinbell/frontend-foundations-training/blob/learning/current/docs/commits/README.md), [실전 질문](https://github.com/woopinbell/frontend-foundations-training/blob/learning/current/docs/interview/README.md).
- **직접 해볼 것:** [필수 학습 범위](README.md#공식-수행-범위)에 따라 문제 한 개를 고른다. 지정된 시작 커밋에 `study/frontend-foundations-<ID>`를 만들고 route, server/client 경계, form·data·UI state 실패를 기록한다. 자기 시도 뒤 해설과 비교하고 다시 구현한다.
- **현재 완성본 확인:** 별도의 깨끗한 작업 공간에서 Node·pnpm과 browser를 확인하고 `make check-repo && make build && make test-e2e`를 실행한다.
- **완료 조건:** route와 server/client 경계, form·data·UI 상태 흐름을 설명하고 선택한 문제를 해설 없이 다시 통과한다.
- **다음 과제:** [F2. frontend-delivery-training](#stage-frontend-delivery-training).

<a id="stage-frontend-delivery-training"></a>
## F2. frontend-delivery-training

- **시작 조건:** [F1. Frontend 기초](#stage-frontend-foundations-training)를 완료한다.
- **먼저 읽을 것:** [Frontend 배포 읽는 순서](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-frontend-delivery-training)의 Central·프로젝트 delivery 노트를 읽는다.
- **저장소와 학습 자료:** [`frontend-delivery-training`](https://github.com/woopinbell/frontend-delivery-training), 완성본 `delivery-v1.0.1`, 읽기 전용 자료 `learning/current`; [학습 자료 목차](https://github.com/woopinbell/frontend-delivery-training/blob/learning/current/docs/README.md), [연습문제 목록](https://github.com/woopinbell/frontend-delivery-training/blob/learning/current/docs/practice/README.md), [해설 목록](https://github.com/woopinbell/frontend-delivery-training/blob/learning/current/docs/commits/README.md), [실전 질문](https://github.com/woopinbell/frontend-delivery-training/blob/learning/current/docs/interview/README.md).
- **직접 해볼 것:** [필수 학습 범위](README.md#공식-수행-범위)에 따라 문제 한 개를 고른다. 지정된 시작 커밋에 `study/frontend-delivery-<ID>`를 만들고 route, asset budget, SEO·build와 release checklist 실패를 기록한다. 해설과 비교한 뒤 다시 구현한다.
- **현재 완성본 확인:** 별도의 깨끗한 작업 공간에서 Node·pnpm, image와 Chromium 도구를 확인하고 `make check`를 실행한다. 실제 DNS나 Search Console은 변경하지 않는다.
- **완료 조건:** 배포 가능한 산출물, route·asset·SEO·build 확인 순서를 자기 말로 설명한다.
- **다음 과제:** [F3. cloud-launch-training](#stage-cloud-launch-training).

<a id="stage-cloud-launch-training"></a>
## F3. cloud-launch-training

- **시작 조건:** [F2. Frontend 배포](#stage-frontend-delivery-training)를 완료한다.
- **먼저 읽을 것:** [Cloud 읽는 순서](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-cloud-launch-training)의 request lifecycle·browser security·Next·Playwright와 프로젝트 Cloud 노트를 읽는다.
- **저장소와 학습 자료:** [`cloud-launch-training`](https://github.com/woopinbell/cloud-launch-training), 완성본 `cloud-launch-v1.0.1`, 읽기 전용 자료 `learning/current`; [학습 자료 목차](https://github.com/woopinbell/cloud-launch-training/blob/learning/current/docs/README.md), [연습문제 목록](https://github.com/woopinbell/cloud-launch-training/blob/learning/current/docs/practice/README.md), [해설 목록](https://github.com/woopinbell/cloud-launch-training/blob/learning/current/docs/commits/README.md), [실전 질문](https://github.com/woopinbell/cloud-launch-training/blob/learning/current/docs/practice/interview/README.md).
- **직접 해볼 것:** [필수 학습 범위](README.md#공식-수행-범위)에 따라 문제 한 개를 고른다. 지정된 시작 커밋에 `study/cloud-launch-<ID>`를 만들고 Rules 허용·거부, Functions 신뢰와 Cloudflare 경계 실패를 기록한다. emulator에서 확인한 뒤 해설과 비교하고 다시 구현한다.
- **현재 완성본 확인:** 별도의 깨끗한 작업 공간에서 Node·npm, Java, Firebase Emulator와 세 browser를 확인하고 `make check`를 실행한다. 실제 credential·비용·DNS 변경은 필수가 아니다.
- **완료 조건:** client의 주장과 서버 권한을 구분하고 Rules·Functions·edge 경계를 설명한다.
- **다음 과제:** [F4. frontend-reliability-training](#stage-frontend-reliability-training).

<a id="stage-frontend-reliability-training"></a>
## F4. frontend-reliability-training

- **시작 조건:** [F3. Cloud](#stage-cloud-launch-training)를 완료한다.
- **먼저 읽을 것:** [Frontend 안정성 읽는 순서](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-frontend-reliability-training)의 RSC·router·query·form·접근성·test 범위를 읽는다.
- **저장소와 학습 자료:** [`frontend-reliability-training`](https://github.com/woopinbell/frontend-reliability-training), 완성본 `reliability-v1.0.1`, 읽기 전용 자료 `learning/current`; [학습 자료 목차](https://github.com/woopinbell/frontend-reliability-training/blob/learning/current/docs/README.md), [연습문제 목록](https://github.com/woopinbell/frontend-reliability-training/blob/learning/current/docs/practice/README.md), [해설 목록](https://github.com/woopinbell/frontend-reliability-training/blob/learning/current/docs/commits/README.md), [실전 질문](https://github.com/woopinbell/frontend-reliability-training/blob/learning/current/docs/interview/README.md).
- **직접 해볼 것:** [필수 학습 범위](README.md#공식-수행-범위)에 따라 문제 한 개를 고른다. 지정된 시작 커밋에 `study/frontend-reliability-<ID>`를 만들고 오래된 응답, rollback, URL state, focus와 reconnect 실패를 재현한다. 실패 test를 만든 뒤 해설과 비교하고 다시 구현한다.
- **현재 완성본 확인:** 별도의 깨끗한 작업 공간에서 Node·pnpm과 Playwright를 확인하고 `pnpm check:repo && make lint && make typecheck && make test && make build && make test-e2e`를 실행한다.
- **완료 조건:** 비동기 응답과 UI 상태의 권위, 실패 rollback과 접근성 focus 복구를 설명한다.
- **다음 과제:** [F5. 낯선 API 평가](#stage-frontend-transfer).

<a id="stage-frontend-transfer"></a>
## F5. 낯선 API 평가

- **시작 조건:** [F4. Frontend 안정성](#stage-frontend-reliability-training)을 완료한다.
- **먼저 읽을 것:** [답지 없는 Frontend 평가](https://github.com/woopinbell/central-notes/blob/main/assessments/frontend-transfer/README.md)의 contract와 금지 사항을 읽는다.
- **저장소와 학습 자료:** 별도 해설은 없다. 평가 문서가 지정한 starter·contract·evidence만 새 복사본에 준비한다.
- **직접 해볼 것:** `npm ci`, `npx playwright install chromium firefox webkit`, `npm run check`, `npm run test:starter-red`를 실행한다. 처음 21개 assertion이 실패하는 것이 정상이다. URL, validation, 취소된 요청, 오래된 응답, optimistic rollback과 focus·ARIA를 직접 구현한다.
- **현재 완성본 확인:** Chromium·Firefox·WebKit acceptance 결과와 사람 평가 기록이 같은 구현을 가리키는지 확인한다.
- **완료 조건:** Chromium·Firefox·WebKit 검사와 사람 평가를 통과하고 완료 직후 복습을 기록한다. 정답 구현은 Central Notes에 commit하지 않는다.
- **다음 과제:** [F6. portfolio-site](#stage-portfolio-site). 7일·30일 복습은 다음 프로젝트와 함께 진행한다.

<a id="stage-portfolio-site"></a>
## F6. portfolio-site

- **시작 조건:** [F5. 낯선 API 평가](#stage-frontend-transfer)와 완료 직후 복습을 마친다.
- **먼저 읽을 것:** [Portfolio 읽는 순서](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-portfolio-site)의 production CSS·asset·build 범위를 읽는다.
- **저장소와 학습 자료:** [`portfolio-site`](https://github.com/woopinbell/portfolio-site), 시작 template `template-v3.0.1`, 완성본 `portfolio-v3.0.1`, 독자가 읽을 유일한 집필 branch `learning/current`; [학습 시작](https://github.com/woopinbell/portfolio-site/blob/learning/current/docs/README.md), [연습문제 목록](https://github.com/woopinbell/portfolio-site/blob/learning/current/docs/practice/README.md), [해설 목록](https://github.com/woopinbell/portfolio-site/blob/learning/current/docs/commits/README.md), [실전 질문](https://github.com/woopinbell/portfolio-site/blob/learning/current/docs/interview/README.md).
- **직접 해볼 것:** [필수 학습 범위](README.md#공식-수행-범위)에 따라 문제 한 개를 고른다. 일반 문제는 지정된 시작 커밋에서 진행한다. 통합 content publication 문제만 `git switch -c study/portfolio template-v3.0.1`로 시작한다. content·schema·render, five-design, 반응형과 접근성 실패를 기록한 뒤 해설과 비교하고 다시 구현한다.
- **현재 완성본 확인:** 별도의 깨끗한 작업 공간에서 `npm run lint`, `npm run typecheck`, `npm test`, `npm run build`, `npm run test:e2e`를 실행한다.
- **완료 조건:** neutral template와 개인 content를 구분하고, content 허용 경로와 반응형·접근성 결과를 설명한다.
- **다음 과제:** [F7. Web production 장애 평가](#stage-web-production-regression).

<a id="stage-web-production-regression"></a>
## F7. Web production 장애 평가

- **시작 조건:** [F6. Portfolio](#stage-portfolio-site)를 완료한다.
- **먼저 읽을 것:** [답지 없는 Web production 평가](https://github.com/woopinbell/central-notes/blob/main/assessments/web-production-regression/README.md)의 contract와 금지 사항을 읽는다.
- **저장소와 학습 자료:** 별도 해설은 없다. starter·contract·evidence fixture와 staged deployment만 사용한다.
- **직접 해볼 것:** 답지와 이전 제출을 닫고 bundle·network·main thread·render, DNS·TLS·proxy·header와 XSS·CSRF·CORS·CSP를 하나의 원인 사슬로 진단한다.
- **현재 완성본 확인:** 측정, 최소 수정, 재검사, rollback과 외부 검토 기록이 한 실행 흐름으로 이어지는지 확인한다.
- **완료 조건:** 자동 검사, 사람 평가, 실제 수정·staged deployment·rollback과 외부 검토를 모두 통과한다. transfer 복습과 별도로 완료 직후·7일·30일 복습을 기록한다.
- **다음 과제:** 두 평가의 30일 복습 뒤 [Frontend 완료](#stage-frontend-complete).

<a id="stage-frontend-complete"></a>
## Frontend 완료

다음 기록이 모두 있으면 완료다.

- 5개 프로젝트의 선택 문제, 실제 실패, 해설 확인 시각, 다시 구현한 결과와 현재 완성본 검사
- 두 답지 없는 평가의 자동·사람 검사
- 두 평가의 완료 직후·7일·30일 복습
- 42 통합 평가의 30일 복습
- Portfolio의 neutral template와 개인 content를 구분한 결과

취업 지원 자료가 필요할 때만 [Frontend 공고 데이터](../data/jobs/frontend/)를 사용한다. 공고 데이터는
학습 완료 조건이 아니며 지원 직전에 원문을 다시 확인한다.

[전체 학습 시작](README.md#트랙-선택)으로 돌아가 Backend를 선택하거나 과정을 종료한다.
