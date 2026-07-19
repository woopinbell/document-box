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
- `format-printer`, `signal-message-bus`, `thread-dining`, `small-shell`, `stack-sort`의 current source release에는
  learner-navigation-only commit을 추가하지 않았습니다. 다섯 저장소의 main backlink 부재는 명시적
  예외이며 current ref·학습 진입점은 Document Box 단계 카드가 소유합니다. 이 예외는 각각
  `be4966f3c1d176453a34b609036ef4998fa8b022`/`fe7a0d79cb9733f4f6871e5164a305907cd7b78e`,
  `ed859ce08c0d84154c21be6ffd6cdb1ea1c353c3`/`7563b6325e6c1a31bc63dbf22b935bb155e0e434`,
  `94ccaa4085af3decfd6d7bba2ff0b879954947e5`/`983bb1f4ce52ce33feb68955d9c0788670b12fb4`,
  `0fb1f6bf4825890f7b657ce5de918aed52a8318d`/`3e7164817b3883783c80c6a1ced90531faf85efe`,
  `51325493a5e0e10f72dcfc04079d3b4f2c96488e`/`dc08a9be3ec27a5096be753ef7f7126ce8b713e9`
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
