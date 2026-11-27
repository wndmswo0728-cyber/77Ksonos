# V2 PF split decks: native reads at 77-200 K and 300 K states read at 77 K (ATLAS-only, verified runs)

| read | T (K) | VT gm (V) | VT cc 1e-7 A (V) | SS (mV/dec) | netcharge (C/um) |
|---|---|---|---|---|---|
| initial | 300 / 200 / 150 / 120 / 100 / 77 | 0.607 / 0.584 / 0.564 / 0.543 / 0.522 / 0.484 | 0.435 / 0.383 / 0.344 / 0.307 / 0.274 / 0.217 | 90.8 / 90.7 / 91.2 / 92.0 / 92.3 / 93.2 | 0 |
| PGM | 300 / 200 / 150 / 120 / 100 / 77 | 3.429 / 2.989 / 2.717 / 2.527 / 2.418 / 2.232 | 3.257 / 2.787 / 2.494 / 2.309 / 2.182 / 1.968 | ~91-94 | -8.357 / -7.119 / -6.401 / -5.910 / -5.688 / -5.319 e-15 |
| 300 K PGM state read at 77 K | 77 | 3.305 | 3.039 | 93.4 | -8.357e-15 |
| 300 K ERS state read at 77 K | 77 | 1.553 | 1.285 | 94.0 | -3.208e-15 |

SS does not scale with T (physics: ~22-26 mV/dec at 77 K; the make_cryo 77 K retention deck gave 25.9) and VT_init
falls on cooling (retention deck: +0.22 V). Suspect: the V2 decks set MODELS ... temperature= AFTER CONTACT/METHOD
(manual 2.5.2: models set in the wrong order may not be used). Test decks TEST_O1 (read) / TEST_O2 (erase ramp).

## TEST_O1 (MODELS moved before CONTACT/METHOD) - CONFIRMED
| read (fresh device, 0-2 V) | VT cc 1e-7 A | SS | Id(0 V) |
|---|---|---|---|
| V2 300 K | 0.435 V | 90.8 mV/dec | 2.2e-12 A |
| O1 300 K | 0.432 V | 90.6 mV/dec | 2.2e-12 A |
| V2 77 K | 0.217 V | 93.2 mV/dec | 5.0e-10 A |
| O1 77 K | 0.701 V | 22.1 mV/dec | 1.8e-35 A |
300 K is unchanged; at 77 K the order fix gives the physical swing and a VT that rises on cooling (+0.27 V).
