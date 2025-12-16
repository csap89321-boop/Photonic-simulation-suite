This script programmatically builds a 3D FDTD model of a symmetric silicon microring resonator with an add-drop configuration in Lumerical. It automates the geometry construction, source placement, and monitor setup, saving a ready-to-run simulation file (.fsp).

Key Features
1. Geometry & Materials
Structure: Creates a central silicon ring with two symmetric straight bus waveguides (upper and lower).

Materials: Standard Silicon-on-Insulator (SOI) platform (Si core, SiO2 cladding).

Parametric Control: Automated setup of ring radius, waveguide width/height, and the critical coupling gap distance.

2. Simulation Configuration
Solver: 3D FDTD with PML boundaries.

Time Domain: Sets simulation time to 4000 fs to allow for sufficient field decay in high-Q resonances.

Mesh & Resolution: Configured for broadband simulation (1.5 µm - 1.6 µm) with 500 frequency points.

3. Source & Monitors
Excitation: Fundamental TE mode source injected into the upper waveguide (Input Port).

Data Collection:

4-Port Analysis: Power monitors placed at Input, Through, Add, and Drop ports to measure transmission spectra.

Field Visualization: A central Z-plane monitor captures the 2D field distribution to visualize coupling and resonance.

Output
Generates a fully configured Lumerical project file: ring_resonator_add_drop.fsp.

Note: This script builds the simulation file but does not run it. Open the file in Lumerical FDTD to execute the simulation and view results.
