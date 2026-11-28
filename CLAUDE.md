# 77 K TANS retention project — notes for Claude Code

Answer the user in Korean.

## Goal
Show with Silvaco ATLAS 5.36.0.R (DeckBuild/TonyPlot) plus a Python model that TANS
(TaN/Al2O3/Si3N4/1 nm SiO2/Si), whose retention is weak at 300 K, keeps its memory
window for 10 years at 77 K. Compare SONOS, TANOS and TANS at 300 K and 77 K.
Reference paper: Hur et al., "Cryogenic Storage Memory with High-Speed, Low-Power, and
Long-Retention Performance", Adv. Electron. Mater. 2023, 9, 2201299 (SONS without tunnel
oxide; RT window closes in about 1 year or less than 10 years; at 77 K open beyond 10 years;
extrapolation current = alpha - beta*ln(t + gamma); cause: suppressed thermally activated
charge loss).

## Fixed parameters (team, all three structures)
Nsub = 1e17 cm^-3, Nnit = 5e19 cm^-3, Enit = 1.2 eV, Tbox = 3 nm (TANS 1 nm native oxide),
blocking 8 nm (SiO2 for SONOS, Al2O3 for TANOS/TANS), nitride 7 nm, Lg = 1 um,
gate work function 4.05 eV (SONOS) / 4.5 eV (TANOS, TANS), PGM +16 V 100 us,
ERS -12 V 500 us, read VD = 0.1 V, retention 3e8 s at 0 V.

## Layout
- `atlas/original_300K/` team's 300 K decks. Never edit.
- `atlas/make_cryo_decks.py` -> `atlas/decks/<DEV>_{PRG_ERS,retention}_{300K,77K}.in`.
  The 300 K and 77 K decks differ only in `set temp=` and output prefixes. Temperature
  models are ADDED to the originals (pf.nitride, fermidirac, incomplete ioniz, cvt,
  bbt.kl, trap.tunnel, temperature= on every MODELS). Other changes: solve init sonos,
  common read sweep -2..8 V / 0.1 V (speed; gm rises again above ~6 V), extract lines, output names T<T>K_<PE|RET>_...
- `python_cryo/cryo_model.py` 1-D trap model (v3): activated hopping, multiphonon
  (Makram-Ebeid & Lannoo) trap ionization above PF, Franck-Condon trap<->electrode
  tunneling (fc_tunnel), retention-only mode, ATLAS device values.
- `python_cryo/couple_atlas.py` multiplies the ATLAS trapped charge vs time by
  F(t) = Q_full/Q_base from Python. Puts results in `python_cryo/results/`.
- `results/atlas/` ATLAS outputs that the user runs and uploads.
- `archive/python_qf_path/` earlier teammate package (Python -> equivalent qf -> ATLAS
  read). Kept for reference only; its trap density (1e19) and 4-plane grid are outdated.

## Verified facts
- ATLAS/DeckBuild keywords used in the decks were checked against the user manuals
  (stored in the private repo wndmswo0728-cyber/silvaco-manuals; do not copy them here).
- 77 K read decks converge at default precision (SONOS v1 read: VT fresh 0.7542 V,
  programmed 1.2199 V, shift equals the Python value within 2 uV).
- 4-plane v1 Python results were grid-dependent (the SONOS PGM/ERS inversion was a
  numerical artifact). Use planes >= 8 (default 16).

- 77 K convergence (diag decks in atlas/diag): SOLVE INIT failed until MODELS was moved
  before CONTACT/METHOD (manual 2.5.2 order); VD=0.1 V in one step diverged, a small VD
  ramp works. With both fixes the 77 K DYNASONOS deck reaches VD=0.1 V, VG=1 V (diag H2,
  26.9 min, -160 precision). Starting at 300 K and lowering T inside one run diverged.
  77 K decks need simflags -160: with 64-bit the read converged but the first Program
  time step failed with "NaN or Inf in SONOS tunnel current" (exp(E/kT) overflow).

- Program transient "NaN or Inf in SONOS tunnel current" (also at 300 K, diag P6) came from
  the deck changes: PF.NITRIDE with NT.P>0 needs HOLE.DEPTH (default -999 eV) -> set
  hole.depth=@Enit; and the 1 ns gate ramp needs METHOD DT.MAX=2e-11 (time step jumped to
  0.6 ns near 13 V). With both (diag P11a/P11c) the 300 K SONOS Program reaches 16 V / 10 ns
  with all added models. MODELS now sits after NITRIDECHARGE and before METHOD.

- 77 K Program ramp: with PROJ on the ramp solves the tunnel current became NaN near Vg
  2.1-2.4 V for every time step tried (P12, P13 down to 0.25 ps, P13b, P15b without
  PF.NITRIDE). Diag P14 (DT.MAX 5e-12 over the whole 1 ns ramp, ramp split at Vg/10, NO
  PROJ on the ramp) reached 16 V / 10 ns at 77 K in 2.8 h with all models. All decks use
  this ramp form (300 K too); PROJ kept for constant-bias holds.

- Retention decks: the original nit.n=1e18 + 1e19 in two SOLVE steps did not converge at
  77 K (Newton 25 iterations).
- SOLVE NIT.N OVERWRITES (measured, despite the manual's "cumulative"): 10 x 1e17 + 40 x
  2.5e17 left exactly 2.5e17 in the PGM .str (probe 2.2e17); the team original ends at 1e19
  (teammate probe 9.0e18). Decks step 1e17, 2.5e17 ... 3.75e18, then 1.25e17 steps to 1e19
  (66 solves): 2.5e17 steps stopped at 4e18 at 77 K, half steps reached 1e19 (diag R1).

- First 77 K SONOS retention run (2.2e17 only, not for the 10-year verdict): charge continuous
  through every step (SOLVE INIT SONOS keeps the trapped charge); SS 22-23 mV/dec (mesh OK);
  -18 % in 10 y via tunnel-oxide electron current; post-retention read diverged at Vg -1.09 V
  (cause unclear; see model order below); trapped electrons moved to the blocking-oxide side
  (2e18 in one row), unexplained by 77 K PF -> retention split at 1 s / 1e4 s with .str saves.
- TAU.N/TAU.P are unused when PF.NITRIDE is on: diag R2a (tau 1e-4 s, team) and R2b (tau
  removed) gave byte-identical 77 K results to 1 s. First-second loss (~8 %) = the nitride row
  next to the tunnel oxide tunnels out; interior unchanged; blocking-side pile-up comes later.
- Deck VT extract picks the global max gm (end of sweep); couple_atlas.py re-extracts VT at the
  first gm peak from the Id-Vg files. Python initial occupancy = ATLAS probe Q(0).
- P/E decks end with an ERS-state retention (team review item 4): MW = VT_PGM(t) - VT_ERS(t).
- All decks: static solves (injection, reads) without PF.NITRIDE, transients with it. The 2nd 77 K
  retention run with PF.NITRIDE in static solves was invalid (PGM channel off up to 8 V, +28 %
  charge at the retention start). Reads after pulses LOAD the .str saved at the end of the pulse.

- Both temperatures now use simflags -160: 300 K 64-bit stalled at NIT.N 6e18 (precision floor).
- "solve init"/"solve init sonos" + "solve prev" after a read RE-APPLIED the read bias (Vg 8 V,
  VD 0.1 V): the 300 K Erase ramp started at 8 V and failed. P/E decks now ramp drain and gate
  back to 0 V with DC steps before Program, Erase and the ERS retention.

- SOLVE INIT SONOS keeps the trapped charge AND the electrode biases (SOLVE INIT resets to 0 V):
  after the PGM read it re-solved at Vg 8 V / VD 0.1 V with 1e19 trapped, failed, and the 77 K
  retention transient then hit NaN. Decks now reach 0 V by DC steps (RAMP_DOWN / gate steps)
  after every read or pulse that precedes a transient or a read; SOLVE INIT SONOS only at 0 V.
- 300 K NIT.N stall is caused by PF.NITRIDE during the static injection (diag R3c without it:
  1e19 in 3 Newton iterations per step; R3b ni.min 1e-40 failed; R3d without bbt.kl/trap.tunnel
  barely passed). Diag R4 (77 K and 300 K OK): retention decks now inject and read with
  "srh + Si models" and re-specify "srh pf.nitride + Si models" only for the retention
  transient (team original order, without mos); all three reads use the same models.

- LOAD INFILE=<.str> MASTER restores the trapped nitride charge exactly (diag R5a: same netcharge
  and VT as the in-run PGM read). Reads after a retention transient now LOAD the .str just saved
  (in-run SOLVE INIT SONOS + SOLVE PREV failed at 300 K; R5b load read worked).
- bbt.kl with default D = 1 generates in equilibrium (0 V current, left Id-Vg branch, PGM hump =
  drain->substrate); VT identical without it (R6); retention Q(1e4 s) identical with bbt.hurkx (R7b,
  0.7527 vs 0.7526). Decks now use bbt.kl bbt.hurkx; SONOS runs without hurkx stay valid
  (charge and VT identical); redo only their Id-Vg leakage plots by LOAD + read with hurkx.
- 300 K SONOS retention (ATLAS-only, 8.84e18 probe): VT_init 0.534, VT_PGM 3.480, VT 10 y 2.242 V;
  Q/Q0 10 y 0.635; electrons pile up at the blocking-oxide side (1.24e19 in the top row), so VT
  falls more than Q (58 % vs 63.5 %): use the read VT, not VT linear in Q (0.16 V too high).

- Diag B1 77 K: PF.NITRIDE in a static solve changes nothing (a/b .str identical; PGM read with it
  normal, VT 4.00 V). So the 2nd 77 K run failure is NOT read-time free electrons; open candidate:
  injection with PF.NITRIDE on (compare R1 vs R4 77 K .str). Final decks inject without it.
- Diag B1 (300 K): a static solve with PF.NITRIDE diverges (NaN) from a converged 1e19 state:
  in static solves the trap occupancy is frozen but the PF emission term still feeds free electrons
  into the nitride (no steady state). Keep PF.NITRIDE out of static solves (correct, not a bypass).
- Diag B2/B3: after a transient, SOLVE INIT SONOS + SOLVE PREV leaves a stale initial guess (the
  next solve at the SAME 0 V starts with a 1e-1.4 potential update and fails); without the
  transient (B2) it works; METHOD reset does not help (B3b). save -> LOAD restarts from the saved
  solution, so reads after transients use LOAD.

- Diag B5/B6 (77 K): the injected states with/without PF.NITRIDE are identical, and so are the
  read states at Vg 0-4 V (B6). The failed reads (channel off to 8 V / stop at 4.6 V) only occur
  with PF.NITRIDE active in static solves AND a read path through -2 V: a path-dependent Newton
  problem, not physics. Keep PF.NITRIDE out of static solves. Diag B7 checks the final read path.

- Diag B7/B8 (77 K, final models, no PF.NITRIDE): the PGM read via -2 V still kept the channel off
  up to 8 V -> the B5/B6 "PF.NITRIDE" condition was wrong; the trigger is the read path through
  -2 V with 1e19 trapped at 77 K (0 V-start reads in B6 all fine; 300 K fine). All reads now start
  at 0 V: up 0 -> 8 V, then LOAD the saved Vg=0 state and go down 0 -> -2 V (_IdVg_neg.dat; merged
  by couple_atlas.py). Diag B9 (77 K, 300 K) checks it.

- Diag B9 (77 K VT 3.6959 V, 300 K 3.4795 V): 0 V-start reads work; in-run read = load read. Checks done.
- Retention transients stop at 1, 10, 100, 1e3, 1e4 s (save .str, continue with tstop) and the deck
  end LOAD-reads each (states RETt1s..RETt1e4s, ERSt1s..ERSt1e4s). couple_atlas.py: paper_fit (fit
  1 s-1e4 s with alpha - beta*ln(t+gamma), extrapolate, compare with the 3e8 s read; MW(t)), loss per
  decade after 1 s, and a Python equilibrium test (empty/PGM/ERS starts at 0 V).
- Python v4: the equilibrium test found the oxide-only FN/direct band injection charging EMPTY traps
  to +1.0 V in 10 y at 300 K (no reverse process; carrier left the oxide below the nitride band edge).
  Band injection now continues the WKB action through the Si3N4 gap (nit_mass 0.5) and is 0 without a
  turning point in the nitride. Empty starts stay at 0; PGM-start retention unchanged.

- Diag P16 (77 K Program ramp to 10 ns): DT.MAX 2e-11 on the 2nd segment = 5e-12 within 0.03 % at
  10 ns (1.49 h -> 35.7 min); -P 4 byte-identical (-> 23.5 min). P/E decks use both; Erase ramp keeps
  5e-12 (untested); retention decks unchanged.

- 300 K P/E (P16 decks): static gate steps from the end-of-Program state (16 V) failed at every step
  incl. a direct 16 -> 0 V solve (NaN in currents; frozen traps + high-field injection, no steady
  state); the read log was empty. P/E decks now end each pulse with a transient fall edge (mirrored
  rise, pf.nitride on, then 1 us at 0 V, TSTOP ... RELATIVE), save at 0 V, load, read. Not run yet.

- MY DECK BUG (2026-11-22): after the split reads every read ENDED at Vg = -2 V and RAMP_DOWN's gate
  step (vstep=-0.2 to 0 V) cannot move up from -2 V, so the 300 K retention ran 3e8 s at Vg = -2 V
  (invalid) and the P/E pulses/ERS retention started at -2 V. Each read block now LOADs its _rd0.str
  (Vg 0, VD 0.1) at the end. atlas/check_bias.py traces Vg/VD statically; make_cryo_decks.py runs it
  and stops on any problem. The FIRST 300 K retention result (VT 2.242 V at 10 y) stays valid.

- 300 K retention (0 V fixed deck): post-retention LOAD + first static solve at 0 V failed (Newton 25).
  Hypothesis: MODELS without pf.nitride does NOT switch it off after a pf.nitride transient (logicals
  are set false only with ^, manual 2.5); static PF diverges at 300 K (B1), harmless at 77 K. Explains
  B3a/b, the P/E post-Program NaN and this failure; fresh runs never with PF (B2, R5b) worked. Static
  MODELS now 'srh ^pf.nitride'. CONFIRMED by diag D1 (300 K): D1b (no ^) failed at the first static
  solve after the 1 s retention; D1a (^) read normally (VT_init 0.5348, VT_PGM 3.4799, VT 1 s 3.2018 V).
  The B2/B3 'stale initial guess' reading is superseded by this.

- Teammate package review (C, A): couple_atlas.py also extracts constant-current VT (1e-9..1e-7 A)
  -> T<T>K_<DEV>_vt_methods.csv; 300 K SONOS dVT agrees with max gm within 4 mV. Python nit_offset
  (Si->Si3N4 CB, default 2.0 eV) sensitivity 1.45-2.1 eV: retention 10 y dVT changes <= 0.19 V, F <= 0.08,
  77 K > 300 K in all cases (Python-only; Program comes from ATLAS).

- Paper pulse decks (not run): <DEV>_PAPER_{PGM,ERS}_{T}K.in from paper_decks(): wake-up +6.5/-6.5 V 500 us,
  write +6.5 V / erase -6.5 V 5 us, all transient times RELATIVE, PGM and ERS retention from real pulses
  (outputs _PP_). couple_atlas.py analyses them with prefix PP_. Python standalone P/E is weak (own PF
  with optical_k 4 empties traps at 16 V/300 K; FN capture 0.05) - not used for results; compare with the
  ATLAS pulse P/E before aligning. Earlier '~3 V in ATLAS' referred to nit.n injection, not a pulse.

- 300 K SONOS retention, FINAL deck (ATLAS-only, results/atlas/run3_300K_SONOS_RET): VT 0.5336/3.4795/
  2.2401 V (10 y); snapshots 1 s..1e4 s 3.2005/3.1943/3.1369/2.8562/2.6340 V; loss concentrated 100 s-1e4 s.
  Paper log fit on 1 s-1e4 s predicts 1.400 V at 3e8 s vs 2.240 simulated (0.84 V too pessimistic):
  report the direct 3e8 s value. cc-VT = gm-VT within 4 mV. 77 K retention failed at the t1e3s snapshot
  load (Newton 25 at 0 V); t100s read ran at VD 0.011 V (drain ramp stalled). Waiting for .str/logs.

- 77 K SONOS retention, FINAL deck (ATLAS-only, results/atlas/run3_77K_SONOS_RET): valid reads init/PGM/10 y
  VT 0.7503/3.6959/1.8422 V (deck Vt_RET 7.17 is a wrong global-gm pick). Snapshot reads 1/10/100 s: channel
  never on (invalid), t100s drain stalled at 0.011 V, t1e3s load + solve prev failed (Newton 25). Q/Q0 equals
  300 K to 1e3 s, then 77 K loses MORE (3e8 s 0.453 vs 0.634). .str: top nitride row (blocking side) fills to
  3.3e19, free electrons ~3e2 cm^-3 in the nitride CB during the transient at both T (not thermal). Suspect
  free-electron drift; diag E3b (nitride mun 0.01, 77 K to 1e4 s), E2a/b/c (snapshot reads, with SOLVE INIT
  SONOS after LOAD) in the 77 K retention folder. Do not tune toward the expected result.

- 77 K ERS stall (V2 decks, atlas/V2_sonos/77/test_mesh, fresh device ramp 0 -> -12 V in 1 ns): stalls at -8.07 V (A),
  -8.85 V without hole traps (H1, p converges, n does not), -8.2 V with S/D 50 nm outside the gate (H2), -8.2 V with bottom-oxide mv=10 (H3, hole tunneling
  mass; manual: MC/MV are the tunnel-oxide masses) -> not hole traps, not the gate-edge n+ overlap, not hole tunneling. Failing pattern: n x-norm stuck at -0.301 (n can only halve per Newton iteration) and
  n/p rhs nearly equal. PGM-state .str at -6.6 V (77 K): free n 1e2..1e10 and p 1e9..1e12 cm^-3 in the nitride bands,
  n piled at the tunnel-oxide side (oxide n 60+ orders lower; 1 eV CB offset blocks thermionic escape at 77 K).
  TEST_S_save_{77,300}K.in save the fresh-device state at -6.0/-7.2/-7.8/-8.04 V with SONOS.RATES/RECOMB to locate it.
- TEST_S result (fresh device, same Vg, 77 vs 300 K): gate-side (blocking oxide) SONOS rates identical at both T (gate
  injection is fine). At 77 K only, the tunnel-oxide side shows free n/p 1e9..1e12 in the nitride, trapped n/p ~1e13..1e15,
  trap rates 1e23..1e25 (300 K: free carriers <1e-9, rates <1e3); minority electrons in p-Si median 1e7..1e8 at 77 K
  (equilibrium ~1e-57) vs 1e2.9 at 300 K (= equilibrium). Reading: unresolved minority carriers below the CLIM.DD cut-off
  (manual: solutions below it are not required to converge, "false solution") feed DYNASONOS Si<->nitride exchange.
  clim.dd=4.5e13 was MY addition (commit 0d2a22d, = Si default); original V2 had none and also stalled (-7.1 V, PGM state).
  TEST_T1 (clim.dd 1e8) / TEST_T2 (5e-17 = 300 K default ratio to ni) test this; they also save the 0 V initial state.
- TEST_T1/T2 result: lowering clim.dd makes the 77 K ramp unusable. After 3.1 h T1 (1e8) was at Vg -0.07 V (dt 1.6e-14 s),
  T2 (5e-17) at -1.03 V (dt 2.3e-15 s); n rhs floors at 1e-14..1e-15 (criterion 5e-18), n x-norm up to +2.9. The default
  cut-off cannot be lowered at 77 K; the init0V .str files (static 0 V) are still to be checked for minority n.
- Why the 77 K exchange is non-physical (TEST_S77 -6 V .str band edges; code 114 = Ec, 113 = Ev, eV): nitride hole-trap level
  (Ev_nit + 1.2) lies inside the Si gap (manual: tunneling that starts/ends in the channel gap is zero); nitride Ev is 1.05 eV
  below Si Ev, so hole injection ~exp(-1.05/kT) = 1e-18 (300 K) vs 1e-69 (77 K); ATLAS gives the reverse (1e-5 vs 1e23).
  Exact internal term not identifiable from outputs. Workaround in progress: temperature scan with the PF split decks
  (atlas/V2_sonos/tscan/<T>/, only `set temp` differs: 200/150/120/100 K) to find the lowest T where ERS converges and the
  VT_ERS(T) trend; report 77 K ERS as extrapolated if flat.
- SONOS.RATES codes (TEST_S): 833 = free-hole capture (matches sigmat.p*vth*p*(NT.P-pt) within x3 at 77 and 300 K);
  830/832 = tunneling generation terms. Gate side 830/832 identical at both T; tunnel-oxide side 77 K 1e22.7/1e22.8 vs
  300 K 1e1.4/1e-4.5 (-6 V). The documented equations (3-586/3-589) with the .str band edges give ~0 there, so the deviation
  is in undocumented internals (Fermi factor s, equilibrium emission e_eq, sub-cut-off carrier handling).
- tscan run 1: PGM_PF finished at 300/120/100 K (ERS running). 150 K and 200 K PGM_PF stalled right after the ramp
  (16 V hold, t ~1.03-1.06 ns, dt 3e-13/4e-14 s): n x-norm floor -3.6..-4.0 vs criterion -4 (cx.tol 1e-4), rhs n ~1e-12.
  Fallback decks <T>K_tol5e-4.in change only cx.tol 1e-4 -> 5e-4 on PGM_PF lines 129/132/134 (hold + PGM read).
- tscan run 1 ERS: 300 K ERS_PF finished. 100 K and 120 K ERS_PF show the 77 K stall pattern (n x-norm -0.301 halving,
  n/p rhs equal) from about -7.2 V (100 K, ~0.01 V/min at 42 min) and -7.8 V (120 K, ~0.003 V/min). Stall onset vs T
  (PGM state, ERS_PF): 77 K -7.1..-7.2 V, 100 K -7.2 V, 120 K -7.8 V, 300 K none. If they crawl through, check the
  .str for spurious tunnel-oxide-side trapping before using VT_ERS.
- tscan 300 K result (results/atlas/tscan_300K_SONOS_PF, ATLAS-only, verified): VT init/PGM/ERS 0.6073/3.4290/1.6770 V
  (gm), MW 1.752 V; netcharge -8.357e-15 -> -3.208e-15 C/um (61.6 % removed). Erase = trap-to-channel tunneling from the
  rows next to the tunnel oxide (interior rows unchanged, holes small): physically T-independent, which supports
  extrapolating VT_ERS(T). Older no-PF V2 300 K deck gave PGM 3.509 / ERS 1.395 V (tau.n 1e-4 s emission).
- tscan run 2: ERS_PF stalls with the 77 K pattern at 100, 120, 150 and 200 K (user report); only 300 K completes, so no
  VT_ERS(T) trend. Fallback (ASSUMPTION, label it): 77 K ERS state = 300 K erase charge read at 77 K. tscan/300noTE/
  SONOS_ERS_300K_noTE.in = 300 K ERS_PF with tau.n/tau.p removed and ^pf.nitride in the transient (no thermal emission;
  bounds the thermal part that is absent at 77 K). tscan/cool77/SONOS_COOL77_from300K.in loads ../300 PGM0V, ../300 ERS and
  ../300noTE NOTE_ERS at temperature=77, solve init, and runs the PGM_PF/ERS_PF reads (COOL77_*.log). Not run yet.
- V2 TEMPERATURE NOT FULLY APPLIED (strong evidence, results/atlas/tscan_native_reads): every V2 read has SS 91-94
  mV/dec from 300 K down to 77 K (physics ~22-26 at 77 K; make_cryo 77 K retention deck 25.9) and VT_init FALLS on
  cooling (0.607 -> 0.484 V; retention deck +0.22 V), while mobility (Id) does follow T. V2 decks put MODELS ...
  temperature= after CONTACT/NITRIDECHARGE/METHOD; manual 2.5.2 order is MATERIAL -> MODELS -> CONTACT -> METHOD.
  Cooled 300 K states read at 77 K behave like the native V2 77 K reads (same -0.124 V shift; MW 1.752 V = 300 K).
  PGM charge falls with T in V2 (-8.36 -> -5.32e-15 C/um, 300 -> 77 K). All V2 77 K numbers are suspect until
  TEST_O1 (read, 77/300 K) and TEST_O2 (77 K fresh erase ramp) with MODELS moved before CONTACT are checked.
- 300 K erase without thermal emission (results/atlas/tscan_300K_SONOS_noTE, ATLAS-only, verified): VT_ERS 1.6896 vs
  1.6770 V with PF (12.6 mV), charge removed 61.14 vs 61.61 %; electron profiles identical, difference = holes trapped
  only with PF on. The 300 K erase is tunneling; thermal emission bound for a 77 K ERS assumption: ~13 mV.
- Order-fixed cool77 (MODELS before CONTACT): load 300 K PGM0V + plain SOLVE INIT at 77 K -> first Newton solve diverged
  (n/p x-norm +3..+10, psi capped, "Cannot trap"), unlike the V2-order run: with the fix the run is really at 77 K and
  needs SOLVE INIT SONOS (manual: prevents large carrier concentrations in a charged nitride at SOLVE INIT). v2 deck:
  load -> [solve init (ERS files were saved at -12 V)] -> solve init sonos -> solve prev; outputs COOL77s_*.
- CONFIRMED (TEST_O1, 2026-11-28): with MODELS ... temperature= before CONTACT/METHOD the 77 K fresh read gives SS 22.1
  mV/dec, VT_cc 0.701 V (V2 order: 93.2 mV/dec, 0.217 V); 300 K is unchanged (0.432 vs 0.435 V, 90.6 vs 90.8). So every
  V2-order result below 300 K (77 K PGM/ERS, the ERS stall, tscan 100-200 K, the first cool77) was a mixed 77/300 K
  calculation and is invalid; 300 K V2 results stay valid. 77 K decks must insert the MODELS line before CONTACT.
- cool77 v2 (order fixed): PGM300 block (load PGM0V -> solve init sonos -> solve prev -> read to 8 V) WORKED at true 77 K
  (Id(8 V) 6.9e-3 A). ERS300 block (load ERS saved at -12 V -> plain solve init -> solve init sonos -> solve prev) diverged
  in solve prev (n x-norm +3..+6): plain SOLVE INIT at 77 K with a charged nitride poisons the guess. v3: SONOS_ERS0V_make
  _300K.in brings both 300 K ERS states to 0 V with SOLVE INIT at 300 K (as PGM_PF does for PGM0V); SONOS_COOL77_ERS
  _order_v3.in loads them at 77 K with solve init sonos only and reads 0 -> 7 V (no -2 V excursion).

- TEST_O2 (order fixed, fresh 77 K Erase ramp) reached -12 V at 1 ns with no stall (results/atlas/order_fix_77K): the 77 K ERS
  stall was the V2 MODELS order. cool77 v3: PGM300 read at true 77 K VT_gm 3.706 / VT_cc 3.516 V, SS 22.4 (300 K 3.429 V gm). ERS reads
  with the drain ramp at Vg = 0 failed (PF: stop at 0.63 V; noTE: false 2.6 mA state at Vg = 0). Charged states loaded at 77 K show a
  1e-13 A zero-bias S/D current (fresh 1e-35 A). v4 uses the PGM300 order (gate 0 -> 1 V, drain ramp at 1 V, read 1 -> 7 V). tscan/77fix:
  300 K PGM_PF/ERS_PF + MODELS before CONTACT, O1 fresh read, solve prev after solve init, transient fall edges (make_cryo form) instead
  of SOLVE INIT after the pulses, LOAD + solve prev reads in the v4 order, Erase times RELATIVE. Not run yet.

## Rules for this project
- Keep the original 300 K decks unchanged; derive everything through make_cryo_decks.py.
- Do not tune models toward the expected conclusion; add mechanisms to both
  temperatures and report sensitivity ranges for uncalibrated parameters.
- Mark every result as Python-only, ATLAS-only or coupled, and as verified or not run.
