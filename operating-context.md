<!-- 이관·보존 스냅샷 (2026-06-19). 구 워크스페이스 루트 라우터 `~/Desktop/seungwoo/CLAUDE.md`를
     document-box로 이관한 것이다. 루트의 비-git auto-load 라우터는 **제거**됨 — 워크스페이스 루트에는
     더 이상 auto-load 라우터가 없다. 활성 라우팅은 document-box 고유 라우터 `CLAUDE.md`가 맡고,
     이 파일은 구 루트 라우터의 보존본(현 국면·ops-lab 포인터 포함)이다. -->

# (이관·보존) seungwoo 워크스페이스 루트 라우터 — 구 `~/Desktop/seungwoo/CLAUDE.md`

`~/Desktop/seungwoo`는 학습-through-구현 독립 git 레포 코퍼스(~40+) + 허브 3개다. 워크스페이스
루트 자체는 git이 아니다. 이 파일은 **얇은 진입 라우터** — 룰 본문은 두지 않고 정본을 가리킨다.
(여기에 새 룰을 적지 말 것. 레포 목록도 박지 말 것 — `find . -maxdepth 3 -name .git`로 탐지.)

## 먼저 읽어라 (거버넌스 정본)

- **`document-box/CLAUDE.md`** — 워크스페이스 라우터(의도별 정본 색인). 작업 전 이걸 먼저 읽어라.
- 전체 지도 `document-box/WORKSPACE.md` · **학습 정본 `document-box/STUDY.md`**(전 분야·순서·완주 단일
  문서 — 구 `SEQUENCE`·`LEARNING`·`mobile-track`은 흡수된 동결 레거시).
  (병렬 진행 = 경로 F → `document-box/parallel-track.md`).

## 허브 3개

- `document-box/` (git) — 거버넌스·교차 문서·학습 가이드. **정본.**
- `plan-box/` (비-git) — 기획·원장(TARGET·SEQUENCE-ai·각종 ledger).
- `launch-box/` (**private git**) — 출하·취업·**운영 증명** 실행. 현 국면의 실행 트랙.

## 지금 국면 (2026-06~)

- **학습 코퍼스(~40 레포)는 포화** — 새 *학습* 레포는 만들지 않는다. 할 일 둘: ① 학습/체화 [메인]
  → `document-box/STUDY.md` · ② 갭 메우기(출하·취업·운영) [병렬] → `launch-box/`.
- **단, 실제 *제품* 빌드·운영은 going-forward 작업이다**(출하 증명 = 학습 콘텐츠 제작 아님). 실빌드
  제품 레포(예: `btc-cycle-signals`)는 synthetic 타임라인이 아니라 *실제 시점*으로 커밋하고, 자기
  `CLAUDE.md`를 진입점으로 둔다.

### 활성 이니셔티브 — 운영 증명 랩(ops-lab) ※당장 아님, 신호 대기

백엔드의 마지막·가장 내구성 있는 갭 = *실전 압력 아래 운영 판단*("한 번도 살아있던 적 없다" —
전 레포 회고가 운영 트래픽 없음·오프라인 검증을 고백). $0(자기 머신 + 무료 터널 / Oracle
Always-Free + 자가 부하 + 카오스 + 시간)으로 한 서비스를 라이브 운영하며 **비자명 장애를 진단·
일지화**한다. AI-내성 운영 판단의 증거.

- **계획 정본: `launch-box/ops-lab.md`.**
- 트리거: 사용자가 "ops-lab 시작"이라 신호하면 그 계획을 픽업해 단계별로 함께 진행
  (주도: Claude 설계·진단·문서화 / 사용자: 인프라 결정·배포 실행).
- 돈 가드레일: **$0 우선.** 유료 스케일·실사용자 마케팅 금지(그건 사업이지 운영 *증명*이 아니다).

## 공통 불변 (본문 정본은 document-box)

- **추측·환각 금지** — `git show`/실소스 근거 없으면 멈추고 보고.
- 커밋: 영어 명령형 제목 + 한국어 `[근거]/[변경]/[검증]`, AI 트레일러 없음, KST 근무시간
  (정본 `document-box/commit-policy.md`). sportsbook 레포는 ADR-0016대로 영어 본문.
- 바뀐 파일만 커밋(`-A` 금지). **레포 밖 상대링크 금지**(각 레포 독립 push → `../다른레포` 깨짐).
- 워크스페이스 루트·`plan-box`는 비-git → 그곳 파일은 커밋 대상이 아니다. `launch-box`는 **private git**이니 자기 레포에 커밋한다(단 출하 허브라 dual-form/문서 캠페인 대상은 아님 — document-box처럼 명시 제외).

> 라우터는 의도적으로 얇다. 세부 룰·기준·절차는 위 정본에 있다 — 여기에 새 룰을 적지 말 것.
