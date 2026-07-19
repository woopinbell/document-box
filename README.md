# document-box

여러 저장소에 공통으로 적용하는 **트랙 순서, 개발 작업 방식, Git/ref 규칙, commit 기반 학습
문서 규칙**의 정본입니다. 저장소별 source·API·검증 명령의 사실은 각 저장소의 현재 tree와 release
문서가 우선하고, document-box는 그 사실을 가로지르는 운영 규칙만 소유합니다.

document-box 자체와 `central-notes` 같은 거버넌스 저장소는 dual-form 대상이 아니며 `main`만
사용합니다.

## 정본 카탈로그

| 문서 | 단일 책임 |
| --- | --- |
| [`WORKFLOW.md`](WORKFLOW.md) | preflight부터 격리 작업, A/B/C 판정, 구현, 검증, 공개와 로컬 정리까지 |
| [`commit-policy.md`](commit-policy.md) | source window, `main`/`learning/current`, tag, history rewrite와 push |
| [`docs-commit-note.md`](docs-commit-note.md) | 답지 선집필, 문제지 수작업 파생, stable ID, mapping과 수량 reconciliation |
| [`legacy-exceptions.md`](legacy-exceptions.md) | pre-migration object evidence, 30개 source window와 전환 승인 경계 |
| [`tracks/README.md`](tracks/README.md) | 공통 기반에서 Frontend/Backend로 갈라지는 전체 과정 지도와 현재 상태 |
| [`tracks/42.md`](tracks/42.md) | Linux/Git Foundations와 42 트랙 13개 프로젝트의 공식 순서·완료 gate |
| [`tracks/backend.md`](tracks/backend.md) | Backend 3개 훈련 저장소와 Sportsbook 9개 하위 저장소의 공식 순서 |
| [`tracks/frontend.md`](tracks/frontend.md) | Frontend 4개 훈련 저장소와 5-design Portfolio의 공식 순서 |
| [`tracks/frontend-fast-track.md`](tracks/frontend-fast-track.md) | 42 복습자의 지원 준비를 위한 비정규 Frontend 브리지와 정규 사슬 복귀 gate |
| [`data/README.md`](data/README.md) | 날짜가 붙는 공고·시장 관측과 지원 증거처럼 변동하는 운영 데이터의 색인·갱신 규칙 |

이 README는 권한 지도와 색인만 담당합니다. 세부 규칙을 복제하지 않습니다.

## 학습 시작

[**42 → Frontend/Backend 전체 완주 시작**](tracks/README.md)

학습 경로, 환경 점검, 중단·재개, 개인 원장과 마지막 평가·회상까지 위 문서에서 끊김 없이
연결합니다. 다른 문서를 학습 첫 진입점으로 사용하지 않습니다.

42를 이미 직접 구현한 복습자를 위한 빠른 지원 준비 경로도 전체 완주 문서의 42 incident 분기에서
연결합니다. 별도 시작점이나 별도 Frontend 트랙은 만들지 않습니다.

## 거버넌스 작업

- source refactor, history rewrite, 검증 또는 정리 작업이면 `WORKFLOW.md`를 읽습니다.
- commit, tag, branch, push를 만들거나 바꾸면 `commit-policy.md`를 함께 읽습니다.
- 기존 공개 object가 현행 규칙과 다르면 `legacy-exceptions.md`의 migration 대상·expected-old·승인
  범위를 확인합니다.
- `docs/commits/**` 또는 `docs/practice/**`를 만들거나 갱신하면 `docs-commit-note.md`도 반드시
  함께 읽습니다.
- 채용 데이터는 [`data/jobs/`](data/jobs/)의 최신 snapshot을 읽고 제출 직전에 원문을 확인합니다.

신규 프로젝트의 복합 작업 순서는 다음과 같습니다.

```text
WORKFLOW로 범위·baseline·A/B/C 확정
→ commit-policy로 topology·metadata·source-only rollback 확정
→ source 구현과 검증
→ source hash/release tag 고정
→ 전담 집필자가 docs-commit-note로 answers 전부 수작업 집필
→ practices 수작업 파생
→ commit-policy의 lease·atomic push gate
→ fresh clone 검증 후 로컬 정리
```

기존 프로젝트의 승인된 정렬 migration은 source freeze 뒤 기존 learning 후보의 tip·tree·path·blob을
먼저 비교합니다. 동일 blob은 재독하지 않고 `oid-identical`, `metadata-only`, `direct-content`로
disposition한 뒤 영향 answer와 대응 practice만 전담 집필자가 보정합니다. Source surface의 AI
provenance 0건 gate와 저장소별 직렬 publication은 이 최적화의 영향을 받지 않습니다. Learning과
governance 본문은 AI 식별자 제거 대상이 아닙니다.

30개 정렬 migration은 42·신규 프로젝트 lane과 Frontend→Backend delegated lane으로 나눠 겹치지 않는
로컬 감사·candidate·검증을 병행할 수 있습니다. 각 lane 내부와 각 저장소의 source→집필→publication은
직렬이며, project ref와 `document-box`·`central-notes`를 바꾸는 모든 원격 작업은 전역 publication
slot 하나로 직렬화합니다. 세션 인계와 공유 registry 재적용 규칙은 [`WORKFLOW.md`](WORKFLOW.md)와
[`legacy-exceptions.md`](legacy-exceptions.md)를 따릅니다.

## 권한과 충돌 처리

1. 실제 동작은 대상 저장소의 기준 commit tree와 테스트가 정본입니다.
2. 트랙 포함 여부와 순서는 `tracks/*.md`가 정본입니다.
3. 작업 단계와 중단 기준은 `WORKFLOW.md`가 정본입니다.
4. commit/ref/push는 `commit-policy.md`, dual-form 내용은 `docs-commit-note.md`가 각각 정본입니다.
5. 규칙끼리 충돌하면 더 구체적인 책임 문서를 따르고, source 사실과 충돌하면 문서를 고칩니다.

## 공통 저장소 모델

- 개발 저장소: deployable `main` + 독자의 유일한 집필 진입점 `learning/current`
- learning branch: 선택적 notes → answers → practices, 실제 집필 시각, `main`에 merge하지 않음
- 공개 재사용 제품: template tag → content publication → release tag/main → `learning/current`
- 거버넌스 허브: local·remote 모두 `main` only
- 개발 저장소의 임시 `feature/*`, `fix/*`, `chore/*`: local 작업 중에만 존재하고 공개 검증 뒤 제거

현재 ref와 수량은 각 원격에서 직접 확인합니다. 이 허브에 변하기 쉬운 SHA·commit 수를 복제하지
않습니다.
