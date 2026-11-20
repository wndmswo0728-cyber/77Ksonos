# 읽기 VT 추출 결과 (VD = 0.1 V, 최대 gm 접선의 Vg축 절편)

VT 열은 VD/2 보정 전 값, VT−VD/2 열은 0.05 V를 뺀 값이다. 창(window)은 보정과 무관하다.

| 구조 | 모델 | 상태 | 입력 | VT (V) | VT−VD/2 (V) | Vg@gm,max (V) | DeckBuild VT (V) | Python ΔVT (V) | 상태 |
|---|---|---|---|---:|---:|---:|---:|---:|---|
| SONOS | BTBT | fresh | SONOS_77K_fresh_IdVg.dat | +0.7542 | +0.7042 | +0.985 | +0.7542 | +0.0000 | 추출됨 |
| SONOS | BTBT | programmed | SONOS_77K_programmed_IdVg.dat | +1.2199 | +1.1699 | +1.445 | +1.2199 | +0.4656 | 추출됨 |
| SONOS | BTBT | erased | — | — | — | — | — | +0.5151 | 미실행(파일 없음) |
| SONOS | BTBT | program_retained | — | — | — | — | — | +0.4230 | 미실행(파일 없음) |
| SONOS | BTBT | erase_retained | — | — | — | — | — | +0.3908 | 미실행(파일 없음) |

## VT,PGM − VT,ERS (부호 유지)

| 구조 | 모델 | 구분 | VT,PGM (V) | VT,ERS (V) | VT,PGM−VT,ERS (V) | 역전 | Python 예측 (V) | ATLAS−Python (mV) |
|---|---|---|---:|---:|---:|---|---:|---:|
| SONOS | BTBT | 직후 | +1.2199 | — | — | — | -0.0495 | — |
| SONOS | BTBT | 보존 후 | — | — | — | — | +0.0321 | — |

ATLAS 덱은 Python의 ΔVT를 Si 계면 고정전하 qf로 넣으므로, 정상 실행이면 ATLAS−Python 차이는 격자·Vg 간격에서 오는 수 mV 이내여야 한다. 크게 다르면 qf 전달, 수렴, 추출 구간을 먼저 확인한다.
