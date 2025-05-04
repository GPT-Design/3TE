import numpy as np
from scipy.integrate import quad, odeint

# --- baseline ΛCDM-like params (tweak later) ---
h         = 0.68
Omega_b   = 0.0224 / h**2
Omega_cdm = 0.12   / h**2
Omega_m   = Omega_b + Omega_cdm
Omega_r   = 9.2e-5
Omega_L   = 1.0 - Omega_m - Omega_r

# --- 3T_E extras (placeholder values) ---
Omega_R0  = 1e-4
Omega_E0  = 2e-3
w_E       = 0.02  # ~ α/3

def H(a):
    """Hubble parameter in units of H0."""
    return np.sqrt(
        Omega_r * a**-4
        + (Omega_m + Omega_R0)*a**-3
        + Omega_E0*a**(-3*(1+w_E))
        + Omega_L
    )

def comoving_distance(z):
    return quad(lambda zp: 1.0 / H(1/(1+zp)), 0, z)[0]

def angular_diameter_distance(z):
    return comoving_distance(z) / (1+z)

def growth_factor():
    def dDdx(D, ln_a):
        a    = np.exp(ln_a)
        D1,D2 = D
        dlnH = (
            - Omega_r*a**-4
            - 1.5*(Omega_m+Omega_R0)*a**-3
            - 1.5*(1+w_E)*Omega_E0*a**(-3*(1+w_E))
        )/H(a)**2
        return [D2, -(2+dlnH)*D2 + 1.5*(Omega_m+Omega_R0)*a**-3/H(a)**2 * D1]

    ln_a = np.linspace(-7,0,500)
    D0,_ = odeint(dDdx, [1e-5,1e-5], ln_a)[-1]
    return D0/D0  # normalized to 1 at a=1       # normalised → 1.0

class FLRWTheory:
    # Tell Cobaya which parameters we expect and which functions we provide:
    requires = ['alpha','log10S0_over_H02','omega_b','omega_cdm','h','n_s']
    provides = ['angular_diameter_distance','growth_factor']

    def __init__(self, info):
        # You can pull out alpha, log10S0_over_H02 here if you want them
        self.alpha = info.get('alpha')
        self.S0    = 10**info.get('log10S0_over_H02') * (info.get('h')**2)

    def angular_diameter_distance(self, z):
        return angular_diameter_distance(z)

    def growth_factor(self):
        return growth_factor()

if __name__ == "__main__":
    D1 = growth_factor()
    print({"sigma8": 0.81 * D1})          # ~0.81 for these placeholders
