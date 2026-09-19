# Mammography Dosimetry and PET Simulations

This folder contains Monte Carlo simulations (PENELOPE/penmain) developed to evaluate X-ray spectra and dosimetric parameters in mammography, alongside preliminary simulations for Positron Emission Tomography (PET).

## 🔬 Simulations Overview
*   **Mammography Dosimetry:** Analyzes standard target/filter combinations (Mo/Mo at 25 kVp, Rh/Rh at 30 kVp) and evaluates dose deposition across different phantom thicknesses and breast tissue glandular fractions (0%, 50%, 100%).
*   **PET Simulation:** Models positron transport and annihilation using specific materials (Bone, Lead, Water, Air).

## 📁 Folder Structure
*   **`input_decks/`**: Contains the PENELOPE source files (`.in`, `.inp`), geometric definitions (`.geo`), and material cross-sections (`.mat`) for both Mammography and PET simulations.
*   **`python_scripts/`**: Contains the Jupyter Notebook used for data extraction, attenuation coefficient analysis, and spectral plotting.
*   **`results_and_plots/`**: Contains the final rendered spectra and attenuation coefficient plots for different glandular tissue fractions.
