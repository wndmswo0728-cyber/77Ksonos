# SONOS N5 덱 수정 요청 (77 K / 300 K, SEED·PE)

## 대상 파일
| 파일 | 내용 |
|---|---|
| `SONOS_77K_SEED_N5.in`, `SONOS_300K_SEED_N5.in` | `nit.n`으로 전하를 넣고 3×10⁸ s 보존 |
| `SONOS_77K_PE_N5.in`, `SONOS_300K_PE_N5.in` | Program(+16 V, 100 µs), Erase(−12 V, 500 µs) |

77 K 덱과 300 K 덱은 지금 `set temp` 한 줄만 다릅니다. **수정한 뒤에도 이 관계를 유지해 주세요.** 아래 수정은 77 K와 300 K 덱에 똑같이 넣습니다. 줄 번호는 지금 파일 기준입니다.

## 왜 고치나 (요약)
- 77 K SEED 초기·PGM 로그를 분석한 결과, Vt 이동량은 맞았습니다. ΔVt = 2.91 V이고, probe 전하 −1.013e-14 C/µm로 계산한 값은 2.88 V입니다.
- 하지만 **SS가 94 mV/dec**로 나왔습니다. 77 K 이론값은 약 21 mV/dec입니다(참고로, 같은 구조를 메시를 촘촘하게 하고 `fermidirac`을 켜서 따로 돌려 본 시도에서는 약 29 mV/dec가 나왔습니다). Vg = 0 V에서 Id = 5e-10 A/µm도 77 K에서는 나올 수 없는 값입니다. 그래서 **절대 Vt를 믿을 수 없습니다.**
- 온도 설정은 제대로 적용됐습니다. gm으로 계산한 이동도가 약 7700 cm²/Vs인데, 이는 1000 × (77/300)^−1.5과 맞습니다. 따라서 원인은 **메시와 수치 정밀도**로 봅니다.
- 이 밖에 두 가지 덱 구조 문제가 있습니다.
  - 보존 뒤 읽기 범위가 PGM Vt(3.1~3.3 V)보다 좁습니다.
  - 읽기마다 이동도 모델이 다릅니다.

---

## A. 반드시 고칠 것 (실행 전)

### A1. [SEED] 모든 Id–Vg 읽기 범위를 같게
지금 보존 뒤 읽기(178번째 줄)는 `vfinal=3`에서 끝납니다. 그런데 77 K PGM의 Vt가 이미 3.13~3.34 V라서, 보존 중 전하가 거의 빠지지 않으면 Vt를 추출할 수 없습니다.

`go atlas` 아래 `set` 블록에 다음을 추가합니다.
```
set Vrd_lo=-2
set Vrd_hi=8
set Vrd_step=0.02
```
그리고 세 읽기(초기 116, PGM 137, 보존 뒤 178)를 모두 같은 형태로 바꿉니다.
```
solve vcgate=0 vstep=-0.1 name=cgate vfinal=$Vrd_lo
solve vdrain=0 vstep=0.01 name=drain vfinal=0.1
log outf=<이름>.log master
solve vcgate=$Vrd_lo vstep=$Vrd_step name=cgate vfinal=$Vrd_hi
log off
```
- 0.1 V 간격은 77 K의 가파른 곡선에 너무 굵어서 0.02 V로 줄입니다.
- 지금 PGM 읽기(133번째 줄)는 Vg를 0→2 V로 **올린** 다음 2→6 V를 기록합니다. 위 형태로 바꾸면 Vg를 먼저 내렸다가 처음부터 다시 올립니다.

### A2. [SEED] 세 번의 읽기를 같은 MODELS로
- 지금은 초기·PGM 읽기가 `models srh`이고, 보존 뒤 읽기(168번째 줄)가 `models srh mos`입니다.
- `mos`가 들어가면 이동도 모델이 바뀌고, 최대 gm 접선법 Vt가 그만큼 움직입니다. 그러면 **ΔVt(보존)에 모델 차이가 섞입니다.**
- 수정 방법: 읽기 직전의 MODELS를 모두 `models srh mos temperature=@temp print`로 맞춥니다. 105번째 줄과 168번째 줄이 해당하고, PGM 읽기에는 105번째 줄 설정이 그대로 이어집니다.
- 보존 과도 계산(145번째 줄) `models mos srh pf.nitride temperature=@temp print`는 그대로 둡니다.
- 주의: 105번째 줄에 `mos`를 넣으면 초기 Vt 기준값도 바뀝니다. 바뀐 값을 새 기준으로 씁니다.

### A3. [PE] 같은 읽기 범위·간격·MODELS
- PE 덱의 세 읽기(115, 146, 178번째 줄)도 A1과 같은 형태로 바꿉니다. 지금은 −1~6, 1~8, −2~7 V로 제각각입니다.
- 범위는 `Vrd_lo=-2`, `Vrd_hi=8`이고, 프로그램 Vt가 8 V를 넘으면 `Vrd_hi`를 올립니다.
- 읽기 MODELS는 A2와 같이 `models srh mos temperature=@temp print`로 맞춥니다.

### A4. [PE] `solve init`이 프로그램 전하를 지우는지 확인 후 수정
- PGM 읽기 앞(140), 소거 앞(148·152), ERS 읽기 앞(172)에 모두 그냥 `solve init`이 있습니다.
- `solve init`이 질화막에 갇힌 전하를 초기화한다면 다음 일이 생깁니다.
  - PGM 읽기 곡선이 초기 곡선과 같게 나옵니다.
  - 소거가 프로그램된 상태가 아니라 빈 상태에서 시작합니다.
- 이 때문에 SEED 덱에서는 이미 `load`로 바꿨습니다. PE 덱도 같은 방식으로 바꿉니다.

```
#### Program 끝 ####
log off
output qfn qfp con.band val.band Band.param t.quantum e.field sonos.rates
save outf=<..._PGM.str>

# PGM 읽기: 전하가 찬 상태에서 바이어스만 0으로 돌린 뒤 읽기
solve previous vcgate=0
(A1/A3 읽기 블록)

# Erase 시작 전에 프로그램 직후 상태로 되돌리기
load infile=<..._PGM.str> master
solve previous vcgate=0 vdrain=0
log outf=<..._TRNS_ERS.log>
solve vcgate=$ecgate ramptime=1e-9 tstep=1e-12 tfinal=1e-9 proj
...

#### Erase 끝 ####
save outf=<..._ERS.str>
solve previous vcgate=0
(A1/A3 읽기 블록)
```
- 148번째 줄의 `solve init`은 PGM 읽기 로그가 열린 채로 실행됩니다. `log off`보다 앞에 있으니 지웁니다.
- 156번째 줄(소거 첫 과도 계산)에 `proj`를 붙여 다른 줄과 맞춥니다.
- 읽기를 마친 뒤 Program 쪽 바이어스(vcgate 0 → +16 V)를 줄 때는 `ramptime`으로 올리므로 그대로 둡니다.

### A5. [PE] 77 K 트랩 전자 방출 모델
- 지금 PE 덱은 `models srh`뿐이고, `nitridecharge tau.n=1e-4 tau.p=1e-4`입니다. 그래서 질화막 트랩 방출이 **온도와 상관없이 100 µs 수명**으로 일어납니다.
- TPGM(100 µs)과 TERS(500 µs)가 이 수명과 같은 크기라서, 77 K와 300 K의 P/E 창에 온도 효과가 제대로 나오지 않습니다.
- 수정 방법: Program·Erase 과도 계산 직전에 다음을 넣습니다. 77 K와 300 K **둘 다** 넣어야 두 덱이 온도만 다른 상태로 남습니다.
  ```
  models srh mos pf.nitride temperature=@temp print
  ```
- 확인할 것: `pf.nitride`를 켜면 `tau.n`, `tau.p`가 계속 쓰이는지 아니면 PF 방출로 대체되는지 설명서(DYNASONOS 절)와 `print` 출력에서 확인하고 보고해 주세요.
- 300 K 원본(PF 없음) 결과는 따로 남겨 두고, 새 결과와 섞지 않습니다.

---

## B. 77 K 결과를 믿으려면 고칠 것 (수치)

### B1. 정밀도
네 덱 모두 첫 줄 `go atlas`를 다음으로 바꿉니다. 근거는 설명서 §21.11과 §3.3.3입니다. 300 K 덱도 같이 바꿔야 두 덱이 온도만 다릅니다.
```
go atlas simflags="-160"
```
실행 시간과 메모리가 늘어납니다. 수렴이 안 되면 `"-256"`을 씁니다.

### B2. x 메시 (S/D 접합 가장자리)
- 지금 게이트 가장자리의 x 간격이 50 nm입니다. 그런데 접합 lateral char는 5 nm이고 77 K의 kT/q는 6.6 mV입니다. 소스 장벽이 요소 하나 안에 다 들어갑니다.
- 네 덱 모두 x.mesh 블록을 다음으로 바꿉니다(위치 순서 유지).
```
x.mesh loc=0.0          spac=$Lgate*0.25
x.mesh loc=@Ls          spac=0.005
x.mesh loc=@Lgate_left  spac=0.005
x.mesh loc=@Lgate_mid   spac=0.05
x.mesh loc=@Lgate_right spac=0.005
x.mesh loc=@Ld          spac=0.005
x.mesh loc=@Ltotal      spac=$Lgate*0.25
```

### B3. [SEED] 구조를 PE 덱과 같게
- SEED는 y 원점이 다르고(Si 표면이 y = −0.002 µm), Si 표면 y 간격이 0.5 nm로 거칩니다. 반면 PE는 Si 표면이 y = 0이고 간격이 0.03 nm입니다. 이대로면 **SEED와 PE의 절대 Vt를 비교할 수 없습니다.**
- 수정 방법: SEED의 y.mesh, region, electrode 블록(49~79번째 줄)을 PE 덱의 49~80번째 줄로 바꿉니다. 그리고 질화막 좌표를 다음과 같이 맞춥니다.
  - probe(102번째 줄): `y.min=-$Tnit-$Tbox y.max=-$Tbox`
  - `solve nit...`(124·126번째 줄): `nit.ymin=-$Tnit-$Tbox nit.ymax=-$Tbox`

---

## C. VT 자동 추출 (네 덱 공통)
각 읽기의 `log off` 바로 뒤에 다음을 넣습니다. `<상태>`는 init / PGM / ERS / RET 중 하나로 바꿉니다.
```
extract init infile="<읽기 로그 이름>.log"
extract name="Vt_gm_<상태>" xintercept(maxslope(curve(v."cgate",i."drain"))) - ave(v."drain")/2 datafile="<덱이름>_Vt.dat"
extract name="Vt_cc_<상태>" x.val from curve(v."cgate",i."drain") where y.val=1e-7 datafile="<덱이름>_Vt.dat"
extract name="IdVg_<상태>" curve(v."cgate",i."drain") outfile="<덱이름>_<상태>_IdVg.dat"
```
gm이 거의 일정하면 최대 gm 접선법이 불안정합니다. 그래서 정전류법(1e-7 A/µm, W = 1 µm, L = 1 µm)도 함께 뽑습니다.

---

## D. 실행 후 확인 (결과와 함께 보내주세요)
| # | 확인 | 기준 |
|---|---|---|
| 1 | SEED `ret_entry.log`의 netcharge | `seed_charge.log`의 마지막 값과 같음 (약 −1.0e-14 C/µm). 0이면 `load`로 전하가 안 넘어온 것 |
| 2 | PE `TRNS_PGM.log`의 마지막 netcharge와 `PGM.log`의 netcharge | 같아야 함 |
| 3 | PE `TRNS_ERS.log`의 첫 netcharge | 프로그램 직후 값에서 시작해야 함 |
| 4 | 77 K 초기 SS (1e-11~1e-7 A 구간) | 약 20~35 mV/dec. 90 mV/dec 근처면 B1·B2가 반영 안 된 것 |
| 5 | 모든 읽기에서 Vt가 Vrd_lo~Vrd_hi 범위 안 | 범위 밖이면 `Vrd_hi`를 올리고 다시 실행 |
| 6 | 77 K와 300 K 덱의 차이 | `diff`로 확인해서 `set temp`와 출력 이름만 달라야 함 |
| 7 | 수렴 경고 | runtime 출력(.out)에서 확인 |

**보내줄 파일:** 수정한 덱 4개, 모든 `.log`, `*_Vt.dat`, `*_IdVg.dat`, runtime 출력(.out). .str은 `PGM`, `ret_start`, `RETEN`, `ERS`만 보내면 됩니다.

## 권장 진행 순서
1. 77 K SEED에 B1·B2만 반영해서 초기 읽기까지만 실행합니다. SS가 30 mV/dec 안팎으로 내려오는지 확인합니다. 정밀도와 메시 중 어느 쪽이 원인인지 보려면 B1만 넣은 경우와 B2만 넣은 경우를 따로 돌려 봅니다.
2. A1~A5, B3, C를 모두 반영해서 네 덱을 실행합니다.
3. D의 확인표를 채워서 결과와 함께 보내주세요.
