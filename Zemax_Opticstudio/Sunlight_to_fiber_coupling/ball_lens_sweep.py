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

# Load the file from the ball lens folder
file_path = r"C:\Users\Sumedh\Downloads\ball lens\ball lens 2.ZOS"
oss.load(file_path, saveifneeded=False)

print("System loaded successfully")
lde = oss.LDE

# Get the surfaces
surface_1 = lde.GetSurfaceAt(1)  # STOP (front of ball lens)
surface_2 = lde.GetSurfaceAt(2)  # (aper) rear of ball lens
sys_aperture = oss.SystemData.Aperture

# Store original values
original_radius_1 = surface_1.Radius
original_thickness_1 = surface_1.Thickness
original_semi_dia_1 = surface_1.SemiDiameter
original_radius_2 = surface_2.Radius
original_thickness_2 = surface_2.Thickness
original_aperture = sys_aperture.ApertureValue

print(f"\nOriginal configuration saved")
print(f"  Radius: {original_radius_1} mm")
print(f"  Surface 2 thickness: {original_thickness_2} mm\n")

# Define radius values to sweep (10mm to 100mm)
radius_values = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]  # in mm

# Define working distance values (0 to 60mm in 1mm steps)
distance_values = np.arange(0, 61, 1, dtype=float)  # 0 to 60mm, 1mm increments

# Dictionary to store results for each radius
results = {}

# Temporary text file path - also in the ball lens folder
text_file = r"C:\Users\Sumedh\Downloads\ball lens\gia_temp.txt"

print("="*60)
print("STARTING COMPREHENSIVE BALL LENS ANALYSIS")
print("="*60)
print(f"Ball lens radii: {radius_values}")
print(f"Working distances: 0 to 60mm (step: 1mm)")
print(f"Total iterations: {len(radius_values) * len(distance_values)}")
print("="*60 + "\n")

# Loop through each radius
for radius in radius_values:
    print(f"\n{'='*60}")
    print(f"ANALYZING BALL LENS RADIUS: {radius} mm (Diameter: {2*radius} mm)")
    print(f"EPD: {radius} mm (50% of diameter)")
    print(f"{'='*60}")
    
    # Update ball lens parameters
    surface_1.Radius = float(radius)
    surface_1.Thickness = float(2 * radius)
    surface_1.SemiDiameter = float(radius)
    surface_2.Radius = float(-radius)
    surface_2.SemiDiameter = float(radius)
    sys_aperture.ApertureValue = float(radius)  # EPD = radius
    
    efficiencies = []
    
    # Loop through working distances
    for distance in distance_values:
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
                
                efficiencies.append(efficiency if efficiency is not None else np.nan)
                if efficiency is not None:
                    print(f"  Distance: {distance:5.1f} mm -> Eff: {efficiency:6.2f}%")
            else:
                efficiencies.append(np.nan)
            
            gia.Close()
            
        except Exception as e:
            print(f"  Error at distance {distance}: {e}")
            efficiencies.append(np.nan)
    
    # Store results
    results[radius] = np.array(efficiencies)

# Restore original values
surface_1.Radius = original_radius_1
surface_1.Thickness = original_thickness_1
surface_1.SemiDiameter = original_semi_dia_1
surface_2.Radius = original_radius_2
surface_2.Thickness = original_thickness_2
sys_aperture.ApertureValue = original_aperture

print(f"\n{'='*60}")
print("ANALYSIS COMPLETE - Original configuration restored")
print(f"{'='*60}\n")

# Clean up temp file
try:
    if os.path.exists(text_file):
        os.remove(text_file)
except:
    pass

# Create comprehensive plot with Nature-style colors
fig, ax = plt.subplots(figsize=(16, 9))


nature_colors = [
    '#0173B2',  # Blue
    '#DE8F05',  # Orange
    '#029E73',  # Green
    '#CC78BC',  # Purple
    '#CA9161',  # Brown
    '#949494',  # Gray
    '#ECE133',  # Yellow
    '#56B4E9',  # Sky blue
    '#E69F00',  # Dark orange
    '#009E73'   # Teal
]

# Plot each radius curve
for idx, radius in enumerate(radius_values):
    eff = results[radius]
    valid = ~np.isnan(eff)
    
    if np.any(valid):
        ax.plot(distance_values[valid], eff[valid], 
                '-', linewidth=2.5, 
                color=nature_colors[idx], label=f'R = {radius} mm')
        
        # Find and mark optimal point for this radius
        best_idx = np.nanargmax(eff)
        best_dist = distance_values[best_idx]
        best_eff = eff[best_idx]
        ax.plot(best_dist, best_eff, '*', markersize=18, 
                color=nature_colors[idx], markeredgecolor='black', markeredgewidth=1.5)

ax.set_xlabel('Distance between ball lens and fiber (mm)', fontsize=14, fontweight='bold')
ax.set_ylabel('Coupling efficiency (%)', fontsize=14, fontweight='bold')
ax.set_title('Ball lens fiber coupling efficiency versus working distance\nfor various ball lens radii (10–100 mm), EPD = radius', 
             fontsize=16, fontweight='bold')
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_xlim([0, 60])
ax.set_ylim([0, 100])
ax.legend(fontsize=11, loc='best', ncol=2, framealpha=0.95, edgecolor='black')


ax.spines['top'].set_linewidth(1.5)
ax.spines['right'].set_linewidth(1.5)
ax.spines['bottom'].set_linewidth(1.5)
ax.spines['left'].set_linewidth(1.5)

plt.tight_layout()

# Save plot to ball lens folder
save_path = r'C:\Users\Sumedh\Downloads\ball lens\efficiency_comparison_0to60mm_1mm_step.png'
plt.savefig(save_path, dpi=300, bbox_inches='tight')
plt.show()

# Print summary table
print(f"\n{'='*70}")
print("SUMMARY: OPTIMAL WORKING DISTANCE FOR EACH BALL LENS RADIUS")
print(f"{'='*70}")
print(f"{'Radius [mm]':<15} {'Diameter [mm]':<15} {'EPD [mm]':<15} {'Opt Dist [mm]':<20} {'Max Eff [%]':<15}")
print(f"{'-'*80}")

for radius in radius_values:
    eff = results[radius]
    if np.any(~np.isnan(eff)):
        best_idx = np.nanargmax(eff)
        best_dist = distance_values[best_idx]
        best_eff = eff[best_idx]
        print(f"{radius:<15.1f} {2*radius:<15.1f} {radius:<15.1f} {best_dist:<20.1f} {best_eff:<15.2f}")

print(f"{'='*80}")
print(f"\nPlot saved to: {save_path}")
print(f"{'='*80}")
