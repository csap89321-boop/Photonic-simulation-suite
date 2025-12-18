import os
import numpy as np
import matplotlib.pyplot as plt
import zospy as zp

# Initialize and connect to ZOS
zos = zp.ZOS()

try:
    zos.disconnect()
except:
    pass

oss = zos.connect()

# Load the corrected ballad file (with real Edmund Optics achromat)
file_path = r"C:\Users\Sumedh\Downloads\ball lens\ballad_corrected.ZOS"
oss.load(file_path, saveifneeded=False)

print("ballad_corrected.ZOS file loaded successfully")
lde = oss.LDE

print(f"\n{'='*60}")
print("CURRENT CONFIGURATION (Real Edmund Optics Achromat):")
print(f"{'='*60}")
for i in range(lde.NumberOfSurfaces):
    surf = lde.GetSurfaceAt(i)
    mat = surf.Material if surf.Material else "Air"
    print(f"Surface {i}: {surf.Comment:<20} | R: {surf.Radius:>8.3f} | T: {surf.Thickness:>8.3f} | Mat: {mat:<10}")

# Get the surfaces
surface_2 = lde.GetSurfaceAt(2)  # Ball lens rear - controls distance to doublet

# Store original distance
original_distance = surface_2.Thickness
print(f"\n{'='*60}")
print(f"Current ball-to-doublet distance: {original_distance} mm")
print(f"{'='*60}\n")

# Define distance values to sweep (1mm to 20mm in 1mm steps)
distance_values = np.arange(1, 21, 1, dtype=float)  # 1 to 20mm

efficiencies = []

print("="*60)
print("SWEEPING BALL-TO-DOUBLET DISTANCE (1mm to 20mm)")
print("With REAL Edmund Optics Achromat Specs")
print("="*60)
print(f"Step size: 1mm")
print(f"Total points: {len(distance_values)}")
print("="*60 + "\n")

# Temporary text file path
text_file = r"C:\Users\Sumedh\Downloads\ball lens\gia_corrected_ballad_temp.txt"

# Loop through distances
for distance in distance_values:
    # Set the distance from ball lens to doublet
    surface_2.Thickness = float(distance)
    
    try:
        # Run Geometric Image Analysis
        gia = oss.Analyses.New_Analysis(zp.constants.Analysis.AnalysisIDM.GeometricImageAnalysis)
        gia.ApplyAndWaitForCompletion()
        gia_results = gia.GetResults()
        
        # Get text file output
        success = gia_results.GetTextFile(text_file)
        
        if success and os.path.exists(text_file):
            with open(text_file, 'r', encoding='utf-16') as f:
                content = f.read()
            
            # Extract efficiency
            efficiency = None
            for line in content.split('\n'):
                if 'Efficiency' in line and ':' in line:
                    try:
                        parts = line.split(':')
                        if len(parts) >= 2:
                            efficiency_str = parts[1].strip().replace('%', '').strip()
                            efficiency = float(efficiency_str)
                            break
                    except:
                        pass
            
            if efficiency is not None:
                efficiencies.append(efficiency)
                print(f"Ball-to-doublet distance: {distance:5.1f} mm -> Efficiency: {efficiency:6.2f}%")
            else:
                efficiencies.append(np.nan)
                print(f"Ball-to-doublet distance: {distance:5.1f} mm -> Could not extract efficiency")
        else:
            efficiencies.append(np.nan)
            print(f"Ball-to-doublet distance: {distance:5.1f} mm -> Text file not created")
        
        gia.Close()
        
    except Exception as e:
        print(f"Error at distance {distance}: {e}")
        efficiencies.append(np.nan)

# Restore original distance
surface_2.Thickness = original_distance
print(f"\nRestored original distance: {original_distance} mm")

# Clean up temp file
try:
    if os.path.exists(text_file):
        os.remove(text_file)
except:
    pass

# Convert to numpy array
efficiencies = np.array(efficiencies)

print(f"\nResults summary:")
print(f"  Valid efficiencies: {np.sum(~np.isnan(efficiencies))}")
if np.any(~np.isnan(efficiencies)):
    print(f"  Efficiency range: {np.nanmin(efficiencies):.2f}% to {np.nanmax(efficiencies):.2f}%")

# Check if we have valid data
valid_indices = ~np.isnan(efficiencies)

if not np.any(valid_indices):
    print("\nERROR: No valid efficiency data extracted")
else:
    # Create plot
    fig, ax = plt.subplots(figsize=(14, 8))
    
    ax.plot(distance_values[valid_indices], efficiencies[valid_indices], 
            '-o', linewidth=3, markersize=8, color='#029E73', 
            label='Coupling Efficiency (Real Edmund Achromat)')
    
    ax.set_xlabel('Distance from ball lens to achromatic doublet [mm]', fontsize=14, fontweight='bold')
    ax.set_ylabel('Coupling efficiency [%]', fontsize=14, fontweight='bold')
    ax.set_title('Ball Lens + Real Edmund Optics Achromat: Efficiency vs Ball-to-Doublet Distance\n(R=50mm Ball, 12.5mm Edmund Achromat, EPD=50mm)', 
                 fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlim([0, 21])
    ax.set_ylim([0, max(100, np.nanmax(efficiencies)*1.1)])
    
    # Mark the optimal point
    best_idx = np.nanargmax(efficiencies)
    best_distance = distance_values[best_idx]
    best_efficiency = efficiencies[best_idx]
    
    ax.plot(best_distance, best_efficiency, '*', markersize=25, 
            color='red', markeredgecolor='black', markeredgewidth=2,
            label=f'Optimal: {best_efficiency:.2f}% at {best_distance:.0f}mm')
    
    ax.axvline(best_distance, color='red', linestyle='--', linewidth=2, alpha=0.5)
    
    # Mark current position (17mm)
    if 17 in distance_values:
        current_idx = np.where(distance_values == 17)[0][0]
        current_eff = efficiencies[current_idx]
        ax.axvline(17, color='orange', linestyle='--', linewidth=2, 
                   alpha=0.5, label=f'Current (17mm): {current_eff:.2f}%')
    
    ax.legend(fontsize=12, loc='best', framealpha=0.95, edgecolor='black')
    
    # Thicker axes (Nature style)
    for spine in ax.spines.values():
        spine.set_linewidth(1.5)
    
    plt.tight_layout()
    
    # Save plot
    save_path = r'C:\Users\Sumedh\Downloads\ball lens\efficiency_vs_ball_to_doublet_REAL_achromat.png'
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()
    
    # Print detailed summary
    print(f"\n{'='*70}")
    print(f"BALL LENS + REAL EDMUND OPTICS ACHROMAT OPTIMIZATION")
    print(f"{'='*70}")
    print(f"System configuration:")
    print(f"  - Ball lens: R=50mm, D=100mm, EPD=50mm")
    print(f"  - Achromatic doublet: Real Edmund Optics specs")
    print(f"    • Diameter: 12.5mm, EFL: 20mm")
    print(f"    • Materials: S-BAH11 (crown) + N-SF10 (flint)")
    print(f"    • R1=13.98mm, R2=-9.35mm, R3=-76.14mm")
    print(f"  - Doublet-to-fiber distance: 15mm (fixed)")
    print(f"\nOptimization results:")
    print(f"  - Optimal ball-to-doublet distance: {best_distance:.0f} mm")
    print(f"  - Maximum coupling efficiency:      {best_efficiency:.2f} %")
    
    if 17 in distance_values:
        print(f"  - Current position (17mm):          {current_eff:.2f} %")
        print(f"  - Improvement potential:            {best_efficiency - current_eff:.2f} pp")
    
    # Calculate total optical path
    doublet_thickness = 6.35  # 5.25mm + 1.10mm
    doublet_to_fiber = 15.0  # Fixed
    total_at_optimal = best_distance + doublet_thickness + doublet_to_fiber
    
    print(f"\n{'='*70}")
    print(f"OPTICAL PATH AT OPTIMAL CONFIGURATION:")
    print(f"{'='*70}")
    print(f"  Ball rear → Doublet front:  {best_distance:.0f} mm")
    print(f"  Through doublet:            {doublet_thickness} mm")
    print(f"  Doublet rear → Fiber:       {doublet_to_fiber} mm")
    print(f"  TOTAL (ball rear to fiber): {total_at_optimal:.2f} mm")
    print(f"{'='*70}")
    
    print(f"\nPlot saved to: {save_path}")
