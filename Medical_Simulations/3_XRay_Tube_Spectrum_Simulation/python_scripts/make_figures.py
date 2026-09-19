"""
make_figures.py
================

Generate all comparison figures for the X-ray tube practice report.

For each of the six PENELOPE simulations (penmain example 5 and its variants),
loads spc-impdet-02.dat, generates the matching SpekPy analytical spectrum,
and saves a clean PNG ready to be inserted in the LaTeX report.

The script must be run from the user's local Python environment (where
spekpy is installed). It writes its output into ./figures/ next to itself.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import spekpy as sp


# -------------------------------------------------------------------------
# Paths
# -------------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.abspath(os.path.join(HERE, ".."))
PEN_BASE = os.path.join(BASE, "Simulation_Penelope", "My_penelope", "fsource")
FIG_DIR = os.path.abspath(os.path.join(HERE, "..", "Latex", "figures"))
os.makedirs(FIG_DIR, exist_ok=True)


# -------------------------------------------------------------------------
# Case definitions
# -------------------------------------------------------------------------
CASES = {
    "W_150_45_1mm":  {"folder": "5-x-ray-tube",            "kvp": 150, "th": 45, "targ": "W",  "filt": 1.0},
    "W_28_45_1mm":   {"folder": "5-x-ray-tube_28kev",      "kvp":  28, "th": 45, "targ": "W",  "filt": 1.0},
    "Mo_28_45_1mm":  {"folder": "5-x-ray-tube_Mo_28",      "kvp":  28, "th": 45, "targ": "Mo", "filt": 1.0},
    "W_150_20_2mm":  {"folder": "5-x-ray-tube_150_20_2mm", "kvp": 150, "th": 20, "targ": "W",  "filt": 2.0},
    "W_28_20_2mm":   {"folder": "5-x-ray-tube_28_20_2mm",  "kvp":  28, "th": 20, "targ": "W",  "filt": 2.0},
    "Mo_28_20_2mm":  {"folder": "5-x-ray-tube_Mo_28_20_2mm","kvp": 28, "th": 20, "targ": "Mo", "filt": 2.0},
}


# -------------------------------------------------------------------------
# Loaders
# -------------------------------------------------------------------------
def load_penelope(case_key):
    """Load PENELOPE photon spectrum from spc-impdet-02.dat.

    Columns 1, 6, 7 (0-indexed: 0, 5, 6) hold energy [eV], photon
    probability density and 3-sigma uncertainty respectively. Empty
    bins are filled with the sentinel 1e-35 and are filtered out.

    Returns
    -------
    E_keV : ndarray   bin midpoints (keV)
    flux  : ndarray   probability density normalised to unit area (1/keV)
    err   : ndarray   3-sigma uncertainty, normalised the same way
    """
    folder = CASES[case_key]["folder"]
    path = os.path.join(PEN_BASE, folder, "spc-impdet-02.dat")
    raw = np.loadtxt(path, comments="#")
    E = raw[:, 0] / 1e3
    flux = raw[:, 5]
    err = raw[:, 6]
    mask = flux > 1e-34
    E, flux, err = E[mask], flux[mask], err[mask]
    area = np.trapezoid(flux, E)
    return E, flux / area, err / area


def load_spekpy(case_key):
    """SpekPy analytical photon fluence, area-normalised."""
    c = CASES[case_key]
    s = sp.Spek(kvp=c["kvp"], targ=c["targ"], th=c["th"])
    s.filter("Al", c["filt"])
    E, flux = s.get_spectrum(edges=False, flu=True)
    E = np.asarray(E)
    flux = np.asarray(flux)
    area = np.trapezoid(flux, E)
    return E, flux / area


# -------------------------------------------------------------------------
# Plot style
# -------------------------------------------------------------------------
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 11,
    "axes.labelsize": 11,
    "legend.fontsize": 9,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "savefig.dpi": 200,
    "savefig.bbox": "tight",
})

C_PEN  = "#c0392b"   # PENELOPE (red)
C_SPK  = "black"     # SpekPy
C_BLUE = "#1f3a93"


# -------------------------------------------------------------------------
# Individual figures
# -------------------------------------------------------------------------
def fig_baseline():
    """Original spectrum: W 150 keV 45 deg 1 mm Al, PENELOPE only."""
    E, f, e = load_penelope("W_150_45_1mm")
    fig, ax = plt.subplots(figsize=(6.0, 3.8))
    ax.step(E, f, where="mid", color=C_BLUE, lw=1.2, label="PENELOPE")
    ax.fill_between(E, np.maximum(0, f - e), f + e, step="mid",
                    color=C_BLUE, alpha=0.20, lw=0,
                    label=r"PENELOPE $3\sigma$")
    ax.set_xlabel("Photon energy (keV)")
    ax.set_ylabel("Probability density (1/keV)")
    ax.set_xlim(0, 160)
    ax.set_ylim(bottom=0)
    ax.legend(frameon=False)
    ax.grid(True, ls=":", alpha=0.5)
    fig.savefig(os.path.join(FIG_DIR, "fig01_baseline.png"))
    plt.close(fig)


def fig_compare(case_key, fname, xlim):
    """PENELOPE vs SpekPy for a single configuration."""
    E_p, f_p, e_p = load_penelope(case_key)
    E_s, f_s = load_spekpy(case_key)
    fig, ax = plt.subplots(figsize=(6.0, 3.8))
    ax.plot(E_s, f_s, color=C_SPK, lw=1.4, label="SpekPy")
    ax.step(E_p, f_p, where="mid", color=C_PEN, lw=1.0, label="PENELOPE")
    ax.fill_between(E_p, np.maximum(0, f_p - e_p), f_p + e_p, step="mid",
                    color=C_PEN, alpha=0.20, lw=0,
                    label=r"PENELOPE $3\sigma$")
    ax.set_xlabel("Photon energy (keV)")
    ax.set_ylabel("Probability density (1/keV)")
    ax.set_xlim(*xlim)
    ax.set_ylim(bottom=0)
    ax.legend(frameon=False, loc="best")
    ax.grid(True, ls=":", alpha=0.5)
    fig.savefig(os.path.join(FIG_DIR, fname))
    plt.close(fig)


def fig_compare_energy():
    """Effect of beam energy at fixed geometry (45 deg, 1 mm Al)."""
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.8))
    plots = [
        (axes[0], "W_150_45_1mm", (0, 160), C_BLUE, "W, 150 keV"),
        (axes[1], "W_28_45_1mm",  (0,  32), C_PEN,  "W, 28 keV"),
    ]
    for ax, key, lim, color, label in plots:
        E, f, e = load_penelope(key)
        ax.step(E, f, where="mid", color=color, lw=1.2, label=label)
        ax.fill_between(E, np.maximum(0, f - e), f + e, step="mid",
                        color=color, alpha=0.2, lw=0)
        ax.set_xlabel("Photon energy (keV)")
        ax.set_ylabel("Probability density (1/keV)")
        ax.set_xlim(*lim)
        ax.set_ylim(bottom=0)
        ax.legend(frameon=False)
        ax.grid(True, ls=":", alpha=0.5)
    fig.savefig(os.path.join(FIG_DIR, "fig08_compare_energy.png"))
    plt.close(fig)


def fig_compare_anode():
    """Effect of anode material at fixed energy and geometry."""
    fig, ax = plt.subplots(figsize=(6.0, 3.8))
    for key, color, label in [
        ("W_28_45_1mm",  C_BLUE, "W, 28 keV"),
        ("Mo_28_45_1mm", C_PEN,  "Mo, 28 keV"),
    ]:
        E, f, e = load_penelope(key)
        ax.step(E, f, where="mid", color=color, lw=1.2, label=label)
        ax.fill_between(E, np.maximum(0, f - e), f + e, step="mid",
                        color=color, alpha=0.2, lw=0)
    ax.set_xlabel("Photon energy (keV)")
    ax.set_ylabel("Probability density (1/keV)")
    ax.set_xlim(0, 32)
    ax.set_ylim(bottom=0)
    ax.legend(frameon=False)
    ax.grid(True, ls=":", alpha=0.5)
    fig.savefig(os.path.join(FIG_DIR, "fig09_compare_anode.png"))
    plt.close(fig)


def fig_compare_geometry():
    """Effect of anode angle and filtration: 45°/1 mm vs 20°/2 mm.

    Vertical 3x1 layout, one row per case, fits comfortably in a single
    LaTeX figure on a portrait A4 page.
    """
    pairs = [
        ("W_150_45_1mm",  "W_150_20_2mm",  "W, 150 keV", (0, 160)),
        ("W_28_45_1mm",   "W_28_20_2mm",   "W, 28 keV",  (0,  32)),
        ("Mo_28_45_1mm",  "Mo_28_20_2mm",  "Mo, 28 keV", (0,  32)),
    ]
    fig, axes = plt.subplots(3, 1, figsize=(6.4, 9.0), constrained_layout=True)
    for ax, (k1, k2, title, lim) in zip(axes, pairs):
        E1, f1, _ = load_penelope(k1)
        E2, f2, _ = load_penelope(k2)
        ax.step(E1, f1, where="mid", color=C_BLUE, lw=1.2, label="45°, 1 mm Al")
        ax.step(E2, f2, where="mid", color=C_PEN,  lw=1.2, label="20°, 2 mm Al")
        ax.set_xlabel("Photon energy (keV)")
        ax.set_ylabel("Probability density (1/keV)")
        ax.set_xlim(*lim)
        ax.set_ylim(bottom=0)
        ax.text(0.97, 0.95, title, transform=ax.transAxes,
                ha="right", va="top",
                bbox=dict(facecolor="white", edgecolor="none",
                          alpha=0.85, boxstyle="round,pad=0.2"))
        ax.legend(frameon=False, loc="upper right",
                  bbox_to_anchor=(1.0, 0.85))
        ax.grid(True, ls=":", alpha=0.5)
    fig.savefig(os.path.join(FIG_DIR, "fig10_compare_geometry.png"))
    plt.close(fig)


# -------------------------------------------------------------------------
# Driver
# -------------------------------------------------------------------------
def main():
    print(f"Saving figures into: {FIG_DIR}")
    fig_baseline()
    fig_compare("W_150_45_1mm",  "fig02_W_150_45_1mm.png",  (0, 160))
    fig_compare("W_28_45_1mm",   "fig03_W_28_45_1mm.png",   (0,  32))
    fig_compare("Mo_28_45_1mm",  "fig04_Mo_28_45_1mm.png",  (0,  32))
    fig_compare("W_150_20_2mm",  "fig05_W_150_20_2mm.png",  (0, 160))
    fig_compare("W_28_20_2mm",   "fig06_W_28_20_2mm.png",   (0,  32))
    fig_compare("Mo_28_20_2mm",  "fig07_Mo_28_20_2mm.png",  (0,  32))
    fig_compare_energy()
    fig_compare_anode()
    fig_compare_geometry()
    print("All figures generated.")


if __name__ == "__main__":
    main()
