# 3T_E Galactic‑Rotation Analysis

Reproducible pipeline for comparing Three‑Tensor Entropy gravity (3T_E) with GR and ΛCDM on galaxy rotation‑curve data.

* **Batch notebook** – quick Colab exploration (`notebooks/rotation_batch.ipynb`).
* **Hierarchical sampler** – CUDA‑accelerated MCMC on a local 40‑series GPU (`run_hier.py`).
* **Makefile** – `make quick`, `make hier`, `make pdf`.

Clone, create the conda env, and run:

```bash
conda env create -f env.yml
conda activate 3te
make quick   # Colab/CPU
make hier    # full GPU hierarchical fit
```
