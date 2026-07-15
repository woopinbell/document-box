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
| [`commit-policy.md`](commit-policy.md) | commit object, `main`/immutable learning, tag, history rewrite와 push |
| [`docs-commit-note.md`](docs-commit-note.md) | 답지 선집필, 문제지 수작업 파생, stable ID, mapping과 수량 reconciliation |
| [`legacy-exceptions.md`](legacy-exceptions.md) | 이미 공개된 pre-policy release의 불변 예외 범위와 후속 준수 경계 |
| [`tracks/README.md`](tracks/README.md) | 공통 기반에서 Frontend/Backend로 갈라지는 전체 과정 지도와 현재 상태 |
| [`tracks/42.md`](tracks/42.md) | 42 트랙 11개 프로젝트의 공식 순서와 완료 gate |
| [`tracks/backend.md`](tracks/backend.md) | Backend 3개 훈련 저장소와 Sportsbook 9개 하위 저장소의 공식 순서 |
| [`tracks/frontend.md`](tracks/frontend.md) | Frontend 4개 훈련 저장소와 5-design Portfolio의 공식 순서 |
| [`data/README.md`](data/README.md) | 날짜가 붙는 공고·시장 관측과 지원 증거처럼 변동하는 운영 데이터의 색인·갱신 규칙 |

이 README는 권한 지도와 색인만 담당합니다. 세부 규칙을 복제하지 않습니다.

## 학습 시작

[**42 → Frontend/Backend 전체 완주 시작**](tracks/README.md)

학습 경로, 환경 점검, 중단·재개, 개인 원장과 마지막 평가·회상까지 위 문서에서 끊김 없이
연결합니다. 다른 문서를 학습 첫 진입점으로 사용하지 않습니다.

## 거버넌스 작업

- source refactor, history rewrite, 검증 또는 정리 작업이면 `WORKFLOW.md`를 읽습니다.
- commit, tag, branch, push를 만들거나 바꾸면 `commit-policy.md`를 함께 읽습니다.
- 기존 공개 object가 현행 규칙과 다르면 rewrite하지 말고 `legacy-exceptions.md`에 등록된 범위인지
  확인합니다.
- `docs/commits/**` 또는 `docs/practice/**`를 만들거나 갱신하면 `docs-commit-note.md`도 반드시
  함께 읽습니다.
- 채용 데이터는 [`data/jobs/`](data/jobs/)의 최신 snapshot을 읽고 제출 직전에 원문을 확인합니다.

복합 작업 순서는 다음과 같습니다.

```text
WORKFLOW로 범위·baseline·A/B/C 확정
→ commit-policy로 topology·metadata·backup 확정
→ source 구현과 검증
→ source hash/release tag 고정
→ docs-commit-note로 answers 전부 집필
→ practices 수작업 파생
→ commit-policy의 lease·atomic push gate
→ fresh clone 검증 후 로컬 정리
```

## 권한과 충돌 처리

1. 실제 동작은 대상 저장소의 기준 commit tree와 테스트가 정본입니다.
2. 트랙 포함 여부와 순서는 `tracks/*.md`가 정본입니다.
3. 작업 단계와 중단 기준은 `WORKFLOW.md`가 정본입니다.
4. commit/ref/push는 `commit-policy.md`, dual-form 내용은 `docs-commit-note.md`가 각각 정본입니다.
5. 규칙끼리 충돌하면 더 구체적인 책임 문서를 따르고, source 사실과 충돌하면 문서를 고칩니다.

## 공통 저장소 모델

- 개발 저장소: deployable `main` + release별 immutable `learning/<release>`
- learning branch: 선택적 notes → answers → practices, `main`에 merge하지 않음
- 공개 재사용 제품: template tag → content publication → release tag/main → learning branch
- 거버넌스 허브: `main` only
- 임시 `feature/*`, `fix/*`, `chore/*`: 작업 중에만 존재하고 공개 검증 뒤 제거

현재 ref와 수량은 각 원격에서 직접 확인합니다. 이 허브에 변하기 쉬운 SHA·commit 수를 복제하지
않습니다.
