# corpus-router.md — 코퍼스 작업 라우터 (구 루트 CLAUDE.md)

> 코퍼스를 **만들고·검수·개선·커밋**하는 작업 세션용 라우터다(빌드/품질/감사/커밋 규율). 원래 루트
> `CLAUDE.md`였고, 루트가 출하·취업 국면 라우터로 바뀌면서 여기로 이동했다. 작업 종류를 보고
> 아래 정본을 읽어라(룰 추가·수정은 그 정본에 한다). 경로는 이 파일 기준(=`document-box/`) 상대.

## 작업 단위

- **독립 git 레포 하나**가 작업 단위다(`find . -maxdepth 3 -name .git -type d`의 부모).
- **예외(멀티레포 폴더)**: `sportsbook/`·`ai-capstone/`은 레포가 아니라 독립 레포들의 폴더 — 하위 각 레포가 단위(이런 캡스톤 폴더는 더 생길 수 있음 — 폴더명 박지 말고 `find` 결과를 따른다).
- **허브**: `document-box`(거버넌스 문서)·`plan-box`(기획 문서)·`launch-box`(출하·취업) — dual-form/작업 대상 아님.

## 작업 종류별 정본 (읽고 따르라)

| 하려는 일 | 읽을 문서 |
|---|---|
| dual-form 신규 집필·복구·보강 (문서 없음 포함) | `docs-commit-note.md` (= from-zero 집필·분류·파생·검증 정본) |
| 무엇을 / 어떤 순서로 · 각 프로젝트를 어떻게 도나 (분야·순서·루프) | `STUDY.md`(학습 정본). 구 `SEQUENCE`·`LEARNING`은 STUDY에 흡수된 **동결 레거시**(외부 §참조 호환용) |
| 일반 저장소 후속 refactor·fix·확장 | `commit-policy.md` §일반 phase 배치 → `docs-commit-note.md` §후속 phase와 history rewrite |
| **이력 재작성 + from-zero dual-form** | `commit-policy.md`로 topology·metadata 확정 → hash/tag 고정 → `docs-commit-note.md`로 집필·검증 → `commit-policy.md` push gate |
| 커밋·날짜·release ref·push 규율 | `commit-policy.md` |
| **재검수** — 일반 dual-form (읽기전용 탐지·보고) | `AUDIT.md` |
| **품질 개선 런** (읽기-쓰기: 탐지→수정→커밋·푸시) | `QUALITY.md` §1–§8 |
| **품질 런 인수 검토** (read-only: 클레임·원장·표본 검증, 안 고침) | `QUALITY.md` §9 |
| 모바일 트랙 설계 | `STUDY.md` Part 4(모바일)·Part 6(캡스톤 API). 구 `mobile-track.md`는 **동결 레거시**(빌드 세션 절차는 그 §6) |

표의 행은 서로 배타적인 선택지가 아니다. 한 요청이 이력 재작성·source 변경·dual-form 집필·원격
교체를 함께 포함하면 해당 행의 정본을 **모두 누적 적용**하고, 복합 경로에 적힌 순서를 지킨다.

## 공통 불변

- 독립 레포는 **자기 커밋 히스토리와 연동된 `docs/commits/`** 를 가져야 한다(없거나 비면 위반).
- **추측·환각 금지** — 근거(`git show`/실소스)를 못 찾으면 멈추고 보고.
- 커밋: 영어 명령형 제목 + 한국어 `[근거]/[변경]/[검증]`, **AI 트레일러 없음**, 근무시간 09:00–21:59 KST(상세 `commit-policy.md`).
- **코퍼스 학습 범위는 포화 상태다.** 독립 신규 학습 주제를 추가하지 않는다. 다만 기존 저장소에
  `docs/commits/**`·`docs/practice/**`가 없거나 기준 source와 어긋난 경우의 복구는 신규 주제 추가가
  아니라 필수 거버넌스 수선이므로 수행한다.

> 이 라우터는 의도적으로 얇다. 세부 룰·기준·절차는 위 정본에 있다 — 여기에 새 룰을 적지 말 것.
