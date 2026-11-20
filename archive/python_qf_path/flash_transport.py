"""1-D charge-trap sensitivity model. SI internally, energies in eV."""
from dataclasses import dataclass, replace
from pathlib import Path
import csv
import numpy as np
from scipy.constants import e, epsilon_0, electron_mass, hbar, Boltzmann
from scipy.integrate import solve_ivp, cumulative_trapezoid
from scipy.special import expit
from scipy.optimize import brentq

@dataclass(frozen=True)
class Options:
    temperature: float = 77
    retention_s: float = 1.0
    hopping: bool = True
    fn: bool = True
    pf: bool = True
    density: float = 1e25       # m^-3 per trap family
    localization_nm: float = 0.22
    hop_hz: float = 1e12
    emission_hz: float = 1e13
    escape_fraction: float = 0.02  # emitted band carriers collected before recapture
    capture_fraction: float = 0.05 # incident FN carriers captured, empty traps
    optical_k: float = 4.0
    elastic_hz: float = 1e12  # attempt rate for trap-to-reservoir escape
    sio2_me: float = 0.3  # baseline deck; ratios to vacuum electron mass
    sio2_mh: float = 1.0
    depth_e: float = 1.2
    depth_h: float = 1.2
    no_erase_hopping: bool = False
    planes: int = 4  # nitride discretisation; 4 reproduces the audited package


PATHS = ("Si_band_e","Si_band_h","gate_band_e","gate_band_h",
         "Si_trap_e","Si_trap_h","gate_trap_e","gate_trap_h","PF_thermal")

def sonos(options=Options()):
    return simulate("SONOS", options)


def tanos(options=Options()):
    return simulate("TANOS", options)


def tans(options=Options()):
    return simulate("TANS", options)


def simulate(device, opt):
    if not 77 <= opt.temperature <= 300 or opt.retention_s <= 0 or opt.planes < 2:
        raise ValueError("Expected 77–300 K and positive retention time.")
    # Effective trap-site planes; each plane represents an ensemble, not a TCAD mesh.
    n = opt.planes
    dx = 7e-9 / n
    x = (np.arange(n) + 0.5) * dx
    cap = opt.density * dx
    kt = Boltzmann * opt.temperature / e
    en = np.array([opt.depth_e, opt.depth_h])[:, None]
    signs = np.array([-1, 1])[:, None]
    tunnel = 0 if device == "TANS" else 3e-9
    block_k = 3.9 if device == "SONOS" else 9.3
    eps_n = epsilon_0 * 7.5
    # Inverse capacitances between electrodes and charge sheets.
    r = np.r_[tunnel/(3.9*epsilon_0) + dx/(2*eps_n),
              np.full(n-1, dx/eps_n), dx/(2*eps_n) + 8e-9/(block_k*epsilon_0)]
    to_gate = r.sum() - np.cumsum(r)[:-1]
    # Equilibrium MOS charge sheet. Fermi-Dirac carrier densities from a tabulated
    # parabolic-band integral, and local ionization of a 45 meV boron acceptor.
    eg = 1.17 - 4.73e-4*opt.temperature**2/(opt.temperature+636)
    nc = 2.8e25*(opt.temperature/300)**1.5
    nv = 1.04e25*(opt.temperature/300)**1.5
    eta = np.linspace(-40,260,3001)
    energy_grid = np.linspace(0,300,2001)
    from scipy.integrate import trapezoid as fd
    values = np.array([2/np.sqrt(np.pi)*fd(np.sqrt(energy_grid)*expit(z-energy_grid),energy_grid) for z in eta])
    def fhalf(z):
        return np.where(z<-40,np.exp(np.minimum(z,-40)),np.interp(z,eta,values))
    def mobile(ef):
        return nc*fhalf((ef-eg)/kt), nv*fhalf(-ef/kt)
    def rho(ef):
        ne,ph = mobile(ef)
        return e*(ph-ne-1e23*expit((ef-.045)/kt-np.log(4)))
    ef0 = brentq(rho,-.3,.6)
    # Gate workfunction minus bulk semiconductor workfunction.
    wf = 4.05 if device=="SONOS" else 4.60
    vfb = wf-(4.05+eg-ef0)
    psi_grid = np.linspace(-.55,eg+.55,16001)
    psi_grid = np.unique(np.r_[psi_grid,0.])
    rho_grid = rho(ef0+psi_grid)
    # Integrate outward from flat band independently to avoid subtractive cancellation.
    zero = np.searchsorted(psi_grid,0.)
    accum = np.r_[cumulative_trapezoid(rho_grid[zero::-1],psi_grid[zero::-1],initial=0)[::-1][:-1],
                  cumulative_trapezoid(rho_grid[zero:],psi_grid[zero:],initial=0)]
    qs_grid = -np.sign(psi_grid)*np.sqrt(np.maximum(-2*epsilon_0*11.7*accum,0))
    voltage_grid = psi_grid-qs_grid*r.sum()
    def fields(y, vg):
        sheet = e * cap * (y[1] - y[0])
        added = np.r_[0, np.cumsum(sheet)]
        target = vg-vfb+added@r
        if not voltage_grid[0] <= target <= voltage_grid[-1]:
            raise ValueError("Outside MOS electrostatics table.")
        surface = np.interp(target,voltage_grid,psi_grid)
        disp = added + (surface-target)/r.sum()
        potential = surface-np.cumsum(disp*r)[:-1]
        return disp, potential, sheet, surface

    def fn_supply(field, barrier, mass, thickness):
        # SI Fowler-Nordheim current, finite-film WKB exponent; FN supply prefactor.
        if field <= 0:
            return 0.
        action = 4*np.sqrt(2*mass*electron_mass*e)*barrier**1.5/(3*hbar*field)
        fraction = min(1.,field*thickness/barrier)
        action *= (1. if fraction == 1. else -np.expm1(1.5*np.log1p(-fraction)))
        return e**2*field**2/(16*np.pi**2*hbar*barrier)*np.exp(-action)

    # Approximate electron/hole injecting barriers (eV) and mass ratios.
    left_phi = (2.0, 5.1-eg-2.) if not tunnel else (3.10, 9.-eg-3.10)
    right_phi = (3.10, 5.90) if device == "SONOS" else (3.10, 4.90)
    def mean_sqrt_barrier(a,b):
        # Integral of sqrt(max(U,0)) for linear U; stable at equal endpoints.
        sa,sb = np.sqrt(np.maximum(a,0)),np.sqrt(np.maximum(b,0))
        above = (2/3)*(sa*sa+sa*sb+sb*sb)/np.maximum(sa+sb,1e-100)
        fraction = np.where(np.minimum(a,b)>=0,1.,np.maximum(a,b)/np.maximum(np.abs(b-a),1e-100))
        return above*np.clip(fraction,0,1)

    def rates(y, vg, diagnostics=False):
        disp, phi, _, surface = fields(y, vg)
        local_f = 0.5*(disp[:-1]+disp[1:])/eps_n
        gate = vg-vfb
        currents = {}
        vacancies = 1-y
        energy = signs*phi-en
        du = np.diff(energy, axis=1)
        base = opt.hop_hz*np.exp(-2*dx/(opt.localization_nm*1e-9))
        hop = base*(y[:,:-1]*vacancies[:,1:]*np.exp(-np.maximum(du,0)/kt)
                  - y[:,1:]*vacancies[:,:-1]*np.exp(-np.maximum(-du,0)/kt))
        if not opt.hopping:
            hop *= 0
        change = np.zeros_like(y)
        change[:,1:] += hop
        change[:,:-1] -= hop
        # PF OFF retains ordinary zero-field thermal emission.
        lowering = np.sqrt(e*np.abs(local_f)/(np.pi*epsilon_0*opt.optical_k)) if opt.pf else 0
        loss = opt.escape_fraction*opt.emission_hz*np.exp(-np.maximum(en-lowering,0)/kt)*y
        change -= loss
        currents["PF_thermal"] = e*cap*np.sum(-signs*loss)
        # WKB escape from each localized site through actual intervening films.
        # Midpoint barrier in each linear-potential segment. Energies relative to Si band edge.
        ns_offset = np.array([2.,5.1-eg-2.])[:,None]
        trap_energy = ns_offset + energy
        phi_left_n = surface-disp[0]*tunnel/(3.9*epsilon_0)
        phi_right_n = gate + disp[-1]*8e-9/(block_k*epsilon_0)
        phi_nodes = np.r_[phi_left_n,phi,phi_right_n]
        widths = np.diff(np.r_[0,x,7e-9])
        coef = 2*np.sqrt(2*electron_mass*e)/hbar
        for gate_side in (False,True):
            masses = (0.3,1.) if gate_side and device!="SONOS" else (opt.sio2_me,opt.sio2_mh)
            width = 8e-9 if gate_side else tunnel
            end_v = gate if gate_side else surface
            # Band-edge offsets relative to Si (affinity-rule parameters; EgSi approx 1.12 eV).
            offset = np.array([2.55,8.-eg-2.55] if gate_side and device!="SONOS" else [3.10,9.-eg-3.10])[:,None]
            inner_v = phi_right_n if gate_side else phi_left_n
            action_length = width*np.sqrt(np.array(masses)[:,None])*mean_sqrt_barrier(
                offset+signs*end_v-trap_energy,offset+signs*inner_v-trap_energy)
            for i in range(n):
                seg = slice(i+1,None) if gate_side else slice(None,i+1)
                action_length[:,i] += np.sum(widths[seg]*mean_sqrt_barrier(ns_offset+signs*phi_nodes[:-1][seg]-trap_energy[:,i,None],ns_offset+signs*phi_nodes[1:][seg]-trap_energy[:,i,None]),axis=1)
            # Occupied and empty reservoir states share the same WKB coupling.
            # Electron/hole energies are referenced to bulk Si CB/VB respectively.
            mu = np.array([ef0-eg,-ef0])[:,None] + (signs*vg if gate_side else 0.)
            filled = expit((mu-trap_energy)/kt)
            accessible = np.ones_like(filled) if gate_side else expit((trap_energy-signs*surface)/kt)
            coupling = opt.elastic_hz*accessible*np.exp(-coef*action_length)
            exchange = coupling*(filled-y)
            change += exchange
            side = "gate" if gate_side else "Si"
            for j,carrier in enumerate(("e","h")):
                currents[side+"_trap_"+carrier] = e*cap*signs[j,0]*sum(exchange[j])
        if opt.fn:
            for species, sign in enumerate((-1, 1)):
                for gate_side in (False, True):
                    if gate_side:
                        field = -sign*disp[-1]/(epsilon_0*block_k)
                        barrier, width = right_phi[species], 8e-9
                        dist = 7e-9-x
                    else:
                        field = sign*disp[0]/(epsilon_0*(3.9 if tunnel else 7.5))
                        barrier, width = left_phi[species], tunnel or 7e-9
                        dist = x
                    if gate_side and device!="SONOS":
                        mass = (0.3,1.)[species]
                    elif gate_side or tunnel:
                        mass = (opt.sio2_me,opt.sio2_mh)[species]
                    else:
                        mass = 1.
                    current = fn_supply(field,barrier,mass,width)
                    if not gate_side:
                        # Incident Si flux limits the band-injection current.
                        carrier_density = mobile(ef0+surface)[species]
                        supply = e*carrier_density*np.sqrt(kt*e/(2*np.pi*electron_mass*(.26,.39)[species]))
                        if device=="TANS":
                            # Injection into propagating nitride band states. Direct
                            # transitions to localized traps are handled by exchange above.
                            # Require a turning point inside the nitride for field emission.
                            fraction = 1-barrier/max(field*width,1e-30)
                            current *= max(fraction,0.)**2
                            current += supply*np.exp(-barrier/kt)
                        current = min(current,supply)
                    weight = np.exp(-dist/2e-9)
                    weight /= weight.sum()
                    incoming = opt.capture_fraction*current/(e*cap)*weight
                    # Capture fills empty traps or neutralizes trapped opposite charge.
                    capture = incoming*vacancies[species]
                    neutralize = 0.1*incoming*y[1-species]
                    # Divide a finite incident flux between both capture processes.
                    scale = np.maximum(1.,vacancies[species]+0.1*y[1-species])
                    change[species] += capture/scale
                    change[1-species] -= neutralize/scale
                    key = ("gate" if gate_side else "Si")+"_band_"+("e" if species==0 else "h")
                    currents[key] = sign*e*cap*np.sum((capture+neutralize)/scale)
        if diagnostics:
            net = e*cap*np.sum(signs*change)
            return [surface,net,net-sum(currents.values()),*[currents.get(k,0.) for k in PATHS]]
        return change

    snapshots, history = {}, []
    def record(label, elapsed, state, vg):
        _, _, sheet, _ = fields(state.reshape(2,n),vg)
        dvt = -sheet @ to_gate
        qf = -dvt / (e*r.sum()) / 1e4
        history.append((label,elapsed,vg,sheet.sum(),dvt,qf,*state,*rates(state.reshape(2,n),vg,True)))
        return dvt,qf

    def segment(label, start, v0, v1, duration):
        def bias(t):
            return v0+(v1-v0)*(t/duration)
        t = np.r_[0,np.geomspace(max(duration*1e-12,1e-20),duration,45)]
        sol = solve_ivp(lambda t,s:rates(s.reshape(2,n),bias(t)).ravel(),
                        (0,duration),start,method="BDF",atol=1e-11,rtol=2e-6,t_eval=t)
        if not sol.success or not np.isfinite(sol.y).all() or sol.y.min() < -1e-6 or sol.y.max()>1+1e-6:
            raise RuntimeError(f"{label}: solver or occupancy failure: {sol.message}")
        for time, state in zip(sol.t,sol.y.T):
            record(label,time,state,bias(time))
        return sol.y[:,-1].copy()
    def pulse(name,start,v,duration):
        s=segment(name+"_rise",start,0,v,1e-9)
        s=segment(name+"_hold",s,v,v,duration-1e-9)
        return segment(name+"_fall",s,v,0,1e-9)
    fresh = np.zeros(2*n)
    pgm = pulse("program",fresh,16,1e-4)
    nominal = opt
    if opt.no_erase_hopping:
        opt = replace(opt, hopping=False)
    ers = pulse("erase",pgm,-12,5e-4)
    opt = nominal
    for label, state in (("fresh",fresh),("programmed",pgm),("erased",ers),
              ("program_retained",segment("program_retention",pgm,0,0,opt.retention_s)),
              ("erase_retained",segment("erase_retention",ers,0,0,opt.retention_s))):
        snapshots[label] = record(label,0,state,0)
    return history,snapshots


def write(device, options, folder):
    history, states = {"SONOS":sonos,"TANOS":tanos,"TANS":tans}[device](options)
    folder.mkdir(exist_ok=True,parents=True)
    with (folder/f"{device}_history.csv").open("w",newline="") as f:
        writer=csv.writer(f)
        writer.writerow(["stage","stage_time_s","stack_voltage_V","Q_C_m2","deltaVt_V","equiv_Qf_cm-2",
                         *[f"{s}_plane{i}" for s in ("electron","hole") for i in range(1,options.planes+1)],"psi_s_V","dQdt_A_m2","balance_error_A_m2",*PATHS])
        writer.writerows(history)
    template=(Path(__file__).parent/"templates"/f"{device}.txt").read_text()
    for state,(_,qf) in states.items():
        tag=f"{device}_{options.temperature:g}K_{state}"
        (folder/f"{tag}.in").write_text(template.format(tag=tag,qf=f"{qf:.15g}",temperature=options.temperature))
    # One standalone DeckBuild input per device for all five read states.
    combined = []
    for state in states:
        stem = f"{device}_{options.temperature:g}K_{state}"
        body = (folder/f"{stem}.in").read_text().removesuffix("quit\n")
        combined.append(body)
    (folder/f"RUN_{device}.in").write_text("\n".join(combined)+"quit\n")

    # Sample the actual final hold row, before the 1 ns return to zero.
    # Fixed-Qf DC bias ramps expose the Si junction rate under the pulse bias.
    # They do not feed generated carriers back into the 1-D occupancy ODE.
    diagnostics = []
    for phase, voltage in (("program",16),("erase",-12)):
        row = next(row for row in reversed(history) if row[0] == phase+"_hold")
        tag = f"{device}_{options.temperature:g}K_{phase}_hold"
        setup = template.format(tag=tag,qf=f"{row[5]:.15g}",temperature=options.temperature)
        setup = setup.split("solve init\n",1)[0]
        step = 0.05 if voltage>0 else -0.05
        diagnostics.append(setup+f"solve init\nlog outf={tag}_bias.log\nsolve vcgate=0\n"
                           f"solve name=cgate vstep={step} vfinal={voltage}\n"
                           f"log off\nsave outf={tag}.str\n")
    (folder/f"BIAS_{device}.in").write_text("\n".join(diagnostics)+"quit\n")
    # Matched BTBT-off controls, with separate output names.
    for kind in ("RUN", "BIAS"):
        name = f"{kind}_{device}"
        positive = (folder/f"{name}.in").read_text()
        negative = positive.replace(" bbt.kl print"," print").replace(f"{device}_",f"{device}_noBTBT_")
        (folder/f"{name}_noBTBT.in").write_text(negative)
    return states

if __name__=="__main__":
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument("--temperature",type=float,default=77)
    parser.add_argument("--retention",type=float,default=1.)
    parser.add_argument("--out",type=Path,default=Path("generated"))
    parser.add_argument("--sio2-me", type=float, default=0.3)
    parser.add_argument("--sio2-mh", type=float, default=1.0)
    for flag in ("fn","hopping","pf"):
        parser.add_argument("--no-"+flag,action="store_true")
    parser.add_argument("--no-erase-hopping", action="store_true")
    parser.add_argument("--planes", type=int, default=4, help="number of nitride trap planes (grid study)")
    parser.add_argument("--devices", default="SONOS,TANOS,TANS", help="comma list, e.g. SONOS")
    args=parser.parse_args()
    config=Options(args.temperature,args.retention,not args.no_hopping,not args.no_fn,not args.no_pf, sio2_me=args.sio2_me, sio2_mh=args.sio2_mh, no_erase_hopping=args.no_erase_hopping, planes=args.planes)
    for name in args.devices.upper().split(","):
        print(name,write(name,config,args.out))
