# VT (first gm peak, constant current) and probe netcharge from a tscan run folder: python3 vt_summary.py <folder>
import sys, glob, numpy as np
def load(f):
    rows=[[float(x) for x in l.split()[1:]] for l in open(f) if l.startswith('d ')]
    return np.array(rows)
def vt_gm(v,i):
    g=np.gradient(i,v); thr=0.3*g.max()
    for k in range(1,len(v)-1):
        if g[k]>=thr and g[k]>=g[k-1] and g[k]>=g[k+1]: return v[k]-i[k]/g[k]
def vt_cc(v,i,ref):
    i=np.abs(i); k=np.where(i>=ref)[0]
    if not len(k) or k[0]==0: return None
    k=k[0]; return float(np.interp(np.log10(ref),np.log10(i[k-1:k+1]),v[k-1:k+1]))
d=sys.argv[1]
for st in ('initial','PGM','ERS'):
    f=glob.glob(f'{d}/SONOS_{st}*.log')[0]; a=load(f)
    v,i,q=a[:,0],a[:,8],a[:,12]
    s=np.argsort(v); v,i,q=v[s],i[s],q[s]
    cc=[vt_cc(v,i,r) for r in (1e-9,1e-8,1e-7)]
    print(f'{st:8s} VT_gm {vt_gm(v,i):.4f} V | cc 1e-9/1e-8/1e-7: '+' / '.join(f'{c:.4f}' if c is not None else 'NA' for c in cc)+f' | netcharge {q[0]:.4e} | Vg {v[0]:.1f}..{v[-1]:.1f} n={len(v)}')
for st in ('PGM','ERS'):
    f=glob.glob(f'{d}/TRNS_{st}*.log')[0]; a=load(f)
    t,vg,q=a[:,0],a[:,1],a[:,13]
    print(f'TRNS_{st}: steps {len(t)}, t_end {t[-1]:.3e} s, Vg_end {vg[-1]:.2f}, netcharge start {q[0]:.4e} end {q[-1]:.4e}')
    for tt in (1e-9,1e-8,1e-7,1e-6,1e-5,1e-4,5e-4):
        k=np.searchsorted(t,tt)
        if k<len(t): print(f'   t={t[k]:.2e}  Q={q[k]:.4e}')
