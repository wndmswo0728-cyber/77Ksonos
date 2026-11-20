# 77 K SONOS/TANOS/TANS 읽기 VT 검증 현황 (2026-11-20)

## 1. 결론 요약

1. **실제 ATLAS 실행 결과가 아직 없다.** 받은 ZIP에는 `*_read.log`, `*_Vt.dat`, `*_zero.str`가 없다. 그래서 ATLAS 읽기 곡선에서 뽑은 VT, 실제 수렴 여부, 첫 오류 줄은 **미검증**이다. 아래 숫자는 모두 Python 계산값이거나, 그 값으로부터 예측한 값이다.
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
| `templates/SONOS.txt` 56–57, `TANOS.txt` 57–58, `TANS.txt` 54–55, 그리고 이 템플릿으로 다시 만든 `generated/*.in`, `audit/*/*.in` | `extract name="Vt_gm_vd2" (xintercept(maxslope(curve(v."cgate",i."drain"))) - abs(ave(v."drain"))/2.0) datafile="<tag>_Vt_vd2.dat"` | 같은 최대 gm 접선 절편에서 VD/2(0.05 V)를 뺀 VT. Silvaco 예제의 관례적인 보정이다. 창에는 영향이 없다. |
| 위와 같음 | `extract name="IdVg" curve(v."cgate",i."drain") outfile="<tag>_IdVg.dat"` | 읽기 Id–Vg 곡선을 텍스트로 내보낸다. `analyze_reads.py`가 DeckBuild와 별도로 VT를 다시 계산해 서로 비교할 수 있다. |
| `flash_transport.py` 31, 50, 53, 269, 316, 318 | `planes` 옵션 추가(기본 4) | 격자 수렴 점검용이다. 기본값에서는 기존 CSV·qf와 비트 단위로 같다(재생성 후 diff로 확인). |

ATLAS 물리 모델 줄(models, interface, material, solve)은 바꾸지 않았다. 실제 오류 로그가 없는 상태에서 고치면 추측에 의한 수정이 되기 때문이다. 새로 생기는 출력 파일은 상태마다 `<tag>_Vt_vd2.dat`와 `<tag>_IdVg.dat` 두 개다.

### ATLAS 실행 시 먼저 볼 위험 지점 (설명서 대조 필요, 미검증)

1. **77 K 수치 정밀도**: 77 K에서 Si의 n_i는 약 10⁻²⁰ cm⁻³ 수준이다. 그래서 수렴이 잘 되지 않거나 "negative concentration"류 오류가 날 수 있다. Silvaco는 저온·광대역갭 계산에 확장 정밀도(`go atlas simflags="-80"` 또는 `"-128"`)를 쓰라고 안내한다. 실패하면 이것을 먼저 시도한다. 정확한 옵션 이름은 ATLAS 설명서의 "extended precision" 항목과 대조해야 한다.
2. `probe ... r.bbt`, `models ... incomplete ioniz` 키워드가 5.36.0.R에 있는지는 설명서 PROBE·MODELS 표와 대조해야 한다. 첫 오류가 이 줄에서 나면 해당 키워드만 빼고 다시 실행한다.
3. 이동도는 `analytic`만 지정되어 있고 표면 산란 모델(CVT 등)이 없다. 그래서 gm 최대점의 위치가 실제 소자와 다를 수 있다. 하지만 PGM/ERS 창은 같은 모델을 쓰는 두 곡선의 차이라서 영향이 작다.

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
| ATLAS 문법, 수렴, .log/.str 생성 | 미검증 (ATLAS 실행 결과 없음) |
| ATLAS 읽기 곡선의 VT, 실제 역전 여부 | 미검증 (예측값만 있음) |
| TANOS·TANS에 같은 절차 적용 | 도구는 준비됨. ATLAS 결과가 오면 위 명령 하나로 처리됨 |
