# 커밋 기반 dual-form 문서 집필 정본

독립 git 저장소의 실제 이력을 `docs/commits/**` 답지와 `docs/practice/**` 문제지로 재구성하는
공통 규칙이다. 기존 문서가 전혀 없는 저장소, 불완전한 문서만 있는 저장소, 후속 phase나 이력
재작성으로 기준 hash가 바뀐 저장소에 모두 적용한다. 저장소별 commit 수·언어·프레임워크·현재
문서 수는 이 규칙의 적용 여부를 바꾸지 않는다.

> **복합 작업 필수 정본:** 이 문서는 commit별 분류·답지 집필·문제지 파생·검증을 결정한다.
> commit object의 identity·timestamp·message, release ref topology와 push는 반드시
> [`commit-policy.md`](commit-policy.md)를 함께 따른다. 이력 재작성과 from-zero dual-form을 함께
> 수행할 때의 순서는 **commit-policy로 topology·metadata 확정 → source hash/tag 고정 → 이 문서로
> 답지·문제지 집필 → commit-policy의 commit/push gate**다.

## 적용 단위와 제외 범위

- **작업 단위는 독립 git 저장소 하나**다. 여러 저장소를 담은 상위 폴더를 한 저장소처럼 묶지
  않는다. `.git` 경계를 직접 확인한다.
- 독립 저장소는 자기 commit history에 근거한 `docs/commits/`를 가져야 한다. 문서가 없거나 비어
  있으면 규칙의 예외가 아니라 from-zero 작성 대상이다.
- `document-box`처럼 여러 저장소의 거버넌스를 관리하는 허브, 비-git 기획 허브, 출하·취업 실행
  허브는 dual-form 대상이 아니다. 현행 대상 목록과 명시적 제외는 [`AUDIT.md`](AUDIT.md)를 따른다.
- 저장소 사용자가 읽어야 하는 설치·API·architecture·license 문서와 dual-form을 혼동하지 않는다.
  전자는 제품 tree의 문서이고, 후자는 확정된 개발 이력을 복원·학습하기 위한 문서다.

## 목표와 불변식

dual-form은 같은 작업 단위를 서로 다른 목적으로 보여 준다.

- `docs/commits/NNN.md` — **답지이자 정본**. 실제 commit과 그 tree의 완성 코드·설정·테스트·문서,
  설계 이유, 검증 결과를 설명한다.
- `docs/practice/NNN.md` — **답지에서 수작업 파생한 문제지**. 공개 계약과 작업 경계는 유지하고
  구현·제어 흐름만 책임 중심 TODO로 비운다.

다음 불변식을 항상 지킨다.

1. git commit, parent, diff와 **그 기준 commit의 tree source**가 사실의 정본이다. 현재 HEAD의
   소스나 다른 phase의 지식을 과거 commit 설명에 소급하지 않는다.
2. 답지를 먼저 완성한다. 문제지를 독립적으로 창작하거나 기존 문제지에서 답지를 역산하지 않는다.
3. 근거를 찾지 못한 동작·설계 이유·검증 결과를 추측하지 않는다. 불명확하면 해당 근거를 더 읽고,
   그래도 확정할 수 없으면 사실과 해석을 구분해 기록하거나 작업을 중단한다.
4. 답지와 문제지는 commit의 의미 단위를 빠짐없이 다루되, diff를 그대로 덤프하지 않는다. 학습자가
   변경을 다시 설명하고 구현할 수 있을 만큼 실제 artifact와 책임 경계를 보여 준다.
5. 생성·분석·일괄 파생 스크립트와 다른 저장소 문장 복사는 금지한다. 작성자는 commit과 source를
   직접 읽고 파일별로 수작업 편집한다.

## 허용 도구와 금지 도구

### 허용

- `git log`, `git show`, `git diff`, `git status`, `git rev-parse`, `git ls-tree`로 commit·parent·path·
  source를 **직접** 읽는다.
- 편집기나 `apply_patch`로 개별 문서를 수작업 작성한다.
- 저장소가 정의한 lint, typecheck, unit, integration, build, E2E 명령을 실행한다.
- hash·path·파일 수·raw metadata처럼 본문을 창작하지 않는 기계적 불변식 검사는 사용할 수 있다.
- `rg` 같은 검색은 읽어야 할 위치를 찾는 탐색 보조로만 사용한다.

### 금지

- Python, shell loop, 생성기, 템플릿 치환으로 답지나 문제지 본문을 만들거나 복제하지 않는다.
- `awk`·`grep`·`sed` pipeline이나 본문 분석 pipeline으로 commit 내용을 요약·분류·문서화하지
  않는다. 분류와 설명은 사람이 diff와 source를 직접 읽고 판단한다.
- 답지에서 문제지를 일괄 삭제·치환하거나 기존 문제지에서 답지를 복원하는 스크립트를 쓰지 않는다.
- 다른 저장소의 `docs/commits/**`나 `docs/practice/**` 문장을 복사해 빈칸만 바꾸지 않는다.
- 파일 수나 heading 일치 같은 기계 검사만으로 정독과 의미 검토를 대체하지 않는다.

## 전체 절차

### 1. preflight와 기준 ref 확정

작업 전에 다음을 직접 확인하고 기록한다.

1. repository root, 현재 branch, working tree와 untracked 파일을 확인한다. 기존 사용자 변경을
   복구·삭제·stage하지 않는다.
2. local/remote branch, tag, merge topology와 대상 release ref를 읽는다. 이력 재작성이라면
   `commit-policy.md`의 bundle·expected-old SHA·approval 규칙을 먼저 적용한다.
3. 문서의 기준이 될 release commit 또는 고정 ref를 확정한다. release-boundary 저장소에서는
   template tag, release tag, `main`, `learning/<release>` 경계를 함께 기록한다.
4. root commit부터 기준 ref까지 전체 graph와 각 commit의 parent를 직접 읽는다. merge는 first-parent
   제목만 보고 분류하지 않고 parent별 diff와 고유 resolution을 확인한다.
5. 기준 hash와 tag가 확정되기 전에는 최종 번호나 문서 본문을 쓰지 않는다. source를 고치면 hash를
   다시 확정하고 이 단계부터 반복한다.

### 2. commit 원장 동결

집필 전에 다음 열을 가진 원장을 만들고 동결한다.

```text
NNN ↔ hash ↔ parent hash(es) ↔ subject ↔ phase ↔ 분류
    ↔ 답지 유무 ↔ 문제지 유무 또는 제외 사유
```

- root부터 기준 ref까지 순서를 정하고, 각 실질 commit에 안정적인 `NNN`을 부여한다.
- 각 행에서 changed path, rename/delete/binary/generated 여부와 diff 규모도 확인해 집필 범위를 잡는다.
- 제외한 commit도 원장에서 지우지 않는다. hash·subject·정확한 제외 사유를 남긴다.
- 한 번 공개된 번호는 다시 쓰거나 앞 번호를 재배정하지 않는다. 후속 phase는 마지막 번호 다음에
  append한다.
- release-boundary 재작성으로 이전 publication commit이 새 release ancestry에서 빠지면 그 답지 번호는
  기존 immutable `learning/<old-release>`에만 남긴다. 새 원장에는 `이전 release 전용·현행 ref 비도달`로
  기록하고 번호를 재사용하지 않으며, 새 commit은 역대 마지막 번호 뒤에 append한다.
- 최종 원장은 `docs/commits/README.md`에 독자가 확인할 수 있는 형태로 공개한다.

### 3. 실체성 분류

파일 확장자나 기존 문서 유무가 아니라 실제 diff와 재구현 가치로 분류한다.

| commit 성격 | 답지 | 문제지 | 판단 기준 |
|---|---:|---:|---|
| 실질 source·config·build·test | 작성 | 작성 | 동작·제어 흐름·검증을 다시 유도할 수 있다 |
| 핵심 domain model·schema·validator | 작성 | 얇게 작성 | 공개 계약은 노출하고 핵심 제약 구성만 비운다 |
| 순수 제품 문서·구체 placeholder·개인 publication | 작성 | 생략 | 역사적 결정은 설명하되 재구현 문제로 만들지 않는다 |
| 자명한 DTO mirror·상수 복제 | 조건부 | 보통 생략 | 독립 설계 가치가 있으면 답지, 없으면 사유와 함께 제외한다 |
| 빈 marker·lockfile-only | 제외 | 제외 | 독립적으로 설명하거나 재유도할 결정이 없다 |
| 고유 resolution 없는 merge | 제외 | 제외 | parent를 합친 것 외에 새 결정이 없다 |
| 고유 resolution이 있는 merge | diff에 따라 | diff에 따라 | merge가 직접 만든 resolution을 별도 실질 변경처럼 다룬다 |
| standalone binary/generated baseline | 조건부 | 보통 생략 | 사람이 정한 입력·검증이 있으면 답지, 기계 산출만 있으면 제외한다 |
| revert·fixup | diff에 따라 | diff에 따라 | 제목이 아니라 실제로 바뀐 동작과 학습 가치를 본다 |

- 실질 commit 안의 delete, rename, binary, generated baseline은 답지 범위에서 빠뜨리지 않는다.
- 여러 성격이 섞인 commit은 쪼개 보이게 꾸미지 않고 답지 하나에서 모든 changed path를 설명한다.
  실질 구현이 하나라도 있으면 문제지를 만들되 publication 값 같은 답을 연습 과제로 만들지 않는다.
- 순수 문서라도 release/reset 계약, API 결정, migration 이유처럼 이력 이해에 필요한 내용이면 답지를
  작성한다. 단순 오탈자처럼 독립 설명 가치가 없으면 원장에 사유를 쓰고 제외할 수 있다.
- `A`/`B` 파일 분할은 한 commit이 한 문서로 읽기 어려울 만큼 클 때만 허용한다. 두 파일 모두 같은
  hash를 명시하고 README 원장에서 분할 이유와 범위를 적는다. 문서 수를 늘리기 위한 분할은 금지한다.

### 4. 작업 규모와 역할 분할

기존 문서 파일 수가 아니라 **원장에서 답지 대상으로 판정한 실질 commit 수**로 규모를 정한다.

- 15개 이하: 한 작성자가 전체 답지와 문제지를 맡을 수 있다.
- 16–39개: 두 개의 연속 번호 범위로 나눈다.
- 40개 이상: 세–네 개의 연속 번호 범위로 나누고 동시 작업 한도를 지킨다.

분할할 때도 다음 순서를 강제한다.

1. 오케스트레이터가 원장, 분류, 번호와 한 개의 exemplar를 먼저 확정한다.
2. 각 작성자는 자기 연속 범위의 **답지를 전부 먼저** 쓴다. 일부 문제지를 먼저 만들지 않는다.
3. 전체 답지 선집필 barrier를 통과한 뒤 각 작성자가 자기 답지에서 문제지를 수작업 파생한다.
4. A→B, B→C, C→A처럼 자기 범위가 아닌 연속 범위를 순환 교차검토한다. 두 명이면 서로 교차한다.
5. 최종 담당자는 README를 포함한 모든 파일을 100% 정독한다. 표본 검수로 승인하지 않는다.

## 답지 작성 계약

각 포함 commit은 아래 구조를 가진다. 저장소 언어에 맞게 code fence와 명령은 달라질 수 있지만
필수 heading과 책임 정보는 생략하지 않는다.

```markdown
# NNN. <commit 작업 단위 제목>

- 기준 commit: `<hash>` — `<subject>`
- 부모 commit: `<parent hash>` (merge면 전부)
- 변경 범위: `<핵심 path와 artifact>`

## 개요

## 작업 순서

### 1. <논리 단위>

**책임:** <무엇을 보장하고 왜 이 경계가 필요한지>

<실제 코드·설정·테스트·문서와 설계 이유>

## 검증 계약

## 실제 실행 결과

## 기억/설명 Level

## diff 반영 점검
```

### metadata와 개요

- 기준 hash는 README 원장과 같아야 한다. 축약 hash를 쓰더라도 단 하나의 commit으로 해석 가능해야
  하며, parent는 실제 parent를 적는다.
- `## 개요`는 결과만 나열하지 않고 이전 parent의 한계, 이번 commit의 목표와 완성 상태를 설명한다.
- `## 작업 순서`는 commit을 다시 구현할 때의 의존 순서다. changed-file 목록을 그대로 옮기지 않는다.

### 번호형 논리 단위

- 모든 H3는 `### 1.`, `### 2.`처럼 번호를 붙이고 작업 순서와 대응시킨다.
- 각 H3 바로 아래에 정확히 `**책임:**` 줄을 둔다. “무엇을 만든다”만 반복하지 말고 해당 단위가
  보장하는 결과와 경계를 쓴다.
- 실제 artifact는 signature나 key 이름만 인용하지 않는다. 핵심 body, control flow, constraint,
  assertion이 보이도록 필요한 만큼 제시한다.
- 설계 이유는 diff에서 관찰되는 선택과 저장소 문맥에 근거한다. 확인할 수 없는 저자의 심리를
  사실처럼 쓰지 않고, 대안·trade-off가 실제 계약에 미친 영향을 설명한다.

### artifact별 충실도

- **source code:** 공개 signature와 핵심 body·branch·state transition·error path를 보여 준다.
- **config/build:** 구조와 key뿐 아니라 동작을 결정하는 value·directive·stage 관계를 보여 준다.
- **test:** case 의도, fixture/input, 핵심 assertion과 실패 시 잡아내는 회귀를 보여 준다.
- **UI:** markup 구조, state/interaction, style 또는 responsive/accessibility 계약을 함께 다룬다.
- **문서:** 새로 정한 사용·API·release 계약의 정확한 문구나 명령을 필요한 범위에서 보여 준다.
- **delete/rename:** 왜 사라지거나 이동했고 reference/import/path가 어떻게 정리됐는지 설명한다.
- **binary/generated:** bytes를 전사하지 않는다. source/input, 경로, 형식·크기·role과 검증 방법을
  기록한다. 실질 commit의 산출물이라는 이유로 점검에서 생략하지 않는다.

### 검증과 회고

- `## 검증 계약`은 답지와 문제지가 공유하는 실행 가능한 계약이다. 명령, 전제조건과 관찰 가능한
  성공 결과를 적는다. 단순 파일 존재나 문자열 검색만으로 동작 검증을 대신하지 않는다.
- `## 실제 실행 결과`에는 작성 중 실제로 실행한 환경·명령·결과를 쓴다. 계약과 결과를 섞지 않는다.
- 역사적 commit에서 예상되는 실패는 정확한 error와 그 시점의 제약을 기록한다. 현재 HEAD에서의
  성공을 과거 commit 성공으로 쓰지 않는다.
- `## 기억/설명 Level`은 다음 세 수준을 모두 쓴다.
  - **L3:** 문서 없이 백지에서 설명·작도할 핵심 결정.
  - **L2:** source를 펼쳐 책임·흐름·예외를 설명할 내용.
  - **L1:** 필요할 때 찾아 읽어도 되는 세부.
- `## diff 반영 점검`은 `git show`의 모든 changed path를 열거하거나 명확한 묶음으로 reconcile한다.
  추가·수정뿐 아니라 delete·rename·binary·generated baseline까지 누락 0임을 설명한다.

## 문제지 수작업 파생 계약

문제지는 해당 답지가 완성·검토된 뒤 같은 파일을 옆에 두고 한 파일씩 수작업 파생한다. 최상단에는
아래 배너를 그대로 사용한다.

```markdown
> 답지에서 수작업으로 파생한 문제지. 직접 수정하지 않는다.
>
> 답: ../commits/NNN.md
```

### 반드시 유지할 것

- H1 작업 단위 제목
- 기준 commit, parent commit, 변경 범위 metadata
- `## 개요`와 `## 작업 순서`
- 답지의 모든 번호형 H3와 순서
- 각 H3의 `**책임:**` 줄
- 공개 function/type/schema/API signature, 시작에 필요한 파일·구조 계약
- 답지와 동일한 `## 검증 계약`

### 비울 것과 제거할 것

- 구현 body, control flow, 핵심 config value, schema constraint 구성, test input/assertion을
  `TODO`로 비운다. TODO는 **책임과 성공 조건**을 말하고 구현 절차나 답을 산문으로 누설하지 않는다.
- 공개 계약까지 지워 학습자가 시작점을 잃게 하지 않는다. 반대로 핵심 알고리즘을 그대로 남겨
  베껴 쓰는 문제가 되지 않게 한다.
- 답지의 `## 실제 실행 결과`, 설계 이유·회고, `## 기억/설명 Level`, `## diff 반영 점검`은 제거한다.
- placeholder·publication 값처럼 사용자가 외울 이유가 없는 구체 데이터는 문제로 만들지 않는다.

문제지를 먼저 고치지 않는다. 답지가 바뀌면 기존 문제지에 부분 patch를 이어 붙이지 말고, 답지를
처음부터 다시 대조해 영향받은 문제지 전체를 수작업 재파생한다.

## README 계약과 수량 reconciliation

### `docs/commits/README.md`

다음을 한 문서에서 확인할 수 있어야 한다.

- 대상 release/ref, template/reset 경계와 문서가 설명하는 source 범위
- phase별 번호 범위와 시작 commit
- 전체 `NNN ↔ hash ↔ parent ↔ subject ↔ phase ↔ 분류 ↔ 답지/문제지` 매핑
- 이전 release 전용이라 현행 ref에서 도달하지 않는 영구 번호와 그 release/ref
- 제외 commit의 hash·subject·구체 사유
- 답지는 있으나 문제지가 없는 모든 번호와 사유
- 답지 파일 수, 제외 commit 수, 기준 ref까지의 in-scope commit 수 reconciliation
- 읽는 순서와 각 답지·문제지 링크

필수 수량 불변식은 다음과 같다.

```text
기준 ref에서 도달 가능한 in-scope commit 수
= 번호형 답지로 포함한 commit 수 + 사유를 명시해 제외한 commit 수
```

한 commit을 `A`/`B`로 나눴다면 파일 수가 아니라 고유 commit 수로 계산하고 분할 행에서 설명한다.

### `docs/practice/README.md`

- 대상 release/ref, template/reset 경계와 phase별 번호 범위
- `docs/commits/README.md`의 전체 mapping·제외 commit 원장에 대한 정본 link
- 문제지 사용 순서와 답지 확인 시점
- 제공하는 모든 번호와 링크
- 빠진 모든 답지 번호 및 각각의 생략 사유
- `현행 답지 대상 수 = 문제지 수 + 문제지 생략 수` 파일 수 reconciliation
- 구현·테스트·검증을 끝냈다고 판정하는 completion gate
- 답지에서 수작업 파생했으며 문제지를 직접 수정하지 않는다는 원칙

## 검증 절차

### 기준 commit과 isolated checkout

- 각 답지는 현재 HEAD가 아니라 문서 metadata의 **기준 commit과 그 tree**에 대조한다.
- 과거 commit의 명령은 현재 working tree를 오염시키지 않는 isolated worktree/checkout에서 실행한다.
  해당 commit의 lockfile과 toolchain 계약을 우선한다.
- 문서에 적은 모든 검증 명령을 실제 실행한다. route 수·worker 수·test 수처럼 서로 다른 개념을
  간접 지표로 추정하지 않고 계약이 요구한 결과를 직접 관찰한다.

### 실패 분류

1. **예상된 역사적 실패:** 그 commit이 의도적으로 다음 phase 전의 red 상태이거나 당시 환경 제약이
   재현된 경우다. 정확한 명령·error·후속 해결 commit을 답지에 기록한다.
2. **환경 재현 한계:** 사라진 외부 서비스나 지원 종료 toolchain 때문에 실행할 수 없는 경우다.
   가능한 정적 계약과 대체 관찰을 명시하되 성공했다고 쓰지 않는다.
3. **실제 source 결함:** 문서가 설명하는 계약을 source가 만족하지 못한다. 문장으로 덮거나 예상
   실패로 바꾸지 않는다. 미공개 release라면 tag·문서 확정 전 단계로 돌아가 source를 고치고 새
   hash부터 재확정한다. 이미 공개된 immutable release라면 tag를 이동하지 않고 결함을 사실대로
   기록한 뒤 새 fix phase·새 release에서 수정하고 과거 답지와 새 번호를 연결한다.

### 전수 드리프트 검사

각 답지/문제지 쌍을 직접 펼쳐 다음을 모두 대조한다.

- H1, 기준 commit·parent·scope metadata
- `## 개요`, `## 작업 순서`
- 모든 번호형 H3의 제목·순서와 `**책임:**`
- 공개 계약과 `## 검증 계약`
- 문제지에 완성 구현·결과·회고가 남지 않았는지
- 답지의 모든 changed path가 `## diff 반영 점검`에 포함됐는지

heading 목록을 기계적으로 비교하는 것은 보조 검증일 뿐이다. 작성자는 `git show`와 tree source를,
교차검토자는 답지와 문제지를 직접 읽는다.

### 교차검토와 최종 승인

- 분할 작성이면 A→B, B→C, C→A 순환으로 다른 범위를 검토한다. 검토자는 명백한 오류를 직접
  고치고, source 판단이 필요한 쟁점은 근거와 함께 최종 담당자에게 보고한다.
- 최종 담당자는 원장·두 README·모든 답지·모든 문제지를 100% 정독한다.
- 표본 몇 개의 품질이나 파일 수 일치만으로 from-zero corpus 전체를 승인하지 않는다.
- `git diff --check`, link, path scope, raw metadata와 commit 분리 검사를 마친 뒤에만 commit한다.

## from-zero 실행 상태 머신

문서가 하나도 없는 저장소에서는 아래 순서를 건너뛰지 않는다.

### A. Inventory

기준 ref와 전체 graph를 읽고 원장을 동결한다. 분류·번호·제외 사유·문제지 유무를 집필 전에
확정하고 README 초안의 수량을 reconcile한다.

### B. Answer barrier

모든 답지를 먼저 수작업 집필한다. 각 문서를 기준 commit의 diff와 tree에 대조하고 검증 계약을
실행한다. 답지 전체가 검토되기 전에는 문제지 phase로 넘어가지 않는다.

### C. Practice derivation

문제지 대상 답지를 한 파일씩 옆에 두고 수작업 파생한다. canonical 배너와 유지/제거 계약을 적용한
뒤 practice README에서 모든 생략 번호를 설명한다.

### D. Full review

순환 교차검토, 최종 담당자의 100% 정독, 기준 source 대조, 실제 명령 실행, diff·수량·드리프트
검사를 완료한다. source 결함이면 B를 억지로 끝내지 않고 §실패 분류를 적용한다. 미공개 release는
source 확정 전 단계로 돌아가고, 공개 immutable release는 tag를 보존한 채 새 fix release로 넘긴다.

### E. Commit and publish

답지와 문제지를 별도 commit으로 만들고 `commit-policy.md`의 identity·timestamp·topology·push gate를
적용한다. 실패·부분 완료·원격 drift 상태에서는 publish하지 않는다.

## 기존 문서 상태별 복구

- **문서 없음:** from-zero 상태 머신 전체를 따른다.
- **문제지형 문서만 있음:** 문제지를 정본으로 승격하지 않는다. source에서 답지를 새로 쓰고 그
  답지에서 문제지를 다시 파생한다.
- **산문-only 답지:** TODO 유무로 완성도를 판단하지 않는다. 기준 source의 signature와 핵심 body·
  control flow가 보이도록 답지를 재작성한 뒤 문제지를 다시 파생한다.
- **답지형 문서 있음:** hash·parent·tree·diff를 다시 대조한다. 형식과 coverage를 보강하고 영향받은
  문제지를 수작업 재파생한다.

## 후속 phase와 history rewrite

- **문서의 사실 오류만 수정:** 번호와 source phase를 유지한다. 답지를 먼저 고치고 대응 문제지를
  전부 다시 대조해 파생한다.
- **source 의미 변경:** 새 implementation phase와 새 commit을 만들고 마지막 번호 뒤에 새 답지를
  append한다. 과거 번호를 덮어쓰지 않는다.
- **알려진 source 결함 수정:** 과거 답지의 결함 기록은 삭제하지 않고 수정 phase와 새 번호를
  연결해 이력을 보존한다.
- **hash만 바뀐 rewrite:** tree와 diff가 같아도 모든 기준/parent hash를 직접 재대조하고 README와
  문서 metadata를 갱신한다.
- **의미가 달라진 rewrite:** 첫 영향 commit부터 답지를 기준 source에서 다시 쓰고 대응 문제지를
  수작업 재파생한다. 제목이나 path가 같다는 이유로 재사용하지 않는다.
- **release-boundary 후속 release:** 새 `learning/<release>`에는 그 release의 전체 현행 corpus를
  정확히 두 commit으로 싣는다. 같은 저장소의 기존 답지는 기준 hash·tree·diff와 의미가 그대로임을
  다시 검증하고 새 release ref에서 그 basis commit에 도달할 수 있는 경우에만 carry-forward한다.
  이전 publication처럼 현행 ref에서 비도달하는 답지는 기존 immutable learning branch에만 보존하고,
  새 README에서 영구 번호와 이전 release 전용 사유를 기록하되 현행 도달 commit reconciliation에서는
  제외한다.

## commit과 push

- 일반 phase 저장소에서는 검증된 답지를 `docs(commits)` commit, 문제지를 `docs(practice)` commit으로
  분리해 main의 해당 phase 문서 블록에 둔다.
- release-boundary 저장소에서는 release tag에서 `learning/<release>`를 만들고 첫 commit은
  `docs/commits/**`만, 둘째는 `docs/practice/**`만 변경한다. 정확한 ref graph는
  `commit-policy.md`가 정본이다.
- `git add -A`로 무관한 사용자 변경을 포함하지 않는다. 각 commit의 허용 경로만 명시적으로 stage한다.
- raw author/committer identity·ISO timestamp·message/trailer를 commit object에서 직접 검증한다.
- force push, tag 발행·삭제, remote branch 변경은 사용자의 명시적 권한과 `commit-policy.md`의
  backup·lease·atomic·fresh-clone gate가 있을 때만 수행한다. “문서가 완성됐다”는 사실이 자동
  publish 권한을 뜻하지 않는다.

## 금지 요약

- 답지 없는 문제지 독립 창작, 문제지 직접 보강, 과거 source에 현재 HEAD 동작 소급
- 생성기·Python·shell loop·본문 분석 pipeline·템플릿 치환·다른 저장소 문장 복사
- 빈 marker·lockfile-only·고유 resolution 없는 merge를 억지로 학습 문제화
- delete·rename·binary·generated path를 diff 점검에서 생략
- 검증 명령을 실행하지 않고 통과로 기록하거나 source 결함을 문서 설명으로 은폐
- 표본 검수만으로 from-zero corpus 승인, released 번호 재배정
- 무관한 working-tree 변경 stage, 부분 실패 상태 commit, 권한 없는 remote rewrite
