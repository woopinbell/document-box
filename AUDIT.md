# AUDIT.md — dual-form·release history 전체 재검수 절차

이 문서를 읽은 세션은 모든 독립 저장소의 commit 기반 답지(`docs/commits/**`), 수작업 파생 문제지
(`docs/practice/**`)와 공개 release 경계를 검증하는 **read-only 감사 오케스트레이터**로 작동한다.
코드·문서·ref를 고치거나 commit·push하지 않는다. 결함은 근거와 함께 보고하고 사용자 지시를 기다린다.

시작 전에 다음 정본을 모두 읽는다.

1. [`corpus-router.md`](corpus-router.md) — 작업 라우팅
2. [`docs-commit-note.md`](docs-commit-note.md) — commit 분류·답지·문제지·검증 계약
3. [`commit-policy.md`](commit-policy.md) — raw metadata·phase·release topology·push 계약

## 0. 감사 원칙

- **기준 commit 우선:** 답지는 현재 HEAD나 현재 source 전체가 아니라 문서에 적힌 기준 commit과 그
  commit의 tree를 정본으로 감사한다. 문제지는 그 답지를 정본으로 감사한다.
- **직접 정독:** 기계 검사는 path·hash·수량·명령 exit status 같은 불변식의 보조일 뿐이다. 문서 본문,
  source artifact, 설계 이유와 TODO 책임은 사람이 직접 읽고 판단한다.
- **본문 분석·생성 스크립트 금지:** Python, shell loop, grep/awk/sed pipeline으로 본문을 추출·요약·
  비교하지 않는다. `git show`와 해당 tree source를 직접 열어 파일별로 대조한다.
- **추측 금지:** 근거를 확보하지 못하면 PASS나 FAIL을 단정하지 않고 `확인필요`로 분류해 필요한
  증거를 적는다.
- **실패 구분:** 환경 재현 한계, 예상된 역사적 실패, 실제 source 결함을 구분한다. source 결함을
  문서 표현 문제로 축소하지 않는다.

## 1. 현행 대상 inventory

워크스페이스에서 `.git` 경계를 직접 열거한 독립 저장소가 대상이다. `document-box`는 거버넌스 허브,
`launch-box`는 private 출하·취업 허브이므로 제외한다. `plan-box`는 비-git 허브라 자동 제외된다.
멀티레포 폴더는 폴더 자체가 아니라 발견된 하위 저장소 각각을 센다.

기준일 현재 대상은 **41개**다.

- 최상위 독립 저장소 26개
- `sportsbook/` 하위 독립 저장소 10개
- `ai-capstone/` 하위 독립 저장소 5개

이 숫자는 실행 때 실제 `.git` inventory와 대조한다. 신규·이동 저장소가 있으면 발견 결과를 우선하고
최종 보고에서 이 목록의 갱신 필요성을 알린다. `portfolio-public`은 deployable `main`이 아니라 해당
release의 dual-form을 보관하는 `learning/portfolio-v1`을 감사한다.

## 2. 감사 준비와 역할 분할

### 저장소별 preflight

각 저장소에서 다음을 직접 확인한다.

- repository root, current branch/ref, working tree 상태, remote tracking과 local/remote SHA
- `docs/commits/README.md`가 선언한 기준 release/ref, phase와 전체 mapping
- release-boundary 여부와 template/release/learning ref
- 답지 수, 문제지 수, 제외 commit 수와 README reconciliation

dirty tree나 remote drift가 있으면 read-only 감사를 계속할 수는 있지만 상태를 별도 결함/위험으로
기록한다. checkout이나 branch 전환이 기존 변경을 건드릴 가능성이 있으면 그 저장소의 실행 검증을
중단하고 `확인필요`로 올린다.

### 분담

- 기본 작업 단위는 저장소 하나다. 여러 저장소는 저장소별 검토자에게 나눌 수 있다.
- 큰 저장소는 `docs-commit-note.md`의 **실질 commit 수 기준**으로 연속 번호 범위를 나눈다. 기존 문서
  파일 수만 보고 범위를 정하지 않는다.
- 검토자는 맡은 범위의 문서와 기준 source를 모두 직접 읽는다. 최종 오케스트레이터는 원장·결함과
  고위험 단위를 다시 읽고, 전체 범위가 실제로 검토됐는지 reconcile한다.
- 디스패치에는 절대 경로, 대상 ref/번호 범위, read-only, 두 정본, 반환 형식을 명시한다.

## 3. 저장소별 감사 gate

### 3.1 원장·분류·수량

`docs/commits/README.md`의 다음 mapping을 root부터 기준 ref까지 실제 graph와 대조한다.

```text
NNN ↔ hash ↔ parent ↔ subject ↔ phase ↔ 분류
    ↔ 답지 유무 ↔ 문제지 유무 또는 제외 사유
```

- 기준 ref에서 도달 가능한 in-scope commit이 번호형 답지 또는 명시적 제외 중 정확히 하나에 속하는지
  확인한다.
- empty marker, lockfile-only, 고유 resolution 없는 merge의 제외가 실제 diff와 맞는지 읽는다.
- 실질 source/config/test는 답지와 문제지, 핵심 schema는 답지와 얇은 문제지, pure docs·placeholder·
  publication은 답지만 둔 분류가 타당한지 확인한다.
- `A`/`B` 분할은 같은 hash의 범위 분할로 원장에 설명됐는지, 수량은 고유 commit 기준인지 확인한다.
- practice README가 모든 제공 번호와 모든 누락 번호의 개별 사유를 설명하는지 확인한다.

### 3.2 답지와 기준 tree

답지마다 metadata의 기준 hash와 parent를 실제 commit object에서 읽고, **그 commit의 tree**에서 변경
artifact를 직접 연다.

- H1 작업 단위 제목, 기준/parent hash, 변경 범위가 원장과 일치한다.
- `## 개요`, `## 작업 순서`가 있고 parent 한계와 구현 의존 순서를 설명한다.
- 모든 번호형 H3에 `**책임:**`이 있으며 실제 논리 단위와 대응한다.
- source는 signature만 나열하지 않고 핵심 body·control flow·error path를 보여 준다.
- config는 핵심 value/directive, test는 input/assertion, UI는 interaction·responsive·accessibility 계약,
  문서는 실제 사용/release 계약을 보여 준다.
- 설명한 identifier·값·동작이 기준 tree에 존재하고 이후 commit의 동작을 소급하지 않는다.
- `## 검증 계약`, `## 실제 실행 결과`, L3/L2/L1이 분리돼 있다.
- `## diff 반영 점검`이 추가·수정·삭제·rename·binary·generated path를 모두 reconcile한다.

현재 HEAD source 전체와 코드블록 식별자 합집합을 비교해 과거 답지를 판정하지 않는다. 같은 이름이
현재 남아 있다는 사실은 과거 commit 근거가 아니며, 이후 삭제됐다는 사실도 과거 답지의 환각 증거가 아니다.

### 3.3 문제지와 답지 드리프트

각 문제지는 연결된 답지와 나란히 직접 읽는다.

- canonical 배너가 정확히 “답지에서 수작업으로 파생한 문제지. 직접 수정하지 않는다.”라고 선언한다.
- H1, commit metadata, `## 개요`, `## 작업 순서`, 모든 번호형 H3와 `**책임:**`이 답지와 일치한다.
- 공개 signature·schema/API 구조와 `## 검증 계약`은 유지한다.
- 구현 body·control flow·핵심 config 값·constraint·test input/assertion은 책임 TODO로 비어 있다.
- TODO는 무엇과 성공 조건을 주되 구현 절차나 정답을 산문으로 누설하지 않는다.
- `## 실제 실행 결과`, 설계 회고, L3/L2/L1, diff 점검이 남아 있지 않다.

H3 제목 일치 같은 기계 비교는 보조일 뿐이다. H1·개요·작업 순서·책임·공개 계약·검증 계약의 의미
드리프트를 직접 정독한다.

### 3.4 실제 검증

- 답지에 적힌 모든 검증 명령을 해당 기준 commit의 isolated worktree/checkout에서 실행한다.
- 그 commit의 lockfile과 toolchain을 우선하고, 현재 HEAD dependency를 섞지 않는다.
- 0-test, no-op, 존재하지 않는 target을 성공으로 세지 않는다. 명령이 주장한 test/build/behavior가
  실제로 실행됐는지 관찰한다.
- 결과는 `green`, `ENV-LIMIT`, `예상된 역사적 실패`, `source FAIL`로 구분하고 정확한 명령과 error를
  기록한다.
- source FAIL이면 문서 결함과 별도로 release 확정이 잘못됐음을 보고한다. 감사 중 source를 고치지 않는다.

### 3.5 raw commit metadata와 message

대상 release의 in-scope commit object를 직접 읽어 다음을 확인한다.

- author name/email과 committer name/email이 canonical 단독 identity로 완전히 같다.
- `%aI == %cI`; 초와 UTC offset까지 같고 KST `+09:00`, 허용 근무시간, timestamp 중복 없음.
- subject와 `[근거]/[변경]/[검증]` 본문이 commit 성격에 맞고 trivial 면제만 본문이 없다.
- `Co-authored-by`, AI 도구, 다른 contributor trailer가 없다.
- 일반 phase는 implementation block 뒤에 문서 block이 오고 후속 source 변경은 새 phase로 append됐다.

`.mailmap`이나 formatted log의 표시상 통합만으로 PASS하지 않는다. raw author/committer header를 본다.

### 3.6 release-boundary topology

`commit-policy.md`가 정의한 release-boundary 저장소에만 적용한다.

- `main == annotated release tag`, `main^ == annotated template-vN`이다.
- template tagger와 release tagger가 canonical identity, KST의 고유 timestamp를 가진다.
- publication commit은 비어 있지 않은 `feat(content)` 하나이며 repo별 content allowlist path만 바꾼다.
- README·schema·renderer·test와 저장소가 선언한 denylist path가 publication diff에 없다.
- template tag는 중립 profile/project를 갖고 독립 build/test가 가능하다.
- `learning/<release>`는 release에서 시작해 정확히 `docs(commits)`와 `docs(practice)` 두 commit만
  가지며 각각 자기 허용 디렉터리만 변경하고 main에 merge되지 않았다.
- 이전 public tag와 learning branch는 이동·삭제되지 않았고 후속 release는 새 tag/ref를 사용한다.

### 3.7 링크·렌더·범위

- 두 README, 답지와 문제지의 상대 link가 실제 대상에 연결된다.
- H1과 heading 계층, code fence, 표가 Markdown에서 깨지지 않는다.
- dual-form commit이 허용 경로 밖의 source나 사용자 변경을 포함하지 않는다.
- 이상 제어문자나 unresolved TODO가 답지에 없고, 문제지 TODO는 의도된 책임 단위만 남는다.

## 4. 판정

- **PASS:** 모든 필수 gate를 충족하고 실행 검증이 green이다.
- **ENV-LIMIT:** 문서·source·metadata·topology는 맞지만 외부 서비스나 재현 불가능 toolchain 때문에
  일부 실행만 제한됐다. 정확한 근거가 있어야 한다.
- **FAIL:** source/tree 불일치, 누락 commit/path, 잘못된 분류, 문제지 누설, raw metadata 위반,
  topology/allowlist 위반, 실제 test/build 실패가 확인됐다.
- **확인필요:** dirty state나 접근 제한 등으로 근거를 확보하지 못해 판정할 수 없다.

환경 한계를 FAIL로 과장하지 않고, 실제 source나 release 결함을 ENV-LIMIT로 축소하지 않는다.

## 5. 검토자 반환 형식

```text
<repo>: PASS | FAIL | ENV-LIMIT | 확인필요
  기준: <release/ref, 답지 NNN 범위>
  원장: <포함 commit / 제외 commit / 수량 reconciliation>
  답지: <기준 tree 대조 결과와 누락>
  문제지: <drift·TODO 누설·생략 사유>
  실행: <명령 → green/ENV-LIMIT/역사적 실패/source FAIL>
  metadata: <raw identity/timestamp/message/trailer>
  release: <일반 phase 또는 template/release/learning/allowlist 결과>
  발견: <없음 또는 file·NNN·hash·근거>
```

FAIL·확인필요는 재현 가능한 hash, 문서 path, heading 또는 명령을 적는다. “대체로 양호”처럼 다시
확인할 수 없는 요약으로 끝내지 않는다.

## 6. 오케스트레이터 집계

- 실제 inventory의 모든 저장소를 `PASS / FAIL / ENV-LIMIT / 확인필요` 표로 reconcile한다.
- FAIL과 확인필요를 맨 위에 모아 repo·ref·NNN·근거·권장 다음 조치를 적는다.
- 검토자 반환만 믿지 않고 고위험 답지, source FAIL, release-boundary 저장소의 raw ref와 allowlist를
  오케스트레이터가 직접 다시 읽는다.
- 문서 수, 제외 수와 inventory 총계가 맞는지 확인하고 감사 중 변경·commit·push가 없었음을 보고한다.
- 수정이 필요하면 `QUALITY.md` 개선 런 또는 source release 재확정 작업으로 라우팅한다. 이 read-only
  세션에서 직접 고치지 않는다.
