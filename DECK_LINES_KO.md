# DeckBuild 입력 줄별 해설

길이 좌표는 µm, 바이어스는 V다. 아래 표의 줄 번호는 배포한 파일과 일치한다. 각 구조의 RUN에는 다섯 상태 블록이 순서대로 들어 있다. 첫 블록과 이후 블록의 명령 의미는 같고 제목·qf·출력 이름이 바뀐다. 각 블록 시작 줄은 다음 표에서 찾을 수 있다.

| 파일 | fresh | programmed | erased | program_retained | erase_retained |
|---|---:|---:|---:|---:|---:|
| RUN_SONOS.in | 2 | 60 | 118 | 176 | 234 |
| RUN_SONOS_noBTBT.in | 2 | 60 | 118 | 176 | 234 |
| RUN_TANOS.in | 2 | 61 | 120 | 179 | 238 |
| RUN_TANOS_noBTBT.in | 2 | 61 | 120 | 179 | 238 |
| RUN_TANS.in | 2 | 58 | 114 | 170 | 226 |
| RUN_TANS_noBTBT.in | 2 | 58 | 114 | 170 | 226 |

단일 상태 덱도 동일한 명령을 사용한다. noBTBT 덱은 파일 이름에 noBTBT를 넣고 Si의 bbt.kl 키워드를 뺀 대조군이다. BIAS는 양·음 펄스의 말단 전압에서 접합을 보는 별도 DC 진단이다.

## generated/SONOS_77K_programmed.in

| 줄 | 실제 명령 | 요소와 역할 |
|---:|---|---|
| 1 | `# SONOS_77K_programmed. Reference geometry, uncalibrated parameters.` | 파일 용도 또는 매개변수 가정에 관한 주석. |
| 2 | `go atlas` | 새 ATLAS 세션을 시작한다. 다음 상태의 전극과 전하는 이 세션에서 다시 정의한다. |
| 3 | `title SONOS_77K_programmed` | 실행 결과를 식별할 제목을 정한다. |
| 4 | `mesh width=1` | 2차원 단면의 지면 수직 방향 폭을 1 µm로 설정한다. |
| 5 | `x.mesh loc=0 spac=0.15` | x 방향 좌표 0 µm에서 목표 격자 간격을 0.15 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 6 | `x.mesh loc=0.995 spac=0.005` | x 방향 좌표 0.995 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 7 | `x.mesh loc=1 spac=0.005` | x 방향 좌표 1 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 8 | `x.mesh loc=1.5 spac=0.05` | x 방향 좌표 1.5 µm에서 목표 격자 간격을 0.05 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 9 | `x.mesh loc=2 spac=0.005` | x 방향 좌표 2 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 10 | `x.mesh loc=2.005 spac=0.005` | x 방향 좌표 2.005 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 11 | `x.mesh loc=3 spac=0.15` | x 방향 좌표 3 µm에서 목표 격자 간격을 0.15 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 12 | `y.mesh loc=-0.098000 spac=0.02` | y 방향 좌표 -0.098000 µm에서 목표 격자 간격을 0.02 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 13 | `y.mesh loc=-0.018000 spac=0.0005` | y 방향 좌표 -0.018000 µm에서 목표 격자 간격을 0.0005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 14 | `y.mesh loc=-0.010000 spac=0.0004` | y 방향 좌표 -0.010000 µm에서 목표 격자 간격을 0.0004 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 15 | `y.mesh loc=-0.003000 spac=0.0002` | y 방향 좌표 -0.003000 µm에서 목표 격자 간격을 0.0002 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 16 | `y.mesh loc=0.000000 spac=0.00015` | y 방향 좌표 0.000000 µm에서 목표 격자 간격을 0.00015 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 17 | `y.mesh loc=0.010000 spac=0.002` | y 방향 좌표 0.010000 µm에서 목표 격자 간격을 0.002 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 18 | `y.mesh loc=0.030000 spac=0.004` | y 방향 좌표 0.030000 µm에서 목표 격자 간격을 0.004 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 19 | `y.mesh loc=0.100000 spac=0.012` | y 방향 좌표 0.100000 µm에서 목표 격자 간격을 0.012 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 20 | `y.mesh loc=0.400000 spac=0.05` | y 방향 좌표 0.400000 µm에서 목표 격자 간격을 0.05 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 21 | `region num=1 material=air` | 1번 영역은 배경 공기이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 22 | `region num=2 material=conductor x.min=1 x.max=2 y.min=-0.098000 y.max=-0.018000` | 2번 영역은 도체 게이트이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 23 | `region num=3 material=oxide x.min=1 x.max=2 y.min=-0.018000 y.max=-0.010000` | 3번 영역은 상부 차단 절연막이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 24 | `region num=4 material=nitride x.min=1 x.max=2 y.min=-0.010000 y.max=-0.003000` | 4번 영역은 질화막 전하 저장층이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 25 | `region num=5 material=oxide x.min=1 x.max=2 y.min=-0.003 y.max=0` | 5번 영역은 채널 쪽 SiO₂ 터널막이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 26 | `region num=6 material=silicon y.min=0` | 6번 영역은 Si 기판 및 채널이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 27 | `electrode name=cgate x.min=1 x.max=2 y.min=-0.098000 y.max=-0.018000` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 28 | `electrode name=source x.min=0 x.max=0.666667 y.min=0 y.max=0` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 29 | `electrode name=drain x.min=2.333333 x.max=3 y.min=0 y.max=0` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 30 | `electrode name=substrate bottom` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 31 | `doping uniform p.type conc=1e17 reg=6` | Si(6번)에 균일 p형 배경 도핑 10¹⁷ cm⁻³을 지정한다. |
| 32 | `doping gauss n.type conc=5e20 char=0.03 lat.char=0.005 reg=6 x.r=0.995` | Si에 n형 Gaussian 소스/드레인을 만든다. conc는 피크 농도(cm⁻³), char와 lat.char는 수직·수평 특성 길이(µm), x.r/x.l은 도핑 창 경계다. |
| 33 | `doping gauss n.type conc=5e20 char=0.03 lat.char=0.005 reg=6 x.l=2.005` | Si에 n형 Gaussian 소스/드레인을 만든다. conc는 피크 농도(cm⁻³), char와 lat.char는 수직·수평 특성 길이(µm), x.r/x.l은 도핑 창 경계다. |
| 34 | `material material=nitride permittivity=7.5 eg300=5.1 affinity=2.05 egalpha=0` | 비유전율 permittivity, 300 K 밴드갭 eg300(eV), 전자친화도 affinity(eV), 온도 계수 egalpha를 지정한다. 읽기 덱은 이 층을 유전체로 취급한다. |
| 35 | `material material=oxide permittivity=3.9 eg300=9.0 affinity=0.95 egalpha=0` | 비유전율 permittivity, 300 K 밴드갭 eg300(eV), 전자친화도 affinity(eV), 온도 계수 egalpha를 지정한다. 읽기 덱은 이 층을 유전체로 취급한다. |
| 36 | `interface qf=-685505928584.465 x.min=1 x.max=2 y.min=-0.00001 y.max=0.00001` | 게이트 아래 y=0 계면에 Python의 위치 가중 ΔVt와 등가인 부호 있는 고정전하 밀도 qf(cm⁻²)를 준다. 읽는 동안 고정된다. |
| 37 | `contact name=cgate workf=4.05` | 게이트의 유효 일함수 workf(eV)를 지정한다. SONOS 4.05, TANOS·TANS 4.60이다. |
| 38 | `models srh temp=77 print` | SRH 재결합과 격자 온도 77 K를 지정하고 모델을 출력한다. |
| 39 | `models region=6 fermidirac incomplete ioniz analytic bbt.kl print` | Si 영역에 Fermi–Dirac 통계, 불완전 이온화, 고농도 Si 이온화 보정, analytic 이동도 모델을 지정한다. bbt.kl이 있으면 국소 Klaassen BTBT도 활성화한다. print는 활성 모델을 출력한다. |
| 40 | `method newton carriers=2` | Newton 방법으로 전자·정공 연속방정식과 전위를 푼다. 기준 덱의 dt.min은 허용하는 최소 과도 시간 간격(s)이다. |
| 41 | `probe name=bbt_drain r.bbt x=2.005 y=0.001` | 드레인 쪽 지정 Si 좌표(µm)에서 국소 BTBT율을 로그에 기록한다. 공간 최대값은 .str의 U.BBT 분포를 본다. |
| 42 | `output con.band val.band qfn qfp band.param e.field u.bbt` | 저장 구조에 전도대·가전자대, 전자·정공 준페르미 준위, 재료 밴드 매개변수, 전계, BTBT율을 요청한다. 기준 덱의 sonos.rates는 질화막 주입·포획 속도도 요청한다. |
| 43 | `solve init` | 현재 전하와 물성으로 단자 0 V 초기 해를 구한다. |
| 44 | `save outf=SONOS_77K_programmed_zero.str` | 바로 앞에서 수렴한 구조와 물리량을 outf 이름의 TonyPlot 구조 파일에 기록한다. |
| 45 | `solve vdrain=0.0001` | 지정한 단자의 전압(V)에서 DC 해를 구한다. 다른 단자는 이전 바이어스를 유지한다. |
| 46 | `solve vdrain=0.001` | 지정한 단자의 전압(V)에서 DC 해를 구한다. 다른 단자는 이전 바이어스를 유지한다. |
| 47 | `solve name=drain vstep=0.001 vfinal=0.01` | name 전극의 전압을 vstep(V)씩 바꿔 vfinal(V)까지 DC 해를 구한다. BIAS 덱에서는 끝상태 qf가 램프 내내 고정된다. |
| 48 | `solve name=drain vstep=0.005 vfinal=0.1` | name 전극의 전압을 vstep(V)씩 바꿔 vfinal(V)까지 DC 해를 구한다. BIAS 덱에서는 끝상태 qf가 램프 내내 고정된다. |
| 49 | `solve name=cgate vstep=-0.05 vfinal=-2` | name 전극의 전압을 vstep(V)씩 바꿔 vfinal(V)까지 DC 해를 구한다. BIAS 덱에서는 끝상태 qf가 램프 내내 고정된다. |
| 50 | `log outf=SONOS_77K_programmed_read.log` | 이후 수렴한 점의 단자 전압·전류와 probe 값을 outf에 기록한다. |
| 51 | `solve vcgate=-2` | 지정한 단자의 전압(V)에서 DC 해를 구한다. 다른 단자는 이전 바이어스를 유지한다. |
| 52 | `solve name=cgate vstep=0.01 vfinal=8` | name 전극의 전압을 vstep(V)씩 바꿔 vfinal(V)까지 DC 해를 구한다. BIAS 덱에서는 끝상태 qf가 램프 내내 고정된다. |
| 53 | `log off` | 열린 전기적 로그를 닫는다. |
| 54 | `extract init infile="SONOS_77K_programmed_read.log"` | 방금 저장한 읽기 로그를 추출 입력으로 연다. |
| 55 | `extract name="Vt_gm" xintercept(maxslope(curve(v."cgate",i."drain"))) datafile="SONOS_77K_programmed_Vt.dat"` | 선형 Id–Vg 곡선의 최대 기울기 접선과 Vg축의 교점을 구해 파일에 기록한다. Vd/2 보정은 적용하지 않는다. |
| 56 | `extract name="Vt_gm_vd2" (xintercept(maxslope(curve(v."cgate",i."drain"))) - abs(ave(v."drain"))/2.0) datafile="SONOS_77K_programmed_Vt_vd2.dat"` | 같은 최대 gm 접선 절편에서 VD/2(=0.05 V)를 뺀 값을 기록한다. PGM−ERS 창에는 영향이 없다. |
| 57 | `extract name="IdVg" curve(v."cgate",i."drain") outfile="SONOS_77K_programmed_IdVg.dat"` | 읽기 Id–Vg 곡선을 텍스트로 내보낸다. analyze_reads.py가 이 파일로 VT를 다시 추출한다. |
| 58 | `quit` | DeckBuild 입력의 실행을 끝낸다. |

## generated/TANOS_77K_programmed.in

| 줄 | 실제 명령 | 요소와 역할 |
|---:|---|---|
| 1 | `# TANOS_77K_programmed. Reference geometry, uncalibrated parameters.` | 파일 용도 또는 매개변수 가정에 관한 주석. |
| 2 | `go atlas` | 새 ATLAS 세션을 시작한다. 다음 상태의 전극과 전하는 이 세션에서 다시 정의한다. |
| 3 | `title TANOS_77K_programmed` | 실행 결과를 식별할 제목을 정한다. |
| 4 | `mesh width=1` | 2차원 단면의 지면 수직 방향 폭을 1 µm로 설정한다. |
| 5 | `x.mesh loc=0 spac=0.15` | x 방향 좌표 0 µm에서 목표 격자 간격을 0.15 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 6 | `x.mesh loc=0.995 spac=0.005` | x 방향 좌표 0.995 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 7 | `x.mesh loc=1 spac=0.005` | x 방향 좌표 1 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 8 | `x.mesh loc=1.5 spac=0.05` | x 방향 좌표 1.5 µm에서 목표 격자 간격을 0.05 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 9 | `x.mesh loc=2 spac=0.005` | x 방향 좌표 2 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 10 | `x.mesh loc=2.005 spac=0.005` | x 방향 좌표 2.005 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 11 | `x.mesh loc=3 spac=0.15` | x 방향 좌표 3 µm에서 목표 격자 간격을 0.15 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 12 | `y.mesh loc=-0.098000 spac=0.02` | y 방향 좌표 -0.098000 µm에서 목표 격자 간격을 0.02 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 13 | `y.mesh loc=-0.018000 spac=0.0005` | y 방향 좌표 -0.018000 µm에서 목표 격자 간격을 0.0005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 14 | `y.mesh loc=-0.010000 spac=0.0004` | y 방향 좌표 -0.010000 µm에서 목표 격자 간격을 0.0004 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 15 | `y.mesh loc=-0.003000 spac=0.0002` | y 방향 좌표 -0.003000 µm에서 목표 격자 간격을 0.0002 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 16 | `y.mesh loc=0.000000 spac=0.00015` | y 방향 좌표 0.000000 µm에서 목표 격자 간격을 0.00015 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 17 | `y.mesh loc=0.010000 spac=0.002` | y 방향 좌표 0.010000 µm에서 목표 격자 간격을 0.002 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 18 | `y.mesh loc=0.030000 spac=0.004` | y 방향 좌표 0.030000 µm에서 목표 격자 간격을 0.004 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 19 | `y.mesh loc=0.100000 spac=0.012` | y 방향 좌표 0.100000 µm에서 목표 격자 간격을 0.012 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 20 | `y.mesh loc=0.400000 spac=0.05` | y 방향 좌표 0.400000 µm에서 목표 격자 간격을 0.05 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 21 | `region num=1 material=air` | 1번 영역은 배경 공기이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 22 | `region num=2 material=conductor x.min=1 x.max=2 y.min=-0.098000 y.max=-0.018000` | 2번 영역은 도체 게이트이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 23 | `region num=3 material=Al2O3 x.min=1 x.max=2 y.min=-0.018000 y.max=-0.010000` | 3번 영역은 상부 차단 절연막이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 24 | `region num=4 material=nitride x.min=1 x.max=2 y.min=-0.010000 y.max=-0.003000` | 4번 영역은 질화막 전하 저장층이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 25 | `region num=5 material=oxide x.min=1 x.max=2 y.min=-0.003 y.max=0` | 5번 영역은 채널 쪽 SiO₂ 터널막이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 26 | `region num=6 material=silicon y.min=0` | 6번 영역은 Si 기판 및 채널이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 27 | `electrode name=cgate x.min=1 x.max=2 y.min=-0.098000 y.max=-0.018000` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 28 | `electrode name=source x.min=0 x.max=0.666667 y.min=0 y.max=0` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 29 | `electrode name=drain x.min=2.333333 x.max=3 y.min=0 y.max=0` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 30 | `electrode name=substrate bottom` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 31 | `doping uniform p.type conc=1e17 reg=6` | Si(6번)에 균일 p형 배경 도핑 10¹⁷ cm⁻³을 지정한다. |
| 32 | `doping gauss n.type conc=5e20 char=0.03 lat.char=0.005 reg=6 x.r=0.995` | Si에 n형 Gaussian 소스/드레인을 만든다. conc는 피크 농도(cm⁻³), char와 lat.char는 수직·수평 특성 길이(µm), x.r/x.l은 도핑 창 경계다. |
| 33 | `doping gauss n.type conc=5e20 char=0.03 lat.char=0.005 reg=6 x.l=2.005` | Si에 n형 Gaussian 소스/드레인을 만든다. conc는 피크 농도(cm⁻³), char와 lat.char는 수직·수평 특성 길이(µm), x.r/x.l은 도핑 창 경계다. |
| 34 | `material material=nitride permittivity=7.5 eg300=5.1 affinity=2.05 egalpha=0` | 비유전율 permittivity, 300 K 밴드갭 eg300(eV), 전자친화도 affinity(eV), 온도 계수 egalpha를 지정한다. 읽기 덱은 이 층을 유전체로 취급한다. |
| 35 | `material material=oxide permittivity=3.9 eg300=9.0 affinity=0.95 egalpha=0` | 비유전율 permittivity, 300 K 밴드갭 eg300(eV), 전자친화도 affinity(eV), 온도 계수 egalpha를 지정한다. 읽기 덱은 이 층을 유전체로 취급한다. |
| 36 | `material material=Al2O3 permittivity=9.3 eg300=8.0 affinity=1.50 egalpha=0` | 비유전율 permittivity, 300 K 밴드갭 eg300(eV), 전자친화도 affinity(eV), 온도 계수 egalpha를 지정한다. 읽기 덱은 이 층을 유전체로 취급한다. |
| 37 | `interface qf=-1241870822855.83 x.min=1 x.max=2 y.min=-0.00001 y.max=0.00001` | 게이트 아래 y=0 계면에 Python의 위치 가중 ΔVt와 등가인 부호 있는 고정전하 밀도 qf(cm⁻²)를 준다. 읽는 동안 고정된다. |
| 38 | `contact name=cgate workf=4.60` | 게이트의 유효 일함수 workf(eV)를 지정한다. SONOS 4.05, TANOS·TANS 4.60이다. |
| 39 | `models srh temp=77 print` | SRH 재결합과 격자 온도 77 K를 지정하고 모델을 출력한다. |
| 40 | `models region=6 fermidirac incomplete ioniz analytic bbt.kl print` | Si 영역에 Fermi–Dirac 통계, 불완전 이온화, 고농도 Si 이온화 보정, analytic 이동도 모델을 지정한다. bbt.kl이 있으면 국소 Klaassen BTBT도 활성화한다. print는 활성 모델을 출력한다. |
| 41 | `method newton carriers=2` | Newton 방법으로 전자·정공 연속방정식과 전위를 푼다. 기준 덱의 dt.min은 허용하는 최소 과도 시간 간격(s)이다. |
| 42 | `probe name=bbt_drain r.bbt x=2.005 y=0.001` | 드레인 쪽 지정 Si 좌표(µm)에서 국소 BTBT율을 로그에 기록한다. 공간 최대값은 .str의 U.BBT 분포를 본다. |
| 43 | `output con.band val.band qfn qfp band.param e.field u.bbt` | 저장 구조에 전도대·가전자대, 전자·정공 준페르미 준위, 재료 밴드 매개변수, 전계, BTBT율을 요청한다. 기준 덱의 sonos.rates는 질화막 주입·포획 속도도 요청한다. |
| 44 | `solve init` | 현재 전하와 물성으로 단자 0 V 초기 해를 구한다. |
| 45 | `save outf=TANOS_77K_programmed_zero.str` | 바로 앞에서 수렴한 구조와 물리량을 outf 이름의 TonyPlot 구조 파일에 기록한다. |
| 46 | `solve vdrain=0.0001` | 지정한 단자의 전압(V)에서 DC 해를 구한다. 다른 단자는 이전 바이어스를 유지한다. |
| 47 | `solve vdrain=0.001` | 지정한 단자의 전압(V)에서 DC 해를 구한다. 다른 단자는 이전 바이어스를 유지한다. |
| 48 | `solve name=drain vstep=0.001 vfinal=0.01` | name 전극의 전압을 vstep(V)씩 바꿔 vfinal(V)까지 DC 해를 구한다. BIAS 덱에서는 끝상태 qf가 램프 내내 고정된다. |
| 49 | `solve name=drain vstep=0.005 vfinal=0.1` | name 전극의 전압을 vstep(V)씩 바꿔 vfinal(V)까지 DC 해를 구한다. BIAS 덱에서는 끝상태 qf가 램프 내내 고정된다. |
| 50 | `solve name=cgate vstep=-0.05 vfinal=-2` | name 전극의 전압을 vstep(V)씩 바꿔 vfinal(V)까지 DC 해를 구한다. BIAS 덱에서는 끝상태 qf가 램프 내내 고정된다. |
| 51 | `log outf=TANOS_77K_programmed_read.log` | 이후 수렴한 점의 단자 전압·전류와 probe 값을 outf에 기록한다. |
| 52 | `solve vcgate=-2` | 지정한 단자의 전압(V)에서 DC 해를 구한다. 다른 단자는 이전 바이어스를 유지한다. |
| 53 | `solve name=cgate vstep=0.01 vfinal=8` | name 전극의 전압을 vstep(V)씩 바꿔 vfinal(V)까지 DC 해를 구한다. BIAS 덱에서는 끝상태 qf가 램프 내내 고정된다. |
| 54 | `log off` | 열린 전기적 로그를 닫는다. |
| 55 | `extract init infile="TANOS_77K_programmed_read.log"` | 방금 저장한 읽기 로그를 추출 입력으로 연다. |
| 56 | `extract name="Vt_gm" xintercept(maxslope(curve(v."cgate",i."drain"))) datafile="TANOS_77K_programmed_Vt.dat"` | 선형 Id–Vg 곡선의 최대 기울기 접선과 Vg축의 교점을 구해 파일에 기록한다. Vd/2 보정은 적용하지 않는다. |
| 57 | `extract name="Vt_gm_vd2" (xintercept(maxslope(curve(v."cgate",i."drain"))) - abs(ave(v."drain"))/2.0) datafile="TANOS_77K_programmed_Vt_vd2.dat"` | 같은 최대 gm 접선 절편에서 VD/2(=0.05 V)를 뺀 값을 기록한다. PGM−ERS 창에는 영향이 없다. |
| 58 | `extract name="IdVg" curve(v."cgate",i."drain") outfile="TANOS_77K_programmed_IdVg.dat"` | 읽기 Id–Vg 곡선을 텍스트로 내보낸다. analyze_reads.py가 이 파일로 VT를 다시 추출한다. |
| 59 | `quit` | DeckBuild 입력의 실행을 끝낸다. |

## generated/TANS_77K_programmed.in

| 줄 | 실제 명령 | 요소와 역할 |
|---:|---|---|
| 1 | `# TANS_77K_programmed. Reference geometry, uncalibrated parameters.` | 파일 용도 또는 매개변수 가정에 관한 주석. |
| 2 | `go atlas` | 새 ATLAS 세션을 시작한다. 다음 상태의 전극과 전하는 이 세션에서 다시 정의한다. |
| 3 | `title TANS_77K_programmed` | 실행 결과를 식별할 제목을 정한다. |
| 4 | `mesh width=1` | 2차원 단면의 지면 수직 방향 폭을 1 µm로 설정한다. |
| 5 | `x.mesh loc=0 spac=0.15` | x 방향 좌표 0 µm에서 목표 격자 간격을 0.15 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 6 | `x.mesh loc=0.995 spac=0.005` | x 방향 좌표 0.995 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 7 | `x.mesh loc=1 spac=0.005` | x 방향 좌표 1 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 8 | `x.mesh loc=1.5 spac=0.05` | x 방향 좌표 1.5 µm에서 목표 격자 간격을 0.05 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 9 | `x.mesh loc=2 spac=0.005` | x 방향 좌표 2 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 10 | `x.mesh loc=2.005 spac=0.005` | x 방향 좌표 2.005 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 11 | `x.mesh loc=3 spac=0.15` | x 방향 좌표 3 µm에서 목표 격자 간격을 0.15 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 12 | `y.mesh loc=-0.095000 spac=0.02` | y 방향 좌표 -0.095000 µm에서 목표 격자 간격을 0.02 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 13 | `y.mesh loc=-0.015000 spac=0.0005` | y 방향 좌표 -0.015000 µm에서 목표 격자 간격을 0.0005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 14 | `y.mesh loc=-0.007000 spac=0.0004` | y 방향 좌표 -0.007000 µm에서 목표 격자 간격을 0.0004 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 15 | `y.mesh loc=0.000000 spac=0.00015` | y 방향 좌표 0.000000 µm에서 목표 격자 간격을 0.00015 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 16 | `y.mesh loc=0.010000 spac=0.002` | y 방향 좌표 0.010000 µm에서 목표 격자 간격을 0.002 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 17 | `y.mesh loc=0.030000 spac=0.004` | y 방향 좌표 0.030000 µm에서 목표 격자 간격을 0.004 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 18 | `y.mesh loc=0.100000 spac=0.012` | y 방향 좌표 0.100000 µm에서 목표 격자 간격을 0.012 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 19 | `y.mesh loc=0.400000 spac=0.05` | y 방향 좌표 0.400000 µm에서 목표 격자 간격을 0.05 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 20 | `region num=1 material=air` | 1번 영역은 배경 공기이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 21 | `region num=2 material=conductor x.min=1 x.max=2 y.min=-0.095000 y.max=-0.015000` | 2번 영역은 도체 게이트이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 22 | `region num=3 material=Al2O3 x.min=1 x.max=2 y.min=-0.015000 y.max=-0.007000` | 3번 영역은 상부 차단 절연막이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 23 | `region num=4 material=nitride x.min=1 x.max=2 y.min=-0.007000 y.max=0.000000` | 4번 영역은 질화막 전하 저장층이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 24 | `region num=6 material=silicon y.min=0` | 6번 영역은 Si 기판 및 채널이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 25 | `electrode name=cgate x.min=1 x.max=2 y.min=-0.095000 y.max=-0.015000` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 26 | `electrode name=source x.min=0 x.max=0.666667 y.min=0 y.max=0` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 27 | `electrode name=drain x.min=2.333333 x.max=3 y.min=0 y.max=0` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 28 | `electrode name=substrate bottom` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 29 | `doping uniform p.type conc=1e17 reg=6` | Si(6번)에 균일 p형 배경 도핑 10¹⁷ cm⁻³을 지정한다. |
| 30 | `doping gauss n.type conc=5e20 char=0.03 lat.char=0.005 reg=6 x.r=0.995` | Si에 n형 Gaussian 소스/드레인을 만든다. conc는 피크 농도(cm⁻³), char와 lat.char는 수직·수평 특성 길이(µm), x.r/x.l은 도핑 창 경계다. |
| 31 | `doping gauss n.type conc=5e20 char=0.03 lat.char=0.005 reg=6 x.l=2.005` | Si에 n형 Gaussian 소스/드레인을 만든다. conc는 피크 농도(cm⁻³), char와 lat.char는 수직·수평 특성 길이(µm), x.r/x.l은 도핑 창 경계다. |
| 32 | `material material=nitride permittivity=7.5 eg300=5.1 affinity=2.05 egalpha=0` | 비유전율 permittivity, 300 K 밴드갭 eg300(eV), 전자친화도 affinity(eV), 온도 계수 egalpha를 지정한다. 읽기 덱은 이 층을 유전체로 취급한다. |
| 33 | `material material=Al2O3 permittivity=9.3 eg300=8.0 affinity=1.50 egalpha=0` | 비유전율 permittivity, 300 K 밴드갭 eg300(eV), 전자친화도 affinity(eV), 온도 계수 egalpha를 지정한다. 읽기 덱은 이 층을 유전체로 취급한다. |
| 34 | `interface qf=-5600021166.70533 x.min=1 x.max=2 y.min=-0.00001 y.max=0.00001` | 게이트 아래 y=0 계면에 Python의 위치 가중 ΔVt와 등가인 부호 있는 고정전하 밀도 qf(cm⁻²)를 준다. 읽는 동안 고정된다. |
| 35 | `contact name=cgate workf=4.60` | 게이트의 유효 일함수 workf(eV)를 지정한다. SONOS 4.05, TANOS·TANS 4.60이다. |
| 36 | `models srh temp=77 print` | SRH 재결합과 격자 온도 77 K를 지정하고 모델을 출력한다. |
| 37 | `models region=6 fermidirac incomplete ioniz analytic bbt.kl print` | Si 영역에 Fermi–Dirac 통계, 불완전 이온화, 고농도 Si 이온화 보정, analytic 이동도 모델을 지정한다. bbt.kl이 있으면 국소 Klaassen BTBT도 활성화한다. print는 활성 모델을 출력한다. |
| 38 | `method newton carriers=2` | Newton 방법으로 전자·정공 연속방정식과 전위를 푼다. 기준 덱의 dt.min은 허용하는 최소 과도 시간 간격(s)이다. |
| 39 | `probe name=bbt_drain r.bbt x=2.005 y=0.001` | 드레인 쪽 지정 Si 좌표(µm)에서 국소 BTBT율을 로그에 기록한다. 공간 최대값은 .str의 U.BBT 분포를 본다. |
| 40 | `output con.band val.band qfn qfp band.param e.field u.bbt` | 저장 구조에 전도대·가전자대, 전자·정공 준페르미 준위, 재료 밴드 매개변수, 전계, BTBT율을 요청한다. 기준 덱의 sonos.rates는 질화막 주입·포획 속도도 요청한다. |
| 41 | `solve init` | 현재 전하와 물성으로 단자 0 V 초기 해를 구한다. |
| 42 | `save outf=TANS_77K_programmed_zero.str` | 바로 앞에서 수렴한 구조와 물리량을 outf 이름의 TonyPlot 구조 파일에 기록한다. |
| 43 | `solve vdrain=0.0001` | 지정한 단자의 전압(V)에서 DC 해를 구한다. 다른 단자는 이전 바이어스를 유지한다. |
| 44 | `solve vdrain=0.001` | 지정한 단자의 전압(V)에서 DC 해를 구한다. 다른 단자는 이전 바이어스를 유지한다. |
| 45 | `solve name=drain vstep=0.001 vfinal=0.01` | name 전극의 전압을 vstep(V)씩 바꿔 vfinal(V)까지 DC 해를 구한다. BIAS 덱에서는 끝상태 qf가 램프 내내 고정된다. |
| 46 | `solve name=drain vstep=0.005 vfinal=0.1` | name 전극의 전압을 vstep(V)씩 바꿔 vfinal(V)까지 DC 해를 구한다. BIAS 덱에서는 끝상태 qf가 램프 내내 고정된다. |
| 47 | `solve name=cgate vstep=-0.05 vfinal=-2` | name 전극의 전압을 vstep(V)씩 바꿔 vfinal(V)까지 DC 해를 구한다. BIAS 덱에서는 끝상태 qf가 램프 내내 고정된다. |
| 48 | `log outf=TANS_77K_programmed_read.log` | 이후 수렴한 점의 단자 전압·전류와 probe 값을 outf에 기록한다. |
| 49 | `solve vcgate=-2` | 지정한 단자의 전압(V)에서 DC 해를 구한다. 다른 단자는 이전 바이어스를 유지한다. |
| 50 | `solve name=cgate vstep=0.01 vfinal=8` | name 전극의 전압을 vstep(V)씩 바꿔 vfinal(V)까지 DC 해를 구한다. BIAS 덱에서는 끝상태 qf가 램프 내내 고정된다. |
| 51 | `log off` | 열린 전기적 로그를 닫는다. |
| 52 | `extract init infile="TANS_77K_programmed_read.log"` | 방금 저장한 읽기 로그를 추출 입력으로 연다. |
| 53 | `extract name="Vt_gm" xintercept(maxslope(curve(v."cgate",i."drain"))) datafile="TANS_77K_programmed_Vt.dat"` | 선형 Id–Vg 곡선의 최대 기울기 접선과 Vg축의 교점을 구해 파일에 기록한다. Vd/2 보정은 적용하지 않는다. |
| 54 | `extract name="Vt_gm_vd2" (xintercept(maxslope(curve(v."cgate",i."drain"))) - abs(ave(v."drain"))/2.0) datafile="TANS_77K_programmed_Vt_vd2.dat"` | 같은 최대 gm 접선 절편에서 VD/2(=0.05 V)를 뺀 값을 기록한다. PGM−ERS 창에는 영향이 없다. |
| 55 | `extract name="IdVg" curve(v."cgate",i."drain") outfile="TANS_77K_programmed_IdVg.dat"` | 읽기 Id–Vg 곡선을 텍스트로 내보낸다. analyze_reads.py가 이 파일로 VT를 다시 추출한다. |
| 56 | `quit` | DeckBuild 입력의 실행을 끝낸다. |

## generated/BIAS_SONOS.in

| 줄 | 실제 명령 | 요소와 역할 |
|---:|---|---|
| 1 | `# SONOS_77K_program_hold. Reference geometry, uncalibrated parameters.` | 파일 용도 또는 매개변수 가정에 관한 주석. |
| 2 | `go atlas` | 새 ATLAS 세션을 시작한다. 다음 상태의 전극과 전하는 이 세션에서 다시 정의한다. |
| 3 | `title SONOS_77K_program_hold` | 실행 결과를 식별할 제목을 정한다. |
| 4 | `mesh width=1` | 2차원 단면의 지면 수직 방향 폭을 1 µm로 설정한다. |
| 5 | `x.mesh loc=0 spac=0.15` | x 방향 좌표 0 µm에서 목표 격자 간격을 0.15 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 6 | `x.mesh loc=0.995 spac=0.005` | x 방향 좌표 0.995 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 7 | `x.mesh loc=1 spac=0.005` | x 방향 좌표 1 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 8 | `x.mesh loc=1.5 spac=0.05` | x 방향 좌표 1.5 µm에서 목표 격자 간격을 0.05 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 9 | `x.mesh loc=2 spac=0.005` | x 방향 좌표 2 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 10 | `x.mesh loc=2.005 spac=0.005` | x 방향 좌표 2.005 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 11 | `x.mesh loc=3 spac=0.15` | x 방향 좌표 3 µm에서 목표 격자 간격을 0.15 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 12 | `y.mesh loc=-0.098000 spac=0.02` | y 방향 좌표 -0.098000 µm에서 목표 격자 간격을 0.02 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 13 | `y.mesh loc=-0.018000 spac=0.0005` | y 방향 좌표 -0.018000 µm에서 목표 격자 간격을 0.0005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 14 | `y.mesh loc=-0.010000 spac=0.0004` | y 방향 좌표 -0.010000 µm에서 목표 격자 간격을 0.0004 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 15 | `y.mesh loc=-0.003000 spac=0.0002` | y 방향 좌표 -0.003000 µm에서 목표 격자 간격을 0.0002 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 16 | `y.mesh loc=0.000000 spac=0.00015` | y 방향 좌표 0.000000 µm에서 목표 격자 간격을 0.00015 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 17 | `y.mesh loc=0.010000 spac=0.002` | y 방향 좌표 0.010000 µm에서 목표 격자 간격을 0.002 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 18 | `y.mesh loc=0.030000 spac=0.004` | y 방향 좌표 0.030000 µm에서 목표 격자 간격을 0.004 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 19 | `y.mesh loc=0.100000 spac=0.012` | y 방향 좌표 0.100000 µm에서 목표 격자 간격을 0.012 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 20 | `y.mesh loc=0.400000 spac=0.05` | y 방향 좌표 0.400000 µm에서 목표 격자 간격을 0.05 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 21 | `region num=1 material=air` | 1번 영역은 배경 공기이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 22 | `region num=2 material=conductor x.min=1 x.max=2 y.min=-0.098000 y.max=-0.018000` | 2번 영역은 도체 게이트이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 23 | `region num=3 material=oxide x.min=1 x.max=2 y.min=-0.018000 y.max=-0.010000` | 3번 영역은 상부 차단 절연막이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 24 | `region num=4 material=nitride x.min=1 x.max=2 y.min=-0.010000 y.max=-0.003000` | 4번 영역은 질화막 전하 저장층이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 25 | `region num=5 material=oxide x.min=1 x.max=2 y.min=-0.003 y.max=0` | 5번 영역은 채널 쪽 SiO₂ 터널막이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 26 | `region num=6 material=silicon y.min=0` | 6번 영역은 Si 기판 및 채널이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 27 | `electrode name=cgate x.min=1 x.max=2 y.min=-0.098000 y.max=-0.018000` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 28 | `electrode name=source x.min=0 x.max=0.666667 y.min=0 y.max=0` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 29 | `electrode name=drain x.min=2.333333 x.max=3 y.min=0 y.max=0` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 30 | `electrode name=substrate bottom` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 31 | `doping uniform p.type conc=1e17 reg=6` | Si(6번)에 균일 p형 배경 도핑 10¹⁷ cm⁻³을 지정한다. |
| 32 | `doping gauss n.type conc=5e20 char=0.03 lat.char=0.005 reg=6 x.r=0.995` | Si에 n형 Gaussian 소스/드레인을 만든다. conc는 피크 농도(cm⁻³), char와 lat.char는 수직·수평 특성 길이(µm), x.r/x.l은 도핑 창 경계다. |
| 33 | `doping gauss n.type conc=5e20 char=0.03 lat.char=0.005 reg=6 x.l=2.005` | Si에 n형 Gaussian 소스/드레인을 만든다. conc는 피크 농도(cm⁻³), char와 lat.char는 수직·수평 특성 길이(µm), x.r/x.l은 도핑 창 경계다. |
| 34 | `material material=nitride permittivity=7.5 eg300=5.1 affinity=2.05 egalpha=0` | 비유전율 permittivity, 300 K 밴드갭 eg300(eV), 전자친화도 affinity(eV), 온도 계수 egalpha를 지정한다. 읽기 덱은 이 층을 유전체로 취급한다. |
| 35 | `material material=oxide permittivity=3.9 eg300=9.0 affinity=0.95 egalpha=0` | 비유전율 permittivity, 300 K 밴드갭 eg300(eV), 전자친화도 affinity(eV), 온도 계수 egalpha를 지정한다. 읽기 덱은 이 층을 유전체로 취급한다. |
| 36 | `interface qf=-685509394943.011 x.min=1 x.max=2 y.min=-0.00001 y.max=0.00001` | 게이트 아래 y=0 계면에 Python의 위치 가중 ΔVt와 등가인 부호 있는 고정전하 밀도 qf(cm⁻²)를 준다. 읽는 동안 고정된다. |
| 37 | `contact name=cgate workf=4.05` | 게이트의 유효 일함수 workf(eV)를 지정한다. SONOS 4.05, TANOS·TANS 4.60이다. |
| 38 | `models srh temp=77 print` | SRH 재결합과 격자 온도 77 K를 지정하고 모델을 출력한다. |
| 39 | `models region=6 fermidirac incomplete ioniz analytic bbt.kl print` | Si 영역에 Fermi–Dirac 통계, 불완전 이온화, 고농도 Si 이온화 보정, analytic 이동도 모델을 지정한다. bbt.kl이 있으면 국소 Klaassen BTBT도 활성화한다. print는 활성 모델을 출력한다. |
| 40 | `method newton carriers=2` | Newton 방법으로 전자·정공 연속방정식과 전위를 푼다. 기준 덱의 dt.min은 허용하는 최소 과도 시간 간격(s)이다. |
| 41 | `probe name=bbt_drain r.bbt x=2.005 y=0.001` | 드레인 쪽 지정 Si 좌표(µm)에서 국소 BTBT율을 로그에 기록한다. 공간 최대값은 .str의 U.BBT 분포를 본다. |
| 42 | `output con.band val.band qfn qfp band.param e.field u.bbt` | 저장 구조에 전도대·가전자대, 전자·정공 준페르미 준위, 재료 밴드 매개변수, 전계, BTBT율을 요청한다. 기준 덱의 sonos.rates는 질화막 주입·포획 속도도 요청한다. |
| 43 | `solve init` | 현재 전하와 물성으로 단자 0 V 초기 해를 구한다. |
| 44 | `log outf=SONOS_77K_program_hold_bias.log` | 이후 수렴한 점의 단자 전압·전류와 probe 값을 outf에 기록한다. |
| 45 | `solve vcgate=0` | 지정한 단자의 전압(V)에서 DC 해를 구한다. 다른 단자는 이전 바이어스를 유지한다. |
| 46 | `solve name=cgate vstep=0.05 vfinal=16` | name 전극의 전압을 vstep(V)씩 바꿔 vfinal(V)까지 DC 해를 구한다. BIAS 덱에서는 끝상태 qf가 램프 내내 고정된다. |
| 47 | `log off` | 열린 전기적 로그를 닫는다. |
| 48 | `save outf=SONOS_77K_program_hold.str` | 바로 앞에서 수렴한 구조와 물리량을 outf 이름의 TonyPlot 구조 파일에 기록한다. |
| 49 | `` | 실행 블록을 구분하는 빈 줄. |
| 50 | `# SONOS_77K_erase_hold. Reference geometry, uncalibrated parameters.` | 파일 용도 또는 매개변수 가정에 관한 주석. |
| 51 | `go atlas` | 새 ATLAS 세션을 시작한다. 다음 상태의 전극과 전하는 이 세션에서 다시 정의한다. |
| 52 | `title SONOS_77K_erase_hold` | 실행 결과를 식별할 제목을 정한다. |
| 53 | `mesh width=1` | 2차원 단면의 지면 수직 방향 폭을 1 µm로 설정한다. |
| 54 | `x.mesh loc=0 spac=0.15` | x 방향 좌표 0 µm에서 목표 격자 간격을 0.15 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 55 | `x.mesh loc=0.995 spac=0.005` | x 방향 좌표 0.995 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 56 | `x.mesh loc=1 spac=0.005` | x 방향 좌표 1 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 57 | `x.mesh loc=1.5 spac=0.05` | x 방향 좌표 1.5 µm에서 목표 격자 간격을 0.05 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 58 | `x.mesh loc=2 spac=0.005` | x 방향 좌표 2 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 59 | `x.mesh loc=2.005 spac=0.005` | x 방향 좌표 2.005 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 60 | `x.mesh loc=3 spac=0.15` | x 방향 좌표 3 µm에서 목표 격자 간격을 0.15 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 61 | `y.mesh loc=-0.098000 spac=0.02` | y 방향 좌표 -0.098000 µm에서 목표 격자 간격을 0.02 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 62 | `y.mesh loc=-0.018000 spac=0.0005` | y 방향 좌표 -0.018000 µm에서 목표 격자 간격을 0.0005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 63 | `y.mesh loc=-0.010000 spac=0.0004` | y 방향 좌표 -0.010000 µm에서 목표 격자 간격을 0.0004 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 64 | `y.mesh loc=-0.003000 spac=0.0002` | y 방향 좌표 -0.003000 µm에서 목표 격자 간격을 0.0002 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 65 | `y.mesh loc=0.000000 spac=0.00015` | y 방향 좌표 0.000000 µm에서 목표 격자 간격을 0.00015 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 66 | `y.mesh loc=0.010000 spac=0.002` | y 방향 좌표 0.010000 µm에서 목표 격자 간격을 0.002 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 67 | `y.mesh loc=0.030000 spac=0.004` | y 방향 좌표 0.030000 µm에서 목표 격자 간격을 0.004 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 68 | `y.mesh loc=0.100000 spac=0.012` | y 방향 좌표 0.100000 µm에서 목표 격자 간격을 0.012 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 69 | `y.mesh loc=0.400000 spac=0.05` | y 방향 좌표 0.400000 µm에서 목표 격자 간격을 0.05 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 70 | `region num=1 material=air` | 1번 영역은 배경 공기이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 71 | `region num=2 material=conductor x.min=1 x.max=2 y.min=-0.098000 y.max=-0.018000` | 2번 영역은 도체 게이트이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 72 | `region num=3 material=oxide x.min=1 x.max=2 y.min=-0.018000 y.max=-0.010000` | 3번 영역은 상부 차단 절연막이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 73 | `region num=4 material=nitride x.min=1 x.max=2 y.min=-0.010000 y.max=-0.003000` | 4번 영역은 질화막 전하 저장층이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 74 | `region num=5 material=oxide x.min=1 x.max=2 y.min=-0.003 y.max=0` | 5번 영역은 채널 쪽 SiO₂ 터널막이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 75 | `region num=6 material=silicon y.min=0` | 6번 영역은 Si 기판 및 채널이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 76 | `electrode name=cgate x.min=1 x.max=2 y.min=-0.098000 y.max=-0.018000` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 77 | `electrode name=source x.min=0 x.max=0.666667 y.min=0 y.max=0` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 78 | `electrode name=drain x.min=2.333333 x.max=3 y.min=0 y.max=0` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 79 | `electrode name=substrate bottom` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 80 | `doping uniform p.type conc=1e17 reg=6` | Si(6번)에 균일 p형 배경 도핑 10¹⁷ cm⁻³을 지정한다. |
| 81 | `doping gauss n.type conc=5e20 char=0.03 lat.char=0.005 reg=6 x.r=0.995` | Si에 n형 Gaussian 소스/드레인을 만든다. conc는 피크 농도(cm⁻³), char와 lat.char는 수직·수평 특성 길이(µm), x.r/x.l은 도핑 창 경계다. |
| 82 | `doping gauss n.type conc=5e20 char=0.03 lat.char=0.005 reg=6 x.l=2.005` | Si에 n형 Gaussian 소스/드레인을 만든다. conc는 피크 농도(cm⁻³), char와 lat.char는 수직·수평 특성 길이(µm), x.r/x.l은 도핑 창 경계다. |
| 83 | `material material=nitride permittivity=7.5 eg300=5.1 affinity=2.05 egalpha=0` | 비유전율 permittivity, 300 K 밴드갭 eg300(eV), 전자친화도 affinity(eV), 온도 계수 egalpha를 지정한다. 읽기 덱은 이 층을 유전체로 취급한다. |
| 84 | `material material=oxide permittivity=3.9 eg300=9.0 affinity=0.95 egalpha=0` | 비유전율 permittivity, 300 K 밴드갭 eg300(eV), 전자친화도 affinity(eV), 온도 계수 egalpha를 지정한다. 읽기 덱은 이 층을 유전체로 취급한다. |
| 85 | `interface qf=-758360329250.814 x.min=1 x.max=2 y.min=-0.00001 y.max=0.00001` | 게이트 아래 y=0 계면에 Python의 위치 가중 ΔVt와 등가인 부호 있는 고정전하 밀도 qf(cm⁻²)를 준다. 읽는 동안 고정된다. |
| 86 | `contact name=cgate workf=4.05` | 게이트의 유효 일함수 workf(eV)를 지정한다. SONOS 4.05, TANOS·TANS 4.60이다. |
| 87 | `models srh temp=77 print` | SRH 재결합과 격자 온도 77 K를 지정하고 모델을 출력한다. |
| 88 | `models region=6 fermidirac incomplete ioniz analytic bbt.kl print` | Si 영역에 Fermi–Dirac 통계, 불완전 이온화, 고농도 Si 이온화 보정, analytic 이동도 모델을 지정한다. bbt.kl이 있으면 국소 Klaassen BTBT도 활성화한다. print는 활성 모델을 출력한다. |
| 89 | `method newton carriers=2` | Newton 방법으로 전자·정공 연속방정식과 전위를 푼다. 기준 덱의 dt.min은 허용하는 최소 과도 시간 간격(s)이다. |
| 90 | `probe name=bbt_drain r.bbt x=2.005 y=0.001` | 드레인 쪽 지정 Si 좌표(µm)에서 국소 BTBT율을 로그에 기록한다. 공간 최대값은 .str의 U.BBT 분포를 본다. |
| 91 | `output con.band val.band qfn qfp band.param e.field u.bbt` | 저장 구조에 전도대·가전자대, 전자·정공 준페르미 준위, 재료 밴드 매개변수, 전계, BTBT율을 요청한다. 기준 덱의 sonos.rates는 질화막 주입·포획 속도도 요청한다. |
| 92 | `solve init` | 현재 전하와 물성으로 단자 0 V 초기 해를 구한다. |
| 93 | `log outf=SONOS_77K_erase_hold_bias.log` | 이후 수렴한 점의 단자 전압·전류와 probe 값을 outf에 기록한다. |
| 94 | `solve vcgate=0` | 지정한 단자의 전압(V)에서 DC 해를 구한다. 다른 단자는 이전 바이어스를 유지한다. |
| 95 | `solve name=cgate vstep=-0.05 vfinal=-12` | name 전극의 전압을 vstep(V)씩 바꿔 vfinal(V)까지 DC 해를 구한다. BIAS 덱에서는 끝상태 qf가 램프 내내 고정된다. |
| 96 | `log off` | 열린 전기적 로그를 닫는다. |
| 97 | `save outf=SONOS_77K_erase_hold.str` | 바로 앞에서 수렴한 구조와 물리량을 outf 이름의 TonyPlot 구조 파일에 기록한다. |
| 98 | `quit` | DeckBuild 입력의 실행을 끝낸다. |

## generated/BIAS_TANOS.in

| 줄 | 실제 명령 | 요소와 역할 |
|---:|---|---|
| 1 | `# TANOS_77K_program_hold. Reference geometry, uncalibrated parameters.` | 파일 용도 또는 매개변수 가정에 관한 주석. |
| 2 | `go atlas` | 새 ATLAS 세션을 시작한다. 다음 상태의 전극과 전하는 이 세션에서 다시 정의한다. |
| 3 | `title TANOS_77K_program_hold` | 실행 결과를 식별할 제목을 정한다. |
| 4 | `mesh width=1` | 2차원 단면의 지면 수직 방향 폭을 1 µm로 설정한다. |
| 5 | `x.mesh loc=0 spac=0.15` | x 방향 좌표 0 µm에서 목표 격자 간격을 0.15 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 6 | `x.mesh loc=0.995 spac=0.005` | x 방향 좌표 0.995 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 7 | `x.mesh loc=1 spac=0.005` | x 방향 좌표 1 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 8 | `x.mesh loc=1.5 spac=0.05` | x 방향 좌표 1.5 µm에서 목표 격자 간격을 0.05 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 9 | `x.mesh loc=2 spac=0.005` | x 방향 좌표 2 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 10 | `x.mesh loc=2.005 spac=0.005` | x 방향 좌표 2.005 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 11 | `x.mesh loc=3 spac=0.15` | x 방향 좌표 3 µm에서 목표 격자 간격을 0.15 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 12 | `y.mesh loc=-0.098000 spac=0.02` | y 방향 좌표 -0.098000 µm에서 목표 격자 간격을 0.02 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 13 | `y.mesh loc=-0.018000 spac=0.0005` | y 방향 좌표 -0.018000 µm에서 목표 격자 간격을 0.0005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 14 | `y.mesh loc=-0.010000 spac=0.0004` | y 방향 좌표 -0.010000 µm에서 목표 격자 간격을 0.0004 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 15 | `y.mesh loc=-0.003000 spac=0.0002` | y 방향 좌표 -0.003000 µm에서 목표 격자 간격을 0.0002 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 16 | `y.mesh loc=0.000000 spac=0.00015` | y 방향 좌표 0.000000 µm에서 목표 격자 간격을 0.00015 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 17 | `y.mesh loc=0.010000 spac=0.002` | y 방향 좌표 0.010000 µm에서 목표 격자 간격을 0.002 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 18 | `y.mesh loc=0.030000 spac=0.004` | y 방향 좌표 0.030000 µm에서 목표 격자 간격을 0.004 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 19 | `y.mesh loc=0.100000 spac=0.012` | y 방향 좌표 0.100000 µm에서 목표 격자 간격을 0.012 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 20 | `y.mesh loc=0.400000 spac=0.05` | y 방향 좌표 0.400000 µm에서 목표 격자 간격을 0.05 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 21 | `region num=1 material=air` | 1번 영역은 배경 공기이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 22 | `region num=2 material=conductor x.min=1 x.max=2 y.min=-0.098000 y.max=-0.018000` | 2번 영역은 도체 게이트이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 23 | `region num=3 material=Al2O3 x.min=1 x.max=2 y.min=-0.018000 y.max=-0.010000` | 3번 영역은 상부 차단 절연막이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 24 | `region num=4 material=nitride x.min=1 x.max=2 y.min=-0.010000 y.max=-0.003000` | 4번 영역은 질화막 전하 저장층이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 25 | `region num=5 material=oxide x.min=1 x.max=2 y.min=-0.003 y.max=0` | 5번 영역은 채널 쪽 SiO₂ 터널막이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 26 | `region num=6 material=silicon y.min=0` | 6번 영역은 Si 기판 및 채널이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 27 | `electrode name=cgate x.min=1 x.max=2 y.min=-0.098000 y.max=-0.018000` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 28 | `electrode name=source x.min=0 x.max=0.666667 y.min=0 y.max=0` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 29 | `electrode name=drain x.min=2.333333 x.max=3 y.min=0 y.max=0` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 30 | `electrode name=substrate bottom` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 31 | `doping uniform p.type conc=1e17 reg=6` | Si(6번)에 균일 p형 배경 도핑 10¹⁷ cm⁻³을 지정한다. |
| 32 | `doping gauss n.type conc=5e20 char=0.03 lat.char=0.005 reg=6 x.r=0.995` | Si에 n형 Gaussian 소스/드레인을 만든다. conc는 피크 농도(cm⁻³), char와 lat.char는 수직·수평 특성 길이(µm), x.r/x.l은 도핑 창 경계다. |
| 33 | `doping gauss n.type conc=5e20 char=0.03 lat.char=0.005 reg=6 x.l=2.005` | Si에 n형 Gaussian 소스/드레인을 만든다. conc는 피크 농도(cm⁻³), char와 lat.char는 수직·수평 특성 길이(µm), x.r/x.l은 도핑 창 경계다. |
| 34 | `material material=nitride permittivity=7.5 eg300=5.1 affinity=2.05 egalpha=0` | 비유전율 permittivity, 300 K 밴드갭 eg300(eV), 전자친화도 affinity(eV), 온도 계수 egalpha를 지정한다. 읽기 덱은 이 층을 유전체로 취급한다. |
| 35 | `material material=oxide permittivity=3.9 eg300=9.0 affinity=0.95 egalpha=0` | 비유전율 permittivity, 300 K 밴드갭 eg300(eV), 전자친화도 affinity(eV), 온도 계수 egalpha를 지정한다. 읽기 덱은 이 층을 유전체로 취급한다. |
| 36 | `material material=Al2O3 permittivity=9.3 eg300=8.0 affinity=1.50 egalpha=0` | 비유전율 permittivity, 300 K 밴드갭 eg300(eV), 전자친화도 affinity(eV), 온도 계수 egalpha를 지정한다. 읽기 덱은 이 층을 유전체로 취급한다. |
| 37 | `interface qf=-1242079487506.54 x.min=1 x.max=2 y.min=-0.00001 y.max=0.00001` | 게이트 아래 y=0 계면에 Python의 위치 가중 ΔVt와 등가인 부호 있는 고정전하 밀도 qf(cm⁻²)를 준다. 읽는 동안 고정된다. |
| 38 | `contact name=cgate workf=4.60` | 게이트의 유효 일함수 workf(eV)를 지정한다. SONOS 4.05, TANOS·TANS 4.60이다. |
| 39 | `models srh temp=77 print` | SRH 재결합과 격자 온도 77 K를 지정하고 모델을 출력한다. |
| 40 | `models region=6 fermidirac incomplete ioniz analytic bbt.kl print` | Si 영역에 Fermi–Dirac 통계, 불완전 이온화, 고농도 Si 이온화 보정, analytic 이동도 모델을 지정한다. bbt.kl이 있으면 국소 Klaassen BTBT도 활성화한다. print는 활성 모델을 출력한다. |
| 41 | `method newton carriers=2` | Newton 방법으로 전자·정공 연속방정식과 전위를 푼다. 기준 덱의 dt.min은 허용하는 최소 과도 시간 간격(s)이다. |
| 42 | `probe name=bbt_drain r.bbt x=2.005 y=0.001` | 드레인 쪽 지정 Si 좌표(µm)에서 국소 BTBT율을 로그에 기록한다. 공간 최대값은 .str의 U.BBT 분포를 본다. |
| 43 | `output con.band val.band qfn qfp band.param e.field u.bbt` | 저장 구조에 전도대·가전자대, 전자·정공 준페르미 준위, 재료 밴드 매개변수, 전계, BTBT율을 요청한다. 기준 덱의 sonos.rates는 질화막 주입·포획 속도도 요청한다. |
| 44 | `solve init` | 현재 전하와 물성으로 단자 0 V 초기 해를 구한다. |
| 45 | `log outf=TANOS_77K_program_hold_bias.log` | 이후 수렴한 점의 단자 전압·전류와 probe 값을 outf에 기록한다. |
| 46 | `solve vcgate=0` | 지정한 단자의 전압(V)에서 DC 해를 구한다. 다른 단자는 이전 바이어스를 유지한다. |
| 47 | `solve name=cgate vstep=0.05 vfinal=16` | name 전극의 전압을 vstep(V)씩 바꿔 vfinal(V)까지 DC 해를 구한다. BIAS 덱에서는 끝상태 qf가 램프 내내 고정된다. |
| 48 | `log off` | 열린 전기적 로그를 닫는다. |
| 49 | `save outf=TANOS_77K_program_hold.str` | 바로 앞에서 수렴한 구조와 물리량을 outf 이름의 TonyPlot 구조 파일에 기록한다. |
| 50 | `` | 실행 블록을 구분하는 빈 줄. |
| 51 | `# TANOS_77K_erase_hold. Reference geometry, uncalibrated parameters.` | 파일 용도 또는 매개변수 가정에 관한 주석. |
| 52 | `go atlas` | 새 ATLAS 세션을 시작한다. 다음 상태의 전극과 전하는 이 세션에서 다시 정의한다. |
| 53 | `title TANOS_77K_erase_hold` | 실행 결과를 식별할 제목을 정한다. |
| 54 | `mesh width=1` | 2차원 단면의 지면 수직 방향 폭을 1 µm로 설정한다. |
| 55 | `x.mesh loc=0 spac=0.15` | x 방향 좌표 0 µm에서 목표 격자 간격을 0.15 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 56 | `x.mesh loc=0.995 spac=0.005` | x 방향 좌표 0.995 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 57 | `x.mesh loc=1 spac=0.005` | x 방향 좌표 1 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 58 | `x.mesh loc=1.5 spac=0.05` | x 방향 좌표 1.5 µm에서 목표 격자 간격을 0.05 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 59 | `x.mesh loc=2 spac=0.005` | x 방향 좌표 2 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 60 | `x.mesh loc=2.005 spac=0.005` | x 방향 좌표 2.005 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 61 | `x.mesh loc=3 spac=0.15` | x 방향 좌표 3 µm에서 목표 격자 간격을 0.15 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 62 | `y.mesh loc=-0.098000 spac=0.02` | y 방향 좌표 -0.098000 µm에서 목표 격자 간격을 0.02 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 63 | `y.mesh loc=-0.018000 spac=0.0005` | y 방향 좌표 -0.018000 µm에서 목표 격자 간격을 0.0005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 64 | `y.mesh loc=-0.010000 spac=0.0004` | y 방향 좌표 -0.010000 µm에서 목표 격자 간격을 0.0004 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 65 | `y.mesh loc=-0.003000 spac=0.0002` | y 방향 좌표 -0.003000 µm에서 목표 격자 간격을 0.0002 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 66 | `y.mesh loc=0.000000 spac=0.00015` | y 방향 좌표 0.000000 µm에서 목표 격자 간격을 0.00015 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 67 | `y.mesh loc=0.010000 spac=0.002` | y 방향 좌표 0.010000 µm에서 목표 격자 간격을 0.002 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 68 | `y.mesh loc=0.030000 spac=0.004` | y 방향 좌표 0.030000 µm에서 목표 격자 간격을 0.004 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 69 | `y.mesh loc=0.100000 spac=0.012` | y 방향 좌표 0.100000 µm에서 목표 격자 간격을 0.012 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 70 | `y.mesh loc=0.400000 spac=0.05` | y 방향 좌표 0.400000 µm에서 목표 격자 간격을 0.05 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 71 | `region num=1 material=air` | 1번 영역은 배경 공기이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 72 | `region num=2 material=conductor x.min=1 x.max=2 y.min=-0.098000 y.max=-0.018000` | 2번 영역은 도체 게이트이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 73 | `region num=3 material=Al2O3 x.min=1 x.max=2 y.min=-0.018000 y.max=-0.010000` | 3번 영역은 상부 차단 절연막이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 74 | `region num=4 material=nitride x.min=1 x.max=2 y.min=-0.010000 y.max=-0.003000` | 4번 영역은 질화막 전하 저장층이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 75 | `region num=5 material=oxide x.min=1 x.max=2 y.min=-0.003 y.max=0` | 5번 영역은 채널 쪽 SiO₂ 터널막이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 76 | `region num=6 material=silicon y.min=0` | 6번 영역은 Si 기판 및 채널이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 77 | `electrode name=cgate x.min=1 x.max=2 y.min=-0.098000 y.max=-0.018000` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 78 | `electrode name=source x.min=0 x.max=0.666667 y.min=0 y.max=0` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 79 | `electrode name=drain x.min=2.333333 x.max=3 y.min=0 y.max=0` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 80 | `electrode name=substrate bottom` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 81 | `doping uniform p.type conc=1e17 reg=6` | Si(6번)에 균일 p형 배경 도핑 10¹⁷ cm⁻³을 지정한다. |
| 82 | `doping gauss n.type conc=5e20 char=0.03 lat.char=0.005 reg=6 x.r=0.995` | Si에 n형 Gaussian 소스/드레인을 만든다. conc는 피크 농도(cm⁻³), char와 lat.char는 수직·수평 특성 길이(µm), x.r/x.l은 도핑 창 경계다. |
| 83 | `doping gauss n.type conc=5e20 char=0.03 lat.char=0.005 reg=6 x.l=2.005` | Si에 n형 Gaussian 소스/드레인을 만든다. conc는 피크 농도(cm⁻³), char와 lat.char는 수직·수평 특성 길이(µm), x.r/x.l은 도핑 창 경계다. |
| 84 | `material material=nitride permittivity=7.5 eg300=5.1 affinity=2.05 egalpha=0` | 비유전율 permittivity, 300 K 밴드갭 eg300(eV), 전자친화도 affinity(eV), 온도 계수 egalpha를 지정한다. 읽기 덱은 이 층을 유전체로 취급한다. |
| 85 | `material material=oxide permittivity=3.9 eg300=9.0 affinity=0.95 egalpha=0` | 비유전율 permittivity, 300 K 밴드갭 eg300(eV), 전자친화도 affinity(eV), 온도 계수 egalpha를 지정한다. 읽기 덱은 이 층을 유전체로 취급한다. |
| 86 | `material material=Al2O3 permittivity=9.3 eg300=8.0 affinity=1.50 egalpha=0` | 비유전율 permittivity, 300 K 밴드갭 eg300(eV), 전자친화도 affinity(eV), 온도 계수 egalpha를 지정한다. 읽기 덱은 이 층을 유전체로 취급한다. |
| 87 | `interface qf=-35.2245081817158 x.min=1 x.max=2 y.min=-0.00001 y.max=0.00001` | 게이트 아래 y=0 계면에 Python의 위치 가중 ΔVt와 등가인 부호 있는 고정전하 밀도 qf(cm⁻²)를 준다. 읽는 동안 고정된다. |
| 88 | `contact name=cgate workf=4.60` | 게이트의 유효 일함수 workf(eV)를 지정한다. SONOS 4.05, TANOS·TANS 4.60이다. |
| 89 | `models srh temp=77 print` | SRH 재결합과 격자 온도 77 K를 지정하고 모델을 출력한다. |
| 90 | `models region=6 fermidirac incomplete ioniz analytic bbt.kl print` | Si 영역에 Fermi–Dirac 통계, 불완전 이온화, 고농도 Si 이온화 보정, analytic 이동도 모델을 지정한다. bbt.kl이 있으면 국소 Klaassen BTBT도 활성화한다. print는 활성 모델을 출력한다. |
| 91 | `method newton carriers=2` | Newton 방법으로 전자·정공 연속방정식과 전위를 푼다. 기준 덱의 dt.min은 허용하는 최소 과도 시간 간격(s)이다. |
| 92 | `probe name=bbt_drain r.bbt x=2.005 y=0.001` | 드레인 쪽 지정 Si 좌표(µm)에서 국소 BTBT율을 로그에 기록한다. 공간 최대값은 .str의 U.BBT 분포를 본다. |
| 93 | `output con.band val.band qfn qfp band.param e.field u.bbt` | 저장 구조에 전도대·가전자대, 전자·정공 준페르미 준위, 재료 밴드 매개변수, 전계, BTBT율을 요청한다. 기준 덱의 sonos.rates는 질화막 주입·포획 속도도 요청한다. |
| 94 | `solve init` | 현재 전하와 물성으로 단자 0 V 초기 해를 구한다. |
| 95 | `log outf=TANOS_77K_erase_hold_bias.log` | 이후 수렴한 점의 단자 전압·전류와 probe 값을 outf에 기록한다. |
| 96 | `solve vcgate=0` | 지정한 단자의 전압(V)에서 DC 해를 구한다. 다른 단자는 이전 바이어스를 유지한다. |
| 97 | `solve name=cgate vstep=-0.05 vfinal=-12` | name 전극의 전압을 vstep(V)씩 바꿔 vfinal(V)까지 DC 해를 구한다. BIAS 덱에서는 끝상태 qf가 램프 내내 고정된다. |
| 98 | `log off` | 열린 전기적 로그를 닫는다. |
| 99 | `save outf=TANOS_77K_erase_hold.str` | 바로 앞에서 수렴한 구조와 물리량을 outf 이름의 TonyPlot 구조 파일에 기록한다. |
| 100 | `quit` | DeckBuild 입력의 실행을 끝낸다. |

## generated/BIAS_TANS.in

| 줄 | 실제 명령 | 요소와 역할 |
|---:|---|---|
| 1 | `# TANS_77K_program_hold. Reference geometry, uncalibrated parameters.` | 파일 용도 또는 매개변수 가정에 관한 주석. |
| 2 | `go atlas` | 새 ATLAS 세션을 시작한다. 다음 상태의 전극과 전하는 이 세션에서 다시 정의한다. |
| 3 | `title TANS_77K_program_hold` | 실행 결과를 식별할 제목을 정한다. |
| 4 | `mesh width=1` | 2차원 단면의 지면 수직 방향 폭을 1 µm로 설정한다. |
| 5 | `x.mesh loc=0 spac=0.15` | x 방향 좌표 0 µm에서 목표 격자 간격을 0.15 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 6 | `x.mesh loc=0.995 spac=0.005` | x 방향 좌표 0.995 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 7 | `x.mesh loc=1 spac=0.005` | x 방향 좌표 1 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 8 | `x.mesh loc=1.5 spac=0.05` | x 방향 좌표 1.5 µm에서 목표 격자 간격을 0.05 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 9 | `x.mesh loc=2 spac=0.005` | x 방향 좌표 2 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 10 | `x.mesh loc=2.005 spac=0.005` | x 방향 좌표 2.005 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 11 | `x.mesh loc=3 spac=0.15` | x 방향 좌표 3 µm에서 목표 격자 간격을 0.15 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 12 | `y.mesh loc=-0.095000 spac=0.02` | y 방향 좌표 -0.095000 µm에서 목표 격자 간격을 0.02 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 13 | `y.mesh loc=-0.015000 spac=0.0005` | y 방향 좌표 -0.015000 µm에서 목표 격자 간격을 0.0005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 14 | `y.mesh loc=-0.007000 spac=0.0004` | y 방향 좌표 -0.007000 µm에서 목표 격자 간격을 0.0004 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 15 | `y.mesh loc=0.000000 spac=0.00015` | y 방향 좌표 0.000000 µm에서 목표 격자 간격을 0.00015 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 16 | `y.mesh loc=0.010000 spac=0.002` | y 방향 좌표 0.010000 µm에서 목표 격자 간격을 0.002 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 17 | `y.mesh loc=0.030000 spac=0.004` | y 방향 좌표 0.030000 µm에서 목표 격자 간격을 0.004 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 18 | `y.mesh loc=0.100000 spac=0.012` | y 방향 좌표 0.100000 µm에서 목표 격자 간격을 0.012 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 19 | `y.mesh loc=0.400000 spac=0.05` | y 방향 좌표 0.400000 µm에서 목표 격자 간격을 0.05 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 20 | `region num=1 material=air` | 1번 영역은 배경 공기이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 21 | `region num=2 material=conductor x.min=1 x.max=2 y.min=-0.095000 y.max=-0.015000` | 2번 영역은 도체 게이트이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 22 | `region num=3 material=Al2O3 x.min=1 x.max=2 y.min=-0.015000 y.max=-0.007000` | 3번 영역은 상부 차단 절연막이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 23 | `region num=4 material=nitride x.min=1 x.max=2 y.min=-0.007000 y.max=0.000000` | 4번 영역은 질화막 전하 저장층이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 24 | `region num=6 material=silicon y.min=0` | 6번 영역은 Si 기판 및 채널이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 25 | `electrode name=cgate x.min=1 x.max=2 y.min=-0.095000 y.max=-0.015000` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 26 | `electrode name=source x.min=0 x.max=0.666667 y.min=0 y.max=0` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 27 | `electrode name=drain x.min=2.333333 x.max=3 y.min=0 y.max=0` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 28 | `electrode name=substrate bottom` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 29 | `doping uniform p.type conc=1e17 reg=6` | Si(6번)에 균일 p형 배경 도핑 10¹⁷ cm⁻³을 지정한다. |
| 30 | `doping gauss n.type conc=5e20 char=0.03 lat.char=0.005 reg=6 x.r=0.995` | Si에 n형 Gaussian 소스/드레인을 만든다. conc는 피크 농도(cm⁻³), char와 lat.char는 수직·수평 특성 길이(µm), x.r/x.l은 도핑 창 경계다. |
| 31 | `doping gauss n.type conc=5e20 char=0.03 lat.char=0.005 reg=6 x.l=2.005` | Si에 n형 Gaussian 소스/드레인을 만든다. conc는 피크 농도(cm⁻³), char와 lat.char는 수직·수평 특성 길이(µm), x.r/x.l은 도핑 창 경계다. |
| 32 | `material material=nitride permittivity=7.5 eg300=5.1 affinity=2.05 egalpha=0` | 비유전율 permittivity, 300 K 밴드갭 eg300(eV), 전자친화도 affinity(eV), 온도 계수 egalpha를 지정한다. 읽기 덱은 이 층을 유전체로 취급한다. |
| 33 | `material material=Al2O3 permittivity=9.3 eg300=8.0 affinity=1.50 egalpha=0` | 비유전율 permittivity, 300 K 밴드갭 eg300(eV), 전자친화도 affinity(eV), 온도 계수 egalpha를 지정한다. 읽기 덱은 이 층을 유전체로 취급한다. |
| 34 | `interface qf=-2360815.09108419 x.min=1 x.max=2 y.min=-0.00001 y.max=0.00001` | 게이트 아래 y=0 계면에 Python의 위치 가중 ΔVt와 등가인 부호 있는 고정전하 밀도 qf(cm⁻²)를 준다. 읽는 동안 고정된다. |
| 35 | `contact name=cgate workf=4.60` | 게이트의 유효 일함수 workf(eV)를 지정한다. SONOS 4.05, TANOS·TANS 4.60이다. |
| 36 | `models srh temp=77 print` | SRH 재결합과 격자 온도 77 K를 지정하고 모델을 출력한다. |
| 37 | `models region=6 fermidirac incomplete ioniz analytic bbt.kl print` | Si 영역에 Fermi–Dirac 통계, 불완전 이온화, 고농도 Si 이온화 보정, analytic 이동도 모델을 지정한다. bbt.kl이 있으면 국소 Klaassen BTBT도 활성화한다. print는 활성 모델을 출력한다. |
| 38 | `method newton carriers=2` | Newton 방법으로 전자·정공 연속방정식과 전위를 푼다. 기준 덱의 dt.min은 허용하는 최소 과도 시간 간격(s)이다. |
| 39 | `probe name=bbt_drain r.bbt x=2.005 y=0.001` | 드레인 쪽 지정 Si 좌표(µm)에서 국소 BTBT율을 로그에 기록한다. 공간 최대값은 .str의 U.BBT 분포를 본다. |
| 40 | `output con.band val.band qfn qfp band.param e.field u.bbt` | 저장 구조에 전도대·가전자대, 전자·정공 준페르미 준위, 재료 밴드 매개변수, 전계, BTBT율을 요청한다. 기준 덱의 sonos.rates는 질화막 주입·포획 속도도 요청한다. |
| 41 | `solve init` | 현재 전하와 물성으로 단자 0 V 초기 해를 구한다. |
| 42 | `log outf=TANS_77K_program_hold_bias.log` | 이후 수렴한 점의 단자 전압·전류와 probe 값을 outf에 기록한다. |
| 43 | `solve vcgate=0` | 지정한 단자의 전압(V)에서 DC 해를 구한다. 다른 단자는 이전 바이어스를 유지한다. |
| 44 | `solve name=cgate vstep=0.05 vfinal=16` | name 전극의 전압을 vstep(V)씩 바꿔 vfinal(V)까지 DC 해를 구한다. BIAS 덱에서는 끝상태 qf가 램프 내내 고정된다. |
| 45 | `log off` | 열린 전기적 로그를 닫는다. |
| 46 | `save outf=TANS_77K_program_hold.str` | 바로 앞에서 수렴한 구조와 물리량을 outf 이름의 TonyPlot 구조 파일에 기록한다. |
| 47 | `` | 실행 블록을 구분하는 빈 줄. |
| 48 | `# TANS_77K_erase_hold. Reference geometry, uncalibrated parameters.` | 파일 용도 또는 매개변수 가정에 관한 주석. |
| 49 | `go atlas` | 새 ATLAS 세션을 시작한다. 다음 상태의 전극과 전하는 이 세션에서 다시 정의한다. |
| 50 | `title TANS_77K_erase_hold` | 실행 결과를 식별할 제목을 정한다. |
| 51 | `mesh width=1` | 2차원 단면의 지면 수직 방향 폭을 1 µm로 설정한다. |
| 52 | `x.mesh loc=0 spac=0.15` | x 방향 좌표 0 µm에서 목표 격자 간격을 0.15 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 53 | `x.mesh loc=0.995 spac=0.005` | x 방향 좌표 0.995 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 54 | `x.mesh loc=1 spac=0.005` | x 방향 좌표 1 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 55 | `x.mesh loc=1.5 spac=0.05` | x 방향 좌표 1.5 µm에서 목표 격자 간격을 0.05 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 56 | `x.mesh loc=2 spac=0.005` | x 방향 좌표 2 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 57 | `x.mesh loc=2.005 spac=0.005` | x 방향 좌표 2.005 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 58 | `x.mesh loc=3 spac=0.15` | x 방향 좌표 3 µm에서 목표 격자 간격을 0.15 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 59 | `y.mesh loc=-0.095000 spac=0.02` | y 방향 좌표 -0.095000 µm에서 목표 격자 간격을 0.02 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 60 | `y.mesh loc=-0.015000 spac=0.0005` | y 방향 좌표 -0.015000 µm에서 목표 격자 간격을 0.0005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 61 | `y.mesh loc=-0.007000 spac=0.0004` | y 방향 좌표 -0.007000 µm에서 목표 격자 간격을 0.0004 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 62 | `y.mesh loc=0.000000 spac=0.00015` | y 방향 좌표 0.000000 µm에서 목표 격자 간격을 0.00015 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 63 | `y.mesh loc=0.010000 spac=0.002` | y 방향 좌표 0.010000 µm에서 목표 격자 간격을 0.002 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 64 | `y.mesh loc=0.030000 spac=0.004` | y 방향 좌표 0.030000 µm에서 목표 격자 간격을 0.004 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 65 | `y.mesh loc=0.100000 spac=0.012` | y 방향 좌표 0.100000 µm에서 목표 격자 간격을 0.012 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 66 | `y.mesh loc=0.400000 spac=0.05` | y 방향 좌표 0.400000 µm에서 목표 격자 간격을 0.05 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 67 | `region num=1 material=air` | 1번 영역은 배경 공기이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 68 | `region num=2 material=conductor x.min=1 x.max=2 y.min=-0.095000 y.max=-0.015000` | 2번 영역은 도체 게이트이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 69 | `region num=3 material=Al2O3 x.min=1 x.max=2 y.min=-0.015000 y.max=-0.007000` | 3번 영역은 상부 차단 절연막이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 70 | `region num=4 material=nitride x.min=1 x.max=2 y.min=-0.007000 y.max=0.000000` | 4번 영역은 질화막 전하 저장층이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 71 | `region num=6 material=silicon y.min=0` | 6번 영역은 Si 기판 및 채널이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 72 | `electrode name=cgate x.min=1 x.max=2 y.min=-0.095000 y.max=-0.015000` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 73 | `electrode name=source x.min=0 x.max=0.666667 y.min=0 y.max=0` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 74 | `electrode name=drain x.min=2.333333 x.max=3 y.min=0 y.max=0` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 75 | `electrode name=substrate bottom` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 76 | `doping uniform p.type conc=1e17 reg=6` | Si(6번)에 균일 p형 배경 도핑 10¹⁷ cm⁻³을 지정한다. |
| 77 | `doping gauss n.type conc=5e20 char=0.03 lat.char=0.005 reg=6 x.r=0.995` | Si에 n형 Gaussian 소스/드레인을 만든다. conc는 피크 농도(cm⁻³), char와 lat.char는 수직·수평 특성 길이(µm), x.r/x.l은 도핑 창 경계다. |
| 78 | `doping gauss n.type conc=5e20 char=0.03 lat.char=0.005 reg=6 x.l=2.005` | Si에 n형 Gaussian 소스/드레인을 만든다. conc는 피크 농도(cm⁻³), char와 lat.char는 수직·수평 특성 길이(µm), x.r/x.l은 도핑 창 경계다. |
| 79 | `material material=nitride permittivity=7.5 eg300=5.1 affinity=2.05 egalpha=0` | 비유전율 permittivity, 300 K 밴드갭 eg300(eV), 전자친화도 affinity(eV), 온도 계수 egalpha를 지정한다. 읽기 덱은 이 층을 유전체로 취급한다. |
| 80 | `material material=Al2O3 permittivity=9.3 eg300=8.0 affinity=1.50 egalpha=0` | 비유전율 permittivity, 300 K 밴드갭 eg300(eV), 전자친화도 affinity(eV), 온도 계수 egalpha를 지정한다. 읽기 덱은 이 층을 유전체로 취급한다. |
| 81 | `interface qf=854787309402.439 x.min=1 x.max=2 y.min=-0.00001 y.max=0.00001` | 게이트 아래 y=0 계면에 Python의 위치 가중 ΔVt와 등가인 부호 있는 고정전하 밀도 qf(cm⁻²)를 준다. 읽는 동안 고정된다. |
| 82 | `contact name=cgate workf=4.60` | 게이트의 유효 일함수 workf(eV)를 지정한다. SONOS 4.05, TANOS·TANS 4.60이다. |
| 83 | `models srh temp=77 print` | SRH 재결합과 격자 온도 77 K를 지정하고 모델을 출력한다. |
| 84 | `models region=6 fermidirac incomplete ioniz analytic bbt.kl print` | Si 영역에 Fermi–Dirac 통계, 불완전 이온화, 고농도 Si 이온화 보정, analytic 이동도 모델을 지정한다. bbt.kl이 있으면 국소 Klaassen BTBT도 활성화한다. print는 활성 모델을 출력한다. |
| 85 | `method newton carriers=2` | Newton 방법으로 전자·정공 연속방정식과 전위를 푼다. 기준 덱의 dt.min은 허용하는 최소 과도 시간 간격(s)이다. |
| 86 | `probe name=bbt_drain r.bbt x=2.005 y=0.001` | 드레인 쪽 지정 Si 좌표(µm)에서 국소 BTBT율을 로그에 기록한다. 공간 최대값은 .str의 U.BBT 분포를 본다. |
| 87 | `output con.band val.band qfn qfp band.param e.field u.bbt` | 저장 구조에 전도대·가전자대, 전자·정공 준페르미 준위, 재료 밴드 매개변수, 전계, BTBT율을 요청한다. 기준 덱의 sonos.rates는 질화막 주입·포획 속도도 요청한다. |
| 88 | `solve init` | 현재 전하와 물성으로 단자 0 V 초기 해를 구한다. |
| 89 | `log outf=TANS_77K_erase_hold_bias.log` | 이후 수렴한 점의 단자 전압·전류와 probe 값을 outf에 기록한다. |
| 90 | `solve vcgate=0` | 지정한 단자의 전압(V)에서 DC 해를 구한다. 다른 단자는 이전 바이어스를 유지한다. |
| 91 | `solve name=cgate vstep=-0.05 vfinal=-12` | name 전극의 전압을 vstep(V)씩 바꿔 vfinal(V)까지 DC 해를 구한다. BIAS 덱에서는 끝상태 qf가 램프 내내 고정된다. |
| 92 | `log off` | 열린 전기적 로그를 닫는다. |
| 93 | `save outf=TANS_77K_erase_hold.str` | 바로 앞에서 수렴한 구조와 물리량을 outf 이름의 TonyPlot 구조 파일에 기록한다. |
| 94 | `quit` | DeckBuild 입력의 실행을 끝낸다. |

## reference/SONOS_reference_PE.in

| 줄 | 실제 명령 | 요소와 역할 |
|---:|---|---|
| 1 | `# SONOS_reference_PE. Reference geometry, uncalibrated parameters.` | 파일 용도 또는 매개변수 가정에 관한 주석. |
| 2 | `go atlas` | 새 ATLAS 세션을 시작한다. 다음 상태의 전극과 전하는 이 세션에서 다시 정의한다. |
| 3 | `title SONOS_reference_PE` | 실행 결과를 식별할 제목을 정한다. |
| 4 | `mesh width=1` | 2차원 단면의 지면 수직 방향 폭을 1 µm로 설정한다. |
| 5 | `x.mesh loc=0 spac=0.15` | x 방향 좌표 0 µm에서 목표 격자 간격을 0.15 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 6 | `x.mesh loc=0.995 spac=0.005` | x 방향 좌표 0.995 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 7 | `x.mesh loc=1 spac=0.005` | x 방향 좌표 1 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 8 | `x.mesh loc=1.5 spac=0.05` | x 방향 좌표 1.5 µm에서 목표 격자 간격을 0.05 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 9 | `x.mesh loc=2 spac=0.005` | x 방향 좌표 2 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 10 | `x.mesh loc=2.005 spac=0.005` | x 방향 좌표 2.005 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 11 | `x.mesh loc=3 spac=0.15` | x 방향 좌표 3 µm에서 목표 격자 간격을 0.15 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 12 | `y.mesh loc=-0.098000 spac=0.02` | y 방향 좌표 -0.098000 µm에서 목표 격자 간격을 0.02 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 13 | `y.mesh loc=-0.018000 spac=0.0005` | y 방향 좌표 -0.018000 µm에서 목표 격자 간격을 0.0005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 14 | `y.mesh loc=-0.010000 spac=0.0004` | y 방향 좌표 -0.010000 µm에서 목표 격자 간격을 0.0004 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 15 | `y.mesh loc=-0.003000 spac=0.0002` | y 방향 좌표 -0.003000 µm에서 목표 격자 간격을 0.0002 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 16 | `y.mesh loc=0.000000 spac=0.00015` | y 방향 좌표 0.000000 µm에서 목표 격자 간격을 0.00015 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 17 | `y.mesh loc=0.010000 spac=0.002` | y 방향 좌표 0.010000 µm에서 목표 격자 간격을 0.002 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 18 | `y.mesh loc=0.030000 spac=0.004` | y 방향 좌표 0.030000 µm에서 목표 격자 간격을 0.004 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 19 | `y.mesh loc=0.100000 spac=0.012` | y 방향 좌표 0.100000 µm에서 목표 격자 간격을 0.012 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 20 | `y.mesh loc=0.400000 spac=0.05` | y 방향 좌표 0.400000 µm에서 목표 격자 간격을 0.05 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 21 | `region num=1 material=air` | 1번 영역은 배경 공기이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 22 | `region num=2 material=conductor x.min=1 x.max=2 y.min=-0.098000 y.max=-0.018000` | 2번 영역은 도체 게이트이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 23 | `region num=3 material=oxide x.min=1 x.max=2 y.min=-0.018000 y.max=-0.010000` | 3번 영역은 상부 차단 절연막이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 24 | `region num=4 material=nitride x.min=1 x.max=2 y.min=-0.010000 y.max=-0.003000` | 4번 영역은 질화막 전하 저장층이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 25 | `region num=5 material=oxide x.min=1 x.max=2 y.min=-0.003 y.max=0` | 5번 영역은 채널 쪽 SiO₂ 터널막이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 26 | `region num=6 material=silicon y.min=0` | 6번 영역은 Si 기판 및 채널이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 27 | `electrode name=cgate x.min=1 x.max=2 y.min=-0.098000 y.max=-0.018000` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 28 | `electrode name=source x.min=0 x.max=0.666667 y.min=0 y.max=0` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 29 | `electrode name=drain x.min=2.333333 x.max=3 y.min=0 y.max=0` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 30 | `electrode name=substrate bottom` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 31 | `doping uniform p.type conc=1e17 reg=6` | Si(6번)에 균일 p형 배경 도핑 10¹⁷ cm⁻³을 지정한다. |
| 32 | `doping gauss n.type conc=5e20 char=0.03 lat.char=0.005 reg=6 x.r=0.995` | Si에 n형 Gaussian 소스/드레인을 만든다. conc는 피크 농도(cm⁻³), char와 lat.char는 수직·수평 특성 길이(µm), x.r/x.l은 도핑 창 경계다. |
| 33 | `doping gauss n.type conc=5e20 char=0.03 lat.char=0.005 reg=6 x.l=2.005` | Si에 n형 Gaussian 소스/드레인을 만든다. conc는 피크 농도(cm⁻³), char와 lat.char는 수직·수평 특성 길이(µm), x.r/x.l은 도핑 창 경계다. |
| 34 | `interface n.i dynasonos` | 질화막–인접 절연막의 DYNASONOS 경계를 활성화한다. TANS의 하부는 Si/질화막 직접 접촉이다. |
| 35 | `material material=oxide eg300=9 egalpha=0 affinity=0.95 permittivity=3.9 semiconductor nc300=1e19 nv300=1e19 mc=0.3 mv=1 mun=0.1 mup=0.01 taun0=1 taup0=1` | 비유전율 permittivity, 300 K 밴드갭 eg300(eV), 전자친화도 affinity(eV), 온도 계수 egalpha를 지정한다. 기준 덱의 semiconductor는 절연막을 넓은 밴드갭 반도체로 풀게 한다. mc/mv는 유효질량비, nc300/nv300은 유효 상태밀도(cm⁻³), mun/mup은 이동도(cm²/Vs), taun0/taup0은 SRH 수명(s)이다. |
| 36 | `material material=nitride semiconductor eg300=5.1 egalpha=0 affinity=2.05 permittivity=7.5 nc300=1e19 nv300=1e19 mc=1 mv=1 mun=0.1 mup=0.01 taun0=1 taup0=1` | 비유전율 permittivity, 300 K 밴드갭 eg300(eV), 전자친화도 affinity(eV), 온도 계수 egalpha를 지정한다. 기준 덱의 semiconductor는 절연막을 넓은 밴드갭 반도체로 풀게 한다. mc/mv는 유효질량비, nc300/nv300은 유효 상태밀도(cm⁻³), mun/mup은 이동도(cm²/Vs), taun0/taup0은 SRH 수명(s)이다. |
| 37 | `# e/h depths and cross-sections are starting assumptions, not fitted data.` | 파일 용도 또는 매개변수 가정에 관한 주석. |
| 38 | `nitridecharge nt.n=1e19 nt.p=1e19 elec.depth=1.2 hole.depth=1.2 sigmat.n=1e-14 sigmat.p=1e-14 sigman.p=1e-16 sigmap.n=1e-16 pf.b=1e13` | nt.n/nt.p는 전자·정공 트랩 수(cm⁻³), depth는 깊이(eV), sigmat와 교차 sigman/sigmap은 포획 단면적(cm²), pf.b는 PF 시도율(s⁻¹)이다. |
| 39 | `contact name=cgate workf=4.05` | 게이트의 유효 일함수 workf(eV)를 지정한다. SONOS 4.05, TANOS·TANS 4.60이다. |
| 40 | `models srh temp=77 print pf.nitride` | SRH 재결합과 격자 온도 77 K를 지정하고 모델을 출력한다. pf.nitride는 질화막 PF 방출을 켠다. |
| 41 | `models region=6 fermidirac incomplete ioniz analytic bbt.kl print` | Si 영역에 Fermi–Dirac 통계, 불완전 이온화, 고농도 Si 이온화 보정, analytic 이동도 모델을 지정한다. bbt.kl이 있으면 국소 Klaassen BTBT도 활성화한다. print는 활성 모델을 출력한다. |
| 42 | `method newton carriers=2 dt.min=1e-14` | Newton 방법으로 전자·정공 연속방정식과 전위를 푼다. 기준 덱의 dt.min은 허용하는 최소 과도 시간 간격(s)이다. |
| 43 | `probe name=bbt_drain r.bbt x=2.005 y=0.001` | 드레인 쪽 지정 Si 좌표(µm)에서 국소 BTBT율을 로그에 기록한다. 공간 최대값은 .str의 U.BBT 분포를 본다. |
| 44 | `probe name=netcharge sonos.charge integrate x.min=1 x.max=2 y.min=-0.010000 y.max=-0.003000` | 게이트 아래 질화막 범위의 SONOS 트랩 전하를 적분해 과도 로그에 남긴다. |
| 45 | `output con.band val.band qfn qfp sonos.rates u.bbt e.field band.param` | 저장 구조에 전도대·가전자대, 전자·정공 준페르미 준위, 재료 밴드 매개변수, 전계, BTBT율을 요청한다. 기준 덱의 sonos.rates는 질화막 주입·포획 속도도 요청한다. |
| 46 | `solve init` | 현재 전하와 물성으로 단자 0 V 초기 해를 구한다. |
| 47 | `log outf=SONOS_reference_PE_pgm.log sonos.curr` | 이후 수렴한 점의 단자 전압·전류와 probe 값을 outf에 기록한다. sonos.curr는 SONOS 터널 전류 성분을 더한다. |
| 48 | `solve vcgate=16 ramptime=1E-9 tstep=1E-11 tstop=0.000000001` | 게이트 목표전압으로 선형 램프를 준다. ramptime은 램프 시간, tstep은 초기 시간 간격, tstop은 시뮬레이션 누적 종료 시각(s)이다. |
| 49 | `solve tstop=0.00000001` | 직전 단자 바이어스를 유지하며 지정한 누적 시간(s)까지 연속으로 적분한다. |
| 50 | `solve tstop=0.0000001` | 직전 단자 바이어스를 유지하며 지정한 누적 시간(s)까지 연속으로 적분한다. |
| 51 | `solve tstop=0.000001` | 직전 단자 바이어스를 유지하며 지정한 누적 시간(s)까지 연속으로 적분한다. |
| 52 | `solve tstop=0.00001` | 직전 단자 바이어스를 유지하며 지정한 누적 시간(s)까지 연속으로 적분한다. |
| 53 | `solve tstop=0.0001` | 직전 단자 바이어스를 유지하며 지정한 누적 시간(s)까지 연속으로 적분한다. |
| 54 | `solve vcgate=0 ramptime=1E-9 tstep=1E-11 tstop=0.000100001` | 게이트 목표전압으로 선형 램프를 준다. ramptime은 램프 시간, tstep은 초기 시간 간격, tstop은 시뮬레이션 누적 종료 시각(s)이다. |
| 55 | `log off` | 열린 전기적 로그를 닫는다. |
| 56 | `save outf=SONOS_reference_PE_pgm_zero.str` | 바로 앞에서 수렴한 구조와 물리량을 outf 이름의 TonyPlot 구조 파일에 기록한다. |
| 57 | `log outf=SONOS_reference_PE_ers.log sonos.curr` | 이후 수렴한 점의 단자 전압·전류와 probe 값을 outf에 기록한다. sonos.curr는 SONOS 터널 전류 성분을 더한다. |
| 58 | `solve vcgate=-12 ramptime=1E-9 tstep=1E-11 tstop=0.000100002` | 게이트 목표전압으로 선형 램프를 준다. ramptime은 램프 시간, tstep은 초기 시간 간격, tstop은 시뮬레이션 누적 종료 시각(s)이다. |
| 59 | `solve tstop=0.000100011` | 직전 단자 바이어스를 유지하며 지정한 누적 시간(s)까지 연속으로 적분한다. |
| 60 | `solve tstop=0.000100101` | 직전 단자 바이어스를 유지하며 지정한 누적 시간(s)까지 연속으로 적분한다. |
| 61 | `solve tstop=0.000101001` | 직전 단자 바이어스를 유지하며 지정한 누적 시간(s)까지 연속으로 적분한다. |
| 62 | `solve tstop=0.000110001` | 직전 단자 바이어스를 유지하며 지정한 누적 시간(s)까지 연속으로 적분한다. |
| 63 | `solve tstop=0.000600001` | 직전 단자 바이어스를 유지하며 지정한 누적 시간(s)까지 연속으로 적분한다. |
| 64 | `solve vcgate=0 ramptime=1E-9 tstep=1E-11 tstop=0.000600002` | 게이트 목표전압으로 선형 램프를 준다. ramptime은 램프 시간, tstep은 초기 시간 간격, tstop은 시뮬레이션 누적 종료 시각(s)이다. |
| 65 | `log off` | 열린 전기적 로그를 닫는다. |
| 66 | `save outf=SONOS_reference_PE_ers_zero.str` | 바로 앞에서 수렴한 구조와 물리량을 outf 이름의 TonyPlot 구조 파일에 기록한다. |
| 67 | `quit` | DeckBuild 입력의 실행을 끝낸다. |

## reference/TANOS_reference_PE.in

| 줄 | 실제 명령 | 요소와 역할 |
|---:|---|---|
| 1 | `# TANOS_reference_PE. Reference geometry, uncalibrated parameters.` | 파일 용도 또는 매개변수 가정에 관한 주석. |
| 2 | `go atlas` | 새 ATLAS 세션을 시작한다. 다음 상태의 전극과 전하는 이 세션에서 다시 정의한다. |
| 3 | `title TANOS_reference_PE` | 실행 결과를 식별할 제목을 정한다. |
| 4 | `mesh width=1` | 2차원 단면의 지면 수직 방향 폭을 1 µm로 설정한다. |
| 5 | `x.mesh loc=0 spac=0.15` | x 방향 좌표 0 µm에서 목표 격자 간격을 0.15 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 6 | `x.mesh loc=0.995 spac=0.005` | x 방향 좌표 0.995 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 7 | `x.mesh loc=1 spac=0.005` | x 방향 좌표 1 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 8 | `x.mesh loc=1.5 spac=0.05` | x 방향 좌표 1.5 µm에서 목표 격자 간격을 0.05 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 9 | `x.mesh loc=2 spac=0.005` | x 방향 좌표 2 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 10 | `x.mesh loc=2.005 spac=0.005` | x 방향 좌표 2.005 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 11 | `x.mesh loc=3 spac=0.15` | x 방향 좌표 3 µm에서 목표 격자 간격을 0.15 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 12 | `y.mesh loc=-0.098000 spac=0.02` | y 방향 좌표 -0.098000 µm에서 목표 격자 간격을 0.02 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 13 | `y.mesh loc=-0.018000 spac=0.0005` | y 방향 좌표 -0.018000 µm에서 목표 격자 간격을 0.0005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 14 | `y.mesh loc=-0.010000 spac=0.0004` | y 방향 좌표 -0.010000 µm에서 목표 격자 간격을 0.0004 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 15 | `y.mesh loc=-0.003000 spac=0.0002` | y 방향 좌표 -0.003000 µm에서 목표 격자 간격을 0.0002 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 16 | `y.mesh loc=0.000000 spac=0.00015` | y 방향 좌표 0.000000 µm에서 목표 격자 간격을 0.00015 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 17 | `y.mesh loc=0.010000 spac=0.002` | y 방향 좌표 0.010000 µm에서 목표 격자 간격을 0.002 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 18 | `y.mesh loc=0.030000 spac=0.004` | y 방향 좌표 0.030000 µm에서 목표 격자 간격을 0.004 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 19 | `y.mesh loc=0.100000 spac=0.012` | y 방향 좌표 0.100000 µm에서 목표 격자 간격을 0.012 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 20 | `y.mesh loc=0.400000 spac=0.05` | y 방향 좌표 0.400000 µm에서 목표 격자 간격을 0.05 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 21 | `region num=1 material=air` | 1번 영역은 배경 공기이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 22 | `region num=2 material=conductor x.min=1 x.max=2 y.min=-0.098000 y.max=-0.018000` | 2번 영역은 도체 게이트이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 23 | `region num=3 material=Al2O3 x.min=1 x.max=2 y.min=-0.018000 y.max=-0.010000` | 3번 영역은 상부 차단 절연막이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 24 | `region num=4 material=nitride x.min=1 x.max=2 y.min=-0.010000 y.max=-0.003000` | 4번 영역은 질화막 전하 저장층이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 25 | `region num=5 material=oxide x.min=1 x.max=2 y.min=-0.003 y.max=0` | 5번 영역은 채널 쪽 SiO₂ 터널막이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 26 | `region num=6 material=silicon y.min=0` | 6번 영역은 Si 기판 및 채널이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 27 | `electrode name=cgate x.min=1 x.max=2 y.min=-0.098000 y.max=-0.018000` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 28 | `electrode name=source x.min=0 x.max=0.666667 y.min=0 y.max=0` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 29 | `electrode name=drain x.min=2.333333 x.max=3 y.min=0 y.max=0` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 30 | `electrode name=substrate bottom` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 31 | `doping uniform p.type conc=1e17 reg=6` | Si(6번)에 균일 p형 배경 도핑 10¹⁷ cm⁻³을 지정한다. |
| 32 | `doping gauss n.type conc=5e20 char=0.03 lat.char=0.005 reg=6 x.r=0.995` | Si에 n형 Gaussian 소스/드레인을 만든다. conc는 피크 농도(cm⁻³), char와 lat.char는 수직·수평 특성 길이(µm), x.r/x.l은 도핑 창 경계다. |
| 33 | `doping gauss n.type conc=5e20 char=0.03 lat.char=0.005 reg=6 x.l=2.005` | Si에 n형 Gaussian 소스/드레인을 만든다. conc는 피크 농도(cm⁻³), char와 lat.char는 수직·수평 특성 길이(µm), x.r/x.l은 도핑 창 경계다. |
| 34 | `interface n.i dynasonos` | 질화막–인접 절연막의 DYNASONOS 경계를 활성화한다. TANS의 하부는 Si/질화막 직접 접촉이다. |
| 35 | `material material=Al2O3 eg300=8 egalpha=0 affinity=1.50 permittivity=9.3 semiconductor nc300=1e19 nv300=1e19 mc=0.3 mv=1 mun=0.1 mup=0.01 taun0=1 taup0=1` | 비유전율 permittivity, 300 K 밴드갭 eg300(eV), 전자친화도 affinity(eV), 온도 계수 egalpha를 지정한다. 기준 덱의 semiconductor는 절연막을 넓은 밴드갭 반도체로 풀게 한다. mc/mv는 유효질량비, nc300/nv300은 유효 상태밀도(cm⁻³), mun/mup은 이동도(cm²/Vs), taun0/taup0은 SRH 수명(s)이다. |
| 36 | `material material=oxide eg300=9 egalpha=0 affinity=0.95 permittivity=3.9 semiconductor nc300=1e19 nv300=1e19 mc=0.3 mv=1 mun=0.1 mup=0.01 taun0=1 taup0=1` | 비유전율 permittivity, 300 K 밴드갭 eg300(eV), 전자친화도 affinity(eV), 온도 계수 egalpha를 지정한다. 기준 덱의 semiconductor는 절연막을 넓은 밴드갭 반도체로 풀게 한다. mc/mv는 유효질량비, nc300/nv300은 유효 상태밀도(cm⁻³), mun/mup은 이동도(cm²/Vs), taun0/taup0은 SRH 수명(s)이다. |
| 37 | `material material=nitride semiconductor eg300=5.1 egalpha=0 affinity=2.05 permittivity=7.5 nc300=1e19 nv300=1e19 mc=1 mv=1 mun=0.1 mup=0.01 taun0=1 taup0=1` | 비유전율 permittivity, 300 K 밴드갭 eg300(eV), 전자친화도 affinity(eV), 온도 계수 egalpha를 지정한다. 기준 덱의 semiconductor는 절연막을 넓은 밴드갭 반도체로 풀게 한다. mc/mv는 유효질량비, nc300/nv300은 유효 상태밀도(cm⁻³), mun/mup은 이동도(cm²/Vs), taun0/taup0은 SRH 수명(s)이다. |
| 38 | `# e/h depths and cross-sections are starting assumptions, not fitted data.` | 파일 용도 또는 매개변수 가정에 관한 주석. |
| 39 | `nitridecharge nt.n=1e19 nt.p=1e19 elec.depth=1.2 hole.depth=1.2 sigmat.n=1e-14 sigmat.p=1e-14 sigman.p=1e-16 sigmap.n=1e-16 pf.b=1e13` | nt.n/nt.p는 전자·정공 트랩 수(cm⁻³), depth는 깊이(eV), sigmat와 교차 sigman/sigmap은 포획 단면적(cm²), pf.b는 PF 시도율(s⁻¹)이다. |
| 40 | `contact name=cgate workf=4.60` | 게이트의 유효 일함수 workf(eV)를 지정한다. SONOS 4.05, TANOS·TANS 4.60이다. |
| 41 | `models srh temp=77 print pf.nitride` | SRH 재결합과 격자 온도 77 K를 지정하고 모델을 출력한다. pf.nitride는 질화막 PF 방출을 켠다. |
| 42 | `models region=6 fermidirac incomplete ioniz analytic bbt.kl print` | Si 영역에 Fermi–Dirac 통계, 불완전 이온화, 고농도 Si 이온화 보정, analytic 이동도 모델을 지정한다. bbt.kl이 있으면 국소 Klaassen BTBT도 활성화한다. print는 활성 모델을 출력한다. |
| 43 | `method newton carriers=2 dt.min=1e-14` | Newton 방법으로 전자·정공 연속방정식과 전위를 푼다. 기준 덱의 dt.min은 허용하는 최소 과도 시간 간격(s)이다. |
| 44 | `probe name=bbt_drain r.bbt x=2.005 y=0.001` | 드레인 쪽 지정 Si 좌표(µm)에서 국소 BTBT율을 로그에 기록한다. 공간 최대값은 .str의 U.BBT 분포를 본다. |
| 45 | `probe name=netcharge sonos.charge integrate x.min=1 x.max=2 y.min=-0.010000 y.max=-0.003000` | 게이트 아래 질화막 범위의 SONOS 트랩 전하를 적분해 과도 로그에 남긴다. |
| 46 | `output con.band val.band qfn qfp sonos.rates u.bbt e.field band.param` | 저장 구조에 전도대·가전자대, 전자·정공 준페르미 준위, 재료 밴드 매개변수, 전계, BTBT율을 요청한다. 기준 덱의 sonos.rates는 질화막 주입·포획 속도도 요청한다. |
| 47 | `solve init` | 현재 전하와 물성으로 단자 0 V 초기 해를 구한다. |
| 48 | `log outf=TANOS_reference_PE_pgm.log sonos.curr` | 이후 수렴한 점의 단자 전압·전류와 probe 값을 outf에 기록한다. sonos.curr는 SONOS 터널 전류 성분을 더한다. |
| 49 | `solve vcgate=16 ramptime=1E-9 tstep=1E-11 tstop=0.000000001` | 게이트 목표전압으로 선형 램프를 준다. ramptime은 램프 시간, tstep은 초기 시간 간격, tstop은 시뮬레이션 누적 종료 시각(s)이다. |
| 50 | `solve tstop=0.00000001` | 직전 단자 바이어스를 유지하며 지정한 누적 시간(s)까지 연속으로 적분한다. |
| 51 | `solve tstop=0.0000001` | 직전 단자 바이어스를 유지하며 지정한 누적 시간(s)까지 연속으로 적분한다. |
| 52 | `solve tstop=0.000001` | 직전 단자 바이어스를 유지하며 지정한 누적 시간(s)까지 연속으로 적분한다. |
| 53 | `solve tstop=0.00001` | 직전 단자 바이어스를 유지하며 지정한 누적 시간(s)까지 연속으로 적분한다. |
| 54 | `solve tstop=0.0001` | 직전 단자 바이어스를 유지하며 지정한 누적 시간(s)까지 연속으로 적분한다. |
| 55 | `solve vcgate=0 ramptime=1E-9 tstep=1E-11 tstop=0.000100001` | 게이트 목표전압으로 선형 램프를 준다. ramptime은 램프 시간, tstep은 초기 시간 간격, tstop은 시뮬레이션 누적 종료 시각(s)이다. |
| 56 | `log off` | 열린 전기적 로그를 닫는다. |
| 57 | `save outf=TANOS_reference_PE_pgm_zero.str` | 바로 앞에서 수렴한 구조와 물리량을 outf 이름의 TonyPlot 구조 파일에 기록한다. |
| 58 | `log outf=TANOS_reference_PE_ers.log sonos.curr` | 이후 수렴한 점의 단자 전압·전류와 probe 값을 outf에 기록한다. sonos.curr는 SONOS 터널 전류 성분을 더한다. |
| 59 | `solve vcgate=-12 ramptime=1E-9 tstep=1E-11 tstop=0.000100002` | 게이트 목표전압으로 선형 램프를 준다. ramptime은 램프 시간, tstep은 초기 시간 간격, tstop은 시뮬레이션 누적 종료 시각(s)이다. |
| 60 | `solve tstop=0.000100011` | 직전 단자 바이어스를 유지하며 지정한 누적 시간(s)까지 연속으로 적분한다. |
| 61 | `solve tstop=0.000100101` | 직전 단자 바이어스를 유지하며 지정한 누적 시간(s)까지 연속으로 적분한다. |
| 62 | `solve tstop=0.000101001` | 직전 단자 바이어스를 유지하며 지정한 누적 시간(s)까지 연속으로 적분한다. |
| 63 | `solve tstop=0.000110001` | 직전 단자 바이어스를 유지하며 지정한 누적 시간(s)까지 연속으로 적분한다. |
| 64 | `solve tstop=0.000600001` | 직전 단자 바이어스를 유지하며 지정한 누적 시간(s)까지 연속으로 적분한다. |
| 65 | `solve vcgate=0 ramptime=1E-9 tstep=1E-11 tstop=0.000600002` | 게이트 목표전압으로 선형 램프를 준다. ramptime은 램프 시간, tstep은 초기 시간 간격, tstop은 시뮬레이션 누적 종료 시각(s)이다. |
| 66 | `log off` | 열린 전기적 로그를 닫는다. |
| 67 | `save outf=TANOS_reference_PE_ers_zero.str` | 바로 앞에서 수렴한 구조와 물리량을 outf 이름의 TonyPlot 구조 파일에 기록한다. |
| 68 | `quit` | DeckBuild 입력의 실행을 끝낸다. |

## reference/TANS_reference_PE.in

| 줄 | 실제 명령 | 요소와 역할 |
|---:|---|---|
| 1 | `# TANS_reference_PE. Reference geometry, uncalibrated parameters.` | 파일 용도 또는 매개변수 가정에 관한 주석. |
| 2 | `go atlas` | 새 ATLAS 세션을 시작한다. 다음 상태의 전극과 전하는 이 세션에서 다시 정의한다. |
| 3 | `title TANS_reference_PE` | 실행 결과를 식별할 제목을 정한다. |
| 4 | `mesh width=1` | 2차원 단면의 지면 수직 방향 폭을 1 µm로 설정한다. |
| 5 | `x.mesh loc=0 spac=0.15` | x 방향 좌표 0 µm에서 목표 격자 간격을 0.15 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 6 | `x.mesh loc=0.995 spac=0.005` | x 방향 좌표 0.995 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 7 | `x.mesh loc=1 spac=0.005` | x 방향 좌표 1 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 8 | `x.mesh loc=1.5 spac=0.05` | x 방향 좌표 1.5 µm에서 목표 격자 간격을 0.05 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 9 | `x.mesh loc=2 spac=0.005` | x 방향 좌표 2 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 10 | `x.mesh loc=2.005 spac=0.005` | x 방향 좌표 2.005 µm에서 목표 격자 간격을 0.005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 11 | `x.mesh loc=3 spac=0.15` | x 방향 좌표 3 µm에서 목표 격자 간격을 0.15 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 12 | `y.mesh loc=-0.095000 spac=0.02` | y 방향 좌표 -0.095000 µm에서 목표 격자 간격을 0.02 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 13 | `y.mesh loc=-0.015000 spac=0.0005` | y 방향 좌표 -0.015000 µm에서 목표 격자 간격을 0.0005 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 14 | `y.mesh loc=-0.007000 spac=0.0004` | y 방향 좌표 -0.007000 µm에서 목표 격자 간격을 0.0004 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 15 | `y.mesh loc=0.000000 spac=0.00015` | y 방향 좌표 0.000000 µm에서 목표 격자 간격을 0.00015 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 16 | `y.mesh loc=0.010000 spac=0.002` | y 방향 좌표 0.010000 µm에서 목표 격자 간격을 0.002 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 17 | `y.mesh loc=0.030000 spac=0.004` | y 방향 좌표 0.030000 µm에서 목표 격자 간격을 0.004 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 18 | `y.mesh loc=0.100000 spac=0.012` | y 방향 좌표 0.100000 µm에서 목표 격자 간격을 0.012 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 19 | `y.mesh loc=0.400000 spac=0.05` | y 방향 좌표 0.400000 µm에서 목표 격자 간격을 0.05 µm로 지정한다. 경계·접합에서의 전계 해상도에 영향을 준다. |
| 20 | `region num=1 material=air` | 1번 영역은 배경 공기이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 21 | `region num=2 material=conductor x.min=1 x.max=2 y.min=-0.095000 y.max=-0.015000` | 2번 영역은 도체 게이트이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 22 | `region num=3 material=Al2O3 x.min=1 x.max=2 y.min=-0.015000 y.max=-0.007000` | 3번 영역은 상부 차단 절연막이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 23 | `region num=4 material=nitride x.min=1 x.max=2 y.min=-0.007000 y.max=0.000000` | 4번 영역은 질화막 전하 저장층이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 24 | `region num=6 material=silicon y.min=0` | 6번 영역은 Si 기판 및 채널이다. material은 재료, x.min/max 및 y.min/max는 경계 좌표(µm)다. y=0은 Si 표면이다. |
| 25 | `electrode name=cgate x.min=1 x.max=2 y.min=-0.095000 y.max=-0.015000` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 26 | `electrode name=source x.min=0 x.max=0.666667 y.min=0 y.max=0` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 27 | `electrode name=drain x.min=2.333333 x.max=3 y.min=0 y.max=0` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 28 | `electrode name=substrate bottom` | 지정한 범위에 전극을 배치한다. cgate는 게이트, source·drain은 소스·드레인, bottom은 기판 아래쪽 접촉을 뜻한다. |
| 29 | `doping uniform p.type conc=1e17 reg=6` | Si(6번)에 균일 p형 배경 도핑 10¹⁷ cm⁻³을 지정한다. |
| 30 | `doping gauss n.type conc=5e20 char=0.03 lat.char=0.005 reg=6 x.r=0.995` | Si에 n형 Gaussian 소스/드레인을 만든다. conc는 피크 농도(cm⁻³), char와 lat.char는 수직·수평 특성 길이(µm), x.r/x.l은 도핑 창 경계다. |
| 31 | `doping gauss n.type conc=5e20 char=0.03 lat.char=0.005 reg=6 x.l=2.005` | Si에 n형 Gaussian 소스/드레인을 만든다. conc는 피크 농도(cm⁻³), char와 lat.char는 수직·수평 특성 길이(µm), x.r/x.l은 도핑 창 경계다. |
| 32 | `interface n.i dynasonos` | 질화막–인접 절연막의 DYNASONOS 경계를 활성화한다. TANS의 하부는 Si/질화막 직접 접촉이다. |
| 33 | `material material=Al2O3 eg300=8 egalpha=0 affinity=1.50 permittivity=9.3 semiconductor nc300=1e19 nv300=1e19 mc=0.3 mv=1 mun=0.1 mup=0.01 taun0=1 taup0=1` | 비유전율 permittivity, 300 K 밴드갭 eg300(eV), 전자친화도 affinity(eV), 온도 계수 egalpha를 지정한다. 기준 덱의 semiconductor는 절연막을 넓은 밴드갭 반도체로 풀게 한다. mc/mv는 유효질량비, nc300/nv300은 유효 상태밀도(cm⁻³), mun/mup은 이동도(cm²/Vs), taun0/taup0은 SRH 수명(s)이다. |
| 34 | `material material=nitride semiconductor eg300=5.1 egalpha=0 affinity=2.05 permittivity=7.5 nc300=1e19 nv300=1e19 mc=1 mv=1 mun=0.1 mup=0.01 taun0=1 taup0=1` | 비유전율 permittivity, 300 K 밴드갭 eg300(eV), 전자친화도 affinity(eV), 온도 계수 egalpha를 지정한다. 기준 덱의 semiconductor는 절연막을 넓은 밴드갭 반도체로 풀게 한다. mc/mv는 유효질량비, nc300/nv300은 유효 상태밀도(cm⁻³), mun/mup은 이동도(cm²/Vs), taun0/taup0은 SRH 수명(s)이다. |
| 35 | `# e/h depths and cross-sections are starting assumptions, not fitted data.` | 파일 용도 또는 매개변수 가정에 관한 주석. |
| 36 | `nitridecharge nt.n=1e19 nt.p=1e19 elec.depth=1.2 hole.depth=1.2 sigmat.n=1e-14 sigmat.p=1e-14 sigman.p=1e-16 sigmap.n=1e-16 pf.b=1e13` | nt.n/nt.p는 전자·정공 트랩 수(cm⁻³), depth는 깊이(eV), sigmat와 교차 sigman/sigmap은 포획 단면적(cm²), pf.b는 PF 시도율(s⁻¹)이다. |
| 37 | `contact name=cgate workf=4.60` | 게이트의 유효 일함수 workf(eV)를 지정한다. SONOS 4.05, TANOS·TANS 4.60이다. |
| 38 | `models srh temp=77 print pf.nitride` | SRH 재결합과 격자 온도 77 K를 지정하고 모델을 출력한다. pf.nitride는 질화막 PF 방출을 켠다. |
| 39 | `models region=6 fermidirac incomplete ioniz analytic bbt.kl print` | Si 영역에 Fermi–Dirac 통계, 불완전 이온화, 고농도 Si 이온화 보정, analytic 이동도 모델을 지정한다. bbt.kl이 있으면 국소 Klaassen BTBT도 활성화한다. print는 활성 모델을 출력한다. |
| 40 | `method newton carriers=2 dt.min=1e-14` | Newton 방법으로 전자·정공 연속방정식과 전위를 푼다. 기준 덱의 dt.min은 허용하는 최소 과도 시간 간격(s)이다. |
| 41 | `probe name=bbt_drain r.bbt x=2.005 y=0.001` | 드레인 쪽 지정 Si 좌표(µm)에서 국소 BTBT율을 로그에 기록한다. 공간 최대값은 .str의 U.BBT 분포를 본다. |
| 42 | `probe name=netcharge sonos.charge integrate x.min=1 x.max=2 y.min=-0.007000 y.max=0` | 게이트 아래 질화막 범위의 SONOS 트랩 전하를 적분해 과도 로그에 남긴다. |
| 43 | `output con.band val.band qfn qfp sonos.rates u.bbt e.field band.param` | 저장 구조에 전도대·가전자대, 전자·정공 준페르미 준위, 재료 밴드 매개변수, 전계, BTBT율을 요청한다. 기준 덱의 sonos.rates는 질화막 주입·포획 속도도 요청한다. |
| 44 | `solve init` | 현재 전하와 물성으로 단자 0 V 초기 해를 구한다. |
| 45 | `log outf=TANS_reference_PE_pgm.log sonos.curr` | 이후 수렴한 점의 단자 전압·전류와 probe 값을 outf에 기록한다. sonos.curr는 SONOS 터널 전류 성분을 더한다. |
| 46 | `solve vcgate=16 ramptime=1E-9 tstep=1E-11 tstop=0.000000001` | 게이트 목표전압으로 선형 램프를 준다. ramptime은 램프 시간, tstep은 초기 시간 간격, tstop은 시뮬레이션 누적 종료 시각(s)이다. |
| 47 | `solve tstop=0.00000001` | 직전 단자 바이어스를 유지하며 지정한 누적 시간(s)까지 연속으로 적분한다. |
| 48 | `solve tstop=0.0000001` | 직전 단자 바이어스를 유지하며 지정한 누적 시간(s)까지 연속으로 적분한다. |
| 49 | `solve tstop=0.000001` | 직전 단자 바이어스를 유지하며 지정한 누적 시간(s)까지 연속으로 적분한다. |
| 50 | `solve tstop=0.00001` | 직전 단자 바이어스를 유지하며 지정한 누적 시간(s)까지 연속으로 적분한다. |
| 51 | `solve tstop=0.0001` | 직전 단자 바이어스를 유지하며 지정한 누적 시간(s)까지 연속으로 적분한다. |
| 52 | `solve vcgate=0 ramptime=1E-9 tstep=1E-11 tstop=0.000100001` | 게이트 목표전압으로 선형 램프를 준다. ramptime은 램프 시간, tstep은 초기 시간 간격, tstop은 시뮬레이션 누적 종료 시각(s)이다. |
| 53 | `log off` | 열린 전기적 로그를 닫는다. |
| 54 | `save outf=TANS_reference_PE_pgm_zero.str` | 바로 앞에서 수렴한 구조와 물리량을 outf 이름의 TonyPlot 구조 파일에 기록한다. |
| 55 | `log outf=TANS_reference_PE_ers.log sonos.curr` | 이후 수렴한 점의 단자 전압·전류와 probe 값을 outf에 기록한다. sonos.curr는 SONOS 터널 전류 성분을 더한다. |
| 56 | `solve vcgate=-12 ramptime=1E-9 tstep=1E-11 tstop=0.000100002` | 게이트 목표전압으로 선형 램프를 준다. ramptime은 램프 시간, tstep은 초기 시간 간격, tstop은 시뮬레이션 누적 종료 시각(s)이다. |
| 57 | `solve tstop=0.000100011` | 직전 단자 바이어스를 유지하며 지정한 누적 시간(s)까지 연속으로 적분한다. |
| 58 | `solve tstop=0.000100101` | 직전 단자 바이어스를 유지하며 지정한 누적 시간(s)까지 연속으로 적분한다. |
| 59 | `solve tstop=0.000101001` | 직전 단자 바이어스를 유지하며 지정한 누적 시간(s)까지 연속으로 적분한다. |
| 60 | `solve tstop=0.000110001` | 직전 단자 바이어스를 유지하며 지정한 누적 시간(s)까지 연속으로 적분한다. |
| 61 | `solve tstop=0.000600001` | 직전 단자 바이어스를 유지하며 지정한 누적 시간(s)까지 연속으로 적분한다. |
| 62 | `solve vcgate=0 ramptime=1E-9 tstep=1E-11 tstop=0.000600002` | 게이트 목표전압으로 선형 램프를 준다. ramptime은 램프 시간, tstep은 초기 시간 간격, tstop은 시뮬레이션 누적 종료 시각(s)이다. |
| 63 | `log off` | 열린 전기적 로그를 닫는다. |
| 64 | `save outf=TANS_reference_PE_ers_zero.str` | 바로 앞에서 수렴한 구조와 물리량을 outf 이름의 TonyPlot 구조 파일에 기록한다. |
| 65 | `quit` | DeckBuild 입력의 실행을 끝낸다. |

