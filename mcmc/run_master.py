from cobaya.yaml import yaml_load
from cobaya.run import run

info = yaml_load("""
likelihood:
  bao.desi_2024_bao_all:           null
  planck_2018_lowl.TT:             null
  planck_2018_lowl.EE:             null
  planck_2018_highl_CamSpec.TTTEEE: null

params:
  alpha:          [0., 0.2]
  log10S0_over_H02: [-2, 2]
  omega_b:        0.0224 ± 0.0001
  omega_cdm:      0.12   ± 0.002
  h:              0.68   ± 0.01
  n_s:            0.965  ± 0.004
sampler:
  mcmc:
    Rminus1_stop: 0.01
""")

run(info, resume=False)
