from cobaya.yaml import yaml_load
from cobaya.run import run

info = yaml_load("""
likelihood:
  bao.desi_2024_bao_all:            null
  planck_2018_highl_CamSpec.TTTEEE: null

theory:
  external:
    module: src.flrw_3te
    class:  FLRWTheory

params:
  # 3T_E freedom
  alpha:           [0.0, 0.2]
  log10S0_over_H02: [-2.0, 2.0]

  # “Planck-lite” uniform priors
  omega_b:   [0.0222, 0.0226]
  omega_cdm: [0.118,  0.122 ]
  h:         [0.67,   0.69  ]
  n_s:       [0.964,  0.968 ]

sampler:
  mcmc:
    Rminus1_stop: 0.01
    max_tries:    900000
""")

run(info, resume=False)
