# ATLAS 실행 결과를 넣는 폴더

`atlas/decks/`의 덱을 실행한 뒤, 아래 파일을 이 폴더에 복사한다. 그다음 저장소 최상위 폴더에서 `python python_cryo/couple_atlas.py`를 실행하면 Python 보정 결과가 연결된다. 출력은 `python_cryo/results/`에 생긴다.

| 덱 | 꼭 필요한 파일 (T = 300 또는 77, DEV = SONOS / TANOS / TANS) |
|---|---|
| `<DEV>_PRG_ERS_<T>K.in` | `T<T>K_<DEV>_PE_Vt.dat` (Vt_init, Vt_PGM, Vt_ERS), `T<T>K_<DEV>_PE_<init/PGM/ERS>_IdVg.dat` |
| `<DEV>_retention_<T>K.in` | `T<T>K_<DEV>_RET_Vt.dat` (Vt_init, Vt_PGM, Vt_RET), `T<T>K_<DEV>_netcharge_vs_time.dat`, `T<T>K_<DEV>_RET_<init/PGM/RET>_IdVg.dat` |

`.str`와 `.log`는 용량이 크고 Silvaco 저작권 문구가 들어 있으므로 저장소에 올리지 않는다(`.gitignore` 처리).
