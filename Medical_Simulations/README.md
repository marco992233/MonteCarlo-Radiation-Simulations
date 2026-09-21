# Medical and Industrial Applications of Radiation

Four PENELOPE Monte Carlo studies, from industrial quality control to mammographic dosimetry.
Each folder has its own README with the setup, the results and the full report.

## [1 — Beta Attenuation for Paper Grammage Control](1_Beta_Attenuation_Paper_Control/)

Beta transmission through cellulose for the radiation sensors used in on-line paper thickness
control. Attenuation coefficients for ⁸⁵Kr, ²⁰⁴Tl and ⁹⁰Sr, a gamma counter-test showing why
photons make the sensor blind, and a lead counter-test establishing where beta sensors stop
working.

> µ/ρ from 25.0 to 40.5 cm²/g across the three sources · gamma transmission flat at 0.53 ·
> beta fully absorbed by 0.15 mm of lead

## [2 — PIXE Material Characterization](2_PIXE_Material_Characterization/)

Proton-Induced X-ray Emission on pure elements and industrial alloys, validated against EADL
transition energies: silver, copper, bronze, Eurofer97 fusion steel and white gold.

> Mn resolved at 0.43% mass fraction in Eurofer97 · Ag/Pd Kα intensity ratio 3.4 against a
> nominal mass ratio of 3.4

## [3 — X-ray Tube Spectrum Simulation](3_XRay_Tube_Spectrum_Simulation/)

Six tube configurations varying beam energy, anode material and geometry, each cross-validated
against the SpekPy v2 analytical toolkit.

> Mo K-lines at 17.5 and 19.6 keV appear at 28 keV where the W lines cannot · beam hardening
> from 45°/1 mm to 20°/2 mm, strongly energy-dependent

## [4 — Mammographic Dosimetry and PET](4_Mammography_and_PET_Simulations/)

Dose in a breast phantom across three clinical spectra and three tissue compositions, carried
through to an absolute dose in mGy.

> 2.43 mGy average breast dose at 100 mAs (Rh/Rh, 30 kVp) · breast-to-skin ratio improves from
> 3.58 to 4.43 as the beam hardens · +27% entrance dose from adipose to fully glandular tissue

---

All simulations use **PENELOPE-2018** (`penmain`, `penh`). Analysis and plotting in Python;
spectra generated or cross-checked with **SpekPy v2**.

*Aplicaciones Médicas e Industriales de las Radiaciones, Universidad de Granada, 2025/2026.*
