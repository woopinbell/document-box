# 개발·리팩터링·이력 작업 Workflow

기능 구현, 행동 보존형 refactor, 문서 정리, Git history 재편과 저장공간 정리를 같은 안전 절차로
수행하는 실행 정본입니다. 대상 저장소마다 독립적으로 적용합니다. 일반 작업에서는 한 저장소의 실패가
다른 안전한 저장소 진행을 막지 않습니다. 승인된 30개 정렬 migration은 `legacy-exceptions.md`에 등록한
execution lane마다 현재 저장소의 publication과 fresh-clone이 끝날 때까지 같은 lane의 다음 저장소로
넘어가지 않는 stop-the-line 순서를 따릅니다. 서로 다른 lane의 겹치지 않는 로컬 작업은 병행할 수 있지만
원격 mutation과 governance publication은 전역으로 하나씩만 수행합니다.

## 1. Preflight

작업을 시작하거나 다른 세션에서 인수할 때 먼저 `document-box/main`의 exact commit SHA를 고정하고
`commit-policy.md`, `docs-commit-note.md`, 이 문서, `legacy-exceptions.md`, `tracks/curriculum.json`과 담당
트랙 문서를 현재 object에서 끝까지 읽습니다. 대화 요약, Desktop handoff와 이전 세션의 기억은 범위와
상태를 전달할 뿐 이 read barrier를 대신하지 않습니다. 작업 중 `document-box/main`이 전진하면 다음
phase나 publication 전에 old policy SHA와 new policy SHA의 diff를 읽고, 변경된 규칙이 현재 candidate,
원장과 승인 자료에 반영됐는지 확인합니다. 반영 여부가 불명확하면 remote mutation만 중단합니다.

1. 대상과 제외 대상을 절대경로로 고정합니다. 사용자 변경이 있는 원본, 별도 세션 소유 저장소와
   명시적 hard-exclude 경로는 checkout·restore·clean·reset하지 않습니다.
2. `git ls-remote`로 실제 remote branch/tag SHA를 읽고 expected-old를 기록합니다.
3. local HEAD, tracking SHA, branch, tag, merge, stash, dirty, untracked, local-only commit과 worktree를
   기록합니다. dirty·diverged 상태를 임의로 정상화하지 않습니다.
4. root부터 대상 ref까지 graph와 source/config/test/docs phase를 읽습니다. 기존 문서의 basis SHA,
   mapping과 실제 tree를 대조합니다.
5. 공개 source 이력을 바꾸는 작업이면 정확한 source ref만 fetch한 bare snapshot, source-only bundle,
   복원 clone과 bundle SHA-256을 먼저 검증합니다. Learning ref와 learning-only object는 bundle이나
   preservation ref에 넣지 않습니다.
6. Source 감사에서는 `learning/*`을 별도 집필 surface로 분리하고, source branch·tag 이름,
   annotated tag object, reachable commit metadata·trailer와 tracked tool-control artifact를 전수
   inventory합니다. 제품-domain allowlist는 실제 감사 전에 고정합니다.
7. 일회성 migration이면 source expected-old SHA와 별도로 모든 learning ref의 tip, tree, path와 blob
   OID를 고정하고, source old/new crosswalk와 learning disposition ledger 위치를 먼저 정합니다.
   Learning 본문 bytes를 복제하지 않습니다.
8. Migration 중에는 `legacy-exceptions.md`, registry 전환 뒤에는 `tracks/curriculum.json`의 대상
   `sourceWindow`를 읽고 source commit/tagger 날짜 경계를 고정합니다. 다른 프로젝트 window와
   겹치는 것은 허용하지만 대상 window 이탈은 허용하지 않습니다.

## 2. 격리 작업

- Desktop 원본 대신 별도 clone/worktree에서 작업합니다. hardlink에 의한 원본 object 공유도 피합니다.
- baseline clone, candidate clone, clean verification clone의 역할을 분리합니다.
- Source 분석 서브에이전트는 서로 겹치지 않는 read-only 범위를 맡을 수 있습니다. 본문 집필은 저장소별
  전담 집필자 한 명만 맡고 commit, tag, push를 하지 않습니다.
- 오케스트레이터는 최종 diff와 신규 문서를 전부 직접 읽습니다. 기존 learning corpus의 동일 blob은
  재독하지 않고 신규·변경·고유·충돌 파일만 직접 읽습니다.

### 다중 세션 execution lane과 publication slot

- 한 저장소는 한 시점에 정확히 한 execution lane과 한 담당 세션만 소유합니다. 다른 lane은 그 저장소의
  clone, worktree, candidate, bundle, ref와 원장을 수정하지 않습니다.
- 서로 다른 저장소의 preflight, read-only graph 감사, 격리 candidate replay, build/test와 diff matrix는
  절대경로가 겹치지 않을 때 lane 사이에서 병행할 수 있습니다. 같은 저장소의 source 개발과 집필,
  같은 corpus의 여러 집필자, 같은 원격의 mutation은 병행하지 않습니다.
- `publication slot`은 이번 migration 전체에서 원격 변경 권한을 한 세션에만 주는 전역 배타 lease입니다.
  Project push, force-with-lease, tag·branch 생성·이동·삭제, private repository 생성, `document-box/main`과
  `central-notes/main` publication은 slot 소유자만 수행합니다. Slot은 Git ref나 보존 branch가 아니며
  handoff 문서가 고정한 로컬 원자적 lock 또는 사용자의 명시적 단일 소유권으로 구현합니다.
- Destructive approval을 기다리는 동안 slot을 점유하지 않습니다. 승인을 받은 세션은 push 직전에 slot을
  획득하고 모든 remote ref와 governance `main`을 다시 읽습니다. Expected-old가 승인 자료와 다르면 slot을
  해제하고 새 exact 값으로 approval을 다시 받습니다.
- Slot이 이미 점유됐으면 원격 명령을 재시도하거나 lock을 임의 제거하지 않습니다. 현재 저장소의 로컬
  검증 결과를 보존하고 소유자가 publication·fresh-clone 검증을 끝낼 때까지 원격 단계만 멈춥니다.
- Governance clone이 slot 획득 전 기준보다 뒤처졌으면 stale commit을 force-push하지 않습니다. 최신
  `main`에서 담당 lane의 허용 path·entry 변경만 다시 적용하고 전체 governance gate를 재실행한 뒤
  actual-time commit을 만듭니다. 다른 lane의 commit, registry entry, 단계 카드와 원장을 덮지 않습니다.
- 같은 lane은 현재 저장소의 remote publication, governance pointer와 fresh-clone이 모두 green이어야
  다음 저장소로 이동합니다. 다른 lane은 자기 소유 저장소의 로컬 작업을 계속할 수 있습니다.

### Source 개발과 집필 격리

- 신규 프로젝트는 source 전체 gate가 green이고 release tag·basis가 freeze된 뒤에만 Central Notes와
  learning 집필을 시작합니다. 개발자와 집필자는 같은 사람이 아니며 두 phase를 병행하지 않습니다.
- 저장소마다 전담 집필자 한 명만 둡니다. Central gap, answer와 practice의 경로나 번호를 나눠 여러
  본문 작성자가 동시에 작업하지 않습니다.
- 집필자는 문서 본문만 파일별로 수작업 작성하며 source/config/test를 고치거나 commit, tag, push하지
  않습니다. 생성기·템플릿 치환·본문 pipeline은 금지하고 metadata/hash/path/tree/count/link 검사용
  자동화만 허용합니다.
- 신규 corpus는 모든 answer의 작성과 1회 전수검토가 끝나기 전 practice를 시작하지 않습니다.
  Practice는 완성 answer를 처음부터 읽고 같은 번호별로 한 파일씩 다시 작성합니다. 기존 corpus
  migration은 `docs-commit-note.md`의 blob/tree/diff 통합 절차를 사용합니다.
- Source 결함을 발견하면 집필을 멈추고 개발자에게 반환합니다. 수정 뒤 source hash가 바뀌면 release
  basis를 다시 freeze하고 원장, Central gap과 작성 중인 corpus를 처음부터 재검증합니다.
- 승인된 신규 트랙 추가 작업에서는 현재 저장소의 집필, publication과 fresh-clone 검증까지 끝난 뒤
  다음 저장소 source 개발을 시작합니다.
- 기존 저장소 migration도 source replay → release freeze → learning diff 통합·필요한 본문 보정 →
  `learning/current` → publication → fresh-clone을 한 저장소에서 모두 끝낸 뒤 다음 저장소로 이동합니다.
  이 순서는 lane 내부에서 직렬이며, 모든 lane의 원격 mutation은 위 publication slot으로 직렬화합니다.

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
- 개발 저장소의 source·test·build·reference·README/DESIGN commit은 등록 `sourceWindow` 안에서
  작성합니다. Learner navigation과 집필 본문은 source commit에 섞지 않습니다.

## 6. 검증

변경 전후에 같은 명령을 실행하고 다음을 직접 대조합니다.

- lint, typecheck, unit/integration, build, E2E와 accessibility
- 필요 시 visual snapshot과 DOM/style/asset 비교
- `git diff --check`, changed-path allowlist와 clean status
- `git range-diff`, parent/tree/path 비교와 merge/tag topology
- 기존 learning ref별 tip/tree/path/blob inventory와 final `learning/current` disposition
- 신규 답지의 basis tree 직접 대조, 기존 답지의 old/new source crosswalk와 변경 파일 직접 대조,
  문제지 drift·수량 reconciliation
- raw author/committer/tagger identity, sourceWindow 또는 실제 집필 timestamp, message와 trailer
- Source ref/tag 이름, annotated message, reachable commit metadata와 tracked tool-control artifact의
  금지 provenance 0건
- Source migration의 old/new parent·tree·patch·timestamp crosswalk와 source-only bundle SHA-256·복원
  결과
- Governance 저장소는 원격 `main` 하나, 프로젝트는 `main`과 `learning/current` 두 branch만 존재
- Active corpus에는 `docs/README.md`, `docs/commits/`, `docs/practice/`가 하나씩 있고 versioned duplicate나
  archive subtree가 없음

기존 corpus의 사람 검토는 신규·변경·고유·충돌 파일을 한 번 읽는 것으로 제한합니다. Blocker가
발견되면 수정한 파일·hunk만 재검토하고, source 의미 변경으로 전체 basis가 무효화되지 않는 한 이미
통과한 파일이나 동일 blob을 다시 읽지 않습니다. 이 최적화는 development/source surface의 ref·tag·
metadata·trailer·tracked path/blob provenance 0건 gate에는 적용하지 않습니다. Learning branch와
governance surface의 본문은 그 provenance 제거 대상이 아닙니다.

필수 gate가 red이거나 observable mismatch가 있으면 candidate를 확정하지 않습니다.

## 7. Commit과 공개

검증 뒤에만 `commit-policy.md`에 맞춰 commit합니다. 공개 전에는 remote SHA를 다시 읽습니다.

- append: expected remote가 그대로일 때 fast-forward
- rewrite/non-FF/delete: 변경하는 main, learning과 tag ref마다
  `--force-with-lease=<exact-ref>:<expected-old>`
- 새 tag와 `learning/current`: expected-old 또는 사전 부재 확인
- main, release tag, `learning/current` 전환과 old ref 삭제: 가능한 범위에서 하나의 atomic push
- source main rewrite, tag 이동·삭제와 old learning branch 삭제: 저장소별 exact 대상, expected-old SHA,
  old/new crosswalk, learning disposition과 source-only rollback bundle을 제시한 뒤 destructive approval
  범위에서만 수행
- Approval에는 old learning-only object를 bundle/tag로 보존하지 않으며 remote garbage collection 뒤
  복구할 수 없다는 점을 명시
- Push 직전 전체 remote heads/tags를 다시 읽고, 승인 뒤 하나라도 drift했으면 atomic update 전체 중단

Push 후 `ls-remote`, tag object/peeled SHA, 정확한 branch topology와 visibility/redirect를 다시 확인하고
clean clone에서 전체 gate를 실행합니다. 실패하면 완료로 보고하지 않습니다.

## 8. 로컬 정리

원격과 clean clone이 장기 정본이 됐음을 확인한 뒤에만 로컬을 지웁니다.

1. dirty, stash, local-only branch/commit과 고유 artifact가 없는지 다시 확인합니다.
2. Exact absolute-path allowlist로 candidate, source snapshot, worktree, source-only bundle과 임시 결과를
   지웁니다. Learning branch를 보존하는 bundle이나 archive는 남기지 않습니다.
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
