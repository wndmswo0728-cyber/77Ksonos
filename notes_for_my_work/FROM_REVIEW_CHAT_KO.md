# "검토 요청" 채팅에서 넘어온 점검 메모 (내 작업용)

- 기준 시점: 브랜치 `claude/kind-keller-zbu9y4`, 커밋 `e769367`
- 대상: `atlas/decks/`, `atlas/README_KO.md`, `python_cryo/README_KO.md`
- 이 메모는 "검토 요청" 채팅에서 팀원 작업을 검토하다가, **내 작업에도 해당할 수 있어 보이는 점**만 모은 것이다. ATLAS는 실행하지 않았고, 덱과 README를 읽고 판단했다.
- 확정된 버그 목록이 아니다. **확인해 볼 목록**이다. 이미 처리했으면 넘어가면 된다.

## 팀원 결과에서 근거로 쓴 것
- **팀원 SONOS SEED 덱 77 K 실행 결과**
  - 구조는 내 덱과 같다: x 간격 50 nm, 64-bit, 0.1 V 간격, MODELS는 `srh`만.
  - SS = 94 mV/dec, Vt(정전류) 0.21 V. 77 K 이론 SS는 약 21 mV/dec이다.
  - gm으로 계산한 이동도는 약 7700 cm²/Vs다. 1000 × (77/300)^−1.5과 맞으므로 온도는 제대로 적용됐다.
  - PGM ΔVt는 2.91 V로, probe 전하로 계산한 정전기 값 2.88 V와 맞았다.
  - `nit.n` 1e18 + 1e19(공칭 1.1e19)를 넣었는데 probe netcharge는 −1.013e-14 C/µm였다. 질화막 평균으로 약 **9.0e18 cm⁻³**다.
- **팀원 Python 패키지(v1 계열 수송 코드)의 300 K 결과**
  - SONOS를 빈 트랩에서 0 V로 10년 두면 전하가 −3.5e-15 C(ΔVt 약 1 V)까지 찬다.
  - PGM에서 시작한 보존도, ERS에서 시작한 보존도 같은 값으로 모인다.

---

## 1. 77 K subthreshold 정확도 — x 메시 (확인 권장)
- 지금 `atlas/decks/*_77K.in`의 x.mesh는 게이트 가장자리 간격이 50 nm다. S/D 접합 lateral char는 5 nm이고 77 K의 kT/q는 6.6 mV다.
- 진단 F에서 S/D 격자는 **수렴 실패의 원인이 아니라고** 확인했다. 하지만 **SS와 절대 VT의 정확도**는 별개 문제다. 같은 메시를 쓴 팀원 결과는 SS가 94 mV/dec로 나왔다. 팀원은 64-bit였고 내 덱은 `-160`이라 결과가 다를 수는 있다.
- 확인 방법: 첫 77 K 초기 읽기에서 SS를 본다(1e-11~1e-7 A 구간).
  - 30 mV/dec 안팎이면 문제없다.
  - 80~90 mV/dec면 x.mesh에 다음을 추가한다. 예전 qf 경로 덱은 이 설정으로 SS가 29 mV/dec였다.
    `x.mesh loc=@Ls spac=0.005`, `loc=@Lgate_left spac=0.005`, `loc=@Lgate_right spac=0.005`, `loc=@Ld spac=0.005`
- 함께 볼 것: 읽기 간격 0.1 V는 SS 약 20~30 mV/dec에서 한 점에 3~5 decade를 건너뛴다. 메모리 창에는 영향이 작지만, 77 K 보존 뒤 **작은 VT 변화**를 말할 때는 오차가 커질 수 있다.

## 2. retention 덱: 읽기마다 MODELS가 다름
- `SONOS_retention_77K.in`(300 K도 같음)의 MODELS가 읽기마다 다르다.
  - 초기·PGM 읽기: `models srh temperature=@temp` + region 6 `cvt` 등
  - 보존 뒤 읽기: `models srh mos temperature=@temp` + region 6 `cvt` 등
- `mos`가 들어가면 이동도나 통계 설정이 바뀔 수 있다. 그러면 최대 gm 접선법 VT가 움직이고, **VT_RET − VT_PGM에 모델 차이가 섞인다.**
- P/E 덱은 세 읽기의 MODELS가 같아서 이 문제가 없다.
- 제안: retention 덱의 세 읽기를 같은 MODELS로 맞춘다. 또는 `print`로 `mos`가 실제로 무엇을 바꾸는지 확인한다.

## 3. `solve init sonos` 뒤에 전하가 이어지는지 확인
- 내 덱은 설명서 권장대로 `solve init sonos`를 쓴다. 팀원은 같은 자리를 `save` → `load ... master` → `solve previous`로 바꿨다.
- 어느 방식이든 **probe netcharge가 단계마다 이어지는지** 첫 결과에서 확인하면 된다.
  - retention: PGM 읽기 시점의 netcharge = 보존 과도 계산 첫 점의 netcharge = 보존 끝 값 → 보존 뒤 읽기의 netcharge
  - P/E: Program 과도 계산 끝 = PGM 읽기, Erase 과도 계산 첫 점 = 프로그램 직후 값

## 4. 300 K 평형 점유 → ERS 상태도 보존 중에 움직일 수 있음
- 팀원 Python에서는 300 K, 0 V에서 빈 트랩이 Si 쪽에서 전자를 받아 평형 점유로 갔다(SONOS에서 약 1 V). 내 `python_cryo`도 TANS에서 트랩–Si 평형(0.55~0.65 V)을 이미 확인했다.
- `couple_atlas.py`는 MW(t) = VT(t) − VT_ERS를 계산한다. 여기서 **VT_ERS는 상수**(P/E 덱의 소거 직후 값)다.
- 300 K에서 ERS 상태도 보존 중에 평형 쪽으로 올라간다면, 상수 VT_ERS로 계산한 MW(t)는 300 K 창을 **실제보다 크게** 볼 수 있다. 77 K에서는 이 효과가 거의 없다(팀원 결과에서 77 K 빈 트랩 보존은 거의 0).
- 제안 (둘 중 하나):
  - (a) ERS 상태에서 시작하는 보존도 같은 방식으로 계산해 VT_ERS(t)를 쓴다.
  - (b) 최소한 빈 트랩 상태로 0 V에서 보존하는 기준선을 계산해서, 300 K에서 평형 쪽으로 얼마나 차는지 확인한다.

## 5. ATLAS 실제 전하와 Python 초기 점유율
- `python_cryo`의 초기 점유율은 공칭 1.1e19(0.22)이다. 팀원 결과를 보면 probe로 측정한 실제 전하는 공칭의 약 82%(평균 9.0e18)였다. 질화막 경계 노드 처리 때문으로 보인다.
- F(t) = Q_full/Q_base는 비율이라 상당 부분 상쇄된다. 하지만 hopping이나 전계 의존 경로는 점유율에 비선형이다.
- 제안: 첫 retention 결과에서 `netcharge_vs_time.dat`의 t = 0 값을 Python Q(0)과 비교한다. 차이가 크면 Python 초기 점유율을 ATLAS 실제값에 맞춘다.

## 6. SONOS 소거 창 (ATLAS 결과가 나오면 확인)
- 예전 v1 Python(archive)에서도 SONOS 소거가 약했다(+0.466 V → +0.454 V). 팀원 v1 계열 Python에서도 소거 뒤 정공이 약 1e2 cm⁻³로, 사실상 소거가 안 됐다.
- ATLAS DYNASONOS P/E 결과(`T*_SONOS_PE_Vt.dat`)에서 VT_ERS가 VT_init 근처까지 내려오는지 본다. 안 내려오면 3 nm 하부 산화막의 정공 경로를 확인해야 한다.
- 이 문제는 4번(MW 계산)에도 직접 영향을 준다.

## 7. 참고: 이미 해결된 것으로 보이는 것
- **v1 호핑(온도와 무관):** `python_cryo/cryo_model.py`(v3)에서 열활성 호핑으로 바뀌었다. 해결됨.
  - 팀원 패키지는 아직 v1 계열 식으로 보인다. 그래서 두 결과를 나란히 비교할 때 호핑을 켠 조건은 같은 기준이 아니다.
- **P/E 덱의 상수 `tau.n`:** `pf.nitride`가 P/E 덱에 들어가 있다. README에 "설명서상 전자 방출은 PF 식"이라고 정리돼 있다.
- **PF 민감도:** 팀원 Python은 `optical_k=4`일 때 프로그램 전계에서 PF 장벽이 약 1 eV 낮아져 300 K 프로그램이 거의 지워졌다. ATLAS `pf.nitride` 매개변수(PF.B, 유전율)는 이와 다르지만, 300 K P/E 결과에서 Program 이동량이 예상보다 크게 작으면 PF를 의심해 볼 만하다. 진단 P15b(PF 없음)와 비교할 수 있다.
