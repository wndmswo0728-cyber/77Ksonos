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

- Diag B1 (300 K): a static solve with PF.NITRIDE diverges (NaN) from a converged 1e19 state:
  in static solves the trap occupancy is frozen but the PF emission term still feeds free electrons
  into the nitride (no steady state). Keep PF.NITRIDE out of static solves (correct, not a bypass).
- Diag B2/B3: after a transient, SOLVE INIT SONOS + SOLVE PREV leaves a stale initial guess (the
  next solve at the SAME 0 V starts with a 1e-1.4 potential update and fails); without the
  transient (B2) it works; METHOD reset does not help (B3b). save -> LOAD restarts from the saved
  solution, so reads after transients use LOAD.

## Rules for this project
- Keep the original 300 K decks unchanged; derive everything through make_cryo_decks.py.
- Do not tune models toward the expected conclusion; add mechanisms to both
  temperatures and report sensitivity ranges for uncalibrated parameters.
- Mark every result as Python-only, ATLAS-only or coupled, and as verified or not run.
