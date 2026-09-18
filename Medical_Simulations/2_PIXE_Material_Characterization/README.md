# PIXE Simulations for Material Characterization

This project models Proton-Induced X-ray Emission (PIXE) using Monte Carlo simulations (PENELOPE/penh) to identify elemental compositions in various materials. 

The simulated targets progress logically from pure elements to complex industrial alloys:
* **Pure Silver (Ag):** Including an energy-dependence study of the emission yield.
* **Pure Copper (Cu):** Baseline K-series emission analysis.
* **Bronze Alloy (Cu-Sn):** Demonstrating matrix (Cu) and alloying element (Sn) peak separation.
* **Eurofer97 Steel:** Resolving primary matrix components (Fe, Cr) and trace elements (Mn).
* **White Gold (Au-Ag-Pd):** Analyzing L-series and K-series emissions, comparing **14-karat** and **18-karat** alloy configurations.

## 📁 Repository Structure
* **`Aplicaciones_Médicas_e_Industriales_de_las_radiaciones_paper__X_ray_.pdf`**: The complete physical analysis, methodology, and comparison with EADL theoretical transition energies.
* **`input_decks/`**: Contains the PENELOPE/penh input configurations (`.in`), the target geometry (`disc.geo`), and the simulated material definitions (`.mat`).
* **`results_and_plots/`**: Contains the final X-ray emission spectra generated from the simulations.
