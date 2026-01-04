# Lumerical FDE Parametric Sweep for SOI Waveguides

This Python script automates the design and modal analysis of Silicon-on-Insulator (SOI) waveguides using the **Ansys Lumerical API**. It constructs a parametric geometry (including grating features) and performs an FDE (Finite Difference Eigenmode) sweep to analyze mode confinement.


<img width="1218" height="521" alt="soi" src="https://github.com/user-attachments/assets/623cde9d-a7bf-42f6-b82b-59701abccf90" />


## Key Features
* **Automated Geometry:** Programmatically builds Clad, BOX, Wafer, Waveguide, and Grating structures.
* **FDE Solver Setup:** Configures mesh settings and boundary conditions for eigenmode solving.
* **Custom Sweep Engine:** Defines and runs parametric sweeps (e.g., Waveguide Width vs. Effective Index) completely via Python.
* **Data Visualization:** Automatically extracts simulation results and generates dispersion plots using Matplotlib.

## Usage
1.  Update the `lumapi_path` variable to point to your local Lumerical installation.
2.  Choose your sweep parameter (Width or Thickness) in the `__main__` section.
3.  Run the script to generate the $n_{eff}$ dispersion curves.

## Dependencies
* Python 3.x
* Numpy
* Matplotlib
* Ansys Lumerical (lumapi)
