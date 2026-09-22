# Monte Carlo Radiation Transport Simulations

Six computational physics studies developed at the **University of Granada**, applying Monte
Carlo radiation transport to nuclear engineering, medical physics and industrial quality
control — one of them validated against laboratory measurements. Simulations run with
**MCNP6.2** and **PENELOPE-2018**; analysis in Python and MATLAB.

Each folder has its own README with the setup, the results and the full report.

## [Nuclear — MCNP simulation of a PWR fuel assembly](Nuclear_Simulations/)

Criticality study of an idealised 3×3 UO₂ lattice with reflective boundary conditions,
benchmarked against the Westinghouse 17×17 commercial design. Parametric studies of lattice
pitch, moderator density and fuel enrichment, plus the neutron spectrum behind the moderation
curve.

> k∞ = 1.41856 ± 0.00031 at the reference PWR configuration · predicted optimal pitch
> p\* = 1.33 cm, within ~5% of the commercial design · Δk∞/k∞ = −2.1% at PWR-hot moderator
> density, reproducing the reactor's self-stabilising feedback

## [Detector characterization — experiment against two Monte Carlo codes](Detector_Characterization/)

The one experimental study here. A Canberra 802 3"×3" NaI(Tl) scintillation detector
characterised with calibrated ¹³⁷Cs, ⁶⁰Co, ²²Na and ¹⁵²Eu sources, then reproduced in
PENELOPE and cross-checked with MCNP6.

> Energy resolution 3.4% at 662 keV against 7.5% nominal · PENELOPE reproduces the measured
> photopeak efficiencies within 2% · MCNP6 and PENELOPE agree within 5%

## [Medical and industrial — four PENELOPE studies](Medical_Simulations/)

**[1 — Beta attenuation for paper grammage control](Medical_Simulations/1_Beta_Attenuation_Paper_Control/)**
Beta transmission through cellulose for on-line thickness sensors, with gamma and lead
counter-tests marking the limits of the technique.
> µ/ρ from 25.0 to 40.5 cm²/g across ⁸⁵Kr, ²⁰⁴Tl and ⁹⁰Sr · gamma transmission flat at 0.53

**[2 — PIXE material characterization](Medical_Simulations/2_PIXE_Material_Characterization/)**
Proton-induced X-ray emission on pure elements and industrial alloys, validated against EADL
transition energies.
> Mn resolved at 0.43% mass fraction in Eurofer97 · Ag/Pd Kα ratio 3.4 against a nominal 3.4

**[3 — X-ray tube spectrum simulation](Medical_Simulations/3_XRay_Tube_Spectrum_Simulation/)**
Six tube configurations varying beam energy, anode material and geometry, cross-validated
against the SpekPy v2 toolkit.
> Mo K-lines at 17.5 and 19.6 keV appear at 28 keV where the W lines cannot

**[4 — Mammographic dosimetry and PET](Medical_Simulations/4_Mammography_and_PET_Simulations/)**
Dose in a breast phantom across three clinical spectra and three tissue compositions, carried
through to an absolute dose.
> 2.43 mGy average breast dose at 100 mAs · breast-to-skin ratio improves from 3.58 to 4.43 as
> the beam hardens

## Repository structure

```text
MonteCarlo-Radiation-Simulations/
├── Nuclear_Simulations/          # MCNP6 — neutron transport, criticality, lattice physics
├── Detector_Characterization/    # PENELOPE + MCNP6 against laboratory gamma spectrometry
└── Medical_Simulations/          # PENELOPE — photon, electron and positron transport
```

## Methods

| | |
|---|---|
| **Nuclear** | MCNP6.2 with ENDF/B-VII.1, `kcode` criticality calculations, F4 flux tallies, reflective boundary conditions |
| **Detector** | PENELOPE `penhmain` with a detailed detector model, MCNP6 with Gaussian Energy Broadening, measurements on an Ortec Easy-MCA-2k |
| **Medical** | PENELOPE-2018 (`penmain`, `penh`), 3D dose grids, impact detectors, spectra from SpekPy v2 and the LNHB database |
| **Analysis** | Python and MATLAB — output parsing, tally extraction, fitting and plotting |

Every study includes its full written report as a PDF in the corresponding folder. The
detector characterization was carried out with Pablo Flores Pérez, Davide Goretti and Rafael
Guerrero Alonso; the other five are individual work.

---

*Universidad de Granada, academic year 2025/2026.*
