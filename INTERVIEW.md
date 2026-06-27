# INTERVIEW.md — L3 백지 설명 세트 (면접 답안 골격)

> [LEARNING.md](LEARNING.md) §6("전 프로젝트의 L3 항목만 모아 백지 설명 세트를 만든다")의 산출물.
> **L3 = 문서·코드 없이 백지에서 설명/작도할 수 있어야 하는 항목** — 그 자체가 면접 답안의 골격이다.
>
> **사용법**: Part 1(주제별 코어)을 면접 축으로 백지 설명 연습 → 막히면 `[레포 NNN]` 포인터로 해당
> `docs/commits/NNN.md` 답지를 펼쳐 복기 → Part 2(레포별 전체 색인)로 프로젝트 단위 커버리지 점검.
> **정본 관계**: 각 답지의 `## 기억/설명 Level` L3가 정본이고 이 문서는 파생 색인이다(2026-06-11 추출,
> 40/40 레포). 답지 L3가 바뀌면 여기를 재추출한다 — 여기에 새 항목을 직접 창작하지 않는다.

---

## Part 1 — 주제별 코어 세트 (폭발 반경 축)

LEARNING §1의 "폭발 반경 큰 것만 과투자" 주제를 축으로, 같은 원리가 스택을 가로질러 반복되는 항목을
묶었다. 면접 질문은 레포가 아니라 주제로 들어온다 — 한 주제를 백지 설명할 때 아래 사례들을 같은 답의
변주로 엮을 수 있으면 통과.

### A. 동시성·락

- 식사 철학자: 홀짝 fork 순서로 원형 대기 차단, monitor 단일 종료 판정, 단일 철학자 전용 수명주기 [thread-dining 005·007·009]
- mutex 경계 설계: state_mutex(일관성) vs print_mutex(출력 직렬화), death 경로 잠금 순서 [thread-dining 004]
- DB 행 직렬화: `@Lock(PESSIMISTIC_WRITE)`와 락 해제의 트랜잭션 커밋 결속 [wallet 005], `findByCodeForUpdate`+차감의 oversell 방지 [backend-reliability 014]
- 단일 락 ownership boundary: ConcurrentSessionRegistry/ThreadsafeSessionRegistryLite의 copy snapshot 반환 [gsr 029 / gsf 021]
- single-flight: 401 storm에서 refresh 1회로 접기(`current != failedToken` 재사용 판단) [mobile-client 004·012 / mr 067~069]
- bounded concurrency: unbuffered channel+고정 worker, 취소 시 accepted만 drain [backend-reliability 073·074 / bf 088]
- race 증명 테스트 설계: 100 동시 debit→단일 분개 쌍, 8스레드 storm→refresh 1회, 16스레드 재정산→outbox 1행 [wallet 008 / mobile-client 012 / settlement 014]
- coarse-lock vs snapshot-broadcast를 counter로 관찰(벽시계 아님) [gsr 065]

### B. 트랜잭션·정합성

- 트랜잭션 경계: debit—실패—credit 단일 boundary의 양행 rollback 증명 [bf 061·062], 부분 반영 미커밋 [bf 060]
- 외부 HTTP를 DB 트랜잭션에 넣지 않는 이유(커넥션 점유→풀 고갈) + 별도 빈=경계 강제·self-invocation 회피 [betting 014]
- double-entry: 차변/대변 합=0 invariant, `UNIQUE(idempotency_key, side)`로 멱등 강제+matched-pair 허용 [wallet 002]
- 이중 정합성: per-operation 검사 + 일일 배치(스냅샷-원장 일치), after-commit invariant vs 트랜잭션 시점 방어 분담 [wallet 016·017]
- 2-phase 정산: prepare tx+lock → credit(트랜잭션 밖) → finalize tx + isPending 재가드 [settlement README→009]
- 정산 수학: payout=unitStake×Σ_lines Π_legs multiplier, WON 2-leg(REFUND+PAYOUT — 단일 credit은 double-entry 파괴), LOST=forfeit locked→house [settlement README→004·008·021 / wallet 020]
- 보상(reconciliation): stale PENDING 멱등 re-debit, 200=roll-forward/422=roll-back/503=defer, roll-back 환불 금지 이유 [betting 018]

### C. 멱등성·중복 제거

- 멱등 3층: Redis fast path(가속) / 비관적 락 write path / DB UNIQUE(권위) — 최종 권위는 항상 DB [wallet 007 / betting 003·014]
- 멱등 키=의도의 순수 함수: same key+payload replay vs same key+different payload conflict [backend-reliability 009 / bf 064·065 / rag-agent 006 / shared-contracts 008]
- 실패는 캐시하지 않는다(키 삭제) — exactly-once의 폭발 반경 [ai-reliability 008 / reliability-gateway 003]
- 클라이언트 멱등 정책: 한 슬립=한 키 재사용, 재시도=같은 키, 재가격(드리프트 재확인)=새 키 [mobile-client 007·011·012]
- 소비자 멱등: BetSettled 재배달 no-op, unknown betId/불법 전이 throw→DLT [betting 024·026]

### D. 돈 계산

- long minor units 표현(부동소수 차단), 와이어(Avro)·도메인 동시 미러 [shared-protocol 003 / orchestration notes]
- `Math.*Exact`(조용한 wraparound=금전 사고) [shared-protocol 003 / mobile-client 002]
- BigDecimal 함정: record 기본 equals의 scale 동등성(1.85≠1.8500) → compareTo 기반 equals+hashCode 계약 정합 [shared-protocol 004 / mobile-client 002]
- 경계 정밀도: double 0.01 부정확 → divide scale+RoundingMode 명시, slippage cross-multiplication 무반올림 [odds-feed README→006 / betting 006]
- K-of-N payout: C(N,K) line 조합, FLOOR 1회 보수적, binomial long 안전 상한 [betting 008·009]

### E. 분산·이벤트

- transactional outbox: dual-write 불일치 vs 같은 트랜잭션 원자 기록, publisher drain at-least-once(ack 후 published_at), 중복은 소비자 멱등 흡수 [betting 012·016 / wallet 009·010 / backend-reliability 042·043]
- partition key 선택: 슬립은 다중 경기→userId(per-user 순서), 시세는 eventId(경기 전순서) [betting 013 / odds-feed README→006]
- 동기 orchestration vs 비동기 Saga: 접수=동기(slippage 분쟁·즉답 UX·강한 일관성), 정산=비동기 [betting README→014 / orchestration 008]
- 계약 드리프트의 검출 한계: producer/consumer 토픽 불일치(`bet.placed` vs `.v1`)는 단위 테스트가 구조적으로 못 잡고 전체 스택 e2e만 잡는다 [gateway 006 / settlement README→020 / orchestration 007]
- 인프라 기본값 위장 장애: Kafka 단일 브로커 RF=1 미설정→coordinator 부재→consumer 전 마비·producer 멀쩡 [orchestration 003·007]
- write-through가 non-atomic이어도 되는 경우: odds 이벤트 멱등성·다음 변경이 정정 — 돈만 outbox [odds-feed README→005]

### F. 네트워크·실시간

- 이벤트 루프 추상화: kqueue/epoll backend 분리, fd 관심사만 표현 [irc 002], nonblocking framing(완성 줄만 소비·partial buffer 유지) [irc 005·007 / gsr 013]
- backpressure 2층: 연결별 outbound queue cap + 서버 전체 max connection [irc 017], slow client 격리(per-client bounded channel) [gsr 038]
- heartbeat/idle: registration timeout·idle ping·ping timeout 분리, 같은 tick 오판 방지 순서 [irc 015]
- STOMP: 핸드셰이크 URL vs SUBSCRIBE destination(합치면 영원히 무수신), per-user 라우팅(서버가 `sub`로 해소) [mobile-client 009 / gateway 004]
- 재연결: 지터 지수 백오프(천둥 무리 방지), 한 연결=한 flow 수명, 재연결마다 최신 토큰 [mobile-client 009 / mr 074·075]
- 서버 권위 게임 상태: 입력 방향만 신뢰, tick 루프 계산, 인증 전 payload 버퍼링·매칭 큐 pruning [pong 022·041]
- 시그널 IPC: 비트 조립 MSB-first, ACK 동기화(sigsuspend), NACK 단일 송신자 소유권 [signal-message-bus 002~007]

### G. 시스템·프로세스·메모리

- fork/exec/wait 모델, 자식의 `_exit`(stdio flush 이중 출력 방지), 127/126·128+sig 관례, EINTR 재시도 [small-shell 009]
- fd/리다이렉션: dup2 후 close, 파이프 "모든 끝 닫기"(EOF 데드락), heredoc 임시파일 실체화 [small-shell 009]
- parent builtin 경계: 부모 상태를 바꾸는 명령은 자식에서 실행하면 효과 소실 [small-shell 008]
- ownership 규율: 소유/참조 분리(table-philo, t_env 복사), 부분 초기화 실패 시 destroy 대상 한정 [thread-dining 003 / small-shell 003]
- allocator·예외 안전: construct 중 예외 시 강한 보장 정리, rebind node allocator [stl-container 006A·016A]
- async-signal-safe 경계: volatile sig_atomic_t·핸들러 내 write [signal-message-bus 002]

### H. 인증·보안

- 엣지 검증+신뢰 헤더: gateway가 JWT 검증 후 `X-User-Id` 주입, 인바운드 위조본 strip — 내부망 신뢰 모델 [gateway 001·003]
- RS256/alg 고정: HS256 혼동 공격(공개키=HMAC 비밀) 방어 [admin-api 001·004]
- stateless JWT vs 세션: 수평 확장 자유, 무효화는 짧은 TTL+refresh / 수동 세션·Spring Security 세션의 저장 위치 [gateway 001 / bf 029·033]
- 로그아웃 권위=서버 세션 저장소(쿠키 아님): 토큰 폐기로 전 경로 무효 [pong 084]
- 권한 판단 분리: role 기반 policy matrix(401/403 분리), aspect ordering의 거부까지 감사 [backend-reliability 047 / admin-api 003]
- 클라이언트 보안 경계: RSC server-only 모듈·serialized props로 private field leak 차단, auth state 결정 전 sensitive UI flash 차단 [frt 107~129]

### I. 신뢰성 패턴

- circuit breaker: 비즈니스 거절(200/422)을 실패로 세면 안 되는 이유 — record-exceptions를 인프라 예외만으로 [betting 010]; 세 상태 전이+open 시 비호출(attempts 0) [backend-reliability 062 / ai-reliability 032]
- token bucket: refill 수식·burst 허용·key isolation, `retryAfterMillis`=다음 refill 경계 [backend-reliability 025·026 / ai-reliability 012 / br Go 068~070]
- fail-open vs fail-closed: rate limiter Redis 다운=fail-open(front door 가용성), admin JWT 공개키 부재=fail-closed crash [gateway 002 / orchestration 007]
- timeout·retry·fallback의 순서: budget pre-check→breaker→retry→fallback, cache hit→charge 스킵 [reliability-gateway 010]
- degraded vs outage: tier 순서 무너짐(싼 모델→캐시→canned), 전 tier 실패만 503 [reliability-gateway 009 / ai-reliability 032]
- 재시도 분류의 단일 출처: transient(업스트림·429) vs 결정적 실패(grounding·validation)를 계약에 둔다 [shared-contracts 002 / reliability-gateway 002]
- async job lifecycle: PENDING 선기록→worker 후 terminal, RETRY_WAITING/DEAD_LETTER, pessimistic lock 동시 실행 경계 [bf 068·069 / backend-reliability 031·032]

### J. 프론트·클라이언트 신뢰성

- stale response 방지: 필터를 query key에 포함(늦은 이전 응답의 현재 화면 덮어쓰기 차단), flatMapLatest 취소 [frt 016~020 / mr 012·013]
- optimistic update: snapshot→optimistic 반영→identity-gated commit/rollback(stale mutation 무시), pending guard=요청 1회 증명 [frt 042~048 / mr 030·031 / mobile-client 011]
- URL이 source of truth: search/sort/page의 공유·재진입·히스토리 재현, invalid param 정규화, page 1 리셋 [frt 035~040·078~083 / portfolio 018·020]
- error boundary: local 격리·recoverable fallback·reset 이중성, global boundary가 작은 실패를 키우는 실패 모드 [frt 022~026]
- 오프라인 우선: DB 단일 진실원·write-through·실패 시 캐시 보존, versioned cache의 fresh/stale/error 정직 라벨 [mr 036~038 / mf 009 / frt 064~069]
- 상태 모델: sealed/discriminated union으로 불가능 상태 차단, 일회성 이벤트는 Channel 분리(회전 재생 차단) [mf 004 / mr 002·018·019]
- 가상화 안전: visible slice+overscan만 mount, `aria-activedescendant`의 mounted 한정, off-by-one 가드 [frt 057~062 / mr 092·093]
- RSC/Suspense 경계: server/client 직렬화 경계, 느린 섹션 격리 streaming, protected route의 서버 측 auth 결정 [frt 098~129]

### K. 관측성·검증 문화

- correlation id 전파: API/cache/db/queue 전 구간 동일 id, 실패의 구조적 이벤트 기록 [backend-reliability 057·058]
- 다단계 회계: token/cost 전체 합·latency는 root만(이중 계산 회피) [ai-reliability 024 / reliability-gateway 007]
- 측정 정직성: dev-host p99 한계를 하드웨어 경계로 정직 기술(정합 불변식=dev 증명, 규모=production), constant-arrival-rate vs constant-vus [betting 022 / risk README→009 / settlement README→018]
- 단독 그린≠통합 그린: 단위 테스트가 구조적으로 못 잡는 3계층(인프라 기본값/설정 주입/서비스 간 계약) [orchestration 007]
- 검증 도구를 의심: libc parity byte 비교(null byte), 독립 적용기로 출력 스트림 검증, 데이터로 인한 그린 함정 [format-printer 009 / stack-sort 018]
- e2e 결정론: restart·flush로 stale 상태 제거(영영 안 끝나는 시나리오 차단) [orchestration 006]

### L. AI 신뢰성

- grounding 게이트: 검색 청크·인용 교차 대조, 인용 0 거부=환각 방어, "응답 인용 ⊇ 일정 인용" 가시성 [rag-agent 008 / shared-contracts 005·009 / ai-foundations 028]
- step-cap: FINAL return vs MAX_STEPS raise — 무한 루프=무한 비용, HTTP 계약화(비종료 trace 200 차단) [rag-agent 007·009 / ai-foundations 036·037]
- eval 3층(결정·judge·회귀): judge 비결정성은 baseline tolerance로 견디고 결정적 메트릭이 백본, golden 순환 끊기 [ai-foundations 040·041 / eval-gate 003~008]
- sampling 제어: temperature 분포 조형·top-p nucleus·seed 재현 경계, 수치 안정화 [ai-foundations 012·013]
- semantic cache 트레이드오프: 비용·지연 절감 vs 낮은 threshold의 틀린 답 재사용·stale 무효화 [reliability-gateway 006]

---

## Part 2 — 레포별 전체 L3 색인

추출 기준: 각 답지 `## 기억/설명 Level`의 L3 절(일부 레포는 commits/README 중앙 색인 — `README→NNN`으로
표기). 항목 수는 추출 시점 기준.

### 클러스터 1 — C

#### small-shell (13)
- [002] 입력 한 줄이 `t_token`→`t_command`→`t_pipeline`→`t_sequence`로 올라가고 실행 상태가 `t_env`/`t_shell`에 남는 데이터 모델
- [002] parser/expander/executor가 같은 헤더 계약을 공유해 원본 문자열 재해석 대신 구조체 경계를 넘기는 이유
- [003] `envp`를 내부 소유 `t_env` 리스트로 복사하고 그것이 확장·외부 환경 전달·export/unset의 기준 저장소가 되는 흐름
- [004] lexer의 책임 경계(문법 검증이 아닌 최소 토큰 절단)와 parser로 넘기는 오류 구분
- [004] 작은따옴표 `LITERAL_MARK` 보존 vs 큰따옴표 확장 가능 문자 — expansion 판단 근거 생성
- [005] token list→command(argv/redirs)→pipeline(|)→sequence(;/&&/||) 계층
- [005] 연산자 의미를 실행 전 구조에 보존해 executor가 재해석하지 않게 하는 설계
- [006] expansion 단계의 위치와 `$NAME`/`$?`/quote marker/heredoc dequote가 다른 규칙인 이유
- [006] 작은따옴표 marker의 `$` 재해석 차단, heredoc delimiter의 확장 없는 dequote
- [008] 부모 셸 상태를 바꾸는 builtin을 부모에서 실행해야 하는 원칙
- [009] `shell_process_line`의 토큰화→파싱→heredoc→실행→정리 전체 모델
- [009] heredoc 수집·redirection·parent builtin·fork/pipe/exec/wait·connector dispatch의 프로세스/단계 배치
- [009] parent builtin의 stdio 저장/복구 vs pipeline 내부 명령의 자식 실행 경계

#### format-printer (8)
- [002] `%` 뒤 flags→width→precision→specifier 고정 소비 순서와 `t_format` 구조
- [002] parser가 출력 단계 입력 계약을 결정해 변환 함수가 format을 재독하지 않는 책임 분리
- [006] 출력 길이 선계산→`width-실길이` padding→`-` flag 정렬 골격
- [006] digit buffer 선구성+공통 padding helper로 text/숫자/hex 통일
- [007] 문자열 절단·숫자 leading zero·`precision=0`+`value=0` digit 숨김 세 분기와 출력 순서
- [007] 숫자 precision 지정 시 `0` flag 무효 우선순위
- [009] stdout pipe 캡처로 `ft_printf` bytes를 `snprintf`와 byte 단위 비교하는 parity 테스트 방법론
- [009] 정적 라이브러리+테스트 바이너리 묶음과 null byte 같은 문자열 비교 함정의 byte 비교 해소

#### signal-message-bus (13)
- [002] 시그널 비트 조립(좌시프트+LSB 설정, 8비트 flush) 상태 전이
- [002] MSB-first 복원 원리(서버 좌시프트 선행→클라이언트 상위 비트 먼저)
- [002] 핸들러 안전성: volatile sig_atomic_t·SA_SIGINFO·write(async-signal-safe)
- [003] 바이트→8 시그널 변환 전송과 한 비트 실패=바이트 실패
- [003] send_byte의 7→0 비트 순서와 서버 조립의 연결
- [004] NUL 종료 프로토콜(본문 뒤 '\0' 전송→서버 줄바꿈 변환)과 경계 결정
- [004] 빈 메시지=종료 바이트만, 경계는 내용이 아닌 종료 바이트
- [005] ACK 기반 비트 전송 제어와 고정 usleep 대비 필요성
- [005] ACK 선블록+sigsuspend 대기 — kill 직후 ACK 유실 방지
- [006] ACK 성공/송신 오류/timeout 세 종결 상태 모델
- [006] 서버 부재 시 SEND_TIMEOUT 종료의 필요성
- [007] 단일 활성 송신자 소유권(첫 비트 PID, NUL까지 유지)
- [007] NACK 거절로 서로 다른 메시지 비트 혼합 차단

#### thread-dining (36)
- [003] table 소유/philo 참조의 ownership 구조와 원형 fork 매핑 `(i+1)%n`
- [003] cleanup 기준=초기화 성공 기록값(fork_count 등), 부분 초기화 실패의 중복 destroy 위험
- [003] last_meal_ms 임시값과 실제 기준 시각의 재설정 시점
- [003] "table이 소유하고 philo가 참조한다" + "destroy 가능한 대상만 닫는다" 압축
- [004] state_mutex(일관성) vs print_mutex(출력 직렬화) 분담
- [004] 일반 로그의 종료 후 억제, death 로그의 should_print 단일 출력
- [004] death 경로의 잠금 순서(상태 락 해제 후 출력 락)
- [004] timestamp 계산과 smoke 출력 형식 기준
- [005] 홀짝 fork 순서의 원형 대기 차단
- [005] fork 2개 확보 후 식사 전이, "has taken a fork" 출력 시점
- [005] last_meal_ms 갱신=monitor 사망 판정 기준 갱신
- [005] meals/full_count의 중복 완료 차단과 state_mutex 보호
- [005] 단일 철학자 미분기 시 같은 mutex 이중 잠금 한계(009에서 해소)
- [006] philo_run의 시작 진입점과 start_ms 통일 초기화
- [006] thread 인자 ownership 전제(table destroy 전까지 배열 생존)
- [006] pthread_create 실패 시 생성분만 join하는 부분 복구
- [007] 종료 판단 주체=main thread monitor(worker는 관찰만)
- [007] 전체 완료 vs death 판정 조건과 state_mutex 보호
- [007] create→monitor→join 흐름
- [007] "종료 조건을 monitor에 모았다" 면접 압축
- [009] 단일 철학자의 같은 mutex 이중 잠금 위험
- [009] number==1 선분기 차단 위치
- [009] 전용 경로(fork 1개+time_to_die 대기, is eating 없음)
- [009] "일반 알고리즘을 단일 케이스에 강요하지 않는다" 압축
- [010] 마지막 필수 식사 완료의 즉시 ended 반영(polling 의존 제거)
- [010] meals/full_count/ended 동일 락 갱신과 최초 도달만 카운트
- [010] eat_once 반환값과 종료 재확인(후속 로그 차단)
- [010] "완료=종료 조건이자 로그 차단 조건" 압축
- (외 004~010 세부 항목 — 답지 원문 참조)

#### stack-sort (11)
- [001] 공통 소스+이중 entry의 Makefile 이중 빌드 골격
- [001] public header의 함수 경계 선점 책임
- [002] 배열 0=top, values/ranks 병렬 저장의 값 범위 독립 모델
- [002] 정렬기·checker 공유 완료 판정 함수
- [003] emit 플래그로 출력/적용 책임을 한 wrapper에 묶는 호출 규약
- [003] 모든 push의 values/ranks 동순 이동 invariant
- [004] rr/rrr 복합 명령의 단일 출력 wrapper
- [007] 좌표 압축(임시 정렬+binary search→0..n-1 rank)
- [007] 중복 거절(정렬 사본 인접 비교)
- [011] LSD radix(bit 라운드, ra/pb 분리→pa 복원)
- [018] Python 독립 적용기로 출력 스트림 의미를 구현과 분리 검증하는 전략

### 클러스터 2 — C++/시스템서버

#### stl-container (7)
- [005] iterator base/traits/포인터 특수화/reverse_iterator의 역방향 증감·역전 비교
- [006A] vector의 alloc/data/size/capacity 직접 보유와 allocator 생명주기 처리
- [006A] _reallocate의 construct 중 예외 시 강한 보장 정리
- [009A] map의 BST 노드·rebind·NULL end iterator+_root snapshot·순회 helper 모델
- [012] range assign/insert의 임시 vector 선복사 self-aliasing 안전 처리
- [016A] value allocator→node allocator rebind 경로(전 생성자 동일 상태)
- [016B] 노드 색상·root black·insert_fixup(uncle 색)·erase_fixup(black-height 보정)

#### ray-scene-tracer (6)
- [002] 공유 타입 시스템(Vec3/Ray/Material/HitRecord/Scene/Image)
- [002] Shape 추상+동일 intersect 시그니처·setFaceNormal 일관성
- [003] .rt 파싱 파이프라인(검증→ParseError 위치 보고→렌더 전 중단)
- [003] 카메라 광선→최근접 hit→그림자→shading 픽셀 계산 helper 구조
- [004] 구(2차방정식)/평면/원기둥(옆면+캡 closest 공유) 교차와 앞/뒷면 처리
- [007] 결정성 계약(P3 PPM+FNV-1a 체크섬)으로 렌더 검증·회귀를 한 형식에 고정

#### irc-relay-server (22)
- [000] 구현 전 README로 event loop/nonblocking/명령 범위/검증 기준 고정
- [002] EventManager의 kqueue/epoll 분리와 read/write 관심사 표현
- [005] Connection의 fd 소유·line 추출·outbound queue·partial write 캡슐화
- [005] wouldBlock/peer close/line 초과/pending flush 상태 전이
- [006] Server의 accept~disconnect lifecycle과 line callback 경계
- [006] close 후 pending write의 write interest 유지
- [007] IrcMessage의 prefix/command/params/trailing 구조화(protocol boundary)
- [007] 완성 newline frame만 소비(TCP stream framing)
- [009] Channel의 membership/operator/invite/topic 상태 모델
- [010] IrcApplication의 registration gate·canonical nick·broadcast·cleanup 연결
- [011] 실 TCP smoke가 parser/루프/핸들러를 한 흐름으로 검증
- [015] ClientState의 timeout 3종 분리와 maintainClient 판단 순서
- [016] rate limit의 배치 위치(activity 기록 후·parser 후·handler 전)
- [017] queue cap+max connection의 이중 backpressure
- (외 — 답지 원문 참조)

#### game-server-foundations-training (16)
- [000] 두 트랙(cpp/csharp)+common/spine/bridge 책임 분리와 make 검증 일원화
- [002] PacketDecoder/Result/TickAccumulator 세 축 계약
- [006] PacketFramer의 partial/coalesced/oversized 시나리오
- [009] RoomDirectory=도메인 서비스(스냅샷 읽기 모델+enum 분기 강제)
- [012] FIFO 매칭 계약(2 미만 비소비, skill 미사용)
- [021] 단일 mutex 레지스트리(get 복사본·lock 안 순회)
- [031] C# RoomDirectory(대소문자 무시 인덱스·owner 자동 등록·빈 방 제거)
- [035] LobbyService(브로드캐스트 자기 제외·가득 찬 큐 oldest drop)
- [043] 어댑터=검증+enum→문자열 코드 매핑(도메인 규칙 미창조)
- [047] SessionContext(전이 규칙 통과만 갱신·Closed 전환 보존)
- [055] AsyncWorker(bounded Channel 단일 reader·Stop의 pending 취소)
- [062] CI 3-job(cpp/csharp/docs) 분리 구조
- (외 — 답지 원문 참조)

#### game-server-reliability-training (23)
- [009] TCP 세션 상태 머신과 protocol violation 분리 기록
- [013] 프레임 포맷(4B len+2B type)·partial buffering·fault reset 의미
- [017] HeartbeatMonitor(주입 clock·sequence 엄격 증가·late heartbeat 부활 금지)
- [021] FIFO anchor 매칭(mode+skill gap 후보→capacity 모음)
- [025] FixedTickLoop(wall-clock 직접 적용 금지·stale input drop·fractional 보존)
- [029] ConcurrentSessionRegistry(단일 ownership boundary·copy snapshot·정렬 반환)
- [033] .NET room server(lock 기반 snapshot/outbox/metrics)
- [038] WebSocket lobby(per-client bounded channel로 slow client 격리)
- [043] 매치메이킹(pending 리스트+player 인덱스 이중 구조·완화 정책)
- [053] ReconnectResumeStore(ticket TTL·controlling session 교체로 stale command 차단)
- [057] InterestManager(radius predicate+spatial hash·enter/leave diff)
- [061] ShardRouter(single-route invariant·atomic move)
- [065] coarse-lock vs snapshot-broadcast counter 관찰 lab
- [069] selective reliability(pending map·due resend·seen dedup·reliable만 ack)
- [077] A* per-request expansion budget(부분 경로 노출 금지)
- [081] union-find 연결성(mutation/rebuild 경계·flood fill 회피)
- [085] priority scheduler(due/priority 순서·per-tick budget·stale entry suppression)
- [095] SRE 드릴 5종+C# anti-cheat/recovery 드릴 모델
- (외 — 답지 원문 참조)

### 클러스터 3 — 인프라

#### container-stack (9)
- [000] nginx 443 단일 진입점+내부 서비스 경계
- [004] MariaDB entrypoint의 첫 실행 판별→임시 socket bootstrap→최종 전환
- [004] _FILE 비밀번호·필수 env 검증의 secret 분리
- [007] WordPress entrypoint의 대기→WP-CLI idempotent 준비·재실행 내성
- [009] nginx의 정적 직접 처리+PHP만 FastCGI 전달
- [010] healthcheck 체인(MariaDB→WordPress→nginx)과 service_healthy
- [010] 볼륨의 보존·공유 역할과 읽기 전용 접근
- [011] Compose secrets(/run/secrets)+_FILE 정책
- [013] source-only 정적 검증기의 실행 전 정책 강제 경계

#### linux-admin (2)
- [004] hardening checklist의 동시 점검 이유(계정·암호·SSH·sudo·방화벽·모니터링)
- [004] SSH policy(유입 통제) vs sudo policy(권한 상승 통제) 책임 분리

#### network-routing-notes (2)
- [003] 서브넷 계산 순서(prefix→mask→network/broadcast→usable→동일 서브넷 판정)
- [003] longest prefix match 우선과 default route fallback

### 클러스터 4 — TS/Node

#### grounded-travel (19)
- [003] schemas=API·agent·web 공유 단일 계약, config의 검증 경계
- [005] provider 계약 의존(구현 이름 비의존)·무료 기본값+명시적 확장점
- [005] 캐시·rate limiter가 provider 내부 핵심 책임인 이유
- [007] planTravel 루프(검증→후보→클러스터→LLM 초안→결정적 일정→검증→재계획)
- [007] LLM draft는 placeIds만 제안·후보 ID 재검증으로 grounded 보장
- [007] deterministic fallback(LLM 부재에도 일정 생성)
- [009] API-agent 경계(스키마 검증→실행→응답 재검증)
- [011A/B] 공유 계약 기반 프론트, 두 디자인의 동일 상태·액션 계약
- [016] "파싱 성공≠계약 만족" — 외부(LLM) 입력의 런타임 타입 가드 필요
- (외 — 답지 원문 참조)

#### chatbot-evaluation (16)
- [003] schemas가 runner/API/UI/storage 공통 언어, local-first 데이터 흐름
- [005] SUT/Judge/Runner 분리와 한 run의 실행 흐름(판정 병합→요약→리포트)
- [005] SUT 오류 격리·LLM judge fallback·secret masking 실패 원칙
- [007] 비동기 run(즉시 runId+polling/SSE), sample/imported suite 통합 경계
- [009] 대시보드 운영 흐름과 Design 1/2 공유 상태
- [012] local-first 평가 전략(mock/replay 기본, Ollama 보강, rule fallback)
- (외 — 답지 원문 참조)

#### pong-pong (83 — 대표 발췌, 전량은 답지 README L3 참조)
- [003·004·005] 서버 권위 Pong 계약·입력 union 제한·shared 단일 진입점
- [006·008·010] 초기 스키마 경계, SQL 마이그레이션 경로, AppRepository 단일 저장소 계약(PG/Memory 동일 표면)
- [016·018] DATABASE_URL 기반 저장소 선택, cookie/Bearer/query 단일 세션 조회 경계
- [021·022] /play의 의도 송신·스냅샷 수신, GameHub 서버 tick 루프와 종료 기록
- [041] 인증 전 payload 버퍼링·큐 pruning(연결 직후 유실/오염 방지)
- [049·050·057] liveStats=허브 상태(저장 데이터 아님), 로비 채팅 쓰기 경계, presence 이벤트 동기화
- [055·056] 샘플 제거 후 서버 스냅샷 파생 상태, pause/resume 서버 권위 전환
- [060~063] 토너먼트 브래킷 전이 모델·감사 로그·정지 계정 이중 차단·통합 검증 축
- [065·069·070] bestStreak=저장소 계산 계약, onlinePlayers=라이브 세션, 공 가속=서버 tick 상태
- [073~076] 익명 즉시 null 세션 경계, 401=토큰 즉시 제거, 두 비로그인 수렴 차이
- [077~081] NPC seed/DTO 계약→큐 fallback timer→실경기 연결의 전체 흐름
- [084] 로그아웃 권위=서버 세션 저장소(deleteSession 전 경로 무효)

#### frontend-foundations-training (13)
- [000] check:repo 검증 표면과 단계별 차단 실패
- [002] 공유 데이터 계약 경계와 createPageResponse 안정화 규칙
- [003] API route의 공유 타입·fixture 기반 응답 통일
- [004] catalog helper+ExerciseDemo 런타임 구조, slug 기반 패널 선택
- [067] App Router server/client 책임 모델(URL 소유·직렬화 경계)
- [087·088] CI 필수 경로 확장, catalog 기반 문서 검사 표면
- [092·094] pagination 불가능 상태 방지(clamp·삭제 후 보정)와 회귀 고정
- (외 — 답지 원문 참조)

#### frontend-reliability-training (157 — 대표 발췌, Part 1 J절과 답지 README L3 참조)
- [001~007] dual workspace 계약, drill 아키텍처(catalog/registry/layout), 테스트 baseline(MSW unhandled error), CI verify job
- [009~013] 폼 검증 계약(클라이언트 차단·서버 field error 재매핑·중복 제출 방지)과 접근 가능한 오류
- [016~020] async 상태 분리와 stale response 방지(query key scope)
- [022~026] local error boundary 격리·복구·로깅, boundary 배치 원칙
- [028~030] 접근 가능한 modal(focus trap·restoration·Escape)
- [035~040] URL state source of truth와 정규화·write-back
- [042~048] optimistic update lifecycle과 mutation identity
- [050~054] route locale source of truth와 side effect 묶음
- [057~062] virtualization safety(visible slice·activedescendant 한정)
- [064~069] versioned cache freshness/fallback
- [071~076] design-system state priority(loading>disabled)
- [078~083] URL-backed filtering 계약과 scale boundary
- [085~089] realtime ordering/dedup·bounded memory
- [091~096] performance budget gate(CI 연결·drift 위험)
- [098~121] RSC/Suspense 경계(server-only·직렬화 props·섹션 격리 streaming)
- [123~129] protected route(서버 auth 결정·sensitive UI flash 차단)
- [136] drill 아키텍처 확장과 docs verification contract

#### portfolio-site (36 — 대표 발췌)
- [004~006] 콘텐츠 JSON 경계→타입 경계(union key)→조립·노출 필터·env href 정책
- [018~021] App Router query 처리(view/debug 유지), 동적 상세 route와 generateStaticParams
- [035] helper 순수 계약 선잠금 전략(browser 없이)
- [037] browser smoke 경계(unit이 못 보는 실 routing·source-only 정책)
- [038~040] timeline 데이터/해석 분리, interview-map 양방향 연결, curation rationale(뺀 것 명시)

### 클러스터 5 — Java/Spring

#### backend-foundations-training (51 — 대표 발췌)
- [001] 멀티 프로젝트 구조와 공통 정책, 학습 경계로서의 의존성 선택
- [005·009·013] MVC 계약, 인메모리 CRUD 책임 분리, validation→안정적 오류 코드 변환
- [017·021] JPA 계층 흐름(dirty checking vs 명시 저장), one-to-many 경계 검증(부모 확인·자식 오조작 방지)
- [024·026] 테스트 슬라이스 선택 기준(web/data/full)
- [029·033] 수동 세션 vs Spring Security 세션 인증 흐름과 logout 정리
- [037·041·045·049·053] pagination 계약, multipart 정책(404 vs 413), owner-only, cart 스냅샷, workflow 경계
- [057·060~062] profile 분리, 트랜잭션 경계와 rollback 증명
- [064·065·068·069] 멱등 create semantics, async job lifecycle
- [076~088] Go: Handler 분리, mutex Store, 결정적 List, 설정 우선순위, worker 이중 select
- (외 — 답지 원문 참조)

#### backend-reliability-training (100 — 대표 발췌, Part 1 B·C·I절 참조)
- [004·005] 가입 전이(정규화→트랜잭션→unique fallback), PBKDF2 per-salt, 동시 중복 가입 수렴
- [009·010] 멱등 3요소(JVM lock+tx+DB unique), replay/conflict, 동시 중복의 row 1 증명
- [014·015] 비관 잠금 차감의 oversell 방지와 잔여 음수 차단
- [019·020] keyset cursor(anchor+tie-breaker)의 offset drift 회피, insert-between-pages 무중복
- [025·026] token bucket(키별 lock·refill·retryAfter 계산·key isolation)
- [031·032] 재시도 잡 상태 전이(RETRY_WAITING/DEAD_LETTER)와 delivery 멱등
- [036·037] cache-aside(hit/miss·update eviction·TTL)
- [042·043] outbox 원자 기록과 publish 상태 전이
- [047·048] 정책 matrix(401/403)와 service 경계 enforce
- [052·053] upload 순서(검증→PENDING→저장→READY)와 실패 cleanup
- [057·058] correlation id 전파와 실패 구조적 기록
- [062·063] timeout/retry/circuit 통합 실행기와 open 시 비호출
- [068~082] Go: token bucket 임계구역, server timeout 필드, worker pool 경계, idempotency store
- [086] 드릴 종합(p95 리포트·saga 보상 순서·ledger projection·failover)

#### sportsbook/betting-service (20)
- [001] STI 선택과 불변식(aggregate) vs 정책(validator) 분리
- [003] 멱등 최종 권위=DB UNIQUE(Redis는 가속), CHECK의 SYSTEM 한정
- [005] 불변식/정책/인프라 예외 타입 분리(circuit breaker 거절 미집계 기반)
- [006] slippage 보호 의미와 경계 계산(무반올림 cross-multiplication, 권위=odds-feed)
- [008·009] K-of-N payout(C(N,K)·FLOOR 보수·binomial 안전)과 손 검산
- [010] breaker가 비즈니스 거절을 세면 안 되는 이유, betId=wallet 멱등 키
- [012·013] outbox 이유(dual-write), partition key=userId 근거
- [014] 외부 HTTP 비트랜잭션 orchestrator+짧은 BetStore 트랜잭션, 멱등 2겹
- [016] publisher at-least-once(ack 후 마킹·재시도·replay 보존)
- [018] reconciliation 보상(roll-forward/back/defer, 환불 금지 이유)
- [020] RFC 7807+ErrorCode 매핑, UUIDv7 keyset cursor
- [022] dev-host p99 한계의 정직 기술(하드웨어 경계)
- [024~026] 정산/void consume 멱등·전이 가드·@Version 불변 증거
- [README→014] 접수=동기 orchestration인 이유(분쟁·UX·강한 일관성)

#### sportsbook/wallet-service (16)
- [001] available/locked 2-bucket과 추적 가능성
- [002] double-entry invariant와 UNIQUE(key, side) 설계
- [005] PESSIMISTIC_WRITE 직렬화와 커밋 결속
- [007] 멱등 3층 분담, TransactionTemplate 선택 이유, 4연산→단일 primitive 매핑
- [008] 100 동시 debit race 증명 구조
- [009~011] outbox 원자성·at-least-once·성공/실패 이벤트의 트랜잭션 분리
- [016·017] after-commit invariant vs 시점 방어, 이중 정합성(per-op+배치)
- [019] 부하의 정합성 증명 확장과 hardware bound 판단
- [020] 정산 4결과→leg 매핑과 forfeit 누락 결함의 의미

#### sportsbook/settlement-service (9)
- [README→004] 판정 수학(Π multiplier·Σ line, betting과 대칭)
- [README→008] WON 2-leg payout(단일 credit은 double-entry 파괴)
- [README→009] 2-phase+중복 차단(betId 멱등→payout 0)
- [README→011] 판정 입력 계약(resultDetail, score 재해석 금지)
- [README→014] 동시 재정산 1회 수렴(16스레드→outbox 1행)
- [README→018] 처리량 narrative(엔진 vs wallet 왕복 지배)
- [README→020·021·022] 토픽 .v1 통일 교훈, LOST forfeit 경로, DLQ 24h 윈도우 한계

#### sportsbook/risk-service (8)
- [README→003] sliding window 합 불변식(Lua 원자), check의 TOCTOU 허용 범위, sliding vs tumbling
- [README→005] BLOCK short-circuit 안 하는 이유(호출자별 의미 차이, 순수 fold)
- [README→007] wire 스키마↔내부 모델 의도적 불일치, event sourcing vs HTTP pull
- [README→009] constant-arrival-rate 1000 RPS 선택 근거
- [README→011] command vs connect timeout 분리(콜드스타트 오탐)

#### sportsbook/odds-feed-service (18)
- [README→000·001] library vs application, List vs Stream, sealed 이벤트
- [README→002] 평균회귀 시세(발산·예외 방지)
- [README→003·004] YAGNI 추상화 기준, 결정론 UUID 유도
- [README→005] write-through non-atomic 허용 근거(멱등·정정), enum 이름 저장
- [README→006] Avro Instant 전역 등록, BigDecimal 경계, partition key=eventId
- [README→007] cache 무조건/publish만 threshold(cache가 canonical), Java 17 instanceof 체인
- [README→008·009] cursor pagination, in-process broker=JVM ceiling
- [README→011~013] commons-pool2 부팅 의존 교훈, 마켓 상태 양방향 캐시, mock 결과 채점 순서
- (외 — README L3 참조)

#### sportsbook/gateway (11)
- [000] servlet 게이트웨이 선택(STOMP 공존)
- [001] 엣지 검증+신뢰 헤더 모델, stateless 선택
- [002] rate limit fail-open과 보안 뒤 배치
- [003] userId 안전 전파(strip+주입+query 덮기)
- [004] 본인 한정 푸시(CONNECT principal=sub)
- [005] 1만 연결 증명 전략(dev=정합성, 규모=Phase 5)
- [006] 토픽 .v1 정렬 — 계약 불일치는 e2e만 검출

#### sportsbook/admin-api (4)
- [001] RS256 구성+alg 고정, 필터체인 순서
- [002] admin context 전파, UUIDv7 사전 생성
- [003] aspect ordering(거부까지 감사), AOP 바인딩 함정, best-effort 이중 박제
- [004] 알고리즘 혼동 공격 방어

#### sportsbook/shared-protocol (12)
- [001] BOM import vs parent 상속, 생성 소스 lint 제외
- [003] long minor units·음수 허용 경계·Math.*Exact
- [004] BigDecimal equals 함정과 compareTo 정합
- [007] sealed+permits 컴파일 타임 닫힘, System(minWins,total) 일반화
- [008] 구조 불변식 vs 도메인 검증 경계, 다섯 그룹이 막는 wire 모순
- [009] ProblemDetail 자체 정의(중립성), 추측성 비대화 회피
- [015] 형태 검증/dedup 책임 분리, printable-ASCII 단일 규칙

#### sportsbook/orchestration (9)
- [002] ADR 승격 기준과 상태 갱신 보존
- [003] Kafka RF=1 위장 장애, 호스트 패키징 전략(ADR-0018)
- [004] additive 오버레이 원리, Promtail 파이프라인
- [005] Kafka 비프록시 이유, 분리 프록시 격리, fail-closed 증명점
- [006] e2e 검증 경계, restart·flush의 결정론
- [007] 단독 그린≠통합 그린 3계층
- [008] 시스템 정체성(동기 접수/비동기 정산 두 경로)
- [009] 횡단 스택 중앙집중 이유

### 클러스터 6 — Kotlin/모바일

#### mobile-foundations-training (9)
- [002] 상태 호이스팅과 recomposition 모델
- [004] sealed UiState+stateIn(WhileSubscribed) 상태 소유(회전 내성)
- [005] 라우트/백스택 모델, 화면의 NavController 비인지, SavedStateHandle
- [006] Entity/도메인 분리와 DAO Flow 단일 진실원천
- [009] 오프라인 우선(캐시 즉시+백그라운드 갱신+실패 보존), main-safety
- [010] 낙관적 삭제와 롤백, 데모 API 비영속 흡수
- [014] 수동 페이징(근접 로드·끝/중복 가드·snapshotFlow)

#### mobile-reliability-training (16)
- [002] 닫힌 상태 집합의 누락 방지
- [006/007] 폼 실패 예방 흐름(차단·매핑·단일 비행)
- [012/013] flatMapLatest 취소의 stale 차단과 WhileSubscribed 소유
- [018/019] 영속 상태 vs 일회성 Channel(회전 재생 차단)
- [024/025] PagingSource 키 종료 규칙
- [030/031] 낙관적 쓰기와 identity-gated 롤백
- [036~038] DB 단일 진실원·write-through·실패 캐시 보존
- [043/044] transient/permanent 매핑과 unique work·백오프
- [049/050] STOMP 프레이밍·callbackFlow 생명주기·dedup
- [055/056] loading>disabled>enabled 우선순위
- [061/062] 지수 백오프와 shouldRetry 안전판
- [067~069] single-flight Authenticator
- [074/075] backoff+jitter 재연결·교차연결 dedup·storm cap
- [080/081] withTimeout과 CancellationException 비-삼킴
- [086/087] online/cache/freshness 전략 결정 표
- [092/093] 가시 window off-by-one 가드·안정 키·재구성 예산

#### sportsbook/mobile-client (17)
- [002] Odds scale-4 equality, Money overflow-exact
- [003] problem+json→ErrorCode 분기, CancellationException 보존
- [004] 단일 비행 refresh(락+토큰 비교), DI 사이클 차단, 발급자 부재 seam
- [005] offline-first SoT, clear+upsert 단일 트랜잭션
- [006] 병합점 단일화, odds 비대칭, last-write-wins 정당성
- [007] 멱등 키 규약, DUPLICATE_BET 양성, ODDS_DRIFT 무부작용
- [009] 핸드셰이크 vs SUBSCRIBE 분리, 지터 백오프, 한 연결=한 flow, connectHeaders 람다
- [011] 키 보관/재사용, 낙관적+롤백 경계, drift→재가격, 세션 게이트 라우팅
- [012] 단일비행 증명 테스트 설계(N스레드→requestCount==1), 재시도=같은 키/재가격=새 키

### 클러스터 7 — AI

#### ai-foundations-training (14)
- [012·013] temperature/top-p/seed 제어와 수치 안정화, 재현/탐색 양면
- [024·025] 검색="내적+정렬" 환원(정규화 cosine), 알려진 벡터 검증 설계
- [028·029] RAG 5단계와 grounding 강제 지점, 결정적 fake 교차 증명
- [036·037] 에이전트 루프 두 종료 조건과 스텝 캡(타협 불가), scripted 모델로 가드 증명
- [040·041] eval 3층과 회귀 게이트(tolerance가 가르는 회귀/흡수)

#### ai-reliability-training (10)
- [008] 세 상태 멱등(absent→in_flight→done)·실패 미캐시, 선기록 순서
- [012] token bucket refill 수식, 부하 하 cost/p95의 emergent함
- [024] 다단계 회계(합·root latency·이중 계산 회피), 가짜 시계 소비
- [032·033] breaker 세 상태+degrade 순서(전부 실패만 outage), open 비호출 증거, Served.tier 관측

#### ai-capstone (5 레포, 35)
- [eval-gate 002~008] eval 타입 소유 경계, 결정 메트릭=바닥/judge=보조, baseline tolerance, ERROR 격리, golden 순환 끊기, 게이트 판정 순서
- [orchestration 002~006] bare handler 재조립 seam, 코어+횡단층 한 줄 본질, AnswerPort 어댑터, 풀스택 e2e 범위
- [rag-agent 006~009] 멱등 키=의도 함수, 두 종료 조건, grounding 게이트, 비종료 trace 200 차단
- [reliability-gateway 002~010] transient 분류 단일 출처, 멱등·retry 공존, 예산 가시화, grounding/guardrail 분리, semantic cache 트레이드오프, 다단계 회계, breaker+chaos 계약 주입, degraded vs outage, 8패턴 순서, 부작용/읽기 분리
- [shared-contracts 002~009] transient vs 결정적 실패 경계, NUL 구분 sha256 파생, 포트 주입 설계, 인용 승격=1차 방어, 종료 타입 내장, 구조 불변식 vs 의미 검증 분담, 키를 바꾸는 것/안 바꾸는 것

---

> 항목 수 합계: 약 370 (대형 레포는 대표 발췌 — 전량은 각 레포 답지 L3 절이 정본).
> 갱신 절차: 답지 L3 변경 → 해당 레포 절 재추출 → 이 파일 갱신 커밋(`docs(interview)` 스코프).
