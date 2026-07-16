# Frontend 지원 준비 브리지

<a id="route-frontend-application-bridge"></a>

이 문서는 42를 직접 구현한 경험이 있고 42 통합 incident의 즉시 checkpoint를 통과한 학습자가
Frontend 정규 트랙을 완주하기 전, 기억을 복구하고 검증 가능한 지원 자료를 먼저 준비하는 **선택
브리지**다. 새 트랙이나 새 release가 아니며 [`tracks/frontend.md`](frontend.md)의 정규 prev/next
사슬을 바꾸지 않는다.

```text
42 통합 incident 즉시 checkpoint
→ Foundations 핵심 4개 review
→ Reliability 핵심 4개 hands-on ─┐
                                  ├→ Portfolio 검증·지원 gate
Portfolio neutral content 병행 ───┘
→ frontend-application-readiness
→ 정규 Frontend의 Delivery로 복귀
```

```text
route_id: frontend-application-bridge
outcome: frontend-application-readiness
grants_mastery=false
canonical_resume: frontend-delivery-training
```

`frontend-application-readiness`는 지원을 시작해도 된다는 운영 판정일 뿐이다.
`grants_mastery=false`는 overlay 선택 자체가 어떤 완료도 자동 부여하지 않는다는 뜻이다. 아래
artifact가 정규 카드와 동일한 조건을 충족하면 해당 프로젝트 gate의 근거로는 사용할 수 있지만,
Frontend mastery는 이후 Delivery부터 기존 사슬을 따라 transfer·production regression과 각 회상
checkpoint까지 통과해야 한다.

## 0. 42 전체 복습 사슬

이 경로는 42를 건너뛰는 지름길이 아니다. 먼저 `make preflight TRACK=42`를 실행한 뒤 아래 행을
위에서 아래로 따른다. 각 source 프로젝트에서는 [공식 수행 범위](README.md#공식-수행-범위)에 따라
대표 practice 한 개의 historical gate, clean release gate와 current release까지의 연결 설명을
완료한다. 과거에 직접 구현했더라도 기억만으로 PASS를 기록하지 않는다.

| 순서 | Central 선수 handoff | 정규 단계 카드 | 복습 gate |
| ---: | --- | --- | --- |
| 0 | [Linux/Git Foundations](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-linux-foundation) | [Linux/Git](42.md#stage-linux-foundation) | quick probe, self-review와 rollback 설명 |
| 1 | [format-printer](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-format-printer) | [format-printer](42.md#stage-format-printer) | `make && make test` |
| 2 | [signal-message-bus](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-signal-message-bus) | [signal-message-bus](42.md#stage-signal-message-bus) | `make && make test`, 긴 메시지와 중도 종료 sender |
| 3 | [thread-dining](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-thread-dining) | [thread-dining](42.md#stage-thread-dining) | `make && make test`, timing 시나리오 |
| 4 | [small-shell](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-small-shell) | [small-shell](42.md#stage-small-shell) | `make && make test` |
| 5 | [stack-sort](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-stack-sort) | [stack-sort](42.md#stage-stack-sort) | `make && make test`, Python oracle |
| 6 | [stl-container](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-stl-container) | [stl-container](42.md#stage-stl-container) | `make && make test`, strict C++98 compile |
| 7 | [irc-relay-server](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-irc-relay-server) | [irc-relay-server](42.md#stage-irc-relay-server) | `make && make test && make smoke` |
| 8 | [container-stack](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-container-stack) | [container-stack](42.md#stage-container-stack) | `make test && make config`, 가능한 환경에서 up/smoke/down |
| 9 | [web-boundary-inspector](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-web-boundary-inspector) | [web-boundary-inspector](42.md#stage-web-boundary-inspector) | `make check`, request 3개와 browser 21개 |
| 10 | [pong-pong](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-pong-pong) | [pong-pong](42.md#stage-pong-pong) | install/typecheck/test/build와 가능한 E2E·Compose smoke |
| 11 | [42 incident](https://github.com/woopinbell/central-notes/blob/main/assessments/42-incident/README.md#assessment-42-incident) | [42 incident](42.md#stage-42-incident) | answerless checker·사람 rubric·즉시 회상 |

마지막 행을 통과하고 7일·30일 회상을 예약한 시점이 이 overlay의 진입점이다. 회상은 Frontend
진행과 병행하며, 30일 checkpoint 전에는 42 mastery라고 기록하지 않는다.

## 1. 진입 gate

- 이전 gate: [42 통합 incident](42.md#stage-42-incident)의 자동·사람 gate와 즉시 회상을 통과한다.
- 환경: repository root에서
  `make preflight ROUTE=frontend-application-bridge`를 실행하고 현재 단계의 `BLOCK`을
  없앤다.
- 기준 ref:
  - Foundations `foundations-v1.0.1`, `learning/foundations-v1.0.1`
  - Reliability `reliability-v1.0.1`, `learning/reliability-v1.0.1`
  - Portfolio neutral `template-v3.0.1`, release `portfolio-v3.0.1`, learning
    `learning/portfolio-v3.0.1`
- 각 release를 clean checkout하고 아래 묶음에 들어가기 전에 해당 baseline이 green임을 기록한다.

이 브리지는 공개 release나 immutable learning ref를 움직이지 않는다. `learning/*`는 읽기 전용이고,
실제 구현이 있는 Foundations `041`과 Reliability practice만 historical parent에서 만든 개인
`study/*` branch에 둔다. Practice에 full parent가 없으면 answer 본문은 열지 않고 current answer
ledger README의 해당 metadata mapping 행만 읽어 parent를 확인한다.

## 2. Foundations 핵심 4개 review

이 묶음은 과거 구현 기억을 빠르게 복구하는 **review 묶음**이다. Form의 `041`만 제공된 practice를
practice-first로 수행하고, 나머지 세 항목은 읽기·관찰·설명으로 검토한다. App Router, Query Cache,
Accessibility 행에는 독립 구현 practice가 없으므로 가짜 parent, orphan branch, 실패 증거를 만들지
않는다. `041`의 실패→answer→무자료 재구현, clean release 전체 gate와 current release 연결 설명까지
완료하면 정규 카드의 대표 practice 규칙에 따라 Foundations 프로젝트 gate로 기록할 수 있다. 네
review 행만 훑은 것은 Foundations 완료가 아니다.

먼저 release source와 route를 보고 자기 말로 설명한 뒤에만 learning answer/crosswalk와 비교한다.
네 review를 마친 뒤 clean release에서 `make check-repo && make build && make test-e2e`를 실행한다.

| 순서 | Stable ID | review 대상 | 수행·증거 |
| ---: | --- | --- | --- |
| 1 | `039/040/041` | [Form Validation Zod](https://github.com/woopinbell/frontend-foundations-training/blob/foundations-v1.0.1/src/exercises/spine/09-form-validation-zod/README.md) | schema와 React Hook Form의 책임, client/server error, 접근 가능한 feedback을 먼저 설명한다. 이어 [`041` practice](https://github.com/woopinbell/frontend-foundations-training/blob/learning/foundations-v1.0.1/docs/practice/041.md)를 practice-first로 수행한다. Parent가 파일에 없으면 current answer ledger가 연결한 full crosswalk의 `041` metadata mapping 행만 확인한다. Catalog와 E2E는 `pnpm test src/exercises/catalog.test.ts`, `pnpm test:e2e e2e/exercise.spec.ts`로 검증한다. |
| 2 | `067/068/069` | [App Router Boundary Lite](https://github.com/woopinbell/frontend-foundations-training/blob/foundations-v1.0.1/src/exercises/bridge/app-router-boundary-lite/README.md) | server/client 책임, serializable props와 boundary를 source에서 찾아 설명하고 `pnpm typecheck`, `pnpm build`를 통과한다. Metadata-only review이며 구현 완료로 세지 않는다. |
| 3 | `071/072/073` | [Query Cache Lite](https://github.com/woopinbell/frontend-foundations-training/blob/foundations-v1.0.1/src/exercises/bridge/query-cache-lite/README.md) | `/exercises/bridge/query-cache-lite`에서 query status와 refetch를 관찰하고 server state, cache state, form/UI state를 구분한다. Metadata-only review다. |
| 4 | `079/080/081` | [Accessibility Check Lite](https://github.com/woopinbell/frontend-foundations-training/blob/foundations-v1.0.1/src/exercises/bridge/accessibility-check-lite/README.md) | `/exercises/bridge/accessibility-check-lite`에서 label 연결, role feedback, keyboard 도달성을 검사한다. Metadata-only review다. |

각 행마다 진행 원장에 stable ID, 실제 commit hash·parent·tree, 읽은 source 경로, 자기 설명, 실행한
명령과 관찰 결과를 남긴다. `041`에만 일반 practice-first 절차와
실패→answer→무자료 재구현을 적용한다. 자기 설명을 쓴 뒤
[Foundations current answer ledger](https://github.com/woopinbell/frontend-foundations-training/blob/learning/foundations-v1.0.1/docs/commits-foundations-v1.0.1/README.md)에서
연결한 full crosswalk의 stable ID 행만 먼저 대조한다. Mapping의 abbreviated commit·parent는
clone에서 `git rev-parse <mapped-sha>^{commit}`으로 full SHA를 확인하고, tree는
`git show -s --format=%T <full-commit>`으로 기록한다.

## 3. Reliability 핵심 4개 hands-on

이 묶음은 review가 아니라 실제 historical practice 수행이다. 각 ID의 문제지를 먼저 연다. Full
`부모 commit`이 없으면 answer 본문은 열지 않고
[Reliability current answer ledger README](https://github.com/woopinbell/frontend-reliability-training/blob/learning/reliability-v1.0.1/docs/commits-reliability-v1.0.1/README.md)가
연결한 full crosswalk의 해당 metadata mapping 행만 읽어 parent를 확인한다. Abbreviated commit과
parent는 clone에서 `git rev-parse <mapped-sha>^{commit}`으로 full SHA로 해소하고 tree는
`git show -s --format=%T <full-commit>`으로 기록한다. 그 parent에서 새
`study/*` branch를 만들고 첫
실패·가설·반증을 남긴 뒤 answer를 열며, 다시 같은 parent에서 무자료 재구현한다. 마지막에는 별도
clean release worktree에서 다음 전체 gate를 실행한다.

```sh
pnpm install --frozen-lockfile
pnpm check:repo
pnpm lint
pnpm typecheck
pnpm test
pnpm build
CI=1 NEXT_TELEMETRY_DISABLED=1 pnpm test:e2e
```

| 순서 | Stable ID와 문제지 | 구현 계약 | Historical gate |
| ---: | --- | --- | --- |
| 1 | [`010`](https://github.com/woopinbell/frontend-reliability-training/blob/learning/reliability-v1.0.1/docs/practice/010.md) / [`011`](https://github.com/woopinbell/frontend-reliability-training/blob/learning/reliability-v1.0.1/docs/practice/011.md) / [`013`](https://github.com/woopinbell/frontend-reliability-training/blob/learning/reliability-v1.0.1/docs/practice/013.md) | Form: RHF+Zod, client/server error, duplicate submit lock, accessible error/reset | `pnpm --filter react-main test form-validation`; 구현 단계에서 `pnpm --filter react-main typecheck` |
| 2 | [`036`](https://github.com/woopinbell/frontend-reliability-training/blob/learning/reliability-v1.0.1/docs/practice/036.md) / [`037`](https://github.com/woopinbell/frontend-reliability-training/blob/learning/reliability-v1.0.1/docs/practice/037.md) / [`039`](https://github.com/woopinbell/frontend-reliability-training/blob/learning/reliability-v1.0.1/docs/practice/039.md) | Table pagination: URL source of truth, 정규화, history restore, loading/error/retry, table semantics | `pnpm --filter react-main test table-pagination`; 구현 단계에서 `pnpm --filter react-main typecheck` |
| 3 | [`043`](https://github.com/woopinbell/frontend-reliability-training/blob/learning/reliability-v1.0.1/docs/practice/043.md) / [`044`](https://github.com/woopinbell/frontend-reliability-training/blob/learning/reliability-v1.0.1/docs/practice/044.md) / [`046`](https://github.com/woopinbell/frontend-reliability-training/blob/learning/reliability-v1.0.1/docs/practice/046.md) / [`047`](https://github.com/woopinbell/frontend-reliability-training/blob/learning/reliability-v1.0.1/docs/practice/047.md) | Optimistic update: rollback, mutation identity, out-of-order callback, stale response 거부 | `pnpm --filter react-main test optimistic-update`; 구현 단계에서 `pnpm --filter react-main typecheck` |
| 4 | [`108`](https://github.com/woopinbell/frontend-reliability-training/blob/learning/reliability-v1.0.1/docs/practice/108.md) / [`109`](https://github.com/woopinbell/frontend-reliability-training/blob/learning/reliability-v1.0.1/docs/practice/109.md) / [`110`](https://github.com/woopinbell/frontend-reliability-training/blob/learning/reliability-v1.0.1/docs/practice/110.md) / [`112`](https://github.com/woopinbell/frontend-reliability-training/blob/learning/reliability-v1.0.1/docs/practice/112.md) | Server/client boundary: public serializable props, `server-only`, module separation, private field 비노출 | `pnpm --filter next-sub test server-client-boundary`, `pnpm --filter next-sub typecheck`, `pnpm --filter next-sub test:e2e server-client-boundary` |

한 묶음 안의 ID는 작은 역사적 증분이므로 끝 ID만 읽고 현재 구현을 흉내 내지 않는다. 표의 순서대로
각 parent와 당시 gate를 분리해 재현하고, 현재 release 전체 gate 결과와 섞지 않는다.

## 4. Portfolio 병행

Foundations 네 review를 마치면 Reliability hands-on과 병행해 Portfolio의 neutral content 작업을 시작할
수 있다. [`portfolio-site`](https://github.com/woopinbell/portfolio-site)의
[정규 카드](frontend.md#stage-portfolio-site) topology를 그대로 사용한다.

```sh
git switch -c study/portfolio-application template-v3.0.1
```

- 개인화 변경은 neutral template가 허용하는 `src/content/**`, `public/content/**` 경계 안에 둔다.
- 공개할 repository와 근거 명령을 고르고, 각 항목을 `문제 → 설계 결정 → 검증 → 결과`로 설명한다.
- `npm run lint`, `npm run typecheck`, `npm test`, `npm run build`, `npm run test:e2e`를 모두 기록한다.
- Reliability의 네 hands-on이 끝나기 전에도 content를 편집할 수 있지만, 아래 지원 gate를 통과한 것으로
  표기하거나 공개 완료로 주장하지 않는다.

## 5. 지원 gate

다음이 모두 있으면 진행 원장에 outcome `frontend-application-readiness`를 기록하고 지원을 시작할 수
있다.

- Foundations 네 review의 source·commit metadata·자기 설명·관찰 증거
- Reliability 네 hands-on의 historical 실패→answer→무자료 재구현과 current release 전체 gate
- Portfolio neutral/content 경계, 전체 gate, 공개 대상으로 고른 repository와 설명 artifact
- 프로젝트 경험을 실무 경력으로 과장하지 않고 검증된 개인 프로젝트로 표현한 지원 자료

지원 대상은 [Frontend 공고 데이터](../data/jobs/frontend/)에서 고르고 제출 직전에 원문을 다시
확인한다. 이 판정은 채용 가능성을 보증하지 않으며 Frontend 완료 표시에 사용하지 않는다.

## 6. 정규 사슬로 복귀

지원과 동시에 정규 트랙의
[`frontend-delivery-training`](frontend.md#stage-frontend-delivery-training)으로 복귀한다. 이후 순서는
Delivery → Cloud → Reliability 전체 카드 → unfamiliar-API transfer → Portfolio 정규 gate → Web
production regression → 두 회상 clock이다.

빠른 브리지에서 만든 artifact는 같은 명령·tree를 정확히 가리킬 때 근거로 재사용할 수 있지만,
Reliability 일부 수행을 프로젝트 전체 완료로, Portfolio 지원용 publication을 transfer 이후의 정규
완료로 바꾸어 기록할 수 없다. 정규 카드가 요구하는 대표 practice·전체 gate·평가·회상은 각각 다시
판정한다.

## 완료 체크

- [ ] 42 incident 즉시 checkpoint를 통과했다.
- [ ] Foundations `041` practice·clean release gate·연결 설명과 세 metadata-only review를 구분해 기록했다.
- [ ] Reliability 4 hands-on을 historical tree와 current release tree에서 각각 검증했다.
- [ ] Portfolio를 neutral template에서 개인화하고 전체 gate를 통과했다.
- [ ] outcome `frontend-application-readiness`를 기록했다.
- [ ] `grants_mastery=false`를 확인하고 Delivery 정규 카드로 복귀했다.

[전체 과정 지도](README.md) · [Frontend 정규 트랙](frontend.md)
