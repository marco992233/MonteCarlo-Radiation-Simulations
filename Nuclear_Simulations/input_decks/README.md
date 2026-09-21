# MCNP6 input decks

Every deck in this folder, the configuration it runs and the result it produced. All runs use
`kcode 10000 1.0 30 300` (3×10⁶ active histories) with ENDF/B-VII.1 cross sections at room
temperature, unless noted otherwise.

| Deck | Configuration | Result |
|---|---|---|
| `Fision.txt` | original course deck — fixed source, two metallic-uranium rods in water | R_f = (6.40 ± 0.25)×10⁻³ fissions per source neutron (validation run) |
| `assembly_p090.txt` | pitch 0.90 cm, 3% enrichment | k∞ = 1.19250 ± 0.00040 |
| `assembly_p110.txt` | pitch 1.10 cm, 3% enrichment | k∞ = 1.37507 ± 0.00032 |
| `assembly_p126.txt` | **reference** — pitch 1.26 cm, 3% enrichment, ρ_H₂O = 1.00 g/cm³ | k∞ = 1.41856 ± 0.00031 |
| `assembly_p150.txt` | pitch 1.50 cm, 3% enrichment | k∞ = 1.41092 ± 0.00026 |
| `assembly_p200.txt` | pitch 2.00 cm, 3% enrichment | k∞ = 1.27576 ± 0.00024 |
| `assembly_p126_hot.txt` | reference at PWR-operating moderator density, ρ_H₂O = 0.71 g/cm³ | k∞ = 1.38847 ± 0.00033 (−2.1%) |
| `assembly_e015.txt` | pitch 1.26 cm, 1.5% enrichment | k∞ = 1.20611 ± 0.00026 |
| `assembly_e050.txt` | pitch 1.26 cm, 5% enrichment | k∞ = 1.52263 ± 0.00031 |
| `assembly_e200.txt` | pitch 1.26 cm, 20% enrichment | k∞ = 1.66622 ± 0.00036 |
| `assembly_p090_spec.txt` | pitch 0.90 cm + F4 flux tally on the central pin | Φ_th/Φ_fast = 0.108 |
| `assembly_p126_spec.txt` | pitch 1.26 cm + F4 flux tally on the central pin | Φ_th/Φ_fast = 0.372 |
| `assembly_p200_spec.txt` | pitch 2.00 cm + F4 flux tally on the central pin | Φ_th/Φ_fast = 0.821 |

Running a deck:

```bash
mcnp6 i=assembly_p126.txt o=out_p126.txt
```

See the [folder README](../README.md) for the model, the parametric studies and the discussion.
