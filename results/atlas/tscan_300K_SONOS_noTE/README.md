# 300 K erase without thermal emission (ATLAS-only, verified run)
Deck: atlas/V2_sonos/tscan/300noTE/SONOS_ERS_300K_noTE.in (= 300 K ERS_PF with tau.n/tau.p removed and ^pf.nitride
in the Erase transient), starting from the same 300 K PGM0V state.

| erase | VT gm (V) | VT cc 1e-7 A (V) | netcharge after ERS (C/um) | charge removed |
|---|---|---|---|---|
| PF on (tscan_300K_SONOS_PF) | 1.6770 | 1.5007 | -3.2081e-15 | 61.61 % |
| no thermal emission | 1.6896 | 1.5152 | -3.2477e-15 | 61.14 % |

Time evolution identical to 1 us, within 0.9 % at 500 us. Trapped-electron profiles identical (mean nt 3.724e18 vs
3.726e18); the whole difference is trapped holes present only with PF on (mean pt 4.1e16 -> 0.046e-15 C/um).
So the 300 K erase is trap-to-channel tunneling; thermal emission changes VT_ERS by 12.6 mV.
