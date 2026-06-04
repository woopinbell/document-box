# 커밋 정책 (commit-policy)

`~/Desktop/seungwoo` 하위 모든 레포의 커밋·푸시 규칙 **정본**이다. CLAUDE.md의 커밋 절은 이
문서를 참조하고, 각 레포의 검증 스크립트는 baseline 용도로만 본다. 여러 레포에 걸치므로
`document-box`에 둔다.

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

## 날짜

이 repo들은 학습 여정을 시간순으로 보여주는 **의도된 synthetic 타임라인**이다(history는
`git filter-repo`로 구성됨). 커밋 날짜는 그 타임라인이 자연스럽게 보이도록 **설정·교정한다.**

규율(모든 커밋 공통):

- **author date == committer date.**
- 타임존 **Asia/Seoul (KST, UTC+9).**
- **근무시간대(대략 09–21시)** 에 둔다.
- **타임스탬프 중복 금지.**

배치:

- 구현/feature 커밋 → 그 프로젝트의 학습 시기 window 안에 시간순으로.
- 메타·dual-form 커밋 → 최근 작업 시점 부근에 두되 위 규율(근무시간·중복금지)을 지킨다.

**history 재작성이 정상 수단이다.** 날짜·메시지를 정책에 맞추려 rebase/amend/`git filter-repo`
\+ force-push 하는 것은 허용된다(개인 소유 repo). "재작성 금지"는 이 워크플로에 해당하지 않는다.

## 커밋·푸시 워크플로

- **검증을 통과한 뒤에만** 커밋한다(빌드/테스트 실제 실행 + 의미 리뷰). 부분 실패면 커밋 안 함.
- 현재 브랜치(`main`)에 **직접 커밋**. 별도 브랜치/PR 없음.
- **바뀐 파일만** 담는다(예: dual-form은 `git -C <repo> add docs/commits docs/practice`).
  전체 `-A` 금지 — 무관한 변경을 싸잡지 않는다.
- 변경 종류가 다르면 커밋 분리(답지 `docs(commits)` / 문제지 `docs(practice)` 따로).
- `git -C <repo> push`(upstream 설정됨). 실패하면(원격 없음·인증 등) 멈추고 보고한다.
- 서브에이전트로 분할해도 **커밋·푸시는 레포 세션이 마지막에 한 번**.

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
