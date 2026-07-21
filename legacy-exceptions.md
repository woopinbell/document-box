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

- 실행은 두 lane으로 나눕니다. 42 lane은 기존 42 저장소를 현재 순서로 정리한 뒤, 두 lane의 기존 27개
  정리가 모두 끝났다는 barrier를 확인하고 신규 `c-foundation` → `buffered-line-reader` →
  `cpp-foundation`을 각각 개발·집필·publication까지 직렬 완료합니다. Delegated lane은 Frontend 5개를
  순서대로 끝낸 뒤 Backend 12개를 순서대로 처리합니다.
- 두 lane은 소유 저장소가 겹치지 않는 read-only 감사, 격리 source replay, build/test와 learning diff
  작업을 병행할 수 있습니다. 한 저장소의 source → freeze → 단일 집필자 → publication → fresh-clone과
  각 lane의 저장소 순서는 계속 직렬입니다. 모든 project·governance 원격 mutation은
  `WORKFLOW.md`의 전역 publication slot으로 하나씩만 수행합니다.
- 42 lane은 신규 세 저장소, 42 단계 순서와 최종 30개 수량·전체 navigation 통합을 소유합니다.
  Delegated lane은 기존 Frontend·Backend 저장소와 그 track entry·단계 카드만 수정하며 42 저장소,
  신규 프로젝트, 전체 프로젝트 수와 최종 42 sequence를 변경하지 않습니다. 공유 registry나 governance
  문서는 slot 획득 뒤 최신 `main`에 담당 entry만 다시 적용합니다.
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

### 동결된 format-printer learning publication과 navigation 예외

`format-printer`는 전수 집필·검토를 거쳐 이미 동결됐으므로 learning history를 다시 분할하지 않습니다.
정확한 source 기준은 `main` `be4966f3c1d176453a34b609036ef4998fa8b022`(tree
`359bd26b61fdbb72489deb3f71bc4f67e5a5316c`)이고, annotated `v1.0.0` tag object
`fe7a0d79cb9733f4f6871e5164a305907cd7b78e`는 그 commit을 가리킵니다. `learning/current` tip
`7a271026d6afbec22e8e32c6cfeaf7ac5ae1d777`(tree
`458d900fb3793b6e61cce0121961560c8a4ae08a`)은 source 바로 뒤의 단일
`docs(learning): publish v1.0.0 corpus` commit입니다.

- 이 단일 commit은 실제 frozen tree에 존재하는 `docs/README.md`, `docs/commits/**`,
  `docs/practice/**`, `notes/**`만 변경할 수 있습니다. Versioned duplicate와 source·config·test path는
  허용하지 않습니다.
- 단일 `docs(learning)` role은 위 exact object의 `format-printer`에만 허용합니다. 이후 새 learning
  publication은 전역의 notes → commits → practice 순서를 따릅니다.
- `format-printer`, `signal-message-bus`, `thread-dining`, `small-shell`, `stack-sort`, `stl-container`,
  `irc-relay-server`, `container-stack`, `web-boundary-inspector`, `pong-pong`의 current source release에는
  learner-navigation-only commit을 추가하지 않았습니다. 열 저장소의
  main backlink 부재는 명시적
  예외이며 current ref·학습 진입점은 Document Box 단계 카드가 소유합니다. 이 예외는 각각
  `be4966f3c1d176453a34b609036ef4998fa8b022`/`fe7a0d79cb9733f4f6871e5164a305907cd7b78e`,
  `ed859ce08c0d84154c21be6ffd6cdb1ea1c353c3`/`7563b6325e6c1a31bc63dbf22b935bb155e0e434`,
  `94ccaa4085af3decfd6d7bba2ff0b879954947e5`/`983bb1f4ce52ce33feb68955d9c0788670b12fb4`,
  `0fb1f6bf4825890f7b657ce5de918aed52a8318d`/`3e7164817b3883783c80c6a1ced90531faf85efe`,
  `51325493a5e0e10f72dcfc04079d3b4f2c96488e`/`dc08a9be3ec27a5096be753ef7f7126ce8b713e9`,
  `6f875e0677674d86145188d8558e3cf56b61c9cb`/`d6ff0b12322c9221d47f308097dc4b4980f3b483`,
  `b69347797e81c803397ced1ba23042216caa74fd`/`7c8fe460cd8e4e01ac5c82a5e6e987be7cce58fb`,
  `bd498c17f255681cbc57e598e09a876abb2c0a2e`/`dd878d65945e32c9a499b175643a1ae39880cb3a`,
  `cf57ffeb652288548c351209a278d4907f0b2f95`/`5ee7967b12c27a259d1a64f4c72de67f524c46c7`,
  `e537ffb457bfbb6225c55beb1dd9cb7b7389867d`/`30db31454a16571cdbbb129671ad2d6218a29afa`
  main/tag object 쌍에만 적용하며 어느 object든 이동하면 backlink 검사를 다시 요구합니다.

### `small-shell` 정렬 실행 원장

2026-07-20 KST에 private `woopinbell/small-shell`의 source와 learning ref를 exact lease를 사용한 단일
atomic push로 전환했습니다. Expected-old `main`은
`8b83a05024136f599414e37e76b207bdd7f8f513`이었고 replacement `main`은
`0fb1f6bf4825890f7b657ce5de918aed52a8318d`(tree
`656c3a1e0e3fa404501e0a2382c757670e660f54`)입니다. Annotated `v1.0.0` tag object
`3e7164817b3883783c80c6a1ced90531faf85efe`는 replacement `main`으로 peel됩니다.

Source-only rollback bundle은 old `main`과 아래 여섯 source tag만 담았고 learning ref는 포함하지
않았습니다. Bundle SHA-256은
`684cc16c34b7641501533982aced38b54ec35995ae31d97dda09ab4c41a8ae79`이며 verify, strict fsck와
복원 clone의 일곱 ref exact 대조를 통과했습니다. Project remote publication과 fresh-clone gate가
green이 된 뒤 snapshot, bundle과 restore clone을 폐기했으므로 active ref나 offline 보존본으로
복구할 수 없습니다.

삭제한 source tag의 ref/object/peeled target은 다음과 같습니다.

| ref | old tag object | old peeled target |
| --- | --- | --- |
| `codex-5.6` | `16529accf835ac4cfcc0372fc2946d5195b97fef` | `3e25f6430b70df68896c46c9a310ca37dbc4d13f` |
| `codex-5.6.1` | `cd40c73311a882ebcc5401100d392c8f87f11bb2` | `340456da2599637c759848da65706e7d7c3b6c0a` |
| `codex-5.7` | `7f6f5244891efcdff172613470951dbda42be24c` | `8b83a05024136f599414e37e76b207bdd7f8f513` |
| `pre-codex-5.6` | `cdd9f5d697a078590bd82054ef8e579e2730eb09` | `c9ebf6e378b11a5346d8db939fc97b4567d7b279` |
| `pre-history-clean-codex-5.7` | `9fb9682463e82c0f527aa02bd1423533c9b48e34` | `340456da2599637c759848da65706e7d7c3b6c0a` |
| `pre-learning-split-codex-5.6` | `ec2e9d447362a2ebb9ad4f74cccde7268f11ffd9` | `b9730315b24a71d1c31d6c22cd88a19d48991354` |

Source replay는 old patch 순서와 16개 책임을 보존하고 source window
`2023-09-25`–`2023-12-27` KST에 배치했습니다. 아래 표의 tree·patch 표기 `same`은 양쪽 object가
byte-for-byte 같음을 뜻합니다. Makefile의 progressive build repair가 누적 tree를 바꾼 행도 그
책임의 source patch가 `same`이면 기존 patch를 보존한 것입니다.

| source ID | old commit | new commit | old tree → new tree | patch-id disposition |
| --- | --- | --- | --- | --- |
| `000` | `02dd49b3b95a70db8038756c634678c926e09afa` | `68f812ed16a568198f59d63f578a201cfe56d6d2` | `eebce37a1f7cfc42d85927fc08e7a8a9c42779fa` → same | `27e84a0dd329babca280dc3e224d78a9e044d7ff` same |
| `001` | `a0fd80ed0338474b6ef86bc03c8238a46d4464fd` | `7de0bb7d81de6c8b215ddcbba91c6cc6f7f93c22` | `a2ea801d5af3af94c835fcef730dac75929e7aa9` → `0fc8c25997e2bee51b5cd80f10d059817b5db033` | `6e80be6e82b76ee3c68699a6759417f112fe8c71` → `758fcca1a25556545dd2d8bccc282856c621ceda` |
| `002` | `13d020b180fb8d29f71930be1d681194e308e6f5` | `a8ac47ada9515814f5c075240a298f5f6b03db07` | `abb1e534b14f786c1c42dd31b8967381aae19fa6` → `fd9235c87ed0ec8cedd1774c34a3ed4a308baa65` | `d297a6e0eff28a3339179f5090ef17ac3a7dc1e1` same |
| `003` | `d44fdd013d4bb2f70d7c54cfaa9e50324b944307` | `e4251bbe9995d4716a8b702e031824c0f5608a1e` | `64483c04daab60c779fdfcefd4bcd05e18e43943` → `b33ae344fe66261f8404b975c68f017b69bbeaa8` | `a249cb954dac3030c59a5815db836eaf7274573a` same |
| `004` | `3f0080f6ab4d8959d34105075e9abb1a873b4f31` | `04a86da2100f42ff53a851020a7044df18a7d15d` | `77ab21a890d7a67aa5d4eb6b33e92a78e82f2a32` → `a01d8956406c03b077f7327f283a40c0c4726acb` | `5fa66e6cf7a5cf46424851f4575d12582bbf89ec` same |
| `005` | `16358b56cc8a78efdbd3ab3a5b7d7a712d7f290c` | `32f83bda23c7cabfba2356452020247bc814f329` | `d8a446a09aa5a740a6c8acc3e165dac49557da0f` → `909cba1b9d487f0431e2391958dbfba51035db79` | `940af06a195a3f3f88e80220e763dfefdd9033ad` same |
| `006` | `1a12abf78fe0bfb8edbf710957ee63551c3b4775` | `7187aa05d8a9f7f02f8878697e40bf06a84fa1c5` | `a106c9c307e8d54b31089aa9d13b0d79dcc7ee7a` → `41b37eed629935e20c5394c7bdb79d324ae2ea4a` | `345742007b2d4087e2bc6f211408fd6b45dd7280` same |
| `007` | `6ce670e7bde2a8818073d820ed87a97ad7c3b17c` | `0bed1831b0fe0c54307e45c4fbb42c7cf39420df` | `953e59e96746dc1a6bb768ec25600e4a839dc54f` → `2d59dfe7caa92ec98977241b368e84ae57611f4f` | `a97bc70a9b36ebdb60833f507afe7e000ef75c23` same |
| `008` | `83c8ca0c6e708ce5a0fef7bcfea5b850f7e79042` | `498bebe6e526646ed092fca5b391389a98128c27` | `25b45baa357e0387e46d05124116aa61459e4fe2` → `485a7031c61b2cb37fc6ba1b71b088228e353cd0` | `fa079ce3f0a3d2a90bd4023408f0e701c21e3896` same |
| `009` | `9f53db822082dd8a22c2757496fdc3f6d894fa2c` | `662e7bd8dd5a3e968f03b4c3c2d366249b3f64ab` | `0dba248ff9df3ec4cc68a336f9fe37c7be21ecbe` → `15467d770f1ce9ccc45e55a517bf13743a38a250` | `eddaab3f3ecf36f7bdeaad92b1ec00ece70c3f74` same |
| `010` | `ace1be3c63dfdfbc87a3f2cd5507a7131b9ca5e6` | `105ba8422c5352998137b41f5078d11183950d31` | `21b3f36d2440459e14beaf72796f59c6870a4f71` same | `3b290732e54c252e0189bdfb4aee83fa7020de0f` → `918d0e7d73f9fdaa284cb4ce0e8afc872403926a` |
| `015` | `03a0be74c907c5fc036a429b1a42dd38e19140cd` | `ed06ae2045228c5bc397efa9fdd6e3ee8e049823` | `cf83233d435f77081cc347a2a47dc59ecdc8d890` same | `890bb84900c33bb3fc783cc5ab9ec5c76e88a020` same |
| `012` | `8af7cfd473c3e8f8ed2401b278acbacf646e1561` | `8f4ec5b78a65a2de3fad00a9d2009b1a8b17dcda` | `36baa81ea89ec5f1d833072d90a9eb455c02fc15` same | `3e46237a08080b10372f449fe01ef1c0e6dfd05b` same |
| `013` | `d027bb9faa4ea1b7be433dc289d18cf9f245896b` | `14b1f75475cb16b0ba183a7d2c9bbe04924697f8` | `c4186af4f13db79ae8d427174015327300cf2a37` same | `2549f972f87abc4348370b3a0278c6ed1a6b1b1d` same |
| `014` | `846d5d04ba592d8d5b1802c082538c3e44816d16` | `33f342e75a3b633b7ff43a2e939b65ebef4e5585` | `c72aa65ae635785a3f96f651095bd4772c64cc86` same | `f407b3e5f3f8544f77e3aff193ac15510b207ef2` same |
| `016` | `676b60b002e0c109cd8c51c2dd21809b20916e4b` | `0fb1f6bf4825890f7b657ce5de918aed52a8318d` | `67256970c24e427b7817fe19f981ca7f77da1a72` → `656c3a1e0e3fa404501e0a2382c757670e660f54` | `120c4eefa17655842a6be0d5173c95b37c30974f` → `1bb599f15539b97494c37305f9c653b2fe6abd4d` |

Old final object `8b83a05024136f599414e37e76b207bdd7f8f513`(tree
`6b43f81cacfa0e03ee724f23ca53fba87287ac4c`, patch-id
`e66e745bf6363630e12e8b53c4a0181f2056e24c`)은 source 기여가 없는 learner-navigation-only 책임이라
replay에서 제외하고 stable ID `017`을 reserved 처리했습니다.

Learning 후보는 다음 세 ref였습니다.

| old ref | tip | tree | paths |
| --- | --- | --- | --- |
| `learning/codex-5.6` | `6af122bd5c4219c8496975d8f5098ba432420b09` | `670917acea0a98dcd42190bb8f25b7c34f71ef82` | 97 |
| `learning/codex-5.6.1` | `1f907da4122e1ac4ec3a4307dba2e7dbab5c3ebc` | `1f922fc573dde6dad015d8d3abe68be7a2cafca5` | 100 |
| `learning/codex-5.7` | `90bc14a293e393fb83b3850ddd5a11fbd59391db` | `02c0cc7b8a371553f4c42e2a6208bb49409c1e10` | 112 |

세 후보는 commit ancestor 관계가 아니지만 path set이 5.6 ⊂ 5.6.1 ⊂ 5.7이고 공통 92 paths와
5.6.1 추가 3 paths의 blob이 동일해 5.7을 기준본으로 택했습니다. 84개 legacy Markdown 후보는
contributing 47, discarded/reserved 37로 disposition했고 동일 blob 12개는 재독하지 않았습니다.
최종 corpus는 source 16 = answers 16 + exclusions 0, answers 16 = practices 14 + omissions 2
(`000`, `016`)입니다.

`learning/current`는 source 뒤의 actual-time publication 세 commit
`a2418a623eb5afbdb22ada4f04bbef226a515405`(`docs(notes)`),
`280beb3427206c40ac8fc5ba248605ade21689e1`(`docs(commits)`),
`45d367edb7191ffc1f0165e97e2b069400a583fa`(`docs(practice)`, tip)으로만 구성되며 tip tree는
`e5b66ee99c2b882ee5b7c8e5294ba69b1bc26101`입니다. Fresh clone에서 advertised ref가 `main`,
`learning/current`, annotated `v1.0.0`뿐임을 확인하고 default/readline build·smoke, 두 reference,
source provenance, corpus metadata·H3·links와 source drift zero gate를 다시 통과했습니다.

### `stack-sort` 정렬 실행 원장

2026-07-20 KST에 private `woopinbell/stack-sort`의 source와 learning ref를 exact lease로
전환했습니다. Expected-old `main`은
`e4ea219cd6bd0709f97837d8c3fd8785a6369b42`이었고 replacement `main`은
`51325493a5e0e10f72dcfc04079d3b4f2c96488e`(tree
`1b47a872f322d2e6dbff7989d4ab9ee569879199`)입니다. Annotated `v1.0.0` tag object
`dc08a9be3ec27a5096be753ef7f7126ce8b713e9`는 replacement `main`으로 peel됩니다.

Source-only rollback bundle은 old `main`과 아래 여섯 source tag만 담았고 learning ref는 포함하지
않았습니다. Bundle SHA-256은
`3e8ad03633180cd5c8ea5d20d6380e825b98f7e90a617c3afc930884921b9fd9`이며 bundle verify,
strict fsck, restore clone과 일곱 ref exact 대조를 통과했습니다. Project와 governance publication 및
fresh-clone gate가 green이 된 뒤 snapshot, bundle과 restore clone을 폐기하므로 active ref나 offline
보존본으로 복구할 수 없습니다.

삭제한 source tag의 ref/object/peeled target은 다음과 같습니다.

| ref | old tag object | old peeled target |
| --- | --- | --- |
| `codex-5.6` | `ecc65f819d696c5aaaa61e9701be3bec6ceb5182` | `5d848093d7896df1d9525b3994ef07f2420d5255` |
| `codex-5.6.1` | `66b459110efcf875ac5d2cd2cac770b9f7caf94c` | `10ed0997fc04352b2b8aaf7bcaebe6b8c189b6e1` |
| `codex-5.7` | `fe8221d4d11599c0fba56abd7afa184ecb41928a` | `e4ea219cd6bd0709f97837d8c3fd8785a6369b42` |
| `legacy/codex-5.6-monolith` | `328edc606898e6236f7f1555d75e2069670bce57` | `2b3e91d22c9450f1e949ba0c7dfd9f00970e5d79` |
| `pre-history-clean-codex-5.7` | `822fde027b9229b73be36dccccceeab2208a7b15` | `10ed0997fc04352b2b8aaf7bcaebe6b8c189b6e1` |
| `pre-learning-split-codex-5.6` | `4d49bb2624aed0f15639de2e9d8813399aed0e94` | `c50d15b58a0a071ca0e1692dacc8e1cbd58199b3` |

Source replay는 old patch 책임 순서와 stable ID를 보존하고 source window
`2023-10-09`–`2023-11-12` KST에 23개 commit을 배치했습니다. `exact`는 old/new tree와 stable
patch-id가 모두 같음을 뜻하며, `carry`는 해당 책임 patch는 같지만 앞선 progressive Makefile이
누적 tree에 포함된 경우입니다.

| source ID | old commit | new commit | old tree → new tree | patch disposition |
| --- | --- | --- | --- | --- |
| `000` | `fad4c0630232523490fc28b729abd266f4929821` | `13876678e3139c02cca9ed8fd2da3a2da76ec257` | `e514ea99a6fc3ef3d67e2eccd6553863651ece62` → same | exact |
| `001` | `9932299e85a775e9e26291bef2c851c2e441b7ea` | `d6e7306047c4851156bba535ee519f04cbfa8694` | `4b3923ff38d14766c899a396efde72e71f86314d` → `91368c69c58c96d397692b8225a725dd0cc9be3a` | progressive Makefile |
| `002` | `b7b023962b164b6108e24a392e5f8819d792506a` | `5c33077c7edeb386d3d0ea83c9eeb76ee0f8ad13` | `60b74fd23acee0bfcc7eb887be7ff91552d29888` → `c2b113fc55c122c03fc124f5f4846e56a1740f2b` | carry |
| `003` | `fb15679f8485251d238a9e875dc375c09ffa1792` | `27417c2a1e6a2f07bcb4bbfda0dc70fcf32f34fd` | `dba1fb12ebe6dac3d714d4a2e41c86a7a8bafa4b` → `8e57d1063384b795157cfab6f1c70ba3219693df` | carry |
| `004` | `384643addd3fea2b0dc846678e06eccf8527d4ad` | `124b3ab5d4b0ef5e315e040da93a35fa77d41d30` | `b5f10d1190c368df74ed5dc53e56bde2ac8ea694` → `67d3013264c9b3901825c75c02013f49a8f9f012` | carry |
| `005` | `0b9a9ceebd3b4af70dcf849639b8daa567a88ad7` | `204f19a609a9303f9023095ab5724e125aaa58bf` | `ceb2bf19c90d7c657bc3e74da7deed002b70bbcc` → `7b7e21895fef7b9363a9cf1857c102462107fdb2` | carry |
| `006` | `c7a6f6fd695b4da4748cc06dba9381526a3fefc4` | `524fce413ead8bfc60e40109c2bf66082cded80f` | `3507863db03419f0fff7387d55c726f15d78dd85` → `fb44884777a44687cfa06d7abbb84af7284c373a` | carry |
| `007` | `ca26c8119c3c0a1ace3209dfbc2891e0fbf9aaf1` | `cab2917d39ac7daa10837b4ccec77aeab69e84f4` | `034982dab7383d9130cd870332559d684953ee60` → `9cf4b7bf7dbee8bf8b1cdbed8175dbd0c1f8bd34` | carry |
| `008` | `d906d701f9ca2b19c3533772f5f9fd5b8937b595` | `7aa47108ec559560b3a350ce11c22baf2e67cf1e` | `40d5d71bbdb424a9385228944bdff05dc87a8eac` → `369131932a15a6872b70030795087876c25c5a3f` | carry |
| `009` | `319b98368a88a238746acbbdf2204277400c9b26` | `2ab2adeb49644fa9995ac251fe763936bf91371e` | `1d25d9449128bb876100cd2b023873c3eeafc87e` → `631269f677bab9ef9595e3d07f1e6bb631e9391b` | carry |
| `010` | `392342dd3d464a43f1ee1a3dcaa3825d2a726b7a` | `4151d76ddbf1a10e69660542a29ded0d541ecbb2` | `f3e45dcfebe482db958a9ea77925b012c4fe879f` → `f00cb605348126382edb5800e409a23fe4731f35` | carry |
| `011` | `b3d62e9f2868b485980ac508a11b1993d01cb67f` | `1ff025aaea55a4179813452907ee7acce6eaf540` | `1297402641a39b8ba3283f27ef71badc01bffb48` → `aa0f575d7d4bc7f7ce9faf760bc2cc122ab539c4` | carry |
| `012` | `73916c7c065913bd996bd085dc1727a7309adbd7` | `57e8db3d2f2ed86d43a5852c9a4786b7e01ee9fc` | `c8dbf3d7d5d69510297f5b051a2afde5d4734b36` → `a34272b318164b9e5e0848f60d692373ce77ff15` | carry |
| `013` | `d654fccca12a15437a983dc711778a16b53e64a7` | `8db2bfaf9aee27c0f8e5220f1a729978a3610b50` | `0491f1d943e896ef9c95e2cdf0eb3679bd83bf9c` → `f4a95bc94a4938c4a41e1aa8d80124cfb10abed0` | carry |
| `014` | `2f7bd12809ea89f79047b5af597c51b16ddb57b9` | `bc1e0b8e368d46bfb1e6265667bcacd6f718b035` | `add7271d13ed662d3294fa240bd91215ee8e48f2` → `c6758fa5e362a495a86d1230bc695df3a0e3a1ec` | carry |
| `015` | `a4832a636916573d64a774a8c270f2f181696fed` | `d0eb77c17a82c456aa85b78d7a704a34644a8126` | `9fe42766a77afb5a03e7f9b95e6fe9bbac4fa4e3` → `2b3a1a22bbb6ab3dc0eaa8af74273bdf5cbc02d7` | carry |
| `016` | `722f378f6d4fa6185edae3143ebb6e055fd372a7` | `79d4206fc808abf64ed057501147d8daf0824112` | `754488282a9e53efff419e02da03645a01b14140` → same | strict Makefile convergence |
| `017` | `5a9f8c4c7d4e81e0c1176b8393502b7c3ca117a7` | `db718e2f1880fb5fccec3a02c78891d21d5bd561` | `707f4338bfc5d0a468a010992c7dd887ebe484ba` → same | exact |
| `018` | `f0ccb19173c8610c605cdd66786444d50363fe16` | `fc1f7a5a046aa460f7589975a9aacd4f4104b0e0` | `5f6efdb99d57d3be78298f57b2d42fd4fb747d83` → same | exact |
| `019` | `6ca5a953ca725d52478901b5abfdbdd51a364276` | `cd9c7bb4d3ab89d7dc83b17af52411477f2c4792` | `5e4516bb3bf5492278abb81291b3987dcad7e618` → same | exact |
| `020` | `703dcc6a859031ff6c28d302119ef6e8df07c94d` | `09810acbc05dda6515e4271ff5dc8e4151608eb4` | `6c6ba5bd8c1e8070c6268be5c17902874f69c24a` → same | exact |
| `022` | `e805fd44141307ba62c4e37a7cd768f426c1b587` | `7502b7619da6affd225a6781a4ac5ee8f6aeb2d7` | `d21e3c2c4fe52ea85e375e4f3bc4572a99c51467` → same | exact |
| `023` | `d031ec5e962c1113ec5b9984b68acb06c58954fb` | `51325493a5e0e10f72dcfc04079d3b4f2c96488e` | `e3cd624647f0210973434f15c63fc28737f2b834` → `1b47a872f322d2e6dbff7989d4ab9ee569879199` | neutral source docs |

ID `001`의 progressive Makefile은 불완전한 역사적 tree도 존재하는 source만 빌드하게 하며 ID
`002–015`의 원래 책임 patch는 그대로 보존했습니다. ID `016`에서 final strict Makefile로 수렴해
old/new tree가 다시 같아집니다. ID `023`은 고정된 legacy-learning provenance를 중립 source 문서와
역사 기간으로 바꿉니다. Expected-old `main`의 마지막
`e4ea219cd6bd0709f97837d8c3fd8785a6369b42`는 source 기여가 없는 learner-navigation-only
commit이므로 replay에서 제외하고 ID `024`를 removed 처리했습니다. ID `021`은 과거 mixed
learning-support 책임이라 current source ID로 재사용하지 않습니다.

Learning 후보는 다음 세 ref였습니다.

| old ref | tip | tree | paths |
| --- | --- | --- | ---: |
| `learning/codex-5.6` | `c35154f879b974f09fd6a2ae7e5cfffd7a26e423` | `f4d6d15b0da971d25f083fe2a336534790e044eb` | 115 |
| `learning/codex-5.6.1` | `c2187fc11369b86d0991cd875c4c423f7efe2c60` | `a497897034de5066c60d0fd610396a3eb3a2443a` | 118 |
| `learning/codex-5.7` | `9d8d723597883457fe75c773819d708874c93608` | `68b6345c552056aac78332ed5ee21de444744e9c` | 124 |

세 tip은 서로 ancestor가 아니지만 path set은 `5.6 ⊂ 5.6.1 ⊂ 5.7`이고 공통 111개 path의
blob이 같습니다. Source 호환성, commit coverage, link·metadata와 유효한 고유 내용을 대조해 5.7을
기준본으로 선택했습니다. 동일한 note/reflection blob은 다시 읽지 않았고 source crosswalk가 달라진
answer와 고유·충돌 문서만 전담 집필자와 저장소 담당자가 한 번 직접 검토했습니다.

최종 `learning/current`는 source 뒤의 actual-time publication 세 commit으로만 구성됩니다.

| phase | commit | tree | parent | actual KST time |
| --- | --- | --- | --- | --- |
| notes | `2a8698752eda41e290a28bf6162b35d106cef884` | `3bb84064fcd8e0e1e47b62ce116d5af04ce8469d` | source `51325493a5e0e10f72dcfc04079d3b4f2c96488e` | `2026-07-20T04:12:57+09:00` |
| answers | `f37d592b835298c526fe68c618e9b288e5f2e081` | `a8ee843721dfef80844f1d02ff78fa58427e568c` | notes | `2026-07-20T04:13:21+09:00` |
| practices / tip | `c8d0b2c3670373246cc2756c56b62c90e60909dd` | `decaa25b9024bdba17ffcc6fa1f738abf2ae9ede` | answers | `2026-07-20T04:13:59+09:00` |

Final corpus는 source 23 = answers 23 + exclusions 0, answers 23 = practices 21 + omissions 2
(`000`, `023`)입니다. Stable ID `021`은 reserved, learner-navigation-only `024`는 removed입니다.
ID `016`의 answer는 Makefile에서 제거된 cleanup/safeguard까지 reconcile했고, 대응 practice는 내부
helper·fixture·control-flow를 누설하지 않도록 다시 파생했습니다. Practice 원장의 answer publication
basis도 최종 answer commit `f37d592b835298c526fe68c618e9b288e5f2e081`로 고정했습니다.
`docs/README.md`는 notes commit에, `docs/commits/**`는 answers commit에,
`docs/practice/**`는 practices commit에만 두어 publication role별 허용 path를 분리했습니다.

Replay 저장소의 `origin`이 GitHub가 아니라 local audit mirror였으므로 첫 push 출력의 destination을
보고 원격 오인을 발견했습니다. 이 transaction은 local mirror만 바꿨고 GitHub ref는 그대로였습니다.
`/opt/homebrew/bin/gh` API와 explicit HTTPS `ls-remote`로 GitHub expected-old를 다시 확인한 뒤
`https://github.com/woopinbell/stack-sort.git`에 exact-lease atomic transaction을 실행했습니다.
첫 fresh clone이 practice 원장의 stale answer basis를 잡아냈고, `learning/current`
`431ad5bf1ec940fa4ae39db834c945bccc6cd911`만 exact lease로 `7326dc0…`에 교정했습니다.
Authenticated remote-navigation은 이어 practice commit에 잘못 놓인 `docs/README.md`를 발견했습니다.
본문을 다시 만들지 않고 그 exact blob을 notes phase로 옮기고 세 publication commit을 다시 연결한 뒤,
remote `7326dc0a0efa073991e3cc19f876ee7747c42257` lease에서 final tip
`c8d0b2c3670373246cc2756c56b62c90e60909dd`로 전환했습니다.

최종 advertised project ref는 `main`, `learning/current`, annotated `v1.0.0`뿐입니다. Final fresh clone은
23개 linear source commit, source identity·timestamp·message·provenance, strict build·test, Python
reference, annotated tag와 strict fsck를 통과했습니다. Learning은 source 뒤 3개 publication commit,
23 answer·21 practice의 ID/hash/parent/tree/H3 전수 대조, 상대 link 76개 missing 0, canonical path,
source/config/test/reference drift 0을 통과했습니다. 삭제한 old learning ref는 별도 bundle이 없고 GitHub
garbage collection 뒤 복구할 수 없습니다.

### `stl-container` 정렬 실행 원장

2026-07-20 KST에 private `woopinbell/stl-container`의 source와 learning ref를 exact lease의 단일 atomic
push로 전환했습니다. Expected-old `main`은
`2d42a1a18d8541aa94aa78b3538db2dc2d60d951`이었고 replacement `main`은
`6f875e0677674d86145188d8558e3cf56b61c9cb`(tree
`3443f2643611b360ead0489b3aff9e2d75696c8f`)입니다. Annotated `v1.0.0` tag object
`d6ff0b12322c9221d47f308097dc4b4980f3b483`는 replacement `main`으로 peel됩니다.

Source-only rollback bundle은 old `main`과 아래 여섯 source tag만 담았고 learning ref는 포함하지
않았습니다. Bundle SHA-256은
`9cfe08c6aadf27b9e65f45224aa310d03cdb3012016bda6625b0550469d0913c`이며 bundle verify, strict fsck,
restore clone과 일곱 ref exact 대조를 통과했습니다. Project와 governance publication 및 fresh-clone
gate가 green이 된 뒤 snapshot, bundle과 restore clone을 폐기하므로 active ref나 offline 보존본으로
복구할 수 없습니다. Old learning ref는 별도 bundle·tag·archive를 만들지 않았으며 remote garbage
collection 뒤 복구할 수 없습니다.

삭제한 source tag의 ref/object/peeled target은 다음과 같습니다.

| ref | old tag object | old peeled target |
| --- | --- | --- |
| `codex-5.6` | `f3f665dc25666248bc573c9b46aa59f5ec9408a9` | `e5d04ef059f94b3910a5ed7d3e79aded5008d427` |
| `codex-5.6.1` | `0b50fda263fab00bcc4321412cec186a9436bdc3` | `11011c5e87f0ec363776052cd186cf6183732968` |
| `codex-5.7` | `9c89472475e8a33e8ec8d11c907a6befefd98270` | `2d42a1a18d8541aa94aa78b3538db2dc2d60d951` |
| `legacy/codex-5.6-monolith` | `aa2b4ad634456e8aec8ec7117a8ec53444bffa54` | `72f2411381854e6fee8c4a48a3a97d312c1fff5d` |
| `pre-history-clean-codex-5.7` | `2ee891d382d2f1d2c47f74fc464698bf927e748e` | `11011c5e87f0ec363776052cd186cf6183732968` |
| `pre-learning-split-codex-5.6` | `7014e53a90f8aa3a2585b5481b5c2485ee7cae04` | `4fb697ffe1bf2ac99b5215cb1d69fb4d55644585` |

Source window `2024-02-28`–`2024-04-11` KST 안에 25개 linear commit을 고정했습니다. Root부터
`7e12df3abdef1c29edfcc36274edc00868124d2b`까지의 첫 23개 commit은 object·tree·patch가 exact입니다.
나머지 source disposition은 다음과 같습니다.

| stable ID | old commit / tree / patch-id | new commit / tree / patch-id | disposition |
| --- | --- | --- | --- |
| `025` | `62a535d4dd641c826931b1c53565f4e9dfc72ce4` / `1d74d9081c93a0e1bcbcd0f327b1b12a7d829f8d` / `c12c5d6b56a8905fefd93c1924158b6985121493` | `284340eaaa9df5263947a7a9ac7264b92bd71338` / same / same | executable C++98 reference 책임과 patch를 보존하고 timestamp를 `2024-04-11T11:08:18+09:00`으로 배치 |
| `026` | `5f1998b1fc55ed0b899b054e6f9b2113cff96bf3` / `bfdb95821ae4a8649c7c8d8ebd971d1dd7809d5b` / `4919d75b35ef8edaa2034350c300735653cb2967` | `6f875e0677674d86145188d8558e3cf56b61c9cb` / `3443f2643611b360ead0489b3aff9e2d75696c8f` / `7470dcb04b5aef320f6c2cdf74435e3bf4704ca3` | 네 source 문서의 versioned learning provenance와 중복 문장을 정리하고 timestamp를 `2024-04-11T17:08:19+09:00`으로 배치 |

Old final `2d42a1a18d8541aa94aa78b3538db2dc2d60d951`(tree
`6d6a2faa55854af56544ffdff8553543fc1b9eee`, patch-id
`53d22f941862234ae7dc7539db80221a6b58573c`)은 learner-navigation-only라 source에서 제외하고 stable
ID `027`을 discarded/reserved 처리했습니다. 그 commit에 섞인 DESIGN의 중복 `사후 평가` 한 줄 교정만
source-doc 책임 `026`에 통합했습니다. Old main과 replacement main의 source, config, tests와 executable
reference 구현 diff는 0입니다.

Learning 후보와 선택 근거는 다음과 같습니다.

| old ref | tip | tree | paths / commits |
| --- | --- | --- | ---: |
| `learning/codex-5.6` | `76bf9c6239a490b85b15db2f3603897a97f397b7` | `58edfed27c854b5f97eeb8853317b2c1a66af372` | 137 / 28 |
| `learning/codex-5.6.1` | `769b0b435388d3f34c4c97b7070e6b7762be9db4` | `ff8350169d9248959703a1863e4b15652bb936d3` | 140 / 29 |
| `learning/codex-5.7` | `ac64ec2943676058c9e48be1a027c1bedd8e51f5` | `99d68d6708ea6def77cb03a54cf70dba393b68a2` | 146 / 29 |

세 tip은 ancestor 관계가 아니므로 source 호환성, commit coverage, link·metadata와 유효한 고유 내용을
대조해 `5.7`을 integration basis로 골랐습니다. `5.6`의 answer `000`–`022`와 대응 practice 본문,
`5.7`의 `025`·`026` answer와 `025` practice를 canonical path로 통합했습니다. `023`, `024`는 old
mixed release 전용 reserved ID, `027`은 source 비도달이라 active corpus에서 제거했습니다. 네 note와
reflection blob은 `oid-identical`, prefix answer/practice의 필수 ID·ordinal·tree·start·target·link
hunk는 `metadata-only`, `025`·`026`과 세 canonical index는 `direct-content`로 한 번 검토했습니다.

최종 `learning/current`는 source 뒤의 actual-time publication 세 commit으로만 구성됩니다.

| phase | commit | tree | parent | actual KST time |
| --- | --- | --- | --- | --- |
| notes | `a69e92e08e3d96d973ec02b07c410da184244df3` | `433070569bec906f2148577746f876f24f984084` | source `6f875e0677674d86145188d8558e3cf56b61c9cb` | `2026-07-20T05:05:05+09:00` |
| answers | `0a69bd50aa84b84011b4c143babd6004e55d4efc` | `3f6a2e26ae8453af8de4fad99efa023e762d791e` | notes | `2026-07-20T05:05:20+09:00` |
| practices / tip | `7ab33c89683e79b072e6baae5c98819ba46c9342` | `145826f812136557fd2c723378f36f016276a546` | answers | `2026-07-20T05:12:56+09:00` |

Final corpus는 source target 25개, numbered answer 28개와 numbered practice 25개이며 practice omission은
`000`, `008`, `026`입니다. A/B split 세 개를 반영하면 `28 answers = 25 practices + 3 omissions`입니다.
Final fresh clone은 advertised ref가 `main`, `learning/current`, annotated `v1.0.0`뿐임을 확인했고 strict
C++98 root/reference tests, UBSan, native `leaks` 0 bytes, source provenance, publication path role,
ID/hash/tree/parent/ordinal/H3, 상대 link 90개 missing 0, source drift 0과 strict fsck를 통과했습니다. ASan은
project `main` 전에 Apple clang runtime shadow-memory 초기화에서 교착해 `ENV-LIMIT`로 분리했습니다.

### `irc-relay-server` 정렬 실행 원장

2026-07-20 KST에 private `woopinbell/irc-relay-server`의 source와 learning ref를 exact lease의 단일
atomic push로 전환했습니다. Expected-old `main`은
`0367c17d77f94253347275ca3c755311061ba88f`이었고 replacement `main`은
`b69347797e81c803397ced1ba23042216caa74fd`(tree
`d08375e09c8a044d907dbfdc15103c27582e85c7`)입니다. Annotated `v1.0.0` tag object
`7c8fe460cd8e4e01ac5c82a5e6e987be7cce58fb`는 replacement `main`으로 peel됩니다.

Source-only rollback bundle은 old `main`과 아래 여섯 source tag만 담았고 learning ref는 포함하지
않았습니다. Bundle SHA-256은
`942fe329ed05ca7307187f521e415dfc1121075f63190c6c01d3e10f17923a12`이며 bundle verify, strict fsck,
restore clone과 main·tag·HEAD ref exact 대조를 통과했습니다. Project와 governance publication 및
fresh-clone gate가 green이 된 뒤 snapshot, bundle과 restore clone을 폐기하므로 active ref나 offline
보존본으로 복구할 수 없습니다. Old learning ref는 별도 bundle·tag·archive를 만들지 않았으며 remote
garbage collection 뒤 복구할 수 없습니다.

삭제한 source tag의 ref/object/peeled target은 다음과 같습니다.

| ref | old tag object | old peeled target |
| --- | --- | --- |
| `codex-5.6` | `b11e067747ea8c2b835af4b5cf428fd098aba4b9` | `6c76d8456a1acbd187904d2d0d5b4776ea70e93a` |
| `codex-5.6.1` | `83bdc36a26f0c9116c806e477a1c58f8b4fb5de5` | `812b2312ebe45b50e3dcaf1a746ff6101d05def8` |
| `codex-5.7` | `905d1303f59f73bcd668cd82290bd45d765f7ede` | `0367c17d77f94253347275ca3c755311061ba88f` |
| `legacy/codex-5.6-monolith` | `419a7cac2c76b219fdf5d7ac2477ea2c0cce59f5` | `d760aad5a122045b041017bdbd8be9557838a433` |
| `pre-history-clean-codex-5.7` | `2b52f59e1114d492f1ab024f97217073ffe3d31f` | `812b2312ebe45b50e3dcaf1a746ff6101d05def8` |
| `pre-learning-split-codex-5.6` | `9ccece0b30099c765dab4a21bb1d82bf392af66a` | `85ec9d47a21f4b1688a7a473a4e13bcba441f02f` |

Source window `2024-04-08`–`2024-07-16` KST 안에 37개 linear commit을 고정했습니다. Root
`30b90c77d22976aa5b0bdb0324dd2d57f0d39f43`부터
`cd817cd4de1bc81c6759a56db2af30e3a42661b9`까지의 첫 29개 commit은 object·tree·patch·timestamp가
exact입니다. 나머지 source disposition은 다음과 같습니다.

| stable ID | old commit / tree / patch-id | new commit / tree / patch-id | disposition |
| --- | --- | --- | --- |
| `036` | `6bb1257cb1cd604de4934bc5c545b4c72263e5cb` / `030a7cf60efdf002c0c2aee79624c1d34478b47f` / `4b151b8e7320c51a011bf82971ff9b7eb810162d` | `1105974a93ac20cbe18d3461fe193579d9fce6ba` / same / same | executable-reference 책임과 patch를 보존하고 active ordinal 29에 배치 |
| `030` | `2a6f4e2d33a33515072f8209d697be5825ebaa83` / `43720d535e969a0b848a1caddc57a7891c177e92` / `fa78b3b8a2cc57adde67955f804126e872e32b71` | `a58e683f74b93922db82e76e2c0c4209f7ae66c5` / same / same | timestamp replay |
| `031` | `fcfb9931f7cfe9f5942e53078048b973afe1a06a` / `fcc224efb73a823e0088027bb73a185792b16626` / `8a3e7fa624d0dfc822d06bc8441661bb12940aab` | `8323d80de47210fb8fd9e128befa085a848095d0` / same / same | timestamp replay |
| `032` | `61f5ef00357c33414c2cdc0e2931461684757e79` / `8c66d7277af153647f18e4f424b05011c074b37c` / `296ac0d66a2d9d89286f1c1f8c3d71b40f0d6995` | `506a97e81ccbeeaba889347caf75724b2760222d` / same / same | timestamp replay |
| `033` | `f7de072c6ba062cac67e2a034bd05db49f197d76` / `81166901c98b93ef866c67768b70e16a3191a41b` / `dfeec8f6fd96bd520162b3b722cec419e2242017` | `070f3e9121b64e5a7e89f25c07815f212dff8d70` / same / same | timestamp replay |
| `034` | `61f5ba2470fa572fc053fc92652b1df4f4959f3f` / `994da50897a18ef777a65e3b90b1e348be0ab842` / `13331591c5485eb5b54d186b41f0a0161fdb292f` | `aaae9e5cf2cf029a49ec6bed6c2f45c2be4d5434` / same / same | timestamp replay |
| `035` | `3b008e1c85b3985dac62b1bb7c7f95ace7929739` / `1dc8fcbdff781f66738283bca3713099266f70ea` / `e21253bdbd65a66ff514c71f5f70fadf9d54f9d3` | `77636de54539f40b4ce1365ca79c5f210a9e99a0` / same / same | timestamp replay |
| `037` | `cc5f31812f5dbcfd418cac739711136837651727` / `7d441c287e9ba59c78ab638d08bb0c8b3ee58030` / `2647d95b5c84fb9572fbd48b431ea5fb84c9fd5e` | `b69347797e81c803397ced1ba23042216caa74fd` / `d08375e09c8a044d907dbfdc15103c27582e85c7` / `4b4cd2ff35863a970038dbed9b270bdea753f006` | source 문서의 versioned provenance를 중립화하고 실제 root·책임 순서로 DESIGN을 교정 |

위 old suffix의 timestamp는 순서대로 `2026-07-16T09:08:13+09:00`부터
`2026-07-16T09:08:20+09:00`까지였고, new suffix는 같은 patch 순서로
`2024-07-16T16:18:13+09:00`, `16:42:14`, `17:05:15`, `17:31:16`, `18:02:17`, `18:37:18`,
`19:11:19`, `20:03:20` KST에 배치했습니다. 각 commit의 author/committer timestamp는 같습니다.

Old final `0367c17d77f94253347275ca3c755311061ba88f`는 learner-navigation-only라 source에서 제외하고 stable
ID `038`을 reserved 처리했습니다. 그 commit의 실제 DESIGN 문법 교정만 source-doc 책임 `037`에
통합했습니다. 첫 candidate `9e1e8efeac9c6d61f61ed6c601d39b938563b936`에서 발견한 잘못된 DESIGN root hash와
책임 범위는 같은 `037`에서 교정한 뒤 freeze를 다시 고정했습니다. Old main과 replacement main의
source, config, tests와 executable reference 구현 diff는 0입니다.

Learning 후보와 선택 근거는 다음과 같습니다.

| old ref | tip | tree | paths / commits |
| --- | --- | --- | ---: |
| `learning/codex-5.6` | `307d67bb354f891466c5065e1c8d54896ba51efb` | `ff12a721e12aea1a19e65a8a196ece11253d6a0e` | 209 / 40 |
| `learning/codex-5.6.1` | `50706544b0a4fb8ee8fdfc4635267e08cd3e945d` | `b45173c02c365bd7172fca360ced58cebd7553c7` | 212 / 41 |
| `learning/codex-5.7` | `cbcce4df187e51ed064bd49cb1c0decdab077d7d` | `c24bac95edbb2fe4d5c038c0bb7567ba21707f94` | 230 / 41 |

세 tip은 ancestor 관계가 아니고 공통 path blob도 일부 diverge하므로 source 호환성, commit coverage,
link·metadata와 유효한 고유 내용을 대조했습니다. `5.7`을 inventory basis로 삼되 그 branch의 잘못된
030–036 renumbering은 채택하지 않고, 안에 보존된 `5.6` stable corpus를 canonical answer/practice
본문으로 선택했습니다. Answer `000`–`028`과 18개 note body, 합계 47개 blob은 OID-identical입니다.
Practice `002`–`028`, `030`–`035`의 33개는 canonical answer link와 final hash/parent만 정규화했고,
executable-reference `036`과 current index는 직접 검토했습니다. Old mixed publication `029`와
learner-navigation-only `038`은 active corpus에서 제외했습니다.

최종 `learning/current`는 source 뒤의 actual-time publication 세 commit으로만 구성됩니다.

| phase | commit | tree | parent | actual KST time |
| --- | --- | --- | --- | --- |
| notes | `4658d952a43d466207b7c1003c2495f12a5b6528` | `52bdaf6c415bdb161ba06ebd1a09b444415180a7` | source `b69347797e81c803397ced1ba23042216caa74fd` | `2026-07-20T06:06:22+09:00` |
| answers | `48be54bbdba103d5a03c9cf9b92e7ac5320e29fd` | `a3ba369919ebc6e94024624abcacaec72c07a93d` | notes | `2026-07-20T06:06:43+09:00` |
| practices / tip | `46bf45dcacb3875ffe093fb40c8e6bb208867ea5` | `b1fb8804c55446008776174ba3ff620e7e5402c7` | answers | `2026-07-20T06:16:01+09:00` |

Final corpus는 source 37 = answers 37 + exclusions 0, answers 37 = practices 34 + omissions 3
(`000`, `001`, `037`)입니다. Stable `029`, `038`은 reserved라 식에 넣지 않습니다. Final fresh clone은
advertised ref가 `main`, `learning/current`, annotated `v1.0.0`뿐임을 확인했고 strict C++17 root build와
TCP smoke, 네 Darwin standalone reference, source provenance, 37 answer·34 practice의
ID/hash/tree/parent/ordinal/H3·책임, canonical link, source drift 0과 clean status를 통과했습니다.
격리 sandbox의 socket bind `PermissionError`는 host에서 재현되지 않아 `ENV-LIMIT`로 분리했습니다.

### `container-stack` 정렬 실행 원장

2026-07-20 KST에 private `woopinbell/container-stack`의 source와 learning ref를 exact lease의 단일
atomic push로 전환했습니다. Expected-old `main`은
`a7f6c98889d5d23277432efd4310c0c2023e7bf2`였고 replacement `main`은
`bd498c17f255681cbc57e598e09a876abb2c0a2e`(tree
`9cfddf11fe5340e1110fd883f025450bf3533f7e`)입니다. Annotated `v1.0.0` tag object
`dd878d65945e32c9a499b175643a1ae39880cb3a`는 replacement `main`으로 peel됩니다.

Source-only rollback bundle은 old `main`과 아래 여섯 source tag만 담았고 learning ref와 세 old learning
tip object는 포함하지 않았습니다. Bundle SHA-256은
`2bb20e8ab04ec4265ec8dfc48bc7ae4c8ce78b2ff278830894bfa8f6e94f06d6`이며 bundle verify, strict fsck,
restore clone과 일곱 ref exact 대조를 통과했습니다. Project와 governance publication 및 fresh-clone gate가
green이 된 뒤 source-only snapshot, bundle과 restore clone을 폐기하므로 active ref나 offline 보존본으로
복구할 수 없습니다. Old learning ref는 별도 bundle·tag·archive를 만들지 않았으며 remote garbage
collection 뒤 복구할 수 없습니다.

삭제한 source tag의 ref/object/peeled target은 다음과 같습니다.

| ref | old tag object | old peeled target |
| --- | --- | --- |
| `codex-5.6` | `3d58131bee387959618e2f5a5d230333994241d8` | `ebf91b37bc1633c9c31167bb782a55c236ac4595` |
| `codex-5.6.1` | `b874bdc6c597e5c0564b305f11552035e4023b23` | `e2bf6d5297254c63f43ea7b0f2c04938b93ef5b9` |
| `codex-5.7` | `2a6c004711f98f17f1cb03a13b94a25f72ddc3ba` | `a7f6c98889d5d23277432efd4310c0c2023e7bf2` |
| `legacy/codex-5.6-monolith` | `fdd66fa36d38bb619b9d3827d9b38edee46a91e7` | `429cfa46dfc45f6872d5020d81c70ca548f18b7c` |
| `pre-history-clean-codex-5.7` | `d16f249713f590efe7404bb04dd348f4c52f32db` | `e2bf6d5297254c63f43ea7b0f2c04938b93ef5b9` |
| `pre-learning-split-codex-5.6` | `6d16d5092991af66390ee260295340805d2f73bc` | `37d7dc6e79a171b3d4f55387fb339bde94ea1c32` |

Source window `2024-07-24`–`2024-09-10` KST 안에 21개 linear commit을 고정했습니다. Stable
`000`–`017`의 첫 18개 commit은 root `68cb047608161e944b6c975573264b7e0d612977`부터
`8dfdaff6bbf75f82625bf9720522f722b4d53f12`까지 object·tree·patch·timestamp가 exact입니다. 나머지
source disposition은 다음과 같습니다.

| stable ID | old commit 또는 basis | new commit / tree / patch-id | disposition |
| --- | --- | --- | --- |
| `020` | advertised `7fee2346aebc750a76bee025d4a3b57d60600ff8`, split basis `afc3c01cef8aeaf61574008896221cb5a59d82f3` | `7382198223d5592d870634aac324e9f5bd7845f1` / `d2d23b2487d8494bf476c444c8f0d21c94fafcfe` / `1f9cde2bcf0f18c549b227f82051e8981c27644d` | executable reference의 tree와 patch를 보존하고 `2024-09-10T11:11:36+09:00`에 배치 |
| `019` | advertised `42d71ce2c72808580ffdf38526dffb9819896bb2`, split basis `5c96b01cc39c31d016baef54aad0a09b5de36bc0` | `38e5bd7a27cfa958b477ccb27f90592e90c75fd6` / `b3feed50f9b7708e3630aaf1d75f6b06b16f8f4f` / `e5517e6c7974394c0d9c7019f7aeb081d42ebf7a` | one-file validator patch를 보존하고 `2024-09-10T13:19:49+09:00`에 배치 |
| `021` | `3cb3a4ee13ee1e2140f2faba27796467c10183c6` + learner-navigation `a7f6c98889d5d23277432efd4310c0c2023e7bf2` | `bd498c17f255681cbc57e598e09a876abb2c0a2e` / `9cfddf11fe5340e1110fd883f025450bf3533f7e` / `38e7478c7f57d16098977c8a948317c5d07bd20d` | release 문서 책임을 합치고 root backlink와 versioned reference link를 source에서 제거 |

Old advertised suffix의 source timestamp는 `2026-07-16T09:08:24+09:00` 이후 current 시각이었고,
replacement suffix는 위 source window의 책임 순서에 배치했습니다. Old main과 replacement main은 같은 135
paths와 mode를 가지며 차이는 13개 Markdown path의 23 additions/32 deletions뿐입니다. Executable
`srcs`, `tests`, `tools` subtree OID는 각각
`69b67be08928678af37ac9ae8d9d9306bfbedbfb`,
`80393147b037743c833902d8bd105485321d5689`,
`9ff8e9e0096fbcac9a0a79d55e73fed80ee396aa`로 old main과 같습니다. Source ref·tag·path·blob·commit
metadata의 금지 provenance는 0건이고 canonical identity, source window, three-section message와 trailer
gate를 통과했습니다.

Learning 후보와 선택 근거는 다음과 같습니다.

| old ref | tip | tree | paths / commits |
| --- | --- | --- | ---: |
| `learning/codex-5.6` | `1e47145a752afac9583ef7a156ab39ffb443a8f5` | `9982d289324e9269e2fe595db5ce4a0ec31b3f97` | 246 / 24 |
| `learning/codex-5.6.1` | `aa11c46d17c71e7393eca4e964d406caa8a92afb` | `04ac42e257065e37c77c65a1f0b2a3418eb56f94` | 249 / 25 |
| `learning/codex-5.7` | `e09f5fb8ff227fda54083a62d561993a683d131f` | `436a8a8fbdd7b17958688cfc409556d89b03fb33` | 257 / 25 |

세 tip은 ancestor 관계가 아니므로 path/blob/tree matrix와 final source crosswalk를 대조했습니다.
`5.7`이 유효 path/blob superset이어서 inventory basis로 선택됐습니다. Concept note body 25개는
OID-identical로 재독 없이 채택했고 current index만 직접 작성했습니다. Answer `000`–`006`은
source hash·ref·link metadata hunk만 한 번 검토한 `metadata-only`, `007`–`017`, `019`–`021`은
source 책임과 문서 전체를 직접 대조한 `direct-content`입니다. Old practice는 current H3 책임 구조와
일치하지 않아 active 20개 전부 canonical answer에서 파일별로 다시 수작업 파생하고 한 번 검토했습니다.
Old mixed-publication `018`, prose facet `018A`, executable facet `018B`와 learner-navigation `022`는
reserved이며 active corpus에서 제거했습니다.

최종 `learning/current`는 source 뒤의 actual-time publication 세 commit으로만 구성됩니다.

| phase | commit | tree | parent | actual KST time |
| --- | --- | --- | --- | --- |
| notes | `aa6473f1a7d0b2935670bf2268dffbc7580421cb` | `b695a4dd2cb81bc3807e708b917352c41b2e77a6` | source `bd498c17f255681cbc57e598e09a876abb2c0a2e` | `2026-07-20T07:31:47+09:00` |
| answers | `cbcccbe0c21ccbe1019f1d82c03c1f84d0ffa8ab` | `1629ec4292b93758b01d496de3f99f7b427913aa` | notes | `2026-07-20T07:32:16+09:00` |
| practices / tip | `4862bd8720928975470f907d653b054b51fea12b` | `1e80d609ede426168ec457ff080daf3417fadcb8` | answers | `2026-07-20T07:45:46+09:00` |

Final corpus는 source 21 = answers 21 + exclusions 0, answers 21 = practices 20 + omission `021`입니다.
Final remote는 `main`, `learning/current`, annotated `v1.0.0`만 advertise합니다. Fresh clone은 204 files,
24 linear commits, strict fsck, ID/hash/tree/parent/ordinal/H3·책임, 상대 link missing 0, source drift 0,
`make test`, normalized Compose config와 source provenance gate를 통과했습니다. 별도 fresh source clone의
세 image build, MariaDB→WordPress→nginx health chain, HTTPS health smoke와 WordPress HTTP 200도
통과했으며 검증용 container, volume, network와 local image는 즉시 제거했습니다. Reference 17개 중
기존 `mysqladmin` readiness race 한 건은 보존된 known red이고 이 migration의 source 변경으로
교정하지 않았습니다.

### `web-boundary-inspector` 정렬 실행 원장

2026-07-20 KST에 private `woopinbell/web-boundary-inspector`의 source와 learning ref를 exact lease의
단일 atomic push로 전환했습니다. Expected-old `main`은
`33a62cf963bb48e55b304f7d80f6a582d9c90f81`이었고 replacement `main`은
`cf57ffeb652288548c351209a278d4907f0b2f95`(tree
`c25c91cccedc88f1afcf171d71624590a9c1c3ae`)입니다. Annotated `v1.0.0` tag object
`5ee7967b12c27a259d1a64f4c72de67f524c46c7`는 replacement `main`으로 peel됩니다.

Source-only rollback bundle은 old `main`과 세 source tag만 담았고 learning ref와 learning-only object는
포함하지 않았습니다. Bundle SHA-256은
`36fa2b8010827b388aee0ead1f704879f9cea053dec87d9b3bbc00334558d263`이며 complete-history,
bundle verify, strict fsck, restore clone과 네 ref exact 대조를 통과했습니다. Project와 governance
publication 및 fresh-clone gate 뒤 bundle, snapshot과 restore clone을 폐기합니다. Old learning ref는
별도 bundle·tag·archive로 보존하지 않았으며 remote garbage collection 뒤 복구할 수 없습니다.

삭제한 source tag의 ref/object/peeled target은 다음과 같습니다.

| ref | old tag object | old peeled target |
| --- | --- | --- |
| `codex-5.6` | `917695f32a1069a3bad820adcda627cc8705da8f` | `237834c7e0cc83efc8c74ef6fffaeb435eaa8613` |
| `codex-5.7` | `8eea6c54810886d974334683d8b4d8a5e491ddb7` | `33a62cf963bb48e55b304f7d80f6a582d9c90f81` |
| `pre-history-clean-codex-5.7` | `d54d8d78ecff72fe3bf0202d545b010b998b8883` | `237834c7e0cc83efc8c74ef6fffaeb435eaa8613` |

Source window `2024-07-29`–`2024-08-04` KST 안에 일곱 linear responsibility를 원래 순서대로
배치했습니다. 모든 replacement commit의 raw author/committer는 canonical identity이고 author와
committer timestamp가 같습니다.

| stable ID | old commit / tree / patch-id | replacement commit / tree / patch-id | disposition / timestamp |
| --- | --- | --- | --- |
| `010` | `176cb1c4680f3969e8eee8786709ee6696d99e97` / `617c9fcde54f0abd13b1f8a8819d29d46ad74c51` / `d596f16e6f9d2176301cd264fb5c5acfe457d693` | `862f9b8bd5fcdc847ebbeec8275998153064d36d` / same tree / same patch | metadata replay / `2024-07-29T10:12:00+09:00` |
| `011` | `4aebfda67d67d899e7f73807ffb37e2f1cd33e87` / `4c48da3ef2ea1675c1bf27fa85862cbf44b06a20` / `27c6e65707bf5deca7f6d146b805b8135c515fbf` | `836053fa5870f2f1cbe8e0cfbf1fe187b9691742` / same tree / same patch | metadata replay / `2024-07-30T11:08:17+09:00` |
| `012` | `2a7ce2310338b27634484b16089c0792d0a8f754` / `ec8fd78011394b874d2b2317111c84c3edbd13e0` / `32afdcaf692ae7f7542046a81b22441ff49e907c` | `ebf0d569ecce10d43becaae4d58fe79be9d8045c` / `df602ae14fcd75a07aedc6d9613f9adceedbf655` / `126a247d39fd5854fbcb000644bbca77000f9404` | RT-08 exact content type와 RT-09 body-length assertion 보강 / `2024-07-31T14:26:31+09:00` |
| `013` | `4ee8d6ec88c2be6eab10eab129d201e2590f0744` / `f125600fc833e4dc35bc405c6381365271dcd54b` / `d189a494524ec88a275d4b625b8cf2757bb7e6f4` | `1f7fd409387551965836d3356137ee8183819a64` / `e2bdbdf5dfed9d98dbd66299c41f4eecd06b5499` / `57aba85ef90e62d026f7c9b60ec41c6abc1deb2c` | slow fixture `180`→`10,000` ms 결정화 / `2024-08-01T10:42:15+09:00` |
| `014` | `0d5958759de96139e191701a2a86887331399cda` / `9464b729c16828476d9deac1cd1757d9a2172c8c` / `fc90b7be1ec1a295fc8ce538ef4fa09eb9197cff` | `5bce204045f7012816f19d905e51bc8586a669a3` / `6c7ec545f5dcb43e4f705ff944b01a780498f43c` / same patch | 선행 fix를 상속한 metadata replay / `2024-08-02T15:17:42+09:00` |
| `015` | `a99f84989220a98b72d1c6f4503efe8a75d61095` / `1f6cce5e2733c4e47ad2c084780a73de534e4d77` / `3ad160d0ed3c3774b21b120690ed1552e0a5351f` | `e237e3c37a102699ba23445fac2b86e6621df853` / `f3b49d4157c1dd1a0ba1adaa3ebcb03fb14a26d6` / same patch | 선행 fix를 상속한 metadata replay / `2024-08-03T13:33:28+09:00` |
| `016` | `33a62cf963bb48e55b304f7d80f6a582d9c90f81` / `2b864b9362dd0388afb697a08381484c28b7f2e4` / `8258ab8aac752d47075c827fc104b76df51be83d` | `cf57ffeb652288548c351209a278d4907f0b2f95` / `c25c91cccedc88f1afcf171d71624590a9c1c3ae` / `516ce632ba827055be0e426f2268948fba8bece1` | release를 `v1.0.0`과 Document Box 소유의 중립 handoff로 전환 / `2024-08-04T17:21:09+09:00` |

Old main과 replacement main은 같은 22 paths와 mode를 가집니다. 차이는 `README.md`,
`request-trace/test/request-trace.test.mjs`, `browser-platform/server.mjs` 세 path의 9 additions/6
deletions입니다. 그 밖의 source/config/test blob은 동일합니다. Final source ref·tag·metadata·tracked
artifact의 금지 provenance는 0건이고 canonical identity, source window, message/trailer와 annotated tag
gate를 통과했습니다.

Learning 후보와 선택 근거는 다음과 같습니다.

| old ref | tip | tree | paths / commits | disposition |
| --- | --- | --- | ---: | --- |
| `learning/codex-5.6` | `ba4670383d0c2fbdba77bb2037ff7d504f04951a` | `9da321af82b1ecef4f237eccb9578563acf84a71` | 43 / 12 | 21 corpus blobs가 5.7에 byte-identical하게 포함돼 별도 active copy를 폐기 |
| `learning/codex-5.7` | `7a0e6e31e3c9d28983c8c21611ed4dd4b19c8f80` | `b38cc890f63832225d3ab9bdb21964b07022a45f` | 58 / 9 | versioned stable `010`–`016` corpus를 current basis로 채택 |

두 old tip은 ancestor 관계가 없지만 5.7 corpus가 5.6의 21개 corpus blob을 전부 포함하고 15개를 더
가진 path/blob superset입니다. Active source와 호환되지 않는 unversioned `000`–`009`는 이전 release
전용 reserved ID로만 원장에 남기고 active tree에서 제거했습니다. Answer 010, 011, 014, 015와 practice
010, 011, 014, 015는 hash/ref/path metadata만 보정했고 practice body는 byte-identical합니다. Answer
012, 013, 016과 두 active index, practice 012, 013과 practice index는 final source/answer에서
`direct-content`로 한 번 검토했습니다. Answer barrier가 닫힌 뒤 같은 sole writer가 practice를 파일별로
파생했으며 repository owner와 독립 reviewer가 변경 hunk만 다시 대조했습니다.

Final `learning/current`는 source 뒤의 actual-time publication 두 commit으로만 구성됩니다.

| phase | commit | tree | parent | actual KST time |
| --- | --- | --- | --- | --- |
| answers | `7b752235fd3ac3926176b012c91c96a270234e72` | `d045caf008613c8c6a466e376ad4a67e96e48205` | source `cf57ffeb652288548c351209a278d4907f0b2f95` | `2026-07-20T08:57:49+09:00` |
| practices / tip | `8d5ce94446c9d9cf4025307b5084203e37e50a3b` | `2a4a9b6f93761a87c30b2e1a80e76a51445633c1` | answers | `2026-07-20T09:05:40+09:00` |

Final corpus는 source 7 = answers 7 + exclusions 0, answers 7 = practices 6 + omission `016`입니다. Final
remote는 `main`, `learning/current`, annotated `v1.0.0`만 advertise합니다. Fresh source와 learning clone은
각각 strict fsck, exact 7/9 linear graph, 22/38 file topology, raw metadata, source drift 0, active corpus
root·mapping·relative link와 수량 gate를 통과했습니다. 두 fresh clone 모두 request 3/3과
Chromium·Firefox·WebKit browser 21/21의 `make check`를 통과했습니다.

### `pong-pong` 정렬 실행 원장

2026-07-20 KST에 private `woopinbell/pong-pong`을 두 차례의 exact-lease atomic transition으로
정렬했습니다. Original `main`은 `1f23360c3fc4829aedf2ea6a1633d2b34f466406`이었습니다. 첫 transition은
old learning 세 ref와 금지 provenance가 있는 source tag 일곱 개를 모두 제거하고 interim
`main` `091a9326c7efe94f59b7e6db4dd841eb2bb228cd`, `learning/current`
`d647dc25b51c566e5d0e5dab9929518a0cc3a6a5`, annotated `v1.0.0` object
`22f9d6e3b646b6e76cfa545497c9f14e5f0bfebd`만 게시했습니다.

그 fresh source의 실제 Chromium desktop/mobile navigation trace가 session identity 전 profile 항목을
`/` anchor로 노출하는 race를 찾았습니다. Source freeze를 다시 열어 `AppShell`이 identity 전에는
`aria-disabled` non-link를, 유효한 handle 뒤에는 `/profile/<handle>` link만 노출하게 했습니다. 두 번째
transition은 위 세 interim object를 exact lease로 잡아 final `main`
`e537ffb457bfbb6225c55beb1dd9cb7b7389867d`(tree
`060530a6b480e49db056950c3a27b5975802c556`), final `learning/current`
`04d4f9d54c5f235ca0c368506217650b8f623f62`, annotated tag object
`30db31454a16571cdbbb129671ad2d6218a29afa`로 한 번에 교체했습니다. Tag는 final `main`으로 peel됩니다.

Source-only recovery artifact는 learning ref와 learning-only object를 포함하지 않습니다. Original
`main`과 일곱 source tag를 담은 bundle의 SHA-256은
`a103a04de242b7c0b941bbb298d8d3864bc6121ae41cb30571de8c5dcb7e17c3`이고, interim clean source와
old interim tag를 담은 두 번째 bundle의 SHA-256은
`6dc061bfa8a7c1094b56d5cac8a4cd47f628be7ea2f6e8b9e5257981bbc91d73`입니다. 두 bundle 모두
complete-history, verify, strict fsck와 restore checkout을 통과했습니다. Learning bundle·tag·archive는
만들지 않았으며 project·governance publication과 final remote audit 뒤 recovery artifact를 폐기합니다.

삭제한 source tag는 remote에 neutral alias로 남기지 않았습니다.

| ref | old tag object | old peeled target |
| --- | --- | --- |
| `codex-5.6` | `437ed54c9e853aa60b6eb08a8683a80bd4f73707` | `b949bbeabf7c93d1a3c7acc0cfd6b1230486a79f` |
| `codex-5.6.1` | `fbce934afd920658d54c9625f829fc5b4f8367ed` | `cdc444b96934530ed72ae6b5eecb964bd7b60131` |
| `codex-5.7` | `c3c17b98b01cab07d32c3d5919df5bd4084faf66` | `1f23360c3fc4829aedf2ea6a1633d2b34f466406` |
| `legacy/codex-5.6-active-union` | `c39b80c63e660d08e8a24cd610525af9d6dc40b7` | `d96d9d9b5ff8ce525b04388b624848df777a37ac` |
| `legacy/codex-5.6-monolith` | `7f6908ecdb9b6388ee9be31e7ae42393c25646df` | `1a3e70a6475404ac8edbe09c08586e726209b56d` |
| `pre-history-clean-codex-5.7` | `ce0343f3f1177bf2a6ad793cd4364ec7d1238162` | `cdc444b96934530ed72ae6b5eecb964bd7b60131` |
| `pre-learning-split-codex-5.6` | `fc7ed821ef8d621b3f6a718d375fa447b5684699` | `258edf487ac18ef6f5fe19259eed5a681726fc0d` |

Old `main`의 첫 85 commits는 `07017767044e4882733a587a2c5cebe6893d95b6`까지 object ID, parent
topology, patch 순서, identity와 timestamp를 byte-for-byte 보존했습니다. Final source는 88 commits와
13 conflict-free merges이며 source window는 `2024-08-05T18:45:46+09:00`부터
`2024-11-13T21:08:41+09:00`까지입니다.

| stable ID | old responsibility | final responsibility | disposition |
| --- | --- | --- | --- |
| `086` | `4674dcc146a0ad75f93efa0d7973d6f9925335eb` / tree `230c88173dfa8c5f785e4599919b34dcf8d8c1cd` / patch `0d0a0fb2cc6ce006f79ba0cc064cd577f7537e8c` | `699d065cc2dbc80ba11d2ac5b59561d7b4365bb5` / tree `dfe742615265304ff075071b0847f80a2098613b` / patch `348d1f67af920a21062201f591a0d48610107a40` | 12 reference를 보존하고 세 target-DB readiness를 실제 query 기준으로 교정 |
| `087` | `0344a7868934c5461d8ede83d36a3243ea605081` / tree `aaa8cb0222fb49f0e5cb68e55db473c0b46d3f01` / patch `29df97af9b91a38b59ef10eda979b8ef0cf1f30f` | `091a9326c7efe94f59b7e6db4dd841eb2bb228cd` / tree `ecf5b3b9e7bb2a1c4cc17d868b221379ffdfcc69` / patch `ad180aac81a0017ecfde8888e0eddc20920885d6` | product guide와 DESIGN을 source-local contract로 정리 |
| `088` | `1f23360c3fc4829aedf2ea6a1633d2b34f466406` / tree `2a2d0b479105b10f1322c256524fd80852798992` / patch `3b65cf727015b3dc81174a684a3d42c6c73f5a5f` | none | learner-navigation-only 책임을 source에서 제거하고 ID를 영구 reserved |
| `089` | none | `e537ffb457bfbb6225c55beb1dd9cb7b7389867d` / tree `060530a6b480e49db056950c3a27b5975802c556` / patch `5df5368e5b6057615f4b0148b610aa81f0676b0f` | profile identity readiness를 새 source 책임으로 추가 |

Old `main`과 final `main`의 tree diff는 19 paths, 60 additions와 96 deletions입니다. Final source의 raw
identity, timestamp ordering, three-section suffix message, trailer, ref/tag/path/blob provenance, strict
fsck와 annotated-tag gate를 통과했습니다. Root frozen install, four-package typecheck, API 9/9, DB 5/5,
declared zero-test gates, nine-route production build, HTTP/WebSocket smoke와 desktop/mobile Playwright
12/12도 통과했습니다.

Source의 `cursor` token은 제품 CSS 의미만 허용합니다. Historical reachable graph의 exact allowlist는
20 unique blobs와 31 occurrences이고 final tree는 아래 첫 다섯 blobs의 7 occurrences입니다. 새
`AppShell` blob에는 해당 token이 없습니다.

| blob | path | occurrences | 의미 |
| --- | --- | ---: | --- |
| `9626c6be546653bd9036c89a435d2ee15f65df9c` | `apps/web/src/app/page.tsx` | 1 | disabled cursor utility |
| `fa403682248123737bf04dad2e23e3d96921ff93` | `apps/web/src/app/play/page.tsx` | 3 | disabled cursor utility |
| `4838aa8d57cbaf6f1b64e34e6f09daf618d2ee7a` | `apps/web/src/app/profile/[handle]/page.tsx` | 1 | disabled cursor utility |
| `5bd900d480f2124c12be69b583a457335a227237` | `apps/web/src/app/tournaments/page.tsx` | 1 | disabled cursor utility |
| `d9fdc73a2bd94d571642689f1846b3219e91d4ed` | `notes/reference-impl/playwright/public/index.html` | 1 | CSS pointer cursor |
| `c5bd8882af4a90caee04a81124e595766c80485f` | `apps/web/src/app/page.tsx` | 1 | disabled cursor utility |
| `af7121090b4f90e2ed7703a8e28ab5060c41459f` | `apps/web/src/app/play/page.tsx` | 3 | disabled cursor utility |
| `88d795878eefc5bfd2f5b5ada59fadcfc7b7f098` | `apps/web/src/app/play/page.tsx` | 3 | disabled cursor utility |
| `640736ee5c05b3ca50e9994b1f10380715275cdb` | `apps/web/src/app/tournaments/page.tsx` | 1 | disabled cursor utility |
| `d578fb46dcaab0e79ef64c5d2599c7a988cf92dd` | `apps/web/src/app/profile/[handle]/page.tsx` | 1 | bare cursor utility |
| `f6351562622e7a880784e1342930ab5c75dcb310` | `apps/web/src/app/page.tsx` | 1 | disabled cursor utility |
| `b53e2b8d608563a739bf4836761c1f5a92e8db33` | `apps/web/src/app/profile/[handle]/page.tsx` | 1 | bare cursor utility |
| `8fc3a52af6a78fe4c20e3f5721e926ed1132e9fb` | `apps/web/src/app/tournaments/page.tsx` | 1 | disabled cursor utility |
| `ef1999c6634c0f76cef31bd1550456f9a5b40e7e` | `apps/web/src/app/page.tsx` | 1 | disabled cursor utility |
| `b925177781be139af7d14cf80b4685a852434f42` | `apps/web/src/app/play/page.tsx` | 3 | disabled and bare cursor utilities |
| `cbae31488c4eeca78bcd819477fc7d3e77d11859` | `apps/web/src/app/play/page.tsx` | 2 | disabled and bare cursor utilities |
| `1b1351daf86af5633b105ab3b2b86f92f28ae4d1` | `apps/web/src/app/page.tsx` | 1 | disabled cursor utility |
| `258f52483f447b0a6646531cdbb59619377f948a` | `apps/web/src/app/play/page.tsx` | 2 | disabled and bare cursor utilities |
| `ab4ac861010bfcd3022559bbca5b4d73352a0e2a` | `apps/web/src/app/profile/[handle]/page.tsx` | 1 | bare cursor utility |
| `e90955a9f1e6b8593012935317c07fd549509872` | `apps/web/src/app/play/page.tsx` | 2 | disabled and bare cursor utilities |

Preserved prefix의 historical gate는 85 commits와 73 unique trees를 모두 검사했습니다. Machine result
SHA-256은 `867acdeef30535d57e1bee97d65e39b0c9b9bbbf8229a15f76752d107ad7ef32`이고 commit
분류는 PASS 75, PHASE-RED 9, EXPECTED-RED 1입니다. Post-lock unexpected red는 0입니다.

| progressive responsibility | bounded historical failure | first green |
| --- | --- | --- |
| `981d6a3886644d96bff7b921109e7da714b18548`, `3b5bb1b96596d7939d106b8c7e795cb952d5b607` | shared later export | `a93304cdb1d709bb41ae29b5ffeac6f04524309b` |
| `fa3b46fc3d78b47bce96e5581af3d087811ec931`, `ed32ebcd1b4a0eabe83e5dd16ba12bc13774d0db` | DB input와 repository index 순서 | `dff0e024a7c969ce317157526612e8c958f7f6f7` |
| `3cb89a215abe772997b03531256594869887461a`, `8b7eef825e6f6b6ede70b9c3e967dcd1ceb561c4`, `da87cb492a151818ba120f51a39562ffe6a89093`, `d6b2fe11e20ccc9d17a1ced1884e5d8b9c311735` | API input, app, game hub와 test collection 순서 | `90c193689c75372d8ca6483a172013b90a65175d` |
| `c85f3745cabe28e9f75b6bde418575bb578b274d` | Next workspace가 app directory보다 먼저 존재 | `e67eae94cd6ddfd9aaa9e6d0ec1fc4fa7954b182` |

EXPECTED-RED `a3f44baacd97bf017742254a34230cf9136bb22f`는 lockfile-only zero-test state이고
`76f3dac37552d2ed050e87eb1fa044d4f5c21deb`에서 명시적으로 green이 됩니다.

Learning 후보는 path/blob matrix의 완전 포함관계로 비교했습니다.

| old ref | tip | tree | paths / commits | disposition |
| --- | --- | --- | ---: | --- |
| `learning/codex-5.6` | `984b1235ab80300f223092fe36b80482311d8c1e` | `3baad8655ff7a3f8cb8dc5da3beabe44811bbe1d` | 539 / 90 | 5.7에 없는 유효 corpus path가 없어 별도 active copy 폐기 |
| `learning/codex-5.6.1` | `a9ddbbfe2ec408326a1358bbc3ba905bc99fbb6d` | `a608ad06c3f24a39c6ad5bc461242da7bc5131fb` | 542 / 91 | 5.7에 완전 포함 |
| `learning/codex-5.7` | `f39366c57a73624f77bbdbf18b8a2a1f7a8c8998` | `99dd261f4a59e2c6245fbd7970141c4746d274d4` | 548 / 91 | canonical blob reuse basis |

동일한 000–084 answer, 67 canonical practice, notes와 reflection blob은 재독하지 않았습니다. Stable ID
`086`의 기존 answer/practice를 재사용하고 `087`의 actual source 책임만 좁혀 읽었으며, 신규 source
`089` answer를 전담 집필자가 수작업 작성했습니다. Answer 전체 review barrier가 닫힌 뒤 같은 집필자가
`089` practice를 처음부터 수작업 파생했습니다. Writer는 stage·commit·tag·push를 하지 않았고 repository
owner와 독립 reviewer가 신규·변경 파일만 한 번 검토했습니다.

Final learning publication은 source 뒤의 actual-time commits 세 개입니다.

| phase | commit | tree | parent | actual KST time | paths |
| --- | --- | --- | --- | --- | ---: |
| notes | `44a62b7a8b280b181954b80ebea370b87cb9b655` | `31ee408ca0c30b1998ef4748d2a1c03d84336eac` | source `e537ffb457bfbb6225c55beb1dd9cb7b7389867d` | `2026-07-20T11:41:56+09:00` | 48 |
| answers | `f3931695110f9f49856ca8a25f413ff5f2931bc1` | `915caadcd2b9efd594cc8b96fe28a61377dcbf38` | notes | `2026-07-20T11:56:06+09:00` | 89 |
| practices / tip | `04d4f9d54c5f235ca0c368506217650b8f623f62` | `30540fb255177cc65fba590365d0efbbde7fbc14` | answers | `2026-07-20T12:07:12+09:00` | 70 |

Final reconciliation은 `88 reachable = 74 answers + 14 exclusions`와
`74 answers = 69 practices + 5 omissions`입니다. Exclusion은 13 conflict-free merges와 lockfile-only
`032`, omission은 `000`, `002`, `039`, `048`, `087`이고 stable IDs `085`, `088`은 reserved입니다.
Numbered answer는 88개, practice는 69개입니다. Final checkout은 179 source paths와 207 learning-only
paths, 총 386 tracked files이며 source/config/test diff는 0입니다.

Final remote는 `main`, `learning/current`, annotated `v1.0.0`만 advertise합니다. 별도 fresh source와
learning clone에서 exact ref/tag/tree, strict fsck, 88/13 source graph, 3단 learning publication,
386-file topology, raw publication metadata, 288 local Markdown links missing 0과 corpus 수량을
재검증했습니다. Fresh source의 frozen install, typecheck, API 9/9, DB 5/5와 nine-route build도
통과했고 최종 source object에서 앞서 완료한 HTTP/WebSocket 및 Playwright 12/12 증거와 일치합니다.
Document Box의 인증 remote-navigation에서도 42의 13개 project와 Central link가 모두 PASS했습니다.
전체 30개 실행이 별도로 보고한 `frontend-reliability-training`, `portfolio-site`,
`sportsbook-shared-protocol` 세 저장소의 5개 오류는 delegated lane의 미완료 집필 publication 문제이며
이 42 migration에서 source나 registry를 임의 수정하지 않습니다.

### Execution lane handoff 원장

다른 세션으로 lane을 넘길 때 handoff 문서는 최소한 다음을 고정합니다.

```text
lane / 담당 track / 저장소 순서 / hard exclude
정본 policy commit / sourceWindow / release 의미 / branch topology
완료·진행·미착수 저장소 / remote expected-old / local artifact 위치
source-only bundle SHA-256 / learning disposition / approval 상태
publication slot 구현 / governance 허용 path / 최종 통합 소유자
```

Handoff에는 token, credential, private key와 삭제할 learning 본문 bytes를 복제하지 않습니다. 인수 세션은
문서에 적힌 SHA를 그대로 신뢰하지 않고 첫 작업에서 `document-box/main`과 대상 remote ref를 다시 읽어
drift를 확인합니다. 소유권이 겹치거나 publication slot 상태가 불명확하면 remote mutation만 중단하고
사용자에게 보고합니다.

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

### `frontend-foundations-training` 일회성 corpus 형식·교정 경계

이 절은 2026-07 정렬 migration의 `frontend-foundations-training` 한 저장소와 그
`learning/current` 정렬에만 적용합니다. Old learning 기준은 다음과 같습니다.

- `learning/foundations-v1`
  - tip `446e6d59f0e8acec6fe62ffbbaf7b5c048d9e3ff`
  - tree `4c7087dab9050ae43af16c1b1121ef8cd61cd1b8`
- `learning/foundations-v1.0.1`
  - tip `fdffc0e6842df7d44701bb2569806f72e5c72d67`
  - tree `11814eafe1f7ba2859940a479dc1df67930977e6`
- legacy answer subtree `b2a3211f8ec4dce7357d59be3cbe0a811e66c35c`
- legacy practice subtree `3b0b0c4e9c19fc6d4afdab538fbb6634251b3bd7`

README를 제외한 numbered legacy file의 pre-migration path·blob·byte manifest는 다음과 같습니다.

| corpus | 파일 | bytes | manifest SHA-256 |
| --- | ---: | ---: | --- |
| answers | 73 | 253966 | `621f9cb2d57040d408c5907455803e0f032379822aaeb0db0dba0963ff0408b3` |
| practices | 12 | 55451 | `4c306aa78e366cbf8913b79df35a620b98ec5ad9639c4d5e95bc8bf2307cd076` |
| 합계 | 85 | 309417 | `ae70f92fee7d307d62ddbcb1f83314dc8872daefc924b6d51fd6b828b0a34624` |

위 digest는 예외 대상인 old 입력 집합의 경계이며 잘못된 내용을 byte 보존하라는 지시가 아닙니다.
저장소 실행 원장은 각 row의 exact old path, blob OID와 byte 수를 보존하고, 교정 파일은 final blob
OID와 old↔new hunk disposition을 추가합니다.

이 85개 numbered file에는 구 corpus 형식을 한 번 유지할 수 있습니다. 구체적으로
`docs-commit-note.md` §6의 현행 metadata·번호형 H3·`**책임:**` 전체 형식과 §7의 현행 practice
banner 문구를 소급해 전면 재작성하지 않아도 됩니다. 다음 항목은 예외가 아닙니다.

- source commit·parent·tree·diff·공개 계약·검증 계약의 사실 정확성
- answer→practice link, active path, stable ID와 번호 대응
- 신규·변경·source 영향 파일의 직접 검토
- active README의 전체 mapping, exclusion, omission과 수량식
- 단일 집필자, source freeze, answer 전체 완료·검토 뒤 practice 진입
- 수작업 교정, commit별 path allowlist와 실제 집필 시각
- `docs/README.md`, `docs/commits/README.md`, `docs/practice/README.md`의 현행 형식

다음 answer는 old blob을 그대로 채택할 수 있습니다.

```text
000 001 002 003 004 005 007 008 011 012 015 016 019 020
023 024 027 028 031 032 035 036 039 040 043 044 047 048
051 052 055 056 059 060 063 064 067 068 071 072 075 076
079 080 083 084 087 088 089 090 092 093 094
```

다음 practice도 old blob을 그대로 채택할 수 있습니다.

```text
001 002 003 004 005 087 088 090 092 094
```

단, answer·practice `090`은 final source에서 parent patch 관계가 달라졌으므로 byte가 같아도
`oid-identical`로 기록하지 않습니다. 전담 집필자가 파일 전체를 final source와 직접 대조하고
`direct-content — reviewed, unchanged`로 기록합니다.

다음 answer는 파일 전체를 한 번 직접 읽고 final source의 catalog diff·계약과 충돌하는 hunk만
수작업 교정합니다.

```text
009 013 017 021 025 029 033 037 041 045
049 053 057 061 065 069 073 077 081 085
```

대응 practice 중 실제로 존재하는 `009`, `041`도 교정합니다. 모든 answer 교정과 answer review가 끝난
뒤, 같은 집필자가 교정된 answer 전체와 해당 practice 전체를 다시 대조하고 잘못된 hunk만 수정합니다.
따라서 final diff가 hunk 단위라는 사실은 §7이 금지한 “hunk만 보고 치환하는 파생”을 허용하지 않습니다.
각 파일은 `direct-content`로 기록합니다.

다음 파일은 위 legacy-format manifest의 적용 대상이 아닙니다.

- old `docs/commits-codex-5.6/104.md`와 대응 practice는 실제 stable ID `105`로 판정해
  `docs/commits/105.md`, `docs/practice/105.md`로 옮기고 현행 metadata를 적용합니다.
- old `docs/commits-codex-5.6/107.md`와 대응 practice는 실제 stable ID `106`으로 판정해
  `docs/commits/106.md`, `docs/practice/106.md`로 옮기고 현행 metadata를 적용합니다.
- stable ID `104`의 Zustand source 책임은 새 현행-format answer와 practice를 수작업 작성합니다.
- final source의 stable ID `107` source-doc 책임은 commit exclusion으로 기록합니다.
- old stable ID `108` learner-navigation-only commit은 final source에서 비도달하므로 reserved로
  기록하고 old answer를 active corpus에서 폐기합니다.

`104`, `105`, `106`, 세 active README와 이번 migration 뒤 새로 만드는 모든 파일은
`docs-commit-note.md` 현행 형식을 완전히 따릅니다. 등록된 legacy file도 위에 열거한 교정 hunk 외의
본문을 바꾸거나 이후 source 의미 변경 때문에 다시 수정하면 이 예외가 끝나며 해당 파일을 현행
형식으로 전환하거나 새 별도 승인을 받아야 합니다. 이 예외는 다른 저장소로 복제하지 않습니다.

Final README와 실제 graph는 최소한 다음을 reconcile합니다.

```text
reachable source commits 99 = answers 76 + exclusions 23
answers 76 = practices 15 + omissions 61
exclusions 23 = resolution 없는 merge 22 + stable ID 107 source-doc 1
stable ID 108 = old release 전용 reserved, final reachable count에서 제외
```

### `frontend-foundations-training` source product-token allowlist

| 저장소 | exact path | 허용 token·context | exact blob과 책임 commit | 제품상 이유·검토 근거 |
| --- | --- | --- | --- | --- |
| `frontend-foundations-training` | `src/exercises/ExerciseDemo.tsx` | 소문자 `cursor`가 exact Tailwind utility `disabled:cursor-not-allowed` 안에 있는 경우만 | blob `6a2df91aa750ceb812fbc32f034e596070da66fd`, replay commit `4a5e35f6a1b42af82ec5e7284f6c6d3332018f9b`; blob `73e1c8b09e72cd6cc128f6e91ca9abbfaa92054c`, replay commit `db6b2310203604744793152447c5cea8137b6783` | disabled pagination button의 CSS `cursor: not-allowed` 시각 피드백입니다. 두 blob의 JSX, `disabled` 조건과 source diff를 직접 확인했으며 작업 도구 provenance가 아닙니다. |

각 blob에는 이 utility가 pagination 이전·다음 button에 두 번 존재합니다. 이 allowlist는 exact path,
exact blob과 exact utility context에만 적용합니다. 다른 path·blob의 `cursor`, 대소문자 변형, ref/tag
이름, commit/tag metadata·trailer, tool-control artifact를 허용하지 않습니다. 새 occurrence는 별도
승인 전까지 실패입니다. Source provenance gate는 “등록되지 않은 일치 0건”과 위 등록 occurrence를
분리해 보고합니다.

### `frontend-foundations-training` 실행 원장

이 원장은 위 일회성 예외를 실제 object와 review disposition에 닫습니다. 원격 전환 전 고정한 source
기준은 `main` `3fb57c957265a76301dbad44f2abd8be074318b5`, tree
`a078559ec7d206fa31f533256507090d769b3d74`입니다. 두 차례의 승인된 atomic transition 뒤 최종
게시 state는 다음과 같습니다.

- `main` `cfa232f03aab569d7ebb6c8ed1f1a7ac1dc2464c`, tree
  `b1b5d3236f13c1f5f89c5fc2210dd9deb7039d04`
- annotated `foundations-v1.0.1` tag object
  `c535edc866d84b1769953a0e2f35b2b0d0dd47fa`, peeled source tip `cfa232f03aab569d7ebb6c8ed1f1a7ac1dc2464c`
- source graph 99 commits, 고유 resolution이 없는 merge 22개, root
  `3873113c30b132034533ab0f080e578090801688`

최초 transition은 `main` `206a4a5b333e3110cc0216e3b94111fb211f0f30`, tree
`73af694cbc32daea022b71eeb7ca5c74e59b706a`, tag object
`d63004ae0927582f705e5d64781f05fc9c923f5d`, `learning/current`
`51020f0d7e391db94305409894e0effa68fff1d1`을 게시했습니다. 게시 뒤 authenticated remote-navigation이
root README의 exact 단계 카드 backlink, 현행 stable/ordinal mapping row 인식과 두 learning publication
scope를 각각 보정해야 함을 발견했습니다. 후속 정정은 final source 문서 commit에 backlink 한 줄을
추가하고 같은 source basis에서 learning publication 세 개를 다시 만들었습니다. 최초 publication과 최종
publication의 전체 path set은 같고 변경 blob은 root `README.md`, `docs/README.md`,
`docs/commits/README.md`, `docs/practice/README.md` 네 개뿐입니다.

Old `foundations-v1.0.1` object `0a1a725407eb199f7f283e86e46ffa417fdb5ce3`(peel old `main`)은 위
최종 annotated object로 교체했습니다. Old `foundations-v1` object
`bc22473d30b398108b0af03749ee5b6664c3a939`, `legacy-feature-graph-v1` object
`645ad72533fa9fa8df202cce3e0b350347e36c9d`, `pre-codex-5.6` object
`43b6ba37cc7c1adcfb688b6b0f9a113cc3c64b34`는 원격에서 삭제하고 최초 source rollback bundle에 포함한 뒤
아래 fresh-clone gate가 끝나자 함께 폐기했습니다.

99개 old↔new commit·tree·parent·timestamp row는
[`data/migrations/frontend-foundations-training-source-crosswalk.tsv`](data/migrations/frontend-foundations-training-source-crosswalk.tsv)에
고정합니다. 파일은 header 포함 100줄이며 SHA-256은
`5d9f66baab190b28593770811b358b030560e4944c154467784c6f89b57b83d8`입니다. Source commit의 patch
순서와 기존 timestamp는 보존했고, 승인 window 밖 publication 책임 4개만 같은 마지막 개발일의 순서
안으로 옮겼습니다. Source identity, `%aI == %cI`, message, trailer와 등록되지 않은 provenance 검사는
모두 0건입니다. 위 product-token allowlist 4 occurrence만 별도로 통과합니다.

최초 transition의 source rollback bundle은 승인 전 다음 값으로 검증했습니다.

- 경로:
  `/Users/woopinbell/Documents/Codex/2026-07-19/1/work/frontend-lane/frontend-foundations-training/frontend-foundations-training-3fb57c95-source.bundle`
- SHA-256: `a534e577221e1d8a9bf204a9825b4ba542883fdbd5d796f43036db9ab21fd267`
- 범위: old `main`과 old source tag 4개, learning ref 0개
- 복원 검증: bundle verify, restore clone의 exact ref와 `git fsck --full --no-reflogs` 통과

이 bundle과 검증용 restore clone은 최초 published fresh-clone gate가 끝날 때까지만 보존했고,
2026-07-19T22:41:21+09:00에 성공 gate를 확인한 뒤 폐기했습니다. 복구할 수 있는 local copy는 남기지
않았습니다.

후속 정정 전에는 당시 공개 source만 담은 별도 rollback bundle을 다시 만들었습니다.

- 경로:
  `/Users/woopinbell/Documents/Codex/2026-07-19/1/artifacts/frontend-foundations-training-correction-206a4a5b/frontend-foundations-training-206a4a5b-source.bundle`
- SHA-256: `8a9e7083ed0d0f931ce520a74121d12b5f2582b299621a408172c91f2460b0e1`
- 범위: 당시 `main` `206a4a5b333e3110cc0216e3b94111fb211f0f30`과 tag object
  `d63004ae0927582f705e5d64781f05fc9c923f5d`, learning ref 0개
- 복원 검증: bundle verify, restore clone의 exact main·tag와 strict fsck 통과

후속 정정의 fresh clone에서 source build·test·E2E, 독립 Zustand package와 corrected corpus를 확인한 뒤
2026-07-19T23:19:57+09:00에 bundle·snapshot·restore clone을 함께 폐기했습니다. 복구할 수 있는 local
copy는 남기지 않았습니다. Learning branch는 사용자 결정대로 두 transition 모두 bundle, archive ref
또는 보존 tag를 만들지 않았습니다. 따라서 삭제한 기존 두 learning ref와 교체된 최초
`learning/current`는 아래 object 기록만으로 복구를 보장하지 않습니다.

Learning 입력과 단일화 결과는 다음과 같습니다.

- `learning/foundations-v1`: tip `446e6d59f0e8acec6fe62ffbbaf7b5c048d9e3ff`, tree
  `4c7087dab9050ae43af16c1b1121ef8cd61cd1b8`
- `learning/foundations-v1.0.1`: tip `fdffc0e6842df7d44701bb2569806f72e5c72d67`, tree
  `11814eafe1f7ba2859940a479dc1df67930977e6`; path/blob matrix에서 앞 branch의 유효 corpus를 포함하므로
  canonical legacy basis로 사용
- 최종 `learning/current`: tip `96e1d790d4c606212f1f1a5afe9500e395cce2ec`, tree
  `d8a79df99ecfe3cdde4953f9f21397cd2d83e886`
- 최종 실제 시각 publication commits: notes `98e82792e756a060eb9d65294869b23bdb78b09c`, answers
  `85abe85711fd3311d821a5c48906f3b451df21c4`, practices
  `96e1d790d4c606212f1f1a5afe9500e395cce2ec`

96개 old corpus path의 blob·byte·final path·final blob·판정·review mode는
[`data/migrations/frontend-foundations-training-learning-disposition.tsv`](data/migrations/frontend-foundations-training-learning-disposition.tsv)에
고정합니다. 파일은 header 포함 97줄이며 SHA-256은
`95325fe3023fbf136d193b26eabda818b0509cda77d6615e0c884e6bacb582bf`입니다. Disposition은
`adopted 63 / corrected 22 / replaced 10 / discarded 1`, review mode는
`oid-identical 61 / direct-content 35`입니다. Direct-content answer review는
2026-07-19 21:31:20 KST, practice review는 2026-07-19 21:57:47 KST에 닫았습니다. 후속 정정은 위 네
README의 backlink·basis metadata hunk만 전담 집필자와 저장소 담당자가 다시 읽고 나머지 동일 blob은
재독하지 않았습니다.

Final corpus 수량은 `99 reachable = 76 answers + 23 exclusions`,
`76 answers = 15 practices + 61 omissions`입니다. Old stable `108` navigation-only 문서는 active corpus에서
폐기하고 번호만 reserved로 남깁니다. 2026-07-19 최초 전환과 후속 정정은 각각 exact lease와 사용자
승인을 통과해 atomic push로 완료했습니다. Advertised project ref는 `main`, `learning/current`, annotated
`foundations-v1.0.1`만 남았고 fresh clone에서 source build·test·E2E, 독립 Zustand package와 corpus
topology를 다시 검증했습니다. Authenticated remote-navigation에서도 project와 Frontend application
overlay가 통과했습니다.

### `frontend-delivery-training` 실행 원장

2026-07-20 KST에 private `woopinbell/frontend-delivery-training`을 사용자 승인과 exact lease를 사용한
단일 atomic push로 전환했습니다. Expected-old `main`은
`6a08f77379408f87874239893b368b47e0366ea2`(tree
`753dce5dce94b1f6daa6ade6e3cc5cd50cc6b23f`)였고 replacement `main`은
`eaab17de0c56f236362b6e53ab0e8af6e650e5e7`(tree
`fd4178ba7d9eea46c7997ec866759725806c725a`)입니다. Annotated `delivery-v1.0.1` tag object
`ccb838904a006b0fdb9b0e111dedc61dbe9c74c2`는 replacement `main`으로 peel됩니다. Final source는 root
`c5f7d82d9c84aae7e1327fb2a08367354df0e391`부터 16개 linear commit이며 merge는 없습니다.

삭제하거나 교체한 source tag의 ref/object/peeled target은 다음과 같습니다.

| ref | old tag object | old peeled target | disposition |
| --- | --- | --- | --- |
| `delivery-v1` | `0370ef9a6f11ec46ef0d70ec0a0cd7fe4ae0ba79` | `95c4d9ed5130f56c56dfbc881dccaa0918d5bffd` | 삭제 |
| `delivery-v1.0.1` | `b8b6b25c76deda00cc0882b3efca51d67fb2ddb8` | `6a08f77379408f87874239893b368b47e0366ea2` | 위 final annotated object로 교체 |
| `pre-codex-5.6` | `79a1902151d1bbcdc75bd7c10048ff54947a17a0` | `6fa3d12de7cf00e59de667cc0e0031db7cc03b16` | 삭제 |

17개 old↔new source disposition은
[`data/migrations/frontend-delivery-training-source-crosswalk.tsv`](data/migrations/frontend-delivery-training-source-crosswalk.tsv)에
고정합니다. 파일은 header 포함 18줄이며 SHA-256은
`094285202dfc64a165a5acea1e91002984a64485f95aa6dc055c59f165336f16`입니다. 첫 9개 책임은 old/new
tree와 stable patch-id가 exact이고 원래 `2025-05-04`–`2025-05-06` KST timestamp도 보존했습니다.
Old `b96d5bef7b587e0cf689559c440d19edcd1176b8`의 source boundary 문서는 stable topology에 맞게 수동
교정했습니다. 그 뒤 lockfile, generated framework file, local browser QA, smooth scroll과 production E2E
다섯 patch는 원래 patch-id와 순서를 보존해 승인 window 안에 replay했습니다. Final
`95c4d9ed5130f56c56dfbc881dccaa0918d5bffd` 책임은 active 문서의 exact heading, H3별 단일 책임과
answer 누출 검사를 강화해 replacement tip에 통합했습니다. Old final
`6a08f77379408f87874239893b368b47e0366ea2`는 source 기여가 없는 learner-navigation-only commit이라
source graph에서 제외했습니다. Source identity, author/committer timestamp 일치, source window,
three-section message, trailer와 source ref·tag·path·blob·metadata의 금지 provenance 검사는 모두 0건입니다.

전환 전 source-only rollback bundle은 다음 값으로 검증했습니다.

- 경로:
  `/Users/woopinbell/Documents/Codex/2026-07-19/1/work/frontend-lane/frontend-delivery-training/frontend-delivery-training-6a08f773-source.bundle`
- SHA-256: `0a4fe6c6451b36b11b2e1b3a23fe9ea601f9d012b6e7e80e41fa774faab5f63f`
- 범위: old `main`과 old source tag 3개, learning ref 0개
- 복원 검증: bundle verify, 네 ref exact 대조와 restore clone의 strict fsck 통과

Project·governance publication, fresh clone과 authenticated Delivery remote-navigation이 모두 green이 된
뒤 2026-07-20T10:36:21+09:00에 위 bundle, source-only snapshot과 restore clone 세 개를 폐기했습니다.
따라서 이 migration 전 source를 보장하는 offline rollback artifact는 남아 있지 않습니다. Old learning
ref도 사용자 결정대로 bundle, archive ref 또는 보존 tag를 만들지 않았습니다.

Learning 후보와 단일화 근거는 다음과 같습니다.

| old ref | tip | tree | total paths |
| --- | --- | --- | ---: |
| `learning/delivery-v1` | `f394e71293c8fe29a424ecfb78eaa3cdb670ac65` | `368a7f2b23077adf95a1f104a613638d088cb6e5` | 89 |
| `learning/delivery-v1.0.1` | `75b284f385e206fec53f5f0d37a7c9a1b1944fe2` | `89f51ce0518fc480002d2a929b5c67b740b35376` | 92 |

두 tip은 ancestor 관계가 아니지만 공통 86 paths의 blob이 같고 충돌은 source 소유 `README.md`,
`docs/DESIGN.md`, `docs/README.md`뿐입니다. `delivery-v1.0.1`은 `delivery-v1`의 유효 corpus에 stable
`023`과 versioned answer/practice row를 더한 strict corpus superset이라 canonical legacy basis로
선택했습니다. Canonical basis의 commit/practice 37개 row는
[`data/migrations/frontend-delivery-training-learning-disposition.tsv`](data/migrations/frontend-delivery-training-learning-disposition.tsv)에
고정합니다. 파일은 header 포함 38줄이며 SHA-256은
`c422429b716734141c722d3d192693b71d6297b6acd1faa1168768a088bd41b1`입니다. Disposition은
`corrected 21 / replaced 10 / discarded 6`, review mode는 `direct-content 33 / metadata-only 4`입니다.
원장의 `reviewed_at` `2026-07-20T10:07:26+09:00`은 publication 전 이미 끝난 content review의 시각을
소급해 만든 값이 아니라, repository owner가 disposition과 object를 다시 대조한 governance ledger 검증
시각입니다. Original content-review의 정확한 종료 시각은 별도로 기록되지 않았고 세 publication commit
전에 완료됐습니다.

위 37-row corpus 원장 밖의 legacy note 5개와 reflection 2개는 EOF를 포함한 blob byte가 exact임을 확인해
별도 내용 변경 없이 재사용했습니다. 최초 publication tip
`79dd60e9f88bd188a47e192024ba4956caaa9b05`는 project 자체 gate를 통과했지만 authenticated
remote-navigation에서 notes publication이 `docs/README.md`를 소유하지 않은 사실을 발견했습니다. 같은
전담 집필자가 일곱 본문을 다시 바꾸지 않고 실제 범위와 순서에 맞는 7-link learning 색인을
`docs/README.md`에 수작업 추가했습니다. Repository owner는 그 한 hunk와 일곱 target을 직접 읽고, 기존
answer/practice blob을 byte-identical하게 재사용해 세 publication commit을 actual time으로 다시
만들었습니다. 사용자 승인과 expected-old `79dd60e9f88bd188a47e192024ba4956caaa9b05` lease로
`learning/current`만 non-FF 교정했으며 source와 annotated tag는 이동하지 않았습니다. Old/final tip의
tree diff는 `docs/README.md` 10 additions 한 path뿐입니다.

Final `learning/current`는 source 뒤의 actual-time publication 세 commit으로만 구성됩니다.

| phase | commit | tree | parent |
| --- | --- | --- | --- |
| notes | `b004e104fe263818174ade3a4ee40387060af8fe` | `23920a9c0d792d29359e641a05319e49d8fdd5cd` | source `eaab17de0c56f236362b6e53ab0e8af6e650e5e7` |
| answers | `abd76ce5fd02b5767186d88ca7de43133d69d457` | `86916bf60676b38460048909b25a52df992a582f` | notes |
| practices / tip | `e34e3b400c2cceeea1880475f5ca264a3b96b8ab` | `84a81160c234b0b8bf88aa334e15cbdd213a7df2` | answers |

Final 수량은 learning tip에서 reachable한 `19 commits = 13 answers + 6 exclusions`,
`13 answers = 12 practices + omission 002`입니다. Exclusion은 source ordinal `009`–`011` 세 개와
publication ordinal `016`–`018` 세 개입니다. Remote는 branch `main`, `learning/current`와 annotated
`delivery-v1.0.1`만 advertise합니다. 교정 뒤 별도 fresh clone의 `learning/current`에서 lint, typecheck,
unit 19, docs 6, build 11, Chromium 1과 corpus checker를 포함한 `check:learning`을 통과했습니다. Exact
ref·tree, strict fsck, source drift 0과 clean status를 확인했고 authenticated 30-project 검사에서도
`frontend-delivery-training` project와 Frontend overlay, Central links가 PASS입니다. 같은 검사에 남은
다른 미완료 저장소 오류는 Delivery completion과 분리합니다.

### `cloud-launch-training` source product-token allowlist

| 저장소 | exact path | 허용 token·context | exact blob과 책임 commit | 제품상 이유·검토 근거 |
| --- | --- | --- | --- | --- |
| `cloud-launch-training` | `package-lock.json` | 소문자 `cursor`가 `cli-cursor` 또는 `restore-cursor` npm package name, dependency key, registry URL에 포함된 정확한 7 occurrence | blob `db938f6e72a5a49b6b31b3393beed5ea3b3e3a9c`, replay commit `aba9a7f1b58f2470d879d1fd81b66a6f137ac4da` | `firebase-tools → ora → cli-cursor → restore-cursor` terminal dependency chain을 frozen install에 고정한 lockfile 필드입니다. 일곱 줄의 package key, dependency와 registry URL을 직접 대조했으며 작업 도구 provenance가 아닙니다. |

이 allowlist는 위 exact path, blob과 일곱 dependency occurrence에만 적용합니다. 다른 path·blob의
`cursor`, 대소문자 변형, ref·tag 이름, commit·tag metadata·trailer 또는 tool-control artifact는 허용하지
않습니다. Final source graph를 전수 검사했을 때 이 일곱 줄 외 product token과 등록되지 않은 금지
provenance는 0건입니다.

### `cloud-launch-training` 실행 원장

2026-07-20 KST에 private `woopinbell/cloud-launch-training`을 사용자 승인과 exact lease를 사용한 단일
atomic push로 전환했습니다. Expected-old `main`은
`480e18b5b47cccf5fe0f38e6c5811fde567bdfe4`(tree
`b1300dc53ea6fac73453a92a095ae495e34ef918`)였고 replacement `main`은
`0b47343e9a3e472b11b5c254b5690f8a6a3ac8ab`(tree
`b5efe27f58156dd2e8ab4efe71f4a9da55fb0e33`)입니다. Annotated
`cloud-launch-v1.0.1` tag object `268aa5a58d62a822b8bf9d0cb721fe4ea857ebac`는 replacement
`main`으로 peel됩니다. Final source는 root `1ad172b8865e7b62ee15d45ac5d60666faa40369`부터 19개
linear commit이며 merge는 없습니다.

삭제하거나 교체한 source tag의 ref, object와 peeled target은 다음과 같습니다.

| ref | old tag object | old peeled target | disposition |
| --- | --- | --- | --- |
| `cloud-launch-v1` | `a2b68bd0c0cda5f20db8f641add436ba86a05375` | `4c6dd0b7a6405ebf6776879450cf67eb20945dba` | 삭제 |
| `cloud-launch-v1.0.1` | `20857ee56df971d3a1b5eb7a8cf181377dd971ef` | `480e18b5b47cccf5fe0f38e6c5811fde567bdfe4` | 위 final annotated object로 교체 |
| `pre-cloud-launch-v1` | `b04d2ca9bfca65dd3412bd8e1d08d4a08b056069` | `a87a61061e084bb05fa00f6ccff34d0d9c9128a0` | 삭제 |

20개 old source disposition은
[`data/migrations/cloud-launch-training-source-crosswalk.tsv`](data/migrations/cloud-launch-training-source-crosswalk.tsv)에
고정합니다. 파일은 header 포함 21줄이며 SHA-256은
`0d8a9b85d3b458cbda540d2b5e4540f0f4e97df499ec8ae05548f0daee680d39`입니다. Root 책임은 exact
object로 유지했고 old ordinal 003–015의 patch-id와 책임 순서를 보존했습니다. Old ordinal 002와
016–019는 source/config/test 계약의 실제 오류만 수동 교정했고, old ordinal 020
`480e18b5b47cccf5fe0f38e6c5811fde567bdfe4`는 source 기여가 없는 learner-navigation-only
commit이라 replacement graph에서 제외했습니다. 기존 개발 timestamp는 그대로 보존하거나 승인된
`2025-05-10`–`2025-05-16` KST window 안에 책임 순서대로 배치했습니다. Old main과 final tree의 차이는
`README.md`, `next-env.d.ts`, `next.config.mjs`, `package-lock.json`, `package.json`,
`tests/audit-commits.mjs`, `tests/docs.test.mjs`, `tests/source-docs.test.mjs` 여덟 path뿐이며 그 밖의
application feature source path는 byte-identical입니다. Source identity, author/committer timestamp 일치, three-section
message, trailer와 source ref·tag·path·blob·metadata의 등록되지 않은 금지 provenance 검사는 모두
0건입니다. 위 product-token allowlist 일곱 occurrence만 별도로 통과합니다.

전환 전 source-only rollback bundle은 다음 값으로 검증했습니다.

- 경로:
  `/Users/woopinbell/Documents/Codex/2026-07-19/1/work/frontend-lane/cloud-launch-training/cloud-launch-training-480e18b5-source.bundle`
- SHA-256: `594e6cd4bb14c35e6b7f980a85c6b26ceac2bb5b1f2f570b635a51b6fd6f2271`
- 범위: old `main`과 old source tag 3개, learning ref 0개
- 복원 검증: bundle verify, 네 ref exact 대조와 restore clone의 strict fsck 통과

Project와 governance publication 뒤 authenticated Cloud project, Central Cloud anchor와 Frontend
application overlay가 모두 PASS했고, 공식 30-project 검사에서도 Cloud project·overlay·Central links가
PASS임을 확인했습니다. 이에 따라 2026-07-20T18:09:14+09:00에 위 bundle, source-only snapshot과 restore
clone을 함께 폐기했습니다. 이 migration 전 source를 보장하는 offline rollback artifact는 남아 있지
않습니다. Learning branch는 사용자 결정대로 bundle, archive ref 또는 보존 tag를 만들지 않았으며, 이전
all-refs bundle도 publication 전에 폐기했습니다.

Learning 후보와 단일화 근거는 다음과 같습니다.

| old ref | tip | tree | total paths |
| --- | --- | --- | ---: |
| `learning/cloud-launch-v1` | `94a69c837a53cb01ac0e29f25fd728517719d2de` | `c1788b6775133b53aafd1c0224b4023f6a12cf71` | 104 |
| `learning/cloud-launch-v1.0.1` | `c13b944e41f7b3cbf4f6949636e2104218dc48a3` | `ae44708fdf4a3b0312af06d2f4785f282520d205` | 107 |

두 tip은 ancestor 관계가 아니지만 공통 104 paths 중 93개 blob이 같고 11개가 divergent이며,
`learning/cloud-launch-v1.0.1`에 canonical-only path 3개가 있습니다. Source 호환성, commit coverage와
metadata를 대조해 v1.0.1을 canonical legacy basis로 선택했습니다. Canonical basis의 learning-only 50개
path disposition은
[`data/migrations/cloud-launch-training-learning-disposition.tsv`](data/migrations/cloud-launch-training-learning-disposition.tsv)에
고정합니다. 파일은 header 포함 51줄이며 SHA-256은
`f38ec57103a4d225465671a41172e8700c24dcbf8f4940ad4f23e6efccf29bd6`입니다. Disposition은
`corrected 36 / replaced 3 / discarded 1 / adopted 10`, review mode는
`direct-content 40 / oid-identical 10`입니다. 원장의 `reviewed_at`
`2026-07-20T17:43:52+09:00`은 과거 content-review 종료 시각을 재구성한 값이 아니라 repository owner가
disposition, path와 object를 다시 대조한 governance ledger 검증 시각입니다.

Notes 9개와 reflection 1개는 old/final blob·byte가 exact라 다시 읽지 않고 채택했습니다. Answer
`001`–`019`를 final source에 직접 대조했고, 전체 answer barrier 뒤 practices `002`–`017`, `019`를
확정했습니다. Old answer `020`은 대응 source 책임이 없어 폐기했습니다. Final omissions는 `001`,
`018`입니다. 따라서 `19 reachable source commits = 19 answers + 0 exclusions`,
`19 answers = 17 practices + 2 omissions`입니다. Final learning-only path는 49개이고 source 58개와 합친
tracked path는 107개입니다.

Final `learning/current`는 final source 뒤의 actual-time publication 세 commit으로만 구성됩니다.

| phase | commit | tree | parent |
| --- | --- | --- | --- |
| notes | `b02ee59ed32d6aa9d0a2306e00aa680aea3a1940` | `993e895f853d92e5ff001b14be6d066d2616bcc7` | source `0b47343e9a3e472b11b5c254b5690f8a6a3ac8ab` |
| answers | `9d714abfaea3803f39b2976cd5ab982161a9905f` | `d845137f7dc49b9bd0da8cab34b2fa801385952e` | notes |
| practices / tip | `cd266d629e172d4be2af0237a91dcf09eada0b3c` | `33302a868f66a4d67387c40faf847e66a1469265` | answers |

Remote는 branch `main`, `learning/current`와 annotated `cloud-launch-v1.0.1`만 advertise합니다. Local과
별도 private fresh clone의 `learning/current`에서 source audit 19개, unit/source-doc 18개, Emulator와
config 6개, production build 10 routes, Chromium·Firefox·WebKit 30개, corpus 8개 검사를 포함한 전체
`make check-learning`을 통과했습니다. Exact ref·tree, annotated tag, strict fsck, source drift 0과 clean
status도 확인했습니다. Authenticated remote-navigation의 Cloud project, Frontend application overlay와
Central links는 PASS입니다. 같은 전체 검사에서 아직 migration 전인 `frontend-reliability-training`,
`portfolio-site`, `sportsbook-shared-protocol`의 다섯 오류만 별도로 남았으며 Cloud completion과 분리합니다.

### `frontend-reliability-training` source product-token allowlist

`frontend-reliability-training`의 final source에는 AI 작업 provenance가 아니라 제품 동작을 뜻하는 소문자
`cursor`만 남습니다. 허용 범위는 아래 exact path, blob, occurrence와 그 blob을 처음 도입한 replay
commit으로 한정합니다.

| exact path | exact blob | occurrence | 책임 commit | 제품상 이유 |
| --- | --- | ---: | --- | --- |
| `react-main/src/shared/components/Button.tsx` | `41cf3fd9e828be04169398edb0faf4e214de4ab4` | 1 | `04396f821ce7046d018f04ed6b64c4b6e5f3e875` | Tailwind `cursor-not-allowed` disabled styling |
| `react-main/src/advanced/design-system/components.tsx` | `01bfa80d89db584f2a6fe5c436f533b0ffa7e15e` | 1 | `1d5c69694ec470b53e2e11cf61f702786872a690` | Tailwind `cursor-not-allowed` disabled styling의 최초 blob |
| `react-main/src/advanced/design-system/components.tsx` | `086c6995f27afd681dd93d2daba6f521f2189b82` | 1 | `365eda6f3739e3d6a46fb5eab3c0dc1ed0c9f4b9` | 같은 제품 styling의 후속·final blob |
| `react-main/src/advanced/complex-filtering/Exercise.tsx` | `a1cb838a8f346ed8eafccf13ef23969bb14e099e` | 2 | `7926f775df06539d69b4863fc3959d2655afc616` | 두 disabled control의 Tailwind `cursor-not-allowed` styling |
| `react-main/src/advanced/realtime-dashboard/README.md` | `bd09642e103732777ffb5d5832f4d714ede5f642` | 1 | `372cf5cbc517cf9854a94324f23d308b8edede3b` | reconnect replay의 per-topic sequence cursor 설명 |
| `react-main/src/advanced/realtime-dashboard/README.md` | `863ab411daa390aeff8b92837499c36fc4094d0c` | 1 | `b159e0487638a5be344cdd3e3b00620b784461fe` | 같은 제품 개념의 후속 blob |
| `react-main/src/advanced/realtime-dashboard/README.md` | `1bd96d224924b5e2f7119066548d4238fb9cee4d` | 1 | `900754d9b89afde00d0e66ecdbacb816856c247c` | 같은 제품 개념의 final blob |
| `react-main/src/advanced/realtime-dashboard/Exercise.tsx` | `a196af77c8fbad83a8cef8536735e32c5408075d` | 4 | `275448e09e11d2ef1c4a5b52ae335ec1a582ae02` | event stream의 현재 sequence 위치 state와 갱신 로직 |

Historical source graph 전체에서는 8개 blob의 12 occurrence이고 final tree에서는 5개 path의 9
occurrence입니다. 다른 path·blob의 `cursor`, 대소문자 변형, ref·tag 이름, commit·tag
metadata·trailer 또는 tool-control artifact에는 이 allowlist를 적용하지 않습니다. Final source의 ref,
path, commit metadata·본문·trailer와 blob을 전수 검사했을 때 이 제품 token 외 금지 provenance는
0건입니다.

### `frontend-reliability-training` 실행 원장

2026-07-20 KST에 private `woopinbell/frontend-reliability-training`을 사용자 승인과 모든 ref의 exact
lease를 사용한 단일 atomic push로 전환했습니다. Expected-old `main`은
`1e340a517e6e0f2961bb49ea4a351a98b64532f4`(tree
`a5d2fbd988b3dd38449192f8c4bc33d122061ffd`)이고 replacement `main`은
`a8516228a4c04456c309af267ba72af0fa4acab2`(tree
`f4026f392f3c73445db9e88cbc9b676a48d6ad98`)입니다. Final source는 root
`fed83e4b2e08eb186f8275175107c26d86e10860`부터 140개 commit이며 merge는 23개입니다. Annotated
`reliability-v1.0.1` tag object `725b363abf4171e4a1ac737d0d765989cfee3a39`는 replacement
`main`으로 peel됩니다.

삭제하거나 교체할 source tag의 exact object와 peeled target은 다음과 같습니다.

| ref | old tag object | old peeled target | disposition |
| --- | --- | --- | --- |
| `legacy-feature-graph-v1` | `5d94f63540204338fd58cbc0ab102ee08ee30bda` | `b4904bdb3c795458d56b2b7a19d83a31e6dffef2` | 삭제 |
| `pre-codex-5.6` | `b290decd03f4c3c7096240a1b161c9d7e14a8525` | `7e08ddf6d43690b5bb451840ef5a7dbd09d673c7` | 삭제 |
| `reliability-v1` | `4eb88e7b3056e349df1e1cf0702c68bd0d33aec1` | `1988796e6d246bf58430934edc85305bab0eaddf` | 삭제 |
| `reliability-v1.0.1` | `ac87ae51d63b2a12206fd97f36b831b5b5e02133` | `1e340a517e6e0f2961bb49ea4a351a98b64532f4` | final annotated object로 교체 |

141개 old source disposition은
[`data/migrations/frontend-reliability-training-source-crosswalk.tsv`](data/migrations/frontend-reliability-training-source-crosswalk.tsv)에
고정합니다. 파일은 header 포함 142줄이며 SHA-256은
`9730fdb1c765ac7f4a92c9eeb2589b3216b0520d583f664e7b80b1c96d95e5a9`입니다. 140개 책임은 원래
topology와 patch 순서를 유지해 승인된 `2025-05-17`–`2026-01-16` KST window에 배치했고, old final
`1e340a517e6e0f2961bb49ea4a351a98b64532f4`는 source 기여가 없는 learner-navigation-only commit이라
제외했습니다. Old와 replacement main의 tree 차이는 `README.md`, `docs/DESIGN.md`, `docs/README.md`
세 source-owned 문서뿐이며 application source, config와 test는 byte-identical합니다. Source identity,
author/committer timestamp 일치, 책임 순서, three-section message, trailer와 등록되지 않은 금지
provenance 검사는 모두 통과했습니다.

원격 전환 전 source-only rollback bundle은 다음 값으로 검증했습니다.

- 경로:
  `/Users/woopinbell/Documents/Codex/2026-07-19/1/work/frontend-lane/frontend-reliability-training/frontend-reliability-training-1e340a51-source.bundle`
- SHA-256: `9f08785feb0b126647b48ba56c6adce155df308ab151c087098ae570f954b6e6`
- 범위: old `main`과 old source tag 4개, learning ref 0개
- 복원 검증: bundle verify, 여섯 advertised ref exact 대조, restore clone의 strict fsck 통과

두 legacy learning ref까지 담았던 all-refs bundle
`frontend-reliability-training-1e340a51.bundle`(SHA-256
`4256bbda8a7cec8196debefbf9bfcfa7cf59ce730be0dea4666a5090656918fa`)은 사용자 결정에 따라 원격
publication 전에 폐기했습니다. Learning branch는 bundle, archive ref 또는 보존 tag를 만들지 않습니다.
Project·governance publication, authenticated navigation과 별도 private fresh-clone 전체 gate가 모두
green이 된 뒤 `2026-07-20T20:13:28+09:00`에 위 source-only bundle, snapshot과 restore clone을
폐기했습니다. 따라서 이 migration 전 source를 보장하는 offline rollback artifact는 남아 있지 않습니다.

Learning 후보와 단일화 근거는 다음과 같습니다.

| old ref | tip | tree | total paths |
| --- | --- | --- | ---: |
| `learning/reliability-v1` | `b93d990d21447b03cfea416ea2de16e00b62deb4` | `c63ca7b1bd81cddc452e0db962a33181ce7dc583` | 699 |
| `learning/reliability-v1.0.1` | `4be1f7741030818e723351162618ee94e2c47e80` | `c11737f9d9b1a4acdcf9b14c3eb14c94abaaa9ab` | 702 |

두 tip은 ancestor 관계가 아닙니다. 699개 공통 path 중 source-owned `README.md`, `docs/DESIGN.md`,
`docs/README.md` 세 blob만 다르고 696개는 identical이며, v1.0.1에는 release-specific answer/practice
index와 navigation answer 143의 세 path가 추가됩니다. Current source 호환성, commit coverage와 metadata를
대조해 v1.0.1을 canonical legacy basis로 선택했습니다. 두 branch의 동일 blob은 재독하지 않았고,
고유·충돌 blob과 final source patch의 영향을 받는 answer/practice만 직접 검토했습니다.

Canonical basis의 513개 path disposition은
[`data/migrations/frontend-reliability-training-learning-disposition.tsv`](data/migrations/frontend-reliability-training-learning-disposition.tsv)에
고정합니다. 파일은 header 포함 514줄이며 SHA-256은
`e6295422f00f3ce3efd1d489b4a950f8ce2eff3ce316d1cb6793781af5f8e0dc`입니다. Disposition은
`adopted 328 / corrected 177 / replaced 3 / discarded 5`, review mode는
`oid-identical 328 / metadata-only 174 / direct-content 11`이고 `PENDING`은 0입니다. 원장의
`reviewed_at` `2026-07-20T19:39:37+09:00`은 과거 content-review 시각을 재구성한 값이 아니라 repository
owner가 disposition, source crosswalk와 object를 최종 대조한 governance 검증 시각입니다.

Final `learning/current`는 final source 뒤의 actual-time publication 세 commit으로만 구성됩니다.

| phase | commit | tree | parent |
| --- | --- | --- | --- |
| notes | `09fce2f8a54343970a57db12920b47739237eb39` | `d4319c5360d51d5b529a56dae805cfdc666b1748` | source `a8516228a4c04456c309af267ba72af0fa4acab2` |
| answers | `a4dbce445ca2bd954b481f2ed195e2e44720d2ed` | `1cf0499cc91d2fa32d42b477ed6a59c08e222943` | notes |
| practices / tip | `43ff06851c55b2eb299fb1b36d9de2b2e25afe50` | `509fcb1185bdf8e9a8f7369196da06fb5a9c2cc4` | answers |

Final 수량은 `140 reachable source commits = 115 answers + 25 exclusions`,
`115 answers = 61 practices + 54 omissions`입니다. Exclusion은 source merge 23개와 source-owned document
책임 2개입니다. Local과 별도 private fresh clone의 `learning/current`에서 Node 22.22.0, pnpm 10.32.1
frozen install, repository guard, lint, typecheck, React·Next unit 80개, 두 production build, Playwright
6개와 corpus audit 47개를 통과했습니다. Exact ref·tree, annotated tag, strict fsck, source drift 0과 clean
status도 확인했습니다. Remote는 branch `main`, `learning/current`와 annotated `reliability-v1.0.1`만
advertise합니다. Document Box `298687b6dd6645d22ad33392b4eaebf696c58860`의 authenticated
remote-navigation에서 Reliability project, Frontend application overlay, ref snapshot과 Central links가
모두 PASS했습니다. 같은 전체 검사에 남은 `portfolio-site`와 `sportsbook-shared-protocol`의 네 오류는
아직 완료되지 않은 다른 저장소 publication 문제이며 Reliability completion과 분리합니다.

### `portfolio-site` source product-token allowlist

`portfolio-site`의 final source에는 작업 provenance가 아니라 UI와 pagination 제품 동작을 뜻하는 소문자
`cursor`만 남습니다. 허용 범위는 아래 exact path, blob과 occurrence로 한정합니다.

| exact path | exact blob | occurrence | 제품상 이유 |
| --- | --- | ---: | --- |
| `src/designs/editorial/editorial-route.module.css` | `4ef379393957dc098f035f43811e075ec5c290d9` | 1 | pointer cursor styling |
| `src/designs/brutalist/brutalist.module.css` | `604157ca27d5dec9c0cf335c73187dc8f1dda704` | 1 | pointer cursor styling |
| `src/designs/cinematic/cinematic.module.css` | `6074765b87493850d4808f2c15012e6372fcc182` | 1 | pointer cursor styling |
| `src/components/portfolio/design-switcher.module.css` | `9f048004d5c38b20718241ea0ddd7758c1e56770` | 2 | clickable selector cursor styling |
| `src/content/projects.json` | `a641c187f89bb9d6527b65c2c8df22e7021a715d` | 3 | pagination cursor 설계 설명 |
| `src/components/portfolio/site-shell.tsx` | `e9bc83a9c2d0f5273a987b54e3b6e02594ff4c3b` | 1 | navigation pagination cursor 설명 |

Source union 전체에서 6개 blob의 9 occurrence입니다. 다른 path·blob의 `cursor`, 대소문자 변형,
ref·tag 이름, commit·tag metadata·trailer와 tool-control artifact에는 이 allowlist를 적용하지 않습니다.
Final source의 ref, path, commit metadata·본문·trailer와 blob을 전수 검사했을 때 위 제품 token 외 금지
provenance는 0건입니다.

### `portfolio-site` 실행 원장

2026-07-20 KST에 private `woopinbell/portfolio-site`를 사용자 승인과 모든 ref의 exact lease를 사용한
단일 atomic push로 전환했습니다. Expected-old `main`은
`ff4e1854fabe7d061278044033c41383dc5cb2cd`이고 replacement `main`은
`38f61b1a405d1e1e72342f290cf36cdf6b1ef111`(tree
`5ef4beb998ac68bcb5b337cffe2e7ab020383afd`, parent
`049496ffd7d50f0ec2ae745d1e613c04560a1e05`)입니다. Final current source는 42개 commit이고 historical
release 세 개를 합친 source union은 45개 commit, resolution-free merge는 5개입니다. 38개 commit은
three-section message를 사용하고 empty root, lockfile-only와 merge 5개 등 7개는 승인된 예외입니다.

네 source release의 old/new annotated tag object와 peeled target은 다음과 같습니다.

| ref | old object → peeled | final object → peeled |
| --- | --- | --- |
| `template-v1` | `ed6e74ad90d734266bb1550be6480d3f22d54e1a` → `fb0a4b9661de7f4544754b384a5c4a3ed9dda12e` | `bf531c9c628fd623cfc0b1ec87de13b54b31402d` → `847f10e27aeda6871d66e5a76ae16087cf569993` |
| `portfolio-v1` | `6bd1265ba870bb4ccf3028a5b61249ef0a4c305f` → `8159dc3dd7cf6d0b304834806c0e2f834c12048b` | `59db3a6dcc219a7bb7cdd57318a004c9c5b9232d` → `63c4aecd756e29abf1570253451f79c949625725` |
| `template-v2` | `f7afc175e28eac5aefb218338d3aba87e375e2f4` → `5f4301c976bb3d6659c4dd85a568df1ccd572530` | `210375d9f052bfb0af7a2d8916f30b691ac17f14` → `28e39ba95d7414f80b510fa1cac644f660ec801b` |
| `portfolio-v2` | `d6937e28e0c81347cf09c9a2f0cbce0c25ef13d4` → `a69b0ad9d4decb3f60f806766f7ee4e4e2f27421` | `246a23166fb32769e31848d599449864b8b271e9` → `b0d4f7c5071e17a231890bb82a14728950e189f5` |
| `template-v3` | `46edd4271db5eb1507e3e3ee7e6bfd9c16e293b6` → `82df0f245e55120d87e45b3fe648ea6eee240f0e` | `7f2e06bdab688523d518a767b4609d4c0212bf53` → `f5bd465b08f79db815605e87e4d67eae65719389` |
| `portfolio-v3` | `cc4be3105fb15431cc3313c7176fbc68970d06f7` → `3f90d20cdc7a43b8af9e27414f3a58a2a70cf80e` | `6a0727c719601cba79475161ab5d6b5ccc291392` → `10076d214bd232ebf2a306a89f6fcba10b7a83a5` |
| `template-v3.0.1` | `7c683a9e039ba7796b0aceb84d26153158ca3991` → `05e81cd168e9b0bbc1d7d1428ab0e0df1fe5cf14` | `ece83dc0d55fd2ff346af6e9400ed35b8eb69faa` → `049496ffd7d50f0ec2ae745d1e613c04560a1e05` |
| `portfolio-v3.0.1` | `7914062a57542cbfdcdff67536a418da79ae9f2f` → `ff4e1854fabe7d061278044033c41383dc5cb2cd` | `66bef79b6020d68af3da014489b226bc2e09ee36` → `38f61b1a405d1e1e72342f290cf36cdf6b1ef111` |

각 final `portfolio-*` peeled commit의 단일 parent는 같은 버전 `template-*` peeled commit입니다. Source
README와 `docs/DESIGN.md`에서 learner navigation을 제거하고 reset·license·hydration·release 계약만
유지했습니다. Content publication 네 개의 diff는 `src/content/**`, `public/content/**`에만 있으며,
`public/content/site/og.png`의 legacy blob `48a24ec75635212a2e0a496abdfc76e1afc809f8`에서 C2PA tool
metadata만 제거한 clean blob `f120316ea012c651d2bcc6da144b9e4486355547`을 사용합니다. ImageMagick
pixel 비교는 `0`이므로 decoded visual은 동일합니다.

45개 old/new source disposition은
[`data/migrations/portfolio-site-source-crosswalk.tsv`](data/migrations/portfolio-site-source-crosswalk.tsv)에
고정합니다. 파일은 header 포함 46줄이며 SHA-256은
`1b3e153aa388d04b8d2a82eb754c47f68fa5b4a4609344839cfbb8457a07966c`입니다. 원래 topology와 patch
순서를 보존하면서 승인된 `2025-10-06`–`2025-11-28` KST window에 배치했고 source identity,
author/committer timestamp 일치, tagger timestamp, message, trailer와 provenance gate를 모두
통과했습니다.

원격 전환 전 source-only rollback bundle은 다음 값으로 검증했습니다.

- 경로: `/Users/woopinbell/Documents/Codex/2026-07-19/1/work/bundles/portfolio-site-source-ff4e1854.bundle`
- SHA-256: `2df31089f019b1b7ba674317e4e16f299776ecca27d8cf3cede907d54f7ed137`
- 범위: old source branch 2개와 source tag 8개, learning ref 0개
- 복원 검증: bundle verify, source ref 10개 exact 대조와 restore clone strict fsck 통과

Learning ref를 포함했던 all-refs bundle은 publication 전에 폐기했고 learning bundle, archive ref 또는
보존 tag는 만들지 않았습니다. Project fresh-clone, Document Box `c55d6de9c49c752d9e7aec61385be6bcfb99196d`,
Central Notes `077283d6f7073ac97b0e1a0689d855cde10cd0c9`, authenticated remote-navigation과 closure 검사가
모두 green이 된 뒤 `2026-07-20T22:16:57+09:00`에 위 source-only bundle, restore clone, audit
mirror/candidate와 검증용 worktree·fresh clone을 폐기했습니다. 따라서 migration 전 Portfolio source를
보장하는 offline rollback artifact는 남아 있지 않습니다.

Learning 후보의 path/blob/tree matrix는 다음과 같습니다.

| old ref | tip | tree | learning corpus paths |
| --- | --- | --- | ---: |
| `learning/portfolio-v1` | `d40b2d51b50209524b103a69890e7bc20eca9365` | `f9e85943784e5e1dce037c56ac2e245b96241aed` | 51 |
| `learning/portfolio-v2` | `5c289930a40e235b681ebab015349cea45dba608` | `e290497b2b0fbc11730c7161846692a39d6afb54` | 59 |
| `learning/portfolio-v3` | `7cfaae14b960cf5b89138660a2ebe8bf094db4af` | `7a3c92bda97867c983de2af1c629fffbfc9b6195` | 64 |
| `learning/portfolio-v3.0.1` | `21bb76a7bb19e0cd01afe350d329900c39ce5f0c` | `7c5e9548fac355eda6a634dcfd34c2997249eb01` | 68 |

네 tip은 ancestor 관계로 우열을 정할 수 없습니다. v3.0.1은 v3 canonical corpus 64개 blob을 전부 그대로
포함하고 v3.0.1 answer 두 개와 versioned wrapper 두 개만 추가하므로 canonical donor로 선택했습니다.
v1→v2와 v2→v3의 canonical 충돌은 ledger README뿐이고 동일 blob은 재독하지 않았습니다. Reserved
historical content ID `026`, `032`, `036`은 active corpus에서 제거하고 정화된 source tag가 release
evidence를 보존합니다.

네 ref의 learning corpus 242개 path disposition은
[`data/migrations/portfolio-site-learning-disposition.tsv`](data/migrations/portfolio-site-learning-disposition.tsv)에
고정합니다. 파일은 header 포함 243줄이며 SHA-256은
`fe6eadda56c605a18af1d8257aeee03f3b40247a6f8dd8d73334d08996e78a69`입니다. Disposition은
`corrected 228 / replaced 8 / discarded 6`, review mode는 `metadata-only 196 / direct-content 46`이고
`PENDING`은 0입니다. 원장의 `reviewed_at` `2026-07-20T21:56:02+09:00`은 과거 집필 시각이 아니라
repository owner가 old/final blob, source crosswalk와 publication basis를 최종 대조한 governance 검증
시각입니다.

Final `learning/current`는 final source 뒤 actual-time publication 두 commit으로만 구성됩니다.

| phase | commit | tree | parent |
| --- | --- | --- | --- |
| answers | `6757af78f48ede995a801c21dd9d53c28c6c8aef` | `340d1ce545a94c4ca03f0ee481d1dc5c8dcb406c` | source `38f61b1a405d1e1e72342f290cf36cdf6b1ef111` |
| practices / tip | `6d720c187bf8690b3b0cca499e61dd685bb867a1` | `7b9cc579713af18e3371316022dc77001659e751` | answers |

Final 수량은 `42 reachable source commits = 35 answers + 7 exclusions`, `35 answers = 28 practices + 7
omissions`, `44 final learning reachable = 42 source + 2 publication`입니다. Local과 별도 private fresh
clone의 Node 22.22.0 clean install에서 content 16 projects/5 designs, content-only 61 paths, lint,
typecheck, Vitest 38개, Turbopack·Webpack production build 26 pages, Playwright/visual 27 pass와 의도된
desktop skip 1을 통과했습니다. Exact branches·tag object·peeled target, strict fsck, source provenance,
learning path allowlist, corpus metadata·link·count와 clean status도 확인했습니다. Remote는 branch
`main`, `learning/current`와 위 annotated source tag 8개만 advertise합니다. Authenticated
30-project remote-navigation에서 Frontend 프로젝트 5개, Portfolio strict topology, Frontend application
overlay, ref snapshot과 Central links는 모두 PASS했습니다. 같은 전체 검사에서 남은
`sportsbook-shared-protocol`의 `docs/README.md` publication/404 두 오류는 Backend lane 문제이며
Frontend closure와 분리합니다. Frontend 전용 authenticated preflight는 private repository 접근과 도구
검사를 포함해 PASS했습니다.

### `backend-foundations-training` source product-token allowlist

Final source의 `cursor`는 작업 provenance가 아니라 pagination 제품 계약입니다. 허용 범위는 다음 exact
path와 blob에 한정하며, 다른 ref·path·metadata·trailer·blob에는 적용하지 않습니다.

| exact path | exact blob | 제품상 이유 |
| --- | --- | --- |
| `notes/reference-impl/spring-data-commons-pagination/README.md` | `44552ae1a8bcb76158e94ba86d8948ecd48cfea5` | source commit `2353925fb126d8f2c98e3e22cb1a3c771ac1c60e`에서 도입된 historical cursor pagination 설명과 HTTP 예시 |
| `notes/reference-impl/spring-data-commons-pagination/README.md` | `5707799959a52ad67df4a2933c658d806e30c737` | cursor pagination 설명과 HTTP 예시 |
| `notes/reference-impl/spring-data-commons-pagination/src/main/java/com/example/refsdcpag/ArticleController.java` | `1dfda2e8161993dd9b994f127a6a16bb7e8ac5cd` | cursor endpoint |
| `notes/reference-impl/spring-data-commons-pagination/src/main/java/com/example/refsdcpag/ArticleRepository.java` | `8abf62c62c85086105bac19ba368e87b6917aa5f` | keyset query boundary |
| `notes/reference-impl/spring-data-commons-pagination/src/main/java/com/example/refsdcpag/ArticleService.java` | `b657c9037c11c756149efb5eeccde0fa7efad7bd` | cursor state와 next cursor 계산 |
| `notes/reference-impl/spring-data-commons-pagination/src/main/java/com/example/refsdcpag/Models.java` | `6dc8f6ee94b9c07972ad1e83986c1eac277f0395` | cursor response model |
| `notes/reference-impl/spring-data-commons-pagination/src/test/java/com/example/refsdcpag/ArticlePaginationTest.java` | `5eb47aff8c77c8b2ab6093868659a7f4e633a890` | cursor 진행·연속성 검증 |

위 일곱 blob 외 source ref·tag, commit/tag metadata·본문·trailer, path와 blob의 금지 provenance는 0건입니다.

### `backend-foundations-training` 실행 원장

2026-07-20 KST에 private `woopinbell/backend-foundations-training`을 사용자 승인과 모든 ref의 exact
lease를 사용한 단일 atomic push로 전환했습니다. Expected-old `main`
`432b43bc42af8daeef62ad6ac8fbef13f52eb41f`은 replacement `main`
`0fa98e5775ddf2862735ff5d23a56fe3a1f5cbf6`으로 이동했습니다. Authenticated navigation이 source
README의 canonical 단계 카드 역링크 누락을 발견해 2026-07-21 KST에 exact lease와 별도 source-only
bundle로 세 ref를 다시 atomic 교정했습니다. Final `main`은
`a81d00757aaa679a66391512fac62a8e09c155bd`(tree
`69d907b14a89626034e93d2c637964e8627a6dc3`)입니다. Final source는 104개 commit, first-parent
34개와 merge 24개이며 승인된 `2024-11-01`–`2025-01-31` KST window, canonical identity,
author/committer timestamp 일치, parent chronology, message·trailer gate를 통과했습니다.

Current annotated release `foundations-v2.0.1`은 old object
`742c2dd8113e6ecb661e3a934d44f054bb6afaa0`(peeled old main)에서 initial clean object
`6eb6ddc787b0d53e938b9aa073dcdc2368b6b506`을 거쳐 final object
`3e5bf07228d149065af2b5a2f0a0e82b33b5fe86`(peeled final main)으로 교체했습니다. Legacy source tag
`foundations-v1`, `foundations-v2`, `pre-foundations-v1`은 승인된 exact object에서 삭제했습니다.

110개 old source commit의 disposition은
[`data/migrations/backend-foundations-training-source-crosswalk.tsv`](data/migrations/backend-foundations-training-source-crosswalk.tsv)에
고정합니다. Header 포함 111줄, SHA-256
`7ba7a7b2be15994a669c732849e624e3efae6f6671d9f6713b8d5395405f8643`이며 104개 retained와 6개
excluded row가 old graph 전체를 닫습니다. Checker와 Spring JSON repair는 원래 책임에 흡수했고,
learner-navigation-only tip의 canonical 카드 역링크는 source-navigation 책임에 흡수하고 나머지 절차는
source에서 제외했습니다. Final source/config/test diff는 정화 대상
`README.md`와 `docs/DESIGN.md` 외 old current release와 동일합니다.

원격 전환 전 source-only rollback bundle은 다음 값으로 검증했습니다.

- 경로: `/Users/woopinbell/Documents/Codex/2026-07-19/1/work/backend-lane/backend-foundations-training/backend-foundations-training-432b43bc-source.bundle`
- SHA-256: `29f74219352c140abc1358f0b42991bed5f4a732f7e11a7edf37739e6343da1f`
- 범위: old `main`과 source tag 4개, learning ref 0개
- 복원 검증: `git bundle verify`, restore clone `git fsck --full` 통과
- lifecycle: project fresh clone, governance pointer와 authenticated Backend Foundations navigation이 PASS한 뒤 2026-07-21 KST에 삭제; checksum과 범위만 원장에 보존

역링크 교정 전 공개 source의 별도 rollback bundle도 learning ref 없이 검증했습니다.

- 경로: `/Users/woopinbell/Documents/Codex/2026-07-19/1/work/backend-lane/backend-foundations-training/backend-foundations-training-0fa98e-source-correction.bundle`
- SHA-256: `8c337e15e4279211ab42ee2c92c8f440da3b6628cd98541cd6e922fc3a9c5f55`
- 범위: correction 전 `main` `0fa98e5775ddf2862735ff5d23a56fe3a1f5cbf6`과 annotated tag object `6eb6ddc787b0d53e938b9aa073dcdc2368b6b506`
- 복원 검증: explicit ref restore와 `git fsck --full --strict` 통과
- lifecycle: 같은 closure gate 뒤 2026-07-21 KST에 삭제; learning bundle은 만들지 않음

Learning branch 세 개는 ancestor 관계가 아니지만 corpus path/blob 포함관계는 v1 → v2 → v2.0.1입니다.
동일 blob은 재독하지 않고 canonical v2.0.1의 고유·충돌 파일과 source basis가 바뀐 hunk만 직접
검토했습니다.

| old ref | tip | tree | disposition |
| --- | --- | --- | --- |
| `learning/foundations-v1` | `d7f50a1e08c08892c5af8704971fe6b15091acc5` | `7ddcbb50be57ee22641fbf3609da926125b484aa` | v2.0.1에 path/blob 포함; 삭제 |
| `learning/foundations-v2` | `f3ff5588485497150dbd382eb709777cf84de8f1` | `9a9afb4820071ef7a9fecbcc6fcfca9a133c2187` | v2.0.1에 path/blob 포함; 삭제 |
| `learning/foundations-v2.0.1` | `b39f0a55bee761e3a88fbd2e6f82252f0a977689` | `d09b54405c4683d3a7488164895cb31a04c0fb14` | canonical donor; 단일화 뒤 삭제 |

Learning bundle, archive ref와 보존 tag는 만들지 않았습니다. Final `learning/current`는 source 뒤의
actual-time publication 세 commit으로만 구성됩니다.

| phase | commit | tree | parent |
| --- | --- | --- | --- |
| notes | `fd047dbdd73888e6ef85018cf728e94eb1cc8046` | `5c2d65f5b1f6675a00241a996c6fc66cfd35b7ee` | source `a81d00757aaa679a66391512fac62a8e09c155bd` |
| answers | `e4b6eb314211992ce38af1e4e50270bc15f88b2c` | `8bef9a42c7bb9f0be8f966a8b3b862ed46b6d4d9` | notes |
| practices / tip | `8b5de54384fd853e78ae57e31bfdce226eccf2d3` | `b8599637a0269622c9ede96caad89626ecb9e098` | answers |

Final 수량은 `104 source = 78 answers + 26 exclusions`, `78 answers = 47 practices + 31 omissions`입니다.
Reserved ID `095`, `097`, `100`, `107`은 active path에서 제거하고 index에 근거를 남겼습니다. 별도 private
fresh clone에서 branches가 `main`, `learning/current`뿐이고 annotated tag는 `foundations-v2.0.1` 하나임을
확인했습니다. Source strict fsck·provenance, Spring 52 tasks, Go packages, 21 exercise document contracts,
17 standalone reference implementations, Compose static configuration과 learning metadata·link·count·path
gate가 모두 통과했습니다. Authenticated 30-project 검사에서 Backend Foundations는 PASS이고 남은 두
오류는 후속 `sportsbook-shared-protocol`에만 속합니다. 두 source-only bundle은 이 B1 closure 뒤
삭제했으며 checksum과 복원 범위만 위 원장에 남겼습니다.

### `backend-delivery-training` 실행 원장

2026-07-21 KST에 private `woopinbell/backend-delivery-training`의 source와 learning ref를 모든 ref의
exact lease를 사용한 단일 atomic push로 전환했습니다. Expected-old `main`
`af7ba0aa827862991b2e405ad36bcc7dea924ed6`은 replacement `main`
`fc9e1d3dc36415b4d6e7287d3738b4c1c9136364`(tree
`be1fda88eb5fed37e9fd941bb13204f76cc78121`)로 이동했습니다. Final source는 linear 11개 commit,
merge 0개이며 승인된 `2025-02-01`–`2025-02-14` KST window, canonical identity,
author/committer timestamp 일치, `09:00`–`21:59` KST 시간대, parent chronology와 message·trailer gate를
통과했습니다. Source ref·tag·commit metadata·tracked path와 blob의 금지 AI provenance는 0건입니다.

Current annotated release `delivery-v1.0.1`은 old object
`6c4a4af648390f4199d6fa741a30c9e67286e879`(peeled old main)에서 final object
`69ccd5daedfae45c1d8871468d6e2c74d1ae8d5d`(peeled final main)로 교체했습니다. 다음 legacy source tag는
승인된 exact object에서 삭제했습니다.

| ref | old tag object | old peeled target |
| --- | --- | --- |
| `delivery-v1` | `60d0f8dc26b6ca36e176fc3a315da1884096942b` | `66b095b7bf34a114b99f14ea80bd75763ef60eed` |
| `pre-delivery-v1` | `dcdc5ee4b945bfccbb30957d9d21e441218f84a3` | `56d791cfcdaebe5e5b8eb4bf99aa6b4ffb909e3a` |

23개 old advertised source commit의 disposition은
[`data/migrations/backend-delivery-training-source-crosswalk.tsv`](data/migrations/backend-delivery-training-source-crosswalk.tsv)에
고정합니다. Header 포함 24줄, SHA-256
`392de1883d1dc48db6b7ae99f21119aff91721ca617a5429850bb455a91c6a64`입니다. Canonical main의 첫
9개 commit은 exact object로 보존했고 ID `011` 책임은 parent·tree·patch를 보존한 채 source timestamp와
message만 정규화했습니다. 두 release-navigation commit은 final navigation 책임 하나로 통합했습니다.
별도 legacy `pre-delivery-v1` graph의 source patch 8개는 canonical main의 같은 patch 책임으로
deduplicate했고 mixed root는 learning placeholder를 제거한 clean root로 canonicalize했습니다. 그 graph의
publication-only 2개 commit은 source에서 제외했습니다.

원격 전환 전 source-only rollback bundle은 다음 값으로 검증했으며, learning ref는 담지 않았습니다.

- 경로: `/Users/woopinbell/Documents/Codex/2026-07-19/1/work/backend-lane/backend-delivery-training/backend-delivery-training-af7ba0aa-source.bundle`
- SHA-256: `b5bd86f7c70d46e968aafb2abc5488c6806eaf9b57eca8e976cca772f4256d8a`
- 범위: old `main`과 source tag `delivery-v1`, `delivery-v1.0.1`, `pre-delivery-v1`; learning ref 0개
- 복원 검증: `git bundle verify`, restore clone `git fsck --full --strict`와 네 ref exact 대조 통과
- lifecycle: project fresh-clone gate, Document Box `c39bf1de1836fc609891840dc1eb099f2e52424a`,
  Central Notes `41905ff1e62eedf7348dd52fc8222c7727f09333` pointer와 authenticated Backend Delivery
  remote-navigation이 모두 통과한 뒤 `2026-07-21T01:22:33+09:00`에 삭제했습니다. 위 checksum과
  복원 범위만 원장에 남으며 migration 전 source를 보장하는 offline rollback artifact는 더 이상 없습니다.

Learning 후보는 서로 ancestor가 아닌 다음 두 ref였습니다.

| old ref | tip | tree | repository paths | disposition |
| --- | --- | --- | ---: | --- |
| `learning/delivery-v1` | `bf1a84e6eecd4544676a71ea7143b01a01b18a4d` | `02eb4ab1036663c14a967d7c11238247decbb81b` | 84 | v1.0.1의 유효 corpus와 blob 대조 뒤 삭제 |
| `learning/delivery-v1.0.1` | `034e284ce49915c5f2fed4e7d170fa46a7055204` | `ca27a81d7691abe6c80fcb5c9c48e24e6284a0e0` | 87 | canonical donor; 단일화 뒤 삭제 |

동일 blob은 재독하지 않고 source 호환성, commit coverage, link·metadata와 유효 고유 내용을 비교해
v1.0.1을 기준본으로 선택했습니다. 83개 legacy corpus row의 exact 판정은
[`data/migrations/backend-delivery-training-learning-disposition.tsv`](data/migrations/backend-delivery-training-learning-disposition.tsv)에
고정합니다. Header 포함 84줄, SHA-256
`b2d2b0152cf2d1292ee530f6bda906f6db571d65c73d2049e2acb03727e14b38`이며 final disposition은 adopted 12,
replaced 66, discarded 5입니다. Review mode는 동일 OID 39, 직접 내용 검토 44로 나뉩니다.
Learning bundle, archive ref와 보존 tag는 만들지 않았습니다.

Final `learning/current`는 source 뒤의 actual-time publication 세 commit으로만 구성됩니다.

| phase | commit | tree | parent | actual KST time |
| --- | --- | --- | --- | --- |
| notes | `76053e3425f9fc45fd0a7d25ef2be18c1ddb8d3d` | `084270a29ccf4c03b7994873dcf395b720587fa9` | source `fc9e1d3dc36415b4d6e7287d3738b4c1c9136364` | `2026-07-21T00:38:45+09:00` |
| answers | `cfeb6fc437dcddb1c31a89362dbc181de62dc6e0` | `f4ab8bf537854e3d359b4ade8f0ac8e4cc46728a` | notes | `2026-07-21T00:48:54+09:00` |
| practices / tip | `2c2ad03000a66ba6d1ef7381bb4401c714f506f9` | `dafa9e0e015c692845cd601b7ce9029cff740651` | answers | `2026-07-21T01:02:17+09:00` |

Final 수량은 `11 source = 10 answers + 1 exclusion`, `10 answers = 6 practices + 4 omissions`입니다.
Stable ID `009`, `010`, `012`는 legacy publication·navigation 전용 번호로 예약하고 active path에서
제거했습니다. Final source와 learning 사이 source/config/test/build diff는 0이며 versioned duplicate
corpus 없이 `docs/README.md`, `docs/notes/**`, `docs/reflection/**`, `docs/commits/**`,
`docs/practice/**`만 publication role에 따라 배치했습니다.

별도 private fresh clone에서 advertised branch가 `main`, `learning/current`뿐이고 annotated tag는
`delivery-v1.0.1` 하나이며 exact object가 final main으로 peel되는 것을 확인했습니다. Source와 learning
각각 Spring·Go test, `make build-spring`, `make build-go`, `make check-docs`, strict fsck와 corpus
metadata·H3·link·count·path gate를 통과했습니다. Unique Spring·Go image build, Compose config와
`up --build --wait --wait-timeout 120`도 통과했습니다. Spring live·ready·runtime·checks는 모두 HTTP 200,
ready database `UP`, `secretConfigured=true`, runtime release `compose-local`, delivery checks 3개
`READY`와 seed 3을 확인했고 response의 secret 출현은 0건이었습니다. Go live·ready·runtime도 주입한
config로 HTTP 200이고 response와 log의 secret 출현은 0건이었습니다. Go 컨테이너의
`SIGTERM` stop은 0.057초, exit 0, OOM false, restart 0과 stopped log를 확인했습니다. Gate가 만든
Compose container·network·anonymous volume, Go container와 unique image 3개를 정리한 뒤 대상
container·network·image는 0개이고 volume 목록은 실행 전과 같았습니다. Sandbox의 localhost·Docker
socket·Gradle lock 거부는 환경 제약에 따른 false negative였고 host 재실행 결과는 모두 green입니다.

### `backend-reliability-training` source product-token allowlist

Final source의 소문자 `cursor`는 작업 도구 provenance가 아니라 opaque keyset pagination의 제품 계약과
exercise 경로입니다. Exact path, blob, occurrence, 최초 책임과 제품상 이유는
[`data/migrations/backend-reliability-training-source-allowlist.tsv`](data/migrations/backend-reliability-training-source-allowlist.tsv)에
고정합니다. Header 포함 25줄, SHA-256
`de2e74820091972d77f81230b8ff66464ff54b69f103ab79cab930270685ff20`입니다.

Final tree에서 path token은 11개 path의 15 occurrence, blob content token은 12개 path의 61
occurrence입니다. `.gitkeep`과 `PostSummary.java`는 token을 blob에 담지 않지만 exact 제품 module
경로에 token이 있으므로 함께 등록합니다. Historical reachable graph까지 합치면 24개 allowlist row,
14개 unique path입니다. 위 원장의 exact path·blob·occurrence 외 `cursor`, 대소문자 변형, 다른 AI 도구
식별자, ref·tag 이름, commit·tag metadata·본문·trailer와 tool-control artifact에는 이 allowlist를
적용하지 않습니다. Final source 전수 검사에서 등록되지 않은 금지 provenance는 0건입니다.

### `backend-reliability-training` 실행 원장

2026-07-21 KST에 private `woopinbell/backend-reliability-training`의 source와 learning ref를 모든 ref의
exact lease를 사용한 단일 atomic push로 전환했습니다. Expected-old `main`
`f3ff5654d9a40e1701bda82d21ca0929941076e7`은 replacement `main`
`d1675f1f07056df81ad2719f5b9fc067d14ad365`(tree
`5bc7840641632b17636e232b75a57ef48a283e42`)로 이동했습니다. Final source는 96개 reachable commit,
19개 merge이며 승인된 `2025-02-15`–`2025-08-15` KST window, canonical identity,
author/committer timestamp 일치, unique KST time, parent chronology, three-section message와 trailer gate를
통과했습니다. 기존 첫 88개 책임은 patch 순서와 merge topology를 보존해 정확히 14일 이동했고 마지막
8개 책임은 마지막 개발일 안에서 순서를 보존했습니다.

Go 1.22의 `http.Client` timeout 회귀는 별도 현재 시각 commit을 만들지 않고 old test 책임
`f82ceefc69d0192593c2a2631da56bd8d74ed630`의 replacement
`f691b74ec86bac13c4291dfc4078f1f6d6d83e94`에 흡수했습니다. `errors.As`로 `net.Error`를 확인하고
`Timeout()`과 기존 175 ms elapsed bound를 함께 검증합니다. Final source는 old `main`과 비교해
`README.md`, `docs/DESIGN.md`, `go-sub/advanced/http-timeout/http_timeout_test.go` 세 path만 다릅니다.

107개 old advertised source commit의 disposition은
[`data/migrations/backend-reliability-training-source-crosswalk.tsv`](data/migrations/backend-reliability-training-source-crosswalk.tsv)에
고정합니다. Header 포함 108줄, SHA-256
`a2da7ecb2041ab9bd16ca8afb4c4b46892e5d50bb9e1af65a0658ba3d203261b`입니다. Canonical `main` 96개와
legacy `pre-reliability-v1` graph의 unique 11개 책임을 old/new commit, parent, tree, stable patch-id,
timestamp, subject와 disposition으로 모두 닫습니다.

Current annotated release `reliability-v2.0.1`은 old object
`9935d2650e412562ffcc1bda5f5115642d97b87e`에서 final object
`a1d6b924942fd52fe7b7449ec498182bd6daa30a`으로 교체했으며 final `main`으로 peel됩니다. 다음 legacy
source tag는 exact old object에서 삭제했습니다.

| ref | old tag object | old peeled target |
| --- | --- | --- |
| `pre-reliability-v1` | `f00ddddb38e014566b4e2ea1be0220e1a2ac9c15` | `1a64f994afdcaf4f03d40e588dcfa8bf7f92f6dd` |
| `reliability-v1` | `7902d50106b40c1673a09f44f43c1c9a53b15eea` | `a28ad09ceea9bc28a1321601ff4202816ac00775` |
| `reliability-v2` | `159548ce66a01ca9fda47464872b82568966b904` | `b0aad3cd7f74f98e9ab1c3b2a88b0f302bccc9fc` |

원격 전환 전 source-only rollback bundle은 다음 값으로 검증했으며 learning ref를 담지 않았습니다.

- 경로: `/Users/woopinbell/Documents/Codex/2026-07-19/1/work/backend-lane/backend-reliability-training/backend-reliability-training-f3ff5654-source.bundle`
- SHA-256: `64f345cf46b8dbd8369e1135f5dfcd864aeaac6ef150a5a88a5d028d59d6dd90`
- 범위: old `main`, source tag 네 개와 `HEAD`; learning ref와 learning-only 보존 object 0개
- 복원 검증: `git bundle verify`, complete history, restore clone exact refs와 `git fsck --strict` 통과
- lifecycle: project source·learning fresh-clone gate, Document Box
  `6ff2450ba6d65ebb64d50ef4da294581fb23222f`, Central Notes
  `054e818c9ad5edf0d334b4a13e70ba5376293fd5` pointer와 authenticated Backend Reliability
  remote-navigation이 모두 통과한 뒤 `2026-07-21T03:00:04+09:00`에 삭제했습니다. 위 checksum과
  복원 범위만 원장에 남으며 migration 전 source를 보장하는 offline rollback artifact는 더 이상 없습니다.

Learning 후보는 다음 세 ref였습니다. Commit ancestor 관계가 아니라 path/blob/tree matrix로 비교했고,
모든 유효 path를 포함하며 current source와 호환되는 v2.0.1 corpus를 canonical donor로 선택했습니다.

| old ref | tip | tree | disposition |
| --- | --- | --- | --- |
| `learning/reliability-v1` | `c4b34b46e3024f4f9ccef8b3c884184763622680` | `1c9eaf7989dc2c840281fdf0207bd3bb7dc5926d` | v2.0.1 포함관계와 유효 blob 대조 뒤 삭제 |
| `learning/reliability-v2` | `634f9c27776ce10ccf9fe52d885d831abce4c0e2` | `52f7d148321dd747b6195a7465d0c1e4631f8bd7` | v2.0.1 포함관계와 유효 blob 대조 뒤 삭제 |
| `learning/reliability-v2.0.1` | `5a6a11d65379e4607c3bdaadf467c37cc0b42d50` | `69cd9950e5c933048dbe3de609dc582defbdbfcc` | canonical donor; 단일화 뒤 삭제 |

528개 legacy path 판정은
[`data/migrations/backend-reliability-training-learning-disposition.tsv`](data/migrations/backend-reliability-training-learning-disposition.tsv)에
고정합니다. Header 포함 529줄, SHA-256
`f231293ab896dfd3c244f608ca59f6f17b27b845736264233d1a70e21b398b5d`입니다. 동일 OID는 다시 읽지
않았고 metadata-only 변경과 고유·충돌·source 영향 본문만 분리해 한 번 검토했습니다. Final active
corpus는 source-shared 305개와 learning-only 217개, 합계 522개 path이며 versioned answer/practice root는
없습니다. Learning bundle, archive ref와 보존 tag는 만들지 않았습니다.

Final `learning/current`는 source freeze 뒤 actual-time publication 세 commit으로만 구성됩니다.

| phase | commit | tree | parent | actual KST time |
| --- | --- | --- | --- | --- |
| notes | `7e949c1e0086b95476e9dbd4ea391cf72e8bf649` | `f5fef47eb6eae93fa2327039006ca9750028f406` | source `d1675f1f07056df81ad2719f5b9fc067d14ad365` | `2026-07-21T02:43:02+09:00` |
| answers | `d04c6e5484afcfc011befefd683d79c2a83858d4` | `3cedcc590c6f0fffcd1df086fa237e676307c9b5` | notes | `2026-07-21T02:43:30+09:00` |
| practices / tip | `6fbeeb3a3d17a7e1106010c57c7f9e7adf1707ce` | `68b430e31d130556904e40a7578b196f48258f1b` | answers | `2026-07-21T02:43:48+09:00` |

Final 수량은 `96 source = 74 answers + 22 exclusions`, `74 answers = 41 practices + 33 omissions`입니다.
Answer 전체 barrier와 검토 뒤 practice를 수작업으로 파생했으며 source/config/test diff는 0입니다. Local
source와 learning strict fsck, Go 1.22 targeted/full test, `make check`, Redis·PostgreSQL runtime gate,
corpus metadata·H3·link·count·path 검사를 모두 통과했습니다. 별도 HTTPS fresh clone에서도 source와
learning 전체 gate, exact branch·tag topology와 clean status를 확인했습니다. Authenticated 30-project
검사에서 Backend Reliability와 Central links는 PASS했고 남은 두 오류는 다음 작업 대상인
`sportsbook-shared-protocol`에만 속합니다.

### `sportsbook-shared-protocol` 실행 원장

2026-07-21 KST에 private `woopinbell/sportsbook-shared-protocol`의 source와 learning ref를 모든 ref의
exact lease를 사용한 단일 atomic push로 전환했습니다. Expected-old `main`
`4b7cd85bfac75c9339302507514ccac77337f4f3`은 replacement `main`
`b0305168e6d340bc1b73c999649fbd526f964663`(tree
`0e40d4d9b265ac9379690bfb2791648cf372e06a`)로 이동했습니다. Final source는 20개 linear commit,
merge 0이며 승인된 `2026-02-02`–`2026-02-15` KST window, canonical identity,
author/committer timestamp 일치, parent chronology, three-section message와 trailer gate를 통과했습니다.
첫 17개 책임은 원래 in-window timestamp를 보존했고 마지막 세 책임은 마지막 개발 구간 안에서 patch
순서대로 배치했습니다. Old final learner-navigation-only 책임은 source graph에서 제외하고 정확한 release
상태와 canonical Document Box backlink를 final source guide에 통합했습니다. Old `main`과 final source의
tree diff는 `.gitignore`, `README.md` 두 path뿐입니다.

45개 old advertised source commit의 disposition은
[`data/migrations/sportsbook-shared-protocol-source-crosswalk.tsv`](data/migrations/sportsbook-shared-protocol-source-crosswalk.tsv)에
고정합니다. Header 포함 46줄, SHA-256
`17c9d126ba062c2581c0d9de7aecd867198208714dceb2a1d640dfc7bac73083`이며 old/new commit, parent,
tree, stable patch-id, timestamp, subject와 disposition을 모두 닫습니다. Final source ref·tag·commit
metadata·trailer·path·historical reachable blob의 금지 provenance는 0건이며 제품 기능상 허용할 token도
0건입니다.

Current annotated release `shared-v1.0.1`은 old object
`bcd451127a37747d2ab5824902943007dfed1b65`에서 final object
`5acf10a9bab01f3151f1371f1012c5687e79a55b`으로 교체했으며 final `main`으로 peel됩니다. 다음 legacy
source tag는 exact old object에서 삭제했습니다.

| ref | old tag object | old peeled target |
| --- | --- | --- |
| `pre-shared-v1` | `5f1c07eafd1d81445e35df96334c5d1f7a4c051d` | `91e33340f8650fc48d6ab4b3f84e70d64ceb6c8c` |
| `shared-v1` | `bd3ab9cb9df9ddce51aecd32008b8844781a184c` | `e0754c3a68ddce4f9ddef00e3dfb26b3ce53adbb` |
| `v0.1.0` | `1e43d18430cada6d7bbb2468d430ffa9c7a231b5` | `ee28c65b761faea0923ce6a7fa1f1f509911b2be` |

원격 전환 전 source-only rollback bundle은 다음 값으로 검증했으며 learning ref를 담지 않았습니다.

- 경로: `/Users/woopinbell/Documents/Codex/2026-07-19/1/work/backend-lane/sportsbook-shared-protocol/source-audit/sportsbook-shared-protocol-4b7cd85b-source.bundle`
- SHA-256: `5d608387b858178308caa3ee6e3362eda404e94c284d794cbe7e6ac06d059e55`
- 범위: old `main`, source tag 네 개와 `HEAD`; learning ref와 learning-only 보존 object 0개
- 복원 검증: `git bundle verify`, complete history, restore clone exact refs와 `git fsck --strict` 통과
- lifecycle: project source·learning fresh-clone gate, Document Box
  `4dc37f8b2be9776c93b98f1f54d1bdeedf4a9571`, Central Notes
  `619e105c5e6d3cbfdfeef1122690181cf51c3ceb` pointer와 authenticated 30-project Shared Protocol
  remote-navigation이 모두 통과한 뒤 `2026-07-21T04:00:11+09:00`에 삭제했습니다. 위 checksum과 복원
  범위만 원장에 남으며 learning bundle, 대체 offline artifact와 migration 전 source를 보장하는 local
  copy는 더 이상 없습니다.

Learning 입력은 다음 두 ref였습니다. Ancestor 우열로 간주하지 않고 path·blob·tree matrix, source
호환성, commit coverage, link·metadata와 고유 내용을 비교해 최종 corpus를 단일화했습니다.

| old ref | tip | tree | disposition |
| --- | --- | --- | --- |
| `learning/shared-v1` | `415bd8165e66fe8a83a32b4855f43038577a6eac` | `e20ef8469894183db1b8bf40f1d996777c58e353` | 유효 blob 대조 뒤 삭제 |
| `learning/shared-v1.0.1` | `90b81d9d49472673a85fb740ef425173119125d7` | `29dd20ca56fdb15739703938604daf8978a9a03e` | source-split canonical donor; 단일화 뒤 삭제 |

134개 union path 판정은
[`data/migrations/sportsbook-shared-protocol-learning-disposition.tsv`](data/migrations/sportsbook-shared-protocol-learning-disposition.tsv)에
고정합니다. Header 포함 135줄, SHA-256
`c8c3086875c06ee1d89c4cf534ff236eb191e025679f18196cbb360150e4dcc3`입니다. Final disposition은
adopted 44, replaced 30, discarded 60이며 review mode는 `oid-identical` 44, `metadata-only` 23,
`direct-content` 7, discard 60입니다. 동일 OID는 재독하지 않고 고유·충돌·source 영향 본문만 2026-07-21
03:41:05 KST에 한 번 검토했습니다. Learning bundle, archive ref와 보존 tag는 만들지 않았습니다.

Final `learning/current`는 source freeze 뒤 actual-time publication 두 commit으로만 구성됩니다. 별도
repository-local concept notes가 없으므로 notes phase는 만들지 않았습니다.

| phase | commit | tree | parent | actual KST time |
| --- | --- | --- | --- | --- |
| answers | `86ee2af2913a6fb9c2af88fa56a41a8d0ac484a9` | `9117d012cbb34c8638bdae957519078d8ce581ec` | source `b0305168e6d340bc1b73c999649fbd526f964663` | `2026-07-21T03:47:08+09:00` |
| practices / tip | `63c5639cec295d83e5bc47671e1d1d02641a8537` | `cc3c9240d7ef85c96ac2d9abbf1d5999f74804aa` | answers | `2026-07-21T03:47:15+09:00` |

Final 수량은 `20 source = 19 answers + 1 marker-only exclusion`,
`19 answers = 7 practices + 12 omissions`입니다. Answer 전체 barrier와 검토 뒤 practice를 수작업으로
파생했으며 final source와 learning 사이 source/config/test diff는 0입니다. 별도 HTTPS fresh clone에서
source와 learning exact tip·tree, strict fsck, active root·link·metadata·path role, source provenance 0과
`./mvnw verify`의 Avro Java 생성, handwritten/generated compile, 89 tests, Spotless, Checkstyle, package를
다시 통과했습니다. Avro 1.12.0은 `dateTimeLogicalTypeImplementation`을 unknown parameter로 경고하며 이
저장소에는 명시적 schema compatibility test gate가 없습니다. 이 migration은 그 호환성을 검증했다고
기록하지 않습니다. Remote는 branch `main`, `learning/current`와 annotated `shared-v1.0.1`만
advertise합니다.

두 actual-time publication은 source·answer·practice 순서와 path role을 모두 지켰지만 subject scope를
각각 `docs(learning): publish source responsibility answers`, `docs(learning): publish derived practice
corpus`로 기록했습니다. 완료된 learning graph를 다시 쓰지 않도록 exact commit과 exact subject pair만
remote-navigation 예외로 동결합니다. 이 예외는 다른 commit, 다른 subject 또는 다른 저장소에
`docs(learning)` scope를 허용하지 않으며 notes→commits→practice path gate도 완화하지 않습니다.

### `sportsbook-wallet-service` 실행 원장

2026-07-21 KST에 private `woopinbell/sportsbook-wallet-service`의 source와 learning ref를 모든 ref의
exact lease를 사용한 단일 GitHub atomic push로 전환했습니다. Expected-old `main`
`bd203952b9ef1a0bec47f8a19c95fa8930e952cd`은 replacement `main`
`a4be0d5fdfdd08a76952dbafadadb620ffdbcc8e`(tree
`6599086e7a71250f7dc1a9c1747bd9f15a44aa97`)로 이동했습니다. Final source는 28개 linear commit,
merge 0이며 승인된 `2026-02-16`–`2026-03-01` KST window, canonical identity,
author/committer timestamp 일치, parent chronology, three-section message와 trailer gate를 통과했습니다.
Old formatter-only 책임은 final source 책임에 완성 상태로 흡수했고 learner-navigation-only tip은 source
graph에서 제외한 뒤 정확한 release 상태와 Document Box backlink를 final source guide에 통합했습니다.
Old `main`과 final source의 tree diff는 provenance·learning navigation 정화에 필요한 `.gitignore`,
`README.md`, `load-test/scenarios/debit_load.js`, `SystemAccountIds.java`, `UuidV7.java` 다섯 path뿐입니다.

41개 old advertised source commit의 disposition은
[`data/migrations/sportsbook-wallet-service-source-crosswalk.tsv`](data/migrations/sportsbook-wallet-service-source-crosswalk.tsv)에
고정합니다. Header 포함 42줄, SHA-256
`0f39220b71ce3242f2450f003d210052b69696f157954de496ddb2f29c5173d5`이며 old/new commit, parent,
tree, stable patch-id, timestamp, subject와 disposition을 모두 닫습니다. Final source ref·annotated tag·commit
metadata·trailer·historical path·reachable blob의 금지 provenance는 0건이며 제품 기능상 허용할 token도
0건입니다.

Current annotated release `wallet-v1.0.2`는 old object
`6c895206f8dc8ce42d18d9c4f1249b3faf3efa81`에서 final object
`559bebcebcbb3b0d4737914ecd564b2d6b7c2c20`으로 교체했으며 final `main`으로 peel됩니다. 다음 legacy
source tag는 exact old object에서 삭제했습니다.

| ref | old tag object | old peeled target |
| --- | --- | --- |
| `pre-wallet-v1` | `acabf64d4077c82a5d01a5e96379920b6ca0cc8c` | `2fcb8cca9f81dfd45bdc23af273d966885446cda` |
| `wallet-v1` | `89afc07a1886426ce8d68bdae3c99f650fbf98b7` | `0f28d668856d702c1bcea90e1a42bd43871c0a9f` |
| `wallet-v1.0.1` | `836c6b6823ae09ceca3ee7b0974f7752f08ef3f9` | `04c0c9706ed16ae6ba763aadd02d8eddd6bde536` |

원격 전환 전 source-only rollback bundle은 다음 값으로 검증했으며 learning ref를 담지 않았습니다.

- 경로: `/Users/woopinbell/Documents/Codex/2026-07-19/1/work/backend-lane/sportsbook-wallet-service/source-audit/sportsbook-wallet-service-bd203952-source.bundle`
- SHA-256: `509e6c3f6d5ce929a68f6de6f9f46ee80af4941a0a2f60f8d4dcd89073542ade`
- 범위: old `main`, source tag 네 개와 `HEAD`; learning ref와 learning-only 보존 object 0개
- 복원 검증: `git bundle verify`, complete history, restore clone exact refs와 `git fsck --strict` 통과
- lifecycle: project source·learning fresh-clone gate, Document Box
  `96ddffeb7915cf9a0c9780ab4f7a1ec443fbb703`, Central Notes
  `7be875aa2a42b33109841933f83607001f31eba4` pointer와 authenticated 30-project remote-navigation이 모두
  통과한 뒤 `2026-07-21T05:50:14+09:00`에 삭제했습니다. 위 checksum과 복원 범위만 원장에 남으며
  learning bundle이나 대체 offline rollback artifact는 없습니다.

Learning 입력은 다음 세 ref였습니다. Ancestor 우열로 간주하지 않고 path·blob·tree matrix, source
호환성, commit coverage, link·metadata와 고유 내용을 비교해 최종 corpus를 단일화했습니다.

| old ref | tip | tree | disposition |
| --- | --- | --- | --- |
| `learning/wallet-v1` | `009de12feb4dc99410dddb08469d9261e4a3ffcf` | `5cfc9f474b3e890f863b11e6bdddbbab6c501516` | 유효 blob 대조 뒤 삭제 |
| `learning/wallet-v1.0.1` | `dacb59158a50897c4de93ff780663862ce0ab407` | `5da42d781a24bd4edda3b4fc5bc6436dd37e0d0e` | source-split donor 대조 뒤 삭제 |
| `learning/wallet-v1.0.2` | `33552cb95a3ff8f443ec8c471c24ba4a41bb3522` | `bdeeabf374cb4101d20b76a2c2c24d559323215a` | provisional superset donor; 단일화 뒤 삭제 |

225개 union path 판정은
[`data/migrations/sportsbook-wallet-service-learning-disposition.tsv`](data/migrations/sportsbook-wallet-service-learning-disposition.tsv)에
고정합니다. Header 포함 226줄, SHA-256
`b840501b4c728e85118c04614d6786ba47abddcd51c3f661b038f9c43aacd2db`입니다. Review mode는
`oid-identical` 161, `metadata-only` 48, `direct-content` 16입니다. 동일 OID는 재독하지 않고 고유·충돌·
source 영향 본문만 한 번 검토했습니다. 최종 50개 문서의 정규화 digest는
`4d216ce35033e02c1b64a06f701ddd3f38a696a5efad56df90b4c3bc7eb358db`이며 learning bundle,
archive ref와 보존 tag는 만들지 않았습니다.

Final `learning/current`는 source freeze 뒤 actual-time publication 세 commit으로만 구성됩니다.

| phase | commit | tree | parent | actual KST time |
| --- | --- | --- | --- | --- |
| notes | `677a2f9fe8cb9205f56bc1b85cad3a6d39a9cecd` | `7f1ee589d844b563f349520a8074a8e5025956fd` | source `a4be0d5fdfdd08a76952dbafadadb620ffdbcc8e` | `2026-07-21T05:26:14+09:00` |
| answers | `42bf59fec8bba200a5fcabfbb40d8184ff498014` | `fd7ed92b9769ec7ca996fd50e6c2d5058e495e96` | notes | `2026-07-21T05:26:23+09:00` |
| practices / tip | `49275a73a5b3b5677f42d8f9ce3b97b0fbac959b` | `6ceb755a5016372bf0db31df7e9dd3e6661fdc31` | answers | `2026-07-21T05:26:35+09:00` |

Final 수량은 `28 source = 24 answers + 4 exclusions`, `24 answers = 21 practices + 3 omissions`입니다.
Answer 전체 barrier와 검토 뒤 practice를 수작업으로 파생했으며 final source와 learning 사이
source/config/test diff는 0입니다. Host clean verify에서 PostgreSQL·Kafka·Redis integration, 62 tests,
Spotless 52 files, Checkstyle 0 violations와 package를 통과했습니다. Remote는 branch `main`,
`learning/current`와 annotated `wallet-v1.0.2`만 advertise합니다. 별도 HTTPS fresh clone에서도 source
tip·tree·28-commit graph·source provenance 0·62-test build와 learning tip·tree·세 publication 역할·50개
문서·수량식·link·metadata·source drift 0을 독립적으로 다시 통과했습니다.

### `sportsbook-risk-service` 실행 원장

2026-07-21 KST에 private `woopinbell/sportsbook-risk-service`의 source와 learning ref를 모든 ref의
exact lease를 사용한 단일 GitHub atomic push로 전환했습니다. Expected-old `main`
`be7b9c43f435323b0c638d68fd9c649557fc1bc0`은 replacement `main`
`de3ddc4c54ec5f992ef893ae96e4a1673024e163`(tree
`7760c735992ddbc92466ca73de8f20959b734e10`)으로 이동했습니다. Final source는 29개 linear commit,
merge 0이며 승인된 `2026-03-02`–`2026-04-05` KST window, canonical identity,
author/committer timestamp 일치, parent chronology, three-section message와 trailer gate를 통과했습니다.
Old provenance-only 책임과 learner-navigation-only tip은 source graph에서 제외했고, 정확한 release 상태와
Document Box backlink는 final source guide에 통합했습니다. Old `main`과 final source의 content diff는
`.gitignore`, `README.md`, `load-test/README.md`, `load-test/results/BEST.md`,
`load-test/scenarios/consumer_throughput.sh`, `pom.xml` 여섯 path의 20 insertions·28 deletions뿐이며 source
provenance와 source-side learning publication 언어만 제거하고 제품 동작과 RED 성능 자격은 바꾸지 않았습니다.

Old `main`과 일곱 annotated source tag에서 도달 가능한 70개 old source commit의 disposition은
[`data/migrations/sportsbook-risk-service-source-crosswalk.tsv`](data/migrations/sportsbook-risk-service-source-crosswalk.tsv)에
고정합니다. Header 포함 71줄, SHA-256
`f5e0dddf47482f99364648c3b024c34853e340ecad56ec13a729b4c3b2eccfda`이며 old/new commit, parent,
tree, stable patch-id, timestamp, subject, reaching ref와 disposition을 닫습니다. Final source ref·annotated
tag·commit metadata·trailer·historical path·reachable blob의 금지 provenance는 0건이며 제품 기능상
허용할 token도 0건입니다.

Current annotated release `risk-v1.0.2`는 old object
`ce3ddc0c9bfd403152d5b07793a6101ad7518819`에서 final object
`6f4917e7660f92c3b807873bd6894edeb32fe459`로 교체했으며 final `main`으로 peel됩니다. 다음 legacy source
tag는 exact old object에서 삭제했습니다.

| ref | old tag object | old peeled target |
| --- | --- | --- |
| `diagnostic-atomic-snapshot-v1-red` | `88da276f887292619500228c91e7f2fc8049c10b` | `49c6ec9e023ad0c831de563869b0c22ae46ffeee` |
| `diagnostic-codex-5.6-red` | `51707bec5cf5c6a7bb7ea750f95688f2247f1e2e` | `eca275e3de27222ee774b61c55d07c955a11694d` |
| `pre-history-clean-risk-v1.0.2` | `23c62e081c42da9276e5e0a0623afde07996ee7c` | `6f17d0c7d8361c2db2e26555a5854d01612305fb` |
| `pre-risk-v1` | `d58b9206635a9267fb18547788eb288145d23019` | `db45a5611a2ac4554a78adbed759500af30d85c7` |
| `risk-v1` | `12ae029455dacf1b73f10c64622d977d1b691544` | `76c822b69bc816bad333479dfee79dcf3d19212b` |
| `risk-v1.0.1` | `ee047c2bd2a79d97af7b89e79aa9c28df857864a` | `6f17d0c7d8361c2db2e26555a5854d01612305fb` |

원격 전환 전 source-only rollback bundle은 다음 값으로 검증했으며 learning ref를 담지 않았습니다.

- 경로: `/Users/woopinbell/Documents/Codex/2026-07-19/1/work/backend-lane/sportsbook-risk-service/source-audit/sportsbook-risk-service-be7b9c43-source.bundle`
- SHA-256: `c8a9542323793430f5b4ecf884c1734e4c8f16cfadf2ce7458cd3a620c0d0235`
- 범위: old `main`, source tag 일곱 개와 `HEAD`; learning ref와 learning-only 보존 object 0개
- 복원 검증: `git bundle verify`, complete history, restore clone exact refs와 `git fsck --strict` 통과
- lifecycle: project source·learning fresh-clone gate, Document Box
  `cfe50f8bfed7a8b5e34186d05f1f906271917843`, Central Notes
  `9520bd3ef28ef32186e80a210fe4f487b725c170` pointer와 authenticated 30-project Risk
  remote-navigation이 모두 통과한 뒤 `2026-07-21T07:55:16+09:00`에 영구 삭제했습니다. 위 checksum과
  복원 범위만 원장에 남으며 learning bundle, 대체 offline artifact와 migration 전 source를 보장하는
  local copy는 더 이상 없습니다.

Learning 입력은 다음 세 ref였습니다. Ancestor 우열로 간주하지 않고 path·blob·tree matrix, source
호환성, commit coverage, link·metadata와 고유 내용을 비교해 최종 corpus를 단일화했습니다.

| old ref | tip | tree | disposition |
| --- | --- | --- | --- |
| `learning/risk-v1` | `d262f52ccc845cef5f0912326cd90f69ce04697e` | `1e6761a53f13c41f4cf32428dfc04ceee607f52e` | 유효 blob 대조 뒤 삭제 |
| `learning/risk-v1.0.1` | `8049ab52f725b9b1e94a1ef37a7c302d2928b5d4` | `90d7289b0de96908ea1669a411196bb35564746a` | 고유·충돌 blob 대조 뒤 삭제 |
| `learning/risk-v1.0.2` | `6166b83969b86f639cdc2874fed0bf5c08597819` | `a14dba442df10246cfbf08cb2f9d4b52e5937902` | source-compatible superset donor; 단일화 뒤 삭제 |

174개 union path 판정은
[`data/migrations/sportsbook-risk-service-learning-disposition.tsv`](data/migrations/sportsbook-risk-service-learning-disposition.tsv)에
고정합니다. Header 포함 175줄, SHA-256
`08b8d3407fc7480483a8337c36bf2381480a56c9da19530df1cb9e90dffea3c5`입니다. Review mode는
`oid-identical` 99, `direct-content` 75입니다. 동일 OID는 재독하지 않고 고유·충돌·source 영향 본문만
2026-07-21 07:24:17 KST에 한 번 검토했습니다. 최종 51개 문서의 정규화 digest는
`2d7f6c01de662abd0ac8b422ecf597d11f2db1c4b93fd82f321c6b816f250772`이며 learning bundle,
archive ref와 보존 tag는 만들지 않았습니다.

Final `learning/current`는 source freeze 뒤 actual-time publication 세 commit으로만 구성됩니다.

| phase | commit | tree | parent | actual KST time |
| --- | --- | --- | --- | --- |
| notes | `31db4a406371aa1507383fe9059ddf8e8cd25621` | `331f1e9104631a6f684ca8d20e8fa9d2dd097892` | source `de3ddc4c54ec5f992ef893ae96e4a1673024e163` | `2026-07-21T07:29:41+09:00` |
| answers | `33e423c0f3604a7c5967e620543b554292b78f75` | `969f31f34a62c41f8a16e87f6e17ea43ce1581e8` | notes | `2026-07-21T07:29:55+09:00` |
| practices / tip | `a4cb1c0b1a251ba643c963625d6a6c16c9d80b20` | `6fa5c06a68393eae195632f8390806ea9143e85b` | answers | `2026-07-21T07:33:39+09:00` |

Final 수량은 `29 source = 29 answers + 0 exclusions`, `29 answers = 17 practices + 12 omissions`입니다.
Answer 전체 barrier와 검토 뒤 practice를 파일별 수작업으로 파생했으며 final source와 learning 사이
source/config/test diff는 0입니다. Host clean verify와 별도 HTTPS fresh clone에서 99 tests, failure·error·skip
0, Spotless 61 Java paths, Checkstyle 0 violations, executable package를 통과했습니다. 원격은 branch
`main`, `learning/current`와 annotated `risk-v1.0.2`만 advertise합니다. 1,000 RPS evidence는 58,971
requests, p99 268.450 ms, drops 1,030으로 계속 RED이며 이 migration은 성능 자격을 통과시켰다고
기록하지 않습니다.

### `sportsbook-odds-feed-service` 실행 원장

2026-07-21 KST에 private `woopinbell/sportsbook-odds-feed-service`의 source와 learning ref를 모든
변경 ref의 exact lease를 사용한 단일 GitHub atomic push로 전환했습니다. Expected-old `main`
`5a97082ec9c2f4b295960f8791bdbf5fcb71f6f2`는 replacement `main`
`f6f358d914f429749dec83ef7a266ae7d50778b5`(tree
`5fc7107b3f5fbb4d0d890e1602d17b9073748e72`)로 이동했습니다. Final source는 18개 linear commit,
merge 0이며 승인된 `2026-03-23`–`2026-04-12` KST window, canonical identity,
author/committer timestamp 일치, parent chronology, three-section message와 trailer gate를 통과했습니다.
Learner-navigation-only old tip 한 개는 source graph에서 제외했고, legacy source tag에서만 도달하던
40개 commit은 current advertised source surface에서 제거했습니다.

Old source ref union의 59개 commit disposition은
[`data/migrations/sportsbook-odds-feed-service-source-crosswalk.tsv`](data/migrations/sportsbook-odds-feed-service-source-crosswalk.tsv)에
고정합니다. Header 포함 60줄, SHA-256
`4665f3915170a023a9ed3b5ea3ef17e888f729bf8c592b36ae537a6131748428`이며 old/new commit, parent,
tree, stable patch-id, timestamp, reaching source ref와 disposition을 닫습니다. 그중 18개는 ordered
`main` replay로 retained, 1개는 learner-navigation-only exclusion, 40개는 deleted-tag-only
disposition입니다. Old `main`과 final source tree의 정화 diff는 `.gitignore`, `README.md`, `pom.xml`,
cache key·cache config, publisher config·문서와 `application.yml` 여덟 path의 12 insertions·15 deletions뿐입니다.

Final source ref·annotated tag·commit metadata·trailer·historical path와 reachable blob의 금지 provenance는
등록되지 않은 일치 0건입니다. 제품 pagination 계약에 필요한 `cursor`만 exact path/blob allowlist
8행, 35 matching lines, 49 raw occurrences로 허용했으며 ref/tag/metadata나 작업 도구 설정에는 이
allowlist를 적용하지 않았습니다.

Current annotated release `odds-v1.0.1`은 old object
`fa376456eb3dd7766b37a6c46150dfd11e016b2e`에서 final object
`b0d1f674a4877ab2bfc43f0e61919cb483f34aab`로 교체했으며 final `main`으로 peel됩니다. 다음 legacy
source tag는 exact old object에서 삭제했습니다.

| ref | old tag object | old peeled target |
| --- | --- | --- |
| `diagnostic-codex-5.6-red` | `8a541f7fa667610e4700e8368f47693bd1e219a4` | `155f91de0c97d986561f89017e1e6d04ae6f57d8` |
| `odds-v1` | `763408693cf5277a3975dc56edeebb554237dfea` | `72316d951cc7e289ba2da04ef441ae94474c5009` |
| `pre-odds-v1` | `307f93e5ffad31949b9dae550119a11d9b31739a` | `c0f46ab38335218ea441cc01c13ab1c5b2493caa` |
| `v0.1.0` | `3160af580da8a8c5426176c211e2565e33823361` | `8e97109c7ad7864d4a8b7c13f619a80ee3a0dfa9` |

원격 전환 전 source-only rollback bundle은 다음 값으로 검증했으며 learning ref를 담지 않았습니다.

- 경로: `/Users/woopinbell/Documents/Codex/2026-07-19/1/work/backend-lane/sportsbook-odds-feed-service/source-audit/sportsbook-odds-feed-service-5a97082e-source.bundle`
- SHA-256: `bdd8f34ec1e1613d90e09006f451839f733e5a13606b01455fb9031c16f2013d`
- 범위: old `main`, source tag 다섯 개와 `HEAD`; learning ref와 learning-only object 0개
- 복원 검증: `git bundle verify`, complete history, restore clone exact refs와 `git fsck --strict` 통과
- lifecycle: project source·learning publication과 독립 HTTPS fresh-clone gate는 통과했습니다. Document
  Box·Central pointer publication, authenticated 30-project navigation과 후속 fresh-clone gate가 끝날 때까지
  이 source-only bundle을 유지하며, 그 gate 뒤 영구 삭제 시각을 이 원장에 별도 기록합니다.

Learning 입력은 다음 두 ref였습니다. 두 tip은 서로 ancestor가 아니며 path·blob·tree matrix, final
source 호환성, commit coverage, link·metadata와 고유 내용을 비교해 `learning/odds-v1`을 donor로
선택한 뒤 최종 corpus를 단일화했습니다.

| old ref | tip | tree | disposition |
| --- | --- | --- | --- |
| `learning/odds-v1` | `be22dd966b7105023df38ff111c734dbd74b73d9` | `4ac901a0ebe86ba2034308496de7445b4b0deb46` | source-split donor; canonical path 보정 뒤 삭제 |
| `learning/odds-v1.0.1` | `3325701eb47fe25c459c270ef02020dbff3d12f2` | `221c43eaa01c304364c22a8d27e42825974d558c` | learner-navigation answer와 versioned duplicate 폐기 뒤 삭제 |

146개 union path 판정은
[`data/migrations/sportsbook-odds-feed-service-learning-disposition.tsv`](data/migrations/sportsbook-odds-feed-service-learning-disposition.tsv)에
고정합니다. Header 포함 147줄, SHA-256
`7985ce857a4f2689a8a4af796b09e1a2e1e3b5ded1963ea174ec5f0c94b99da9`입니다. OID-identical 134개는
재독하지 않았고 branch-unique 10개와 conflicting blob 2개만 직접 판정했습니다. Final source replay로
metadata가 바뀐 answer·practice와 source cleanup 영향 ID만 전담 집필자가 다시 대조했습니다. Final
43개 publication path의 `git ls-tree -r` manifest SHA-256은
`492e7449deeb812f1b4690ee7274c3b7fa641e382336ba541cb282ff23ca2d10`이며 learning bundle, archive ref와
보존 tag는 만들지 않았습니다.

Final `learning/current`는 source freeze 뒤 actual-time publication 세 commit으로만 구성됩니다.

| phase | commit | tree | parent | actual KST time |
| --- | --- | --- | --- | --- |
| notes/evidence | `79d482a8723fd4b333e2d18f127cd99ad1bca510` | `24673e46256ed55d2b1e3b873eb9bc11352fe327` | source `f6f358d914f429749dec83ef7a266ae7d50778b5` | `2026-07-21T09:29:06+09:00` |
| answers | `c0b5901414de3d64e8d36481ddcd4a172a2b2ce6` | `99d080cea7842dccdf345a5670fd9ac007e82a47` | notes/evidence | `2026-07-21T09:29:16+09:00` |
| practices / tip | `6b75f6cb5110e7b5023b3967e5747a4dc36247b9` | `a3b181874dfd21575f016e12b1d15b2be027b6de` | answers | `2026-07-21T09:29:24+09:00` |

Final 수량은 `18 source = 18 answers + 0 exclusions`, `18 answers = 13 practices + 5 omissions`입니다.
Answer barrier 전체를 통과한 뒤 practice를 파일별 수작업으로 파생했고 final source와 learning 사이
source/config/test diff는 0입니다. Historical gate는 one-based ordinals 1–12 PASS, ordinals 13–15
`PHASE-RED_SPOTLESS_ONLY`, ordinal 16 first full green, ordinals 17–18 PASS입니다. Phase-red 세 commit도
72 tests와 executable JAR는 green이었고, `FeedOrchestrator.java`와 `FeedOrchestratorTest.java` 두 path의
formatter debt만 ordinal 16의 원래 책임에서 해소했습니다.

Host clean verify와 별도 HTTPS fresh clone에서 72 tests, failure·error·skip 0, Spotless 55 paths,
Checkstyle 0 violations와 executable package를 통과했습니다. Learning의 controlled-local HTTP evidence는
endpoint별 5/5 runs, events p99 최대 9.503 ms, point-odds p99 최대 17.883 ms, errors 0과 drops 0입니다.
이 결과는 OTel sampling off인 단일 ARM macOS local gate이며 production capacity나 observability-on
성능을 인증하지 않습니다. Remote는 branch `main`, `learning/current`와 annotated `odds-v1.0.1`만
advertise합니다.

#### Odds backlink corrective transition

위 실행 원장은 `5a97082e` legacy source에서 첫 정화 publication으로 전환한 당시의 audit truth입니다.
그 기록과 최초 60행 source crosswalk·147행 learning disposition은 수정하거나 소급 재해석하지 않습니다.
첫 publication 뒤 source README에 공식 Document Box B7 backlink가 빠진 것을 발견해, 같은 2026-07-21
KST에 별도의 corrective transition으로 source·release·learning basis를 다시 고정했습니다.

첫 정화 `main` `f6f358d914f429749dec83ef7a266ae7d50778b5`(tree
`5fc7107b3f5fbb4d0d890e1602d17b9073748e72`)는 corrected `main`
`54f89079fecc4690c0126398103accd31437e8d1`(tree
`5fe2d781ee4d08adfa8551706593449e076715b2`)로 교체했습니다. Frozen exact source diff는
`README.md` 한 경로의 1 insertion·0 deletions뿐이며 source/config/test/build path deletion은 0입니다.
One-based source ordinals 1–17의 commit OID, parent와 순서는 그대로이고 ordinal 18만 같은 parent,
subject, author/committer identity·timestamp와 three-section message를 유지한 채 backlink 한 줄을 포함하는
새 object가 됐습니다. 18개 answer, 13개 practice와 5개 명시적 omission의 수량식은 바뀌지 않습니다.

Annotated `odds-v1.0.1` object는 `b0d1f674a4877ab2bfc43f0e61919cb483f34aab`에서
`f82124f469ddae728379135ee5de3df36edceee5`로 교체했고 corrected `main`으로 peel됩니다. 첫 learning tip
`6b75f6cb5110e7b5023b3967e5747a4dc36247b9`는 corrected source freeze 뒤 다음 actual-time publication
세 commit으로 다시 고정했습니다.

| phase | corrected commit | tree | parent | actual KST time |
| --- | --- | --- | --- | --- |
| notes/evidence | `f7df4eb2592e78307fe3d97c2c33947da4d107cf` | `6b6fa8a3eff3ab7a7724920708140c75016d0ef8` | source `54f89079fecc4690c0126398103accd31437e8d1` | `2026-07-21T10:40:23+09:00` |
| answers | `25b02ad6a60cb642594a57f04ba708c53fb5baaf` | `d3c0b06f4ef6b031891bab4e6faa9c2eaef58123` | notes/evidence | `2026-07-21T10:40:45+09:00` |
| practices / tip | `df00e5cdefbe9d55fbe4cb828a9d2c0ee5b1b8af` | `f9d8698c786a9863fbe620f358fe9e1a2e91a607` | answers | `2026-07-21T10:41:00+09:00` |

Publication의 43개 changed path는 old/new path→blob matrix에서 39개가 OID-identical이고 4개만
corrective review 대상입니다. `docs/README.md`는 source tip·tree를, `docs/commits/017.md`는 backlink
책임과 exact source diff를, `docs/commits/README.md`와 `docs/practice/README.md`는 corrected basis·tag와
수량 원장을 반영했습니다. Answers 전체를 다시 쓰거나 동일 blob을 재독하지 않았으며 변경된 answer
017을 직접 대조한 뒤 해당 practice omission 설명만 다시 검토했습니다. Final 수량은 계속
`18 source = 18 answers + 0 exclusions`, `18 answers = 13 practices + 5 omissions`입니다.

Corrective object 관계와 notes publication에서 byte-identical로 보존한 load evidence 일곱 blob은
[`data/migrations/sportsbook-odds-feed-service-correction-crosswalk.tsv`](data/migrations/sportsbook-odds-feed-service-correction-crosswalk.tsv)에
분리해 고정합니다. Header 포함 17줄, SHA-256
`57107cff635e6e575772d2b21e4cfb77b4a8434592f38a43c86f8946d22dc134`입니다. 다섯 transition row는
source main, annotated tag, notes, answers와 practices tip의 old→new object·tree를 닫습니다. 네
`corrected_blob` row는 위 4개 review 대상 path의 old/new blob OID와 review relation을 고정하고, 일곱
`evidence_blob` row는 exact path와 old/new 동일 blob OID를 corrected notes commit
`f7df4eb2592e78307fe3d97c2c33947da4d107cf`에 결박합니다.

원격 정정은 old `main` `f6f358d914f429749dec83ef7a266ae7d50778b5`, old annotated tag object
`b0d1f674a4877ab2bfc43f0e61919cb483f34aab`와 old `learning/current`
`6b75f6cb5110e7b5023b3967e5747a4dc36247b9`의 exact lease를 건 단일 atomic push로 수행했습니다.
후속 `ls-remote`는 branch `main`, `learning/current`와 annotated `odds-v1.0.1`만 확인했고, 별도 HTTPS
fresh clone에서 72 tests, failure·error·skip 0, Spotless 55 paths, Checkstyle 0, executable package,
source/corpus topology와 navigation gate가 green입니다.

Correction 발견 시점에 첫 bundle의 삭제 lifecycle이 아직 닫히지 않았으므로 다음 source-only rollback
bundle 두 개를 모두 유지했습니다. 당시 둘 다 learning ref와 learning-only object를 포함하지 않았고,
corrective Document Box publication, authenticated 30-project remote navigation과 후속 fresh-clone gate가
끝날 때까지 삭제하지 않는 상태였습니다. 실제 삭제 여부는 후속 closure entry에 별도로 기록하기로
했습니다.

- pre-initial migration: `/Users/woopinbell/Documents/Codex/2026-07-19/1/work/backend-lane/sportsbook-odds-feed-service/source-audit/sportsbook-odds-feed-service-5a97082e-source.bundle`, SHA-256 `bdd8f34ec1e1613d90e09006f451839f733e5a13606b01455fb9031c16f2013d`
- corrective transition: `/Users/woopinbell/Documents/Codex/2026-07-19/1/work/backend-lane/sportsbook-odds-feed-service/source-audit/sportsbook-odds-feed-service-f6f358d-correction-source.bundle`, SHA-256 `77fd71025ffae3fd2a9f1df88abb9b1a22a519e267a93f2e069bb7d8252d98a3`

##### Odds rollback closure

`2026-07-21T11:09:57+09:00`에 corrective publication과 후속 검증이 모두 green임을 확인하고 Odds의
임시 source-only rollback lifecycle을 닫았습니다. Project remote의 exact-only topology는 branch
`main` `54f89079fecc4690c0126398103accd31437e8d1`, branch `learning/current`
`df00e5cdefbe9d55fbe4cb828a9d2c0ee5b1b8af`, annotated tag object
`f82124f469ddae728379135ee5de3df36edceee5`뿐이며 tag는 corrected `main`으로 peel됩니다. Project
HTTPS fresh clone은 72 tests, failure·error·skip 0, source/corpus gate와 navigation을 통과했습니다.

Corrective governance는 Document Box `08f49d658629a224bba33ab733d0fea81f260394`로 게시됐습니다. 별도
HTTPS fresh clone에서 remote branch가 `main` 하나뿐임을 확인했고 82/82 tests, local navigation 30개,
authenticated remote navigation 30개와 host Backend preflight가 모두 green입니다. Central Notes는
`dea11a7258a399bcb2ff224b8fb87b4879b323f1`에서 변경하지 않았고 `make check`와
`make check-backend`가 green입니다.

다음 두 등록 bundle과 correction restore copy는 검증 뒤 정확히 영구 삭제(permanent deletion)했습니다.

- `/Users/woopinbell/Documents/Codex/2026-07-19/1/work/backend-lane/sportsbook-odds-feed-service/source-audit/sportsbook-odds-feed-service-5a97082e-source.bundle`, SHA-256 `bdd8f34ec1e1613d90e09006f451839f733e5a13606b01455fb9031c16f2013d`
- `/Users/woopinbell/Documents/Codex/2026-07-19/1/work/backend-lane/sportsbook-odds-feed-service/source-audit/sportsbook-odds-feed-service-f6f358d-correction-source.bundle`, SHA-256 `77fd71025ffae3fd2a9f1df88abb9b1a22a519e267a93f2e069bb7d8252d98a3`
- `/Users/woopinbell/Documents/Codex/2026-07-19/1/work/backend-lane/sportsbook-odds-feed-service/source-audit/correction-rollback-restore`

Learning bundle은 처음부터 생성하지 않았습니다. Project 작업 디렉터리에서 실행한
`find /Users/woopinbell/Documents/Codex/2026-07-19/1/work/backend-lane/sportsbook-odds-feed-service -name '*.bundle'`
결과는 0개이며, 등록된 source-only rollback bundle이나 restore copy는 더 남아 있지 않습니다.

### `sportsbook-betting-service` source product-token allowlist

`sportsbook-betting-service`의 source에서 대소문자를 구분하지 않은 `cursor`는 AI 도구 provenance가
아니라 keyset pagination의 공개 query parameter, continuation field, repository boundary와 이를 검증하는
테스트 이름입니다. 이 예외는
[`data/migrations/sportsbook-betting-service-source-allowlist.tsv`](data/migrations/sportsbook-betting-service-source-allowlist.tsv)에
기록한 exact path/blob 15쌍, 8개 path에만 적용합니다. Header 포함 16줄, SHA-256
`088a5a9efed8bb55b905bd512ed786e9f910f363bd66608950db739a2376dfd1`입니다.

15개 unique path/blob의 본문에는 matching line 50개와 raw case-insensitive occurrence 68개가 있고,
32개 final source commit에서의 path/blob/commit association은 139개입니다. Final tree에는 그중 현재
8개 blob, matching line 30개와 raw occurrence 40개가 남습니다. 각 행은 최초·마지막 source ordinal과
commit, historical-only 또는 final reachability, source 책임과 직접 review 근거를 함께 고정합니다.
이 allowlist는 ref/tag 이름, annotated tag message, commit identity·message·trailer, tool-control artifact,
등록하지 않은 path/blob, 다른 token이나 learning/governance surface로 확장되지 않습니다.

### `sportsbook-betting-service` 실행 원장

이 실행은 old `main` `0fd30c8ee5727eaff01c11e243a0a6fcb8f479ea`(tree
`e0d88040ecca9104c4ce9b4b2f5e12867f7f9574`)와 모든 advertised source tag를 고정한 뒤 수행했습니다.
Final source는 `main` `6ceacca9fceab3638bd710e55a7f1131c180e0a7`, tree
`422a168b44b089d9d1d512126d3db01a01d17ada`인 32개 linear commit이며 merge는 0개입니다. Source
timestamp는 승인된 `2026-04-01`–`2026-04-26` KST window 안에 있고 patch 책임 순서를 보존합니다.
Old main과 final source의 의도된 정화 diff는 `.gitignore`, `README.md`,
`load-test/scenarios/placement_load.js`, `src/main/java/com/sportsbook/betting/infrastructure/id/UuidV7.java`
네 path, 7 insertions·21 deletions입니다.

Annotated `betting-v1.0.1` object는
`d00851281e8c679937bbffa6da59d00460904500`이고 final `main`으로 peel됩니다. Tagger time은
`2026-04-26T18:16:07+09:00`입니다. 다음 old source tag는 exact object/target을 확인한 뒤 remote에서
삭제하거나 교체했습니다.

| old source tag | old object | peeled target | final disposition |
| --- | --- | --- | --- |
| annotated `betting-v1` | `978da92ea9cafa5297fb3fdfa0eb7ee88f9680b0` | `a4009f118b77f6739b591a3c2f87dcfd98c03c21` | 삭제 |
| annotated `betting-v1.0.1` | `d0ddd80e51857c6579b50c9fd410912d0be09157` | `0fd30c8ee5727eaff01c11e243a0a6fcb8f479ea` | final annotated object로 교체 |
| annotated `pre-betting-v1` | `88b963a80610805a1679a5d9bc623ca6ac616ebc` | `c592167e0a29439724fd1d4a1e11eb7bf66c4ec9` | 삭제 |
| lightweight `v0.1.0` | `ab72c3675f5d158d15c352923da493ac06538b16` | 같은 commit | 삭제 |

Old source ref union은 merge 없는 69개 unique commit입니다.
[`data/migrations/sportsbook-betting-service-source-crosswalk.tsv`](data/migrations/sportsbook-betting-service-source-crosswalk.tsv)은
그 전부의 old/new parent·tree·stable patch ID·timestamp·subject·reaching source ref·final 책임과 disposition을
고정합니다. Header 포함 70줄, SHA-256
`21a4dc2be126c626652d4fc0eadb0c8797cb0ff8eba5eb59a6d8baeeb76b9780`입니다. 60개 old object는 final
책임으로 map되고 9개는 learning publication으로 명시적 제외됩니다. Mapped
관계는 patch-identical 50개와 provenance·placeholder·navigation 정화를 포함한 curated 10개입니다.
Final ref/tag 이름, annotated tag message, 32개 commit metadata·message·trailer와 allowlist 밖 path/blob의
금지 provenance 감사 결과는 0건입니다. Historical `source-freeze.txt`의
`prepared-not-executed`는 원격 전환 전 preflight 기록일 뿐 현재 remote 상태가 아닙니다.

Migration 전 source-only rollback bundle은
`/Users/woopinbell/Documents/Codex/2026-07-19/1/work/backend-lane/sportsbook-betting-service/source-audit/sportsbook-betting-service-0fd30c8e-source.bundle`,
SHA-256 `95fbd8d37634fa27f013c8e584e1667b97c14243de721e38860b6638f9964611`입니다. Old `main`과 위 네
source tag, 모두 5개 ref만 포함하며 learning ref는 0개입니다. `git bundle verify`, snapshot strict fsck와
별도 restore strict fsck가 PASS입니다. Learning bundle, archive ref와 보존 tag는 만들지 않았습니다.
Document Box와 Central Notes publication, 인증 remote navigation과 governance fresh-clone gate가 끝날
때까지 이 bundle과 등록된 restore copy를 유지합니다. 실제 영구 삭제 시각과 삭제 뒤 0-bundle 검사는
후속 rollback-closure entry에서만 기록합니다.

Learning 입력 두 개는 서로 ancestor가 아니었습니다. 276개 union path는 identical 271개, divergent
2개와 `learning/betting-v1.0.1`-only 3개였습니다. 동일 blob은 재독하지 않고 source compatibility,
responsibility coverage, link·metadata와 유효한 고유 내용으로 donor와 폐기 대상을 판정했습니다.

| deleted old learning ref | tip | tree | disposition |
| --- | --- | --- | --- |
| `learning/betting-v1` | `4384d307461be43d3ae4761a8de60615a2594336` | `bebd3140dd4b21cb452724b51502b3413c13434e` | source-split corpus donor; canonical path와 frozen metadata로 보정 뒤 삭제 |
| `learning/betting-v1.0.1` | `167b3b512313ce4ced13b466d7c6e50dc0096709` | `d1b0954d376f9ffd88573b548579c4e9a383caac` | navigation-only wrapper와 versioned duplicate를 폐기한 뒤 삭제 |

Per-path 최종 판정은
[`data/migrations/sportsbook-betting-service-learning-disposition.tsv`](data/migrations/sportsbook-betting-service-learning-disposition.tsv)에
고정합니다. Header 포함 277줄, SHA-256
`5b5a90005e9d1d547671470d77826c29580473a3e492a34ef6a7e7db4d17c7b2`입니다. 각 행은 두 old
ref/tip/tree와 mode/blob, stable ID, relation, disposition, review mode, frozen source basis, final path/blob,
reason, reviewer와 actual review time을 포함합니다. Scope는 final-source 95개, final-learning 62개,
discarded 119개입니다. Final owner review barrier는
`seungwoo7050/repository-owner-review`, `2026-07-21T12:44:00+09:00`이며 62개 publication path를 전부
직접 읽고 5개 finding을 수정해 remaining finding 0으로 닫았습니다.

전담 집필자는 frozen source `6ceacca9fceab3638bd710e55a7f1131c180e0a7`와 tree
`422a168b44b089d9d1d512126d3db01a01d17ada`만을 basis로 사용했습니다. 30개 answer와 answer index의
31개 direct-read barrier는 `2026-07-21T12:26:15+09:00`에 끝났습니다. 그 뒤에만 27개 practice와
practice index를 읽었고 28개 barrier는 `2026-07-21T12:39:01+09:00`에 끝났습니다. Entry와 두
reflection의 별도 3개 direct read는 `2026-07-21T12:34:35+09:00`입니다. 실패 hunk만 다시 읽었으며
전체 검토를 반복하지 않았습니다. 집필자는 source를 수정하거나 stage, commit, tag, push하지 않았습니다.

Final `learning/current`는 source freeze 뒤 actual-time publication 세 commit으로만 구성됩니다.

| phase | commit | tree | parent | actual KST time |
| --- | --- | --- | --- | --- |
| notes/entry | `5f3530c4cdb1a3b91090626eb0ff3107630b0e51` | `a711547e1b6b9bab000c207d720f3b922189ecce` | source `6ceacca9fceab3638bd710e55a7f1131c180e0a7` | `2026-07-21T12:45:27+09:00` |
| answers | `4bcec3a048055d7307903f8ccdcf20bbf60600b9` | `47f4d1bea3131d4d732fad62bbf0a04e968f8404` | notes/entry | `2026-07-21T12:46:10+09:00` |
| practices / tip | `9c8038887599368f57ac155978af75e575980307` | `06994f2ad51df10fc505b0c43f63c32e37a59900` | answers | `2026-07-21T12:46:37+09:00` |

Final learning tree의 publication path는 62개이고 path/blob manifest SHA-256은
`7e08fd19054b841dbaf9b53f46db368efa6a8ab394b4a46748f7a0bab59403de`입니다. 수량식은
`32 source commits = 31 answer-covered responsibilities + 1 source-document exclusion`입니다. Answer
022가 source ordinal 22와 23의 두 책임을 함께 다루므로 31개 covered responsibility는 30개 answer
file에 대응합니다. 두 번째 수량식은 `30 answers = 27 practices + 3 omissions (000, 023, 027)`입니다.
Final source와 learning의 `docs/**` 밖 diff는 0이고 relative link 104개와 publication validator 3,445
checks는 실패 0입니다.

Historical gate는 original main 34개 ordinal과 candidate 32개 ordinal의 clean test-compile을 모두
PASS했습니다. Original responsibility gate가 있는 ordinals 1, 2, 3, 4, 5, 8, 10, 12, 16, 18, 20,
22, 28, 30, 31도 PASS입니다. Host candidate와 별도 HTTPS fresh clone의 Java 17
`./mvnw -B clean verify`는 모두 130 tests, failure·error·skip 0, Spotless 67 Java paths, Checkstyle 0과
실행 가능한 Spring Boot JAR를 확인했습니다. 두 JAR는 크기 85,461,143 bytes로 같지만 host candidate
SHA-256 `ec31f3cf646cfbe7bdb36d92a6a1f286a415ac1e912821402d844d50e4ee9fd1`와 fresh-clone SHA-256
`982d0d6e87f6d2091a78918e21978d3871af1b848f3f16b8ee1dd2d30f596046`가 다르므로 reproducible JAR를
주장하지 않습니다.

Controlled-local placement evidence는 149.589 RPS, p95 120.6648 ms, p99 148.495 ms, errors 0입니다.
이 controlled-local placement benchmark threshold `p95 < 50 ms`, `p99 < 100 ms`는 RED입니다. Production
goal `p99 < 100 ms`·`10,000 concurrent bets`는 이 evidence에서 검증하지 않았습니다.
100개 same-key 동시 요청은 HTTP 201/409와 no 5xx만 증명합니다. Accepted DB row 하나 또는 Wallet debit
하나를 증명하지 않습니다.

Project remote는 branch `main`, `learning/current`와 annotated tag `betting-v1.0.1`만 advertise하며
private/default-`main` 상태입니다. Project HTTPS fresh clone에서 source tree, exact topology, clean build,
learning tree, source/corpus diff와 navigation을 검증했습니다. 이 첫 governance publication은 remote
branch가 `main` 하나뿐인 Document Box base `3f05a7911ff2333cd4564855619c2d5b124b1955`와 Central Notes base
`dea11a7258a399bcb2ff224b8fb87b4879b323f1`의 fresh clone, drift 0에서 준비했습니다. 새 governance
commit SHA, authenticated 30-project navigation과 governance fresh-clone 결과는 실제 publication 뒤
rollback-closure entry에서 고정하며 이 1차 원장에서 미리 만들지 않습니다.

#### Betting rollback closure

`2026-07-21T14:09:31+09:00`에 project와 두 governance publication의 후속 검증이 모두 green임을
확인하고 Betting의 임시 source-only rollback lifecycle을 닫았습니다. 삭제 직전
`sportsbook-betting-service-0fd30c8e-source.bundle`의 SHA-256은
`95fbd8d37634fa27f013c8e584e1667b97c14243de721e38860b6638f9964611`이었고, `git bundle verify`는
complete history와 old source ref 5개를 확인했습니다. 등록된 `rollback-restore`의
`git fsck --strict`도 PASS였습니다.

Project remote의 exact-only topology는 branch `main`
`6ceacca9fceab3638bd710e55a7f1131c180e0a7`, branch `learning/current`
`9c8038887599368f57ac155978af75e575980307`, annotated tag object
`d00851281e8c679937bbffa6da59d00460904500`뿐이며 tag는 `main`으로 peel됩니다. Project fresh gate가
green이고, Betting governance는 Document Box
`7e9131deb1c4b3e4690b22f3f8f0c429a77c7448`와 Central Notes
`d6b7ffbb9a426b422abc02caea1eb1802d34f174`로 게시됐습니다. 두 governance fresh gate와 authenticated
remote navigation 30개도 PASS했습니다.

위 검증 뒤 다음 두 exact target을 영구 삭제(permanent deletion)했습니다.

- `source-audit/sportsbook-betting-service-0fd30c8e-source.bundle`
- `source-audit/rollback-restore`

삭제 후 `2026-07-21T14:09:31+09:00` 검사에서
`sportsbook-betting-service` 작업 디렉터리 아래 `*.bundle`은 0개였고 위 두 exact path는 모두
존재하지 않았습니다. Learning bundle은 처음부터 생성하지 않았습니다.

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

위 `cloud-launch-training` 실행 원장이 이 migration에서 승인한 ref 이동·교체·삭제와 learning 단일화에
대해서는 아래 보존 지시를 대체합니다. 아래 SHA와 당시 topology는 crosswalk 입력으로만 남고 현행 ref
보존 지시가 아닙니다.

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

위 `cloud-launch-training` 실행 원장이 이 migration에서 승인한 old source tag 삭제와 old learning ref
삭제를 대체 disposition으로 고정합니다. 아래 오류와 object 정보는 감사 입력으로 남지만 더 이상 active
ref 또는 immutable corpus 보존을 요구하지 않습니다.

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
