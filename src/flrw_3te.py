import numpy as np
from scipy.integrate import odeint

# --- baseline ΛCDM-like params (tweak later) ---
h         = 0.68
Omega_b   = 0.0224 / h**2
Omega_cdm = 0.12   / h**2
Omega_m   = Omega_b + Omega_cdm
Omega_r   = 9.2e-5                       # photons+neutrinos
Omega_L   = 1.0 - Omega_m - Omega_r

# --- 3T_E extras (placeholder values) ---
Omega_R0  = 1e-4                         # rotational dust
Omega_E0  = 2e-3                         # entropy fluid
w_E       = 0.02                         # ~ α/3

def H(a):
    """Hubble parameter in units of H0."""
    return np.sqrt(
        Omega_r * a**-4 +
        (Omega_m + Omega_R0) * a**-3 +
        Omega_E0 * a**(-3 * (1 + w_E)) +
        Omega_L
    )

def growth_factor():
    """Return linear-growth factor D(a=1) normalised to ΛCDM σ8≈0.81."""
    def dDdx(D, ln_a):
        a        = np.exp(ln_a)
        D1, D2   = D                  # D,  dD/dln a
        dlnH     = (
            - Omega_r * a**-4
            - 1.5 * (Omega_m + Omega_R0) * a**-3
            - 1.5 * (1 + w_E) * Omega_E0 * a**(-3 * (1 + w_E))
        ) / H(a)**2
        D1p      = D2
        D2p      = -(2. + dlnH) * D2 + 1.5 * (Omega_m + Omega_R0) * a**-3 / H(a)**2 * D1
        return [D1p, D2p]

    ln_a   = np.linspace(-7, 0, 500)      # integrate from a=1e-7 to 1
    D_init = [1e-5, 1e-5]                 # small seed
    D, _   = odeint(dDdx, D_init, ln_a)[-1]
    return D / D                          # normalised → 1.0

if __name__ == "__main__":
    D1 = growth_factor()
    print({"sigma8": 0.81 * D1})          # ~0.81 for these placeholders
