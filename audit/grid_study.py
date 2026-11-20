"""Nitride-plane (grid) convergence check of the 1-D model. Writes audit/grid_study.csv."""
import csv, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from flash_transport import Options, simulate
rows = []
for dev in ("SONOS", "TANOS", "TANS"):
    for n in (2, 4, 8, 16):
        for mode, kw in (("baseline", {}), ("no-erase-hopping", {"no_erase_hopping": True}), ("no-hopping", {"hopping": False})):
            _, s = simulate(dev, Options(planes=n, **kw))
            r = dict(device=dev, planes=n, mode=mode, **{k + "_dVt_V": v[0] for k, v in s.items() if k != "fresh"})
            r["program_minus_erase_V"] = s["programmed"][0] - s["erased"][0]
            r["retained_program_minus_erase_V"] = s["program_retained"][0] - s["erase_retained"][0]
            rows.append(r); print(r, flush=True)
with open(Path(__file__).with_name("grid_study.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
