# Zemax Ball Lens Coupling Efficiency Sweep

## Purpose
This script automates Zemax OpticStudio to analyze fiber coupling efficiency using a ball lens. It connects to the OpticStudio API (ZOS-API), loads a base optical design, and performs a nested parametric sweep to find the optimal working distance for various lens radii.

## Key Workflow

1. System Setup & Connection
The script establishes a connection to Zemax OpticStudio and loads the baseline optical file (`ball lens 2.ZOS`). It programmatically accesses the Lens Data Editor (LDE) to control surface properties.

2. Parameter Configuration
It identifies and targets three critical system components:
• Surface 1: Front surface of the ball lens (STOP).
• Surface 2: Rear surface of the ball lens.
• System Aperture: Dynamically set to the Entrance Pupil Diameter (EPD).
Original configuration values are backed up to ensure the system can be restored after analysis.

3. Parametric Sweep
The core logic executes a nested loop analysis across 610 total configurations:
• Lens Radii: Sweeps 10 different radii from 10 mm to 100 mm.
• Working Distances: Sweeps 0 mm to 60 mm in 1 mm increments.

For each iteration, the script updates the lens geometry (Radius = ±R, Thickness = 2R) and scales the system aperture (EPD = Radius).

4. Efficiency Calculation
For every configuration, the script runs **Geometric Image Analysis (GIA)** within Zemax. It parses the text output to extract the fiber coupling efficiency value, storing it for analysis.

## Output

• **Visualization:** Generates a comprehensive plot overlaying efficiency curves for all 10 lens radii, marking the optimal working distance (peak efficiency) for each with a star marker.
<img width="2289" height="1281" alt="image" src="https://github.com/user-attachments/assets/05d7a2aa-2bf8-4534-82d4-ea8bbb9f55d6" />

• **Summary Data:** Outputs a table listing the exact optimal working distance and maximum achievable efficiency for each lens size.
<img width="905" height="366" alt="image" src="https://github.com/user-attachments/assets/c5267cba-6d63-4c11-8f64-7f1dfc5f989b" />

• **System Restoration:** Automatically cleans up temporary simulation files and resets the Zemax design to its original state.
