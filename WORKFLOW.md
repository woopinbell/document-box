# 개발·리팩터링·이력 작업 Workflow

기능 구현, 행동 보존형 refactor, 문서 정리, Git history 재편과 저장공간 정리를 같은 안전 절차로
수행하는 실행 정본입니다. 대상 저장소마다 독립적으로 적용하며, 한 저장소의 실패가 다른 안전한
저장소 진행을 막지는 않습니다.

## 1. Preflight

1. 대상과 제외 대상을 절대경로로 고정합니다. 사용자 변경이 있는 원본, 별도 세션 소유 저장소와
   명시적 hard-exclude 경로는 checkout·restore·clean·reset하지 않습니다.
2. `git ls-remote`로 실제 remote branch/tag SHA를 읽고 expected-old를 기록합니다.
3. local HEAD, tracking SHA, branch, tag, merge, stash, dirty, untracked, local-only commit과 worktree를
   기록합니다. dirty·diverged 상태를 임의로 정상화하지 않습니다.
4. root부터 대상 ref까지 graph와 source/config/test/docs phase를 읽습니다. 기존 문서의 basis SHA,
   mapping과 실제 tree를 대조합니다.
5. 공개 이력을 바꾸는 작업이면 mirror, remote archive refs, all-refs bundle, 복원 clone과 bundle
   SHA-256을 먼저 검증합니다.

## 2. 격리 작업

- Desktop 원본 대신 별도 clone/worktree에서 작업합니다. hardlink에 의한 원본 object 공유도 피합니다.
- baseline clone, candidate clone, clean verification clone의 역할을 분리합니다.
- 서브에이전트는 서로 겹치지 않는 경로·번호 범위를 맡고 commit, tag, push를 하지 않습니다.
- 오케스트레이터는 최종 diff와 신규 문서를 전부 직접 읽습니다.

## 3. Baseline과 A/B/C 판정

lockfile과 저장소가 선언한 toolchain으로 install한 뒤 가능한 모든 gate를 독립 실행합니다.

```text
repository/docs checks
lint → typecheck → unit/integration → build
→ E2E/Playwright → accessibility → visual baseline
```

결과를 다음처럼 분류합니다.

| 등급 | 의미 | 처리 |
| --- | --- | --- |
| A | 변경이 불필요하거나 이미 계약을 만족 | 변경 없이 근거만 기록 |
| B | 행동 동일성을 직접 증명할 수 있는 소규모·중간 작업 | characterization 후 구현·검증 |
| C | 규모가 크거나 계약·동일성이 불확실 | 수정 전에 선택지와 승인 gate 보고 |

다음 중 하나면 기본적으로 C입니다.

- source/config/test 10경로 초과
- 3개 초과 모듈 또는 3개 초과 implementation commit
- 25개 초과 commit rewrite
- public component, API, schema, route, build 또는 deploy 계약 영향
- merge/tag/release topology 변경
- baseline red, dirty/local-only/diverged 상태
- hydration, accessibility 또는 visual output의 동일성을 보장할 수 없음

환경 제한은 정확한 오류와 함께 `ENV-LIMIT`로 분리합니다. 실제 source 실패를 환경 제한으로 축소하지
않습니다. 범위 밖 결함은 재현 근거와 영향만 보고하며 승인 없이 버그를 고치지 않습니다.

## 4. Characterization

B 또는 승인된 C 작업은 변경 전에 관찰 가능한 계약을 고정합니다.

- route, status, redirect, query와 public API/schema
- DOM, copy, CSS, asset, href와 responsive layout
- keyboard/focus, ARIA와 axe 결과
- RSC/client 경계, hydration console과 page error
- network/data flow, 상태 소유권, cache와 error/loading/empty 상태
- build artifact와 deploy/runtime 계약

기존 test가 부족하면 dependency 추가 없이 가장 좁은 characterization test를 먼저 만듭니다. 시각
출력이 관련되면 같은 browser, viewport, font와 reduced-motion 조건에서 전후 screenshot을 비교합니다.

## 5. 최소 구현

- 기능 추가, dependency upgrade, copy/content 변경, 시각 재설계와 무관한 정리는 하지 않습니다.
- 책임 분리, 중복 제거, 타입 경계, 상태 소유권, 데이터 흐름과 테스트 구조만 목표 범위에서 바꿉니다.
- 한 commit은 한 검토 가능한 책임을 갖고 path allowlist를 지킵니다.
- source 결함을 문서로 덮지 않습니다. source 의미가 바뀌면 새 basis와 새 corpus mapping을 확정합니다.
- 사용자 변경과 unrelated diff를 보존하며 전체 `git add -A`를 사용하지 않습니다.

## 6. 검증

변경 전후에 같은 명령을 실행하고 다음을 직접 대조합니다.

- lint, typecheck, unit/integration, build, E2E와 accessibility
- 필요 시 visual snapshot과 DOM/style/asset 비교
- `git diff --check`, changed-path allowlist와 clean status
- `git range-diff`, parent/tree/path 비교와 merge/tag topology
- 기존 corpus subtree의 byte 동일성
- 신규 답지의 basis tree 전수 대조와 문제지 drift·수량 reconciliation
- raw author/committer/tagger identity, timestamp, message와 trailer

필수 gate가 red이거나 observable mismatch가 있으면 candidate를 확정하지 않습니다.

## 7. Commit과 공개

검증 뒤에만 `commit-policy.md`에 맞춰 commit합니다. 공개 전에는 remote SHA를 다시 읽습니다.

- append: expected remote가 그대로일 때 fast-forward
- rewrite: `--force-with-lease=refs/heads/main:<expected-old>`
- 새 tag/learning branch: 사전 부재 확인
- main, release tag와 learning branch: 가능하면 하나의 atomic push
- branch 삭제와 repository rename/delete: 보존 ref와 fresh clone 검증 뒤 별도 승인 범위에서 수행

push 후 `ls-remote`, tag object/peeled SHA, branch topology와 visibility/redirect를 다시 확인하고 clean
clone에서 전체 gate를 실행합니다. 실패하면 완료로 보고하지 않습니다.

## 8. 로컬 정리

원격과 clean clone이 유일한 장기 정본이 됐음을 확인한 뒤에만 로컬을 지웁니다.

1. dirty, stash, local-only branch/commit과 고유 artifact가 없는지 다시 확인합니다.
2. exact absolute-path allowlist로 원본 clone, candidate, mirror, worktree, bundle과 임시 결과를 지웁니다.
3. 이 작업이 설치한 `node_modules`, build output와 Playwright browser revision을 정리합니다.
4. Docker는 대상 label/name으로 귀속되는 container/image/volume/network만 제거합니다. 전역 prune과
   다른 프로젝트 cache 삭제는 금지합니다.
5. 삭제 경로 부재, remote ref, Docker 전후 목록과 `df` 전후 여유 공간을 확인합니다.

## 9. 완료 보고

저장소별로 다음을 보고합니다.

```text
repo | old/new main | baseline | A/B/C | source 변경 | history 변경
     | docs 보존/신규 | 검증 | remote/local ref | 삭제·보류 | 승인 필요
```

부분 성공은 부분 성공으로 기록합니다. 미검증, 미공개, 보류 또는 cleanup 대기 상태를 “완료”라고 쓰지
않습니다.
