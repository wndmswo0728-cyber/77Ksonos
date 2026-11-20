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
READ_HEADER = ("set Vrd_lo=-2\nset Vrd_hi=12\nset Vrd_step=0.02\n"
               "# read sweep: Vg from Vrd_lo to Vrd_hi in Vrd_step (V), VD=0.1 V, same for every state\n")
# Temperature-dependent Si models added to the team's 300 K SONOS deck, used
# identically at every temperature:
#   fermidirac, incomplete+ioniz : carrier statistics and dopant freeze-out
#   cvt                          : temperature-dependent inversion-layer mobility
#   bbt.kl                       : band-to-band tunneling (via Eg(T))
#   trap.tunnel                  : trap-assisted (phonon-assisted) tunneling in Si
SI_MODELS = "models region=6 fermidirac incomplete ioniz cvt bbt.kl trap.tunnel"


NI_MIN = "1e-60"   # cm^-3; below the 300 K n_i of SiO2 (~1e-57), so 300 K is unchanged


def numerics(s, T):
    """77 K convergence aids (no change in the physical models).
    - SOLVE INIT failed at 77 K (Gummel oscillation): the insulators that DYNASONOS treats
      as wide-gap semiconductors (Eg 9 eV) have n_i ~ 1e-276 cm^-3 at 77 K, which underflows
      in 64-bit arithmetic. Manual 21.11 / 3.3.3: extended precision (-160) for low T.
    - NI.MIN (MATERIAL) floors n_i of those insulators. Added at both temperatures."""
    s = re.sub(r"^(material material=\S+ semiconductor.*?)\s*$", rf"\1 ni.min={NI_MIN}", s, flags=re.M)
    if T < 200:
        s, k = re.subn(r"^go atlas\s*$", 'go atlas simflags="-160"', s, flags=re.M)
        if k != 1:
            sys.exit("go atlas line not found")
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
    s = sub(s, "models srh\n", f"models srh pf.nitride temperature=@temp\n{SI_MODELS}\n")
    # (4) initial read: fixed range/step + VT extraction
    s = sub(s, "solve vcgate=0 vstep=-0.1 name=cgate vfinal=-1\nsolve vdrain=0.1\n",
            "solve vcgate=0 vstep=-0.1 name=cgate vfinal=$Vrd_lo\nsolve vdrain=0.1\n")
    s = sub(s, "solve vcgate=-1 vstep=0.1 name=cgate vfinal=6\nlog off\n",
            "solve vcgate=$Vrd_lo vstep=$Vrd_step name=cgate vfinal=$Vrd_hi\n" + vt_extract("init", tag, KIND) + "log off\n")
    # (5) PGM read: charged nitride -> solve init sonos; same range; solve init moved after log off
    s = re.sub(r"(save outf=\S*PGM\S*\n\n)solve init\n", r"\1solve init sonos\n", s, count=1)
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
    s = re.sub(r"(save outf=\S*ERS\S*\n\n)solve init\n", r"\1solve init sonos\n", s, count=1)
    s = sub(s, "solve vcgate=0 vstep=-0.1 name=cgate vfinal=-2\nsolve vdrain=0.1\n",
            "solve vcgate=0 vstep=-0.1 name=cgate vfinal=$Vrd_lo\nsolve vdrain=0.1\n")
    s = sub(s, "solve vcgate=-2 vstep=0.1 name=cgate vfinal=7\n",
            "solve vcgate=$Vrd_lo vstep=$Vrd_step name=cgate vfinal=$Vrd_hi\n" + vt_extract("ERS", tag, KIND))
    return prefix_outputs(s, tag, KIND)


def retention(src, T, dev):
    tag = f"T{T}K_{dev}"
    KIND = "RET"
    s = src
    s = sub(s, "set temp=300", f"set temp={T}\n" + READ_HEADER)
    s = numerics(s, T)
    # (1)+(2): every MODELS statement carries the temperature (persistence between
    # MODELS statements is not documented) and the 77 K Si statistics.
    s = sub(s, "models srh\n", f"models srh temperature=@temp\n{SI_MODELS}\n")
    s = sub(s, "models mos srh pf.nitride temperature=@temp\n",
            f"models mos srh pf.nitride temperature=@temp\n{SI_MODELS}\n")
    s = sub(s, "models srh mos\n", f"models srh mos temperature=@temp\n{SI_MODELS}\n")
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
            + "log off\nsolve init sonos\n")
    # (5b) trapped charge vs time during retention, for the Python coupling (python_cryo/)
    s = sub(s, "solve tstep=1e-6 tfinal=@Retime proj\n",
            "solve tstep=1e-6 tfinal=@Retime proj\n"
            f'extract name="Qnit_vs_t" curve(time, probe."netcharge") outfile="{tag}_netcharge_vs_time.dat"\n')
    # (6) read after retention: charged nitride
    s = sub(s, f"{SI_MODELS}\nsolve init\nsolve prev\n", f"{SI_MODELS}\nsolve init sonos\nsolve prev\n")
    s = sub(s, "solve vcgate=0 vstep=-0.1 name=cgate vfinal=-1\n\nsolve vdrain=0 vstep=0.01 name=drain vfinal=0.1\n",
            "solve vcgate=0 vstep=-0.1 name=cgate vfinal=$Vrd_lo\n\nsolve vdrain=0 vstep=0.01 name=drain vfinal=0.1\n")
    s = sub(s, "solve vcgate=-1 vstep=0.1 name=cgate vfinal=3\n\nlog off\nquit",
            "solve vcgate=$Vrd_lo vstep=$Vrd_step name=cgate vfinal=$Vrd_hi\n" + vt_extract("RET", tag, KIND) + "\nlog off\nquit")
    return prefix_outputs(s, tag, KIND)


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
