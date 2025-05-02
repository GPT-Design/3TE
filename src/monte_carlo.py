
import numpy as np
import cupy as cp

def monte_carlo(radii, model_fn, param_means, param_stds, n=10000, seed=42):
    cp.random.seed(seed)
    radii_gpu = cp.asarray(radii, dtype=cp.float32)
    draws = [cp.random.normal(m, s, n).astype(cp.float32)
             for m, s in zip(param_means, param_stds)]
    vel = cp.zeros((n, radii_gpu.size), dtype=cp.float32)
    for i in range(n):
        params = [d[i] for d in draws]
        vel[i] = model_fn(radii_gpu, *params)
    return vel.mean(axis=0).get(), vel.std(axis=0).get()
