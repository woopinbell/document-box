# Commit·ref·push 정책

개발 저장소의 commit object, branch, tag, history rewrite와 원격 공개 규칙의 정본입니다. 작업 단계와
검증은 [`WORKFLOW.md`](WORKFLOW.md), 답지·문제지 내용은
[`docs-commit-note.md`](docs-commit-note.md)가 소유합니다.

## 1. Canonical commit object

모든 새 commit과 annotated tag에 다음 raw identity를 사용합니다.

```text
seungwoo7050 <seungwoo7050@naver.com>
```

- author와 committer의 name/email을 모두 위 값으로 고정합니다.
- `%aI == %cI`: 초와 UTC offset까지 같은 timestamp를 사용합니다.
- Asia/Seoul `+09:00`, 09:00–21:59 KST, 고유한 분·초를 사용합니다.
- timestamp 중복과 기계적인 정각 배치를 피합니다.
- annotated tagger도 같은 identity, KST 근무시간과 고유 timestamp를 사용합니다.
- `.mailmap` 표시 통합은 준수가 아닙니다. raw object를 직접 검사합니다.
- `Co-authored-by`, AI 도구나 다른 contributor trailer를 넣지 않습니다.

## 2. Commit message

```text
<type>(<scope?>): <lowercase English imperative summary>

[근거] 왜 필요한가
[변경] 무엇을 바꿨나
[검증] 무엇을 실행하고 확인했나
```

허용 type은 `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `build`, `ci`, `perf`입니다.
실질 변경은 세 본문을 모두 쓰고, empty merge나 단순 관리 작업만 본문을 생략할 수 있습니다.
Dual-form publication scope는 `docs(commits)`와 `docs(practice)`, 선택적 노트는 `docs(notes)`입니다.

## 3. 장기 branch 모델

일반 개발 저장소의 장기 원격 ref는 deployable `main`과 release별 immutable
`learning/<release>`입니다. 평문 `learning` branch는 사용하지 않습니다.

```text
implementation / refactor / fix / test
→ source를 운영하는 README·DESIGN
→ annotated <release> tag = main
                              \
                               learning/<release>
                               → optional docs(notes)
                               → docs(commits)
                               → docs(practice)
```

- `main`은 source, config, test, asset, 실행 가능한 reference implementation, exercise 계약과 제품
  운영 문서만 가집니다.
- 개념 노트·회고가 있으면 learning의 첫 commit 하나에 둡니다. 없다면 생략합니다.
- 답지는 그 다음 commit, 문제지는 마지막 commit이며 서로의 허용 경로만 변경합니다.
- learning branch는 `main`에 merge하지 않습니다.
- 공개된 release tag와 learning branch는 이동·재작성·삭제하지 않습니다. 후속 release는 새 tag와
  새 `learning/<release>`를 만듭니다.
- 거버넌스 허브인 document-box와 central-notes는 `main` only이며 learning branch를 만들지 않습니다.

답지·문제지 path, stable ID와 수량 규칙은 `docs-commit-note.md`를 따릅니다.

## 4. 임시 branch

`feature/*`, `fix/*`, `chore/*`와 작업용 candidate branch는 구현 중에만 사용합니다.

- main 반영 여부를 patch/tree로 확인합니다.
- main에 없는 고유 변경의 가치와 보존 ref를 결정합니다.
- bundle과 필요한 annotated legacy tag를 검증한 뒤 원격 임시 branch를 삭제합니다.
- 삭제된 branch 이름을 장기 archive로 사용하지 않습니다. 복구 경계는 tag와 bundle이 소유합니다.

## 5. Portfolio template/content topology

사용자가 profile, project, copy와 media를 바꿔 재배포할 수 있는 Portfolio는 다음 topology를
강제합니다.

```text
neutral implementation / refactor / test
→ release docs
→ annotated template-vN
→ non-empty feat(content) publication
   = main = annotated portfolio-vN
                    \
                     learning/portfolio-vN
                     → docs(commits)
                     → docs(practice)
```

- `main^ == template-vN`, `main == portfolio-vN`이어야 합니다.
- publication commit은 저장소가 선언한 content allowlist만 변경합니다. README, schema, renderer,
  source와 test denylist를 건드리지 않습니다.
- template tag는 중립 content로 독립 lint/typecheck/unit/build/E2E/visual 검증을 통과해야 합니다.
- learning branch는 release tag에서 분기해 정확히 answers와 practices 두 commit만 둡니다.
- 다음 release는 이전 개인 publication이 아니라 최신 neutral template에서 시작합니다. 새 template를
  완성한 뒤 최신 개인 content 전체를 새 publication commit으로 다시 적용합니다.
- 기존 template/release tag와 learning branch는 immutable record로 남깁니다.

## 6. Tag와 history 보존

모든 tag는 annotated tag입니다.

- `<release>`: source-only release 또는 deployable publication을 고정
- `template-vN`: 재사용 가능한 neutral product tree를 고정
- `pre-<rewrite>`: rewrite 직전 old main을 고정
- 명명된 legacy tag: 삭제할 branch가 가진 고유 graph의 최소 복구 tip을 고정

공개 history rewrite 전에 다음을 모두 준비합니다.

1. 실제 remote branch/tag SHA와 expected-old main
2. `--mirror --no-hardlinks` snapshot과 remote archive namespace
3. all-refs bundle, `bundle verify`, 복원 clone과 SHA-256
4. reflog/dangling object 중 문서가 참조하는 필요한 basis의 archive ref
5. old main과 삭제 예정 branch의 reachability·patch/tree 비교

Bundle은 push와 fresh-clone 검증이 끝날 때까지 보존합니다. 이후 사용자가 원격을 유일한 장기
보존본으로 선택한 경우에만 삭제합니다.

## 7. Commit과 stage

- 검증을 통과한 뒤에만 commit합니다.
- 한 commit은 한 책임과 명시적 path allowlist를 가집니다.
- source, release 문서, notes, answers, practices를 서로 다른 commit에 둡니다.
- 전체 `git add -A`를 쓰지 않고 허용 경로만 명시적으로 stage합니다.
- 서브에이전트는 commit/tag/push하지 않습니다. 저장소 담당 세션이 최종 검토 뒤 한 번 수행합니다.
- source hash가 바뀌면 corpus basis 갱신을 끝내기 전 release/learning을 공개하지 않습니다.

## 8. Push gate

push 직전에 다음을 직접 읽습니다.

- remote main과 expected-old SHA가 일치하는가
- 새 tag와 learning branch가 아직 없는가
- raw author/committer/tagger, `%aI == %cI`, message와 trailer가 맞는가
- main/tag/learning graph와 commit별 path allowlist가 맞는가
- bundle 복원과 clean-clone 전체 검증이 green인가

정상 append는 fast-forward합니다. Rewrite는 plain `--force` 대신 다음 lease를 사용합니다.

```text
--force-with-lease=refs/heads/main:<expected-old-sha>
```

main, 새 release tag와 learning branch는 가능하면 하나의 `--atomic` push로 공개합니다. 어느 ref라도
drift했거나 서버가 atomic update를 거부하면 전체를 중단합니다. Force-push, tag 공개·삭제, 원격 branch
삭제, repository rename/delete는 사용자가 승인한 범위 안에서만 수행합니다.

## 9. 공개 후 검증과 정리

1. `ls-remote`로 branch, tag object와 peeled SHA를 다시 읽습니다.
2. fresh clone에서 graph, path 경계와 저장소의 전체 검증을 실행합니다.
3. 임시 원격 branch를 삭제하고 재조회합니다.
4. dirty/stash/local-only ref가 없고 원격이 장기 정본임을 확인한 뒤 로컬 clone·bundle·cache를
   `WORKFLOW.md` 절차로 정리합니다.

검증 실패, remote drift 또는 고유 로컬 변경이 있으면 삭제하지 않고 정확한 ref와 결함을 보고합니다.
