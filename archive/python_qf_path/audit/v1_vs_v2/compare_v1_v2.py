"""SONOS: original model (v1) vs activated-hopping model (v2), side by side.

Writes audit/v1_vs_v2/compare_v1_v2.csv. Python dVT only (no ATLAS).
Run from the package root:  python audit/v1_vs_v2/compare_v1_v2.py
"""
import csv, sys
from pathlib import Path
root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root))
import flash_transport as v1
import flash_transport_v2 as v2

cases = [("v1", "baseline (current decks)", v1, {}),
         ("v1", "hopping off", v1, {"hopping": False}),
         ("v2", "a=N^-1/3 (4.64 nm), Ea=1.2 eV", v2, {}),
         ("v2", "a=3.5 nm, Ea=1.2 eV", v2, {"hop_distance_nm": 3.5}),
         ("v2", "a=1.5 nm, Ea=1.2 eV", v2, {"hop_distance_nm": 1.5}),
         ("v2", "a=1.5 nm, Ea=0.6 eV", v2, {"hop_distance_nm": 1.5, "hop_ea": 0.6}),
         ("v2", "a=1.5 nm, Ea=0.3 eV", v2, {"hop_distance_nm": 1.5, "hop_ea": 0.3})]
rows = []
for T in (77, 300):
    for ver, label, mod, kw in cases:
        for n in (4, 8, 16):
            try:
                _, s = mod.simulate("SONOS", mod.Options(temperature=T, planes=n, **kw))
                d = {k: v[0] for k, v in s.items()}
                r = dict(T_K=T, version=ver, case=label, planes=n,
                         P_dVt_V=d["programmed"], E_dVt_V=d["erased"],
                         P_minus_E_V=d["programmed"] - d["erased"],
                         Pret_dVt_V=d["program_retained"], Eret_dVt_V=d["erase_retained"],
                         ret_P_minus_E_V=d["program_retained"] - d["erase_retained"], error="")
            except Exception as ex:
                r = dict(T_K=T, version=ver, case=label, planes=n, error=str(ex))
            rows.append(r)
            print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()}, flush=True)
keys = ["T_K", "version", "case", "planes", "P_dVt_V", "E_dVt_V", "P_minus_E_V",
        "Pret_dVt_V", "Eret_dVt_V", "ret_P_minus_E_V", "error"]
with open(Path(__file__).with_name("compare_v1_v2.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(rows)
