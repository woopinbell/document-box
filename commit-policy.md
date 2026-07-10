# 커밋 정책 (commit-policy)

`~/Desktop/seungwoo` 하위 모든 레포의 커밋·푸시 규칙 **정본**이다. CLAUDE.md의 커밋 절은 이
문서를 참조하고, 각 레포의 검증 스크립트는 baseline 용도로만 본다. 여러 레포에 걸치므로
`document-box`에 둔다.

> **복합 작업 필수 정본:** 이 문서는 commit object·날짜·ref topology·push를 결정한다.
> `docs/commits/**`와 `docs/practice/**`를 새로 만들거나 보강할 때는 반드시
> [`docs-commit-note.md`](docs-commit-note.md)도 함께 읽는다. 이력 재작성과 from-zero dual-form을
> 함께 수행할 때의 순서는 **이 문서로 topology·metadata 확정 → source hash/tag 고정 →
> docs-commit-note로 답지·문제지 집필 → 이 문서의 commit/push gate**다.

## 메시지 형식

```
<type>(<scope?>): <english imperative summary>

[근거] 왜 이 변경이 필요한가
[변경] 무엇을 바꿨나
[검증] 어떻게 통과를 확인했나
```

- **제목**: 소문자 영어 명령형. `<type>` ∈ `feat` / `fix` / `docs` / `test` / `refactor` /
  `chore` / `build` / `ci` / `perf`.
- **scope**: 선택(Conventional 표준). 의미 있는 모듈이 있으면 쓰고 레포 내 일관을 유지한다.
  dual-form 문서 커밋은 `docs(commits)`(답지) / `docs(practice)`(문제지).
- **본문 `[근거]/[변경]/[검증]`**: 실질 커밋(기능·구현·문서 저작/파생 등)엔 **필수**.
  trivial 커밋(`chore` 잡일·merge·lockfile 갱신)은 **면제**.
- **AI 공동저자 트레일러 금지** — 본인 단독 저작 history 유지.

## identity와 날짜

이 repo들은 학습 여정을 시간순으로 보여주는 **의도된 synthetic 타임라인**이다(history는
`git filter-repo`로 구성됨). 커밋 날짜는 그 타임라인이 자연스럽게 보이도록 **설정·교정한다.**

규율(모든 커밋 공통):

- **단독 contributor의 raw identity를 고정한다.** author name과 committer name은 모두
  `seungwoo7050`, author email과 committer email은 모두 `seungwoo7050@naver.com`이다.
  `Co-authored-by`를 비롯해 다른 사람·이메일을 contributor로 기록하는 trailer는 금지한다.
- **author timestamp == committer timestamp.** 날짜만 같은 것으로는 부족하다. 시·분·초와
  UTC offset까지 완전히 같아야 하며, ISO 출력 기준으로 반드시 `%aI == %cI`여야 한다.
- 타임존 **Asia/Seoul (KST, UTC+9).**
- **근무시간대(09:00–21:59 KST)** 에 둔다 — 21시대 포함, 22~08시대가 위반(2026-06-11 잔여 정비
  런에서 코퍼스 선례 기준으로 확정한 해석의 명문화).
- **분·초 랜덤** — 기계적인 `HH:00:00`(정각) 타임스탬프를 피해 분·초를 랜덤하게 정한다.
- **타임스탬프 중복 금지.**
- `.mailmap`처럼 표시 결과만 합치는 방법은 준수로 인정하지 않는다. commit object의 author와
  committer header가 위 identity·timestamp 규칙을 직접 만족해야 한다.
- annotated tag의 tagger도 `seungwoo7050 <seungwoo7050@naver.com>`과 KST 근무시간대의
  고유 timestamp를 사용한다.

## 일반 phase 배치

- 구현/feature 커밋 → 그 프로젝트의 학습 시기 window 안에 시간순으로.
- 메타·dual-form 커밋 → 최근 작업 시점 부근에 두되 위 규율(근무시간·중복금지)을 지킨다.
- **경계 분리(phase 단위)**: 경계 분리는 **phase 단위로** 적용한다. 한 phase = **구현 블록 →
  그 phase의 메타·문서 블록**이며, 두 블록을 시간적으로 인터리브하지 않는다(메타 커밋을 구현
  블록 사이에 끼워 넣지 않는다). **후속 작업(소스 결함 fix·수직 확장)은 새 phase로 연다** —
  phase N+1의 구현 블록은 phase N의 메타 블록 *뒤에* 시간순으로 이어진다(이전 window로
  backdating 하지 않는다).
- **phase의 답지 번호는 append**: 후속 phase의 답지는 직전 phase 마지막 번호에 이어 붙인다
  (사이의 메타 커밋은 종전처럼 색인에서 제외 — 결번 재배정 없음). 그 레포 `docs/commits/README.md`에
  **phase 경계(어디까지가 phase N인지)와 시작 커밋 해시를 명시**한다.

사용자가 교체할 publication surface가 없는 라이브러리·연습 레포는 이 선형 phase 모델을 따른다.
즉 `implementation/refactor/fix/test → release 문서 → docs(commits) → docs(practice)`를 phase 안에서
순서대로 두고, 다음 source 변경은 그 뒤에 새 phase로 append한다.

## 재사용형 공개 저장소의 release boundary

### 적용 판정과 용어

다음 조건을 모두 만족하는 공개 저장소는 **release-boundary 저장소**로 선언한다.

1. clone한 사용자가 profile·project·copy·media·example configuration 같은 소유자 영역을 바꿔
   자기 배포본으로 사용할 수 있다.
2. 그 영역을 repo별 **content allowlist**로 열거할 수 있고 README·schema·renderer·test처럼
   template가 소유할 파일을 **denylist**로 분리할 수 있다.
3. 개인 publication을 제거한 중립 tree가 독립적으로 build/test될 수 있다.

용어는 다음처럼 구분한다.

- **release 문서**: 사용자가 제품을 설치·수정·배포하는 데 필요한 README, architecture/API,
  customization, license. 중립 template의 일부이며 `main`에 남는다.
- **publication content**: 사용자가 자기 소유 정보로 교체하는 allowlist 경로의 profile, project,
  copy, media, baseline. 마지막 `feat(content)` commit 하나가 소유한다.
- **개발 재구성 문서**: 확정 commit과 source를 설명하는 `docs/commits/**` 답지.
- **학습 문서**: 답지에서 수작업 파생한 `docs/practice/**` 문제지.

### 필수 graph와 ref 불변식

```text
implementation / refactor / fix / test
→ release 문서
→ annotated template-vN
→ feat(content) publication commit = main = annotated release tag
                                      \
                                       learning/<release>
                                       → docs(commits) 답지 commit
                                       → docs(practice) 문제지 commit
```

- 중립 구현과 release 문서의 마지막 commit에 새 annotated `template-vN` tag를 붙인다.
- 그 바로 다음 commit은 **비어 있지 않은** `feat(content): ...` publication commit 하나다. repo가
  문서화한 content allowlist만 변경하고 denylist와 application code를 건드리지 않는다.
- deployable `main`과 새 annotated release tag는 같은 publication commit을 가리킨다.
  `main^`와 `template-vN`은 같은 중립 template commit을 가리켜야 한다.
- `learning/<release>`는 release tag에서 분기하며 release 위에 정확히 두 commit만 둔다. 첫째는
  `docs(commits): ...`로 `docs/commits/**`와 그 README만, 둘째는 `docs(practice): ...`로
  `docs/practice/**`와 그 README만 변경한다. 이 브랜치는 `main`에 merge하지 않는다.
- 한 learning branch에는 해당 release의 **전체 현행 corpus**를 싣는다. 이전 release에서 검증된
  문서는 같은 repo 안에서만 carry-forward할 수 있지만 기준 hash·tree·diff를 다시 직접 대조한다.
  새롭거나 의미가 달라진 답지는 새로 집필하고 대응 문제지를 다시 수작업 파생한다.
- release 문서와 dual-form 문서를 모두 `docs`라고 뭉뚱그리지 않는다. reset·배포에 필요한 문서는
  template tag 앞, 역사 재구성·연습 자료는 learning branch의 두 commit에 둔다.

### 후속 refactor·fix·확장

release-boundary 저장소는 선형 `main` ancestry보다 **중립 reset 계약**을 우선한다.

1. 이미 공개한 release tag, template tag와 `learning/<release>`는 이동·재작성·삭제하지 않는다.
2. 다음 phase는 이전 publication commit이 아니라 가장 최근 중립 `template-vN`에서 시작한다.
3. source/refactor/fix/test와 release 문서를 시간순으로 추가하고 새 `template-vN+1`을 만든다.
4. 최신 개인 콘텐츠 전체를 새 중립 parent 위에 다시 적용해 새 `feat(content)` commit을 만든다.
   빈 publication marker는 허용하지 않는다.
5. 새 release tag와 `learning/<new-release>`를 만들고, 갱신된 전체 답지·문제지 corpus를 다시 정확히
   두 commit으로 공개한다.
6. `main`은 새 release로 lease-protected rewrite한다. 이전 publication commit이 새 main의 1차
   ancestry에서 빠지는 것은 정상이며 immutable release tag와 learning branch가 그 이력을 보존한다.

이 방식으로 처리할 교체 가능 content surface가 없다면 release-boundary를 억지로 적용하지 않고
§일반 phase 배치를 사용한다.

**history 재작성이 정상 수단이다.** 날짜·메시지를 정책에 맞추려 rebase/amend/`git filter-repo`
\+ force-push 하는 것은 허용된다(개인 소유 repo). "재작성 금지"는 이 워크플로에 해당하지 않는다.

## 커밋·푸시 워크플로

- **검증을 통과한 뒤에만** 커밋한다(빌드/테스트 실제 실행 + 의미 리뷰). 부분 실패면 커밋 안 함.
- 일반 phase 저장소는 현재 브랜치(`main`)에 직접 커밋한다. release-boundary 저장소는 위 graph대로
  deployable `main`과 `learning/<release>`를 분리한다.
- **바뀐 파일만** 담는다(예: dual-form은 `git -C <repo> add docs/commits docs/practice`).
  전체 `-A` 금지 — 무관한 변경을 싸잡지 않는다.
- 변경 종류가 다르면 커밋 분리(답지 `docs(commits)` / 문제지 `docs(practice)` 따로).
- push 직전 `git log -1 --format='%an|%ae|%aI%n%cn|%ce|%cI'`를 직접 읽어 두 줄의
  이름·이메일·ISO timestamp가 완전히 같은지 확인한다. 다르면 amend한 뒤 다시 검증한다.
- 정상 append는 원격 old SHA가 그대로일 때 fast-forward push한다. 공개 이력 재작성 전에는 모든
  branch·tag·stash를 새 timestamped bundle로 백업하고 원격 ref별 SHA를 기록한다.
- main rewrite는 `--force`가 아니라 `--force-with-lease=refs/heads/main:<expected-old-sha>`를
  명시한다. 새 tag·learning branch의 부재 조건까지 확인하고 main/tag/learning을 하나의
  `--atomic` push로 갱신한다. 어느 ref라도 drift했거나 서버가 atomic update를 거부하면 전체를
  중단한다.
- tag는 annotated tag만 사용하며 §identity와 날짜의 tagger 규칙을 지킨다. 이미 공개한 tag를
  retarget하지 않고 새 version을 발행한다.
- force-push, tag 공개·삭제, 원격 branch 삭제처럼 외부 이력을 바꾸는 작업은 사용자의 명시적
  권한 범위 안에서만 수행한다. 권한이 없으면 로컬 검증까지 마친 뒤 승인 gate에서 멈춘다.
- push 후 `ls-remote`로 branch·peeled tag SHA를 다시 읽고 fresh clone에서 graph와 deployability를
  확인한다. 실패하면 완료로 보고하지 않는다.
- 서브에이전트로 분할해도 **커밋·푸시는 레포 세션이 마지막에 한 번**.

### release-boundary 필수 검증

- `main == release tag`, `main^ == template tag`이고 learning branch의 merge-base가 release tag이며
  그 위 commit 수가 정확히 2인지 확인한다.
- publication `HEAD^..HEAD`의 모든 path가 content allowlist 안이고 README·schema·renderer·test
  denylist를 건드리지 않는지 확인한다.
- template tag와 main 양쪽에서 repo가 요구하는 lint/typecheck/unit/build/E2E와 visual/content
  검증을 실제 실행한다.
- 답지 commit은 `docs/commits/**`, 문제지 commit은 `docs/practice/**`만 변경하는지 확인한다.
- 모든 commit의 raw author/committer identity와 ISO timestamp, annotated tagger, message/trailer를
  직접 읽는다.
- source 결함을 dual-form 검토 중 발견하면 문서로 덮지 않는다. tag·문서 확정 전 단계로 돌아가
  source부터 수정한 뒤 hash와 전체 검증을 다시 확정한다.

## 기존 검증 스크립트와의 관계

`linux-admin`·`network-routing-notes`의 `scripts/check-commit-msg.sh`·`check-timeline.sh`는
**그 레포의 synthetic baseline 히스토리**를 검사하는 per-repo 검증기다(고정 커밋 수, 날짜 범위
2023-05, scope 강제 등). 이 문서의 going-forward 정책과 세부가 다르고, 메타·dual-form 커밋이
추가된 현재 HEAD는 이들을 통과하지 않을 수 있다. **baseline 검증 용도로만** 보고, going-forward
커밋은 이 문서를 따른다. (스크립트는 그 레포 commit 문서가 설명하는 학습 산출물이므로 임의로
편집하지 않는다.)

## 적용 범위

going-forward 커밋은 이 정책으로 작성한다. 이미 푸시된 커밋도 날짜·형식이 정책과 어긋나면
**재작성(force-push)으로 교정**할 수 있다(개인 repo, force-push 허용). 예: 현재 일부 메타·
dual-form 커밋이 새벽 시간대·동일 timestamp로 들어가 있어 근무시간·중복금지 규율에 맞게
정리할 대상이다.
