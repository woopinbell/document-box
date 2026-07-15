# 개인 학습 진행 원장

이 파일을 저장소 밖의 개인 공간에 복사해 사용합니다. `learning/<release>`는 읽기 전용으로 두고,
release tag는 baseline 확인에만 사용합니다. 실제 구현과 실패 기록은 선택한 practice 파일의 full 부모
commit에서 만든 개인 `study/*` branch에 남깁니다. 비밀번호, token, 개인 정보, 실제 서비스 credential은
기록하지 않습니다.

## 과정 선택

- 학습자:
- 시작일(KST):
- 현재 트랙: 42 / Frontend / Backend
- 현재 단계 카드:
- repository:
- annotated release:
- learning ref:
- registry 원격 검증 시각(KST):
- release peeled SHA:
- learning tip SHA:
- 개인 study branch:
- 이전 gate 통과 근거:

## 단계 실행

아래 section은 프로젝트마다 복제하거나 프로젝트별 별도 원장 파일로 저장합니다. 앞 프로젝트의
실패·answer 시각·gate를 다음 프로젝트 기록으로 덮어쓰지 않습니다.

### 1. 환경과 baseline

- 실행한 preflight 명령:
- `PASS` 항목:
- `WARN` 항목과 대응:
- `BLOCK` 해소 근거:
- release baseline 명령:
- baseline 결과와 시각:
- baseline stdout/stderr 또는 artifact 위치:

### 2. 선수 노트와 practice

- Central Notes 선수 문서:
- 자체 설명 또는 요약 artifact:
- 선택한 practice stable ID:
- practice에 적힌 full 부모 commit(부모 없는 root practice면 `ROOT`):
- practice README 확인 시각:
- answer를 열기 전에 세운 가설:

### 3. 실행·실패 증거

- 최초 실행 명령:
- 관찰한 실패:
- 재현 최소 조건:
- stdout/stderr, trace, screenshot 또는 test report 위치:
- 실패 원인 가설:
- 가설을 반증할 수 있는 관찰:
- 수정 또는 구현 단위:

### 4. answer 대조

- answer를 처음 연 시각(KST):
- 확인한 answer stable ID:
- 내 접근과 같았던 결정:
- 달랐던 결정과 근거:
- basis commit/tree/diff 대조 결과:
- answer를 그대로 복사하지 않고 다시 설명한 내용:

### 5. 무자료 재구현

- answer를 닫고 새로 만든 branch/working tree:
- 시작 시각:
- 종료 시각:
- 재구현 commit 또는 patch:
- 기억에 의존하지 못해 다시 조사한 항목:
- release와 public behavior 비교:

### 6. 최종 gate와 handoff

- 최종 검증 명령:
- 결과:
- 완료 artifact:
- 남은 known limitation:
- 다음 단계 카드:
- 다음 단계 시작 가능 여부: PASS / BLOCK

## 독립 평가

Frontend처럼 평가가 둘 이상이면 이 section을 평가마다 복제합니다.

- 평가 이름:
- starter/evidence pack 기준 commit:
- 답지를 보지 않고 시작한 시각:
- 제출 artifact:
- checker 명령과 결과:
- rubric 자기 평가:
- 보완 후 재평가 날짜:

## 무자료 회상

- 회상 clock 이름: 42 incident / Frontend transfer / Web production regression / Backend incident

아래 표는 clock마다 하나씩 복제합니다. 서로 다른 평가의 예정일을 한 표에 합치거나, 뒤 평가를
통과했다는 이유로 앞 clock을 다시 시작하지 않습니다.

| checkpoint | 예정일 | 실제 수행일 | 자료를 닫고 재현한 내용 | gate 결과 | 다음 조치 |
| --- | --- | --- | --- | --- | --- |
| 완료 직후 |  |  |  |  |  |
| 7일 |  |  |  |  |  |
| 30일 |  |  |  |  |  |

42 incident를 통과한 뒤 Frontend 또는 Backend를 시작해도 42의 7일·30일 회상은 취소하지 않습니다.
Frontend transfer와 Web production regression도 서로 다른 회상 clock으로 기록합니다.

## 완료 판정

- [ ] 프로젝트 release gate를 통과했다.
- [ ] practice → 실행·실패 → answer → 무자료 재구현 순서를 지켰다.
- [ ] 답지 없는 독립 평가를 통과했다.
- [ ] 완료 직후 회상을 통과했다.
- [ ] 7일 회상을 통과했다.
- [ ] 30일 회상을 통과했다.
- [ ] 단계 카드의 다음 링크로 이동했다.
- [ ] Frontend/Backend 완료 시 병행 중이던 42 incident의 30일 회상도 통과했다.

모든 항목을 통과하기 전에는 원격 release 완료와 개인 curriculum mastery를 같은 의미로 기록하지
않습니다.
