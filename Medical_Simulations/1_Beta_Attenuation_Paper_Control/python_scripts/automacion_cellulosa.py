import subprocess
import re
import csv
import os
import time

input_template = "kr85_spectrum.in"
output_file = "Results_kr85.csv"
#thicknesses_mm = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10]
thicknesses_mm = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5]

def modify_thickness(new_thickness_cm):
    with open(input_template, 'r') as f:
        lines = f.readlines()
    with open(input_template, 'w') as f:
        for line in lines:
            if line.strip().startswith("LAYER"):
                # Formatted to maintain the specific PENELOPE input structure
                f.write(f"LAYER  0.0  {new_thickness_cm:<10}                                   [Z_lower and Z_higher]\n")
            else:
                f.write(line)

def extract_data():
    filename = "pencyl-res.dat"
    if not os.path.exists(filename):
        return None, None, None
    
    with open(filename, 'r') as f:
        content = f.read()
        
        # 1. Extract Transmitted Fraction (I/I0)
        # Matches "Upbound fraction .... X.XXXXE+XX +- X.XXXXE+XX"
        fraction_match = re.search(r"Upbound fraction \.+\s+([0-9.E+-]+)\s+[-\+]+\s+([0-9.E+-]+)", content)
        
        # 2. Extract Absolute Number of transmitted particles
        # Matches "Upbound primary particles .............  X.XXXXXXE+XX"
        number_match = re.search(r"Upbound primary particles \.+\s+([0-9.E+-]+)", content)
        
        fraction = fraction_match.group(1) if fraction_match else None
        error = fraction_match.group(2) if fraction_match else None
        number = number_match.group(1) if number_match else None
        
        return fraction, error, number

# Terminal Header
print(f"{'Thickness (mm)':<15} | {'Fraction (I)':<18} | {'N. Electrons':<15} | {'Error':<10}")
print("-" * 70)

results = []

for t_mm in thicknesses_mm:
    t_cm = t_mm / 10.0
    # Clean up old result files to ensure fresh data
    if os.path.exists("pencyl-res.dat"): 
        os.remove("pencyl-res.dat")
    
    modify_thickness(t_cm)
    print(f"Simulating {t_mm} mm...", end="\r")
    
    # Run PENELOPE simulation
    subprocess.run(f"./pencyl < {input_template}", shell=True, capture_output=True)
    
    transm, err, num_e = extract_data()
    
    if transm:
        print(f"{t_mm:<15} | {transm:<18} | {num_e:<15} | {err:<10}")
        results.append([t_mm, transm, num_e, err])
    else:
        print(f"{t_mm:<15} | ERROR: Check pencyl-res.dat")

# Save to CSV with updated headers
with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Thickness_mm", "Transmitted_Fraction", "Electron_Count", "Uncertainty"])
    writer.writerows(results)

print(f"\nDone! Data saved in {output_file}")