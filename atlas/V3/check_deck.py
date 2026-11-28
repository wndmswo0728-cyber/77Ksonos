"""Static check of an ATLAS P/E deck (no ATLAS run).

Follows the deck statement by statement and reports, for every SOLVE, the model state (pf.nitride on/off),
the METHOD values in force (assuming METHOD values persist until changed), the gate/drain bias and the
simulated time. Rules taken from earlier runs of these decks:
  - LOAD restores the saved biases and restarts the time at 0 (seen in every run);
  - a RELATIVE TSTOP in the first transient after a LOAD used the previous transient's end time in the same
    run (77fix read deck), so that case is flagged;
  - RAMPTIME starts at the current time (manual SOLVE RAMPTIME).
Problems reported: undefined variables, MODELS after CONTACT/METHOD, LOAD of a file not saved before,
static solves with pf.nitride on, Program/Erase transients with pf.nitride off, an absolute TSTOP not later
than the current time, a ramp longer than its time interval, pulses or reads that do not start at 0 V,
saves of pulse states not at 0 V.

Usage: python3 atlas/V3/check_deck.py <deck.in> [-v]
"""
import re
import sys


def num(x, env):
    x = x.strip()
    if x.startswith(('$', '@')):
        return env[x[1:]]
    return float(x)


def check(path, verbose=False):
    lines = open(path).read().split('\n')
    env, saved, bad, rows = {}, {}, [], []
    pf = False
    meth = {'dt.max': None, 'dt.min': None, 'cx.tol': None}
    vg = vd = 0.0
    t = 0.0
    transient_since_load = True      # the run start counts as "no LOAD before"
    any_transient = False
    seen = []
    for i, raw in enumerate(lines, 1):
        l = raw.split('#')[0].strip() if not raw.lstrip().startswith('#') else ''
        if not l:
            continue
        w = l.split()
        key = w[0].lower()
        # variables
        for v in re.findall(r'[$@]([A-Za-z_][A-Za-z0-9_]*)', l):
            if key == 'set' and l.split('=')[0].strip().endswith(v):
                continue
            if v not in env:
                bad.append((i, f'variable {v} used before set'))
        if key == 'assign':
            m = re.search(r'name=(\w+)\s+n\.value=(\S+)', l)
            if m:
                env[m[1]] = float(m[2])
            continue
        if key == 'set':
            name, expr = l[4:].split('=', 1)
            name = name.strip()
            e = expr.strip()
            for v in sorted(env, key=len, reverse=True):
                e = e.replace('$' + v, repr(env[v])).replace('@' + v, repr(env[v]))
            try:
                env[name] = eval(e, {}, {})
            except Exception:
                env[name] = e
            continue
        if key in ('models', 'contact', 'method', 'material', 'nitridecharge'):
            seen.append(key)
        if key == 'models':
            if 'contact' in seen[:-1] and 'models' not in seen[:-1]:
                bad.append((i, 'first MODELS after CONTACT'))
            if '^pf.nitride' in l:
                pf = False
            elif 'pf.nitride' in l:
                pf = True
            if 'temperature=' not in l:
                bad.append((i, 'MODELS without temperature='))
            continue
        if key == 'method':
            for k in meth:
                m = re.search(rf'{re.escape(k)}=(\S+)', l)
                if m:
                    meth[k] = float(m[1])
            continue
        if key == 'save':
            f = re.search(r'outf=(\S+)', l)[1]
            saved[f] = (vg, vd)
            rows.append((i, 'save', f.split('_nt_')[0], vg, vd, t, pf, dict(meth), ''))
            continue
        if key == 'load':
            f = re.search(r'infile=(\S+)', l)[1]
            if f not in saved:
                bad.append((i, f'LOAD of {f} not saved earlier in this deck'))
            else:
                vg, vd = saved[f]
            t = 0.0
            transient_since_load = False
            rows.append((i, 'load', f.split('_nt_')[0], vg, vd, t, pf, dict(meth), ''))
            continue
        if key != 'solve':
            continue
        kv = dict(re.findall(r'(\w+(?:\.\w+)?)=(\S+)', l))
        is_tr = any(k in kv for k in ('tstop', 'tfinal', 'ramptime'))
        if not is_tr:
            if pf:
                bad.append((i, 'static solve with pf.nitride on'))
            if 'init' in w:
                if len(w) == 2:
                    vg = vd = 0.0
                kind = ' '.join(w[1:])
            elif 'name' in kv:
                tgt = num(kv['vfinal'], env)
                if kv['name'] == 'cgate':
                    start = num(kv.get('vcgate', str(vg)), env)
                    if kv.get('vcgate') is not None and abs(start - vg) > 1e-9:
                        bad.append((i, f'gate sweep starts at {start} V but gate is at {vg} V'))
                    if start == 0 and tgt > 0 and kv.get('log'):
                        pass
                    vg = tgt
                else:
                    vd = tgt
                kind = f"sweep {kv['name']} -> {tgt:g}"
            else:
                if 'vdrain' in kv:
                    vd = num(kv['vdrain'], env)
                if 'vcgate' in kv:
                    vg = num(kv['vcgate'], env)
                kind = ' '.join(w[1:])
            rows.append((i, 'static', kind, vg, vd, t, pf, dict(meth), ''))
            continue
        # transient
        rel = 'relative' in w
        tend_key = 'tstop' if 'tstop' in kv else 'tfinal'
        tv = num(kv[tend_key], env)
        if rel:
            if not transient_since_load and any_transient:
                bad.append((i, 'RELATIVE in the first transient after a LOAD (previous end time would be used)'))
            end = t + tv
        else:
            end = tv
            if end <= t:
                bad.append((i, f'absolute end {end:g} s not after current time {t:g} s'))
        rt = num(kv['ramptime'], env) if 'ramptime' in kv else 0.0
        if rt > end - t + 1e-18:
            bad.append((i, f'ramp {rt:g} s longer than the interval {end - t:g} s'))
        v0g, v0d = vg, vd
        if 'vcgate' in kv:
            vg = num(kv['vcgate'], env)
        if 'vdrain' in kv:
            vd = num(kv['vdrain'], env)
        tag = ('proj ' if 'proj' in w else '') + ('rel' if rel else 'abs')
        rows.append((i, 'trans', f'Vg {v0g:g}->{vg:g} VD {v0d:g}->{vd:g} ramp {rt:g}', vg, vd, end, pf, dict(meth), tag))
        t = end
        transient_since_load = True
        any_transient = True
    # pulse / read checks on the row list
    for k, r in enumerate(rows):
        i, typ, kind, g, d, tt, p, m, tag = r
        if typ == 'trans' and ('->16' in kind or '->-12' in kind) and 'Vg 0->' in kind and not p:
            bad.append((i, 'pulse rise with pf.nitride off'))
        if typ == 'save' and kind in ('SONOS_PGM', 'SONOS_ERS') and (abs(g) > 1e-12 or abs(d) > 1e-12):
            bad.append((i, f'{kind} saved at Vg {g} VD {d} (not 0 V)'))
    if verbose:
        print(f'{"line":>4} {"type":6} {"what":44} {"Vg":>6} {"VD":>6} {"t_end(s)":>10} {"pf":>3} {"dt.max":>7} {"dt.min":>7} {"cx.tol":>7} time')
        for i, typ, kind, g, d, tt, p, m, tag in rows:
            f = lambda x: '-' if x is None else f'{x:.0e}'
            print(f'{i:4d} {typ:6} {kind[:44]:44} {g:6.2f} {d:6.3f} {tt:10.3e} {"on" if p else "off":>3} '
                  f'{f(m["dt.max"]):>7} {f(m["dt.min"]):>7} {f(m["cx.tol"]):>7} {tag}')
    return rows, bad


if __name__ == '__main__':
    verbose = '-v' in sys.argv
    rc = 0
    for p in [a for a in sys.argv[1:] if a != '-v']:
        rows, bad = check(p, verbose)
        print(f'== {p}: {len(rows)} steps, {len(bad)} problem(s)')
        for i, msg in bad:
            print(f'   line {i}: {msg}')
        rc |= bool(bad)
    sys.exit(rc)
