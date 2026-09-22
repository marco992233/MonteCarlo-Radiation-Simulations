# NaI(Tl) Detector Characterization by Gamma Spectrometry and Monte Carlo Simulation

Full characterization of a **Canberra Model 802 3"×3" NaI(Tl)** scintillation detector
(2007P base), combining laboratory measurements with calibrated sources against detailed
**PENELOPE** simulations, cross-validated with **MCNP6**.

*Pablo Flores Pérez, Davide Goretti, Marco Fumagalli, Rafael Guerrero Alonso.
Máster en Física: Radiaciones, Nanotecnología, Partículas y Astrofísica — Universidad de
Granada, April 2026. Course: Detección de Radiación y Dosimetría.*

This is the only experimental work in this repository: everything else is simulation alone.

## Results

| Quantity | Value |
|---|---|
| Channel-energy calibration, 20–1332 keV | linear, better than **2%** |
| Energy resolution law | R(E) = A/√E + B, A = 50.7 ± 2.8 keV<sup>½</sup>%, B = 0.75 ± 0.15% |
| Resolution at 662 keV | **3.4%** — against 7.5% nominal from the manufacturer |
| Absolute photopeak efficiency | 1.24% at 122 keV (d = 1 cm) down to 0.040% at 1332 keV (d = 3 cm) |
| PENELOPE vs experiment | mean deviation **< 2%** across all sources and distances |
| MCNP6 vs PENELOPE | agreement **< 5%** |

Intrinsic efficiency stays constant with distance — 44.2 / 43.7 / 44.0 % at 121.8 keV for
d = 1, 2, 3 cm — confirming that the solid-angle correction is physically sound.

### The Eu-152 discrepancy

The comparison initially showed a large gap for ¹⁵²Eu: 24.6% measured against ~7% simulated.
It is not a failure of either code. The experimental figure was the **total** spectrum
efficiency while the simulated one was the **photopeak** efficiency — two different physical
quantities. The lesson, stated in the report, is that experimental spectra must be processed
to isolate the net photopeak area *before* any comparison against simulation is meaningful.

## Contents

```
Detector_Characterization/
├── NaI_Detector_Characterization_report.pdf   # full report (Spanish)
├── experimental_data/     # measured spectra, calibration points, efficiency results
├── simulations/           # PENELOPE inputs and results, one folder per source and distance
├── mcnp/                  # MCNP6 spectra and efficiencies
└── scripts/               # MATLAB analysis
```

### Experimental spectra

Acquired 17–18 March 2026 with an Ortec Easy-MCA-2k (1024 channels), Maestro 7.01.
**The trailing number is the source-detector distance in cm.**

| File | Source | Distance |
|---|---|---|
| `cesio1/2/3.Spe` | ¹³⁷Cs | 1, 2, 3 cm |
| `cobalto1/2/3.Spe` | ⁶⁰Co | 1, 2, 3 cm |
| `sodio1/2/3.Spe` | ²²Na | 1, 2, 3 cm |
| `europio1/2/3.Spe` | ¹⁵²Eu | 1, 2, 3 cm |
| `combicsco.Spe` | combined ¹³⁷Cs + ⁶⁰Co source | — |
| `fonfodpm.Spe` | background, 82 868 s live time (23 h) | — |
| `secio1-95.Spe` | additional measurement, not used in the report | — |

`calibration_points.txt` holds the seven channel-energy pairs used for the linear calibration.

### PENELOPE simulations

Twelve runs, one per source and distance, each containing the complete input needed to
reproduce it:

- `fuente.in` — source definition and simulation parameters
- `detector.geo` — detector geometry: NaI crystal, aluminium window, reflector, housing and lead shielding
- `material.dat` — material assignment as read back by the code
- `penhmain-res.dat` — run summary, including CPU time and number of showers
- `spc-NaI-enddet.dat` — the simulated pulse-height spectrum

The energy window is 0–1400 keV with 1000 bins, wide enough to contain the ⁶⁰Co lines at
1173 and 1332 keV.

**The PENELOPE material files (`.mat`) are not included.** They are generated from the
PENELOPE database, which is distributed under licence by the OECD/NEA Data Bank and cannot
be redistributed here. Regenerate them with `material.exe` from your own PENELOPE
installation; the compositions are listed in the report.

### MCNP6

The MCNP6 results are included, but **the input deck was not preserved**. The parameters it
was run with are documented in `mcnp/eficiencias_mcnp.txt`:

- 10⁷ histories for the realistic case (with Gaussian Energy Broadening), 10⁸ for the ideal case
- GEB window of ±2 FWHM, with FWHM(MeV) = 0.0565·√E
- Ideal window of ±5 keV around the photopeak
- Analytical Ω/4π = 0.3486563 for an effective distance of 1.21 cm

Together with `detector.geo`, this is enough to rebuild an equivalent deck, but it is a
reconstruction rather than the original.

## Reproducing

The PENELOPE runs need `penhmain` from a PENELOPE-2018 installation and the regenerated
material files:

```bash
cd simulations/Cs137_d1cm
penhmain < fuente.in
```

The MATLAB scripts in `scripts/` process both the measured and the simulated spectra:
`Lineal.m` fits the channel-energy calibration, `spectrum2.m` analyses individual spectra,
and `RepresentacionConjunta.m` produces the experiment-PENELOPE-MCNP comparison.

## Report

[`NaI_Detector_Characterization_report.pdf`](NaI_Detector_Characterization_report.pdf) —
33 pages, in Spanish: theory, method, full results and discussion.
