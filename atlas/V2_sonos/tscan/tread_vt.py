"""VT, SS and netcharge from ATLAS Id-Vg logs (static reads or transient reads).

Usage: python3 tread_vt.py <log> [<log> ...]

- Static log: 13 columns per row (Vg first). Transient log: 14 columns (time first).
- Only rows at the full drain bias (VD within 1 % of its maximum) are used.
- Id = (I_drain - I_source)/2: removes the gate displacement current of a transient read
  (it splits equally between source and drain) and the equal zero-bias S/D floor.
- VT_gm: first gm peak >= 30 % of max gm, linear extrapolation. VT_cc at 1e-9/1e-8/1e-7 A.
- SS: minimum swing between 1e-13 and 1e-8 A. 77 K physical limit 2.303 kT/q = 15.3 mV/dec;
  a smaller value means a jump between solution branches, not a device result.
- netcharge: first and last row of the gate sweep (a change shows read disturb).
"""
import sys
import numpy as np


def load(path):
    rows = [[float(x) for x in line.split()[1:]] for line in open(path) if line.startswith('d ')]
    return np.array(rows)


def analyse(path):
    a = load(path)
    off = 1 if a.shape[1] == 14 else 0          # transient logs start with time
    vg, i_s, vd, i_d, q = a[:, off], a[:, off + 5], a[:, off + 6], a[:, off + 8], a[:, off + 12]
    keep = vd >= 0.99 * vd.max()
    vg, i_s, i_d, q = vg[keep], i_s[keep], i_d[keep], q[keep]
    order = np.argsort(vg, kind='stable')
    vg, i_s, i_d, q = vg[order], i_s[order], i_d[order], q[order]
    vg, idx = np.unique(vg, return_index=True)
    i_s, i_d, q = i_s[idx], i_d[idx], q[idx]
    cur = np.abs((i_d - i_s) / 2)
    common = np.max(np.abs((i_d + i_s) / 2))
    g = np.gradient(cur, vg)
    vt_gm = float('nan')
    for k in range(1, len(vg) - 1):
        if g[k] >= 0.3 * g.max() and g[k] >= g[k - 1] and g[k] >= g[k + 1]:
            vt_gm = vg[k] - cur[k] / g[k]
            break

    def vt_cc(ref):
        k = np.where(cur >= ref)[0]
        if not len(k) or k[0] == 0:
            return float('nan')
        k = k[0]
        return float(np.interp(np.log10(ref), np.log10(cur[k - 1:k + 1]), vg[k - 1:k + 1]))

    lc = np.log10(np.maximum(cur, 1e-300))
    sw = [(vg[k + 1] - vg[k]) / (lc[k + 1] - lc[k]) * 1e3
          for k in range(len(vg) - 1) if 1e-13 < cur[k] < 1e-8 and lc[k + 1] > lc[k]]
    print(f'{path}\n  rows {len(vg)}  Vg {vg[0]:.3f}..{vg[-1]:.3f} V  VD {vd.max():.4f} V'
          f'\n  VT_gm {vt_gm:.4f} V   VT_cc 1e-9/1e-8/1e-7 A: {vt_cc(1e-9):.4f} / {vt_cc(1e-8):.4f} / {vt_cc(1e-7):.4f} V'
          f'\n  SS_min {min(sw) if sw else float("nan"):.1f} mV/dec   Id(Vg_end) {cur[-1]:.3e} A   max common-mode (Id+Is)/2 {common:.2e} A'
          f'\n  netcharge first {q[0]:.5e}  last {q[-1]:.5e}  change {100 * (q[-1] - q[0]) / q[0] if q[0] else 0:.3f} %')


if __name__ == '__main__':
    for p in sys.argv[1:]:
        analyse(p)
