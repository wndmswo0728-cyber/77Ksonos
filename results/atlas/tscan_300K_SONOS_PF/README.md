# tscan 300 K, SONOS, PF split decks (ATLAS-only, verified run)

Decks: atlas/V2_sonos/tscan/300/SONOS_{PGM,ERS}_PF_300K.in (= 300/pgm_pf, 300/ers_pf). Logs renamed (suffix dropped).
`python3 atlas/V2_sonos/tscan/vt_summary.py results/atlas/tscan_300K_SONOS_PF`

| state | VT first-gm-peak (V) | VT cc 1e-7 A (V) | probe netcharge (C/um) |
|---|---|---|---|
| initial | 0.6073 | 0.4350 | 0 |
| PGM (+16 V, 100 us, PF on) | 3.4290 | 3.2572 | -8.3566e-15 |
| ERS (-12 V, 500 us, PF on) | 1.6770 | 1.5007 | -3.2081e-15 |

dVT_PGM 2.822 V, dVT_ERS 1.070 V, MW 1.752 V (cc: 1.757 V). Erase removes 61.6 % of the trapped charge
(1 us 7.8 %, 10 us 25 %, 111 us 48.5 %, 500 us 61.6 %).
.str (not stored): erase empties the nitride rows next to the tunnel oxide (y -3.3/-3.6 nm: 4.9e19 -> 2e15/1e17,
-3.9 nm 4.7e19 -> 1.7e19); interior rows unchanged; blocking side +1.2e17 electrons; trapped holes small (max 3.5e17).
So the 300 K erase is trap-to-channel tunneling, not PF emission (that would empty the interior too).
