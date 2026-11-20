"""Extract read VT from ATLAS Id-Vg outputs and compare PGM/ERS states.

VT method: linear-region (VD = 0.1 V) Id-Vg, tangent at the point of maximum
transconductance gm = dId/dVg, x-axis intercept (same definition as DeckBuild
xintercept(maxslope(curve(v."cgate",i."drain")))).  The VD/2-corrected value
VT - VD/2 is reported in a separate column.  Both corrections cancel in the
window VT,PGM - VT,ERS, which is reported with its sign.

Input per state (first one found wins), in the ATLAS run directory:
  1. <tag>_IdVg.dat   written by the deck line  extract ... curve(...) outfile=
  2. <tag>_IdVg.csv   TonyPlot "Export" of the read log (Vg, Id columns)
  3. <tag>_read.log   only if --log-cols VG,ID is given (column indices of the
                      numeric rows), because the .log column order depends on
                      the ATLAS version and probes.
<tag> = <DEVICE>_<T>K_<state>, e.g. SONOS_77K_programmed.

The DeckBuild values in <tag>_Vt.dat / <tag>_Vt_vd2.dat are read too, when
present, to cross-check this script against DeckBuild's own extraction.

Usage:
  python analyze_reads.py --dir generated
  python analyze_reads.py --dir generated --log-cols 1,3      # parse .log
  python analyze_reads.py --selftest
"""
import argparse
import csv
import re
import sys
import tempfile
from pathlib import Path

import numpy as np

STATES = ("fresh", "programmed", "erased", "program_retained", "erase_retained")
DEVICES = ("SONOS", "TANOS", "TANS")
NUM = re.compile(r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?")


def numeric_rows(path):
    rows = []
    for line in Path(path).read_text(errors="replace").splitlines():
        line = line.strip()
        if not line or line[0] in "#!\"'" or line[0].isalpha():
            continue
        toks = re.split(r"[,\s;]+", line)
        try:
            rows.append([float(t) for t in toks if t])
        except ValueError:
            continue
    # Use the most common row width: DeckBuild curve files start with a
    # "<npoints> <ncols> <nsets>" header line that must not be taken as data.
    widths = [len(r) for r in rows if len(r) >= 2]
    if not widths:
        return np.empty((0, 2))
    width = max(set(widths), key=widths.count)
    return np.array([r for r in rows if len(r) == width])


def vt_maxgm(vg, idd):
    """Max-gm tangent x-intercept. Returns (VT, Vg at gm max, gm max)."""
    order = np.argsort(vg)
    vg, idd = vg[order], np.abs(idd[order])
    keep = np.r_[True, np.diff(vg) > 0]
    vg, idd = vg[keep], idd[keep]
    if len(vg) < 3:
        raise ValueError("fewer than 3 distinct Vg points")
    slope = np.diff(idd) / np.diff(vg)          # forward difference, like maxslope
    k = int(np.argmax(slope))
    vmid, imid = 0.5 * (vg[k] + vg[k + 1]), 0.5 * (idd[k] + idd[k + 1])
    if slope[k] <= 0:
        raise ValueError("no positive gm")
    return vmid - imid / slope[k], vmid, slope[k]


def load_curve(folder, tag, log_cols):
    for suffix in ("_IdVg.dat", "_IdVg.csv"):
        p = folder / f"{tag}{suffix}"
        if p.exists():
            a = numeric_rows(p)
            if len(a):
                return a[:, 0], a[:, 1], p.name
    p = folder / f"{tag}_read.log"
    if p.exists() and log_cols:
        a = numeric_rows(p)
        if len(a):
            return a[:, log_cols[0]], a[:, log_cols[1]], p.name + f" cols{log_cols}"
    return None


def deckbuild_value(folder, name):
    p = folder / name
    if not p.exists():
        return None
    nums = NUM.findall(p.read_text(errors="replace"))
    return float(nums[-1]) if nums else None


def python_dvt(history_csv):
    """Snapshot dVT (initial-relative) per state from <DEVICE>_history.csv."""
    if not history_csv.exists():
        return {}
    out = {}
    for row in csv.DictReader(history_csv.open()):
        if row["stage"] in STATES:
            out[row["stage"]] = float(row["deltaVt_V"])
    return out


def analyse(folder, temperature, vd, log_cols, devices, history_dir):
    folder, history_dir = Path(folder), Path(history_dir or folder)
    records = []
    for dev in devices:
        pred = python_dvt(history_dir / f"{dev}_history.csv")
        for prefix in ("", "noBTBT_"):
            for st in STATES:
                tag = f"{dev}_{prefix}{temperature:g}K_{st}"
                rec = dict(device=dev, variant=prefix.rstrip("_") or "BTBT", state=st,
                           source="", VT_V=None, VT_minus_VD2_V=None, Vg_gmmax_V=None,
                           gm_max_S=None, deckbuild_VT_V=deckbuild_value(folder, f"{tag}_Vt.dat"),
                           python_dVT_V=pred.get(st), status="미실행(파일 없음)")
                curve = load_curve(folder, tag, log_cols)
                if curve:
                    try:
                        vt, vm, gm = vt_maxgm(curve[0], curve[1])
                        rec.update(source=curve[2], VT_V=vt, VT_minus_VD2_V=vt - vd / 2,
                                   Vg_gmmax_V=vm, gm_max_S=gm, status="추출됨")
                    except ValueError as ex:
                        rec.update(source=curve[2], status=f"추출 실패: {ex}")
                elif rec["deckbuild_VT_V"] is not None:
                    rec.update(source=f"{tag}_Vt.dat", VT_V=rec["deckbuild_VT_V"],
                               VT_minus_VD2_V=rec["deckbuild_VT_V"] - vd / 2,
                               status="DeckBuild 값만 있음")
                if prefix and rec["source"] == "":
                    continue          # noBTBT rows only when they were run
                records.append(rec)
    return records


def windows(records):
    out = []
    by = {(r["device"], r["variant"], r["state"]): r for r in records}
    for (dev, var) in sorted({(r["device"], r["variant"]) for r in records}):
        for a, b, name in (("programmed", "erased", "직후"),
                           ("program_retained", "erase_retained", "보존 후")):
            ra, rb = by.get((dev, var, a)), by.get((dev, var, b))
            if not ra or not rb:
                continue
            w = (ra["VT_V"] - rb["VT_V"]) if ra["VT_V"] is not None and rb["VT_V"] is not None else None
            pw = (ra["python_dVT_V"] - rb["python_dVT_V"]) if ra["python_dVT_V"] is not None and rb["python_dVT_V"] is not None else None
            out.append(dict(device=dev, variant=var, pair=name, VT_PGM_V=ra["VT_V"], VT_ERS_V=rb["VT_V"],
                            window_V=w, inverted=None if w is None else w < 0,
                            python_window_V=pw, atlas_minus_python_mV=None if w is None or pw is None else 1e3 * (w - pw)))
    return out


def fmt(v, nd=4):
    return "—" if v is None else (f"{v:+.{nd}f}" if isinstance(v, float) else str(v))


def report(records, wins, vd):
    lines = [f"# 읽기 VT 추출 결과 (VD = {vd} V, 최대 gm 접선의 Vg축 절편)", "",
             f"VT 열은 VD/2 보정 전 값, VT−VD/2 열은 {vd/2:g} V를 뺀 값이다. 창(window)은 보정과 무관하다.", "",
             "| 구조 | 모델 | 상태 | 입력 | VT (V) | VT−VD/2 (V) | Vg@gm,max (V) | DeckBuild VT (V) | Python ΔVT (V) | 상태 |",
             "|---|---|---|---|---:|---:|---:|---:|---:|---|"]
    for r in records:
        lines.append(f"| {r['device']} | {r['variant']} | {r['state']} | {r['source'] or '—'} | {fmt(r['VT_V'])} | "
                     f"{fmt(r['VT_minus_VD2_V'])} | {fmt(r['Vg_gmmax_V'],3)} | {fmt(r['deckbuild_VT_V'])} | "
                     f"{fmt(r['python_dVT_V'])} | {r['status']} |")
    lines += ["", "## VT,PGM − VT,ERS (부호 유지)", "",
              "| 구조 | 모델 | 구분 | VT,PGM (V) | VT,ERS (V) | VT,PGM−VT,ERS (V) | 역전 | Python 예측 (V) | ATLAS−Python (mV) |",
              "|---|---|---|---:|---:|---:|---|---:|---:|"]
    for w in wins:
        inv = "—" if w["inverted"] is None else ("예 (ERS > PGM)" if w["inverted"] else "아니오")
        lines.append(f"| {w['device']} | {w['variant']} | {w['pair']} | {fmt(w['VT_PGM_V'])} | {fmt(w['VT_ERS_V'])} | "
                     f"{fmt(w['window_V'])} | {inv} | {fmt(w['python_window_V'])} | {fmt(w['atlas_minus_python_mV'],2)} |")
    lines += ["", "ATLAS 덱은 Python의 ΔVT를 Si 계면 고정전하 qf로 넣으므로, 정상 실행이면 ATLAS−Python 차이는 "
              "격자·Vg 간격에서 오는 수 mV 이내여야 한다. 크게 다르면 qf 전달, 수렴, 추출 구간을 먼저 확인한다."]
    return "\n".join(lines) + "\n"


def write_outputs(folder, records, wins, vd, out_prefix):
    folder = Path(folder)
    with (folder / f"{out_prefix}_states.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(records[0])); w.writeheader(); w.writerows(records)
    if wins:
        with (folder / f"{out_prefix}_windows.csv").open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(wins[0])); w.writeheader(); w.writerows(wins)
    text = report(records, wins, vd)
    (folder / f"{out_prefix}.md").write_text(text, encoding="utf-8")
    return text


def selftest():
    """Synthetic long-channel curves with known VT: checks the extraction code only."""
    tmp = Path(tempfile.mkdtemp(prefix="vt_selftest_"))
    vd, vt0, beta, theta = 0.1, 0.62, 2e-5, 0.15
    known = {"programmed": 0.465639, "erased": 0.515126, "fresh": 0.0,
             "program_retained": 0.42295, "erase_retained": 0.39083}
    vg = np.arange(-2, 8.0001, 0.01)
    for st, dvt in known.items():
        vt = vt0 + dvt
        n = 1.1 * 0.00663                          # 77 K subthreshold, ~15 mV/dec
        vov = n * np.logaddexp(0, (vg - vt) / n)    # smooth turn-on
        idd = beta * (vov - vd / 2).clip(0) * vd / (1 + theta * vov) + 1e-18
        np.savetxt(tmp / f"SONOS_77K_{st}_IdVg.dat", np.c_[vg, idd], header="Vg Id")
    recs = analyse(tmp, 77, vd, None, ("SONOS",), tmp)
    wins = windows(recs)
    w = wins[0]["window_V"]; expect = known["programmed"] - known["erased"]
    ok = abs(w - expect) < 2e-3
    print(report(recs, wins, vd))
    print(f"SELFTEST {'PASS' if ok else 'FAIL'}: window {w:+.5f} V vs imposed {expect:+.5f} V")
    return ok


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", default="generated")
    ap.add_argument("--history-dir", default=None, help="folder with *_history.csv (default --dir)")
    ap.add_argument("--temperature", type=float, default=77)
    ap.add_argument("--vd", type=float, default=0.1)
    ap.add_argument("--devices", default=",".join(DEVICES))
    ap.add_argument("--log-cols", default=None, help="Vg,Id column indices in numeric rows of _read.log")
    ap.add_argument("--out", default="VT_report")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(0 if selftest() else 1)
    cols = tuple(int(c) for c in a.log_cols.split(",")) if a.log_cols else None
    recs = analyse(a.dir, a.temperature, a.vd, cols, a.devices.split(","), a.history_dir)
    print(write_outputs(a.dir, recs, windows(recs), a.vd, a.out))
