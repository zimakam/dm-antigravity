#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ΔM-Antigravity: A Numerical Model of Repulsive Force Between Nested Mass Layers

Author: Зиявутдинов Магомед Камалович (Zimaka)
Email:  zimakam@gmail.com
License: MIT

Formula:
    g(r) = −G·M / r²  +  α·ΔM / r² · ξ(r / r_eq)
    ξ(x) = (1 − tanh(x − 1)) / 2
    r_eq = (3·G·M / (4π·|α·ΔM|))^(1/3)
"""

from __future__ import annotations
import math
from typing import Tuple

G_DEFAULT = 6.674e-11
ALPHA_DEFAULT = 1.0


def xi(x: float) -> float:
    """Smooth transition from 1 (r ≪ r_eq) to 0 (r ≫ r_eq)."""
    return (1.0 - math.tanh(x - 1.0)) / 2.0


def r_equilibrium(M: float, dM: float,
                  G: float = G_DEFAULT,
                  alpha: float = ALPHA_DEFAULT) -> float:
    """
    Equilibrium radius: r_eq = (3·G·M / (4π·|α·ΔM|))^(1/3).

    Returns +inf if ΔM ≈ 0 (no repulsion → no equilibrium).
    """
    denom = 4.0 * math.pi * abs(alpha * dM)
    if denom < 1e-30:
        return float('inf')
    return (3.0 * G * M / denom) ** (1.0 / 3.0)


def g(r: float, M: float, M_next: float,
      G: float = G_DEFAULT,
      alpha: float = ALPHA_DEFAULT) -> float:
    """
    Gravitational acceleration at radius r between two mass layers.

    Positive g  →  repulsive (antigravity)
    Negative g  →  attractive (gravity)
    """
    if r <= 0.0:
        return 0.0
    dM = M_next - M
    req = r_equilibrium(M, dM, G, alpha)
    if req == float('inf'):
        return -G * M / (r * r)
    return (-G * M / (r * r)
            + alpha * dM / (r * r) * xi(r / req))


def sign_at(r: float, M: float, M_next: float,
            G: float = G_DEFAULT,
            alpha: float = ALPHA_DEFAULT,
            tol: float = 1e-20) -> str:
    """Classify the force at radius r."""
    val = g(r, M, M_next, G, alpha)
    if abs(val) < tol:
        return "equilibrium"
    return "repulsive" if val > 0 else "attractive"


def verify_scaling(M: float = 1.0,
                   dMs: Tuple[float, ...] = (1e-3, 1e-2, 1e-1, 1.0, 10.0),
                   G: float = G_DEFAULT,
                   alpha: float = ALPHA_DEFAULT) -> dict:
    """
    Verify that r_eq³ · ΔM is constant for fixed M.
    Predicted constant: 3·G·M / (4π·|α|).
    """
    expected = 3.0 * G * M / (4.0 * math.pi * abs(alpha))
    errors = []
    for dM in dMs:
        req = r_equilibrium(M, dM, G, alpha)
        observed = req ** 3 * abs(alpha * dM)
        errors.append(abs(observed - 3.0 * G * M / (4.0 * math.pi)))
    max_err = max(errors) if errors else 0.0
    return {
        "expected_constant": expected,
        "max_error": max_err,
        "passed": max_err < 1e-12 * max(abs(expected), 1.0),
    }


def verify_signs(M: float = 1.0,
                 dM: float = 0.1,
                 G: float = G_DEFAULT,
                 alpha: float = ALPHA_DEFAULT) -> dict:
    """Verify that sign(g) flips at r_eq."""
    req = r_equilibrium(M, dM, G, alpha)
    inside = sign_at(0.1 * req, M, M + dM, G, alpha)
    outside = sign_at(10.0 * req, M, M + dM, G, alpha)
    at_eq = abs(g(req, M, M + dM, G, alpha))
    return {
        "r_eq": req,
        "inside": inside,
        "outside": outside,
        "residual_at_r_eq": at_eq,
        "passed": (inside == "repulsive"
                   and outside == "attractive"
                   and at_eq < 1e-12),
    }


def main() -> None:
    print("ΔM-Antigravity — numerical verification\n")

    sc = verify_scaling()
    status = "PASS" if sc["passed"] else "FAIL"
    print(f"  r_eq scaling:  {status}  (max error {sc['max_error']:.2e})")

    sg = verify_signs()
    print(f"  sign at 0.1·r_eq:  {sg['inside']}")
    print(f"  sign at 10·r_eq:   {sg['outside']}")
    print(f"  equilibrium at r_eq: |g| = {sg['residual_at_r_eq']:.2e}")

    if not (sc["passed"] and sg["passed"]):
        raise SystemExit(1)

    print("\n  All checks passed.")


if __name__ == "__main__":
    main()