# 77 K TANS retention: SONOS / TANOS / TANS, 300 K vs 77 K

300 K에서 retention이 약한 TANS가 77 K에서는 약점을 보완해 10년 보존이 가능한지를 Silvaco ATLAS(DYNASONOS)와 Python 모델로 검증한다. 참고 논문: Hur et al., *Adv. Electron. Mater.* 2023, 9, 2201299 (SONS, 77 K에서 10년 이상).

## 폴더 구성
| 폴더 | 내용 | 누가 실행 |
|---|---|---|
| `atlas/original_300K/` | 팀의 원본 300 K 덱 (수정하지 않음) | — |
| `atlas/decks/` | 원본에 온도 관련 모델을 **추가**한 덱. `<DEV>_PRG_ERS_<300K/77K>.in`, `<DEV>_retention_<300K/77K>.in`. 300 K와 77 K는 온도와 출력 이름만 다르다. | 사용자 (DeckBuild) |
| `atlas/make_cryo_decks.py` | 원본으로부터 위 덱을 만드는 스크립트. 바꾼 줄과 이유가 모두 들어 있다. 설명은 `atlas/README_KO.md` | — |
| `python_cryo/` | ATLAS에 없는 온도 메커니즘(열활성 hopping, 다중포논 트랩 이온화, Franck–Condon 트랩↔전극 터널링)과 ATLAS 연결 스크립트. 설명과 결과는 `python_cryo/README_KO.md` | Claude / 사용자 |
| `results/atlas/` | 사용자가 돌린 ATLAS 결과를 넣는 곳 (`results/atlas/README_KO.md`) | — |
| `archive/python_qf_path/` | 이전 단계: 팀원의 Python → 등가 qf → ATLAS 읽기 패키지와 검증 기록. 참고용 (트랩 밀도 1e19, 4칸 격자는 현재 기준과 다름) | — |
| `CLAUDE.md` | Claude Code가 이 저장소를 열 때 읽는 프로젝트 요약 (목표, 고정 매개변수, 규칙) | — |

## 작업 순서
1. DeckBuild에서 `atlas/decks/`의 SONOS 덱 4개(300 K·77 K × P/E·retention)를 실행한다. 그다음 TANOS, TANS도 같은 방식으로 실행한다.
2. 출력 파일(`results/atlas/README_KO.md`의 목록)을 `results/atlas/`에 넣는다.
3. `python python_cryo/couple_atlas.py`: ATLAS 결과와 Python 보정을 연결해 VT(t), 메모리 창, 창이 닫히는 시간을 계산한다.

## 고정 매개변수 (세 구조 공통)
Nsub 1e17 cm⁻³, Nnit 5e19 cm⁻³, Enit 1.2 eV, Tbox 3 nm (TANS 1 nm), 질화막 7 nm, 차단막 8 nm (SONOS SiO₂, TANOS·TANS Al₂O₃), Lg 1 µm, 게이트 일함수 4.05 / 4.5 eV, PGM +16 V 100 µs, ERS −12 V 500 µs, 읽기 VD 0.1 V, 보존 3×10⁸ s.
