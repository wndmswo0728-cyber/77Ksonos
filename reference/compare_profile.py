"""Compare a channel-center TonyPlot cutline to a 1-D programmed-state snapshot."""
import argparse
import csv
import numpy as np
from scipy.constants import e
from scipy.integrate import trapezoid

def compare(cutline, history, state):
    a = np.genfromtxt(cutline, names=True, delimiter=",",encoding="utf-8-sig")
    y = a["y_um"]
    order = np.argsort(y)
    y = y[order]
    if len(y)<2 or np.any(np.diff(y)<=0):
        raise ValueError("Export unique coordinates on the nitride side only.")
    if not np.allclose([y[0],y[-1]],[-.010,-.003],atol=1e-6,rtol=0):
        raise ValueError("Expected full SONOS nitride cutline, -0.010 through -0.003 um")
    with open(history) as f:
        row=next(r for r in csv.DictReader(f) if r["stage"]==state)
    q=0.
    for label,field,sign in (("electron","electron_cm3",-1),("hole","hole_cm3",1)):
        c=a[field][order]
        if not np.isfinite(c).all() or min(c)<0:
            raise ValueError("Use linear concentrations in cm^-3.")
        for i in range(4):
            hi=-.003-i*.00175
            lo=hi-.00175
            nodes=np.r_[lo,y[(y>lo)&(y<hi)],hi]
            avg=trapezoid(np.interp(nodes,y,c),nodes)/.00175
            print(f"{label} plane {i+1}: ATLAS={avg:.5e} model={float(row[f'{label}_plane{i+1}'])*1e19:.5e} cm^-3")
        q+=sign*e*trapezoid(c,y) # cm^-3 to m^-3 and um to m factors cancel
    print(f"Q at center cutline: ATLAS={q:.6g}, model={float(row['Q_C_m2']):.6g} C/m^2")

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("cutline")
    p.add_argument("--history",default="generated/SONOS_history.csv")
    p.add_argument("--state",default="programmed")
    args=p.parse_args()
    compare(args.cutline,args.history,args.state)
