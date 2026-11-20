"""Couple the ATLAS (DYNASONOS) retention results with the mechanisms ATLAS lacks.

ATLAS computes retention with PF emission, ELASTIC trap<->band tunneling, capture and
emission. It has no nitride hopping, no phonon-assisted (multiphonon) trap ionization
and no Franck-Condon (phonon-assisted) weighting of trap<->electrode tunneling.
For each device and temperature this script

 1. runs the Python model (cryo_model.py) twice from the same initial charge as the
    ATLAS retention deck (nit.n = 1.1e19 cm^-3, uniform; Nnit = 5e19):
        base : channels ATLAS also has (elastic WKB exchange), Python PF/thermal OFF
        full : activated hopping + phonon-assisted ionization (above PF)
               + Franck-Condon weighted trap<->electrode tunneling (replaces elastic)
 2. forms F(t) = Q_full(t) / Q_base(t);
 3. if the ATLAS outputs exist, multiplies the ATLAS trapped charge Q_ATLAS(t)
    (T<T>K_<DEV>_netcharge_vs_time.dat) by F(t) and converts it to VT(t) with
        VT(t) = VT_init + (VT_PGM - VT_init) * Q(t) / Q(0)
    (VT_init, VT_PGM, VT_RET from T<T>K_<DEV>_RET_Vt.dat), and the memory window
        MW(t) = VT(t) - VT_ERS   (VT_ERS from the P/E deck, T<T>K_<DEV>_PE_Vt.dat)
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
OCC0 = (1.1e19 / 5e19, 0.0)       # nit.n 1e18 + 1e19 (cumulative) over Nnit 5e19
BASE = dict(thermal_emission=False, hopping=False, pat=False)
FULL = dict(thermal_emission=False, hopping=True, pat=True, fc_tunnel=True,
            hop_distance_nm=1.5, hop_ea=1.2)


def python_run(device, T, extra):
    hist, snap = cm.simulate(device, cm.Options(temperature=T, retention_s=RETENTION_S, **extra),
                             retention_from=OCC0)
    rows = [r for r in hist if r[0] == "retention"]
    t = np.array([r[1] for r in rows])
    q = np.array([r[3] for r in rows])        # net sheet charge, C/m^2
    dvt = np.array([r[4] for r in rows])
    return t, q, dvt


def survival_factor(device, T, full=FULL):
    t, qb, dvb = python_run(device, T, BASE)
    t2, qf, dvf = python_run(device, T, full)
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


def couple(device, T, atlas_dir, out_dir):
    t, f, dvb, dvf = survival_factor(device, T)
    res = dict(device=device, T_K=T, F_10y=f[-1],
               py_dVt_start_V=dvb[0], py_base_dVt_10y_V=dvb[-1], py_full_dVt_10y_V=dvf[-1])
    rows = [dict(time_s=a, F=b, py_base_dVt_V=c, py_full_dVt_V=d) for a, b, c, d in zip(t, f, dvb, dvf)]
    qfile = atlas_dir / f"T{T}K_{device}_netcharge_vs_time.dat" if atlas_dir else None
    vfile = atlas_dir / f"T{T}K_{device}_RET_Vt.dat" if atlas_dir else None
    pfile = atlas_dir / f"T{T}K_{device}_PE_Vt.dat" if atlas_dir else None
    if qfile and qfile.exists() and vfile.exists():
        q = read_two_columns(qfile)
        vt = read_vt(vfile)
        ta, qa = q[:, 0], q[:, 1]
        fa = log_interp(ta, t[1:], f[1:])
        qc = qa * fa
        v0, vp = vt["Vt_init"], vt["Vt_PGM"]
        vt_atlas = v0 + (vp - v0) * qa / qa[0]
        vt_corr = v0 + (vp - v0) * qc / qa[0]
        v_ers = read_vt(pfile).get("Vt_ERS") if pfile.exists() else None
        res.update(VT_init_V=v0, VT_PGM_V=vp, VT_RET_atlas_read_V=vt.get("Vt_RET"), VT_ERS_V=v_ers,
                   VT_10y_atlas_V=vt_atlas[-1], VT_10y_coupled_V=vt_corr[-1],
                   retained_fraction_atlas=qa[-1] / qa[0], retained_fraction_coupled=qc[-1] / qa[0],
                   atlas_status="coupled")
        if v_ers is not None:
            for name, curve in (("atlas", vt_atlas), ("coupled", vt_corr)):
                mw = curve - v_ers
                res[f"MW_10y_{name}_V"] = mw[-1]
                res[f"MW_close_time_{name}_s"] = close_time(ta, mw)
                res[f"logfit_{name}"] = log_fit(ta, curve)
        rows = [dict(time_s=a, Q_atlas=b, F=c, Q_coupled=d, VT_atlas_V=e, VT_coupled_V=g)
                for a, b, c, d, e, g in zip(ta, qa, fa, qc, vt_atlas, vt_corr)]
    else:
        res["atlas_status"] = "ATLAS 결과 없음 (Python 계수만)"
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
    keys = sorted({k for r in res for k in r}, key=lambda k: list(res[0]).index(k) if k in res[0] else 99)
    with (a.out / "summary.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys); w.writeheader(); w.writerows(res)


if __name__ == "__main__":
    main()
