
import numpy as np
try:
    import cupy as cp
    GPU_AVAILABLE = True
except Exception:
    cp = np  # fallback
    GPU_AVAILABLE = False

G_KPC = 4.30091e-6  # kpc (km/s)^2 Msun^-1

def _xp():
    return cp if GPU_AVAILABLE else np

def model_gr(r, M_disk, h):
    xp = _xp()
    x = r / (2.0 * h)
    # CuPy lacks modified Bessel; fallback to NumPy then cast
    if GPU_AVAILABLE:
        import scipy.special as sp
        x_cpu = cp.asnumpy(x)
        term = sp.i0(x_cpu)*sp.k0(x_cpu) - sp.i1(x_cpu)*sp.k1(x_cpu)
        term = np.nan_to_num(term)
        term = cp.asarray(term)
    else:
        from scipy.special import i0, i1, k0, k1
        term = i0(x)*k0(x) - i1(x)*k1(x)
        term = np.nan_to_num(term)
    v2 = (G_KPC * M_disk / h) * 2.0 * x**2 * term
    return xp.sqrt(xp.maximum(v2, 0))

def model_lcdm(r, M_disk, h, rho0, rs):
    xp = _xp()
    v_disk = model_gr(r, M_disk, h)
    x = r/rs
    M_enc = 4.0 * np.pi * rho0 * rs**3 * (xp.log(1+x) - x/(1+x))
    v_halo = xp.sqrt(G_KPC * M_enc / xp.maximum(r, 1e-5))
    return xp.sqrt(v_disk**2 + v_halo**2)

def model_3te(r, M_disk, h, alpha, r_e):
    xp = _xp()
    v_disk = model_gr(r, M_disk, h)
    entropy_grad = 1.0 + alpha * (1 - xp.exp(-r / r_e))
    return v_disk * entropy_grad
