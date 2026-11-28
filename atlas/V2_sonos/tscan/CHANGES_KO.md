# SONOS P/E 덱 정리: 원래 코드와 현재 코드 비교

## 0. 파일

- 원래 코드: 팀의 `SONOS_PRG_ERS.in`. 아래 "원래 N"은 이 파일의 줄 번호.
- 현재 코드: 온도당 덱 하나.
  - `tscan/77fix/SONOS_PE_77K.in`
  - `tscan/300fix/SONOS_PE_300K.in`
  - 두 덱은 29번째 줄 `set temp=`만 다르다. 아래 "현재 N"은 이 덱의 줄 번호.
- 덱 하나가 순서대로 한다: 새 소자 읽기 → Program → PGM 읽기 → Erase → ERS 읽기.
- 출력 파일 (`…`는 `nt_5e+19|_Et_1.2|_Tbox_0.003|_Nsub_1e+17|_toxide_sio2|_cwf_4.05|_temp_77|`, 300 K 덱은 `_temp_300|`):

| 파일 | 내용 |
|---|---|
| `SONOS_initial_….log` | 새 소자 Id-Vg |
| `TRNS_PGM_….log` | Program 중 시간별 전하 |
| `SONOS_PGM_….str` | Program 후 상태 (0 V) |
| `TREAD_PGM_….log` | Program 후 Id-Vg |
| `TRNS_ERS_….log` | Erase 중 시간별 전하 |
| `SONOS_ERS_….str` | Erase 후 상태 (0 V) |
| `TREAD_ERS_….log` | Erase 후 Id-Vg |

## 1. 문제와 원인, 바꾼 곳

### 문제 1. 77 K 덱이 실제로는 300 K로 계산됨

- 증상: `set temp=77`인데 결과가 300 K와 같았다.
- 원인: `set temp=77`은 변수를 만들 뿐이다. 온도는 `models` 문의 `temperature=`로만 적용되는데 원래 코드에는 없었다.
- 바꾼 곳: 원래 104 `models srh` → 현재 109 `models srh temperature=@temp`.
  - 이유: 위 원인.
  - 이 줄의 위치가 문제 5의 원인이 되어, 현재 98에 같은 줄을 하나 더 넣었다. 109는 98과 같은 내용이라 남아 있어도 결과에 영향이 없다.
- 그 뒤에 추가한 `models` 문(현재 132, 164, 175, 183, 212)에도 모두 `temperature=@temp`를 붙였다.
  - 이유: `models` 문을 새로 쓸 때마다 온도를 같이 지정해 두기 위해.

### 문제 2. 77 K Program 램프에서 "NaN or Inf in SONOS tunnel current"

- 증상: 0 → 16 V 램프 중 NaN이 나거나, 시간 간격이 2 fs까지 줄어 진행하지 못했다.
- 원인 세 가지:
  - 64비트 숫자 범위를 넘음.
  - 램프 구간의 `proj`.
  - 시간 간격이 너무 커짐.

**원래 6 `go atlas` → 현재 6 `go atlas simflags="-160 -P 6"`**
- `-160`(160비트 계산)의 이유: 77 K에서 exp(E/kT) 같은 값이 64비트 범위를 넘는다. 64비트로는 읽기까지는 됐지만 첫 Program 단계에서 NaN이 났다. 300 K도 64비트에서 정밀도 한계로 멈춘 적이 있어(리텐션 덱) 두 온도 모두 160비트로 둔다.
- `-P 6`(CPU 6개)의 이유: 속도. `-P 4`로 시험했을 때 결과는 1개와 바이트 단위로 같았고, 시간이 35.7 → 23.5분으로 줄었다(Program 램프 10 ns 시험). 6개로 늘린 것은 사용자 서버 여유(48코어 중 약 32개)에 맞춘 것이고 결과는 바뀌지 않아야 한다(6개로 직접 비교한 적은 없음).

**원래 123 → 현재 134~138**

원래 123:
```
solve vcgate=$vcgate ramptime=1e-9 tstep=1e-12 tfinal=1e-9 proj
```
현재 134~138:
```
set vcgate_split=$vcgate/10
method dt.max=5e-12
solve vcgate=$vcgate_split ramptime=1e-10 tstep=1e-12 tfinal=1e-10
method dt.max=2e-11
solve vcgate=$vcgate ramptime=9e-10 tstep=2e-12 tfinal=1e-9
```
- `proj`를 뺀 이유:
  - `proj`는 직전 두 해를 직선으로 연장해 다음 계산의 출발값으로 쓴다(매뉴얼 SOLVE PROJECT).
  - 램프에서는 터널 전류가 몇 자리씩 바뀌어 이 출발값이 틀린다. 77 K에서 Vg 2.1~2.4 V 근처에서 NaN이 났고, 시간 간격을 0.25 ps까지 줄여도 같았다.
  - `proj` 없이 풀면 16 V까지 계산됐다.
  - 일정 전압을 유지하는 구간에는 `proj`를 그대로 둔다. 그 구간에서는 해가 천천히 변해 직선 연장이 맞기 때문이다.
- `dt.max`를 넣은 이유: 상한이 없으면 13 V 근처에서 시간 간격이 0.6 ns까지 커져 NaN이 났다.
- 1.6 V(Vg/10)에서 나눈 이유: 계산 시간을 줄이기 위해서다.
  - 채널이 생기는 구간(새 소자 VT 약 0.6~0.8 V)을 포함한 0~1.6 V는 작은 상한(5e-12)으로 푼다.
  - 나머지를 2e-11로 풀어도 10 ns 시점 결과 차이가 0.03 %였고, 2.5배 빨랐다.
- 램프 기울기(16 V/ns)와 전체 시간(1 ns)은 원래와 같다.

### 문제 3. 펄스 유지 구간에서 첫 단계부터 멈춤

- 증상: 램프가 끝나고 16 V(또는 −12 V)를 유지하는 첫 단계에서 진행하지 못했다.

**원래 124 `method dt.min=1.0e-9` → 현재 139 `method dt.max=1e-3 dt.min=1e-25 cx.tol=1e-4`**
- `dt.min=1e-25`의 이유: 램프 직후에는 1 ns보다 작은 시간 간격이 필요한데, `dt.min=1e-9`가 이를 막아 멈췄다.
- `dt.max=1e-3`의 이유: 램프에서 정한 상한 2e-11이 유지 구간까지 이어지면 100 µs를 20 ps 간격으로 풀어야 한다. 그래서 상한을 다시 크게 풀어준다.
- `cx.tol=1e-4`의 이유: 77 K에서 전자 갱신량이 2~5e-5에서 더 줄지 않았는데 기본 기준은 1e-5다. 300 K 덱도 같은 값을 쓰므로 두 온도 조건은 같다.

**원래 127, 129 → 현재 142, 144**
- 바꾼 것: `method dt.min=...` 줄에 `cx.tol=1e-4`를 다시 씀.
- 이유: METHOD 값이 다음 `method` 줄 이후에도 유지되는지 매뉴얼에 명시가 없어서, 줄마다 다시 지정한다.

**Erase도 같다: 원래 156, 159, 161, 163 → 현재 187, 190, 192, 194.** Erase 램프 앞(현재 185)에도 `dt.min=1e-25 cx.tol=1e-4`를 넣었다(이유 같음).

**원래 89, 91, 93 → 현재 91, 93, 95: `material` 문(top oxide, bottom oxide, nitride) 끝에 `ni.min=1e-60` 추가**
- 이유: 세 층은 "semiconductor"로 정의되어 있고 밴드갭이 매우 크다.
  - 77 K에서 고유 캐리어 농도가 계산 범위 아래로 떨어져, 유지 구간에서 전자 갱신이 잡음 수준에서 멈췄다.
  - `ni.min`은 고유 농도의 최솟값이다(매뉴얼). 1e-60이라 물리적으로는 0과 같다.

### 문제 4. PF 방출을 넣었더니 정적 계산이 발산

- 배경: 원래 코드의 트랩 방출은 `tau.n`/`tau.p`(고정된 방출 시간)뿐이라 온도와 무관하다. 그래서 `pf.nitride`(Poole-Frenkel 방출)를 추가했다.
  - PF 방출은 열과 전계로 트랩 전자가 빠져나가는 항이라 온도에 따라 달라진다.
  - 300 K/77 K 비교에 필요한 메커니즘이라 두 온도 모두 추가했다.
  - `pf.nitride`가 켜지면 `tau.n`/`tau.p`는 쓰이지 않는다(77 K에서 1초까지 결과가 바이트 단위로 같음).
- 증상: 정적 계산(읽기 등)에서 PF가 켜져 있으면 300 K에서 NaN이 났다. 또 `hole.depth`가 없으면 Program에서 NaN이 났다.

**현재 132, 183 `models srh pf.nitride temperature=@temp` 추가 (Program, Erase 트랜지언트 바로 앞)**
- 이유: PF 방출을 트랜지언트에서만 켠다.

**현재 164, 175, 212 `models srh ^pf.nitride temperature=@temp` 추가 (불러오기와 읽기 앞)**
- 이유 ①: 정적 계산에서는 트랩 점유가 고정되는데, PF 항은 계속 전자를 내보내 정상 상태가 없다(300 K NaN).
- 이유 ②: `models`에서 `pf.nitride`를 빼고 쓰기만 하면 꺼지지 않고, `^`로 명시해야 꺼진다(매뉴얼 2.5. 시험으로 확인: `^` 없이는 첫 정적 계산에서 실패).

**원래 97 → 현재 102: `nitridecharge`에 `hole.depth=@Enit` 추가**
- 이유: PF 계산은 홀 트랩 깊이를 쓴다. 기본값이 −999 eV라서 홀 트랩(`nt.p=1e19`)이 있으면 NaN이 난다.
- 값을 전자 트랩 깊이(1.2 eV)와 같게 둔 이유: 팀이 정한 홀 트랩 깊이가 없어서다. **가정**이다.

### 문제 5. 77 K Erase 램프가 −7~−8 V에서 정체 ★ 핵심 원인

- 증상:
  - Erase 램프가 −7~−8 V에서 거의 멈췄다.
  - Si와 질화막에 물리적으로 있을 수 없는 캐리어가 생겼다.
  - 메시, 홀 트랩, 정밀도, 반복 한도, 수렴 기준을 바꿔도 해결되지 않았다.
- 원인: 문제 1에서 고친 `models ... temperature=` 줄의 **위치**.
  - 원래 104는 `contact`(원래 95), `nitridecharge`(원래 97), `method`(원래 99) **뒤에** 있다.
  - 매뉴얼 2.5.2 순서는 `material → models → contact → method`다.
  - 결과로 보면 이동도는 77 K인데 캐리어 분포는 300 K로 계산되고 있었다(77 K 새 소자 기준):

| | 원래 위치 | 고친 위치 | 77 K에서 맞는 값 |
|---|---|---|---|
| SS | 93.2 mV/dec | 22.1 mV/dec | 약 22 mV/dec |
| VT (1e-7 A) | 0.217 V (300 K보다 낮음) | 0.701 V (300 K보다 높음) | 냉각하면 올라감 |

**현재 97~98 추가 (nitride `material` 다음, `contact` 앞)**
```
material material=nitride ... ni.min=1e-60        ← 현재 95
models srh temperature=@temp                      ← 현재 98 (추가)
contact name=cgate workf=$cwf                     ← 현재 100
```
- 이유: 위 원인.
- 확인:
  - 77 K 새 소자 SS 22.1 mV/dec. 300 K 결과는 바뀌지 않음(VT 차이 3 mV).
  - 새 소자 Erase −12 V 통과.
  - 실제 Erase −12 V 500 µs 끝까지 계산. 수렴 실패 0회.

### 문제 6. 펄스가 끝난 뒤 `solve init`이 77 K에서 실패

- 증상: 펄스 뒤 0 V로 돌아가는 `solve init`에서 발산했고, 그다음 계산도 모두 실패했다.
- 원인:
  - `solve init`은 바이어스를 0 V로 되돌리고 초기값을 새로 만든다. 77 K에서 질화막에 전하가 있으면 이 초기값이 크게 틀린다.
  - 16 V에서 정적 계산으로 내려오는 방법도 실패했다. 트랩이 고정된 채 고전계 주입이 계속돼 정상 상태가 없기 때문이다.

**원래 130 다음 → 현재 148~153 (Program), 원래 164 다음 → 현재 198~203 (Erase): 하강 구간을 트랜지언트로 추가**
```
method dt.max=2e-11 dt.min=1e-25
solve vcgate=$vcgate_split ramptime=9e-10 tstep=2e-12 tstop=9e-10 relative
method dt.max=5e-12 dt.min=1e-25
solve vcgate=0 ramptime=1e-10 tstep=1e-12 tstop=1e-10 relative
method dt.max=1e-3 dt.min=1e-25
solve tstop=1e-6 relative proj
```
- 트랜지언트로 내리는 이유: 실제 펄스도 하강 구간을 거쳐 0 V로 돌아가고, 그동안 트랩은 계속 전하를 주고받는다. 트랜지언트로 풀면 이것이 그대로 계산된다.
- 형태: 상승 구간을 거꾸로 한 모양이다(16 → 1.6 V 0.9 ns, 1.6 → 0 V 0.1 ns). 시간 간격 상한도 상승 구간과 같게 했다. 그 이유는 시험해서 통과한 값을 그대로 쓰기 위해서다.
- Erase 하강의 상한 이유: Erase는 두 구간 모두 5e-12다. Erase 램프를 5e-12로만 시험했기 때문이다.
- 0 V에서 1 µs 유지 후 저장(현재 160, 208)하는 이유: 하강 직후의 변화가 가라앉은 0 V 상태를 다음 단계의 시작점으로 쓰기 위해서다.
- `relative`의 이유: 지금 시각부터 센다(매뉴얼 SOLVE RELATIVE). 하강 구간은 펄스 유지 구간 바로 뒤에 이어지므로 시각이 연속이다.

**원래 139, 147, 151, 171 `solve init` → 삭제.** 대신 저장한 상태를 불러온다(현재 164~166, 175~177, 212~214):
```
models srh ^pf.nitride temperature=@temp
load infile=SONOS_PGM_…str master
solve prev
```
- `load`의 이유: 저장한 0 V 상태를 트랩 전하까지 정확히 그대로 불러온다(시험으로 확인: 불러온 상태의 전하와 VT가 저장 전과 같음).
- `solve prev`의 이유: 불러온 바이어스(0 V)에서 한 번 다시 풀어 다음 계산의 출발점으로 쓴다.
- Erase도 Program 상태를 불러와서 시작하는 이유(현재 175~177): Program 뒤 PGM 읽기를 하면 바이어스가 바뀌고 전하도 약간 바뀐다(0.05 %). 그래서 저장해 둔 Program 직후 상태에서 Erase를 시작한다.

**Erase 시간은 원래처럼 절대 시각 (현재 186~195)**
- 이유: `load` 뒤에는 시간이 0부터 다시 시작한다(모든 실행에서 확인).
  - `relative`를 `load` 직후에 쓰면, 같은 실행 안의 앞 트랜지언트 끝 시각을 기준으로 잡는 문제가 있었다. 읽기 덱에서 0.64 µs를 기다림.
  - 그래서 `load` 뒤 첫 트랜지언트는 절대 시각을 쓰고, `relative`는 바로 앞 트랜지언트에 이어지는 하강 구간에만 쓴다.

### 문제 7. 77 K 읽기에서 드레인 0.1 V를 한 번에 주면 발산

**원래 110~114 → 현재 114~122**

원래:
```
solve prev
solve vcgate=0 vstep=-0.1 name=cgate vfinal=-1
solve vdrain=0.1
log outf=SONOS_initial_…log
solve vcgate=-1 vstep=0.1 name=cgate vfinal=6
```
현재:
```
solve prev
solve vdrain=0.0001
solve vdrain=0.001
solve name=drain vstep=0.001 vfinal=0.01
solve name=drain vstep=0.005 vfinal=0.1
log outf=SONOS_initial_…log
solve vcgate=0 vstep=0.1 name=cgate vfinal=6
```
- 드레인을 작은 단계로 올린 이유: 77 K에서 0 → 0.1 V를 한 번에 풀면 발산했다. 작은 단계로 올리면 수렴했다.
- −1 V를 거치지 않고 0 V에서 읽는 이유:
  - 77 K에서 전하가 있는 상태를 음의 게이트 전압을 거쳐 읽으면, 채널이 8 V까지 안 켜지는 잘못된 해가 나왔다.
  - 새 소자에서는 문제가 없지만 모든 읽기를 같은 방식(0 V 시작)으로 맞췄다.
  - 새 소자 VT가 0.78 V라 0 V에서 시작해도 충분하다.

**현재 128~129 `solve prev` 추가 (Program 직전 `solve init` 다음)**
- 이유: `solve init`은 초기값만 만든다(전위만 계산). `solve prev`는 같은 바이어스에서 전위·전자·홀을 모두 푼다.
- Program 트랜지언트를 완전한 해에서 시작하기 위한 것으로, 77 K에서 시험해 통과한 순서와 같다.
- 이 줄 없이 77 K를 시험한 적은 없다.

### 문제 8. 77 K에서 전하가 있는 상태를 정적으로 읽으면 잘못된 결과

- 증상: 아래 중 하나가 나왔다.
  - 채널이 7 V까지 안 켜짐.
  - 58 mV 안에서 전류가 7자리 뜀. SS < 15.3 mV/dec로, 77 K 물리 한계 아래다.
  - gm이 새 소자의 10배. 같은 온도에서는 상태와 관계없이 같아야 한다.
- 원인: 정적 계산은 전압마다 새 해를 찾는다. 77 K에서 전하가 있으면 바이어스를 거치는 순서에 따라 잘못된 해로 넘어갔다. 순서를 여러 가지로 바꿔도 ERS는 모두 실패했다.

**원래 139~148 (PGM 읽기), 원래 171~180 (ERS 읽기) → 현재 162~171, 210~219: 트랜지언트 읽기로 바꿈**
```
models srh ^pf.nitride temperature=@temp
load infile=SONOS_PGM_…str master
solve prev
method dt.max=1e-9 dt.min=1e-25 cx.tol=1e-5
log outf=TREAD_PGM_…log master
solve vdrain=0.1 ramptime=1e-8 tstep=1e-12 tstop=2e-8
solve vcgate=6.0 ramptime=6.0e-07 tstep=1e-12 tstop=6.20e-07
log off
```
- 트랜지언트로 읽는 이유: 바로 전 시간 단계의 해에서 이어 풀기 때문에 잘못된 해로 넘어가지 않는다.
- 드레인 10 ns 램프의 이유: 한 번에 주면 발산하므로(문제 7) 시간에 따라 올린다.
- 게이트 10 V/µs, `dt.max=1e-9`의 이유:
  - 한 단계가 최대 0.01 V다. 77 K SS가 약 22 mV/dec라 한 단계에 전류가 약 0.45자리 바뀐다.
  - 게이트 충전 전류는 C·dV/dt = 2.4e-15 F × 1e7 V/s = 2.4e-8 A다.
- `cx.tol=1e-5`(기본값)를 적은 이유: 앞의 Erase 블록에서 1e-4로 바꿨기 때문에, 검증 때와 같은 기본값으로 되돌린다.
- 끝 전압의 이유: PGM 6 V, ERS 5 V. VT와 gm 최댓값을 지나도록 했다(77 K PGM VT 2.40 V·gm 최대 2.73 V, ERS 1.78 V·2.11 V).
- 분석은 Id = (I_drain − I_source)/2로 한다(`tscan/tread_vt.py`).
  - 이유: 게이트 충전 전류는 소스와 드레인에 같은 방향으로 반씩 흐르므로, 차이를 반으로 나누면 없어진다.
  - 1e-9 A 아래에는 약 3e-10 A의 바닥이 남는다. 그래서 VT는 gm 방식과 1e-8/1e-7 A 기준으로 뽑는다.
- 검증:
  - 77 K 새 소자에서 정적 읽기와 비교: VT_gm 0.7802 vs 0.7802 V, VT(1e-7 A) 0.7009 vs 0.7014 V, gm 같음.
  - 77 K PGM 상태에서 정적 읽기와 VT 차이 5.5 mV.
  - 읽는 동안 전하 변화 0.05 %.

## 2. 그 밖에 바뀐 것

| 원래 | 현재 | 이유 |
|---|---|---|
| (온도마다 `set temp`만 바꿔 같은 덱 사용) | 온도당 덱 하나(77fix, 300fix). 29번째 줄만 다름 | 두 온도의 계산 절차가 완전히 같아야 비교가 맞다 |
| 읽기 로그 `SONOS_PGM_….log`, `SONOS_ERS_….log` | `TREAD_PGM_….log`, `TREAD_ERS_….log` | 읽기 방식이 바뀌어(트랜지언트) 이름을 구분 |
| 파일 이름 끝 `_cwf_$cwf|` | `_cwf_$cwf|_temp_$temp|` (출력·불러오기 11곳) | 파일 이름만으로 온도를 구분 |
| 원래 147 `solve init` 뒤 `log off` | 삭제 | 문제 6과 같은 이유. Erase는 저장한 Program 상태에서 시작 |
| 7~8번 줄 | 설명 주석 2줄 추가 | 덱 설명 (계산에 영향 없음) |

## 3. 원인을 찾는 동안 넣었다가 지금은 뺀 것

| 항목 | 뺀 이유 |
|---|---|
| Erase 램프를 −6.6 V에서 둘로 나누고 그 지점과 램프 끝 상태 저장 | 정체 직전 상태를 분석하려던 것. 기울기가 같아 계산 결과는 같다 |
| `method`의 `clim.dd=4.5e13` | Si 기본값과 같은 값 |
| PGM/ERS 상태의 정적 읽기 | 77 K에서 결과가 틀리거나 실패(문제 8). 트랜지언트 읽기로 대체 |

## 4. 원래 그대로인 것

- 구조, 메시, 영역, 전극, 도핑.
- `material`의 `ni.min` 외 값.
- `contact workf`.
- `nitridecharge`의 `hole.depth` 외 값: 트랩 밀도, `elec.depth`, `sigmat.n`, `tau.n`/`tau.p`.
- `probe`.
- 펄스 조건: +16 V 100 µs, −12 V 500 µs. Erase 램프는 원래와 같은 1 ns.
- 새 소자 읽기 로그와 `output`/`save` 줄.
- 기본 모델 `srh`(여기에 `pf.nitride`만 트랜지언트에서 추가).

## 5. 아직 이 형태로 돌려보지 않은 부분

각 부분은 따로 돌려서 확인했지만, 하나로 합친 이 덱은 아직 돌리지 않았다. 새로 바뀐 점은 셋이다.

- Erase 램프를 한 구간으로 되돌림. 시간 간격 상한과 기울기는 시험한 것과 같다.
- `load` 뒤 읽기와 Erase에 절대 시각 사용. `load` 뒤 시간이 0부터 시작하는 것은 모든 실행에서 확인했다.
- 읽기의 `cx.tol=1e-5`. 검증한 읽기와 같은 값을 명시한 것이다.
