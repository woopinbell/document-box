# Commit 기반 답지·문제지 규칙

독립 Git 저장소의 실제 source history를 `docs/commits/**` 답지와 `docs/practice/**` 문제지로
재구성하는 정본입니다. Ref topology, identity와 push는 [`commit-policy.md`](commit-policy.md),
작업 격리와 검증은 [`WORKFLOW.md`](WORKFLOW.md)를 함께 따릅니다.

## 1. 핵심 불변식

1. commit object, parent, diff와 **그 commit의 tree**가 사실의 정본입니다.
2. 모든 답지를 먼저 완성하고 직접 검토한 뒤 문제지를 한 파일씩 수작업 파생합니다.
3. 현재 HEAD나 이후 phase의 동작을 과거 commit에 소급하지 않습니다.
4. 근거 없는 동작, 설계 이유와 실행 결과를 추측하지 않습니다.
5. 기존 corpus를 보존하기로 했다면 subtree bytes를 바꾸지 않습니다.
6. 답지·문제지 README는 mapping, 제외/생략 사유와 수량을 완전히 reconcile합니다.

## 2. 절대 금지

다음 방법으로 답지나 문제지 본문을 만들거나 바꾸지 않습니다.

- 생성기, Python, shell loop 또는 본문 분석 pipeline
- `awk`/`sed`/정규식으로 문단을 요약·분류·파생하는 작업
- 템플릿 치환, 답지의 구현 블록 일괄 삭제, 문제지의 역방향 답지화
- 다른 저장소나 기존 문서 문장 복사 후 이름·값만 교체
- 파일 수·heading 검사만으로 직접 정독을 대체

허용되는 자동 검사는 hash, path, tree, file count, metadata, link와 명령 exit status 같은 기계적
불변식뿐입니다. 본문은 commit diff와 source를 직접 읽고 `apply_patch` 또는 편집기로 파일별 작성합니다.

## 3. 기준 ref와 원장

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

## 4. Commit 분류

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

## 5. Answer barrier

답지 대상 commit이 여러 개여도 **답지를 전부 먼저** 작성합니다. 범위를 나눈 경우에도 모든 작성자가
answer phase를 끝내고 교차검토한 뒤에만 practice phase로 넘어갑니다.

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

## 6. 문제지 수작업 파생

완성 답지를 처음부터 다시 읽고 같은 번호의 문제지를 직접 작성합니다. 최상단 배너는 다음과 같습니다.

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
문제지에서 제거합니다. 답지가 바뀌면 문제지를 부분 patch하지 않고 답지 전체에서 다시 파생합니다.

## 7. Mapping과 omission

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

## 8. Branch별 corpus

`learning/<release>`는 release tag에서 분기합니다.

1. 선택적 notes commit: `notes/**`, `docs/notes/**`, `docs/reflection/**`
2. answers commit: `docs/commits/**`와 해당 answer ledger만
3. practices commit: `docs/practice/**`와 해당 practice ledger만

선택적 `docs(notes)` publication은 learning branch 안의 자료를 찾기 위한 `docs/README.md` 한 개를
함께 가질 수 있습니다. 이 파일은 notes·answers·practices의 소비 순서와 링크만 색인하며, 답지 본문이나
source/release 운영 문서를 복제하지 않습니다. `main`의 `docs/README.md`와 책임을 섞지 않고 answers나
practices commit에서 뒤늦게 추가하지 않습니다.

`docs(notes)` 중간 commit에서는 이 색인이 뒤의 publication에서 생길 `docs/commits/**`와
`docs/practice/**`를 미리 링크할 수 있습니다. 중간 tree의 link 검사는 `docs/README.md`에 명시된 이 두
후속 corpus root만 `prospective`로 분류하고, 다른 깨진 내부 링크는 그대로 실패시킵니다. 최종
`learning/<release>` tip에서는 prospective 예외가 0개이고 모든 링크가 실제 path로 해소돼야 합니다.
Answers와 practices commit은 이 링크를 고치기 위해 `docs/README.md`를 다시 변경하지 않습니다.

이 순서는 Git publication 순서입니다. 학습자는 같은 자료를 다음 소비 순서로 사용합니다.

```text
publication: notes → answers → practices
learning: notes → practice → 실행/실패 → answer → 재구현
```

문제지는 답지를 모두 집필·검토한 뒤에만 공개하지만, 학습자는 답지를 열기 전에 문제지를 구현하고
실패 근거를 남깁니다. 답지를 확인한 뒤에는 원본을 복사하지 않고 결정과 경계를 다시 구현합니다.

기존 corpus를 byte 보존하면서 rewrite된 source를 별도로 설명해야 하면
`docs/commits-<revision>/**`, `docs/practice-<revision>/**` 같은 독립 corpus를 둘 수 있습니다. 이때
각 corpus는 자체 README, 전체 mapping, 제외·생략 사유와 수량 reconciliation을 가져야 합니다.

Portfolio release처럼 notes가 없으면 answers → practices 두 commit만 둡니다. Learning branch를
`main`에 merge하지 않습니다.

동일 release의 supplemental/fixup learning branch는 만들지 않습니다. Source release에 종속되지 않는
공통 개념, bridge와 독립 평가는 central-notes에 두며 프로젝트 corpus에 중복 발행하지 않습니다.
기존 공개 learning ref의 migration·삭제·재작성은 이 규칙의 범위가 아닙니다.

## 9. Rewrite와 carry-forward

- Hash만 바뀌어도 basis, parent, tree와 diff를 다시 대조합니다.
- 의미가 달라지면 첫 영향 commit부터 답지를 다시 쓰고 문제지를 재파생합니다.
- 같은 저장소의 이전 corpus만 carry-forward할 수 있으며 새 release에서 basis가 reachable하고
  tree/diff/의미가 같음을 직접 확인해야 합니다.
- 이전 publication처럼 새 release에서 비도달하는 답지는 old immutable learning branch에만 남기고
  stable ID를 reserved로 기록합니다.
- Source 결함을 발견하면 문서로 덮지 않습니다. 미공개 release는 source 확정 전으로 돌아가고,
  공개 immutable release는 새 fix release와 새 ID로 연결합니다.

## 10. 검증과 승인

- 각 답지를 metadata의 기준 commit과 tree에서 직접 대조합니다.
- 문제지 H1, metadata, 작업 순서, H3/책임, 공개 계약과 검증 계약을 답지와 전수 대조합니다.
- README link, mapping, omission과 수량을 실제 graph·파일과 확인합니다.
- 기존 corpus subtree의 byte 동일성과 commit별 path allowlist를 확인합니다.
- 저장소가 선언한 lint/typecheck/test/build/E2E를 isolated checkout에서 실행합니다.
- 최종 담당자는 신규·수정 README, 답지와 문제지를 100% 직접 읽습니다.
- `git diff --check`와 `commit-policy.md`의 raw metadata/ref/push gate를 통과한 뒤에만 공개합니다.
