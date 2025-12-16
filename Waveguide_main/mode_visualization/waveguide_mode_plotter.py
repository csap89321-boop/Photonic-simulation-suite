# Lumerical Automation Script for Unconditional Dual-Solve and Visualization
#
# This script connects to Lumerical MODE, builds a waveguide,
# runs the FDE solver twice unconditionally, and then extracts
# and plots the field profile for every mode found in the final run.
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Add the Lumerical API path to Python's search paths
# --- MODIFY THIS LINE IF YOUR LUMERICAL INSTALLATION IS DIFFERENT ---
lumapi_path = r"C:\Program Files\Lumerical\v241\api\python"
if lumapi_path not in sys.path:
    sys.path.append(lumapi_path)
import lumapi

# --- Main Function to Run the Simulation and Analysis ---
def run_dual_solve_and_plot():
    """
    Connects to Lumerical MODE, runs the FDE solver twice, and then
    plots the profile of every mode found in the final run.
    """
    with lumapi.MODE() as mode:
        print("Successfully connected to Lumerical MODE session.")
        mode.newproject()
        print("Cleared existing project.")

        # --- Define Geometric and Simulation Parameters ---
        wg_width = 0.45e-6
        wg_height = 0.22e-6
        sub_thickness = 2.0e-6
        wg_length = 5.0e-6
        center_wavelength = 1.55e-6
        file_name = "waveguidepy_final.lms"

        # --- Add Waveguide Structure (Si3N4 on Insulator) ---
        mode.addrect(
            name="substrate", x_min=0, x_max=wg_length,
            y_min=-2.5e-6, y_max=2.5e-6,
            z_min=-wg_height / 2 - sub_thickness, z_max=-wg_height / 2,
            material="SiO2 (Glass) - Palik"
        )
        mode.addrect(
            name="waveguide", x_min=0, x_max=wg_length,
            y_min=-wg_width / 2, y_max=wg_width / 2,
            z_min=-wg_height / 2, z_max=wg_height / 2,
            material="Si (Silicon) - Palik"
        )
        print("Waveguide geometry created.")

        # --- Add and Configure FDE Solver ---
        mode.addfde(
            solver_type="2D X normal", x=wg_length / 2,
            y_min=-2e-6, y_max=2e-6, z_min=-1.5e-6, z_max=1.5e-6,
            wavelength=center_wavelength
        )
        mode.setnamed("FDE", "number of trial modes", 10)
        mode.setnamed("FDE", "y min bc", "PML")
        mode.setnamed("FDE", "y max bc", "PML")
        mode.setnamed("FDE", "z min bc", "PML")
        mode.setnamed("FDE", "z max bc", "PML")
        print("FDE solver configured.")
        
        # --- Set the number of mesh cells for the FDE region ---
        mode.setnamed("FDE", "mesh cells y", 200)
        mode.setnamed("FDE", "mesh cells z", 200)
        print("Set FDE mesh cells to 200 in both Y and Z directions.")

        # --- Run the FDE Solver twice, unconditionally ---
        print("\nCalculating modes (first run)...")
        mode.findmodes()
        print("First run finished.")

        print("\nRe-running solver (second run)...")
        num_found = mode.findmodes() # Results from this run will be used
        print(f"Second run finished. Final mode count: {num_found}.")

        # --- Loop Through All Found Modes to Get and Plot Profiles ---
        print("\n--- Starting Data Extraction and Plotting ---")
        if num_found > 0:
            for i in range(1, int(num_found) + 1):
                print(f"Extracting and plotting Mode {i}...")
                # Extract data for the current mode
                neff = mode.getdata(f"mode{i}", "neff")
                y = mode.getdata(f"mode{i}", "y").flatten() * 1e6
                z = mode.getdata(f"mode{i}", "z").flatten() * 1e6
                Ey = mode.getdata(f"mode{i}", "Ey")
                Ez = mode.getdata(f"mode{i}", "Ez")
                
                # Calculate and normalize E-field intensity
                E_intensity = np.abs(np.squeeze(Ey))**2 + np.abs(np.squeeze(Ez))**2
                if E_intensity.max() > 0:
                    E_intensity /= E_intensity.max()

                # Plot the results
                fig, ax = plt.subplots(figsize=(8, 6))
                ax.pcolormesh(y, z, E_intensity.T, shading='gouraud', cmap='jet', vmin=0, vmax=1)
                
                # Add a rectangle to outline the waveguide core
                wg_rect = Rectangle((-wg_width*1e6/2, -wg_height*1e6/2), wg_width*1e6, wg_height*1e6,
                                    linewidth=1.5, edgecolor='w', facecolor='none', linestyle='--')
                ax.add_patch(wg_rect)
                
                ax.set_title(f"Mode {i} Profile | $n_{{eff}}$ = {np.real(neff).item():.4f}")
                ax.set_xlabel("Y Position (μm)")
                ax.set_ylabel("Z Position (μm)")
                ax.axis('equal')
                plt.show()
        else:
            print("No modes were found to plot.")

        # --- Save the Project File After Running ---
        mode.save(file_name)
        saved_path = os.path.join(os.getcwd(), file_name)
        print(f"\nProject file with final results saved successfully as '{saved_path}'")

# --- Execute the script ---
if __name__ == "__main__":
    run_dual_solve_and_plot()
