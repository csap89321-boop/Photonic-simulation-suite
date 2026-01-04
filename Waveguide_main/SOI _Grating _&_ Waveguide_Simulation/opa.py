import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# ---- Add the Lumerical API path to Python's search paths ----
# --- MODIFY THIS LINE IF YOUR LUMERICAL INSTALLATION IS DIFFERENT ---
lumapi_path = r"C:\Program Files\Lumerical\v241\api\python"
if lumapi_path not in sys.path:
    sys.path.append(lumapi_path)
import lumapi

# ---- Create Lumerical MODE object ----
fde = lumapi.MODE()

# ---- Device and Simulation Parameters ----
thick_Clad = 0.48e-6
thick_Si = 0.12e-6
thick_BOX = 2.0e-6
width_Si = 0.8e-6
N = 78
l_g = 0.64e-6
dc = 0.6
t_r = 0.08e-6
t_g = thick_Clad - t_r
l = N * l_g

material_Clad = "SiO2 (Glass) - Palik"
material_BOX = "SiO2 (Glass) - Palik"
material_Si = "Si (Silicon) - Palik"

width_margin = 2.0e-6
height_margin = 1.0e-6
Xmin = -1/2*10e-6
Xmax = l
Zmin = -height_margin
Zmax = thick_Si + height_margin
Y_span = 2*width_margin + width_Si
Ymin = -Y_span/2
Ymax = -Ymin

# ---- Geometry Construction ----
def geometry(sim):
    sim.newproject()
    sim.addstructuregroup()
    sim.set("name", "geometry")
    # Clad
    sim.addrect()
    sim.set("name", "clad")
    sim.addtogroup("geometry")
    sim.set("material", material_Clad)
    sim.set("y", 0)
    sim.set("y span", Y_span + 1e-6)
    sim.set("z min", 0)
    sim.set("z max", thick_Si + thick_Clad)
    sim.set("x min", Xmin)
    sim.set("x max", Xmax)
    sim.set("override mesh order from material database", 1)
    sim.set("mesh order", 2)
    sim.set("alpha", 0.5)
    # BOX
    sim.addrect()
    sim.set("name", "BOX")
    sim.addtogroup("geometry")
    sim.set("material", material_BOX)
    sim.set("x min", Xmin)
    sim.set("x max", Xmax)
    sim.set("y", 0)
    sim.set("y span", Y_span + 1e-6)
    sim.set("z min", -thick_BOX)
    sim.set("z max", 0)
    sim.set("alpha", 0.5)
    # Wafer
    sim.addrect()
    sim.set("name", "Wafer")
    sim.addtogroup("geometry")
    sim.set("material", material_Si)
    sim.set("x min", Xmin)
    sim.set("x max", Xmax)
    sim.set("z max", -thick_BOX)
    sim.set("z min", -thick_BOX - 2e-6)
    sim.set("y", 0)
    sim.set("y span", Y_span + 1e-6)
    sim.set("alpha", 0.4)
    # Waveguide
    sim.addrect()
    sim.set("name", "waveguide")
    sim.addtogroup("geometry")
    sim.set("material", material_Si)
    sim.set("x min", Xmin)
    sim.set("x max", Xmax)
    sim.set("z min", 0)
    sim.set("z max", thick_Si)
    sim.set("y", 0)
    sim.set("y span", width_Si)
    # Grating
    xo = Xmin + 10e-6
    material_gap = "etch"
    xpos = xo
    for i in range(1, N):
        sim.addrect()
        sim.set("name", "grating_gap")
        sim.addtogroup("geometry")
        sim.set("material", material_gap)
        sim.set("x", xpos + 0.5 * l_g * (1 - dc))
        sim.set("x span", l_g * (1 - dc))
        sim.set("y", 0)
        sim.set("y span", Y_span + 1e-6)
        sim.set("z min", thick_Si + t_r)
        sim.set("z max", thick_Si + t_r + t_g)
        xpos += l_g

# ---- FDE Region Setup ----
def setup_fde(sim):
    geometry(sim)
    sim.addfde()
    sim.set("solver type", 1)
    sim.set("z", 0)
    sim.set("z span", 4e-6)
    sim.set("x", 0)
    sim.set("y", thick_Si/2)
    sim.set("y span", 3e-6)
    sim.set("define y mesh by", 1)
    sim.set("define z mesh by", 1)
    sim.set("dy", 0.02e-6)
    sim.set("dz", 0.02e-6)
    sim.findmodes()

# ---- Parameter and Result Setup ----
def paramater_setup(name, parameter, start, stop):
    para = {
        "Name": name,
        "Parameter": f"::model::geometry::waveguide::{parameter}", 
        "Type": "Length",
        "Start": start,
        "Stop": stop,
        "Units": "microns"
    }
    return para

def result_setup(name, number):
    result = {
        "Name": name,
        "Result": f"::model::FDE::data::mode{number}::neff", 
    }
    return result

# ---- Sweep Routine ----
def sweep_parameters(sim, paramater_name, para):
    setup_fde(sim)  # Ensures region is enabled before sweep!
    sim.addsweep(0)
    sim.setsweep("sweep", "name", paramater_name)
    sim.setsweep(paramater_name, "type", "Ranges")
    sim.setsweep(paramater_name, "number of points", 10)
    neff = []
    for i in range(1, 5):
        neff.append(result_setup(f"neff{i}", i))
    sim.addsweepparameter(paramater_name, para)
    for i in range(1, 5):
        sim.addsweepresult(paramater_name, neff[i-1])
    sim.save("simulation.lms")  # Modify filename/path as needed
    sim.runsweep(paramater_name)

# ---- Sweep Results Plotting ----
def sweep_analysis(sim, sweep_name, p, x_):
    colors = ['b', 'orange', 'g', 'r']
    for i in range(1, 5):
        neff = sim.getsweepresult(sweep_name, f'neff{i}')
        plt.plot(neff[p][0], neff['neff'], marker='o', color=colors[i-1], label=f'neff{i}')
    plt.axhline(y=1.45, color='k', linestyle='--')
    plt.text(neff[p][0][0]+0.25e-6, 1.45 + 0.02, 'n_clad = 1.45', color='k')
    plt.axvline(x=x_, color='k', linestyle='-.')
    plt.text(x_ + 0.01e-6, plt.ylim()[1]*0.9, f'{p} = {x_*1e6:.0f} nm', rotation=90, color='k', va='bottom')
    plt.xlabel(p)
    plt.ylabel('Effective Index (neff)')
    plt.grid(True)
    plt.legend()
    plt.show()

# ---- Example Usage ----
para_t = paramater_setup(
    name="thickness",
    parameter="z span",
    start=0.05e-6,
    stop=0.5e-6
)
para_w = paramater_setup(
    name="width",
    parameter="y span",
    start=0.3e-6,
    stop=1.3e-6
)

# Run your desired sweep:
# sweep_parameters(fde, "thickness_sweep", para_t)
sweep_parameters(fde, "width_sweep", para_w)

# Plot the sweep results
# sweep_analysis(fde, "thickness_sweep", "thickness", 0.12e-6)
sweep_analysis(fde, "width_sweep", "width", 0.8e-6)
