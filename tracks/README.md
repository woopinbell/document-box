# 전체 트랙 지도

42의 CS·시스템·웹 공통 기반을 먼저 마친 뒤 Frontend와 Backend로 갈라지는 전체 학습 경로입니다.
프로젝트의 실제 source·검증 명령은 각 저장소가 소유하고, 공통 개념·bridge·독립 평가는
[central-notes](https://github.com/woopinbell/central-notes)가 소유합니다.

```text
42 공통 기반
├─ Frontend → Reliability → unfamiliar-API transfer → Portfolio → Web production regression
└─ Backend → Sportsbook → 통합 분산 시스템 평가(트랙 완성 후 확정)
```

## 어디서 시작하는가

1. 처음 시작한다면 [`42.md`](42.md)의 `linux-admin`부터 순서대로 진행합니다.
2. 각 프로젝트에서는 `main`의 source·계약·검증을 확인한 뒤 immutable
   `learning/<release>`를 학습 자료로 사용합니다.
3. 42 curriculum mastery를 마치면 [`frontend.md`](frontend.md)와
   [`backend.md`](backend.md) 중 하나를 선택합니다. 두 확장 트랙은 병렬로 진행할 수 있지만 각 트랙
   내부 순서는 유지합니다.
4. 토픽별 최초 노출·직접 구현·재사용·독립 평가 연결은
   [Central Notes capability matrix](https://github.com/woopinbell/central-notes/blob/main/CAPABILITY_MATRIX.md),
   전체 bridge 순서는
   [TRACK_SEQUENCE](https://github.com/woopinbell/central-notes/blob/main/TRACK_SEQUENCE.md)에서 확인합니다.

## 전체 순서

### 1. 42 공통 기반

```text
linux-admin → format-printer → signal-message-bus → thread-dining
→ small-shell → stack-sort → stl-container → irc-relay-server
→ container-stack → web-boundary-inspector → pong-pong
→ 42 incident assessment
```

`web-boundary-inspector`는 Central Notes의 Web Foundations 개념을 실제 request/proxy/browser 경계에서
검증하는 독립 release 프로젝트입니다. 중앙 개념 문서와 프로젝트 source·학습 corpus를 서로
복제하지 않습니다.

### 2. Frontend 확장

```text
frontend-foundations-training → frontend-delivery-training
→ frontend-reliability-training → unfamiliar-API transfer
→ portfolio-site → Web production regression
```

### 3. Backend 확장

```text
backend-foundations-training → backend-delivery-training
→ backend-reliability-training → sportsbook
```

Backend는 현재 작업 중입니다. 완료되지 않은 release나 red 통합 gate를 학습 완료로 계산하지 않으며,
Backend 전체가 green이 된 뒤 42·Frontend와의 최종 통합 평가를 설계합니다.

## Git publication과 학습 순서

Git에는 자료의 근거가 되는 source를 먼저 고정해야 하므로 다음 순서로 게시합니다.

```text
publication: source main → annotated release tag
             → optional notes → answers → practices on learning/<release>
```

학습자는 답을 먼저 읽지 않고 다음 순서로 소비합니다.

```text
learning: 공통 개념/notes → practice → 직접 실행·실패
          → answer와 basis diff 대조 → 무자료 재구현
```

상세 ref와 commit 규칙은 [`../commit-policy.md`](../commit-policy.md), 답지·문제지 규칙은
[`../docs-commit-note.md`](../docs-commit-note.md)를 따릅니다.

## 완료 상태의 의미

| 범위 | 현재 상태 | 의미 |
| --- | --- | --- |
| 42 | 프로젝트 release 완료 | 11개 프로젝트의 main/tag/learning과 fresh-clone gate 완료 |
| Frontend | 프로젝트 release 완료 | 세 훈련 저장소와 Portfolio release gate 완료 |
| Backend | 작업 중 | 일부 red gate가 남아 있어 트랙 완료와 통합 진단을 유예 |

**프로젝트 release 완료**는 원격 main, annotated tag, immutable learning branch와 fresh-clone 검증이
green인 상태입니다. **Curriculum mastery**는 여기에 답지 없는 전이·incident·운영 평가와 완료
직후·7일·30일 회상 checkpoint까지 통과한 상태입니다. 게시 완료만으로 개인의 숙달을 선언하지
않습니다.

현재 42와 Frontend는 바로 학습을 시작할 수 있습니다. Backend는 해당 트랙 문서의 green 범위만
사실로 사용하고, 전체 완료나 최종 통합 평가가 준비됐다고 간주하지 않습니다.
