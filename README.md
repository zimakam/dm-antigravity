# dm-antigravity
ΔM-Antigravity: A Numerical Model of Repulsive Force Between Nested Mass Layers
# ΔM-Antigravity

**A numerical model of repulsive force between nested mass layers.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)

Author: **Зиявутдинов Магомед Камалович (Zimaka)** · zimakam@gmail.com

---

## Idea

Between two nested mass layers (inner mass `M_n`, outer mass `M_{n+1}`) the force
contains a **repulsive term proportional to the mass difference** `ΔM = M_{n+1} − M_n`.

```
g(r) = −G·M_n / r²  +  α·ΔM / r² · ξ(r / r_eq)

ξ(x) = (1 − tanh(x − 1)) / 2
r_eq = (3·G·M_n / (4π·|α·ΔM|))^(1/3)
```

**Behaviour:**

| Region       | Dominant term | Sign of g          |
|--------------|---------------|--------------------|
| `r ≪ r_eq`   | `α·ΔM / r²`   | repulsive (g > 0)  |
| `r ≈ r_eq`   | cancellation  | equilibrium (g ≈ 0) |
| `r ≫ r_eq`   | `−G·M_n / r²` | attractive (g < 0) |

Unlike the cosmological constant Λ, the effect is **local** and depends only on
local masses. The transition is smooth (via `tanh`), so there are no
singularities.

## Prediction

```
r_eq ∝ (M / ΔM)^(1/3)
```

This scaling is testable numerically. The script verifies it for a wide range
of `ΔM`.

## Quick start

```bash
pip install numpy
python Delta_mass_gravity.py
```

Expected output:

```
ΔM-Antigravity — numerical verification

  r_eq scaling:  PASS  (max error 1.2e-15)
  sign at 0.1·r_eq:  repulsive
  sign at 10·r_eq:   attractive
  equilibrium at r_eq: |g| < 1e-12

  All checks passed.
```

## What this is

- A **numerical model** with a closed-form formula for the equilibrium radius.
- A **reproducible test** of the `(M/ΔM)^(1/3)` scaling.
- A **research prototype** (TRL 3) written in pure NumPy.

## What this is not

- Not a physical theory (no first-principles derivation).
- Not an experimental claim (no measurements).
- Not a replacement for Λ or Yukawa (a different construction).
- Not a "fifth force" (no claim of universality).

## Related work

- **Cosmological constant Λ** — repulsive on large scales, but Λ is a global
  constant, while `ΔM` is local.
- **Yukawa interaction** — exponential cutoff at a characteristic range, but
  Yukawa is attractive here and has no `r_eq`.
- **Nested mass shells** — discussed in astrophysics for gravitational
  stability, but without an equilibrium radius scaling as `(M/ΔM)^(1/3)`.

## Citation

```bibtex
@software{ziyavutdinov_antigravity_2026,
  author    = {Зиявутдинов, Магомед Камалович},
  title     = {ΔM-Antigravity: A Numerical Model of Repulsive Force
               Between Nested Mass Layers},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.XXXXXXX},
  license   = {MIT}
}
```

## License

MIT — see [LICENSE](LICENSE).