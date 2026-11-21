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

## 4. [적용 권장] ERS 상태 보존도 계산해서 VT_ERS(t)로 메모리 창 구하기
**현재 방식**
- `couple_atlas.py`는 MW(t) = VT_PGM(t) − VT_ERS를 계산한다.
- 여기서 **VT_ERS는 상수**(P/E 덱에서 소거 직후의 값)다. 보존은 PGM 상태(`nit.n` 주입)에서만 계산한다.

**바꿔야 하는 이유**
- 메모리 창은 두 상태로 정해진다. PGM 상태는 전자를 잃어 VT가 내려가고, ERS 상태는 정공을 잃거나 전자를 받아 VT가 올라간다. 실제 소자 측정에서도 두 상태를 각각 보존해서, 두 곡선이 만나는 시점을 "창이 닫히는 시간"으로 본다.
- 팀원 결과(v1 계열 Python, TANS 300 K, 호핑 ON)를 보면 PGM 보존과 ERS 보존이 1초 근처에서 **같은 값(−8.23e-16 C)으로 모인다.** 창이 1초 안에 닫힌다는 뜻이다. PGM 곡선만 봤다면 "전하가 남는다"로 잘못 읽었을 것이다.
  - SONOS 300 K도 PGM 보존과 ERS 보존이 10년 뒤 같은 값(ΔVt 약 1 V)으로 모였다.
- 내 `python_cryo`도 TANS에서 트랩–Si 평형(0.55~0.65 V)을 이미 확인했고, README에 "Erase 상태도 결국 도달하는 값이라 창이 닫힌 것과 같다"고 써 두었다. 그런데 정작 MW 계산에는 이 내용이 반영되지 않았다.
- 상수 VT_ERS를 쓰면 **300 K 창이 실제보다 크게** 나온다. 반대로 77 K는 ERS 상태가 거의 변하지 않아 영향이 작다(팀원 결과 77 K ERS 보존: 10년 동안 2.02e-15 → 2.00e-15 C). 그 결과 **77 K와 300 K의 차이가 실제보다 작게** 보일 수 있다. 이 연구의 핵심 결론에 직접 영향을 주는 부분이다.

**적용 방법**
1. **ATLAS:** `atlas/decks/<구조>_PRG_ERS_<T>K.in`의 ERS 읽기 다음에 보존 블록을 추가한다. retention 덱과 같은 설정을 쓴다.
   ```
   (ERS 읽기 끝, log off)
   solve init sonos            # 또는 save/load로 소거 직후 0 V 상태로 복귀
   models mos srh pf.nitride temperature=@temp
   models region=6 fermidirac incomplete ioniz cvt bbt.kl trap.tunnel
   method lte2step tol.time=1.0e-4 tstep.incr=1.2 dt.max=1.0e7
   log outfile=T<T>K_PE_<DEV>_ERS_Retention.log sonos.curr j.tun
   solve tstep=1e-6 tfinal=@Retime proj
   extract name="Qnit_ERS_vs_t" curve(time, probe."netcharge") outfile="T<T>K_<DEV>_ERS_netcharge_vs_time.dat"
   log off
   (보존 뒤 ERS 읽기: 기존 읽기 블록과 같은 MODELS, 같은 범위)
   ```
   P/E 덱 끝에 붙이면 retention 덱을 새로 만들 필요가 없다. 소거 직후 상태에서 그대로 시작할 수 있다.
2. **Python (`python_cryo`):** 소거 상태에서 시작하는 base/full 보존도 계산해서 F_ERS(t)를 구한다.
3. **`couple_atlas.py`:** MW(t) = VT_PGM(t) − VT_ERS(t)로 바꾸고, 창이 닫히는 시간을 두 곡선의 교점으로 정의한다.
4. **기준선(선택):** 빈 트랩 상태에서 0 V로 보존하는 계산을 하나 추가하면, 300 K에서 평형 쪽으로 얼마나 차는지 바로 보인다.

**비용과 우선순위**
- 보존 과도 계산이 구조 3개 × 온도 2개 = 6개 늘어난다.
- 시간이 부족하면 **300 K를 먼저** 한다. 77 K는 ERS 변화가 작으니, 77 K 한 구조로 "ERS가 거의 안 변한다"만 확인해 두면 된다.

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
