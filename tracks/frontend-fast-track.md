# Frontend 지원 준비 경로

<a id="route-frontend-application-bridge"></a>

42를 직접 구현했고 통합 평가까지 통과했지만, Frontend 전체 과정을 마치기 전에 지원 자료를 먼저
준비해야 할 때 사용하는 선택 경로다. 새 트랙이나 새 release가 아니며 정규 Frontend 순서를 바꾸지
않는다.

```text
42 통합 평가
→ Foundations 핵심 확인
→ Reliability 핵심 실습 ─┐
                           ├→ Portfolio 확인 → 지원 시작 가능
Portfolio 작업 병행 ──────┘
→ 정규 Frontend의 Delivery로 복귀
```

```text
route_id: frontend-application-bridge
outcome: frontend-application-readiness
grants_mastery=false
canonical_resume: frontend-delivery-training
```

`frontend-application-readiness`는 지원을 시작해도 된다는 뜻일 뿐 Frontend 완료를 뜻하지 않는다.
`grants_mastery=false`이므로 이 경로를 마친 뒤에도 정규 Frontend 과정을 계속해야 한다.

## 0. 먼저 42 복습

이 경로는 42를 건너뛰는 지름길이 아니다. `make preflight TRACK=42`를 실행하고 세 갈래와 합류 과정을
모두 확인한다. 각 프로젝트에서는 [필수 학습 범위](README.md#공식-수행-범위)에 따라 문제 한 개를
직접 시도하고, 해설을 닫은 채 다시 구현한 뒤 현재 완성본 검사를 통과한다.

| 갈래 | Central 선수 안내 | 42 카드 | 확인할 명령·결과 |
| --- | --- | --- | --- |
| 공통 | [Linux/Git](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-linux-foundation) | [Linux/Git](42.md#stage-linux-foundation) | 빠른 확인, 자기 검토와 되돌리기 설명 |
| C1 | [c-foundation](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-c-foundation) | [c-foundation](42.md#stage-c-foundation) | `make check` |
| C2 | [format-printer](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-format-printer) | [format-printer](42.md#stage-format-printer) | `make && make test` |
| C3 | [buffered-line-reader](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-buffered-line-reader) | [buffered-line-reader](42.md#stage-buffered-line-reader) | `make check` |
| C4 | [signal-message-bus](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-signal-message-bus) | [signal-message-bus](42.md#stage-signal-message-bus) | `make && make test`, 긴 메시지와 sender 종료 |
| C5 | [thread-dining](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-thread-dining) | [thread-dining](42.md#stage-thread-dining) | `make && make test`, 시간 시나리오 |
| C6 | [small-shell](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-small-shell) | [small-shell](42.md#stage-small-shell) | `make && make test` |
| C7 | [stack-sort](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-stack-sort) | [stack-sort](42.md#stage-stack-sort) | `make && make test`, Python 대조 |
| CPP1 | [cpp-foundation](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-cpp-foundation) | [cpp-foundation](42.md#stage-cpp-foundation) | `make check` |
| CPP2 | [stl-container](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-stl-container) | [stl-container](42.md#stage-stl-container) | `make && make test`, C++98 compile |
| CPP3 | [irc-relay-server](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-irc-relay-server) | [irc-relay-server](42.md#stage-irc-relay-server) | `make && make test && make smoke` |
| INFRA1 | [container-stack](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-container-stack) | [container-stack](42.md#stage-container-stack) | `make test && make config`, 가능한 환경의 up·smoke·down |
| 합류 1 | [web-boundary-inspector](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-web-boundary-inspector) | [web-boundary-inspector](42.md#stage-web-boundary-inspector) | request 3개와 browser 21개 |
| 합류 2 | [pong-pong](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md#stage-pong-pong) | [pong-pong](42.md#stage-pong-pong) | typecheck·test·build와 가능한 E2E |
| 최종 | [42 통합 평가](https://github.com/woopinbell/central-notes/blob/main/assessments/42-incident/README.md#assessment-42-incident) | [42 통합 평가](42.md#stage-42-incident) | 자동·사람 평가와 완료 직후 복습 |

42 통합 평가를 마치고 7일·30일 복습 날짜를 정한 뒤 다음 단계로 이동한다.

## 1. 진입 준비

1. Document Box에서 다음을 실행한다.

   ```sh
   make preflight ROUTE=frontend-application-bridge
   ```

2. 다음 고정 버전을 사용한다.

   - Foundations `foundations-v1.0.1`, `learning/current`
   - Reliability `reliability-v1.0.1`, `learning/current`
   - Portfolio `template-v3.0.1`, `portfolio-v3.0.1`, `learning/portfolio-v3.0.1`

3. `learning/*`는 읽기 전용으로 두고 개인 구현은 문제에서 지정한 시작 커밋의 `study/*` branch에
   작성한다. 시작 커밋이 없으면 [기술 안내](TECHNICAL_GUIDE.md#시작-커밋을-찾는-방법)를 따른다.

## 2. Foundations 핵심 확인

네 항목 중 `041`만 실제 구현 문제다. 나머지 세 항목은 source를 읽고 실행 결과를 설명하는 검토
전용 항목이다. 없는 문제나 실패를 만들어 내지 않는다.

| 대상 | 해야 할 일 |
| --- | --- |
| Form `039/040/041` | [설명](https://github.com/woopinbell/frontend-foundations-training/blob/foundations-v1.0.1/src/exercises/spine/09-form-validation-zod/README.md)을 읽고 [`041` 연습문제](https://github.com/woopinbell/frontend-foundations-training/blob/learning/current/docs/practice/041.md)를 직접 수행한다. `pnpm test src/exercises/catalog.test.ts`와 `pnpm test:e2e e2e/exercise.spec.ts`로 확인한다. |
| App Router `067/068/069` | [설명](https://github.com/woopinbell/frontend-foundations-training/blob/foundations-v1.0.1/src/exercises/bridge/app-router-boundary-lite/README.md)과 source에서 server/client 책임과 직렬화 가능한 props를 찾고 `pnpm typecheck`, `pnpm build`를 실행한다. |
| Query Cache `071/072/073` | [설명](https://github.com/woopinbell/frontend-foundations-training/blob/foundations-v1.0.1/src/exercises/bridge/query-cache-lite/README.md)에서 server·cache·form·UI state를 구분한다. |
| Accessibility `079/080/081` | [설명](https://github.com/woopinbell/frontend-foundations-training/blob/foundations-v1.0.1/src/exercises/bridge/accessibility-check-lite/README.md)에서 label, role feedback과 keyboard 접근을 확인한다. |

각 항목의 실제 commit·parent·tree, 읽은 source와 실행 결과를 기록한다. `041`은 답을 보지 않고 시도한
뒤 [Foundations 해설 목록](https://github.com/woopinbell/frontend-foundations-training/blob/learning/current/docs/commits/README.md)과
비교하고 같은 시작점에서 다시 구현한다. 마지막으로 `make check-repo && make build && make test-e2e`를
실행한다.

## 3. Reliability 핵심 실습

아래 네 묶음은 실제 구현 문제다. 각 링크를 순서대로 열어 문제에서 지정한 시작 커밋에 개인 branch를
만들고 실제 실패를 기록한다. 자기 시도 뒤
[Reliability 해설 목록](https://github.com/woopinbell/frontend-reliability-training/blob/learning/current/docs/commits/README.md)과
비교한 다음 같은 시작점에서 다시 구현한다.

| 묶음 | 연습문제 | 확인할 내용 |
| --- | --- | --- |
| Form | [`010`](https://github.com/woopinbell/frontend-reliability-training/blob/learning/current/docs/practice/010.md), [`011`](https://github.com/woopinbell/frontend-reliability-training/blob/learning/current/docs/practice/011.md), [`013`](https://github.com/woopinbell/frontend-reliability-training/blob/learning/current/docs/practice/013.md) | client/server error, 중복 제출 방지, 접근 가능한 오류·초기화. `pnpm --filter react-main test form-validation`, `pnpm --filter react-main typecheck` |
| Table | [`036`](https://github.com/woopinbell/frontend-reliability-training/blob/learning/current/docs/practice/036.md), [`037`](https://github.com/woopinbell/frontend-reliability-training/blob/learning/current/docs/practice/037.md), [`039`](https://github.com/woopinbell/frontend-reliability-training/blob/learning/current/docs/practice/039.md) | URL 기준 상태, history 복원, loading·error·retry. `pnpm --filter react-main test table-pagination`, `pnpm --filter react-main typecheck` |
| Optimistic update | [`043`](https://github.com/woopinbell/frontend-reliability-training/blob/learning/current/docs/practice/043.md), [`044`](https://github.com/woopinbell/frontend-reliability-training/blob/learning/current/docs/practice/044.md), [`046`](https://github.com/woopinbell/frontend-reliability-training/blob/learning/current/docs/practice/046.md), [`047`](https://github.com/woopinbell/frontend-reliability-training/blob/learning/current/docs/practice/047.md) | rollback, mutation 구분, 순서가 바뀐 callback과 오래된 응답 거부. `pnpm --filter react-main test optimistic-update`, `pnpm --filter react-main typecheck` |
| Server/client | [`108`](https://github.com/woopinbell/frontend-reliability-training/blob/learning/current/docs/practice/108.md), [`109`](https://github.com/woopinbell/frontend-reliability-training/blob/learning/current/docs/practice/109.md), [`110`](https://github.com/woopinbell/frontend-reliability-training/blob/learning/current/docs/practice/110.md), [`112`](https://github.com/woopinbell/frontend-reliability-training/blob/learning/current/docs/practice/112.md) | 공개 가능한 props, server-only module과 private field 비노출. `pnpm --filter next-sub test server-client-boundary`, `pnpm --filter next-sub typecheck`, `pnpm --filter next-sub test:e2e server-client-boundary` |

현재 완성본에서는 다음을 모두 실행한다.

```sh
pnpm install --frozen-lockfile
pnpm check:repo
pnpm lint
pnpm typecheck
pnpm test
pnpm build
CI=1 NEXT_TELEMETRY_DISABLED=1 pnpm test:e2e
```

## 4. Portfolio 병행

Foundations 확인을 마치면 Reliability와 함께 Portfolio 작업을 시작할 수 있다.
[`portfolio-site`](https://github.com/woopinbell/portfolio-site)의 [정규 카드](frontend.md#stage-portfolio-site)를
따르고 다음 branch에서 시작한다.

```sh
git switch -c study/portfolio-application template-v3.0.1
```

- 개인 내용은 `src/content/**`, `public/content/**`에 둔다.
- 각 공개 항목을 `문제 → 설계 결정 → 확인 방법 → 결과`로 설명한다.
- `npm run lint`, `npm run typecheck`, `npm test`, `npm run build`, `npm run test:e2e`를 실행한다.
- Reliability 실습이 끝나기 전에는 지원 준비 완료로 표시하지 않는다.

## 5. 지원 시작 조건

다음이 모두 있으면 `frontend-application-readiness`를 기록하고 지원을 시작할 수 있다.

- Foundations 네 항목의 source·commit 정보, 자기 설명과 실행 결과
- Reliability 네 묶음의 실제 실패, 해설 비교, 다시 구현과 현재 완성본 검사
- Portfolio의 template·content 경계와 전체 검사 결과
- 프로젝트 경험을 실무 경력으로 과장하지 않은 지원 자료

지원 대상은 [Frontend 공고 데이터](../data/jobs/frontend/)에서 고르고 제출 직전에 원문을 확인한다.

## 6. 정규 Frontend로 돌아가기

지원과 함께 정규 트랙의 [frontend-delivery-training](frontend.md#stage-frontend-delivery-training)으로
돌아간다. 빠른 경로에서 만든 정확한 검사 기록은 재사용할 수 있지만 일부 실습을 프로젝트 전체 완료로
바꾸어 기록할 수 없다.

## 완료 확인

- [ ] 42 통합 평가와 완료 직후 복습을 통과했다.
- [ ] Foundations `041` 구현과 세 검토 전용 항목을 구분해 기록했다.
- [ ] Reliability 네 묶음을 직접 구현하고 현재 완성본을 검사했다.
- [ ] Portfolio를 고정 template에서 개인화하고 전체 검사를 통과했다.
- [ ] `frontend-application-readiness`를 기록했다.
- [ ] `grants_mastery=false`를 확인하고 정규 Delivery 카드로 돌아갔다.

[전체 학습 시작](README.md) · [Frontend 정규 트랙](frontend.md)
