# AUDIT.md — dual-form 전체 재검수 절차

이 문서를 읽은 세션은 **곧바로 재검수 오케스트레이터로 작동을 시작**한다. 목적은 모든 독립 레포의
dual-form 작업(답지 `docs/commits/` + 문제지 `docs/practice/`)이 정확·완전한지 검증하는 것이다.
**read-only**: 이 재검수는 보고만 한다. 코드·문서를 고치거나 커밋하지 않는다(수정이 필요하면
사용자에게 보고하고 지시를 기다린다). 먼저 루트 `CLAUDE.md`(공통 룰)도 참조한다.

## 0. 품질 최우선 원칙

- 기계 체크는 보조다. **환각(§3.3)과 블랭킹(§3.5)은 의미 판단이 핵심.**
- 추측 금지 — `git show`/실제 실행으로 근거를 확보한다.
- 의심스러우면 성급히 FAIL이 아니라 **"확인필요"**로 올리고 근거를 제시한다.
- §4 오탐 패턴은 **결함으로 보고하지 않는다.** 환경 한계와 실제 결함을 반드시 구분한다.

## 1. 대상 레포 열거

`find . -maxdepth 3 -name .git -type d` 의 부모 디렉터리 전부. **단 `document-box`와
`portfolio-public`은 제외**(전자는 허브, 후자는 공개 포폴 앱). `sportsbook/<svc>`는 각각 독립
레포 = 각각 대상. (기준일 33개: 최상위 23 + `sportsbook/` 하위 10. 단 `mobile-foundations-training`·
`mobile-reliability-training`·`sportsbook/mobile-client`는 **신규 스캐폴드(골격만, 빌드 세션 대기)** 이므로
`docs/commits`가 비어 있는 게 정상 — 빌드 후 정식 감사 대상이 된다. 기획·청사진은 `document-box/mobile-track.md`.)
누락 없게 실제로 열거한다.

## 2. 서브에이전트 디스패치 (이 워크플로는 서브에이전트 사용 무제한 허용)

- **작업 단위 = 레포 1개 = 서브에이전트 1개**(`general-purpose`). 총 스폰 수 제한 없음.
- **단 동시 실행은 4~6개로 묶는다**(한 배치 끝나면 다음 배치). 이유: ① 빌드(mvn/cmake/npm)를
  너무 많이 병렬로 돌리면 서로 느려짐 ② 오케스트레이터가 결과를 제대로 집계·검수하려면 한 번에
  들어오는 양이 통제돼야 함. 무제한 동시 fan-out은 품질을 떨어뜨린다.
- 큰 레포(>40 문서)는 그 서브에이전트가 자기 안에서 범위 분할해도 된다.
- **디스패치 프롬프트에 반드시 포함**: (a) 대상 레포 절대경로, (b) "`document-box/AUDIT.md`의
  §3 체크리스트·§4 오탐목록·§5 반환형식을 읽고 그대로 따르라", (c) "read-only — 수정·커밋 금지",
  (d) "추측 금지, git show/실제 실행으로 근거 확보".

## 3. 레포당 체크리스트 (각 서브에이전트가 수행)

1. **구조/푸시**: `docs/commits/`·`docs/practice/` 존재? `git status`가 origin/main과 동기화
   (ahead/behind 0)? 미커밋 0? (practice가 0이면 그 사유가 정당한지 §3.2로 판단.)
2. **실체성 게이트**: `practice 수 ≤ commits 수`. 많이 스킵됐으면 `practice/README.md`가 스킵
   사유를 적었는지 확인하고, **스킵된 커밋 2~3개를 `git show`로 열어** 정말 비구현(마커·콘텐츠/
   데이터·순수계약 DTO/스키마·설정·문서·merge)인지 확인. 실구현인데 스킵됐으면 결함.
3. **환각 — 답지→소스 (반드시 이 방향)**: 답지 `docs/commits/*.md`의 ```코드블록``` 안
   식별자(함수/메서드/클래스/타입명)를 뽑아, **레포 실제 소스 전체**(`git ls-files`의 코드 파일을
   ground truth로)에 존재하는지 확인. **커버 ≥ 95% 기대.** 낮으면 환각 의심 → 단 §4 먼저 적용.
   - **A/B 분할 문서(006A/006B 등)는 합산해서 비교**한다.
   - **소스→답지 방향은 쓰지 말 것**(프레임워크·테스트명·스킵커밋 때문에 가짜 누락이 쏟아짐).
   - 퍼-닥 위치 매핑(문서N↔커밋N)은 어긋나기 쉬움 → **소스 전체 합집합**으로 본다.
4. **검증 실제 실행**: 레포의 실제 테스트를 돌린다. 결과 = **green / ENV-LIMIT / FAIL**.
   - Make: `make test` · Maven: `./mvnw test` 또는 `mvn test`(서비스면 의존 라이브러리 먼저
     `install` 필요할 수 있음) · Node: `npm test`(pnpm 레포면 `pnpm -r test`) · C++:
     `cmake -B build && cmake --build build && ctest --test-dir build --output-on-failure` ·
     .NET: `dotnet test`(net8 타깃인데 런타임 없으면 `DOTNET_ROLL_FORWARD=Major dotnet test`) ·
     셸/인프라: 답지 `## 검증`이 지정한 `bash -n`·`shellcheck`.
   - **red면 분류**: Docker 미기동(Testcontainers)·런타임 버전 부재 등은 **ENV-LIMIT**(코드 결함
     아님 — 단 build/compile은 성공하는지 확인). 실제 assertion 실패·컴파일 에러는 **FAIL**.
   - **명령 실효성(반드시)**: 답지·문제지 `## 검증`에 적힌 명령을 **문자 그대로** 돌려 0개 테스트
     실행·no-op으로 끝나지 않는지 확인한다. 0-test/no-op은 green이 아니라 **확인필요**(검증이
     실제로 돌지 않음). 사례: 존재하지 않는 테스트 클래스 `-Dtest=<오타>`(betting 018),
     test 스크립트 없는 `pnpm --filter <pkg> test`(grounded 005/007/009/016).
5. **블랭킹 표본 정독**: 가장 어려운 `practice/` 1~2개를 읽고 — 계약(시그니처/구조/공개 API)은
   노출, 로직·본문은 `// TODO 책임`으로 비움, **책임 줄이 답을 누설하지 않음**, `## 검증`이 실제
   빌드/테스트/관찰인지. 매몰(원 유형 관용구를 억지 이식)·공허(빈칸 채우기=재구현 아님) 여부.
6. **드리프트(보조)**: `practice/NNN.md`의 `###` 제목 목록 == `commits/NNN.md`의 `###` 목록.

## 4. 오탐 패턴 — FAIL로 보고하지 말 것

- **§3.3에서 "소스에 없음"이 다음이면 무시**: SQL 키워드(VARCHAR/NUMERIC/UNIQUE/CHECK),
  JS/Lua 토큰(stringify/uuidv4/tonumber/tostring), 라이브러리·도구명(Mockito/lombok/CMake/plugin),
  `git show --stat` 단어(insertions/deletions/changed), useState 세터(setXxx), std 호출
  (substr/isspace/invalid_argument), prose 속 "TODO 아님", `.sql`/`.lua` DDL·스크립트 토큰.
- **§3.4에서 Docker 미기동·런타임 버전 불일치 = ENV-LIMIT**(결함 아님). `.NET`은 roll-forward로
  재시도, 그래도 안 되면 ENV-LIMIT.
- 위치 매핑으로 커버리지가 낮게 나오면 **합집합으로 재확인** 후 판단.

## 5. 반환 형식 (서브에이전트 → 오케스트레이터)

각 서브에이전트는 마지막에 한 줄 판정 + 근거를 반환한다:

```
<repo>: PASS | FAIL | ENV-LIMIT | 확인필요
  환각 <X>% (의심 <n>: <목록 또는 없음>)
  테스트 <명령> → <green / ENV-LIMIT 사유 / FAIL 사유>
  게이트 <practice>/<commits> (스킵 사유: <정당 / 의심>)
  블랭킹 <표본 문서>: <양호 / 문제>
  발견: <실제 결함 상세 또는 "없음">
```

FAIL·확인필요만 상세 기술한다. 오탐(§4)·환경 한계는 결함으로 적지 않는다.

## 6. 오케스트레이터 집계

- 모든 레포 결과를 한 표로: `PASS / FAIL(사유) / ENV-LIMIT(사유) / 확인필요(사유)`.
- **FAIL·확인필요가 있으면 맨 위에 모아 요약**(레포·항목·근거).
- **품질 게이트**: 무작위 2~3개 레포의 서브에이전트 판정을 골라 핵심 체크(§3.3 또는 §3.4) 하나를
  오케스트레이터가 직접 재실행해 일치하는지 확인(게으른 서브에이전트 방지).
- 끝에 총계(`PASS n / FAIL n / ENV-LIMIT n / 확인필요 n`)와 read-only 재확인(수정한 것 없음).
