"""Make temperature-matched ATLAS-native (DYNASONOS) decks from the team's 300 K decks.

Base = the team's 300 K decks in original_300K/ (kept unchanged as the
original-model reference). Temperature-dependent models are ADDED to them and the
same derived deck is written for every temperature: <name>_300K.in and
<name>_77K.in differ only in `set temp=` and the T<T>K_ output prefix. Every edit
is listed below with its reason; the script stops if an expected line is missing,
so nothing changes silently.

Usage:  python atlas/make_cryo_decks.py     (SONOS, TANOS, TANS at 300 K and 77 K -> atlas/decks/)
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "original_300K"
OUT = HERE / "decks"

# Read-sweep settings shared by every Id-Vg read (VD = 0.1 V).
# Upper end 8 V (was 12 V): above ~6 V gm rises again (high-field current), which moved
# the max-gm VT to 12 V in the first 77 K run; the peak near VT (<= 5 V even for a
# 1e19 cm^-3 programmed state) is inside -2..8 V. Fewer points = shorter 77 K reads.
READ_HEADER = ("set Vrd_lo=-2\nset Vrd_hi=8\nset Vrd_step=0.1\n"
               "# read sweep: Vg from Vrd_lo to Vrd_hi in Vrd_step (V), VD=0.1 V, same for every state\n")
# Temperature-dependent Si models added to the team's 300 K SONOS deck, used
# identically at every temperature:
#   fermidirac, incomplete+ioniz : carrier statistics and dopant freeze-out
#   cvt                          : temperature-dependent inversion-layer mobility
#   bbt.kl                       : band-to-band tunneling (via Eg(T))
#   bbt.hurkx                    : statistical factor D = (nie^2-np)/((n+nie)(p+nie)) for bbt.kl,
#                                  zero in equilibrium. With the default D = 1 bbt.kl generated at
#                                  0 V (diag R6/R7: left Id-Vg branch, PGM hump); retention charge
#                                  to 1e4 s identical with and without it (diag R7b).
#   trap.tunnel                  : trap-assisted (phonon-assisted) tunneling in Si
SI_MODELS = "models region=6 fermidirac incomplete ioniz cvt bbt.kl bbt.hurkx trap.tunnel"


NI_MIN = "1e-60"   # cm^-3; below the 300 K n_i of SiO2 (~1e-57), so 300 K is unchanged


def numerics(s, T):
    """77 K convergence aids (no change in the physical models).
    - SOLVE INIT failed at 77 K (Gummel oscillation): the insulators that DYNASONOS treats
      as wide-gap semiconductors (Eg 9 eV) have n_i ~ 1e-276 cm^-3 at 77 K, which underflows
      in 64-bit arithmetic. Manual 21.11 / 3.3.3: extended precision (-160) for low T.
    - NI.MIN (MATERIAL) floors n_i of those insulators. Added at both temperatures."""
    s = re.sub(r"^(material material=\S+ semiconductor.*?)\s*$", rf"\1 ni.min={NI_MIN}", s, flags=re.M)
    if True:
        # 160-bit arithmetic at BOTH temperatures (numerics only; the two decks again differ
        # only in temperature). 300 K with 64-bit: the NIT.N steps above ~5.7e18 stalled with
        # potential updates hovering at 1e-5..1e-7 (precision floor) and 6e18 failed after
        # 25 Newton iterations; at 77 K with -160 the same steps reached 1e19 (diag R1).
        # 160-bit arithmetic at 77 K. With 64-bit the init/read converged but the first
        # Program time step stopped with "NaN or Inf in SONOS tunnel current": exp(E/kT)
        # terms exceed the 64-bit range at kT = 6.6 meV (manual 21.11). -256 if needed.
        s, k = re.subn(r"^go atlas\s*$", 'go atlas simflags="-160"', s, flags=re.M)
        if k != 1:
            sys.exit("go atlas line not found")
    return s


# Back to 0 V after a read, along converged DC steps, before a transient. "solve init" +
# "solve prev" re-applied the read bias (Vg = Vrd_hi, VD = 0.1 V): the 300 K Erase then
# started from Vg = 8 V and jumped to -1.2 V in 0.1 ns, and Newton failed (25 iterations).
RAMP_DOWN = ("solve name=drain vstep=-0.02 vfinal=0\n"
             "solve name=cgate vstep=-0.2 vfinal=0\n")

NOPF = f"models srh temperature=@temp\n{SI_MODELS}\n"
PF = f"models srh pf.nitride temperature=@temp\n{SI_MODELS}\n"

DRAIN_RAMP = ("solve vdrain=0.0001\nsolve vdrain=0.001\n"
              "solve name=drain vstep=0.001 vfinal=0.01\nsolve name=drain vstep=0.005 vfinal=0.1\n")


def models_before_method(s, block):
    """MODELS after NITRIDECHARGE and before METHOD (diag P8-P11).
    - Before METHOD: at 77 K SOLVE INIT oscillated while MODELS followed METHOD (diag A-H).
    - After NITRIDECHARGE: keeps the original order relative to the trap definition."""
    if s.count("models srh\n") != 1 or s.count("method carriers=2") != 1:
        sys.exit("models/method line not found")
    s = s.replace("models srh\n", "")
    if s.index("nitridecharge") > s.index("method carriers=2"):
        sys.exit("nitridecharge after method")
    return s.replace("method carriers=2", block + "method carriers=2")


def transient_fixes(s):
    """(a) HOLE.DEPTH: with PF.NITRIDE and NT.P > 0 the default HOLE.DEPTH (-999 eV) gives
    an infinite hole emission ("NaN or Inf in SONOS tunnel current" at the first Program
    step, diag P9/P10). Set equal to the electron trap depth (Enit).
    (b) DT.MAX 2e-11 s during the 1 ns gate ramps: the time step jumped to ~0.6 ns near
    Vg = 13 V and the solution diverged (diag P10d); with the cap it reaches 16 V (P11a/c)."""
    s, k = re.subn(r"elec\.depth=@Enit(?! hole)", "elec.depth=@Enit hole.depth=@Enit", s)
    if k != 1:
        sys.exit("nitridecharge elec.depth not found")
    # (c) The 1 ns linear ramp is split at 10 % of the final voltage (0.1 ns), same ramp
    # rate: at 77 K the gate passes VT (~0.8 V) where the channel charge changes by
    # ~16 decades per 0.32 V (SS ~20 mV/dec) and Newton diverged at t = 51 ps with
    # DT.MAX 2e-11 (diag P11d). First segment DT.MAX 2e-12 (0.032 V per step).
    # (d) Final ramp form = diag P14, the first 77 K Program run that reached 16 V / 10 ns:
    # DT.MAX 5e-12 over the whole 1 ns ramp and NO PROJ on the ramp solves. With PROJ the
    # extrapolated guess made the tunnel current NaN near Vg 2.1-2.4 V at 77 K for every
    # time step tried (P12, P13, P13b, P15b); PROJ is kept for the constant-bias hold.
    def split(m):
        v = m.group(1)                       # vcgate or ecgate
        return (f"set {v}_split=${v}/10\n"
                f"method dt.max=5e-12\n"
                f"solve vcgate=${v}_split ramptime=1e-10 tstep=1e-12 tfinal=1e-10\n"
                f"solve vcgate=${v} ramptime=9e-10 tstep=2e-12 tfinal=1e-9\n"
                f"method dt.max=1e-3 dt.min=1.0e-9\n")
    s, k = re.subn(r"solve vcgate=\$([ve]cgate) ramptime=1e-9 tstep=1e-12 tfinal=1e-9( proj)?\nmethod dt\.min=1\.0e-9\n",
                   split, s)
    return s, k


def models_before_contact(s, block):
    """Manual 2.5.2: MATERIAL -> MODELS -> CONTACT -> INTERFACE -> METHOD -> SOLVE.
    The originals put MODELS after METHOD/PROBE; at 300 K (= ATLAS default T) this
    is harmless, at 77 K SOLVE INIT oscillated until MODELS was moved (diag H)."""
    if s.count("models srh\n") != 1 or s.count("contact name=cgate") != 1:
        sys.exit("models/contact line not found")
    s = s.replace("models srh\n", "")
    return s.replace("contact name=cgate", block + "contact name=cgate")


def charge_ramp(s):
    """Insert the trapped charge in small steps. SOLVE NIT.N OVERWRITES the trapped
    density in the box (measured: after 10 x 1e17 + 40 x 2.5e17 the PGM .str held exactly
    2.5e17 cm^-3 everywhere, probe 2.2e17), although the manual calls it cumulative. The
    team's original (1e18 then 1e19) therefore ends at 1e19 (teammate probe: 9.0e18).
    One 1e18 step did not converge at 77 K, so the value is raised in 2.5e17 steps
    (the size that converged) up to 3.75e18, then 1.25e17 steps (diag R1) to the
    original final value 1e19."""
    lines = s.split("\n")
    idx = [k for k, l in enumerate(lines) if l.startswith("solve nit.xmin=")]
    if len(idx) != 2 or not lines[idx[0]].endswith("nit.n=1e18") or not lines[idx[1]].endswith("nit.n=1e19"):
        sys.exit("nit.n lines not as in the original")
    first = lines[idx[0]][:-len("nit.n=1e18")]
    second = lines[idx[1]][:-len("nit.n=1e19")]
    # 2.5e17 steps up to 3.75e18, then 1.25e17 steps to 1e19: at 77 K the 2.5e17 step from
    # 3.75e18 to 4e18 stopped ("Internal error in linear solver"); with half steps above
    # 3.75e18 diag R1 reached 1e19 (77 K, 9.4 min without reads).
    vals = [1e17] + [2.5e17 * k for k in range(1, 16)] + [3.75e18 + 1.25e17 * k for k in range(1, 51)]
    new1 = ["# NIT.N overwrites (not cumulative): raise the value step by step to the original final 1e19"] \
        + [first + f"nit.n={v:.4g}".replace("e+", "e") for v in vals if v <= 1e18]
    new2 = [second + f"nit.n={v:.4g}".replace("e+", "e") for v in vals if v > 1e18]
    lines = lines[:idx[0]] + new1 + lines[idx[0]+1:idx[1]] + new2 + lines[idx[1]+1:]
    return "\n".join(lines)


def drain_ramp(s):
    """Raise VD to 0.1 V in small steps (as in the converged 77 K read decks) instead
    of one 0.1 V step, which needed 4 bias-step halvings at 77 K (diag H)."""
    n = s.count("solve vdrain=0.1\n")
    s = s.replace("solve vdrain=0.1\n", DRAIN_RAMP)
    s = s.replace("solve vdrain=0 vstep=0.01 name=drain vfinal=0.1\n", DRAIN_RAMP)
    if n == 0:
        sys.exit("no drain step found")
    return s


def vt_extract(state, tag, kind):
    """DeckBuild extraction on the current log (same definition as the 77 K read decks)."""
    return (f'extract name="Vt_{state}" xintercept(maxslope(curve(v."cgate",i."drain"))) datafile="{tag}_{kind}_Vt.dat"\n'
            f'extract name="Vt_{state}_vd2" xintercept(maxslope(curve(v."cgate",i."drain"))) - ave(v."drain")/2 datafile="{tag}_{kind}_Vt.dat"\n'
            f'extract name="IdVg_{state}" curve(v."cgate",i."drain") outfile="{tag}_{kind}_{state}_IdVg.dat"\n')


def sub(text, old, new, count=1):
    n = text.count(old)
    if n != count:
        sys.exit(f"expected {count}x {old!r}, found {n}")
    return text.replace(old, new)


def prg_ers(src, T, dev):
    tag = f"T{T}K_{dev}"
    KIND = "PE"
    s = src
    s = sub(s, "set temp=300", f"set temp={T}\n" + READ_HEADER)
    s = numerics(s, T)
    # (1) temperature: the original never applies $temp in this deck (ATLAS default 300 K).
    # (2) 77 K Si statistics (Fermi-Dirac + freeze-out, IONIZ keeps 5e20 S/D ionized).
    # (3) PF.NITRIDE: temperature-dependent trap emission instead of the constant TAU only.
    # (3) Static solves (reads) WITHOUT pf.nitride, transients (Program, Erase, ERS
    # retention) WITH it, as in the retention decks (diag R3/R4; with pf.nitride in the
    # static solves the 77 K PGM read never turned the channel on up to 8 V).
    s = models_before_method(s, NOPF)
    s, k = transient_fixes(s)
    if k != 2:
        sys.exit(f"expected 2 gate ramps (PGM, ERS), found {k}")
    # (4) initial read: fixed range/step + VT extraction
    s = sub(s, "solve vcgate=0 vstep=-0.1 name=cgate vfinal=-1\nsolve vdrain=0.1\n",
            "solve vcgate=0 vstep=-0.1 name=cgate vfinal=$Vrd_lo\nsolve vdrain=0.1\n")
    s = sub(s, "solve vcgate=-1 vstep=0.1 name=cgate vfinal=6\nlog off\n",
            "solve vcgate=$Vrd_lo vstep=$Vrd_step name=cgate vfinal=$Vrd_hi\n" + vt_extract("init", tag, KIND) + "log off\n")
    # (5) PGM read: charged nitride -> solve init sonos; same range; solve init moved after log off
    # SOLVE INIT SONOS keeps the bias (here Vg = 16 V); go to 0 V by DC steps instead.
    s = re.sub(r"(save outf=\S*PGM\S*\n\n)solve init\n", r"\1solve name=cgate vstep=-0.5 vfinal=0\n", s, count=1)
    pg = re.search(r"solve vcgate=0 vstep=0\.1 name=cgate vfinal=1\nsolve vdrain=0\.1\n\n(log outf=\S*PGM\S* master)\n"
                   r"solve vcgate=\d+ vstep=0\.1 name=cgate vfinal=\d+\n\nsolve init\nlog off\n", s)
    if not pg:
        sys.exit("PGM read block not found")
    s = s.replace(pg.group(0),
                  "solve vcgate=0 vstep=-0.1 name=cgate vfinal=$Vrd_lo\nsolve vdrain=0.1\n\n"
                  f"{pg.group(1)}\nsolve vcgate=$Vrd_lo vstep=$Vrd_step name=cgate vfinal=$Vrd_hi\n"
                  + vt_extract("PGM", tag, KIND) + "log off\nsolve init sonos\n")
    # (6) erase starts from the charged nitride -> solve init sonos
    s = sub(s, "#################### Erase #########################\nsolve init\n",
            "#################### Erase #########################\nsolve init sonos\n")
    # (7) ERS read
    s = re.sub(r"(save outf=\S*ERS\S*\n\n)solve init\n", r"\1solve name=cgate vstep=0.5 vfinal=0\n", s, count=1)
    s = sub(s, "solve vcgate=0 vstep=-0.1 name=cgate vfinal=-2\nsolve vdrain=0.1\n",
            "solve vcgate=0 vstep=-0.1 name=cgate vfinal=$Vrd_lo\nsolve vdrain=0.1\n")
    s = sub(s, "solve vcgate=-2 vstep=0.1 name=cgate vfinal=7\n",
            "solve vcgate=$Vrd_lo vstep=$Vrd_step name=cgate vfinal=$Vrd_hi\n" + vt_extract("ERS", tag, KIND))
    # (c) start each P/E transient from a full carrier solution at 0 V, as in the
    # validated diag P11a/c (SOLVE INIT is a zero-carrier initial guess only).
    s = sub(s, "#################### PROGRAM #######################\n\nsolve init\n",
            "#################### PROGRAM #######################\n\nsolve init\nsolve prev\n")
    s = sub(s, "#################### Erase #########################\nsolve init sonos\n",
            "#################### Erase #########################\nsolve init sonos\nsolve prev\n")
    # (8) ERS-state retention (team review item 4): the memory window is
    # VT_PGM(t) - VT_ERS(t), so the erased state is also held at 0 V for @Retime with the
    # same transient settings as the retention deck, starting from the real erased state
    # (SOLVE INIT SONOS keeps the trapped charge: checked in the first 77 K retention run).
    m = re.search(rf'(outfile="{tag}_{KIND}_ERS_IdVg.dat"\n)\s*log off\nquit\s*$', s)
    if not m:
        sys.exit("end of ERS read not found")
    s = s[:m.start()] + m.group(1) + (
        "log off\n\n"
        "################ ERS retention (added) ################\n"
        "solve init sonos\n"
        "method lte2step tol.time=1.0e-4 tstep.incr=1.2 dt.max=1.0e7\n"
        "log outfile=TRNS_ERS_Retention.log sonos.curr j.tun\n"
        "solve tstep=1e-6 tfinal=@Retime proj\n"
        f'extract name="Qnit_ERS_vs_t" curve(time, probe."netcharge") outfile="{tag}_ERS_netcharge_vs_time.dat"\n'
        f"save outf={dev}_ERS_RETEN.str\n"
        "log off\n\n"
        "################ Vt after ERS retention ################\n"
        "solve init sonos\nsolve prev\n"
        "solve vcgate=0 vstep=-0.1 name=cgate vfinal=$Vrd_lo\nsolve vdrain=0.1\n\n"
        f"log outf={dev}_ERS_RETEN.log master\n"
        "solve vcgate=$Vrd_lo vstep=$Vrd_step name=cgate vfinal=$Vrd_hi\n"
        + vt_extract("ERSRET", tag, KIND) + "log off\nquit\n")
    # (9) Program, Erase and the ERS retention start at 0 V on every electrode (as in the
    # original's intent: PGM +16 V / ERS -12 V with S/D/substrate grounded), reached by
    # RAMP_DOWN from the preceding read instead of solve init + solve prev.
    s = sub(s, "#################### PROGRAM #######################\n\nsolve init\nsolve prev\n",
            "#################### PROGRAM #######################\n\n" + RAMP_DOWN)
    s = sub(s, "log off\nsolve init sonos\n", "log off\n")             # after the PGM read
    s = sub(s, "#################### Erase #########################\nsolve init sonos\nsolve prev\n",
            "#################### Erase #########################\n" + RAMP_DOWN)
    s = sub(s, "################ ERS retention (added) ################\nsolve init sonos\n",
            "################ ERS retention (added) ################\n" + RAMP_DOWN)
    # (10) pf.nitride on for each transient, off for each read; a read after a pulse starts
    # from the .str saved at the end of the pulse (LOAD restores the trapped charge, R5a).
    s = sub(s, "#################### PROGRAM #######################\n\n" + RAMP_DOWN,
            "#################### PROGRAM #######################\n\n" + RAMP_DOWN + PF)
    s = sub(s, "#################### Erase #########################\n" + RAMP_DOWN,
            "#################### Erase #########################\n" + RAMP_DOWN + PF)
    s = sub(s, "################ ERS retention (added) ################\n" + RAMP_DOWN,
            "################ ERS retention (added) ################\n" + RAMP_DOWN + PF)
    s = drain_ramp(s)
    s = prefix_outputs(s, tag, KIND)
    for key, step in (("_PGM_nt_", "-0.5"), ("_ERS_nt_", "0.5")):
        m = re.findall(rf"save outf=(\S*{key}\S*\.str)\n", s)
        if len(m) != 1:
            sys.exit(f"saved {key} .str not found")
        s = sub(s, f"save outf={m[0]}\n\nsolve name=cgate vstep={step} vfinal=0\n",
                f"save outf={m[0]}\n\n{NOPF}load infile={m[0]} master\nsolve name=cgate vstep={step} vfinal=0\n")
    s = sub(s, "################ Vt after ERS retention ################\n",
            "################ Vt after ERS retention ################\n" + NOPF)
    return read_from_saved(s, "_ERS_RETEN")


def retention(src, T, dev):
    tag = f"T{T}K_{dev}"
    KIND = "RET"
    s = src
    s = sub(s, "set temp=300", f"set temp={T}\n" + READ_HEADER)
    s = numerics(s, T)
    # (1)+(2): every MODELS statement carries the temperature (persistence between
    # MODELS statements is not documented) and the 77 K Si statistics.
    # (3) Model sets, following the team original's order but without `mos`:
    #   injection + initial/PGM/RET reads : srh + Si models (no pf.nitride)
    #   retention transient               : srh pf.nitride + Si models
    # With pf.nitride during the static NIT.N injection, 300 K stalled at 5e17 (diag R3;
    # without it 1e19 in 3 Newton iterations per step, R3c). Re-specifying MODELS before the
    # retention works at 77 K and 300 K (diag R4). The three reads use the same models
    # (team review item 2: the original read after retention used `srh mos`).
    s = models_before_method(s, f"models srh temperature=@temp\n{SI_MODELS}\n")
    s, _ = transient_fixes(s)
    s = sub(s, "models mos srh pf.nitride temperature=@temp\n",
            f"# pf.nitride for the retention transient only (diag R3/R4)\nmodels srh pf.nitride temperature=@temp\n{SI_MODELS}\n")
    # (4) initial read
    s = sub(s, "solve vcgate=0 vstep=-0.1 name=cgate vfinal=-1\nsolve vdrain=0.1\n",
            "solve vcgate=0 vstep=-0.1 name=cgate vfinal=$Vrd_lo\nsolve vdrain=0.1\n")
    s = sub(s, "solve vcgate=-1 vstep=0.1 name=cgate vfinal=3\nlog off\n\n\n####",
            "solve vcgate=$Vrd_lo vstep=$Vrd_step name=cgate vfinal=$Vrd_hi\n" + vt_extract("init", tag, KIND) + "log off\n\n\n####")
    # (5) PGM read after nit.n: same range; solve init moved after log off
    s = sub(s, "solve vcgate=0 vstep=0.1 name=cgate vfinal=2\nsolve vdrain=0.1\n",
            "solve vcgate=0 vstep=-0.1 name=cgate vfinal=$Vrd_lo\nsolve vdrain=0.1\n")
    s = sub(s, "solve vcgate=2 vstep=0.1 name=cgate vfinal=6\n\nsolve init\nlog off\n",
            "solve vcgate=$Vrd_lo vstep=$Vrd_step name=cgate vfinal=$Vrd_hi\n" + vt_extract("PGM", tag, KIND)
            + "log off\n" + RAMP_DOWN)
    # (5a) SOLVE INIT SONOS keeps the electrode biases: after the PGM read it re-solved at
    # Vg = 8 V, VD = 0.1 V with 1e19 trapped and failed (77 K, "bias step cut back"), and
    # the retention transient then started from that broken solution (NaN in the SONOS
    # tunnel current). The retention starts from 0 V reached by RAMP_DOWN instead.
    s = sub(s, "solve init sonos\n\n#solve prev\n", "#solve prev\n")
    # (5b) trapped charge vs time during retention, for the Python coupling (python_cryo/)
    # (5c) the retention transient is split at 1 s and 1e4 s with a .str saved at each,
    # to see when the trapped charge redistributes inside the nitride (first 77 K run:
    # it moved to the blocking-oxide side). Same time-step control, the solve continues.
    s = sub(s, "solve tstep=1e-6 tfinal=@Retime proj\n",
            "solve tstep=1e-6 tfinal=1 proj\n"
            f"save outf={dev}_RETEN_t1s.str\n"
            "solve tstop=1e4 proj\n"
            f"save outf={dev}_RETEN_t1e4s.str\n"
            "solve tstop=@Retime proj\n"
            f'extract name="Qnit_vs_t" curve(time, probe."netcharge") outfile="{tag}_netcharge_vs_time.dat"\n')
    # (6) read after retention: charged nitride
    s = sub(s, "models srh mos\nsolve init\nsolve prev\n",
            f"# same models as the initial and PGM reads (original: srh mos)\nmodels srh temperature=@temp\n{SI_MODELS}\nsolve init sonos\nsolve prev\n")
    s = sub(s, "solve vcgate=0 vstep=-0.1 name=cgate vfinal=-1\n\nsolve vdrain=0 vstep=0.01 name=drain vfinal=0.1\n",
            "solve vcgate=0 vstep=-0.1 name=cgate vfinal=$Vrd_lo\n\nsolve vdrain=0 vstep=0.01 name=drain vfinal=0.1\n")
    s = sub(s, "solve vcgate=-1 vstep=0.1 name=cgate vfinal=3\n\nlog off\nquit",
            "solve vcgate=$Vrd_lo vstep=$Vrd_step name=cgate vfinal=$Vrd_hi\n" + vt_extract("RET", tag, KIND) + "\nlog off\nquit")
    s = charge_ramp(s)
    s = drain_ramp(s)
    return read_from_saved(prefix_outputs(s, tag, KIND), "_RETEN_nt_")


def read_from_saved(s, key):
    """Start the read after a retention transient from the .str just saved, with LOAD (manual
    2.10.5), instead of SOLVE INIT SONOS + SOLVE PREV. At 300 K the in-run read after 3e8 s
    failed at the first gate step after SOLVE INIT SONOS; loading the saved .str (diag R5b)
    read the same state without problems, and diag R5a showed LOAD restores the trapped
    charge exactly (same netcharge and VT as the in-run PGM read)."""
    m = re.findall(rf"save outf=(\S*{key}\S*\.str)\n", s)
    if len(m) != 1:
        sys.exit(f"saved {key} .str not found")
    return sub(s, "solve init sonos\nsolve prev\n", f"load infile={m[0]} master\nsolve prev\n")


def prefix_outputs(s, tag, kind):
    """Prefix every .str/.log name with T<T>K_<PE|RET>_ so temperatures and the two
    decks (P/E and retention, which reuse names in the originals) never overwrite."""
    s = re.sub(r"(save outf=|log outf=|log outfile=)", lambda m: m.group(1) + tag.split("_")[0] + f"_{kind}_", s)
    return s


DEVICES = (("SONOS", "SONOS_PRG_ERS.in", "SONOS_retention.in"),
           ("TANOS", "TANOS.in", "TANOS_Retention.in"),
           ("TANS", "TANS.in", "TANS_Retention.in"))


def main(devices=DEVICES, temps=(300, 77)):
    OUT.mkdir(exist_ok=True)
    for dev, pe, ret in devices:
        for T in temps:
            (OUT / f"{dev}_PRG_ERS_{T}K.in").write_text(prg_ers((SRC / pe).read_text(), T, dev))
            (OUT / f"{dev}_retention_{T}K.in").write_text(retention((SRC / ret).read_text(), T, dev))
            print("wrote", f"{dev}_PRG_ERS_{T}K.in", f"{dev}_retention_{T}K.in")


if __name__ == "__main__":
    main()
