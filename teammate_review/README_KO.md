# 파일 구분: 내 작업 vs 팀원 작업

이 폴더(`teammate_review/`)는 **팀원 작업과 그에 대한 검토 의견**만 모아 둔 곳이다("검토 요청" 채팅).
저장소의 나머지 파일은 **내 작업**이다("TCAD Atlas 77K Sonos 코드 구현" 채팅).

## 팀원 작업 (`teammate_review/`)
| 경로 | 내용 | 검토 의견 |
|---|---|---|
| `inputs/01_SEED_first_run/` | `SONOS_.in`(첫 SEED 덱), 77 K 초기·PGM 읽기 `.log`, `.str` | `feedback/01_...`에 반영 |
| `inputs/02_N5_decks/` | `SONOS_{77K,300K}_{SEED,PE}_N5.in` (DYNASONOS, 팀 원본 300 K 덱 + `temp`) | `feedback/01_SONOS_N5_decks_KO.md` |
| `inputs/03_ChargeTrap_package/` | `ChargeTrap_77K_Ready_To_Run.zip` (Python 수송 결과 → ATLAS `ox.charge` 읽기, 3구조 × 2온도 × PF/호핑 4조합) | `feedback/02_ChargeTrap_package_KO.md`, `feedback/03_TANS_300K_PF_hopping_KO.md` |
| `inputs/04_Retention_Crosscheck/` | `Retention_Crosscheck_Results.zip` (ChargeTrap 패키지 retention 교차 검증 보고서·그림·스크립트) | `feedback/04_Retention_Crosscheck_KO.md` |
| `build_PF_on_Hopping_on/` | 팀 요청 "PF on·Hopping on 빌드"용. ChargeTrap 패키지의 `ALL_IV.in` 6개(3구조 × 77/300 K)를 계산 절차만 고친 사본 | `build_PF_on_Hopping_on/README_KO.md` |

## 내 작업 (저장소 나머지)
| 경로 | 내용 |
|---|---|
| `flash_transport.py`, `flash_transport_v2.py` | 1D 전하 수송(Python). v2는 열활성화 호핑 |
| `generated/`, `generated_v2/` | Python 결과를 계면 `qf`로 넣은 ATLAS 읽기·바이어스 덱 |
| `cryo_native/` | 팀 원본 300 K 덱을 바탕으로 한 77 K DYNASONOS 덱과 생성 스크립트 |
| `reference/` | DYNASONOS·PF로 P/E를 직접 푸는 ATLAS 기준 덱 |
| `atlas_results/sonos_77K_v1/` | SONOS 77 K fresh·programmed 실제 ATLAS 읽기 결과 |
| `audit/`, `check_results.py`, `analyze_reads.py` | 점검·격자 연구·결과 분석 |
| `README_KO.md`, `VERIFICATION_77K_KO.md`, `DECK_LINES_KO.md` | 문서 |

## 두 접근 비교 (어느 쪽으로 갈지 정할 때 참고)
| 항목 | 내 작업 | 팀원 작업 |
|---|---|---|
| 전하 계산 | Python 1D (v2: 열활성화 호핑, 평면 수 연구) / `cryo_native`·`reference`는 ATLAS DYNASONOS | N5: ATLAS DYNASONOS / ZIP: Python 1D (호핑은 v1 계열 식으로 보임) |
| ATLAS에 전하 넣는 방식 | 등가 계면 전하 `qf` (ΔVt 보존, 질화막 내부 전계는 근사) | `ox.charge` 4평면 체적 전하 (깊이 분포 유지) |
| 범위 | 77 K 중심, SONOS/TANOS/TANS, 보존 1초(기본) | 77 K·300 K, 3구조, PF/호핑 4조합, 보존 10년 |
| ATLAS 실행 | SONOS 77 K fresh·programmed 실행됨 (SS 약 29 mV/dec) | N5 SEED 77 K 실행됨 (SS 약 94 mV/dec), ZIP은 미실행 |
| 알려진 문제 | SONOS 소거 창이 작음(+0.466 → +0.454 V), 4평면에서만 역전, 300 K 평형 기준은 아직 확인 안 함 | `feedback/` 두 문서 참고 |
