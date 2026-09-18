import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# --- 1. Data Loading & Preparation ---
file_path = 'Results_kr85.csv'
try:
    data = pd.read_csv(file_path)
except FileNotFoundError:
    print(f"Error: file {file_path} not found")
    exit()

# Configuration
sheet_thickness_mm = 0.01

# Calculate X values as Number of Papers
x_mm = data['Thickness_mm'].values
x_papers = x_mm / sheet_thickness_mm
y = data['Transmitted_Fraction'].values
y_err = data['Uncertainty'].values

# --- 2. Exponential Fit ---
def attenuation_law(n, I0, k):
    return I0 * np.exp(-k * n)

# Fit against number of papers
popt, pcov = curve_fit(attenuation_law, x_papers, y, p0=[1.0, 0.1])
I0_fit, k_fit = popt
k_error = np.sqrt(pcov[1,1])

# --- 3. Plotting Side-by-Side ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
fig.suptitle(r'Kr-85 Beta Attenuation vs. Number of Cellulose Sheets ($d_{sheet}=0.1$ mm)', fontsize=16)

# Smooth curve for fitting lines
x_smooth_papers = np.linspace(min(x_papers), max(x_papers), 100)
y_smooth = attenuation_law(x_smooth_papers, *popt)

# --- LEFT PLOT: Linear Scale ---
ax1.errorbar(x_papers, y, yerr=y_err, fmt='o', color='red', label='Simulation Data', capsize=5)
ax1.plot(x_smooth_papers, y_smooth, '--', color='blue', 
         label=f'Exponential Fit\n($k$ = {k_fit:.4f} papers$^{{-1}}$)')
ax1.set_title('Linear Scale')
ax1.set_xlabel('Number of Papers (n)')
ax1.set_ylabel('Transmitted Fraction (I/I0)')
ax1.set_xticks(np.arange(min(x_papers), max(x_papers) + 1, 1.0))
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.legend()

# --- RIGHT PLOT: Logarithmic Scale ---
ax2.errorbar(x_papers, y, yerr=y_err, fmt='o', color='red', label='Simulation Data', capsize=5)
ax2.plot(x_smooth_papers, y_smooth, '--', color='blue', 
         label=f'Fit Line ($k$ = {k_fit:.4f} papers$^{{-1}}$)')
ax2.set_yscale('log')
ax2.set_title('Logarithmic Scale')
ax2.set_xlabel('Number of Papers (n)')
ax2.set_ylabel('Transmitted Fraction (Log Scale)')
ax2.set_xticks(np.arange(min(x_papers), max(x_papers) + 1, 1.0))
ax2.grid(True, which="both", linestyle='--', alpha=0.5)
ax2.legend()

# --- Results Text Box ---
mu_cm = k_fit / (sheet_thickness_mm / 10.0)
textstr = (f'Fit Results:\n'
           f'k = {k_fit:.4f} $\pm$ {k_error:.4f} papers$^{{-1}}$\n'
           f'Equivalent $\mu$ = {mu_cm:.2f} cm$^{{-1}}$')

fig.text(0.5, 0.02, textstr, ha='center', fontsize=12, bbox=dict(facecolor='white', alpha=0.8))

# Adjust layout
plt.tight_layout(rect=[0, 0.08, 1, 0.95])

# Save and Show
output_filename = 'Fraction_vs_Papers_Comparison.png'
plt.savefig(output_filename, dpi=300)
print(f"Comparison plot saved as {output_filename}")
print(f"Coefficient k: {k_fit:.4f} per paper")

plt.show()