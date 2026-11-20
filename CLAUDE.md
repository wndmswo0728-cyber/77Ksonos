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
  common read sweep -2..12 V / 0.1 V (speed), extract lines, output names T<T>K_<PE|RET>_...
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
  Production 77 K decks use default precision (faster); -160 is a commented fallback.

## Rules for this project
- Keep the original 300 K decks unchanged; derive everything through make_cryo_decks.py.
- Do not tune models toward the expected conclusion; add mechanisms to both
  temperatures and report sensitivity ranges for uncalibrated parameters.
- Mark every result as Python-only, ATLAS-only or coupled, and as verified or not run.
