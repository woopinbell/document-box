# Immutable legacy release 예외 원장

이미 공개되어 object 이동·재작성이 금지된 release 중 현행 [`commit-policy.md`](commit-policy.md)
이전 형식이거나 공개 뒤 발견된 immutable 위반만 기록합니다. 예외는 표에 적은 기존 object와 위반
종류의 보존 범위이며 새 commit, tag와 branch에 적용되지 않습니다.

## Backend Training v1

| 저장소 | release tag object | peeled source cutoff (포함) | learning ref와 tip cutoff (포함) | 등록된 예외 | 후속 엄격 경계 |
| --- | --- | --- | --- | --- | --- |
| `backend-foundations-training` | `foundations-v1`<br>`46171d1254335c1398f5c23d87a122c2e2bb2048` | `189f49548edea71eb17fc92acf3059daa089d6f3` | `learning/foundations-v1`<br>`d7f50a1e08c08892c5af8704971fe6b15091acc5` | 일부 source prefix의 raw identity·message가 현행 형식 이전이며 v1 corpus가 구 ledger 형식을 사용 | `foundations-v2`의 첫 신규 source object, 신규 tagger와 `learning/foundations-v2`의 신규 publication object 전체 |
| `backend-delivery-training` | `delivery-v1`<br>`60d0f8dc26b6ca36e176fc3a315da1884096942b` | `66b095b7bf34a114b99f14ea80bd75763ef60eed` | `learning/delivery-v1`<br>`bf1a84e6eecd4544676a71ea7143b01a01b18a4d` | 공개 v1 corpus의 구 형식과 path 구성 | 두 cutoff는 고정하고 다음 source release의 첫 신규 object부터 전부 |
| `backend-reliability-training` | `reliability-v1`<br>`7902d50106b40c1673a09f44f43c1c9a53b15eea` | `a28ad09ceea9bc28a1321601ff4202816ac00775` | `learning/reliability-v1`<br>`c4b34b46e3024f4f9ccef8b3c884184763622680` | 일부 source prefix의 raw identity·message가 현행 형식 이전이며 v1 corpus가 구 ledger 형식을 사용 | `reliability-v2`의 첫 신규 source object, 신규 tagger와 `learning/reliability-v2`의 신규 publication object 전체 |

세 v1 tag와 learning branch는 이동·재작성·삭제하지 않습니다. V2 learning은 v1 자료를 같은 저장소
안에서 byte-for-byte carry-forward할 수 있지만, 새 V2 crosswalk·답지·문제지는 현행 metadata, path,
mapping과 수량 규칙을 따라야 합니다.

각 행의 source cutoff는 release tag가 peel되는 commit, learning cutoff는 기록 당시 공개 learning ref의
tip입니다. 등록된 예외 object 집합은 tag object 자체와 두 cutoff에서 도달 가능한 기존 object로
한정합니다. 이후 ref가 새 object를 가리키더라도 그 object가 이 표의 cutoff에서 도달 가능하지 않으면
예외가 자동으로 확장되지 않습니다.

## 42 codex-5.6의 공개 후 미래 timestamp

2026-07-14 KST 감사 시점에 아래 `codex-5.6` release는 이미 원격에 공개됐지만 일부 신규 commit과
tagger timestamp가 감사 시점보다 뒤인 2026-07-17~21 KST에 놓여 있습니다. 공개 object를 실제 시각에
맞추려고 재작성하지 않고, 이 원장은 **actual-time 배정 위반만** 예외로 등록합니다. Raw identity,
message, trailer, tree, path와 topology에는 이 예외를 적용하지 않습니다.

| 저장소 | release tag object | main = peeled source cutoff (포함) | learning ref와 tip cutoff (포함) |
| --- | --- | --- | --- |
| `linux-admin` | `codex-5.6`<br>`2e2fa5a96df1a1149037d44349722944c419f679` | `903ec4ef9343871f36c1dbd5afcb1cc45b91170e` | `learning/codex-5.6`<br>`a946c3faaa0f727be2b1943ec082b05d30053b36` |
| `format-printer` | `codex-5.6`<br>`9bc7af199e125579a1c641512800c4d3d8a7dd53` | `021b9c774738f6d276600cc6369a925e0e0b2e0d` | `learning/codex-5.6`<br>`54a69feb296fb4c8d79ab4a7ad4f0e6f4ee7800c` |
| `signal-message-bus` | `codex-5.6`<br>`1fc1bb20ac04d118d9d3445de8917d9ed9b3dd25` | `be03a332bca5a866a445c53f044e7f07382d9ed7` | `learning/codex-5.6`<br>`74fa7647149006dab58a6d0db639a5ea540255e7` |
| `thread-dining` | `codex-5.6`<br>`9c5432b9af9f82b9ef79f4f53eb23a08d29eeb0e` | `c8a5b2485fc616c54a8759a76d18334637682ba5` | `learning/codex-5.6`<br>`0f128cb669caa53f4d239cee7079981557920e3b` |
| `small-shell` | `codex-5.6`<br>`16529accf835ac4cfcc0372fc2946d5195b97fef` | `3e25f6430b70df68896c46c9a310ca37dbc4d13f` | `learning/codex-5.6`<br>`6af122bd5c4219c8496975d8f5098ba432420b09` |
| `stack-sort` | `codex-5.6`<br>`ecc65f819d696c5aaaa61e9701be3bec6ceb5182` | `5d848093d7896df1d9525b3994ef07f2420d5255` | `learning/codex-5.6`<br>`c35154f879b974f09fd6a2ae7e5cfffd7a26e423` |
| `stl-container` | `codex-5.6`<br>`f3f665dc25666248bc573c9b46aa59f5ec9408a9` | `e5d04ef059f94b3910a5ed7d3e79aded5008d427` | `learning/codex-5.6`<br>`76bf9c6239a490b85b15db2f3603897a97f397b7` |
| `irc-relay-server` | `codex-5.6`<br>`b11e067747ea8c2b835af4b5cf428fd098aba4b9` | `6c76d8456a1acbd187904d2d0d5b4776ea70e93a` | `learning/codex-5.6`<br>`307d67bb354f891466c5065e1c8d54896ba51efb` |
| `container-stack` | `codex-5.6`<br>`3d58131bee387959618e2f5a5d230333994241d8` | `ebf91b37bc1633c9c31167bb782a55c236ac4595` | `learning/codex-5.6`<br>`1e47145a752afac9583ef7a156ab39ffb443a8f5` |
| `pong-pong` | `codex-5.6`<br>`437ed54c9e853aa60b6eb08a8683a80bd4f73707` | `b949bbeabf7c93d1a3c7acc0cfd6b1230486a79f` | `learning/codex-5.6`<br>`984b1235ab80300f223092fe36b80482311d8c1e` |

표의 tag와 learning ref는 이동·재작성·삭제하지 않습니다. 기록된 main tip object도 재작성하지 않으며,
후속 release가 정책에 따라 main을 전진시키더라도 위 object의 예외 범위는 늘어나지 않습니다. 각 행의
tag object, peeled source cutoff와 learning tip cutoff에서 도달할 수 없는 신규 object는 실제 작업
시각을 포함한 현행 정책을 예외 없이 따라야 합니다.

## Sportsbook 공개 legacy 경계

아래 최신 release는 현재 ref 전체를 예외로 두지 않습니다. Source prefix의 raw metadata, 특정
`docs(notes)` commit의 path, 이미 공개된 미래 timestamp처럼 감사에서 식별한 위반만 정확한 object에
등록합니다. 표의 release tag와 learning ref는 이동·재작성·삭제하지 않고, 기록된 main object도
재작성하지 않습니다.

| 저장소 | 최신 release tag object | main = peeled source cutoff (포함) | learning ref와 tip cutoff (포함) | 등록된 예외와 마지막 object | 예외 없는 경계 |
| --- | --- | --- | --- | --- | --- |
| `sportsbook-shared-protocol` | `shared-v1`<br>`bd3ab9cb9df9ddce51aecd32008b8844781a184c` | `e0754c3a68ddce4f9ddef00e3dfb26b3ce53adbb` | `learning/shared-v1`<br>`415bd8165e66fe8a83a32b4855f43038577a6eac` | Root부터 `0e55264294c4cc7a0de7de9f19d068ac8dfc87b9`까지 17개 source commit의 noreply raw email과 현행 3-section 이전 message 형식 | `e55aae226f786cf69acaefbbe52853be1e4192e4`부터의 source suffix, tagger와 learning publication |
| `sportsbook-wallet-service` | `wallet-v1.0.1`<br>`836c6b6823ae09ceca3ee7b0974f7752f08ef3f9` | `04c0c9706ed16ae6ba763aadd02d8eddd6bde536` | `learning/wallet-v1.0.1`<br>`dacb59158a50897c4de93ff780663862ce0ab407` | Root부터 `861e06a16d4bc7c1249f07aea5c5202c14e93f9a`까지 22개 source commit의 noreply raw email과 현행 3-section 이전 message 형식. 감사 시점 뒤 timestamp로 이미 공개된 `6ae4a5f117ad49329e3aa57cae36bc91ef51f6d7`, `dacb59158a50897c4de93ff780663862ce0ab407`의 actual-time 배정 | `531d4fc1994fd18ebbeac818b36efc67a69e8211`부터의 source suffix와 두 명시 commit의 timestamp 외 모든 속성. 신규 object 전체 |
| `sportsbook-betting-service` | `betting-v1`<br>`978da92ea9cafa5297fb3fdfa0eb7ee88f9680b0` | `a4009f118b77f6739b591a3c2f87dcfd98c03c21` | `learning/betting-v1`<br>`4384d307461be43d3ae4761a8de60615a2594336` | Root부터 `b1de1069838e91a5a8ae1b280aea28d3b7451ee5`까지 28개 source commit의 noreply raw email과 현행 3-section 이전 message 형식 | `bb21719c15ab4ad85bb200c5a6e07ebfb1fbdbe2`부터의 source suffix, tagger와 learning publication |
| `sportsbook-odds-feed-service` | `odds-v1`<br>`763408693cf5277a3975dc56edeebb554237dfea` | `72316d951cc7e289ba2da04ef441ae94474c5009` | `learning/odds-v1`<br>`be22dd966b7105023df38ff111c734dbd74b73d9` | `docs(notes)` commit `8d1e7a420c54f6903eedf4ba81cb9bd71a910c1f`가 보존한 `load-test/**` 7개 path의 notes allowlist 이탈 | 명시 commit의 7개 path 외 source와 learning object의 metadata·message·path 전체 |
| `sportsbook-settlement-service` | `settlement-v1`<br>`ec83a25fe46716df48b2ac4922d269299febc780` | `b117d7f71540f3bbd0586a07205634b0a7bf6a28` | `learning/settlement-v1`<br>`a23f46df36b99ac4a016d8f2950ac4dd7f3af61e` | `docs(notes)` commit `891cf6392f93d451f5bd46361ab0a43798b0f212`가 보존한 `load-test/**` 27개 path의 notes allowlist 이탈 | 명시 commit의 27개 path 외 source와 learning object의 metadata·message·path 전체 |
| `sportsbook-gateway` | `gateway-v1`<br>`ad65e266880ff10dd3ed6f9c5e406fe6fdb02713` | `e955ee6ecf0e6b63d31bacfefc8657ff72271b8e` | `learning/gateway-v1`<br>`912d87afc12516313f8ce320581fde77c8f89a60` | Root부터 `95affea7979213ad16468cee0224e8a393f8715f`까지 8개 source commit의 noreply raw email과 현행 3-section 이전 message 형식 | `c2d247bc9974ad1dd2bebeb134cd27ea3084e463`부터의 source suffix, tagger와 learning publication |

Wallet의 미래 시각 예외는 위 두 learning commit의 timestamp에만 적용합니다. Odds와 Settlement의
path 예외는 controlled load evidence를 byte 보존한 명시 commit에만 적용하며, 이후 `docs(notes)`가
`load-test/**`를 다시 변경할 권한을 주지 않습니다. `sportsbook-admin-api` 최신 release는 감사에서
현행 정책을 충족했으므로 등록하지 않습니다.

### Pre-policy Sportsbook release tag

아래 과거 release ref는 최신 release를 만들기 전에 공개된 복구 경계입니다. Annotated tag는 tag
object와 peeled commit을 함께 고정하고, lightweight tag는 target commit 자체를 고정합니다. 과거
learning ref가 없는 release에 현행 topology를 소급해 만들지 않으며, 이 표는 source·corpus의 추가
metadata 예외를 만들지 않습니다.

| 저장소 | 불변 과거 release | tag object 또는 lightweight target | peeled commit | 불변 learning ref와 tip |
| --- | --- | --- | --- | --- |
| `sportsbook-shared-protocol` | annotated `v0.1.0` | `1e43d18430cada6d7bbb2468d430ffa9c7a231b5` | `ee28c65b761faea0923ce6a7fa1f1f509911b2be` | 없음 |
| `sportsbook-wallet-service` | annotated `wallet-v1` | `89afc07a1886426ce8d68bdae3c99f650fbf98b7` | `0f28d668856d702c1bcea90e1a42bd43871c0a9f` | `learning/wallet-v1`<br>`009de12feb4dc99410dddb08469d9261e4a3ffcf` |
| `sportsbook-betting-service` | lightweight `v0.1.0` | `ab72c3675f5d158d15c352923da493ac06538b16` | `ab72c3675f5d158d15c352923da493ac06538b16` | 없음 |
| `sportsbook-odds-feed-service` | annotated `v0.1.0` | `3160af580da8a8c5426176c211e2565e33823361` | `8e97109c7ad7864d4a8b7c13f619a80ee3a0dfa9` | 없음 |
| `sportsbook-gateway` | annotated `v0.1.0` | `5525804e8036b9a2da6c633120a3fd94c57187af` | `78251a94b1d33b73411fa93e33dc83f411416c49` | 없음 |

이 ref들은 이동·재작성·삭제하지 않습니다. 후속 최신 release와 learning ref에 대한 준수 여부는 위
Sportsbook 최신 release 표의 object별 경계를 적용하며, pre-policy tag가 있다는 이유로 예외를
확장하지 않습니다.

## 감사 방법

1. 등록 release tag object와 peeled commit, learning tip을 원격에서 읽습니다.
2. 해당 old ref가 이동하지 않았고 기존 corpus blob OID가 보존됐는지 확인합니다.
3. 후속 release의 첫 신규 commit부터 raw identity, timestamp, message, tagger와 path allowlist를 전수
   검사합니다.
4. 원장에 없는 불일치는 legacy로 소급 분류하지 않고 정책 실패로 처리합니다.

위 표에 등록하지 않은 42·Frontend·Backend release에는 이 원장의 metadata, corpus, path 또는
actual-time 예외를 적용하지 않습니다.
