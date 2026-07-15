# 세 트랙 학습 시작

이 문서가 42·Frontend·Backend 전체 과정의 유일한 첫 학습 정본이다. 다른 index나 프로젝트
README에서 시작했더라도 여기로 돌아와 현재 카드를 찾는다.

```text
42의 11개 프로젝트
→ 42 통합 incident
├─ Frontend 4개 프로젝트 → transfer → Portfolio → production regression → 회상 → 완료
└─ Backend 12개 프로젝트 → distributed incident → 회상 → 완료
```

42는 두 확장 트랙의 필수 선행이다. 42 incident의 즉시 checkpoint를 통과하면 7일·30일 회상을
병행하면서 Frontend, Backend 또는 둘 다 시작할 수 있다. 두 확장 트랙은 서로 기다리지 않지만 각
트랙 내부 카드 순서는 바꾸지 않는다.

## 처음 한 번만 준비

1. 이 repository를 clone하고 원하는 트랙의 환경을 검사한다.

   ```sh
   make preflight TRACK=42
   # 42 incident 뒤 선택할 때:
   make preflight TRACK=frontend
   make preflight TRACK=backend
   ```

   `BLOCK`은 현재 단계를 시작하기 전에 해결한다. `WARN`은 뒤 프로젝트에서 필요한 도구이므로 해당
   카드까지 해결한다. preflight는 설치나 upgrade를 하지 않고 누락 도구와 setup 명령만 알려 준다.

2. [개인 진행 원장 템플릿](PROGRESS_TEMPLATE.md)을 이 저장소 밖의 개인 경로에 복사한다. 프로젝트마다
   별도 파일을 만들거나 `단계 실행` section을 복제하고, baseline, practice ID, 첫 실패, 가설·반증,
   answer를 처음 연 시각, 무자료 재구현, 최종 gate와 회상 날짜를 남긴다.

3. GitHub CLI가 private project를 읽는지 확인한다. `make preflight`의 GitHub 항목이 `BLOCK`이면
   `gh auth login` 뒤 다시 검사한다. Plain `git clone`용 credential helper가 필요하면
   `gh auth setup-git`을 한 번 실행한다. 아래 절차의 `gh repo clone`은 현재 gh 인증을 직접 사용한다.

## 한 프로젝트를 학습하는 정확한 순서

각 단계 카드는 아래 절차에 필요한 실제 release/ref/path와 검증 명령을 제공한다.

1. **이전 gate 확인** — 이전 카드의 최종 gate와 원장 artifact가 없으면 돌아간다.
2. **Central 선수 노트** — 카드의 정확한 문서 anchor만 읽고 프로젝트를 대신 구현하지 않는다.
3. **release baseline** — repository를 clone하고 annotated release를 분리 checkout한다.

   ```sh
   gh repo clone woopinbell/<repo>
   cd <repo>
   git fetch --tags origin
   git switch --detach <release>
   # 카드에 적힌 baseline 명령 실행
   ```

4. **practice-first** — 카드의 current practice README에서 문제를 고른다. Git publication은
   `notes → answers → practices`지만 실제 학습 소비는 다음 순서다.

   ```text
   Central/notes → practice → 직접 실행·실패 → answer → 무자료 재구현
   ```

   `learning/<release>`는 읽기 전용이다. checkout해 수정하거나 `main`에 merge하지 않는다.

5. **개인 구현** — release tag는 baseline에만 사용한다. 선택한 practice 상단의 `부모 commit`을
   정확히 복사해 그 parent에서 개인 branch를 만든다. 그래야 아직 정답 diff가 없는 상태에서 실패와
   구현을 재현할 수 있다.

   ```sh
   PRACTICE_PARENT=<practice에 적힌 full parent hash>
   git switch -c study/<project>-<practice-id> "$PRACTICE_PARENT"
   ```

   Root commit을 재구현하는 practice처럼 부모가 없다고 명시된 경우에만 별도 빈 디렉터리 또는
   `git switch --orphan study/<project>-<practice-id>`를 사용한다.

   최소 한 번의 실제 실패와 자기 원인 가설·반증·검증 결과를 원장에 남긴다. 실패를 일부러 꾸미거나
   source/test 계약을 바꾸지 않는다.

6. **answer barrier** — 자기 시도와 실패 근거가 생기기 전에는 answer 링크를 열지 않는다. 이후
   answer의 basis commit/tree/diff를 자기 branch와 비교하고, 복사 대신 잘못된 결정만 교정한다.

7. **무자료 재구현** — answer와 기존 구현을 닫고 같은 practice parent에서 새 branch를 만들어 같은
   범위를 다시 구현한다. 카드의 전체 gate를 통과하고 핵심 경계를 말로 설명할 수 있어야 완료다.

8. **다음 링크** — 카드의 완료 artifact를 원장에 기록한 뒤 그 카드의 `다음` 링크만 따른다.

### Basis 안내의 우선순위

일부 이미 공개된 immutable project navigation wrapper에는 `tag에서 study branch`라는 축약 문구가
남아 있다. 그 문구는 release baseline checkout에만 적용하며 commit 재구현의 시작점을 뜻하지 않는다.
현재 학습에서는 이 문서와 각 practice 파일의 full `부모 commit` 지시가 우선한다. 공개된 tag와
learning ref는 이 문구를 고치기 위해 이동하거나 rewrite하지 않는다. Portfolio의 통합 content
publication 과제만 카드가 지정한 neutral template tag에서 시작하고, 개별 commit practice는 동일하게
각 파일의 parent를 따른다.

## 중단과 재개

중단할 때 원장에 repository, release, `study/*` branch, practice ID, 마지막 통과/실패 명령과 다음 한
단계를 기록한다. 코드는 개인 study branch에 commit할 수 있지만 public release나 learning ref를
움직이지 않는다. 재개할 때 이 문서 → 해당 트랙 → 현재 단계 anchor 순서로 열고, release ref가 카드와
같은지 `git fetch --tags` 후 확인한다. 카드가 바뀌었다면 `make check-remote-navigation`으로 현행 ref를
먼저 검증한다.

## 42 공통 선행

정확한 순서:

```text
linux-admin → format-printer → signal-message-bus → thread-dining → small-shell
→ stack-sort → stl-container → irc-relay-server → container-stack
→ web-boundary-inspector → pong-pong → 42 incident
```

[첫 카드: linux-admin](42.md#stage-linux-admin)

42 incident의 즉시 checkpoint 뒤 아래 둘 중 하나 또는 둘 다 선택한다.

- [Frontend 첫 카드](frontend.md#stage-frontend-foundations-training)
- [Backend 첫 카드](backend.md#stage-backend-foundations-training)

42의 30일 회상까지 통과해야 42 curriculum mastery를 확정한다. 확장 트랙을 먼저 시작해도 이 clock을
삭제하거나 다시 시작하지 않는다.

## 분기와 완료

### Frontend

```text
Foundations → Delivery → Cloud → Reliability → unfamiliar-API transfer
→ Portfolio → Web production regression → 두 회상 clock의 30일 checkpoint → 완료
```

[Frontend 현재 카드 찾기](frontend.md)

### Backend

```text
Foundations → Delivery → Reliability
→ Shared → Wallet → Risk → Odds → Betting → Settlement → Gateway → Admin → Orchestration
→ distributed incident → 30일 checkpoint → 완료
```

[Backend 현재 카드 찾기](backend.md)

Frontend와 Backend를 병행하면 별도 진행 원장 또는 명확히 분리한 section을 사용한다. 한 트랙의
평가·회상 결과를 다른 트랙 완료 근거로 재사용하지 않는다.

## Release 완료와 학습 완료

- **Project release 완료**: 원격 `main`, annotated release tag, immutable `learning/<release>`와
  fresh-clone 검증이 게시된 상태다. 28개 공식 프로젝트는 이 상태다.
- **Project 학습 완료**: 한 학습자가 practice-first 시도, 실패 증거, answer 비교, 무자료 재구현과
  카드의 최종 gate를 통과한 상태다.
- **Curriculum mastery**: 트랙의 모든 project 학습 완료에 answerless 평가와 완료 직후·7일·30일
  회상까지 더한 상태다.

Risk의 correctness release는 학습 가능하지만 1,000 RPS `p99 < 30 ms`, errors=0, drops=0 성능
qualification은 RED이다. 이 제한을 숨기거나 production SLO 달성 근거로 바꾸어 쓰지 않는다.

## 자체 검증

이 사슬이 현재 원격과 맞는지 다음으로 확인한다.

```sh
make check-navigation
make check-remote-navigation
```

첫 명령은 28개 프로젝트, prev/next 대칭, 42 이후 분기, anchor와 dead end를 오프라인 검사한다. 두 번째
명령은 인증된 GitHub에서 각 `main`, annotated tag, learning publication 순서·path와 current
practice/answer를 고정 SHA로 검사한다. 이번 navigation patch를 발행한 24개 README의 정확한 카드
역링크도 검사한다. 계획상 ref를 유지한 Signal·Web Boundary·Cloud·Orchestration은 이 문서의 current
카드가 진입점을 소유하며 registry에 명시적인 source-unchanged 예외로 고정한다.
