# Waveguide Mode Visualization

## Purpose
This script automates the creation and analysis of a Silicon Nitride (Si3N4) waveguide on an SiO2 substrate. It runs the Finite Difference Eigenmode (FDE) solver to find supported optical modes and generates high-quality field profile plots for every mode found.

## Key Features
1 Geometry Automation: Programmatically builds a 450nm x 220nm waveguide structure.
2 Automated Visualization: Loops through all found modes (fundamental and higher-order) and generates normalized E-field intensity plots using Matplotlib.
3 Data Extraction: Calculates effective index ($n_{eff}$) and mode confinement factors.
