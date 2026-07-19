# Commit·ref·push 정책

개발 저장소의 commit object, branch, tag, history rewrite와 원격 공개 규칙의 정본입니다. 작업 단계와
검증은 [`WORKFLOW.md`](WORKFLOW.md), 답지·문제지 내용은
[`docs-commit-note.md`](docs-commit-note.md)가 소유합니다.

새 세션과 handoff 인수자는 작업 전에 `document-box/main`의 exact SHA를 기록하고 이 문서 전체와
`WORKFLOW.md`, `docs-commit-note.md`, `legacy-exceptions.md`, 현재 registry·담당 트랙 문서를 다시
읽습니다. 일회성 Desktop handoff, 대화 요약과 이전 candidate의 설명은 이 정본을 대체하거나 예외를
추가하지 않습니다. 작업 중 policy SHA가 바뀌면 push 전에 old↔new policy diff를 읽고 candidate의
identity, timestamp, topology, provenance, approval 자료를 새 정본에 다시 대조합니다.

## 1. Canonical commit object

모든 새 commit과 annotated tag에 다음 raw identity를 사용합니다.

```text
seungwoo7050 <seungwoo7050@naver.com>
```

- author와 committer의 name/email을 모두 위 값으로 고정합니다.
- `%aI == %cI`: 초와 UTC offset까지 같은 timestamp를 사용합니다.
- Asia/Seoul `+09:00`, 09:00–21:59 KST와 고유한 분·초를 사용합니다.
- 같은 저장소의 parent timestamp는 child보다 늦을 수 없습니다.
- annotated tagger도 같은 identity와 해당 surface의 timestamp 규칙을 따릅니다.
- `.mailmap` 표시 통합은 준수가 아닙니다. raw object를 직접 검사합니다.
- `Co-authored-by`, `Generated-by`, AI 도구나 다른 contributor를 표시하는 trailer를 넣지 않습니다.

### Surface 경계

개발 저장소의 **source surface**는 다음 ref와 그 ref에서 도달 가능한 commit·tree 전체입니다.

- `main`과 구현 중인 local development branch
- release, template와 deployable tag의 이름, annotated tag object와 peeled graph
- 명시적으로 승인된 source preservation·diagnostic ref와 그 reachable graph

`learning/current`는 집필 surface입니다. `document-box`와 `central-notes`의 `main`은 governance·집필
surface입니다. 이 두 surface는 아래 source timestamp와 도구 식별자 금지 대상에서는 제외되지만,
canonical identity, trailer 금지와 commit message 품질 규칙은 그대로 적용합니다.

Source surface에는 작업 도구의 provenance를 남기지 않습니다. 대소문자를 구분하지 않고 `codex`,
`openai`, `chatgpt`, `claude`, `copilot`, `gemini`, `anthropic`, `cursor`와 같은 식별자를 다음 위치에서
금지합니다.

- branch·tag·preservation·diagnostic ref 이름
- annotated tag message와 tag metadata
- commit author/committer metadata, subject, body와 trailer
- tracked tool-control artifact의 path·파일명·본문: 도구별 instruction, agent 설정, editor rule,
  prompt와 session control 파일

실제 제품 기능, protocol 또는 fixture가 위 문자열을 필요로 하면 `document-box` 승인 원장에 저장소,
정확한 path와 token, 제품상 이유, 검토 근거를 좁게 등록한 allowlist만 인정합니다. Allowlist는 제품
source·test의 명시 path에만 적용하며 ref/tag 이름, commit metadata·trailer 또는 작업 도구 설정을
정당화하지 않습니다. 등록되지 않은 일치는 실패입니다.

## 2. Timestamp와 curriculum source window

공식 개발 저장소의 `main`은 운영 일지가 아니라 트랙 순서에 맞춰 읽는 **curated source history**입니다.
따라서 source·config·build·test·reference implementation과 source를 운영하는 README/DESIGN commit은
[`legacy-exceptions.md`](legacy-exceptions.md)에 승인되고 registry 전환 시
`tracks/curriculum.json`에 복제되는 저장소별 `sourceWindow` 안에 배치합니다.

- Source commit과 그 release annotated tagger는 등록된 시작일과 종료일을 포함한 범위 안에 있어야
  합니다. Tagger는 peeled source tip보다 이르지 않아야 합니다.
- 저장소 내부 patch·의존 순서와 parent 순서를 먼저 지킵니다. Commit 개수를 채우기 위한 빈 변경이나
  기계적인 균등 분배를 만들지 않습니다.
- 서로 다른 프로젝트의 source window는 병렬 개발을 표현하기 위해 겹칠 수 있습니다. 겹침 자체는
  위반이 아닙니다.
- 등록 종료일 뒤 source 변경이 필요하면 기존 window 안의 올바른 역사적 책임 위치에 통합합니다.
  `extensionEnd`는 원장에 명시된 세 신규 프로젝트만 사용할 수 있습니다. 다른 window 자체를 바꿔야
  하면 정확한 새 경계와 이유를 사용자에게 별도 승인받으며, 현재 시각 commit을 그대로 `main`에
  붙이거나 문서 commit으로 위장하지 않습니다.
- 학습자 내비게이션, 답지, 문제지, 개념 노트와 집필용 crosswalk는 source가 아닙니다. 개발 저장소에서는
  `learning/current`, 공통 설명과 정책 기록은 governance 저장소의 `main`에 실제 집필 시각으로 둡니다.
- `learning/current`, `document-box/main`, `central-notes/main`의 author/committer/tagger timestamp는
  실제 작성·publication 시각을 사용합니다. 역사적 source window로 backdate하지 않습니다.
- 전 트랙 정렬 migration에서는 기존 source patch 순서를 보존하되 timestamp를 등록 window로 다시
  배치합니다. Old timestamp는 사실 근거가 아니라 crosswalk의 비교값으로만 기록합니다.

## 3. Commit message

```text
<type>(<scope?>): <lowercase English imperative summary>

[근거] 왜 필요한가
[변경] 무엇을 바꿨나
[검증] 무엇을 실행하고 확인했나
```

허용 type은 `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `build`, `ci`, `perf`입니다. 실질 변경은
세 본문을 모두 쓰고, empty merge나 단순 관리 작업만 본문을 생략할 수 있습니다. Learning publication
scope는 `docs(notes)`, `docs(commits)`, `docs(practice)`입니다.

## 4. 장기 ref topology

### Governance 저장소

`document-box`와 `central-notes`의 local·원격 branch ref는 `main` 하나만 허용합니다. 정책·공통
개념·migration 원장은 실제 집필 시각 commit으로 `main`에서 직접 작성·발행합니다. Learning 또는
작업용 branch를 만들지 않습니다.

### 개발 저장소

공식 개발 저장소의 steady-state 원격 branch는 다음 두 개뿐입니다.

```text
main
learning/current
```

```text
historical source implementation / refactor / test / source docs
→ annotated release tag = main
                         \
                          learning/current
                          → optional docs(notes)
                          → docs(commits)
                          → docs(practice)
```

- `main`은 source, config, test, asset, 실행 가능한 reference implementation, exercise 계약과 source
  운영 문서만 가집니다.
- `learning/current`는 독자가 읽을 유일한 프로젝트 집필 branch입니다. release 이름, 날짜, 도구 이름,
  supplement 또는 fixup suffix를 붙인 다른 `learning/*` branch를 만들지 않습니다.
- 학습자는 Document Box 단계 카드가 가리키는 `learning/current/docs/README.md` 하나에서 시작합니다.
  어느 branch가 최신인지 날짜나 이름으로 추측하게 하지 않습니다.
- `learning/current`는 `main`에 merge하지 않습니다. Source release가 바뀌면 새 고정 basis에서 전체
  corpus의 hash·tree·patch·path·metadata·link를 기계적으로 재검증하고, 신규·변경·고유·충돌 본문만
  직접 검토한 뒤 승인된 publication으로 갱신합니다.
- `learning/current`의 non-fast-forward 갱신은 old/new tip·tree, 전체 file disposition, 신규·변경·고유·
  충돌 파일의 직접 검토, 복구 불가 고지와 destructive approval을 요구합니다. 동일 blob과 final source
  crosswalk가 증명된 본문은 재독하지 않습니다. Old tip을 branch, tag 또는 bundle로 보존하지 않고 exact
  expected-old lease로만 교체합니다.
- 과거 release의 source는 annotated tag가 고정합니다. 과거 집필 branch를 장기 archive로 유지하지
  않으며 active corpus 안에도 versioned duplicate나 archive subtree를 만들지 않습니다.
- 임시 `feature/*`, `fix/*`, `chore/*`는 local 작업에만 사용하고 publication 뒤 제거합니다. Agent·도구
  provenance를 이름에 넣지 않습니다.
- 공통 개념 bridge와 독립 평가는 `central-notes/main`이 소유합니다. 프로젝트 source나 corpus를
  Central에 복제하지 않습니다.

답지·문제지 path, stable ID와 수량 규칙은 `docs-commit-note.md`를 따릅니다.

## 5. Portfolio template/content topology

사용자가 profile, project, copy와 media를 바꿔 재배포할 수 있는 Portfolio도 branch topology는 위와
같습니다. Tag가 neutral template과 개인 publication을 구분합니다.

```text
neutral implementation / refactor / test
→ release docs
→ annotated template-vN
→ non-empty feat(content) publication
   = main = annotated portfolio-vN
                    \
                     learning/current
                     → docs(commits)
                     → docs(practice)
```

- `main^ == template-vN`, `main == portfolio-vN`이어야 합니다.
- publication commit은 저장소가 선언한 content allowlist만 변경합니다. README, schema, renderer,
  source와 test denylist를 건드리지 않습니다.
- template tag는 중립 content로 독립 lint/typecheck/unit/build/E2E/visual 검증을 통과해야 합니다.
- 다음 release는 이전 개인 publication이 아니라 최신 neutral template에서 시작합니다. 최신 개인
  content 전체를 새 publication commit으로 다시 적용합니다.
- 새 source와 content publication도 Portfolio에 등록된 source window 안에 있어야 합니다.

## 6. 전 트랙 source·learning 정렬 migration

2026-07에 승인된 migration은 기존 27개 프로젝트와 신규 3개 프로젝트를 최종 30개 curriculum으로
정렬하는 일회성 작업입니다. `legacy-exceptions.md`의 execution lane 배정은 서로 겹치지 않는 저장소의
로컬 감사·candidate·검증을 여러 세션에서 병행할 수 있게 합니다. 이 배정은 저장소 내부 직렬 gate,
source freeze 뒤 단일 집필자 원칙이나 전역 publication slot을 완화하지 않습니다. 저장소마다 다음
경계를 모두 지킵니다.

1. Remote refs와 expected-old SHA를 고정하고 정확한 source ref만 fetch한 bare snapshot, bundle,
   복원 clone과 SHA-256을 준비합니다. 이 bundle은 rollback용 임시 안전장치이며
   `refs/heads/learning/*`을 포함하지 않습니다.
2. `main` root부터 source patch 순서와 parent topology를 보존해 replay합니다. 등록 source window 안에서
   timestamp를 다시 배치하고 canonical identity, message와 provenance gate를 적용합니다.
3. 학습자 내비게이션만 바꾼 source commit은 `main`에서 제외합니다. 실제 source·test·build·reference
   변경은 책임 순서에 맞는 역사적 위치에 통합하고 같은 tree·patch 또는 명시된 기능 변경 근거를
   crosswalk합니다.
4. Source ref·tag·metadata·tracked path의 금지 provenance만 제거합니다. 제품 기능상 필요한 일치는
   사전 allowlist 없이는 유지하지 않습니다.
5. 기존 learning branch 중 어느 하나도 이름·날짜·tip만으로 자동 정본으로 선택하지 않습니다. 모든
   후보의 tip·tree·path·blob을 먼저 비교하고 동일 blob은 한 번만 판정합니다. 완전 포함관계면 final
   source와 호환되는 유효 상위 corpus를 기준본으로 삼고, divergent corpus는 source 호환성, commit
   coverage, link·metadata 정확성, 유효한 고유 내용 순으로 판정합니다. 전담 집필자는 신규·변경·고유·
   충돌 blob과 source crosswalk가 달라진 answer·practice만 직접 읽고 `learning/current`를 수작업으로
   보정합니다. 그 뒤 기존 `learning/*`를 모두 삭제합니다. 이 diff 중심 절차는 source ref·tag·metadata·
   trailer·tracked path/blob의 금지 provenance 0건 gate를 어떤 경우에도 완화하지 않습니다.
6. 삭제할 learning branch는 bundle, preservation tag 또는 active archive subtree에 보존하지 않습니다.
   Document Box 원장에는 old tip, path/blob, 채택·대체·폐기 판단과 reviewer만 남깁니다. 삭제는 원격
   garbage collection 뒤 복구할 수 없음을 approval에서 명시합니다.
7. 금지 provenance가 남은 old source graph는 원격 preservation tag로 공개하지 않습니다. Source-only
   rollback bundle은 push와 fresh-clone 검증이 끝난 뒤 삭제합니다.
8. Old/new commit, parent, tree, patch 또는 blob 근거, timestamp와 제거·통합 내용을 전수
   crosswalk합니다. Patch 순서를 바꾸거나 commit을 합치고 나누면 책임과 검증 근거를 별도로 적습니다.
9. 저장소별 source, 집필, publication과 fresh-clone gate를 끝낸 뒤 같은 lane의 다음 저장소로
   이동합니다. 다른 lane의 겹치지 않는 로컬 작업은 병행할 수 있지만 project와 governance의 원격
   mutation은 `WORKFLOW.md`의 전역 publication slot 아래 하나씩만 수행합니다.

각 저장소가 전환되기 전에는 기존 `tracks/curriculum.json`과 단계 카드가 가리키는 단 하나의 legacy
learning ref가 임시 독자 정본입니다. 독자에게 여러 branch 비교를 요구하지 않습니다. 저장소 cutover와
동시에 pointer를 `learning/current`로 바꾸며, 전환 전 pointer는 새 branch를 만들거나 old corpus를
보존할 권한이 아닙니다.

기존 legacy 표의 object 불변·learning byte 보존 문구는 이 승인 migration의 대상 ref에 한해
[`legacy-exceptions.md`](legacy-exceptions.md)의 상위 migration 절로 대체됩니다. 다른 저장소나 migration
완료 뒤 신규 object에는 이 예외를 재사용하지 않습니다.

## 7. Commit, 집필과 stage

- 검증을 통과한 뒤에만 commit합니다.
- 한 commit은 한 책임과 명시적 path allowlist를 가집니다.
- source, release 문서, notes, answers, practices를 서로 다른 commit에 둡니다.
- 전체 `git add -A`를 쓰지 않고 허용 경로만 명시적으로 stage합니다.
- Source hash가 바뀌면 corpus basis 갱신을 끝내기 전 release/learning을 공개하지 않습니다.
- Learning과 Central 집필은 source gate가 green이고 release basis가 고정된 뒤에만 시작합니다. Source
  개발과 본문 집필을 병행하지 않습니다.
- 저장소마다 개발자와 다른 전담 집필자 한 명만 둡니다. 집필자는 source를 수정하거나
  commit/tag/push하지 않습니다.
- 저장소 담당자가 신규 Central·learning 본문은 100% 직접 읽고, 기존 corpus 통합에서는 신규·변경·
  고유·충돌 본문을 한 번 직접 읽은 뒤 허용 path만 stage하여 publication commit을 만듭니다. 동일 blob과
  final source crosswalk가 증명된 기존 본문은 file disposition과 기계 gate로 검증합니다.

## 8. Destructive approval과 push gate

Force-push, `learning/current` non-FF 갱신, tag 이동·삭제와 branch 삭제 전에는 저장소별로 다음 실제
값을 다시 제시하고 명시적 승인을 받습니다.

여러 execution lane이 동작 중이면 승인은 publication slot을 대신하지 않습니다. 승인 뒤 slot을 획득한
세션만 remote ref와 governance `main` expected-old를 다시 읽고 push할 수 있습니다. Slot 획득 뒤 drift가
발견되면 원격을 변경하지 않고 slot을 해제한 뒤 새 exact 값으로 다시 승인받습니다. `document-box`와
`central-notes`는 최신 `main` 위에 담당 lane의 허용 변경만 actual-time commit으로 적용하며 다른 lane의
변경을 rebase·reset·force-push로 제거하지 않습니다.

```text
repository / remote
old main / expected-old SHA / new main
old source tag object·peeled SHA / new tag object·peeled SHA / 삭제 tag
old learning refs·tips·trees / new learning/current tip·tree
corpus path·blob disposition / review mode / reviewer
source-only rollback bundle / SHA-256 / restore 결과
삭제 뒤 learning corpus가 복구 불가능해질 수 있다는 고지
```

Push 직전에는 모든 remote head와 tag를 다시 읽고 다음을 모두 확인합니다.

- remote main이 expected-old SHA와 일치하는가
- governance 저장소는 `main`만, 개발 저장소는 `main`과 `learning/current`만 남는가
- source commit/tag timestamp가 등록 window 안이고 learning/governance commit은 실제 시각인가
- raw author/committer/tagger, message와 trailer가 맞는가
- source ref/tag 이름, annotated message, reachable metadata와 tracked artifact의 금지 provenance가
  0건인가
- main/tag/learning graph, corpus path, mapping·omission·수량과 commit별 allowlist가 맞는가
- source-only bundle 복원과 isolated clean-clone 전체 검증이 green인가

Rewrite, non-FF 갱신과 삭제는 plain `--force` 대신 변경하는 **모든 ref의** exact expected-old lease를
사용합니다.

```text
--force-with-lease=refs/heads/main:<expected-old-sha>
--force-with-lease=refs/heads/learning/current:<expected-old-tip>
--force-with-lease=refs/heads/<deleted-learning>:<expected-old-tip>
--force-with-lease=refs/tags/<moved-or-deleted-tag>:<expected-old-tag-object>
```

신규 ref는 push 직전 부재를 다시 확인하고 expected-absence lease를 사용합니다. Main, release tag,
`learning/current` 전환과 old branch/tag 삭제는 가능한 범위에서 하나의 atomic push로 수행합니다. 어느
ref라도 drift했거나 서버가 atomic update를 거부하면 전체를 중단합니다.

## 9. 공개 후 검증과 정리

1. `ls-remote`로 branch, tag object와 peeled SHA를 다시 읽습니다.
2. Fresh clone에서 source window, provenance, graph, corpus path와 저장소의 전체 검증을 실행합니다.
3. Document Box와 Central Notes가 `main` 하나만, 각 프로젝트가 `main`과 `learning/current` 하나씩만
   공개하는지 확인합니다.
4. Navigation이 release와 `learning/current/docs/README.md`를 가리키고 dead link가 없는지 확인합니다.
5. 검증이 green이면 source-only rollback bundle을 삭제하고 disposition ledger에 결과를 기록합니다.

검증 실패, remote drift 또는 고유 로컬 변경이 있으면 정리하지 않고 정확한 ref와 결함을 보고합니다.
