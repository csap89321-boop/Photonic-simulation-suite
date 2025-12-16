# Ring Resonator Coupling Gap Sweep

Purpose
This script expands on the basic ring resonator design by performing a parameter sweep of the coupling gap distance. It automatically builds, runs, and analyzes simulations for four specific gap values (50 nm, 60 nm, 70 nm, and 100 nm) to determine how coupling strength affects the spectral response.

Key Workflow

1. Single Session Architecture
The script operates within a single persistent Lumerical FDTD session. Instead of opening and closing multiple windows, it uses a loop that clears the workspace (newproject) between iterations. This approach is computationally efficient and keeps the desktop environment clean.

2. Smart File Handling
To save simulation time, the script implements a check-before-run logic. For every gap value, it checks if a corresponding compiled simulation file (.fsp) already exists.
• If found: It loads the existing file and skips directly to data extraction.
• If not found: It builds the geometry from scratch, runs the full FDTD simulation, and saves the file.

3. Geometry & Simulation
For each iteration, the script dynamically adjusts the waveguide vertical position based on the current gap value. It configures the full simulation environment, including:
• 3D FDTD solver region with PML boundaries.
• Mode source injection.
• Time-domain execution (4000 fs duration).

4. Data Extraction & Normalization
Post-simulation, the script extracts raw transmission data and the source input power. It calculates the Normalized Transmission (T = Output / Input) to ensure accurate spectral analysis regardless of source variations.

Output
• Simulation Files: Saves individual .fsp files for each gap configuration (e.g., gap_50nm.fsp).
• Visualization: Generates a comparative plot overlaying the transmission spectra for all four gap values, allowing for direct assessment of resonance depth, bandwidth, and extinction ratio changes.
