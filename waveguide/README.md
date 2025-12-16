# Plasmonic Slot Waveguide Analysis

## Purpose
This script analyzes a plasmonic slot waveguide by systematically moving two silver structures (`Ag1` and `Ag2`) while maintaining a constant slot width of **200 nm**. It measures how electromagnetic field confinement and mode properties change during this translation.

## Key Operations
### 1. Initialization
* Loads a Lumerical MODE simulation file (`AG_DSHP.lms`).
* Establishes an API connection to control the simulation programmatically.

### 2. Position Sweep Parameters
* **Ag1 (Lower Silver):** Sweeps from 2.915 µm to 2.725 µm (10 points).
* **Ag2 (Upper Silver):** Sweeps from 4.285 µm to 4.475 µm (10 points).
* **Constraint:** Both structures move symmetrically to maintain a constant **200 nm slot width**.

### 3. Simulation Loop (10 Iterations)
For each configuration, the script:
1.  Updates `Ag1` and `Ag2` y-positions.
2.  Verifies the gap width calculation.
3.  Runs the FDE solver to identify the fundamental mode ($n_{eff}$ between 1.5 and 3.2).
4.  **Field Integration:** Calculates the percentage of total mode energy confined strictly within the gap region.

### 4. Output
* **Plots:** Generates plots for E-field intensity percentage vs. position and Effective Index ($n_{eff}$) vs. position.
* **Data:** Saves all metrics (Positions, Gap Width, $n_{eff}$, Intensity %) to a CSV file.

## Applications
Optimizing plasmonic waveguide designs for applications requiring strong field confinement in nanoscale gaps, such as biosensing, nonlinear optics, and enhanced light-matter interaction.
