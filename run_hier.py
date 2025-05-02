
"""
Hierarchical α, ℓ_E sampler.

Usage:
    python run_hier.py data/*.csv
Outputs:
    results/posterior.h5, per‑galaxy summary plots
"""
import argparse, glob, os, h5py, numpy as np
import emcee, corner, matplotlib.pyplot as plt
from src import models

def log_prior(theta):
    alpha, l_e = theta
    if 0 < alpha < 0.2 and 1 < l_e < 20:
        return 0.0
    return -np.inf

def log_like(theta, galaxies):
    alpha, l_e = theta
    ll = 0.0
    for g in galaxies:
        r, v, err, mdisk, h = g  # pre‑pack
        pred = models.model_3te(r, mdisk, h, alpha, l_e)
        ll += -0.5*np.sum(((v - pred)/err)**2 + np.log(2*np.pi*err**2))
    return ll

def main(patterns):
    files = [f for p in patterns for f in glob.glob(p)]
    galaxies = []
    for f in files:
        import pandas as pd
        df = pd.read_csv(f)
        r = df['Radius_kpc'].values
        v = df['Velocity_km_s'].values
        err = 0.5*(df['Velocity_upper_error_km_s'] - df['Velocity_lower_error_km_s']).values
        # naive priors for mdisk, h
        mdisk = 5e9
        h = 1.5
        galaxies.append((r, v, err, mdisk, h))
    ndim, nwalk = 2, 100
    p0 = np.random.rand(nwalk, ndim)*[0.05, 5] + [0.02, 5]
    sampler = emcee.EnsembleSampler(nwalk, ndim,
                                    lambda th: log_prior(th)+log_like(th, galaxies))
    sampler.run_mcmc(p0, 5000, progress=True)
    chain = sampler.get_chain(discard=1000, flat=True)
    with h5py.File('results/posterior.h5', 'w') as h5:
        h5['chain'] = chain
    fig = corner.corner(chain, labels=[r'$\alpha$', r'$\ell_E$'])
    fig.savefig('results/posterior_corner.png', dpi=200)
    print("Done. Posterior saved to results/")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('patterns', nargs='+')
    args = parser.parse_args()
    main(args.patterns)
