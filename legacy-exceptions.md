# Legacy object·migration 예외 원장

이 문서는 migration 전 공개 object의 실제 상태와 승인된 전환 경계를 기록합니다. 아래의 기존 release
표는 old ref를 식별하기 위한 **pre-migration evidence**입니다. 표에 남아 있는 `immutable`, learning
byte 보존 또는 release별 learning branch 문구는 해당 시점의 정책을 설명할 뿐, 아래 migration 대상
ref의 현재 실행 지시가 아닙니다.

## 2026-07 전 트랙 source·learning 정렬 migration

기존 27개 프로젝트의 source provenance와 timestamp를 정화하고, 신규 3개를 포함한 30개 curriculum의
source history와 단일 `learning/current` 진입점을 만드는 일회성 승인입니다. 이 절은 등록된 대상 ref에
한해 아래 모든 legacy 표의 source object 불변, learning ref 불변과 corpus byte 보존 선언보다
우선합니다.

- 실행 순서는 기존 42 10개 → Frontend 5개 → Backend 12개이며 한 저장소의 source, 집필,
  publication과 fresh-clone을 끝낸 뒤 다음 저장소로 이동합니다. 원격 mutation은 병렬화하지 않습니다.
- 기존 source는 root부터 patch·parent·책임 순서를 보존해 replay하고 아래 `sourceWindow`로 timestamp를
  다시 배치합니다. Learner navigation-only commit은 source graph에서 제외합니다.
- 실제 source·test·build·reference 수정은 characterization과 green gate를 거쳐 역사적 책임 위치에
  통합합니다. 무관한 기능 변경이나 commit 수를 맞추는 재분할은 허용하지 않습니다.
- Source ref·tag·metadata·tracked artifact의 금지 provenance를 제거하고 42의 source baseline tag는
  annotated `v1.0.0`으로 교체합니다. Frontend/Backend의 current 의미 기반 release 이름은 유지합니다.
- 기존 learning branch 중 어느 하나도 이름·날짜·tip만으로 자동 선택하지 않습니다. 모든 후보의
  tip·tree·path·blob matrix를 만들고 동일 blob은 한 번만 판정합니다. 완전 포함관계면 final source와
  호환되는 유효 상위 corpus를 기준본으로 삼고, divergent 후보는 source 호환성, commit coverage,
  link·metadata 정확성과 유효한 고유 내용 순으로 판정합니다. 전담 집필자와 저장소 담당자는 신규·변경·
  고유·충돌 파일만 한 번 직접 읽은 뒤 `learning/current`를 발행합니다. Blocker 수정은 해당 파일·hunk만
  재검토합니다. 이미 더 강한 전수 집필·검토로 완료한 `format-printer`는 다시 작업하지 않으며 이 절은
  남은 26개 기존 프로젝트에 적용합니다.
- 기존 `learning/*`는 발행과 검증 뒤 모두 삭제합니다. Learning ref와 learning-only object를 bundle,
  preservation tag 또는 archive subtree로 보존하지 않으며 GitHub garbage collection 뒤 복구할 수
  없음을 destructive approval에 명시합니다.
- Rollback artifact는 정확한 source ref만 포함한 source-only bare snapshot과 bundle입니다. Push와
  fresh-clone 검증이 끝나면 삭제합니다.
- 아래 정확한 원장이 완성되지 않은 저장소에는 이 절이 force-push, tag 이동·삭제 또는 branch 삭제
  권한을 주지 않습니다.

### 저장소 실행 원장

```text
repository / remote / sourceWindow
source ref / expected-old main / replacement main
old source tag object·peeled SHA / new source tag object·peeled SHA / 삭제 ref
old learning refs·tips·trees / new learning/current tip·tree
source-only snapshot·bundle / bundle SHA-256 / bundle verify·restore 결과
destructive approval 근거 / 실행 시각 / fresh-clone 결과 / bundle 삭제 확인
```

Rewrite된 source commit마다 다음 crosswalk를 둡니다.

```text
old commit / old parent(s) / old tree / old timestamp
new commit / new parent(s) / new tree / new timestamp
patch-id 또는 blob·path 동일성 근거
제거한 provenance / 통합·제외한 책임 / 실제 변경 path / 검증
```

Learning 후보 파일마다 다음 disposition을 둡니다. 본문 bytes는 원장에 복제하지 않습니다.

```text
old learning ref / old tip / old tree
stable ID / old path / blob OID / 채택·대체·폐기 / review mode
final source basis / 판단 근거 / reviewer / review 시각
```

`review mode`는 동일 blob과 source crosswalk를 기계적으로 채택한 `oid-identical`, metadata hunk만 한 번
검토한 `metadata-only`, 신규·고유·충돌·source 영향 본문을 한 번 직접 검토한 `direct-content` 중 하나로
기록합니다.

제품 기능상 AI 식별자가 필요한 source allowlist가 있으면 저장소, 정확한 path·token, 제품상 이유와 검토
근거를 저장소 실행 원장에 좁게 등록합니다. 등록이 없으면 allowlist는 0건입니다.

위 learning diff 최적화는 development/source surface의 AI provenance 제거 범위를 바꾸지 않습니다.
`main`, 개발 source ref, source release/tag와 그 reachable graph는 금지 provenance 0건이어야 합니다.
`learning/current`와 기존 `learning/*`, `document-box/main`, `central-notes/main` 본문은 이 제거 대상에서
제외되며 canonical identity와 trailer 금지 규칙만 그대로 적용합니다.

### 승인된 source window

날짜는 모두 Asia/Seoul `+09:00` 기준이며 양 끝 날짜를 포함합니다. `extensionEnd`가 있는 신규 프로젝트는
품질 gate에 필요한 책임 단위가 기본 종료일까지 끝나지 않을 때만 연장 구간을 사용합니다.

| 트랙 | 저장소 | sourceWindow | extensionEnd |
| --- | --- | --- | --- |
| 42 | `c-foundation` | 2023-02-20–2023-03-24 | 2023-04-07 |
| 42 | `format-printer` | 2023-03-28–2023-04-14 | — |
| 42 | `buffered-line-reader` | 2023-04-17–2023-05-12 | 2023-06-02 |
| 42 | `signal-message-bus` | 2023-07-19–2023-08-04 | — |
| 42 | `thread-dining` | 2023-09-13–2023-10-07 | — |
| 42 | `small-shell` | 2023-09-25–2023-12-27 | — |
| 42 | `stack-sort` | 2023-10-09–2023-11-12 | — |
| 42 | `cpp-foundation` | 2023-11-13–2024-02-23 | 2024-03-15 |
| 42 | `stl-container` | 2024-02-28–2024-04-11 | — |
| 42 | `irc-relay-server` | 2024-04-08–2024-07-16 | — |
| 42 | `container-stack` | 2024-07-24–2024-09-10 | — |
| 42 | `web-boundary-inspector` | 2024-07-29–2024-08-04 | — |
| 42 | `pong-pong` | 2024-08-05–2024-11-13 | — |
| Frontend | `frontend-foundations-training` | 2025-02-01–2025-05-03 | — |
| Frontend | `frontend-delivery-training` | 2025-05-04–2025-05-09 | — |
| Frontend | `cloud-launch-training` | 2025-05-10–2025-05-16 | — |
| Frontend | `frontend-reliability-training` | 2025-05-17–2026-01-16 | — |
| Frontend | `portfolio-site` | 2025-10-06–2025-11-28 | — |
| Backend | `backend-foundations-training` | 2024-11-01–2025-01-31 | — |
| Backend | `backend-delivery-training` | 2025-02-01–2025-02-14 | — |
| Backend | `backend-reliability-training` | 2025-02-15–2025-08-15 | — |
| Backend | `sportsbook-shared-protocol` | 2026-02-02–2026-02-15 | — |
| Backend | `sportsbook-wallet-service` | 2026-02-16–2026-03-01 | — |
| Backend | `sportsbook-risk-service` | 2026-03-02–2026-04-05 | — |
| Backend | `sportsbook-odds-feed-service` | 2026-03-23–2026-04-12 | — |
| Backend | `sportsbook-betting-service` | 2026-04-01–2026-04-26 | — |
| Backend | `sportsbook-settlement-service` | 2026-04-13–2026-05-03 | — |
| Backend | `sportsbook-gateway` | 2026-04-30–2026-05-10 | — |
| Backend | `sportsbook-admin-api` | 2026-05-08–2026-05-17 | — |
| Backend | `sportsbook-orchestration` | 2026-05-15–2026-07-14 | — |

서로 다른 저장소의 window가 겹치는 것은 승인된 병렬 개발 표현입니다. Learning과 governance commit에는
이 표를 적용하지 않고 실제 집필 시각을 사용합니다.

### 기존 표의 효력

아래 표의 SHA, tag와 오류 설명은 old↔new crosswalk를 만들기 위한 입력입니다. 저장소 실행 원장에
replacement ref와 destructive approval이 기록된 순간 해당 행의 “이동·재작성·삭제 금지”와 learning
byte 보존 문구는 그 ref에 대해 효력을 잃습니다. Migration에 포함되지 않은 object에는 기존의 좁은
예외 경계가 계속 적용됩니다.

## Cloud Launch pre-release preservation boundary

`cloud-launch-training`의 공식 release 이전 혼합 `main`은 annotated
`pre-cloud-launch-v1` tag object `b04d2ca9bfca65dd3412bd8e1d08d4a08b056069`가 peeled commit
`a87a61061e084bb05fa00f6ccff34d0d9c9128a0`으로 보존합니다. 이 ref는 복구 경계일 뿐 공식
release나 학습 진입점이 아닙니다.

기존 source prefix는 root `1ad172b8865e7b62ee15d45ac5d60666faa40369`부터
`ba661bd846f327b5a1180a1951ba967bbb2cd2a1`까지 14개 commit입니다. 이 객체들은 raw identity,
timestamp와 3-section message를 포함해 현행 정책을 충족하므로 metadata 예외를 등록하지 않습니다.
첫 strict replay object는 `8351231456de14562b92c06bf06194362bd61e50`이며, 이후 신규 source와
publication object 전체에 현행 정책을 적용합니다.

공식 annotated `cloud-launch-v1` tag object는
`a2b68bd0c0cda5f20db8f641add436ba86a05375`, peeled source는
`4c6dd0b7a6405ebf6776879450cf67eb20945dba`, 단일 immutable
`learning/cloud-launch-v1` tip은 `94a69c837a53cb01ac0e29f25fd728517719d2de`입니다. 기존 혼합
publication은 pre-release tag에서만 도달하고 새 release의 source 또는 learning path 예외로
확장되지 않습니다.

## Cloud Launch v1 immutable corpus basis 오류

Annotated `cloud-launch-v1` tag object
`a2b68bd0c0cda5f20db8f641add436ba86a05375`와 peeled source
`4c6dd0b7a6405ebf6776879450cf67eb20945dba`, 당시 immutable로 운영한
`learning/cloud-launch-v1` tip `94a69c837a53cb01ac0e29f25fd728517719d2de`가 pre-migration 기준점입니다.
상위 migration 승인 뒤에는 old learning ref를 삭제하고 disposition만 남깁니다.

Stable ID `012`의 실제 source object는
`37c5dfb95c3bff4e3f488d6db52c906092cc3853`, tree는
`ce5382acb90a347d44ee22d27e70d0b54f5be66c`, parent는
`e644946819a3f4e9e342fa60e4319e9882dafa9c`입니다. 존재하지 않는
`37c5dfb95c3bff4e9e342fa60e4319e9882dafa9c`가 아래 immutable corpus 필드에 기록됐습니다.

| publication object | path | 잘못된 필드 |
| --- | --- | --- |
| `9403474fb8c7a18a75133f1bf8e6a3a1125f58a1` | `docs/commits/012.md` | 기준 commit |
| `9403474fb8c7a18a75133f1bf8e6a3a1125f58a1` | `docs/commits/013.md` | 부모 commit |
| `9403474fb8c7a18a75133f1bf8e6a3a1125f58a1` | `docs/commits/README.md` | ID 012 commit |
| `9403474fb8c7a18a75133f1bf8e6a3a1125f58a1` | `docs/commits/README.md` | ID 013 parent |
| `94a69c837a53cb01ac0e29f25fd728517719d2de` | `docs/practice/012.md` | 기준 commit |
| `94a69c837a53cb01ac0e29f25fd728517719d2de` | `docs/practice/013.md` | 부모 commit |
| `94a69c837a53cb01ac0e29f25fd728517719d2de` | `docs/practice/README.md` | ID 012 source basis |

등록 예외는 위 일곱 필드의 잘못된 literal에만 적용합니다. V1 source graph, tag/tagger, 실제
tree·parent, raw metadata와 나머지 corpus에는 예외를 적용하지 않으며 supplement/fixup learning
branch도 만들지 않습니다.

교정 release는 ID `019` source object
`64750fe6a3e59734c2c320a23178253e9614e7f7`에서 실제 Git object 검사를 추가하고, ID `020`
`480e18b5b47cccf5fe0f38e6c5811fde567bdfe4`에서 current release 경계를 문서화합니다. Annotated
`cloud-launch-v1.0.1` tag object `20857ee56df971d3a1b5eb7a8cf181377dd971ef`는 ID `020`으로
peel됩니다. 단일 `learning/cloud-launch-v1.0.1`은 release에서 다음 세 commit만 추가합니다.

1. notes: `5c64cfac71dddae0abb04731cf642ad6012f1336`
2. answers: `c4eae9f428b91158e1fd5a06fdbf27d994c20b45`
3. practices/tip: `c13b944e41f7b3cbf4f6949636e2104218dc48a3`

V1.0.1 corpus는 source 20, answers 20, practices 17(`002–017`, `019`), omissions 3(`001`,
`018`, `020`), final reachable 23으로 reconcile됩니다. 잘못된 v1 literal은 새 corpus에 없고 모든
basis/tree/parent가 실제 release object와 일치합니다. V1.0.1의 신규 source, tagger와 learning
publication에는 위 v1 예외를 확장하지 않습니다.

## Backend Training v1

| 저장소 | release tag object | peeled source cutoff (포함) | learning ref와 tip cutoff (포함) | 등록된 예외 | 후속 엄격 경계 |
| --- | --- | --- | --- | --- | --- |
| `backend-foundations-training` | `foundations-v1`<br>`46171d1254335c1398f5c23d87a122c2e2bb2048` | `189f49548edea71eb17fc92acf3059daa089d6f3` | `learning/foundations-v1`<br>`d7f50a1e08c08892c5af8704971fe6b15091acc5` | 일부 source prefix의 raw identity·message가 현행 형식 이전이며 v1 corpus가 구 ledger 형식을 사용 | `foundations-v2`의 첫 신규 source object, 신규 tagger와 `learning/foundations-v2`의 신규 publication object 전체 |
| `backend-delivery-training` | `delivery-v1`<br>`60d0f8dc26b6ca36e176fc3a315da1884096942b` | `66b095b7bf34a114b99f14ea80bd75763ef60eed` | `learning/delivery-v1`<br>`bf1a84e6eecd4544676a71ea7143b01a01b18a4d` | 공개 v1 corpus의 구 형식과 path 구성 | 두 cutoff는 고정하고 다음 source release의 첫 신규 object부터 전부 |
| `backend-reliability-training` | `reliability-v1`<br>`7902d50106b40c1673a09f44f43c1c9a53b15eea` | `a28ad09ceea9bc28a1321601ff4202816ac00775` | `learning/reliability-v1`<br>`c4b34b46e3024f4f9ccef8b3c884184763622680` | 일부 source prefix의 raw identity·message가 현행 형식 이전이며 v1 corpus가 구 ledger 형식을 사용 | `reliability-v2`의 첫 신규 source object, 신규 tagger와 `learning/reliability-v2`의 신규 publication object 전체 |

Pre-migration 정책은 세 v1 tag와 learning branch를 고정하고 V2 learning에서 v1 자료를
byte-for-byte carry-forward하도록 허용했습니다. 상위 migration 실행 시 이 문장은 보존 지시가 아니며,
각 source tag는 provenance·release disposition에 따르고 old learning branch는 삭제합니다.

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

이 표는 당시 learning ref와 source tag/main tip을 고정했던 상태를 기록합니다. 상위 migration 실행
원장에 old/new object, source-only bundle과 승인이 등록된 행은 source tag 교체·삭제, main replay와 old
learning ref 삭제를 수행합니다. Learning corpus는 disposition metadata만 남기며 bytes를 보존하지
않습니다. Migration 범위 밖 object에는 표의 좁은 과거 경계만 적용합니다.

## Sportsbook 공개 legacy 경계

아래 최신 release 표는 source prefix의 raw metadata, 특정 `docs(notes)` commit path와 당시 미래
timestamp처럼 감사에서 식별한 위반의 pre-migration 위치를 기록합니다. 상위 migration 승인 전에는
이 SHA들이 기준점이었으며, 승인 뒤에는 source/tag disposition과 old learning 삭제가 상위 절을
따릅니다.

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

Pre-migration 정책은 이 ref들을 고정했습니다. 상위 migration 실행 시 source tag는 provenance와
release disposition에 따라 유지·교체·삭제하고, 표의 old learning ref는 삭제합니다. Pre-policy tag가
있다는 이유로 metadata나 path 예외를 다른 object에 확장하지 않습니다.

## 감사 방법

1. Migration 전 remote main, release tag object·peeled commit과 모든 learning tip/tree를 읽습니다.
2. Source-only bundle이 learning ref를 포함하지 않는지, verify와 restore가 성공하는지 확인합니다.
3. Old/new source commit의 parent, tree, patch, timestamp와 provenance disposition을 전수 대조합니다.
4. 기존 learning 후보 전체의 tip/tree/path/blob OID와 채택·대체·폐기 판단, final basis와 reviewer가
   기록됐는지 확인합니다. 동일 blob은 disposition을 공유할 수 있으며 신규·변경·고유·충돌 파일의 1회
   직접 검토와 blocker 대상 재검토만 요구합니다.
5. 승인 뒤 remote branch가 프로젝트는 `main`·`learning/current`, governance는 `main`만 남는지
   확인합니다. 삭제한 learning corpus는 blob 보존 여부를 검사하지 않습니다.
6. New source commit/tagger의 identity, sourceWindow, message, path와 provenance를 검사하고,
   `learning/current`의 publication path·실제 시각·수량을 검사합니다.
7. 원장에 없는 불일치는 legacy로 소급 분류하지 않고 정책 실패로 처리합니다.

아래 표에 등록하지 않은 object에는 metadata, corpus 또는 path 예외를 적용하지 않습니다. 전 트랙
migration을 완료한 저장소에는 최상위 migration 절과 저장소 실행 원장이 정본이며, 아래 pre-migration
표를 이유로 삭제한 ref를 복원하거나 다른 learning branch를 다시 만들지 않습니다.
