# 77 K SONOS/TANOS/TANS 읽기 VT 검증 현황 (2026-11-20)

## 1. 결론 요약

1. **실제 ATLAS 실행 결과가 아직 없다.** 덱 문법은 ATLAS·DeckBuild 설명서와 대조해 확인했다(§4-1). 받은 ZIP에는 `*_read.log`, `*_Vt.dat`, `*_zero.str`가 없다. 그래서 ATLAS 읽기 곡선에서 뽑은 VT, 실제 수렴 여부, 첫 오류 줄은 **미검증**이다. 아래 숫자는 모두 Python 계산값이거나, 그 값으로부터 예측한 값이다.
2. **ATLAS 읽기 덱만으로는 역전 여부를 따로 확인할 수 없다.** 덱은 Python이 계산한 ΔVT를 Si 계면의 고정전하 `qf`로 바꿔 넣는다. 고정 계면전하는 평탄대 전압만 −q·qf/C_stack만큼 옮긴다. 따라서 ATLAS에서 얻는 VT,PGM − VT,ERS는 Python 값을 몇 mV 이내로 다시 보여 줄 뿐이다. SONOS에서 ATLAS가 −0.049 V의 역전을 보여도 이는 Python 결과를 그대로 옮긴 것이다. ATLAS가 독립적으로 확인한 결과가 아니다.
3. **SONOS의 역전은 격자 수에 따라 생기거나 사라진다.** 질화막을 몇 개의 plane으로 나누느냐(`--planes`)만 바꿔도 결과가 달라진다. 역전(P−E < 0)은 기존 기본값인 4 plane에서만 나타난다. 2, 8, 16 plane에서는 나타나지 않는다. hopping을 켠 SONOS의 Program ΔVT도 0.47 → 0.10 → 0.03 V로 수렴하지 않는다. 그래서 현재 모델의 "Erase 중 hopping에 의한 역전"은 물리적 결론으로 쓸 수 없다. 이산화 방식이 만든 결과로 봐야 한다(§3).

## 2. VT 추출 정의와 Python 예측 (기본 덱, 4 plane)

- 정의: VD = 0.1 V 선형 Id–Vg에서 gm = dId/dVg가 최대인 점의 접선을 긋고, 그 접선의 Vg축 절편을 VT로 한다(DeckBuild `xintercept(maxslope(curve(v."cgate",i."drain")))`).
- 기존 `*_Vt.dat`은 **VD/2 보정 전** 값이다. 이번에 VD/2 보정값(`*_Vt_vd2.dat`, VT − 0.05 V)을 따로 추가했다. VD/2 보정은 두 상태에 똑같이 빠지므로 창 VT,PGM − VT,ERS에는 영향이 없다.

| 구조 | 구분 | Python ΔVT,PGM (V) | Python ΔVT,ERS (V) | 예측 VT,PGM − VT,ERS (V) | 역전 |
|---|---|---:|---:|---:|---|
| SONOS | 직후 | +0.4656 | +0.5151 | **−0.0495** | 예 (단, §3에서 격자 의존성 확인) |
| SONOS | 1 s 보존 후 | +0.4230 | +0.3908 | +0.0321 | 아니오 |
| TANOS | 직후 | +0.5759 | +0.0000 | +0.5759 | 아니오 |
| TANOS | 1 s 보존 후 | +0.4552 | +0.0000 | +0.4552 | 아니오 |
| TANS | 직후 | +0.0018 | −0.2725 | +0.2743 | 아니오 |
| TANS | 1 s 보존 후 | +0.0000 | +0.0000 | +0.0000 | 창 소멸 |

ATLAS 절대 VT는 (fresh VT) + ΔVT로 예측한다. fresh VT는 ATLAS를 실행해야 알 수 있다.

### 상태별 질화막 전하 분포 (plane1 = 채널 쪽)

- SONOS Program 직후: 전자 점유율 [0.094, 0.093, 0.134, 0.292]. Erase 직후: [0.567, 0, 0, 0]이고 정공은 0이다. Erase 동안 전자의 약 7.5 %만 빠져나간다. 나머지 전자는 hopping으로 채널 쪽 plane1에 모인다. 채널에 가까운 전하일수록 ΔVT에 주는 가중치가 크다. 그래서 Erase 후 ΔVT가 오히려 커진다.
- Erase 구간 끝의 경로별 전류(A/m²): Si의 정공 밴드 주입 ≈ 6×10⁻¹⁶, Si↔트랩 전자 방출 0.26, 게이트 전자 역주입 4.5×10⁻³. 77 K에서 3 nm SiO₂를 지나는 정공 주입이 거의 0이다. 즉 이 모델의 SONOS는 −12 V, 500 µs로 **사실상 지워지지 않는다**. 역전은 이렇게 창이 거의 닫힌 상태에서 나타나는 ±50 mV 크기의 2차 효과다.
- TANOS는 Erase 후 전자가 모두 빠져 중성(ΔVT ≈ 0)이 된다. 정공 주입은 없다.
- TANS는 Program 동안 PF 방출(882 A/m²)이 Si 전자 주입과 거의 같다. 그래서 Program ΔVT가 2 mV밖에 되지 않는다. TANS의 창은 Erase 때 Si에서 트랩으로 들어간 정공에서만 생긴다. 1 s 보존 후에는 모두 사라진다.

## 3. 격자(plane 수) 수렴 점검 — 새로 확인한 문제

`audit/grid_study.py` → `audit/grid_study.csv`. 다른 매개변수는 모두 기본값이다.

| 구조 | plane | 기본 P−E (V) | Erase 중 hopping OFF P−E (V) | hopping 전부 OFF P−E (V) | 기본 ΔVT,PGM (V) |
|---|---:|---:|---:|---:|---:|
| SONOS | 2 | +0.0054 | +0.0054 | +0.0054 | 0.523 |
| SONOS | **4** | **−0.0495** | +0.0119 | +0.0116 | 0.466 |
| SONOS | 8 | +0.0168 | +0.0020 | +0.0608 | 0.098 |
| SONOS | 16 | +0.0226 | −0.0002 | +0.0673 | 0.029 |
| TANOS | 4 / 8 / 16 | +0.576 / +0.680 / +0.691 | — | +0.575 / +0.554 / +0.544 | |
| TANS | 4 / 8 / 16 | +0.274 / +1.130 / +1.324 | +0.248 / +0.004 / +0.096 | | |

원인은 hopping 식에 있다. `flash_transport.py`의 hopping 속도는 `hop_hz·exp(−2·dx/a)`이다(a = 0.22 nm). 여기서 dx는 물리적인 트랩 간격이 아니라 **수치 plane 간격**(7 nm / n)이다. 4 → 8 plane으로 바꾸면 dx가 1.75 → 0.875 nm로 줄어든다. 그러면 hopping 속도가 exp(15.9 − 8.0) ≈ 2.8×10³배 커진다. 가장자리 plane과 전극 사이의 WKB 교환 거리도 dx/2에 따라 달라진다. 그래서 hopping을 끈 경우에도 결과가 완전히 수렴하지는 않는다(SONOS 0.42 → 0.43, TANS Erase −0.246 → −0.004 → −0.092 V).

리뷰 논문(Chiu 2014, 식 12)의 hopping 식은 J = q·a·n·ν·exp(qaE/kT − Ea/kT)이다. 여기서 a는 **평균 hopping 거리(트랩 간격)**라는 물리량이다. 모델이 격자와 무관해지려면 다음 두 가지가 필요하다. (1) a(또는 N_t^(−1/3))를 물리적 매개변수로 고정한다. (2) plane 사이 전달률을 연속체 극한(확산·드리프트 형태, ∝ (a/dx)²)으로 맞춘다. 이 부분은 모델 식을 바꾸는 일이라 이번 작업에서는 고치지 않았다. 대신 문제를 재현하는 도구(`--planes`)와 결과만 추가했다.

PF 장벽 저하 √(qE/(πε₀ε_r))에 광학 유전상수 ε_r = 4를 쓴 것은 리뷰 논문 §3.1의 권고와 맞는다. 다만 77 K에서는 kT = 6.6 meV이다. 그래서 1.2 eV 트랩의 PF 방출은 전계가 아주 높은 TANS에서만 의미가 있다.

## 4. 덱 수정 내역

| 파일 | 바뀐 줄 | 물리적·추출 의미 |
|---|---|---|
| `templates/SONOS.txt` 56–58, `TANOS.txt` 57–59, `TANS.txt` 54–56, 그리고 이 템플릿으로 다시 만든 `generated/*.in`, `audit/*/*.in` | `extract name="Vt_gm_vd2" xintercept(maxslope(curve(v."cgate",i."drain"))) - ave(v."drain")/2 datafile="<tag>_Vt_vd2.dat"` | 같은 최대 gm 접선 절편에서 VD/2(0.05 V)를 뺀 VT. DeckBuild 설명서 §5.5의 Vt 예제와 같은 형식이다. 창에는 영향이 없다. |
| 위와 같음 | `extract name="IdVg" curve(v."cgate",i."drain") outfile="<tag>_IdVg.dat"` | 읽기 Id–Vg 곡선을 텍스트로 내보낸다(`<CURVE_FUNC>(...) [outfile=]` 문법). `analyze_reads.py`가 DeckBuild와 별도로 VT를 다시 계산해 서로 비교한다. |
| 위와 같음 | `extract name="gm" deriv(v."cgate",i."drain") outfile="<tag>_gm.dat"` | gm = dId/dVg 곡선. 최대 gm 위치를 TonyPlot에서 확인하는 용도다. |
| `flash_transport.py` 31, 50, 53, 269, 316, 318 | `planes` 옵션 추가(기본 4) | 격자 수렴 점검용이다. 기본값에서는 기존 CSV·qf와 비트 단위로 같다(재생성 후 diff로 확인). |

ATLAS 물리 모델 줄(models, interface, material, solve)은 바꾸지 않았다. 아래 §4-1의 설명서 대조에서 문법 오류가 나오지 않았기 때문이다. 새로 생기는 출력 파일은 상태마다 `<tag>_Vt_vd2.dat`, `<tag>_IdVg.dat`, `<tag>_gm.dat` 세 개다.

### 4-1. ATLAS·DeckBuild 설명서 대조 결과 (저장소 silvaco-manuals의 atlas_users1.pdf 1822쪽, deckbuild_users1.pdf 256쪽)

**문법**: `templates/*.txt`와 `reference/*.in`에 쓰인 모든 문장과 파라미터를 Chapter 22 각 문장의 파라미터 표와 맞춰 봤다. 모두 정식 이름이거나 §2.5.1 규칙("같은 문장 안에서 다른 파라미터와 구별될 만큼의 글자만 쓰면 된다")에 맞는 **유일한 약어**다.

| 덱에서 쓴 이름 | 설명서상 이름 |
|---|---|
| `x.r`, `x.l` (DOPING) | X.RIGHT, X.LEFT |
| `char`, `conc`, `reg`, `gauss` (DOPING) | CHARACTERISTIC, CONCENTRATION, REGION, GAUSSIAN |
| `workf` (CONTACT) | WORKFUN |
| `temp` (MODELS) | TEMPERATURE |
| `num` (REGION) | NUMBER |
| `outf` (LOG·SAVE) | OUTFILE |
| `init` (SOLVE) | INITIAL |
| `integrate` (PROBE) | INTEGRATED |
| `vdrain`, `vcgate` | SOLVE의 `V<name>` |

| 항목 | 설명서 근거 | 판정 |
|---|---|---|
| `models region=6 fermidirac incomplete ioniz analytic bbt.kl` | MODELS 표·Table 2-2(Carrier Statistics Models): IONIZ는 "INCOMPLETE와 함께 써서 고농도 Si를 완전 이온화" | 맞음. 5×10²⁰ S/D가 77 K에서 동결되지 않도록 하는 설명서 권장 조합이다. |
| `interface qf=...` (x/y 범위) | INTERFACE: "QF = 반도체–절연체 계면의 고정 산화막 전하(cm⁻²). 범위 상자 안의 반도체/절연체 계면에 적용" | 맞음. TANS의 Si/질화막 계면도 읽기 덱에서는 질화막이 절연체라 적용된다. |
| `probe ... r.bbt`, `output ... u.bbt`, `sonos.rates`, `log ... sonos.curr` | PROBE·OUTPUT·LOG 표에 있음 | 맞음 |
| 재료 `air`, `conductor`, `Al2O3`, `oxide`, `nitride` | Table B-1 Atlas Materials | 모두 있음 |
| reference 덱 `interface n.i dynasonos`, `material ... semiconductor`, `nitridecharge ...`, `pf.nitride` | §3 DYNASONOS: N.I로 활성화. INTERFACE는 구조 정의 그룹의 끝에 둔다. 게이트 스택 절연막은 모두 SEMICONDUCTOR로 바꾸고 질량·이동도·상태밀도를 지정한다. | 덱이 이 요구를 모두 따른다. |
| DeckBuild `extract init infile=`, `xintercept(maxslope(curve()))`, `ave()`, `deriv()`, `outfile=` | DeckBuild 설명서 §5 Extract 문법·예제 | 맞음. VD/2 줄은 처음에 `abs(ave(...))/2.0` 형태로 넣었으나, 설명서 예제와 같은 `- ave(v."drain")/2`로 바꿨다. |

**77 K에서 주의할 점 (설명서 근거)**

1. §3.3.3 Low Temperature Simulations: Fermi–Dirac과 불순물 동결을 함께 쓰면 "50 K까지는 이차 수렴을 잃지 않는다"고 되어 있다. 따라서 77 K는 기본 정밀도로 먼저 실행해 본다. 소수 캐리어가 언더플로하면 quasi-Fermi 준위에 "spurious glitch"가 생길 수 있다고도 적혀 있다.
2. §21.11 Numerical Precision의 식 21-68은 P ≥ E_G/(ln2·kT)이다. Si, 77 K에서는 약 253 bit가 나온다. 기본 double(유효 53 bit)보다 크지만, 설명서는 이 값을 "느슨한 상한"이라고 한다. §3.3.3은 저온 계산에 **160-bit**가 매우 효과적이라고 한다. **수렴이 안 되거나 Id가 바닥에서 튀면** 각 블록의 `go atlas`를 `go atlas simflags="-160"`으로 바꾼다. 그래도 안 되면 `"-256"`을 쓴다. 정밀도를 올리면 계산 시간과 메모리가 늘어난다(Table 21-6).
3. 선택 사항: MATERIAL의 `NI.MIN`으로 n_i 언더플로를 막을 수 있다(열 생성률은 틀어질 수 있음). 50 K 미만에서는 METHOD `ITLIMIT`를 늘린다. METHOD `MIN.TEMP`(기본 120 K)는 격자온도 방정식을 풀 때만 해당하므로 이 덱과는 관계없다.
4. PF 식의 차이: ATLAS PF.NITRIDE(식 3-590)의 ε는 "질화막의 유전율"이다. 따로 지정하지 않으면 정적 유전율 7.5를 쓴다. Python은 리뷰 논문의 권고대로 광학 유전율 4를 쓴다. 같은 전계에서 ATLAS의 장벽 저하는 √(4/7.5) ≈ 0.73배로 더 작다. reference 결과와 Python을 비교할 때 이 차이를 감안해야 한다.
5. TANS reference: 설명서는 DYNASONOS의 터널 경로를 "질화막–터널 절연막 계면에서 채널까지"로 정의한다. 터널 산화막이 없는 TANS는 이 정의 밖에 있으므로 Si↔질화막 직접 교환이 의도대로 계산된다는 보장이 없다.
6. 참고: SOLVE의 `NIT.N`/`NIT.P`(NIT.XMIN–YMAX 범위, 여러 번 누적 가능)를 쓰면 질화막 안에 깊이별 포획 전하를 직접 넣을 수 있다. 다만 DYNASONOS 구조가 필요하다. 읽기 VT는 선형 정전기라 등가 qf와 결과가 같다. 질화막 내부의 전계나 밴드를 봐야 할 때만 이 방법이 의미가 있다.

## 5. ATLAS 실행 후 절차

1. DeckBuild 작업 디렉터리를 `generated`로 두고 `RUN_SONOS.in`, `RUN_TANOS.in`, `RUN_TANS.in`을 실행한다.
2. 오류가 나면 실행 로그(DeckBuild 하단 창 전체)를 저장해 전달한다. **첫 번째 `Error`가 나온 줄**을 기준으로 고친다.
3. 일반 터미널에서 실행한다:
   ```
   python analyze_reads.py --dir generated
   ```
   `generated/VT_report.md`와 `VT_report_states.csv`, `VT_report_windows.csv`가 생성된다. 이 표에는 상태별 VT(보정 전·VD/2 보정), DeckBuild 자체 추출값, 부호를 유지한 VT,PGM − VT,ERS, 역전 여부, Python 예측과의 차이(mV)가 들어 있다. ATLAS−Python 차이가 수 mV보다 크면 qf 전달, 수렴, 추출 구간 중 어디에 문제가 있는지 확인한다.
4. `python analyze_reads.py --selftest`로 추출 코드 자체를 점검할 수 있다. 이 점검은 VT를 미리 정해 둔 합성 곡선에서 창을 0.1 mV 이내로 다시 찾는지 확인한다. ATLAS를 검증하는 것은 아니다.

## 6. 검증 상태

| 항목 | 상태 |
|---|---|
| Python 결과 재현 (NumPy·SciPy, 기본 덱 + 4개 audit 조건) | 검증됨 (기존 CSV와 비트 단위로 일치) |
| `check_results.py` | PASS |
| VT 추출 코드 (합성 곡선) | 검증됨 (selftest PASS) |
| 격자 수렴 | **실패**: SONOS 역전과 TANS Erase 크기가 plane 수에 따라 달라짐 |
| ATLAS·DeckBuild 문법 (설명서 대조) | 검증됨 (§4-1). VD/2 extract 줄 1곳 수정 |
| ATLAS 수렴, .log/.str 생성 | 미검증 (ATLAS 실행 결과 없음) |
| ATLAS 읽기 곡선의 VT, 실제 역전 여부 | 미검증 (예측값만 있음) |
| TANOS·TANS에 같은 절차 적용 | 도구는 준비됨. ATLAS 결과가 오면 위 명령 하나로 처리됨 |
