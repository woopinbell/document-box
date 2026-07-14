# Backend 지원 데이터

42·Backend 완주 뒤 실제 지원할 정규직 공고와, 각 요구사항에 제시할 수 있는 검증 근거를 날짜별로
관리합니다. 공고 목록은 트랙 순서나 release 완료 판정을 바꾸지 않습니다.

## 현재 문서

- [`2026-07-14.md`](2026-07-14.md): 2026-07-14 KST에 현재 지원 가능 상태를 재확인한 공고와
  제외 reconciliation
- [`EVIDENCE.md`](EVIDENCE.md): Training·Sportsbook release를 직무 요구사항에 연결하는 제출용
  증거 matrix와 과장 금지선

## 포함 기준

1. 기간의 정함이 없는 국내 정규직만 포함합니다. 인턴, 전환형 인턴, 계약직과 프리랜서는 제외합니다.
2. 국내 숫자 하한은 기본연봉 연 4,000만원입니다. 공고에 숫자가 없으면 4,000만원 이상 회사 평균과
   자동 갱신되는 연봉수준 태그를 함께 확인한 경우만 보상 proxy로 조건부 포함합니다.
3. 해외는 한국 거주자를 employee 또는 EOR로 고용할 수 있고 기본연봉 USD 60,000 이상인 full-time
   공고만 포함합니다. contractor만 가능한 공고는 제외합니다.
4. 신입·0~2년을 직접군, 3년 또는 동등역량을 명시한 공고를 상향군으로 분리합니다. 고정 3년 이상
   실무나 production 운영을 요구하면서 동등역량을 인정하지 않는 공고는 트랙 완주만으로 지원 가능하다고
   판정하지 않습니다.
5. Java·Kotlin·Spring은 직접군, Node·Go·Platform·Fullstack은 현재 release로 실제 요구사항을
   입증할 수 있을 때만 인접군으로 둡니다.
6. VoyagerX는 검색 결과와 관계없이 제외합니다.
7. 회사 평균과 백분위는 개인 offer가 아닙니다. proxy 공고는 전형 전에 기본연봉 하한을 확인합니다.
8. Training V2, Risk correctness와 Orchestration release는 고정된 ref만 지원 근거로 사용합니다.
   공식 27개 프로젝트의 private 전환과 원격 전수 audit는 완료됐으며, 필요한 경우에만 채용
   담당자에게 선택적으로 repository invitation을 제공합니다. 공개 코드를 영구 증거로 약속하지 않습니다.

## 현재 판정

이 snapshot은 지원 후보를 고른 상태일 뿐 실제 제출을 뜻하지 않습니다. Foundations V2,
Reliability V2, Risk correctness와 Orchestration의 release ref는 확정됐습니다. 지원 버튼,
고용형태와 보상은 제출 직전에 다시 확인합니다. 27개 공식 프로젝트는 private audit를 통과했으며,
repository 초대 범위와 기간을 최소화합니다.
