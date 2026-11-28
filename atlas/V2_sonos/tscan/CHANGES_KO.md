# SONOS P/E 덱: 원래 코드와 현재 코드 비교

- 원래 코드: 팀의 `SONOS_PRG_ERS.in` (Program과 Erase가 한 덱). 아래 "원래 N"은 이 파일의 줄 번호.
- 현재 코드: `tscan/77fix/` (77 K), `tscan/300fix/` (300 K). 두 폴더의 덱은 27번째 줄 `set temp=`만 다르다.
  - `SONOS_PGM_PF_77K_fix.in` (PGM 덱): 새 소자 읽기 + Program
  - `SONOS_ERS_PF_77K_fix.in` (ERS 덱): Erase
  - `SONOS_READ_PGM_77K_fix.in`, `SONOS_READ_ERS_77K_fix.in` (읽기 덱): PGM/ERS 상태 트랜지언트 읽기
- 실행 순서(같은 폴더): PGM 덱 → [ERS 덱, READ_PGM 덱 동시 가능] → READ_ERS 덱 (ERS 덱이 끝난 뒤)

## A. PGM 덱 (원래 1~148번 줄과 비교)

| # | 원래 | 현재 | 이 변경의 이유 |
|---|---|---|---|
| A1 | 6 `go atlas` | 6 `go atlas simflags="-160 -P 4"` | `-160`: 77 K에서 exp(E/kT) 같은 값이 64비트 범위를 넘어 첫 Program 단계에서 "NaN or Inf in SONOS tunnel current". 300 K도 64비트에서 정밀도 한계로 멈춘 적이 있어(리텐션 덱) 두 온도 모두 160비트. `-P 4`: CPU 4개. 결과는 바이트 단위로 같고 시간만 줄어듦(Program 램프 시험 35.7 → 23.5분) |
| A2 | 89, 91, 93 `material ...` (top oxide, bottom oxide, nitride) | 같은 줄 끝에 `ni.min=1e-60` | 세 층은 "semiconductor"로 정의되어 있고 밴드갭이 매우 크다. 77 K에서 고유 캐리어 농도가 계산 범위 아래로 떨어져 펄스 유지 구간에서 전자 갱신이 잡음 수준에서 멈췄다. `ni.min`은 고유 농도의 최솟값(매뉴얼). 1e-60이라 물리적으로는 0과 같다 |
| A3 | (없음) | 95~96 `models srh temperature=@temp` (`contact` 앞) | **핵심 원인.** 매뉴얼 2.5.2 순서 `material → models → contact → method`. 원래 위치(104, `contact`/`nitridecharge`/`method` 뒤)에서는 77 K가 일부만 적용됨: 이동도는 77 K, SS 93 mV/dec·VT 하강은 300 K 거동. 이 줄로 77 K SS 22.1 mV/dec, VT 0.701 V(TEST_O1), Erase −12 V 통과(TEST_O2) |
| A4 | 97 `nitridecharge ... elec.depth=@Enit ...` | 100 같은 줄에 `hole.depth=@Enit` | `pf.nitride`(A9)는 홀 트랩 깊이를 쓴다. 기본값 −999 eV이고 홀 트랩(`nt.p=1e19`)이 있으면 NaN. 팀이 정한 홀 트랩 깊이가 없어서 전자 트랩 깊이(Enit = 1.2 eV)와 같게 둠(가정) |
| A5 | 104 `models srh` | 107 `models srh temperature=@temp` | `set temp=77`은 변수만 만들고, 온도는 `models`의 `temperature=`로만 적용된다. 원래 코드는 77 K 덱도 300 K로 계산했다. 이 줄은 A3과 같은 내용이라 남아 있어도 결과에 영향 없음 |
| A6 | 110 `solve vcgate=0 vstep=-0.1 name=cgate vfinal=-1` | 삭제 | 읽기를 −1 V가 아니라 0 V에서 시작. 77 K에서 전하가 있는 상태를 음의 게이트 전압을 거쳐 읽으면 채널이 끝까지 안 켜지는 잘못된 해로 갔다(B7/B8). 모든 읽기를 같은 방식(0 V 시작)으로 맞춤. 새 소자 VT가 0.78 V라 0 V 시작으로 충분 |
| A7 | 111 `solve vdrain=0.1` | 113~117 `vdrain=0.0001` → `0.001` → 0.001 간격 0.01 V → 0.005 간격 0.1 V | 77 K에서 드레인 0 → 0.1 V를 한 번에 풀면 발산. 작은 단계로 올리면 수렴(diag H2, TEST_O1) |
| A8 | 114 `solve vcgate=-1 ... vfinal=6` | 120 `solve vcgate=0 ... vfinal=6` | A6과 같은 이유 |
| A9 | (없음) | 127 `solve prev` (`solve init` 다음) | `solve init`은 초기값만 만든다(반복표에 psi만 나옴). `solve prev`는 같은 바이어스에서 전위·전자·홀을 모두 푼다. Program 트랜지언트를 완전한 해에서 시작하려는 것. 77 K에서 검증된 TEST_O2와 같은 순서. 이 줄 없이 77 K를 시험한 적은 없음 |
| A10 | (없음) | 130 `models srh pf.nitride temperature=@temp` | 원래 코드의 트랩 방출은 `tau.n`/`tau.p`(고정 시간)뿐이라 온도와 무관. `pf.nitride`(Poole-Frenkel 방출)는 열과 전계로 트랩 전자가 빠져나가는 항이라 온도에 따라 달라진다. 300 K/77 K 비교에 필요한 메커니즘이라 두 온도 모두 추가. `pf.nitride`가 켜지면 `tau.n`/`tau.p`는 쓰이지 않음(diag R2a/R2b 결과 동일). 트랜지언트에서만 켬(A14) |
| A11 | 123 `solve vcgate=$vcgate ramptime=1e-9 tstep=1e-12 tfinal=1e-9 proj` | 132~136 `set vcgate_split=$vcgate/10` / `method dt.max=5e-12` / `solve vcgate=$vcgate_split ramptime=1e-10 tstep=1e-12 tfinal=1e-10` / `method dt.max=2e-11` / `solve vcgate=$vcgate ramptime=9e-10 tstep=2e-12 tfinal=1e-9` | ① `proj` 제거: `proj`는 직전 두 해를 직선으로 연장해 다음 출발값을 정한다(매뉴얼 SOLVE PROJECT). 램프에서는 터널 전류가 몇 자리씩 바뀌어 출발값이 틀려지고, 77 K에서 Vg 2.1~2.4 V 근처에서 NaN이 났다(시도한 모든 시간 간격에서). `proj` 없이 상한 5e-12로 램프 전체를 풀면 16 V까지 계산됨(diag P14). 일정 전압 유지 구간에는 `proj`를 그대로 둠. ② `dt.max`: 없으면 13 V 근처에서 시간 간격이 0.6 ns까지 커져 NaN. ③ Vg/10(1.6 V)에서 분할: 채널이 생기는 구간(새 소자 VT 약 0.6~0.8 V)을 포함한 0~1.6 V는 5e-12, 나머지는 2e-11로 풀어도 10 ns에서 결과 차이 0.03 %이고 2.5배 빠름(diag P16). 시간 단축을 위한 분할. 기울기 16 V/ns와 전체 1 ns는 원래와 같음 |
| A12 | 124 `method dt.min=1.0e-9` | 137 `method dt.max=1e-3 dt.min=1e-25 cx.tol=1e-4` | ① `dt.min=1e-25`: 램프 직후에는 1 ns보다 작은 시간 간격이 필요한데 1e-9가 막아서 멈췄다. ② `dt.max=1e-3`: 램프에서 정한 상한 2e-11이 유지 구간까지 이어지면 100 µs를 20 ps씩 풀어야 한다. 상한을 다시 풀어줌. ③ `cx.tol=1e-4`: 77 K에서 전자 갱신량이 2~5e-5에서 더 줄지 않았고 기본 기준은 1e-5. 300 K 덱도 같은 값이라 두 온도 조건은 같음 |
| A13 | 127, 129 `method dt.min=1.0e-8`, `1.0e-7` | 140, 142 같은 줄에 `cx.tol=1e-4` | METHOD 값이 다음 줄에도 유지되는지 매뉴얼에 명시가 없어서 줄마다 다시 지정 |
| A14 | 130 `solve tstop=@TPGM proj` 다음 (없음) | 146~151 하강 구간: `method dt.max=2e-11 dt.min=1e-25` / `solve vcgate=$vcgate_split ramptime=9e-10 tstep=2e-12 tstop=9e-10 relative` / `method dt.max=5e-12 dt.min=1e-25` / `solve vcgate=0 ramptime=1e-10 tstep=1e-12 tstop=1e-10 relative` / `method dt.max=1e-3 dt.min=1e-25` / `solve tstop=1e-6 relative proj` | 원래는 펄스 뒤 `solve init`으로 0 V에 돌아갔다. 77 K에서 질화막에 전하가 있으면 `solve init`의 초기값이 크게 틀려 발산(cool77 v1/v2). 16 V에서 정적 계산으로 내려가는 것도 실패(트랩이 고정된 채 고전계 주입이 계속돼 정상 상태가 없음). 그래서 상승 구간을 거꾸로 한 하강 구간(16 → 1.6 V 0.9 ns, 1.6 → 0 V 0.1 ns)을 트랜지언트로 풀고, 0 V에서 1 µs 유지 후 저장. `relative`: 지금 시각부터 센다(매뉴얼 SOLVE RELATIVE) |
| A15 | 139 `solve init` | 163~165 `models srh ^pf.nitride temperature=@temp` / `load infile=SONOS_PGM_...str master` / `solve prev` | ① `solve init` 제거: A14와 같은 이유. ② `^pf.nitride`: 정적 계산에서는 트랩 점유가 고정되는데 PF 항은 계속 전자를 내보내 정상 상태가 없다(300 K에서 NaN). `pf.nitride`를 빼고 쓰기만 하면 꺼지지 않고 `^`로 명시해야 꺼진다(매뉴얼 2.5, diag D1 확인). ③ `load`: 저장한 0 V 상태를 그대로 불러온다(트랩 전하까지 정확히 복원, diag R5a). ④ `solve prev`: 불러온 바이어스(0 V)에서 다시 푼다 |
| A16 | 142 `solve vdrain=0.1` | 168~171 작은 단계 드레인 램프 | A7과 같은 이유. 게이트를 먼저 1 V로 올린 뒤 드레인을 올리는 순서(원래 141번 줄 유지)는 77 K PGM 상태에서 수렴한 순서(cool77 v2) |
| A17 | 147 `solve init` | 삭제 | A14와 같은 이유. Erase는 A14에서 0 V로 저장한 `SONOS_PGM_...str`에서 시작하므로 필요 없음 |

이 덱 끝의 정적 읽기(167~175)는 남아 있다. 77 K에서 3.6 V까지만 정상이라 결과에는 쓰지 않고, 트랜지언트 읽기와 비교하는 확인용(VT 차이 5.5 mV)으로만 쓴다.

## B. ERS 덱 (원래 149~181번 줄과 비교)

앞부분(6, 89/91/93, 95~96, 100번 줄)은 PGM 덱 A1~A4와 같다.

| # | 원래 | 현재 | 이 변경의 이유 |
|---|---|---|---|
| B1 | (한 덱 안에서 Program 다음에 이어짐) | 106~111 `models srh ^pf.nitride ...` / `load infile=SONOS_PGM_...str master` / `solve prev` | Program과 Erase를 두 덱으로 나눔. Erase만 다시 돌릴 때 1.5시간 걸리는 Program을 반복하지 않기 위해서. 나머지는 A15와 같은 이유 |
| B2 | 151 `solve init` | 삭제 | A14와 같은 이유. 불러온 상태가 이미 0 V |
| B3 | (없음) | 118 `models srh pf.nitride temperature=@temp` | A10과 같은 이유 |
| B4 | 155 `solve vcgate=$ecgate ramptime=1e-9 tstep=1e-12 tfinal=1e-9` | 120~121 `method dt.max=5e-12 dt.min=1e-25 cx.tol=1e-4` / `solve vcgate=$ecgate ramptime=1e-9 tstep=1e-12 tstop=1e-9 relative` | ① `dt.max=5e-12`: 없으면 77 K Erase 램프에서 시간 간격이 0.54 ns까지 커져 −7 V 근처에서 멈췄다(A3 수정 전에 관찰. 수정 후 이 줄 없이 시험한 적은 없음). Program 램프(A11)와 같은 이유. ② `dt.min=1e-25`, `cx.tol=1e-4`: A12와 같은 이유. ③ `relative`: 이 덱은 트랜지언트 직후 저장한 상태를 불러오므로 시간이 0부터 시작한다는 보장이 없다. 램프 모양(1 ns, −12 V)은 원래와 같음 |
| B5 | 156 `method dt.min=1.0e-9` | 122 `method dt.max=1e-3 dt.min=1e-25 cx.tol=1e-4` | A12와 같은 이유 |
| B6 | 157~164 `solve tstop=1.0e-8 proj` … `solve tstop=@TERS proj` (절대 시각) | 123~131 `solve tstop=9e-9 relative proj` … `solve tstop=4.9e-4 relative proj` | B4 ③과 같은 이유. 각 단계가 끝나는 시각(1e-8, 1e-7, 1e-6, 1e-5, 5e-4 s)은 원래와 같다. 예: 앞 단계가 1e-5 s에 끝나므로 4.9e-4 s를 더하면 5e-4 s(TERS) |
| B7 | 159, 161, 163 `method dt.min=...` | 125, 127, 129 같은 줄에 `cx.tol=1e-4` | A13과 같은 이유 |
| B8 | 164 다음 (없음) | 134~139 하강 구간(−12 → −1.2 V 0.9 ns, −1.2 → 0 V 0.1 ns, 0 V 1 µs) | A14와 같은 이유. 두 구간 모두 `dt.max=5e-12`: Erase 램프를 5e-12로만 시험했기 때문 |
| B9 | 171 `solve init` | 149~151 `^pf.nitride` / `load ...ERS...str` / `solve prev` | A15와 같은 이유 |
| B10 | 173 `solve vcgate=0 vstep=-0.1 name=cgate vfinal=-2` | 153 `solve vcgate=0 vstep=0.1 name=cgate vfinal=1` | A6과 같은 이유(−2 V를 거치는 읽기 실패). 게이트를 먼저 1 V로 올리는 순서는 A16과 같음 |
| B11 | 174 `solve vdrain=0.1` | 154~157 작은 단계 드레인 램프 | A7과 같은 이유 |
| B12 | 177 `solve vcgate=-2 ... vfinal=7` | 160 `solve vcgate=1 ... vfinal=7` | A6과 같은 이유 |

이 덱 끝의 정적 읽기(153~161)는 77 K에서 실패한다(덱은 계속 끝까지 감). 결과는 읽기 덱으로 얻는다.

## C. 읽기 덱 (새로 만듦: `SONOS_READ_PGM_77K_fix.in`, `SONOS_READ_ERS_77K_fix.in`)

앞부분은 ERS 덱과 같다. 116~123번 줄(PGM 예):

```
models srh ^pf.nitride temperature=@temp
load infile=SONOS_PGM_...str master
solve prev
method dt.max=1e-9 dt.min=1e-25
log outf=T77fix_PGM_...log master
solve vdrain=0.1 ramptime=1e-8 tstep=1e-12 tstop=2e-8 relative
solve vcgate=6.0 ramptime=6.0e-07 tstep=1e-12 tstop=6.0e-07 relative
log off
```

| 항목 | 이유 |
|---|---|
| 정적 대신 트랜지언트로 읽음 | 77 K에서 전하가 있는 상태를 정적으로 읽으면 바이어스 순서에 따라 잘못된 해가 나왔다: 채널이 7 V까지 안 켜짐, 58 mV 안에서 전류 7자리 점프(SS < 15.3 mV/dec, 77 K 물리 한계 아래), gm이 새 소자의 10배. 트랜지언트는 바로 전 시간 단계의 해에서 이어 풀기 때문에 이런 점프가 없다 |
| 드레인 10 ns 램프 후 20 ns까지 유지 | 드레인을 한 번에 주면 77 K에서 발산(A7)하므로 시간에 따라 올림 |
| 게이트 10 V/µs, `dt.max=1e-9` | 한 단계가 최대 0.01 V. 77 K SS 약 22 mV/dec라 한 단계에 전류 약 0.45자리. 게이트 충전 전류는 C·dV/dt = 2.4e-15 F × 1e7 V/s = 2.4e-8 A |
| 분석에서 Id = (I_drain − I_source)/2 (`tscan/tread_vt.py`) | 게이트 충전 전류는 소스와 드레인에 같은 방향으로 반씩 흐르므로 차이를 반으로 나누면 없어진다. 1e-9 A 아래에는 약 3e-10 A의 바닥이 남아 VT는 gm 방식과 1e-8/1e-7 A 기준으로 뽑음 |
| 끝 전압 PGM 6 V, ERS 5 V | VT와 gm 최댓값을 지나도록(77 K PGM VT 2.40 V·gm 최대 2.73 V, ERS 1.78 V·2.11 V) |
| `^pf.nitride` | 정적 읽기와 같은 모델 조건 |
| PGM/ERS 읽기를 덱 두 개로 나눔 | 한 덱에서 두 번째 블록의 `relative` 시간이 앞 블록의 끝 시각을 이어받아, ERS 읽기가 0.64 µs까지 Vg 0 V로 대기했다(결과 영향 없음, 시간 약 1.5시간 낭비). 나누면 READ_PGM을 ERS 덱과 동시에 돌릴 수도 있다 |
| 검증 | 77 K 새 소자에서 정적 읽기(TEST_O1)와 비교: VT_gm 0.7802 vs 0.7802 V, VT(1e-7 A) 0.7009 vs 0.7014 V, gm 1.923e-4 A/V 같음. 77 K PGM 상태에서 정적 읽기와 VT 차이 5.5 mV. 읽는 동안 전하 변화 0.05 % |

## D. 원인을 찾는 동안 넣었다가 뺀 것 (이번 정리에서 삭제)

| 항목 | 뺀 이유 |
|---|---|
| ERS 덱: Erase 램프를 −6.6 V에서 둘로 나누고 그 지점과 램프 끝 상태 저장(`SONOS_ERSm6p6V_...str`, `SONOS_ERSramp_...str`) | 정체 지점 직전 상태를 분석하려던 것. 기울기가 같아 계산 결과는 같음 |
| ERS 덱 `method` 줄의 `clim.dd=4.5e13` (8곳) | Si 기본값과 같은 값. PGM 덱에는 원래 없었음 |

## E. 원래 그대로인 것

구조·메시·영역·전극·도핑, `material`의 `ni.min` 외 값, `contact workf`, `nitridecharge`의 `hole.depth` 외 값(트랩 밀도, `elec.depth`, `sigmat.n`, `tau.n`/`tau.p`), `probe`, 펄스 조건(+16 V 100 µs, −12 V 500 µs), `output`/`save`/`log` 줄, 모델은 `srh`(+ 위의 `pf.nitride`).
