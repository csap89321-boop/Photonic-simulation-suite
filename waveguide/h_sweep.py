"""
Plasmonic Waveguide Analysis Script
Author: Chittilla Sumedh Srujan
Description: Sweeps Ag structure positions to analyze mode confinement in a 200nm slot.
Full documentation available in README.md
"""
# Sweep Ag1 and Ag2 positions - Constant slot width 200 nm
import sys
import os
import numpy as np
import matplotlib.pyplot as plt

lumapi_path = r"C:\Program Files\Lumerical\v241\api\python"
if lumapi_path not in sys.path:
    sys.path.append(lumapi_path)
import lumapi

def sweep_ag_positions():
    lms_file = r"C:\Users\Sumedh\Downloads\python\Waveguides\AG_DSHP.lms"
    
    with lumapi.MODE() as mode:
        print(f"Loading: {os.path.basename(lms_file)}\n")
        mode.load(lms_file)
        mode.switchtolayout()
        
        # Ag1 position sweep: 2.915 to 2.725 µm (10 points)
        ag1_positions = np.linspace(2.915e-6, 2.725e-6, 10)
        
        # Ag2 position sweep: 4.285 to 4.475 µm (10 points)
        ag2_positions = np.linspace(4.285e-6, 4.475e-6, 10)
        
        # Storage
        neff_array = []
        fraction_array = []
        gap_width_array = []
        
        print("="*70)
        print("POSITION SWEEP: 10 points, slot width = 0.2 µm")
        print("="*70)
        print(f"Ag1: {ag1_positions[0]*1e6:.3f} → {ag1_positions[-1]*1e6:.3f} µm")
        print(f"Ag2: {ag2_positions[0]*1e6:.3f} → {ag2_positions[-1]*1e6:.3f} µm\n")
        
        for idx, (ag1_y, ag2_y) in enumerate(zip(ag1_positions, ag2_positions), 1):
            print(f"[{idx}/10] Ag1={ag1_y*1e6:.3f} µm, Ag2={ag2_y*1e6:.3f} µm", end=" ")
            
            # Set positions
            mode.switchtolayout()
            mode.setnamed("Ag1", "y", ag1_y)
            mode.setnamed("Ag2", "y", ag2_y)
            
            # Get geometry boundaries
            wg_y_min = mode.getnamed("waveguide", "y min")
            wg_z_min = mode.getnamed("waveguide", "z min")
            wg_z_max = mode.getnamed("waveguide", "z max")
            ag1_y_max = mode.getnamed("Ag1", "y max")
            
            # Integration region: Ag1 max to waveguide min
            y2_int = ag1_y_max
            y1_int = wg_y_min
            z2_int = wg_z_min
            z1_int = wg_z_max
            
            gap_width = (y1_int - y2_int) * 1e6  # in µm
            gap_width_array.append(gap_width)
            
            print(f"→ Gap={gap_width:.3f} µm", end=" ")
            
            # Run solver twice
            mode.findmodes()
            num_found = mode.findmodes()
            
            # Find best mode
            best_idx = 1
            best_neff = 0
            for m in range(1, min(5, int(num_found)) + 1):
                try:
                    neff_val = np.real(mode.getdata(f"mode{m}", "neff")).item()
                    if 1.5 < neff_val < 3.2 and neff_val > best_neff:
                        best_neff = neff_val
                        best_idx = m
                except:
                    continue
            
            mode.selectmode(best_idx)
            neff = np.real(mode.getdata(f"mode{best_idx}", "neff")).item()
            print(f"→ neff={neff:.4f}", end=" ")
            
            # Extract fields
            Ex = np.squeeze(mode.getdata(f"mode{best_idx}", "Ex"))
            Ey = np.squeeze(mode.getdata(f"mode{best_idx}", "Ey"))
            Ez = np.squeeze(mode.getdata(f"mode{best_idx}", "Ez"))
            
            y_m = mode.getdata(f"mode{best_idx}", "y").flatten()
            z_m = mode.getdata(f"mode{best_idx}", "z").flatten()
            
            # Calculate intensity
            Y, Z = np.meshgrid(y_m, z_m, indexing='ij')
            E_int = np.abs(Ex)**2 + np.abs(Ey)**2 + np.abs(Ez)**2
            
            # Integration mask
            mask = ((Y >= y2_int) & (Y <= y1_int) & 
                   (Z >= z2_int) & (Z <= z1_int))
            
            # Integrate
            dy = np.abs(y_m[1] - y_m[0]) if len(y_m) > 1 else 1e-9
            dz = np.abs(z_m[1] - z_m[0]) if len(z_m) > 1 else 1e-9
            dA = dy * dz
            
            total = np.sum(E_int) * dA
            region = np.sum(E_int * mask) * dA
            fraction = (region / total * 100) if total > 0 else 0.0
            
            neff_array.append(neff)
            fraction_array.append(fraction)
            
            print(f"→ {fraction:.2f}%")
        
        print(f"\n{'='*70}")
        print("Sweep complete!\n")
        
        # Plot results
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 10))
        
        point_labels = [f"P{i+1}" for i in range(10)]
        x_pos = np.arange(10)
        
        # E-field intensity
        ax1.plot(x_pos, fraction_array, 'b-o', linewidth=2, markersize=8)
        ax1.set_xlabel('Configuration Point', fontsize=12)
        ax1.set_ylabel('E-Field Intensity (%)', fontsize=12)
        ax1.set_title('E-Field Intensity in Gap vs Ag Position', fontsize=13, fontweight='bold')
        ax1.set_xticks(x_pos)
        ax1.set_xticklabels(point_labels)
        ax1.grid(True, alpha=0.3)
        
        # Effective index
        ax2.plot(x_pos, neff_array, 'r-s', linewidth=2, markersize=8)
        ax2.set_xlabel('Configuration Point', fontsize=12)
        ax2.set_ylabel('Effective Index', fontsize=12)
        ax2.set_title('Effective Index vs Ag Position', fontsize=13, fontweight='bold')
        ax2.set_xticks(x_pos)
        ax2.set_xticklabels(point_labels)
        ax2.grid(True, alpha=0.3)
        
        # Gap width verification
        ax3.plot(x_pos, gap_width_array, 'g-^', linewidth=2, markersize=8)
        ax3.set_xlabel('Configuration Point', fontsize=12)
        ax3.set_ylabel('Gap Width (µm)', fontsize=12)
        ax3.set_title('Gap Width vs Configuration (should be constant ~0.2 µm)', fontsize=13, fontweight='bold')
        ax3.set_xticks(x_pos)
        ax3.set_xticklabels(point_labels)
        ax3.grid(True, alpha=0.3)
        ax3.axhline(y=0.2, color='red', linestyle='--', label='Target: 0.2 µm')
        ax3.legend()
        
        plt.tight_layout()
        plt.show()
        
        # Save data
        try:
            data = np.column_stack((ag1_positions*1e6, ag2_positions*1e6, 
                                   gap_width_array, neff_array, fraction_array))
            np.savetxt("ag_position_sweep.csv", data, delimiter=',',
                      header="Ag1_y(um),Ag2_y(um),Gap_width(um),Neff,E_Field_Intensity(%)", 
                      comments='', fmt='%.6f')
            print("Data saved to: ag_position_sweep.csv")
        except:
            print("Could not save CSV")

if __name__ == "__main__":
    sweep_ag_positions()
