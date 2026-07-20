# Commit 기반 답지·문제지 규칙

독립 Git 저장소의 실제 source history를 `docs/commits/**` 답지와 `docs/practice/**` 문제지로
재구성하는 정본입니다. Ref topology, identity와 push는 [`commit-policy.md`](commit-policy.md),
작업 격리와 검증은 [`WORKFLOW.md`](WORKFLOW.md)를 함께 따릅니다.

집필자와 저장소 담당자는 source freeze 뒤 본문 작업을 시작하기 전에 `document-box/main`의 exact policy
SHA를 기록하고 이 문서 전체를 직접 읽습니다. Handoff 문서, 기존 answer와 다른 세션의 요약은 이
규칙을 대신하지 않습니다. 집필 중 policy SHA가 바뀌면 answer→practice barrier 또는 publication 전에
변경된 hunk를 읽고 review mode, active path, metadata, 수량식과 집필 순서에 미치는 영향만 다시
판정합니다. 영향 없는 동일 blob을 이 이유만으로 재독하지 않습니다.

## 1. 핵심 불변식

1. commit object, parent, diff와 **그 commit의 tree**가 사실의 정본입니다.
2. 신규 corpus는 전담 집필자 한 명이 모든 답지를 먼저 완성하고 한 번 전수검토한 뒤 문제지를 한
   파일씩 수작업 파생합니다. 기존 corpus 통합은 §9의 blob/tree/diff 재사용 절차를 따릅니다.
3. 현재 HEAD나 이후 phase의 동작을 과거 commit에 소급하지 않습니다.
4. 근거 없는 동작, 설계 이유와 실행 결과를 추측하지 않습니다.
5. 기존 learning corpus는 이름·날짜·tip만으로 자동 정본이 되지 않습니다. Blob 동일성과 final source
   crosswalk가 증명된 내용은 재사용하고, 신규·변경·고유·충돌 내용만 직접 판정해 `learning/current`에
   채택합니다.
6. 답지·문제지 README는 mapping, 제외/생략 사유와 수량을 완전히 reconcile합니다.

## 2. 집필 ownership과 직렬 gate

신규 Learning branch corpus와 그 프로젝트 때문에 필요한 Central Notes 본문은 source 개발과 분리된
집필 작업입니다. 신규 저장소는 다음 순서를 직렬로 지킵니다.

```text
source 전체 gate green
→ release tag와 source basis freeze
→ 필요한 Central gap 수작업 집필
→ answers 전체 수작업 집필
→ answers 1회 100% 직접 검토
→ practices를 같은 번호별로 한 파일씩 수작업 파생
→ practices 1회 100% 직접 검토
→ learning/current publication
```

- 저장소마다 source 개발자와 다른 전담 집필자 한 명이 Central gap, answers와 practices 본문을
  맡습니다. 경로나 번호를 나눠 다른 본문 작성자를 동시에 투입하지 않습니다.
- 서로 다른 execution lane의 서로 다른 저장소에는 각각 전담 집필자 한 명이 존재할 수 있습니다. 이
  병행 허용은 저장소 사이에만 적용하며, 같은 저장소의 source 개발·answer·practice를 여러 세션이나
  작성자에게 나누는 근거가 아닙니다.
- Source freeze 전에는 본문을 쓰지 않습니다. 기존 corpus의 blob/tree/diff inventory는 읽기 전용으로
  미리 만들 수 있지만 source 의미 판정과 본문 보정은 final basis freeze 뒤에만 합니다. 신규 트랙
  프로젝트는 현재 저장소의 집필·publication과 fresh-clone gate까지 끝난 뒤 다음 저장소 source 개발로
  넘어갑니다.
- 집필자는 고정 basis의 commit, parent, tree와 diff를 직접 읽고 집필 허용 path만 수정합니다. Source,
  config, test와 release tag를 수정하지 않고 commit, tag 또는 push하지 않습니다.
- 집필 중 source 결함을 발견하면 문서로 보정하지 않고 작업을 중단해 개발자에게 반환합니다. 개발자가
  source를 고쳐 hash가 바뀌면 기존 freeze는 폐기하며, 새 release basis를 고정한 뒤 원장과 작성 중인
  모든 본문을 처음부터 다시 대조합니다.
- 저장소 담당자는 publication 전에 Central 신규 본문과 신규 learning의 README·answer·practice를
  100% 직접 읽습니다. 기존 corpus 통합은 신규·변경·고유·충돌 파일만 한 번 직접 읽고 동일 blob은
  disposition과 기계적 crosswalk로 검증합니다. 허용 path만 stage하며 집필자에게 publication 권한을
  위임하지 않습니다.
- Learning·Central commit은 실제 집필·검토 시각을 사용합니다. Source window로 backdate하지 않습니다.
- 집필자는 publication slot을 획득하지 않고 remote ref와 governance를 변경하지 않습니다. 저장소
  담당자가 검토·stage·commit을 끝낸 뒤 `WORKFLOW.md`의 전역 slot과 destructive approval gate를
  통과해 공개합니다.

## 3. 절대 금지

다음 방법으로 Central Notes, 답지, 문제지 또는 corpus README의 본문을 만들거나 바꾸지 않습니다.

- 생성기, Python, shell loop 또는 본문 생성·요약·변환 pipeline
- `awk`/`sed`/정규식으로 문단을 요약·분류·파생하는 작업
- 템플릿 치환, 답지의 구현 블록 일괄 삭제, 문제지의 역방향 답지화
- 다른 저장소나 기존 문서 문장 복사 후 이름·값만 교체
- 파일 수·heading 검사만으로 직접 정독을 대체

허용되는 자동 검사는 hash, blob, path, tree, patch-id, file count, metadata, link와 명령 exit status
같은 기계적 불변식뿐입니다. 기존 corpus의 동일 blob·포함관계·변경 hunk를 식별하는 데도 사용할 수
있습니다. 이 검사 결과가 본문 문장이나 TODO를 만들거나 바꾸면 안 됩니다. 신규·변경·고유·충돌 본문은
commit diff와 source를 직접 읽고 `apply_patch` 또는 편집기로 파일별 작성합니다.

## 4. 기준 ref와 원장

문서를 쓰기 전에 release tag 또는 고정 source commit을 확정합니다. Source가 바뀌면 basis를 다시
고정하고 이 단계부터 반복합니다.

원장은 최소한 다음 열을 가집니다.

```text
stable ID ↔ current ordinal ↔ hash ↔ tree ↔ parent hash(es)
          ↔ subject ↔ phase ↔ 분류 ↔ answer ↔ practice 또는 생략 사유
```

### Stable ID와 ordinal

- **stable ID**는 공개된 답지·문제지와 외부 포인터의 영구 식별자입니다.
- **current ordinal**은 특정 reachable graph에서 root를 0으로 센 위치입니다.
- History rewrite, source/learning 분리 또는 release reset으로 ordinal이 바뀌어도 stable ID를
  재번호화하지 않습니다.
- 현행 graph에서 빠진 publication/content commit의 번호는 해당 old release 전용으로 기록하고
  reserved로 둡니다. 새 commit에 재사용하지 않습니다.
- 같은 patch를 새 parent에 replay하면 old basis → current basis crosswalk를 기록하고 tree/parent가
  달라진 이유와 동일성을 보장하는 patch/blob 근거를 적습니다.

## 5. Commit 분류

제목이나 확장자가 아니라 diff의 실체와 재구현 가치를 봅니다.

| 성격 | 답지 | 문제지 |
| --- | --- | --- |
| source·config·build·test의 실질 변경 | 작성 | 작성 |
| 핵심 schema·domain model·validator | 작성 | 공개 계약을 남긴 얇은 문제지 |
| 제품/release 문서, 개인 publication | 작성 또는 원장 설명 | 보통 생략 |
| 자명한 상수·DTO mirror | 조건부 | 보통 생략 |
| empty marker, lockfile-only | 제외 | 제외 |
| 고유 resolution 없는 merge | 제외 | 제외 |
| 고유 resolution이 있는 merge | 실제 resolution에 따라 작성 | 필요 시 작성 |
| binary/generated baseline | 사람의 결정이 있으면 작성 | 보통 생략 |

Delete, rename, binary와 generated path도 실질 commit의 diff 점검에서 빠뜨리지 않습니다. 하나의
commit에 여러 책임이 섞여 있으면 문서를 가짜 commit처럼 분할하지 않고 한 답지에서 모두 설명합니다.

## 6. Answer barrier

신규 corpus는 답지 대상 commit이 여러 개여도 **답지를 전부 먼저** 작성합니다. 번호나 path를 여러
작성자에게 나누지 않으며, 전담 집필자가 answer phase 전체를 끝내고 모든 답지를 처음부터 끝까지 한 번
직접 검토한 뒤에만 practice phase로 넘어갑니다.

기존 corpus migration은 final source crosswalk로 영향 answer 집합을 먼저 고정합니다. 전담 집필자는
`metadata-only`와 `direct-content` answer를 모두 보정하고 그 범위를 한 번 검토한 뒤에만 대응 practice를
다룹니다. `oid-identical` answer는 barrier에서 재독하지 않으며 blob·crosswalk gate로 통과합니다.

답지 기본 구조:

```markdown
# NNN. <작업 단위>

- stable corpus ID: `NNN`
- current source ordinal: `<ordinal>`
- 기준 commit: `<full hash>` — `<subject>`
- legacy basis: `<optional old hash and relation>`
- 부모 commit: `<full parent hash(es)>`
- 기준 tree: `<full tree hash>`
- 변경 범위: `<paths and diff size>`

## 개요
## 작업 순서

### 1. <논리 단위>
**책임:** <보장과 경계>

## 설계 이유
## 검증 계약
## 실제 실행 결과
## 기억/설명 Level
## diff 반영 점검
```

- `## 개요`는 parent의 한계, 목표와 완성 상태를 설명합니다.
- `## 작업 순서`와 번호형 H3는 재구현 의존 순서가 일치해야 합니다.
- 각 H3 바로 아래 `**책임:**`은 무엇을 보장하며 왜 그 경계가 필요한지 설명합니다.
- Source는 signature뿐 아니라 핵심 body·branch·error path, config는 결정 value, test는 input과
  assertion, UI는 state/interaction/accessibility 계약을 보여 줍니다.
- 실행하지 않은 검증을 성공으로 쓰지 않습니다. 역사적 실패, `ENV-LIMIT`와 source 실패를 구분합니다.
- L3는 백지 설명할 결정, L2는 source를 보며 설명할 구조, L1은 찾아볼 세부입니다.
- `diff 반영 점검`에서 모든 changed path와 artifact를 reconcile합니다.

## 7. 문제지 수작업 파생

신규 corpus는 완성 답지를 처음부터 다시 읽고 같은 번호의 문제지를 직접 작성합니다. 기존 corpus는
변경된 answer와 같은 번호의 practice만 answer 전체에서 다시 수작업 파생하며, 동일 blob practice는
그대로 재사용합니다. 최상단 배너는 다음과 같습니다.

```markdown
> 답지에서 수작업으로 파생한 문제지. 직접 수정하지 않는다.
>
> 답: ../commits/NNN.md
```

반드시 유지합니다.

- H1과 stable ID/current ordinal을 포함한 metadata
- 개요와 작업 순서
- 모든 번호형 H3와 `**책임:**`
- 공개 function/type/schema/API와 시작 구조
- 답지와 같은 검증 계약

다음은 책임 중심 TODO로 비웁니다.

- 구현 body와 control flow
- 핵심 config value와 schema constraint 구성
- test fixture/input/assertion
- 학습자가 직접 판단해야 하는 branch·state transition

답을 누설하는 산문 TODO를 쓰지 않습니다. `실제 실행 결과`, 설계 회고, L3/L2/L1과 diff 점검은
문제지에서 제거합니다. 답지가 바뀌면 같은 번호의 문제지를 hunk만 치환하지 않고 해당 답지 전체에서
다시 파생합니다. 다른 번호의 영향 없는 문제지는 다시 쓰거나 재검토하지 않습니다.

## 8. Mapping과 omission

Answer README는 다음을 모두 공개합니다.

- 대상 release/source basis와 tree
- stable ID/current ordinal/hash/parent/subject/phase/classification 전체 mapping
- merge·meta·marker 등 제외 commit과 구체 사유
- old release 전용 또는 reserved ID와 해당 ref
- legacy → current basis crosswalk
- answer는 있지만 practice를 생략한 모든 ID와 사유
- answer, merge/exclusion, reachable commit 수 reconciliation

Practice README는 다음을 모두 공개합니다.

- 제공하는 모든 practice ID, basis와 answer link
- 빠진 모든 answer ID와 생략 사유
- crosswalk가 필요한 legacy practice
- `answers = practices + omissions`
- 답지에서 수작업 파생했다는 계약과 completion gate

대표 수량 불변식:

```text
reachable in-scope commits = answers + commit exclusions
answer 대상 수 = practices + practice omissions
final learning reachable = source/release history + learning publication commits
```

파일을 A/B로 분할했다면 문서 파일 수가 아니라 고유 commit 수로 계산합니다. Self-publication commit은
자기 hash를 순환 기록하지 않고 meta exclusion으로 설명합니다.

## 9. 기존 learning branch 통합 판단

여러 `learning/*` tip이 서로 상위·하위 관계가 아니어도 branch 이름, commit 시각, 파일 수 또는 최신
tip만으로 우열을 정하지 않습니다. 먼저 모든 후보의 tip·tree와 path→blob OID matrix를 만들고, 동일
blob은 corpus 전체에서 한 번만 판정합니다. 공통 blob은 다시 읽지 않으며 다음 파일만 전담 집필자가
final source commit/tree/diff에서 직접 대조합니다.

- 어느 후보에만 존재하는 고유 blob
- 같은 stable ID·path에서 내용이 다른 충돌 blob
- final source crosswalk에서 tree·patch·changed path 또는 공개·검증 계약이 달라진 blob
- old ref, stale link, metadata 또는 active path 정규화 때문에 실제로 수정할 파일

한 후보의 유효 corpus가 다른 후보를 path/blob 기준으로 완전히 포함하면 상위 corpus를 기준본으로
삼습니다. Divergent 후보는 아래 판단 순서로 기준본을 고르고, 다른 후보의 유효한 고유 내용만
파일별로 통합합니다.

판단 순서는 다음과 같습니다.

1. **정확성**: 기준 commit·parent·tree·changed path와 설명이 일치하는가.
2. **공개 계약**: 실제 signature, type, schema, CLI, 상태와 ownership 경계를 빠짐없이 설명하는가.
3. **핵심 흐름**: body, branch, error/rollback/cleanup path를 재구현할 수 있는가.
4. **검증 계약**: test input, fixture, assertion, 실패 조건과 실행 명령이 source와 일치하는가.
5. **완전성**: changed path, answer/exclusion, practice/omission과 수량이 전부 reconcile되는가.
6. **문제지 품질**: 공개 계약과 검증 계약은 남기되 구현 답이나 assertion을 누설하지 않는가.

Source 사실과 충돌하면 source가 우선합니다. 한 branch의 문장이 더 자세해도 틀리면 폐기합니다. 여러
branch의 장점이 나뉘어 있으면 동일 blob을 복제하지 않고, 필요한 고유·충돌 hunk만 final source를 읽어
파일별로 보정합니다. 판단이 해소되지 않은 stable ID가 하나라도 있으면 `learning/current`를 확정하거나
old branch를 삭제하지 않습니다.

사람 검토는 신규·변경·고유·충돌 파일에 대한 한 번의 pass로 제한합니다. Blocker가 발견되면 영향을
받은 파일과 hunk만 고친 뒤 그 범위만 다시 검토합니다. Source basis의 의미 변경이 corpus 전체를
무효화한 경우가 아니면 이미 통과한 공통 blob이나 전체 corpus를 다시 읽지 않습니다.

Document Box disposition ledger에는 다음 metadata만 남깁니다. 삭제할 본문을 복제하거나 bundle로
보존하지 않습니다.

```text
repository / old learning ref / old tip / old tree
stable ID / old path / blob OID / 채택·대체·폐기 / review mode
final source basis / 판단 근거 / reviewer / review 시각
```

Review mode는 다음 세 값만 사용합니다.

- `oid-identical`: 같은 저장소의 blob OID와 final source crosswalk가 동일해 사람 재독 없이 채택
- `metadata-only`: 본문 계약은 같고 hash·ref·path·link metadata hunk만 달라 그 hunk를 한 번 검토
- `direct-content`: 신규·고유·충돌 blob 또는 source 의미 영향 파일을 전체로 한 번 직접 검토

## 10. `learning/current` active corpus

`learning/current`는 고정 release tag 또는 승인된 source tip에서 분기하며 독자가 읽을 유일한 project
learning branch입니다.

1. 선택적 notes commit: `docs/README.md`, `notes/**`, `docs/notes/**`, `docs/reflection/**`
2. answers commit: `docs/commits/**`와 answer ledger
3. practices commit: `docs/practice/**`와 practice ledger
4. 선택적 interview commit: `docs/interview/**`와 `docs/README.md`의 목차 링크

Active tip에는 다음 root가 정확히 하나씩만 존재해야 합니다.

```text
docs/README.md
docs/commits/
docs/practice/
```

- `docs/commits-<release>/**`, `docs/practice-<release>/**`, old corpus archive 또는 duplicate active
  index를 두지 않습니다.
- `docs/README.md`는 notes → practice → 실행/실패 → answer → 재구현의 소비 순서와 실제 link만
  제공합니다. 답지 본문이나 source 운영 문서를 복제하지 않습니다.
- Notes commit의 `docs/README.md`가 뒤 publication root를 prospective link로 가리킬 수 있지만 final
  tip에는 prospective path가 0개여야 합니다. Answers/practices commit에서 index를 뒤늦게 고치지
  않습니다.
- 문제지는 답지 전체 작성·검토 뒤 공개하지만 독자는 답지를 열기 전에 문제지를 수행합니다.
- Notes가 없으면 answers commit이 `docs/README.md`를 함께 만들고 practices까지 두 commit으로
  발행합니다.
- `learning/current`는 `main`에 merge하지 않습니다. 다른 `learning/*`, supplemental/fixup branch와
  archive subtree를 만들지 않습니다.

### 프로젝트 실전 질문

프로젝트 고유 면접 질문은 source release와 answer·practice publication이 모두 고정된 뒤
`docs/interview/README.md`에 수작업으로 작성합니다. 공통 개념 설명은 Central Notes QnA에 두고,
여기에는 해당 프로젝트의 실제 설계·구현·검증 근거가 있어야 답할 수 있는 질문만 둡니다.

- 질문마다 `질문의 의도`, `짧은 답변`, `프로젝트 근거`, `꼬리 질문`, `과장하면 안 되는 범위`를 둡니다.
- `프로젝트 근거`에는 실제 source path, test 또는 관찰 가능한 검증 명령을 적습니다. 실행하지 않은
  결과와 source에 없는 운영 경험은 만들지 않습니다.
- 기존 answer 문장을 질문 형식으로 일괄 변환하지 않습니다. 저장소별 전담 집필자 한 명이 source와
  관련 answer를 직접 읽고 파일 하나를 수작업 작성한 뒤 한 번 전수검토합니다.
- 기존 corpus 뒤에는 실제 집필 시각의 `docs(interview):` commit 하나만 fast-forward로 추가합니다.
  허용 경로는 `docs/interview/**`와 링크를 추가하는 `docs/README.md`입니다.

## 11. Source rewrite와 corpus 재검증

- 모든 answer의 basis, parent, tree, patch-id와 changed path는 old/new crosswalk로 기계적으로
  대조합니다. Hash만 바뀌고 tree·patch·책임이 동일하면 기존 본문을 재독하지 않고 metadata·link처럼
  실제로 달라진 파일만 보정합니다.
- 의미가 달라지면 첫 영향 commit에 대응하는 answer와 그 이후 실제 영향을 받은 answer만 다시 쓰고,
  변경 answer의 검토가 끝난 뒤 대응 practice만 다시 파생합니다. 영향받지 않은 stable ID는 다시 쓰거나
  재검토하지 않습니다.
- 기존 문장은 동일 blob이거나 final source와의 tree·patch·계약 crosswalk가 증명된 경우 재사용할 수
  있습니다. Release 이름만 치환하거나 근거 없이 다른 저장소 문장을 carry-forward하지 않습니다.
- Final source에서 비도달하는 old stable ID는 active corpus에서 제거하고 disposition ledger에
  `폐기` 또는 `reserved` 사유를 남깁니다.
- Source 결함을 발견하면 문서로 덮지 않습니다. Source freeze 전으로 돌아가 수정·검증하고 새 hash로
  모든 mapping을 다시 시작합니다.
- Old learning branch 삭제는 `commit-policy.md`의 destructive approval 뒤 수행합니다. Bundle이나
  preservation tag는 만들지 않으며 remote garbage collection 뒤 복구 불가능할 수 있습니다.

## 12. 검증과 승인

- 신규 답지는 metadata의 기준 commit과 tree에서 직접 대조합니다. 기존 답지는 전체 crosswalk를
  기계적으로 검사하고 신규·변경·고유·충돌 파일만 직접 대조합니다.
- 신규 문제지는 H1, metadata, 작업 순서, H3/책임, 공개 계약과 검증 계약을 답지와 한 번 전수
  대조합니다. 기존 문제지는 전체 구조를 기계적으로 검사하고 변경·충돌 파일만 직접 대조합니다.
- README link, mapping, omission과 수량을 실제 graph·파일과 확인합니다.
- Active corpus root가 하나씩이고 versioned duplicate/archive가 없는지 확인합니다.
- `reachable source commits = answers + exclusions`, `answers = practices + omissions`를 확인합니다.
- Learning publication commit별 path allowlist와 실제 집필 timestamp를 확인합니다.
- 저장소가 선언한 lint/typecheck/test/build/E2E를 isolated checkout에서 실행합니다.
- 최종 담당자는 신규 Central·corpus 본문을 100% 직접 읽고, 기존 corpus는 신규·변경·고유·충돌 파일을
  한 번 직접 읽어 disposition마다 reviewer 결정을 기록합니다. Blocker 수정 뒤에는 해당 파일만 다시
  읽습니다.
- `git diff --check`와 `commit-policy.md`의 raw metadata/ref/push gate를 통과한 뒤에만 공개합니다.
