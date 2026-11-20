"""Run inside the extracted package: python check_results.py"""
from pathlib import Path
import csv
import math

root = Path(__file__).resolve().parent
modes = ['baseline', 'no-hopping', 'no-erase-hopping', 'no-pf', 'no-fn']
states = ['fresh', 'programmed', 'erased', 'program_retained', 'erase_retained']
metrics = []
for device in ('SONOS', 'TANOS', 'TANS'):
    programmed = None
    for mode in modes:
        directory = root / ('generated' if mode == 'baseline' else f'audit/{mode}')
        with (directory/f'{device}_history.csv').open() as stream:
            rows = list(csv.DictReader(stream))
        snapshot = {r['stage']: r for r in rows if r['stage'] in states}
        assert set(snapshot) == set(states)
        assert all(math.isfinite(float(value)) for r in rows for key,value in r.items() if key != 'stage')
        occupancy = [key for key in rows[0] if '_plane' in key]
        assert all(-1e-6 <= float(r[k]) <= 1+1e-6 for k in occupancy for r in rows)
        residual = max(abs(float(r['balance_error_A_m2'])) for r in rows)
        peak = max(abs(float(r['dQdt_A_m2'])) for r in rows)
        assert residual <= 1e-10*(1+peak)
        for phase, voltage, duration in [('program',16,1e-4),('erase',-12,5e-4)]:
            hold = [r for r in rows if r['stage']==phase+'_hold'][-1]
            assert float(hold['stack_voltage_V'])==voltage
            assert math.isclose(float(hold['stage_time_s'])+1e-9,duration)
            assert float([r for r in rows if r['stage']==phase+'_fall'][-1]['stack_voltage_V'])==0
        for phase in ('program_retention','erase_retention'):
            assert float([r for r in rows if r['stage']==phase][-1]['stage_time_s'])==1
        for state,r in snapshot.items():
            deck=(directory/f'{device}_77K_{state}.in').read_text()
            assert 'models srh temp=77 print' in deck and 'analytic bbt.kl' in deck
            assert ('region num=5 ' in deck) == (device != 'TANS')
            assert ('material=Al2O3' in deck) == (device != 'SONOS')
            assert deck.index('save outf=') < deck.index('solve vdrain')
            qf=float(deck.split('interface qf=')[1].split()[0])
            assert math.isclose(qf,float(r['equiv_Qf_cm-2']),rel_tol=1e-13)
            assert f'save outf={device}_77K_{state}_zero.str' in deck
            assert f'log outf={device}_77K_{state}_read.log' in deck
        for kind, n in [('RUN',5),('BIAS',2)]:
            on=(directory/f'{kind}_{device}.in').read_text()
            off=(directory/f'{kind}_{device}_noBTBT.in').read_text()
            assert on.count('go atlas')==n and on.count('\nquit\n')==1 and on.count('bbt.kl')==n
            assert off==on.replace(' bbt.kl print',' print').replace(device+'_',device+'_noBTBT_')
        pg = snapshot['programmed']
        if mode=='baseline':
            programmed=pg
        if mode=='no-erase-hopping':
            assert all(pg[k]==programmed[k] for k in occupancy+['deltaVt_V'])
        p,e = [float(snapshot[key]['deltaVt_V']) for key in ('programmed','erased')]
        metrics.append([device, mode, p, e, p-e, residual, peak])
with (root/'audit/comparison.csv').open('w', newline='') as stream:
    writer=csv.writer(stream)
    writer.writerow(['device','mode','program_shift_V','erase_shift_V','program_minus_erase_V','max_charge_balance_error_A_m2','peak_abs_dQdt_A_m2'])
    writer.writerows(metrics)
print('PASS: 3 devices x 5 modes, charges, 77 K, geometry, 1 s retention, pulse endpoints, same programmed state, matching ATLAS input and output declarations.')
print('Simulation engine tested: Python/SciPy. Native ATLAS runs require DeckBuild.')
