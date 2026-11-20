"""Make temperature-matched ATLAS-native (DYNASONOS) decks from the team's 300 K decks.

The 300 K originals in original_300K/ are never modified. For each temperature T
this script writes <name>_<T>K.in. The 77 K and 300 K outputs are identical
except for `set temp=` and the T<T>K_ prefix on output files. Every edit is listed
in EDITS below with its reason; the script stops if an expected line is missing,
so nothing changes silently.

Usage:  python cryo_native/make_cryo_decks.py            (SONOS, 77 K and 300 K)
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "original_300K"

# Read-sweep settings shared by every Id-Vg read (VD = 0.1 V).
READ_HEADER = ("set Vrd_lo=-2\nset Vrd_hi=12\nset Vrd_step=0.02\n"
               "# read sweep: Vg from Vrd_lo to Vrd_hi in Vrd_step (V), VD=0.1 V, same for every state\n")
SI_MODELS = "models region=6 fermidirac incomplete ioniz"


def vt_extract(state, tag):
    """DeckBuild extraction on the current log (same definition as the 77 K read decks)."""
    return (f'extract name="Vt_{state}" xintercept(maxslope(curve(v."cgate",i."drain"))) datafile="{tag}_Vt.dat"\n'
            f'extract name="Vt_{state}_vd2" xintercept(maxslope(curve(v."cgate",i."drain"))) - ave(v."drain")/2 datafile="{tag}_Vt.dat"\n'
            f'extract name="IdVg_{state}" curve(v."cgate",i."drain") outfile="{tag}_{state}_IdVg.dat"\n')


def sub(text, old, new, count=1):
    n = text.count(old)
    if n != count:
        sys.exit(f"expected {count}x {old!r}, found {n}")
    return text.replace(old, new)


def prg_ers(src, T, dev):
    tag = f"T{T}K_{dev}"
    s = src
    s = sub(s, "set temp=300", f"set temp={T}\n" + READ_HEADER)
    # (1) temperature: the original never applies $temp in this deck (ATLAS default 300 K).
    # (2) 77 K Si statistics (Fermi-Dirac + freeze-out, IONIZ keeps 5e20 S/D ionized).
    # (3) PF.NITRIDE: temperature-dependent trap emission instead of the constant TAU only.
    s = sub(s, "models srh\n", f"models srh pf.nitride temperature=@temp\n{SI_MODELS}\n")
    # (4) initial read: fixed range/step + VT extraction
    s = sub(s, "solve vcgate=0 vstep=-0.1 name=cgate vfinal=-1\nsolve vdrain=0.1\n",
            "solve vcgate=0 vstep=-0.1 name=cgate vfinal=$Vrd_lo\nsolve vdrain=0.1\n")
    s = sub(s, "solve vcgate=-1 vstep=0.1 name=cgate vfinal=6\nlog off\n",
            "solve vcgate=$Vrd_lo vstep=$Vrd_step name=cgate vfinal=$Vrd_hi\n" + vt_extract("init", tag) + "log off\n")
    # (5) PGM read: charged nitride -> solve init sonos; same range; solve init moved after log off
    s = re.sub(r"(save outf=\S*PGM\S*\n\n)solve init\n", r"\1solve init sonos\n", s, count=1)
    pg = re.search(r"solve vcgate=0 vstep=0\.1 name=cgate vfinal=1\nsolve vdrain=0\.1\n\n(log outf=\S*PGM\S* master)\n"
                   r"solve vcgate=\d+ vstep=0\.1 name=cgate vfinal=\d+\n\nsolve init\nlog off\n", s)
    if not pg:
        sys.exit("PGM read block not found")
    s = s.replace(pg.group(0),
                  "solve vcgate=0 vstep=-0.1 name=cgate vfinal=$Vrd_lo\nsolve vdrain=0.1\n\n"
                  f"{pg.group(1)}\nsolve vcgate=$Vrd_lo vstep=$Vrd_step name=cgate vfinal=$Vrd_hi\n"
                  + vt_extract("PGM", tag) + "log off\nsolve init sonos\n")
    # (6) erase starts from the charged nitride -> solve init sonos
    s = sub(s, "#################### Erase #########################\nsolve init\n",
            "#################### Erase #########################\nsolve init sonos\n")
    # (7) ERS read
    s = re.sub(r"(save outf=\S*ERS\S*\n\n)solve init\n", r"\1solve init sonos\n", s, count=1)
    s = sub(s, "solve vcgate=0 vstep=-0.1 name=cgate vfinal=-2\nsolve vdrain=0.1\n",
            "solve vcgate=0 vstep=-0.1 name=cgate vfinal=$Vrd_lo\nsolve vdrain=0.1\n")
    s = sub(s, "solve vcgate=-2 vstep=0.1 name=cgate vfinal=7\n",
            "solve vcgate=$Vrd_lo vstep=$Vrd_step name=cgate vfinal=$Vrd_hi\n" + vt_extract("ERS", tag))
    return prefix_outputs(s, tag)


def retention(src, T, dev):
    tag = f"T{T}K_{dev}"
    s = src
    s = sub(s, "set temp=300", f"set temp={T}\n" + READ_HEADER)
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
            "solve vcgate=$Vrd_lo vstep=$Vrd_step name=cgate vfinal=$Vrd_hi\n" + vt_extract("init", tag) + "log off\n\n\n####")
    # (5) PGM read after nit.n: same range; solve init moved after log off
    s = sub(s, "solve vcgate=0 vstep=0.1 name=cgate vfinal=2\nsolve vdrain=0.1\n",
            "solve vcgate=0 vstep=-0.1 name=cgate vfinal=$Vrd_lo\nsolve vdrain=0.1\n")
    s = sub(s, "solve vcgate=2 vstep=0.1 name=cgate vfinal=6\n\nsolve init\nlog off\n",
            "solve vcgate=$Vrd_lo vstep=$Vrd_step name=cgate vfinal=$Vrd_hi\n" + vt_extract("PGM", tag)
            + "log off\nsolve init sonos\n")
    # (6) read after retention: charged nitride
    s = sub(s, f"{SI_MODELS}\nsolve init\nsolve prev\n", f"{SI_MODELS}\nsolve init sonos\nsolve prev\n")
    s = sub(s, "solve vcgate=0 vstep=-0.1 name=cgate vfinal=-1\n\nsolve vdrain=0 vstep=0.01 name=drain vfinal=0.1\n",
            "solve vcgate=0 vstep=-0.1 name=cgate vfinal=$Vrd_lo\n\nsolve vdrain=0 vstep=0.01 name=drain vfinal=0.1\n")
    s = sub(s, "solve vcgate=-1 vstep=0.1 name=cgate vfinal=3\n\nlog off\nquit",
            "solve vcgate=$Vrd_lo vstep=$Vrd_step name=cgate vfinal=$Vrd_hi\n" + vt_extract("RET", tag) + "\nlog off\nquit")
    return prefix_outputs(s, tag)


def prefix_outputs(s, tag):
    """Prefix every .str/.log name with T<T>K_ so 77 K and 300 K runs never overwrite each other."""
    s = re.sub(r"(save outf=|log outf=|log outfile=)", lambda m: m.group(1) + tag.split("_")[0] + "_", s)
    return s


def main(devices=(("SONOS", "SONOS_PRG_ERS.in", "SONOS_retention.in"),), temps=(77, 300)):
    for dev, pe, ret in devices:
        for T in temps:
            (HERE / f"{dev}_PRG_ERS_{T}K.in").write_text(prg_ers((SRC / pe).read_text(), T, dev))
            (HERE / f"{dev}_retention_{T}K.in").write_text(retention((SRC / ret).read_text(), T, dev))
            print("wrote", f"{dev}_PRG_ERS_{T}K.in", f"{dev}_retention_{T}K.in")


if __name__ == "__main__":
    main()
