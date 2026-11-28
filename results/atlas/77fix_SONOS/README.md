# SONOS 77 K Program/Erase computed at 77 K (tscan/77fix, order fixed) - ATLAS-only

Decks: atlas/V2_sonos/tscan/77fix (300 K PGM_PF/ERS_PF + MODELS before CONTACT, transient fall edges, transient reads).
Same pulses as 300 K (results/atlas/tscan_300K_SONOS_PF): Program +16 V 100 us, Erase -12 V 500 us. Run times 1.52 h / 1.86 h.

| | 300 K (tscan, static reads) | 77 K (77fix) | status |
|---|---|---|---|
| fresh VT gm / cc(1e-7 A) | 0.6073 / 0.4350 V | 0.7801 / 0.7020 V (static, = TEST_O1) | verified |
| max gm | 2.44e-5 A/V | 1.922e-4 (fresh), 1.925e-4 (PGM, transient) A/V | gm check passed |
| PGM netcharge | -8.357e-15 C/um | -4.971e-15 C/um (59 %) | verified |
| VT_PGM gm / cc(1e-7 A) | 3.4290 / 3.2572 V | 2.3998 / 2.3204 V (transient); static 2.4053 / 2.3341 V | verified (static and transient agree, 5.5 mV gm; transient method validated by fresh2) |
| ERS netcharge | -3.208e-15 C/um (61.6 % removed) | -3.155e-15 C/um (36.5 % removed) | verified |
| VT_ERS | 1.6770 / 1.5007 V | transient read running (T77fix_ERS) | not run yet |

Notes
- Program injection at 77 K is ~6x lower at the start (dQ/dt -1.38e-10 vs -8.26e-10 C/s/um at 10 ns) and the 77 K charge is still
  rising at 100 us (x3.7 from 10 to 100 us; 300 K x2.2). Profile (x = 1.5 um): 300 K fills the rows next to the tunnel oxide
  (4.9e19 = NT, falling to 6e10 at the blocking side); 77 K is spread (2.1e19 at the tunnel side to 7e17 at the blocking side).
  The ATLAS term behind the T dependence is not identified yet.
- Erase at 77 K empties the rows next to the tunnel oxide (2.1e19 -> 6e11) and leaves the upper rows, as at 300 K. No Newton
  failures in either transient (only in the static reads).
- Static reads inside the decks: PGM static read stopped the gate ramp at 0.15 V (Cannot trap), then read normally 0.15-3.6 V and
  went to a false off state from 3.75 V; ERS static read failed (2 points). Use the transient reads.
- Transient read: below ~1e-9 A the displacement-current asymmetry (~1e-11 A) limits the curve; use VT_gm and VT_cc at 1e-8/1e-7 A.
  Read disturb to 6 V: netcharge -0.047 %.
- Charge-moment estimate (1-D, mid channel; 300 K check within 14 %): VT_ERS(77 K, gm) ~ 1.7-1.8 V, MW ~ 0.6-0.7 V. Estimate only.
- 77fix read deck: the ERS block holds Vg = 0 until t = 6.4e-7 s (relative TSTOP after a LOAD in the same run apparently used the
  previous block's end time, 6.2e-7 s; the drain ramp itself ended at 1e-8 s). Charge change during the hold 0.003 %.

Transient-read validation (COOL77t2_FRESH_transient_read_check.log, tscan/cool77/SONOS_COOL77_TREAD_fresh2.in, fresh device at 77 K,
static O1 drain ramp + transient gate sweep): VT_gm 0.7802 V (static TEST_O1 0.7802), VT_cc 1e-7 A 0.7009 (0.7014), 1e-8 A 0.6759
(0.6776), max gm 1.923e-4 (1.923e-4) A/V, Id at 1/1.5/2 V equal within 0.1 %. Below ~1e-9 A the transient curve sits on a ~3e-10 A
displacement-asymmetry floor (VT_cc 1e-9 A 5 mV off), so SS is taken from 1e-8..1e-6 A in transient logs. Method verified.
