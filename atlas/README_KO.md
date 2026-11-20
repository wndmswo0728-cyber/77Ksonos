# 300 K vs 77 K 비교용 ATLAS 자체 계산(DYNASONOS) 덱

**목표**: 300 K에서 retention이 약한 TANS가 77 K에서는 약점을 보완해 10년 보존이 가능함을 보인다. 온도와 관련된 모델·메커니즘을 최대한 넣고, 같은 덱을 두 온도에서 돌려 비교한다.

- **기준**: 팀의 원본 300 K SONOS 덱(`original_300K/`)이다. 원본 파일은 수정하지 않고 "원본 모델" 참고 결과로 보관한다.
- **방식**: `make_cryo_decks.py`가 원본에 온도 관련 모델을 **추가**해 `decks/<구조>_PRG_ERS_<T>K.in`, `decks/<구조>_retention_<T>K.in`을 만든다(SONOS·TANOS·TANS). **300 K 판과 77 K 판은 `set temp=`와 출력 접두어(`T300K_`/`T77K_`)만 다르다.**
- SONOS를 먼저 확정한 뒤, 같은 스크립트로 TANOS·TANS를 만든다.
- 고정 매개변수(세 구조 공통): Nsub = 1e17, Nnit = 5e19, Enit = 1.2 eV, Tbox = 3 nm(TANS는 1 nm).

## 추가한 온도 관련 모델 (두 온도 공통)

| 위치 | 모델 | 온도가 들어가는 방식 |
|---|---|---|
| 질화막 트랩 | `pf.nitride` (P/E 덱에 추가, retention 덱은 원래 있음) | 트랩 전자 방출 PF.B·exp(−(1.2 eV − 장벽저하)/kT) (식 3-590) |
| Si | `fermidirac` | Fermi–Dirac 캐리어 통계(저온·고농도) |
| Si | `incomplete` + `ioniz` | 불순물 동결(77 K에서 붕소 일부 비이온화). `ioniz`는 5e20 S/D를 완전 이온화로 유지 |
| Si | `cvt` | 반전층 이동도(Lombardi). 포논·표면 산란이 온도에 의존 |
| Si | `bbt.kl` | 접합 밴드간 터널링. Eg(T)를 통해 온도 의존 |
| Si | `trap.tunnel` | Si 트랩보조(포논 보조) 터널링(Hurkx) |
| 전체 | `temperature=@temp` (모든 MODELS 문) | 원본 P/E 덱은 `$temp`를 쓰지 않아 늘 300 K였다. MODELS 문 사이에 온도가 유지되는지는 설명서에 나와 있지 않다. |

DYNASONOS가 원래 계산하는 메커니즘(밴드↔트랩 직접 터널링, 포획·방출, 질화막 계면 열전자 방출, Si 밴드갭·열속도의 온도 의존)은 그대로 유지한다.

## 추가가 아닌 변경 (최소한으로, 물리 변화 없음)
| # | 내용 | 이유 |
|---|---|---|
| 1 | 전하가 찬 질화막 다음의 `solve init` → `solve init sonos` | 설명서 권장 사항(SOLVE의 SONOS 옵션) |
| 2 | 읽기 Vg를 −2→12 V, 0.02 V 간격으로 통일 | 원본은 상태마다 범위가 달라 VT가 범위 밖이면 추출할 수 없었다. 77 K의 가파른 곡선에는 0.1 V 간격이 굵다. |
| 3 | 읽기 로그가 열린 상태의 `solve init`을 `log off` 뒤로 이동 | 0 V 점이 읽기 곡선에 섞이지 않게 한다. |
| 4 | 읽기 직후 VT 추출(`extract`)과 출력 이름 접두어 추가 | 두 온도와 세 구조에 같은 추출법을 쓰고, 결과가 서로 덮어쓰지 않게 한다. |

`nitridecharge` 줄(`tau.n = tau.p = 1e-4` 포함)은 원본 그대로 두었다. `pf.nitride`를 켜면 설명서상 전자 방출은 PF 식으로 계산된다.

## ATLAS 기본 기능에 없는 메커니즘 → Python으로 보완 (다음 단계)
- **질화막 hopping**(열활성), **질화막 트랩의 포논 보조(다중포논) 터널링**. DYNASONOS의 트랩 터널링은 탄성 터널링뿐이고, 방출은 상수 수명 아니면 PF 중 하나다.
- Python으로 **300 K와 77 K 모두** 이 두 경로가 10년 동안 빼가는 전하를 계산한다. 그다음 ATLAS 보존 결과(질화막 전하·전계)에 연결해 보정한다. 매개변수가 보정 전 값이므로 범위별 민감도와 함께 제시한다.

## 실행 순서 (SONOS)
1. `SONOS_PRG_ERS_300K.in`, `SONOS_PRG_ERS_77K.in`: 초기 → Program(+16 V, 100 µs) → Erase(−12 V, 500 µs), 각 단계 뒤 읽기
2. `SONOS_retention_300K.in`, `SONOS_retention_77K.in`: `nit.n`으로 전하 주입 → 0 V로 3×10⁸ s(약 10년) 보존 → 읽기

출력: `T<T>K_<DEV>_PE_Vt.dat`, `T<T>K_<DEV>_RET_Vt.dat`(상태별 VT와 VD/2 보정값), `T<T>K_<DEV>_<PE|RET>_<상태>_IdVg.dat`, `T<T>K_<DEV>_netcharge_vs_time.dat`(보존 중 질화막 전하, Python 연결용). `.str`/`.log`는 `T<T>K_<PE|RET>_` 접두어. 받은 결과는 `results/atlas/`에 넣는다.

## 확인이 필요한 점 (바꾸지 않음)
- retention 덱의 `nit.n=1e18` 다음 `nit.n=1e19`는 설명서상 **누적**되어 1.1×10¹⁹이 들어간다. 원본과 같게 두었다.
- TANOS/TANS의 `material=TaN`은 설명서 재료 표(Table B-1)에 없다. 300 K에서 실행됐다면 문제가 없었던 것이다.
- 77 K 수렴이 어려우면 순서대로 시도한다.
  1. `go atlas simflags="-160"`(설명서 §21.11)
  2. MATERIAL `NI.MIN`
  3. `bbt.kl`·`trap.tunnel`을 빼고 실행 → 이 경우 같은 덱을 300 K에도 똑같이 적용한다.
