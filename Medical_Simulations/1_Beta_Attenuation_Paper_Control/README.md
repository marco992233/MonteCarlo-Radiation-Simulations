# Beta Attenuation for Industrial Paper Grammage Control

This folder contains the Monte Carlo simulations (PENELOPE) and data analysis scripts used to evaluate beta radiation ($^{85}Kr, ^{90}Sr, ^{204}$Tl) for industrial paper thickness control.

## 📄 Full Report
For the complete theoretical background, physics discussion, and industrial engineering conclusions, please read the provided PDF: **`Aplicaciones_Médicas_e_Industriales_de_las_radiaciones_paper.pdf`**.

## 📁 Folder Structure
* **`input_decks/`**: Contains the PENELOPE source files (`.in`) for the beta emitters and the gamma-ray counter-tests, along with the `Cellulose.mat` material definition.
* **`python_scripts/`**: Contains the Python automation scripts used to process the simulation outputs and perform the semi-logarithmic data fitting.
* **`results_and_plots/`**: Contains the aggregated `.csv` results and the final attenuation curves (`.png`).

## 🚀 How to Run the Analysis
To reproduce the attenuation plots from the simulation data, run the Python scripts from your terminal:

```bash
python python_scripts/Tot_plot_thickness.py
