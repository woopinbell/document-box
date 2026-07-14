# 전체 트랙 지도

42의 CS·시스템·웹 공통 기반을 먼저 마친 뒤 Frontend와 Backend로 갈라지는 전체 학습 경로입니다.
프로젝트의 실제 source·검증 명령은 각 저장소가 소유하고, 공통 개념·bridge·독립 평가는
[central-notes](https://github.com/woopinbell/central-notes)가 소유합니다.

```text
42 공통 기반
├─ Frontend → Delivery → Cloud → Reliability → unfamiliar-API transfer → Portfolio → Web production regression
└─ Backend → Sportsbook → backend distributed incident → 지연 회상
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
→ cloud-launch-training → frontend-reliability-training → unfamiliar-API transfer
→ portfolio-site → Web production regression
```

### 3. Backend 확장

```text
backend-foundations-training → backend-delivery-training
→ backend-reliability-training → sportsbook
```

Backend의 Training 3개와 Sportsbook 9개는 원격 release·learning ref와 fresh-clone gate가
green입니다. Orchestration strict cold E2E도 144 pass/0 fail로 끝났습니다. Risk는 correctness
release를 학습에 사용할 수 있지만 1,000 RPS 성능 qualification은 RED이므로 production SLO를
주장하지 않습니다. 게시 완료 뒤에도 답지 없는 incident 평가와 회상 checkpoint를 통과하기 전에는
curriculum mastery로 세지 않습니다.

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
| Frontend | 프로젝트 release 완료 | 네 훈련 저장소와 Portfolio, 공식 5개 release gate 완료 |
| Backend | 프로젝트 release 완료 | Training 3개와 Sportsbook 9/9의 main/tag/learning·fresh clone은 green. Risk 성능 qualification은 별도 RED |

**프로젝트 release 완료**는 원격 main, annotated tag, immutable learning branch와 fresh-clone 검증이
green인 상태입니다. **Curriculum mastery**는 여기에 답지 없는 전이·incident·운영 평가와 완료
직후·7일·30일 회상 checkpoint까지 통과한 상태입니다. 게시 완료만으로 개인의 숙달을 선언하지
않습니다.

현재 세 트랙의 공식 프로젝트는 42 11개, Frontend 5개, Backend 12개로 총 28개이며 모두 바로
학습을 시작할 수 있습니다. Backend의 Risk known-red 성능 근거는 실패를
분석하는 자료이지 SLO 인증이 아닙니다. 프로젝트 release 완료와 별개로 답지 없는 incident 평가와
지연 회상 전에는 curriculum mastery로 간주하지 않습니다.
