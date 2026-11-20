# 77 K 플래시 메모리 덱과 점검 결과

## 바로 실행하기

ZIP을 풀고 DeckBuild의 작업 디렉터리를 generated로 맞춘다. RUN_SONOS.in, RUN_TANOS.in, RUN_TANS.in을 각각 실행한다. 각 파일은 다섯 상태를 독립적인 ATLAS 세션에서 읽는다. 상태별 .in 파일 하나만 실행해도 된다. 상대경로 입력이나 별도의 .str 입력이 필요하지 않다. 결과는 실행 작업 디렉터리에 기록된다. 서로 다른 실험 폴더의 덱을 돌릴 때 작업 디렉터리도 바꾼다. 동일 이름으로 다시 돌리는 경우 기존 결과는 백업한다.

| 출력 예 | 읽는 방법 |
|---|---|
| SONOS_77K_programmed_read.log | TonyPlot에서 x=cgate 전압, y=drain 전류. erased 로그를 겹친다. Vd=0.1 V. |
| SONOS_77K_programmed_Vt.dat | DeckBuild가 선형 Id–Vg의 최대 기울기 접선과 Vg축의 교점을 추출한다. 소자의 절대 Vt이며 Vd/2 차감 전 값이다. |
| SONOS_77K_programmed_zero.str | 게이트·드레인·소스·기판 0 V. x=1.5 µm 수직 단면으로 전위·밴드를 본다. 저장층 전하가 계면 qf로 축약된 구조다. |
| SONOS_history.csv | Python에서 이미 계산한 깊이별 트랩 전하·전류율·ΔVt·표면전위 및 누적되지 않은 구간별 시간. plane1은 채널 쪽, plane4는 게이트 쪽. |
| audit/comparison.csv | 세 구조의 다섯 조건을 직접 계산한 결과. program_minus_erase_V는 부호를 유지한 이동량 차이다. |

상태명 fresh는 주입 전, programmed와 erased는 각각 펄스를 0 V로 내린 직후, program_retained와 erase_retained는 각 상태에서 독립적으로 1초 보존한 후이다. 그림에 쓸 메모리 윈도우는 같은 구조·온도·추출법의 Vt(PGM)−Vt(ERS)로 계산한다. Origin에서 관례에 따라 Vd/2=0.05 V를 빼더라도 두 상태에 동일하게 적용하면 윈도우는 같다.

## 어디까지 검증했나

Python/SciPy로 같은 전자 및 정공 SiO₂ 유효질량(0.3/1.0)에서 세 구조 × 다섯 조건을 실행했다. audit의 .log는 실제 Python 실행 기록이다. check_results.py로 펄스 바이어스·시간, 8개 점유율 범위, 전하보존 잔차, 계면전하→덱 전달, 출력 명령, p–n BTBT 대조군의 조건 일치를 검사했다. Python의 PGM/ERS 기준 ΔVt는 이전 ZIP과 일치했다. ATLAS 5.36.0.R 실행 환경이 없어 이 패키지에 실제 TonyPlot용 .str 및 ATLAS 읽기 .log는 없다. 각 덱에 두 출력을 만드는 명령이 있다. 모델 활성화, 수치 수렴, 로그 곡선, 추출 Vt는 현지 실행 결과로 확인해야 한다.

SONOS의 Program 이동량은 +0.465639 V다. 같은 Program 종료 상태에서 Erase 구간의 hopping만 끄면 Erase 후 +0.453718 V, 켜면 +0.515126 V다. 이 코드에서 Erase 중 hopping이 두 상태의 순서를 바꿀 수 있다. PF만 끈 SONOS는 표시한 정밀도에서 차이가 없지만 TANS의 Erase 이동량은 −0.272484 V에서 −0.329400 V로 바뀐다. FN형 밴드 주입을 끄면 SONOS와 TANOS의 Program 이동량이 거의 0이 된다. 이 옵션은 TANS 밴드 경로의 열적 주입도 함께 끄며, 전극↔국소 트랩 WKB 교환은 유지한다.

Hopping, PF, FN형 주입은 Python 1D P/E·보존 해석에 포함된다. Si p–n BTBT는 ATLAS의 2D 읽기·바이어스 진단에서만 계산되어 Python의 트랩 점유율을 갱신하지 않는다. 따라서 이 모델로 p–n 터널링에 의해 생성된 정공이 실제로 질화막에 얼마나 주입됐는지 정량화할 수 없다. PF 계수와 트랩 파라미터, TANS 직접 접촉 장벽/주입률, Si BTBT 계수는 77 K 실측 보정 전이다. 등가 qf 모델은 위치 가중 문턱전압 이동을 보존하지만 질화막 내부 전계·밴드 굽힘을 재현하지 못할 수 있다.

## p–n 터널링 확인

각 구조에서 BIAS_소자명.in을 실행하면 Program 유지 끝의 qf에서 Vg=+16 V, Erase 유지 끝의 qf에서 Vg=−12 V까지 각각 램프한 .str 및 _bias.log가 생긴다. Vd=Vs=Vb=0 V다. 결과는 P/E 말단 바이어스의 고정전하 DC 진단이다. .str에서 Si 영역의 band-to-band tunneling rate(U.BBT)와 전계를 같이 확인한다. _bias.log의 bbt_drain은 x=2.005, y=0.001 µm에서만 읽은 값이라 가장 큰 생성률을 놓칠 수 있다. _noBTBT 덱은 동일 qf와 동일 바이어스에서 BBT.KL을 뺀 대조군이다. 먼저 두 실행의 런타임 모델 표를 확인하고, 단자전류와 전계 분포도 비교한다. 생성률이 작으면 p–n 경로가 활성화되어도 읽기 Vt는 거의 같을 수 있다. 전압 램프의 가로축은 시간 대신 전압이다.

## ATLAS 자체 과도해석과 비교

reference의 세 *_reference_PE.in은 DYNASONOS, PF.NITRIDE, Si BBT.KL로 +16 V 100 µs → 0 V → −12 V 500 µs → 0 V를 푸는 별도의 시도다. 전자·정공 트랩 점유와 접합 생성은 2D 해에 들어가고 Python의 hopping은 들어가지 않는다. 이 경로가 성공하면 각 구조의 P/E 시간 로그와 실제 ATLAS 트랩 분포가 담긴 _pgm_zero.str와 _ers_zero.str를 볼 수 있다. TANS는 터널 산화막이 없어 DYNASONOS의 통상적인 하부 절연막 경계가 없고, Si/질화막을 직접 접촉시킨 탐색용 덱이다. 그 경계의 수송 모델, 터널 경로 인식, 고전계 수치 수렴은 검증 전이다. ATLAS 기준 덱에서도 PF 매개변수와 Python의 PF 손실 근사는 서로 다르다. reference는 주 결과와 별도 폴더에서 실행한다.

## 각 줄과 이론

DECK_LINES_KO.md에서 구조별 읽기·펄스 바이어스·ATLAS 기준 덱의 명령을 줄 번호별로 볼 수 있다. RUN 덱은 상태별 시작 줄 표를 사용한다. 아래는 flash_transport.py의 식과 단위에 대한 설명이다.

| 줄 | 의미 |
|---|---|
| 1–34 | 계산 단위는 SI, 에너지는 eV. 옵션에 77 K, 1초 retention, 수송 on/off, 전자·정공 각 10¹⁹ cm⁻³ 트랩 밀도, 국소화 길이 0.22 nm, hopping 10¹²/s, 열방출 10¹³/s, 유출률 2%, 포획률 5%, 광학 유전율 4, 시도율·질량·트랩 깊이를 둔다. |
| 36–50 | 구조별 함수에서 공통 simulate를 호출하고 온도 및 보존 시간을 검사한다. |
| 51–65 | 질화막 7 nm를 4개 층으로 나눈다. 각 층의 단위면적 트랩 수와 막의 역정전용량을 구한다. TANS는 하부 SiO₂ 두께가 0이다. |
| 66–94 | 온도 의존 Si 밴드갭·상태밀도, Fermi–Dirac 적분, 붕소 45 meV 억셉터 이온화, 전하중성으로 벌크 Fermi 준위를 정한다. Poisson 식을 적분해 표면전위 표를 만든다. |
| 95–104 | 가우스 법칙과 스택 전압 조건으로 각 구간의 전속·전위·표면전위를 계산한다. 1D 채널 중심 준평형 근사다. |
| 106–123 | 전계가 장벽을 얇게 하는 방향에 FN 공급식과 유한 두께 WKB 투과 지수를 사용한다. 장벽 높이와 유효질량은 구조와 캐리어 종류에 따라 선택한다. |
| 125–132 | 각 층의 국소전계, 빈 트랩 비율, 트랩 준위 차이를 만든다. |
| 133–140 | 거리 감쇠 exp(−2Δx/a)와 에너지 상승 확률 exp(−ΔE/kT)를 곱한다. 이웃 층의 빈자리까지 고려한 순 hopping을 양쪽 층에 반대 부호로 더하므로 총전하는 보존된다. |
| 141–145 | PF 장벽 저하는 √(q·abs(E)/(π ε₀κ)) eV이다. 장벽에서 저하분을 빼 열방출과 순유출을 계산한다. PF OFF에서는 장벽 저하분만 0이다. |
| 146–177 | 전극과 트랩 사이 각 막의 WKB 작용을 적분한다. 전극 점유와 트랩 점유의 차가 포획·탈출 방향을 정한다. |
| 178–207 | Si·게이트 양쪽, 전자·정공 각각의 밴드 주입을 구한다. Si 공급 상한과 TANS 직접 접촉의 열적·전계 보조 밴드 주입을 적용한다. |
| 208–223 | 유입 전하를 깊이별로 분배하고 빈 트랩 포획과 반대 전하 중화를 계산한다. 누적 저장전하 변화율과 외부 경로 합을 비교한다. |
| 225–231 | 각 위치의 시트 전하를 게이트까지 역정전용량으로 가중해 ΔVt를 구하고, 같은 ΔVt를 갖는 계면전하 qf(cm⁻²)로 환산한다. |
| 233–259 | BDF 시간 적분으로 Program/Erase 상승·유지·하강 및 보존을 계산한다. --no-erase-hopping은 같은 Program 상태에서 Erase 구간의 hopping만 끈다. |
| 262–280 | 같은 상태에 대해 CSV, 상태별 ATLAS 입력, 다섯 상태를 순서대로 읽는 RUN 덱을 생성한다. |
| 282–302 | 각 유지구간의 마지막 행에서 qf를 꺼내 BIAS 덱을 만들고, 같은 전하·구조에서 Si BBT만 뺀 RUN/BIAS 대조군을 만든다. |
| 304–318 | 명령행 옵션을 처리하고 세 구조를 일괄 생성한다. |

## 재현

기본 덱 실행에 Python은 필요하지 않다. 재계산은 Python 3.9 이상과 NumPy·SciPy 환경에서 python flash_transport.py --out my77을 실행한다. 검증 환경은 NumPy 2.3.5, SciPy 1.17.0이다. audit의 대조군은 각각 --no-hopping, --no-erase-hopping, --no-pf, --no-fn으로 생성했다. python check_results.py는 동봉한 결과와 출력 명령을 검사한다. audit/comparison.csv에서 ΔVt 단위는 V, 전하수지 잔차 단위는 A/m²이다.

참고 근거는 제공된 ATLAS User's Manual의 모델 표, §3의 DYNASONOS·PF 및 식 (3-504), MODELS의 BBT.KL, OUTPUT의 U.BBT, PROBE의 R.BBT, DeckBuild EXTRACT 설명이다. 공식 SONOS 예제 sonos-ex02에서도 PF.NITRIDE 사용을 확인할 수 있다.
