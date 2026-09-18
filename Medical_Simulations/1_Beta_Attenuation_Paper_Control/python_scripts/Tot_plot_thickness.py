import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from matplotlib.ticker import ScalarFormatter, NullFormatter

# --- 1. Caricamento Dati ---
file_path = 'Results_kr85.csv'
n_electrons = "10^7" 
rho = 1.2

try:
    data = pd.read_csv(file_path)
    if 'Incertezza' in data.columns:
        data = data.rename(columns={'Incertezza': 'Uncertainty'})
except FileNotFoundError:
    print(f"Errore: {file_path} non trovato")
    exit()

# Filtriamo i dati per partire da 0.1 mm (escludiamo lo 0)
data_filtered = data[data['Thickness_mm'] >= 0.1]

x_mm = data_filtered['Thickness_mm'].values
x_cm = x_mm / 10.0 
y = data_filtered['Transmitted_Fraction'].values
y_err = data_filtered['Uncertainty'].values

# --- 2. Interpolazione Lineare sui Logaritmi (ln(I) = m*x + q) ---
ln_y = np.log(y)

def linear_func(x, m, q):
    return m * x + q

popt, pcov = curve_fit(linear_func, x_cm, ln_y, sigma=y_err/y) # Ponderato per l'errore logaritmico
m_fit, q_fit = popt
mu_cm = -m_fit
mu_error = np.sqrt(pcov[0,0])

# Parametri per la curva esponenziale nel plot lineare
I0_fit = np.exp(q_fit)

# Calcolo R^2
residuals = ln_y - linear_func(x_cm, m_fit, q_fit)
r_squared = 1 - (np.sum(residuals**2) / np.sum((ln_y - np.mean(ln_y))**2))

# --- 3. Plotting ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle(fr'$^{{85}}$Kr Beta Attenuation Analysis in Cellulose ($\rho={rho}$ g/cm$^3$, $N = {n_electrons}$ $e^-$)', fontsize=14)

# Dominio per le linee di fit (parte da 0.1 mm)
x_limit = 1.55
x_smooth_mm = np.linspace(0.1, x_limit, 100)
y_smooth = I0_fit * np.exp(-mu_cm * (x_smooth_mm / 10.0))

# --- Grafico Lineare ---
ax1.errorbar(x_mm, y, yerr=y_err, fmt='o', color='red', label='Simulation Data', 
             markersize=6, capsize=4, elinewidth=1.5, zorder=3)
ax1.plot(x_smooth_mm, y_smooth, '--', color='navy', linewidth=2, 
         label=fr'Fit: $I(x) = I_0 \cdot e^{{-{mu_cm:.2f} \cdot x}}$')

ax1.set_title('Linear Scale', fontsize=12)
ax1.set_xlabel('Thickness (mm)')
ax1.set_ylabel('Transmitted Fraction (I/I0)')
ax1.set_xlim(0.1, x_limit) # L'asse parte da 0.1 mm
ax1.set_ylim(0, 0.25) 
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.legend(loc='upper right')

# --- Grafico Logaritmico ---
ax2.errorbar(x_mm, y, yerr=y_err, fmt='o', color='red', label='Simulation Data', 
             markersize=6, capsize=4, elinewidth=1.5, zorder=3)

# Legenda con m e q
fit_label_log = (fr'Linear Fit: $\ln(I) = m \cdot x + q$' + '\n' +
                 fr'$m = {m_fit:.2f}$' + '\n' +
                 fr'$q = {q_fit:.2f}$' 
                 #+ '\n' + fr'$R^2 = {r_squared:.5f}$'
                 )

ax2.plot(x_smooth_mm, y_smooth, '--', color='navy', linewidth=2, label=fit_label_log)

ax2.set_yscale('log')
ax2.set_title('Logarithmic Scale (Semi-log)', fontsize=12)
ax2.set_xlabel('Thickness (mm)')
ax2.set_ylabel('Transmitted Fraction (Log)')
ax2.set_xlim(0.1, x_limit) # L'asse parte da 0.1 mm
ax2.set_ylim(0.001, 0.4) 

ax2.yaxis.set_major_formatter(ScalarFormatter())
ax2.yaxis.set_minor_formatter(NullFormatter()) 
ax2.grid(True, which='major', linestyle='-', linewidth=1, alpha=0.7)
ax2.grid(True, which='minor', linestyle=':', linewidth=0.5, alpha=0.5)
ax2.legend(loc='upper right', fontsize=9)

# --- Box Risultati Finale ---
textstr = (fr'Interpolation Results:' + '\n' +
           fr'$\mu = -m = {mu_cm:.4f} \pm {mu_error:.4f}$ cm$^{{-1}}$' + '\n' +
           fr'Mass Attenuation $\mu/\rho = {mu_cm/rho:.3f}$ cm$^2$/g')

fig.text(0.5, 0.1, textstr, ha='center', va='center', fontsize=11,
         bbox=dict(facecolor='white', edgecolor='navy', boxstyle='round,pad=1', alpha=0.8))

output_filename = 'Kr_85_Fraction_vs_Thickness_Comparison.png'
plt.savefig(output_filename, dpi=300)
print(f"Comparison plot saved as {output_filename}")

plt.tight_layout(rect=[0, 0.18, 1, 0.92])
plt.show()