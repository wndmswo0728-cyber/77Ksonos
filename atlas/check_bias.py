"""Bias trace of a generated deck (static check, no ATLAS run).

Follows Vg and VD statement by statement (solve init, DC sweeps and steps, transient ramps,
save/load of .str states) and reports the bias at every read start, NIT.N injection, pulse
rise and retention start. A DC step whose vstep points away from vfinal is a problem: ATLAS
leaves the bias where it is. That is how the 300 K SONOS retention run of 2026-11-22 ran
3e8 s at Vg = -2 V (the read ended at -2 V and RAMP_DOWN stepped with vstep=-0.2 to 0 V).

Usage: python atlas/check_bias.py atlas/decks/*.in   (exit 1 on a problem)
"""
import re
import sys

VARS = {"$Vrd_hi": 8.0, "$Vrd_lo": -2.0, "$vcgate": 16.0, "$vcgate_split": 1.6,
        "$ecgate": -12.0, "$ecgate_split": -1.2, "$Vrd_step": 0.1, "-$Vrd_step": -0.1}


def val(x):
    return VARS[x] if x in VARS else float(x)


def trace(path):
    """Returns (events, problems)."""
    vg = vd = 0.0; saved = {}; out = []; bad = []
    for i, l in enumerate(open(path).read().split("\n"), 1):
        l = l.strip()
        if l == "solve init": vg = vd = 0.0
        elif l.startswith("save outf="): saved[l.split("=", 1)[1]] = (vg, vd)
        elif l.startswith("load infile="):
            k = l.split("=", 1)[1].replace(" master", "")
            if k not in saved: bad.append((i, "load of a .str not saved in this deck")); continue
            vg, vd = saved[k]
        elif m := re.match(r"solve vcgate=(\S+) vstep=(\S+) name=cgate vfinal=(\S+)", l):
            if l.startswith("solve vcgate=0 vstep="): out.append((i, "read sweep starts at", vg, vd))
            a, st, b = val(m[1]), val(m[2]), val(m[3])
            vg = b if (b - a) * st > 0 or a == b else a
            if (b - a) * st < 0: bad.append((i, "gate sweep in the wrong direction"))
        elif m := re.match(r"solve name=(cgate|drain) vstep=(\S+) vfinal=(\S+)", l):
            cur = vg if m[1] == "cgate" else vd; st, b = val(m[2]), val(m[3])
            if abs(cur - b) > 1e-12 and (b - cur) * st < 0:
                bad.append((i, f"{m[1]} step cannot reach {b} from {cur}"))
            else:
                cur = b
            if m[1] == "cgate": vg = cur
            else: vd = cur
        elif m := re.match(r"solve vdrain=(\S+)", l): vd = val(m[1])
        elif m := re.match(r"solve vcgate=(\S+) ramptime", l):
            if "tfinal=1e-10" in l and "split" in l: out.append((i, "pulse rise starts at", vg, vd))
            vg = val(m[1])
        elif re.match(r"solve tstep=1e-6 tfinal=1 ", l): out.append((i, "retention starts at", vg, vd))
        elif "nit.n=" in l and l.startswith("solve"): out.append((i, "nit.n at", vg, vd))
    for i, what, g, d in out:
        if what != "read sweep starts at" and (g, d) != (0.0, 0.0):
            bad.append((i, f"{what} Vg={g} VD={d}, expected 0 V"))
        if what == "read sweep starts at" and (g, d) != (0.0, 0.1):
            bad.append((i, f"read starts at Vg={g} VD={d}, expected 0 / 0.1 V"))
    return out, bad


if __name__ == "__main__":
    fail = False
    for f in sys.argv[1:]:
        _, bad = trace(f)
        print(f, "OK" if not bad else bad)
        fail |= bool(bad)
    sys.exit(1 if fail else 0)
