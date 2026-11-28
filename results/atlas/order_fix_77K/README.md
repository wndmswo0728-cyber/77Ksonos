# 77 K with MODELS before CONTACT (order fix) - ATLAS-only

All runs: V2 SONOS deck, `models srh temperature=77` inserted before CONTACT/METHOD (manual 2.5.2 order).

| file | what | status |
|---|---|---|
| TEST_O2_ERSramp_77K.log | fresh device, Erase ramp 0 -> -12 V in 1 ns at 77 K (deck atlas/V2_sonos/77/test_mesh/TEST_O2_order_ers_77K.in) | verified: reached -12 V at 1 ns (210 steps, dt 5 ps); the V2-order deck stalled at -7..-8 V. At -8.04 V p-Si minority n median 1e-13.9 cm^-3 (V2 order 1e8.1), nitride free p ~1e-156 (V2 1e11.5) |
| COOL77s_PGM300.log | 300 K PGM state (tscan/300 PGM0V) read at true 77 K: load -> solve init sonos -> solve prev, gate 0 -> 1 V, drain ramp at 1 V, Vg 1 -> 8 V | verified: VT_gm 3.706 V, VT_cc(1e-7 A) 3.516 V, SS 22.4 mV/dec, netcharge -8.357e-15 C/um (= 300 K PGM) |
| COOL77s_ERS300_v3_failed.log | 300 K PF Erase state read at 77 K, drain ramp at Vg = 0 (cool77 v3) | failed: stopped at Vg 0.63 V (Newton 25, Cannot trap) |
| COOL77s_ERS300noTE_v3_false.log | 300 K no-thermal-emission Erase state read at 77 K, drain ramp at Vg = 0 (cool77 v3) | invalid: between VD 0.03 and 0.04 V at Vg = 0 the solution jumped to 2.6 mA (channel on at Vg = 0, flat in Vg) |

Notes
- Loaded charged states at 77 K show a 1e-13 A source/drain current at zero bias (fresh 77 K device: 1e-35 A). It sets the
  subthreshold floor; VT (gm, 1e-7 A) is above it.
- Comparison: 300 K PGM read VT_gm 3.429 V -> 77 K 3.706 V (+0.277 V); fresh device VT_cc 0.432 V (300 K) -> 0.701 V (77 K, TEST_O1).
- Next: cool77 v4 (ERS reads with the PGM300 bias order) and tscan/77fix (full Program and Erase at 77 K, order fixed).
