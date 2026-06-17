# document-box — 워크스페이스 거버넌스·학습 가이드 허브 (정본이 모이는 곳)

> **한 줄**: `~/Desktop/seungwoo` 학습 포트폴리오의 **정본 문서 허브**다. 여기엔 코드가 없다 — 여러
> 레포를 가로지르는 *지도·커리큘럼·룰·검수 절차*가 **한 곳에, 각 한 부씩** 있다. (이 레포 자체는 학습
> 레포가 아니므로 dual-form(답지/문제지) 대상이 아니다.)
>
> **처음이면**: 아래 〈처음이면 이 순서로〉 3걸음을 따라가면 된다. 면접 준비면 곧장
> [INTERVIEW.md](INTERVIEW.md), AI로 코퍼스를 **만들거나 검수**하면 〈작업·검수〉 표로.

## 처음이면 이 순서로 (2걸음)

```
① WORKSPACE.md   여기가 뭐고 어디서 시작 — 워크스페이스 전체 지도(허브 3·레포 구조·목적별 동선)
       ▼
② STUDY.md       학습은 이 한 문서로 끝 — 왜 → 한 레포 도는 법 → 분야별 → 전체 순서 → 캡스톤 → 완주·면접
```

**학습 정본은 [STUDY.md](STUDY.md) 하나다.** 전 분야의 학습법·순서·완주가 거기 다 있다(구
`SEQUENCE`·`LEARNING`·`mobile-track`은 STUDY에 흡수된 **동결 레거시** — 외부 §참조 호환용). 면접용
전 레포 L3 색인만 [INTERVIEW.md](INTERVIEW.md)를 부록으로 둔다.

## 문서 카탈로그 — 무엇을, 언제 읽나

### 학습·복기 (독자/학습자용)

| 문서 | 무엇 | 언제 |
|---|---|---|
| [`WORKSPACE.md`](WORKSPACE.md) | 워크스페이스 전체 사용법(지도·레포 구조·목적별 동선) | **첫 진입** · 길을 잃었을 때 |
| [`STUDY.md`](STUDY.md) ★정본 | **학습 단일 완본** — 왜·한 레포 도는 법(루프 Step 0~5)·레포 장르 6종·**분야별 가이드**·전체 순서(경로 A~F)·캡스톤·완주·12 주제축 | **학습은 이것만** |
| [`INTERVIEW.md`](INTERVIEW.md) | 전 레포 L3를 모은 백지 설명 세트(주제 12축 + 레포별 370항 색인) — STUDY의 면접 부록 | 면접 준비·복기 |
| [`SEQUENCE.md`](SEQUENCE.md) · [`LEARNING.md`](LEARNING.md) · [`mobile-track.md`](mobile-track.md) | 🔒 **동결 레거시** — STUDY에 흡수됨. 외부 §참조(8개 레포) 호환용 스냅샷이라 보존만 | (직접 읽지 말 것 — STUDY로) |
| [`parallel-track.md`](parallel-track.md) | 42 주도 + 백/프론트 병렬 실행 캘린더(SEQUENCE 경로 F의 짝) | 세 트랙 동시 진행 |

### 작업·검수 (작업 세션/검수 세션용)

| 문서 | 무엇 | 언제 |
|---|---|---|
| [`docs-commit-note.md`](docs-commit-note.md) | 공통 빌드·파생 룰(dual-form 작성·실체성 게이트·파생 규칙·금지) — 루트 `CLAUDE.md` 라우터의 본체 | 레포를 만들거나 문서를 보강할 때 |
| [`commit-policy.md`](commit-policy.md) | 커밋 메시지·날짜 규율 정본 | 커밋·푸시 전 |
| [`AUDIT.md`](AUDIT.md) | 읽기전용 재검수 절차(탐지·보고만) | 전수 검수 세션 |
| [`QUALITY.md`](QUALITY.md) | 품질 검토·개선 절차(탐지→수정→커밋, §9 인수 검토 포함) | 품질 개선 런·그 인수 검토 |
| [`corpus-router.md`](corpus-router.md) | 코퍼스 작업 라우터 — 작업 종류별 정본 색인(구 루트 `CLAUDE.md`) | 빌드/품질/검수 세션의 진입 |

## 이 허브의 운영 원칙

1. **정본은 한 곳.** 룰 본문은 여기 해당 문서에만 둔다. 루트 `CLAUDE.md`는 AI 세션용 **얇은 라우터**라
   본문을 갖지 않고 여기를 가리킨다. 다른 레포·문서에는 포인터만.
2. **새 룰은 해당 정본에 추가**한다 — README나 라우터에 늘어놓지 않는다.
3. **교차 레포 문서만** 여기 둔다. 한 레포에 속한 결정은 그 레포 `docs/`(ADR·commits)에.
4. 작업 진행 **원장·기획은 `plan-box/`** (비-git 허브) — 품질 런 원장 `quality-ledger.md`, 커리어 타겟
   `TARGET.md`, AI 트랙 기획(`SEQUENCE-ai.md` 등)이 거기 있다.
5. **출하·취업 실행은 `launch-box/`** (private git 허브) — 라이브 배포·OSS·취업 파이프라인(`SHIP.md`·
   `HIRE.md`·`ledger.md`). 현재 국면 라우팅은 루트 `CLAUDE.md`.
