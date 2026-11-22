"""Couple the ATLAS (DYNASONOS) retention results with the mechanisms ATLAS lacks.

ATLAS computes retention with PF emission, ELASTIC trap<->band tunneling, capture and
emission. It has no nitride hopping, no phonon-assisted (multiphonon) trap ionization
and no Franck-Condon (phonon-assisted) weighting of trap<->electrode tunneling.
For each device and temperature this script

 1. runs the Python model (cryo_model.py) twice from the same initial charge as the
    ATLAS run: the trapped density is taken from the ATLAS probe Q(0) of that run
    (|Q|/q over the 1 um x 7 nm x 1 um nitride); without ATLAS data, the nominal
    nit.n = 1e19 cm^-3 (NIT.N overwrites, so the deck ends at 1e19; Nnit = 5e19):
        base : channels ATLAS also has (elastic WKB exchange), Python PF/thermal OFF
        full : activated hopping + phonon-assisted ionization (above PF)
               + Franck-Condon weighted trap<->electrode tunneling (replaces elastic)
 2. forms F(t) = Q_full(t) / Q_base(t);
 3. if the ATLAS outputs exist, multiplies the ATLAS trapped charge Q_ATLAS(t)
    (T<T>K_<DEV>_netcharge_vs_time.dat) by F(t) and converts it to VT(t) with
        VT(t) = VT_init + (VT_PGM - VT_init) * Q(t) / Q(0)
    (VT_init, VT_PGM, VT_RET re-extracted from the Id-Vg files: max-gm tangent at the
    first gm peak, because above ~6 V gm rises again and the deck's own extraction
    then picks the end of the sweep), and the memory window
        MW(t) = VT_PGM(t) - VT_ERS(t)
    with VT_ERS(t) from the ERS-state retention appended to the P/E deck
    (T<T>K_<DEV>_ERS_netcharge_vs_time.dat, coupled the same way). If that file is
    missing, VT_ERS is the constant post-erase value (marked "const" in the output;
    this overstates the window where the erased state drifts, e.g. at 300 K).
    as in Hur et al., Adv. Electron. Mater. 2023, 9, 2201299 (window open at 10 years).
    F(t) can exceed 1 for TANS: the elastic loss that ATLAS computes is reduced by the
    Franck-Condon factor, so the coupling also removes part of the ATLAS loss.

Assumptions (state them in the report): first-order, multiplicative coupling; the
charge centroid does not move (VT linear in Q). Hopping / multiphonon parameters are
literature-motivated, not calibrated: they are varied in --sensitivity.

Usage:
  python python_cryo/couple_atlas.py                       # Python factors (+ ATLAS if present)
  python python_cryo/couple_atlas.py --atlas-dir results/atlas --devices SONOS
  python python_cryo/couple_atlas.py --sensitivity
"""
import argparse
import csv
import re
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cryo_model as cm  # noqa: E402

RETENTION_S = 3e8                 # ATLAS Retime
NNIT = 5e19                       # cm^-3, team value
NIT_VOL_CM3 = 1e-4 * 7e-7 * 1e-4  # nitride under the gate per um width: Lg 1 um x 7 nm x 1 um
Q_E = 1.602176634e-19
OCC0 = (1e19 / NNIT, 0.0)         # nominal: NIT.N overwrites, the deck ends at 1e19


def occ_from_q(q0):
    """(electron, hole) trap occupancy from the ATLAS probe net charge (C/um)."""
    frac = min(abs(q0) / Q_E / NIT_VOL_CM3 / NNIT, 1.0)
    return (frac, 0.0) if q0 < 0 else (0.0, frac)
BASE = dict(thermal_emission=False, hopping=False, pat=False)
FULL = dict(thermal_emission=False, hopping=True, pat=True, fc_tunnel=True,
            hop_distance_nm=1.5, hop_ea=1.2)


def python_run(device, T, extra, occ0=OCC0):
    hist, snap = cm.simulate(device, cm.Options(temperature=T, retention_s=RETENTION_S, **extra),
                             retention_from=occ0)
    rows = [r for r in hist if r[0] == "retention"]
    t = np.array([r[1] for r in rows])
    q = np.array([r[3] for r in rows])        # net sheet charge, C/m^2
    dvt = np.array([r[4] for r in rows])
    return t, q, dvt


def survival_factor(device, T, full=FULL, occ0=OCC0):
    t, qb, dvb = python_run(device, T, BASE, occ0)
    t2, qf, dvf = python_run(device, T, full, occ0)
    assert np.allclose(t, t2)
    with np.errstate(divide="ignore", invalid="ignore"):
        f = np.where(np.abs(qb) > 1e-12 * np.abs(qb[0]), qf / qb, 0.0)
    return t, f, dvb, dvf


def read_two_columns(path):
    rows = []
    for line in Path(path).read_text(errors="replace").splitlines():
        toks = line.split()
        if len(toks) == 2:
            try:
                rows.append((float(toks[0]), float(toks[1])))
            except ValueError:
                pass
    return np.array(rows)


def read_vt(path):
    vals = {}
    for m in re.finditer(r"(Vt_\w+?)=\s*([-+0-9.eE]+)", Path(path).read_text(errors="replace")):
        vals[m.group(1)] = float(m.group(2))
    return vals


def read_idvg(path):
    """Id-Vg of one read: the up sweep (<name>.dat, 0 -> Vrd_hi) merged with the down sweep
    (<name>_neg.dat, 0 -> Vrd_lo) when present, sorted by Vg (reads start at 0 V both ways)."""
    path = Path(path)
    d = read_two_columns(path)
    neg = path.with_name(path.stem + "_neg" + path.suffix)
    if neg.exists():
        n = read_two_columns(neg)
        if len(n):
            d = np.vstack([n[n[:, 0] < 0], d]) if len(d) else n
    return d[np.argsort(d[:, 0])] if len(d) else d


def vt_from_idvg(path):
    """Max-gm tangent VT at the FIRST gm peak (>= 30 % of the largest gm). The deck's
    extract takes the global gm maximum, which sat at the end of the sweep in the first
    77 K run (gm rises again above ~6 V)."""
    d = read_idvg(path)
    if len(d) < 5:
        return None
    v, i = d[:, 0], d[:, 1]
    g = np.gradient(i, v)
    thr = 0.3 * g.max()
    for k in range(1, len(v) - 1):
        if g[k] >= thr and g[k] >= g[k-1] and g[k] >= g[k+1]:
            return float(v[k] - i[k] / g[k])
    return None


def read_states(atlas_dir, T, device, kind, states):
    """VT per state from the Id-Vg files; falls back to the deck's Vt.dat value."""
    deck = read_vt(atlas_dir / f"T{T}K_{device}_{kind}_Vt.dat") if (atlas_dir / f"T{T}K_{device}_{kind}_Vt.dat").exists() else {}
    out = {}
    for st in states:
        f = atlas_dir / f"T{T}K_{device}_{kind}_{st}_IdVg.dat"
        # Id-Vg present but no gm peak (e.g. the read stopped early): no VT, not the deck value
        out[st] = vt_from_idvg(f) if f.exists() else deck.get(f"Vt_{st}")
    return out


def close_time(t, mw):
    """First time the memory window reaches 0 (log-interpolated); None if it stays open."""
    idx = np.where(mw <= 0)[0]
    if not len(idx):
        return None
    k = idx[0]
    if k == 0:
        return float(t[0])
    lt = np.log10(np.maximum(t[k-1:k+1], 1e-12))
    return float(10**np.interp(0, [mw[k], mw[k-1]], [lt[1], lt[0]]))


def log_fit(t, v):
    """Paper-style fit v = alpha - beta*ln(t + gamma); returns (alpha, beta, gamma)."""
    from scipy.optimize import curve_fit
    m = t > 0
    try:
        p, _ = curve_fit(lambda x, a, b, g: a - b*np.log(x + g), t[m], v[m],
                         p0=(v[m][0], 0.01, 1.0), bounds=([-50, -10, 1e-12], [50, 10, 1e6]), maxfev=20000)
        return tuple(float(x) for x in p)
    except Exception:
        return None


def log_interp(x, xp, fp):
    lx, lxp = np.log10(np.maximum(x, 1e-12)), np.log10(np.maximum(xp, 1e-12))
    return np.interp(lx, lxp, fp)


SNAP_T = (("t1s", 1.0), ("t10s", 10.0), ("t100s", 100.0), ("t1e3s", 1e3), ("t1e4s", 1e4))
TEN_Y = 3.15576e8                 # 10 years in s (ATLAS Retime 3e8 s is 9.5 y)


def paper_fit(atlas_dir, T, device):
    """ATLAS-only, Hur et al. method: VT read at 1, 10, 100, 1e3, 1e4 s after programming
    (and after erasing), fit alpha - beta*ln(t + gamma) on 1 s - 1e4 s, extrapolate to the
    end of the run (3e8 s) and to 10 y, and compare with the simulated read at 3e8 s.
    MW(t) = VT_PGM(t) - VT_ERS(t); VT_PGM(t) from the retention deck (nit.n injection),
    VT_ERS(t) from the ERS retention of the P/E deck (real Erase pulse).
    loss_per_decade = mean VT drop per decade between 1 s and 1e4 s (after the first-second
    loss of the row next to the tunnel oxide)."""
    if not atlas_dir:
        return {}
    pgm = read_states(atlas_dir, T, device, "RET", ["RET" + k for k, _ in SNAP_T] + ["RET"])
    ers = read_states(atlas_dir, T, device, "PE", ["ERS" + k for k, _ in SNAP_T] + ["ERSRET"])
    ts = np.array([t for _, t in SNAP_T])
    out = {}
    curves = {}
    for name, d, pre, final in (("PGM", pgm, "RET", "RET"), ("ERS", ers, "ERS", "ERSRET")):
        v = [d.get(pre + k) for k, _ in SNAP_T]
        if any(x is None for x in v):
            out[f"fit_{name}_status"] = "snapshot reads missing"
            continue
        v = np.array(v)
        curves[name] = v
        p = log_fit(ts, v)
        out[f"VT_{name}_snap_V"] = [round(float(x), 4) for x in v]
        out[f"VT_{name}_loss_per_decade_V"] = float((v[0] - v[-1]) / 4.0)
        out[f"VT_{name}_3e8_read_V"] = d.get(final)
        if p:
            a, b, g = p
            out[f"fit_{name}_alpha_beta_gamma"] = p
            out[f"VT_{name}_3e8_fit_V"] = a - b*np.log(RETENTION_S + g)
            out[f"VT_{name}_10y_fit_V"] = a - b*np.log(TEN_Y + g)
            if d.get(final) is not None:
                out[f"VT_{name}_3e8_fit_minus_read_V"] = out[f"VT_{name}_3e8_fit_V"] - d[final]
    if "PGM" in curves and "ERS" in curves:
        mw = curves["PGM"] - curves["ERS"]
        out["MW_snap_V"] = [round(float(x), 4) for x in mw]
        p = log_fit(ts, mw)
        if p:
            a, b, g = p
            out["MW_10y_fit_V"] = a - b*np.log(TEN_Y + g)
            # closing time of the fitted window: alpha - beta*ln(t+gamma) = 0
            out["MW_close_time_fit_s"] = float(np.exp(min(a / b, 700.0)) - g) if b > 0 else None
        if pgm.get("RET") is not None and ers.get("ERSRET") is not None:
            out["MW_3e8_read_V"] = pgm["RET"] - ers["ERSRET"]
    return out


def equilibrium_test(device, T, occ_pgm, occ_ers=None, full=FULL):
    """Python-only check at 0 V: from empty traps the net charge must stay ~0 (no spurious
    charging), and from the PGM / ERS occupancies it must only relax (no sign change beyond
    the empty-start level). Reports Q/Q0 and dVT at 1 s, 1e4 s and the end of the run."""
    out = {}
    starts = [("empty", (0.0, 0.0)), ("PGM", occ_pgm)] + ([("ERS", occ_ers)] if occ_ers else [])
    for name, occ in starts:
        t, q, dvt = python_run(device, T, full, occ)
        k = [int(np.argmin(np.abs(np.log10(np.maximum(t, 1e-12)) - np.log10(x)))) for x in (1.0, 1e4)]
        out[f"eq_{name}_dVt_1s_1e4s_end_V"] = [float(dvt[k[0]]), float(dvt[k[1]]), float(dvt[-1])]
        if name != "empty" and abs(q[0]) > 0:
            out[f"eq_{name}_Q_over_Q0_end"] = float(q[-1] / q[0])
    e = out["eq_empty_dVt_1s_1e4s_end_V"]
    out["eq_empty_pass"] = bool(max(abs(x) for x in e) < 0.01)   # < 10 mV of spurious shift
    return out


def couple(device, T, atlas_dir, out_dir):
    qfile = atlas_dir / f"T{T}K_{device}_netcharge_vs_time.dat" if atlas_dir else None
    efile = atlas_dir / f"T{T}K_{device}_ERS_netcharge_vs_time.dat" if atlas_dir else None
    have_q = bool(qfile and qfile.exists())
    q = read_two_columns(qfile) if have_q else None
    occ0 = occ_from_q(q[0, 1]) if have_q else OCC0
    t, f, dvb, dvf = survival_factor(device, T, occ0=occ0)
    res = dict(device=device, T_K=T, occ0_e=occ0[0], occ0_h=occ0[1], F_10y=f[-1],
               py_dVt_start_V=dvb[0], py_base_dVt_10y_V=dvb[-1], py_full_dVt_10y_V=dvf[-1])
    rows = [dict(time_s=a, F=b, py_base_dVt_V=c, py_full_dVt_V=d) for a, b, c, d in zip(t, f, dvb, dvf)]
    ret = read_states(atlas_dir, T, device, "RET", ("init", "PGM", "RET")) if atlas_dir else {}
    pe = read_states(atlas_dir, T, device, "PE", ("init", "PGM", "ERS", "ERSRET")) if atlas_dir else {}
    if have_q and ret.get("init") is not None and ret.get("PGM") is not None:
        ta, qa = q[:, 0], q[:, 1]
        fa = log_interp(ta, t[1:], f[1:])
        qc = qa * fa
        v0, vp = ret["init"], ret["PGM"]
        vt_atlas = v0 + (vp - v0) * qa / qa[0]
        vt_corr = v0 + (vp - v0) * qc / qa[0]
        res.update(N_trap0_cm3=abs(qa[0]) / Q_E / NIT_VOL_CM3, VT_init_V=v0, VT_PGM_V=vp,
                   VT_RET_atlas_read_V=ret.get("RET"), VT_10y_atlas_V=vt_atlas[-1], VT_10y_coupled_V=vt_corr[-1],
                   VT_init_PE_V=pe.get("init"), VT_PGM_PE_V=pe.get("PGM"), VT_ERS_V=pe.get("ERS"),
                   VT_ERSRET_atlas_read_V=pe.get("ERSRET"),
                   retained_fraction_atlas=qa[-1] / qa[0], retained_fraction_coupled=qc[-1] / qa[0],
                   atlas_status="coupled")
        rows = [dict(time_s=a, Q_atlas=b, F=c, Q_coupled=d, VT_atlas_V=e, VT_coupled_V=g)
                for a, b, c, d, e, g in zip(ta, qa, fa, qc, vt_atlas, vt_corr)]
        v_ers = pe.get("ERS")
        if v_ers is not None:
            if efile and efile.exists():
                qe = read_two_columns(efile)
                te, qe_a = qe[:, 0], qe[:, 1]
                occ_e = occ_from_q(qe_a[0])
                tp, fe, _, _ = survival_factor(device, T, occ0=occ_e)
                qe_c = qe_a * log_interp(te, tp[1:], fe[1:])
                if abs(qe_a[0]) > 1e-3 * abs(qa[0]):       # own scaling: VT_init at Q = 0
                    ve_atlas = v0 + (v_ers - v0) * qe_a / qe_a[0]
                    ve_corr = v0 + (v_ers - v0) * qe_c / qe_a[0]
                else:                                       # nearly neutral: PGM slope dVT/dQ
                    sl = (vp - v0) / qa[0]
                    ve_atlas = v_ers + sl * (qe_a - qe_a[0])
                    ve_corr = v_ers + sl * (qe_c - qe_a[0])
                ers = {"atlas": log_interp(ta, te, ve_atlas), "coupled": log_interp(ta, te, ve_corr)}
                res.update(ERS_mode="VT_ERS(t)", occ0_ers_e=occ_e[0], occ0_ers_h=occ_e[1],
                           VT_ERS_10y_atlas_V=ers["atlas"][-1], VT_ERS_10y_coupled_V=ers["coupled"][-1])
                for r, a_, c_ in zip(rows, ers["atlas"], ers["coupled"]):
                    r.update(VT_ERS_atlas_V=a_, VT_ERS_coupled_V=c_)
            else:
                ers = {"atlas": np.full_like(ta, v_ers), "coupled": np.full_like(ta, v_ers)}
                res["ERS_mode"] = "const (ERS retention not run)"
            for name, curve in (("atlas", vt_atlas), ("coupled", vt_corr)):
                mw = curve - ers[name]
                res[f"MW_10y_{name}_V"] = mw[-1]
                res[f"MW_close_time_{name}_s"] = close_time(ta, mw)
                res[f"logfit_{name}"] = log_fit(ta, curve)
    else:
        res["atlas_status"] = "ATLAS 결과 없음 (Python 계수만)"
    res.update(paper_fit(atlas_dir, T, device))
    occ_e = None
    if efile and efile.exists():
        occ_e = occ_from_q(read_two_columns(efile)[0, 1])
    res.update(equilibrium_test(device, T, occ0, occ_e))
    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / f"T{T}K_{device}_coupled.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    return res


SENS = [("기본 (a=1.5 nm, Ea=1.2 eV, ħω=64 meV, W_opt/W_T=2, 탈출=1, FC 터널링)", {}),
        ("FC 터널링 끔 (탄성 유지)", {"fc_tunnel": False}),
        ("포논 에너지 50 meV", {"pat_phonon_ev": 0.050}),
        ("포논 에너지 80 meV", {"pat_phonon_ev": 0.080}),
        ("W_opt/W_T = 1.8", {"pat_wopt_ratio": 1.8}),
        ("W_opt/W_T = 2.2", {"pat_wopt_ratio": 2.2}),
        ("이온화 전자 탈출 2 %", {"pat_escape": 0.02}),
        ("hopping Ea = 0.9 eV", {"hop_ea": 0.9}),
        ("hopping a = 3.0 nm", {"hop_distance_nm": 3.0})]


def sensitivity(devices, temps, out_dir):
    out = []
    for label, kw in SENS:
        for dev in devices:
            for T in temps:
                full = dict(FULL, **kw)
                t, f, dvb, dvf = survival_factor(dev, T, full)
                out.append(dict(case=label, device=dev, T_K=T, F_10y=f[-1],
                                py_full_dVt_10y_V=dvf[-1], py_base_dVt_10y_V=dvb[-1], dVt_start_V=dvb[0]))
                print(out[-1], flush=True)
    with (out_dir / "sensitivity.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--atlas-dir", type=Path, default=HERE.parent / "results" / "atlas")
    ap.add_argument("--out", type=Path, default=HERE / "results")
    ap.add_argument("--devices", default="SONOS,TANOS,TANS")
    ap.add_argument("--temps", default="300,77")
    ap.add_argument("--sensitivity", action="store_true")
    a = ap.parse_args()
    devs = a.devices.upper().split(",")
    temps = [int(x) for x in a.temps.split(",")]
    a.out.mkdir(parents=True, exist_ok=True)
    if a.sensitivity:
        sensitivity(devs, temps, a.out)
        return
    res = []
    for d in devs:
        for T in temps:
            r = couple(d, T, a.atlas_dir if a.atlas_dir.exists() else None, a.out)
            res.append(r)
            print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()}, flush=True)
    for d in devs:                # loss-rate ratio after the first second (paper: 77 K << 300 K)
        r = {x["T_K"]: x for x in res if x["device"] == d}
        if 77 in r and 300 in r:
            for st in ("PGM", "ERS"):
                a_, b_ = r[77].get(f"VT_{st}_loss_per_decade_V"), r[300].get(f"VT_{st}_loss_per_decade_V")
                if a_ is not None and b_:
                    print(f"{d} {st}: VT loss/decade 1 s-1e4 s  77 K {a_:.4f} V, 300 K {b_:.4f} V, ratio {a_/b_:.3f}")
    keys = sorted({k for r in res for k in r}, key=lambda k: list(res[0]).index(k) if k in res[0] else 99)
    with (a.out / "summary.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys); w.writeheader(); w.writerows(res)


if __name__ == "__main__":
    main()
