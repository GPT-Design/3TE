from cobaya.yaml import yaml_load
from cobaya.run import run

info = yaml_load("""
likelihood:
  bao.desi_2024_bao_all:             null
  planck_2018_lowl.TT:               null
  planck_2018_lowl.EE:               null
  planck_2018_highl_CamSpec.TTTEEE:  null

params:
  # 3T_E freedom
  alpha:           [0.0, 0.2]
  log10S0_over_H02: [-2.0, 2.0]

  # “Planck-lite” uniform priors
  omega_b:   [0.0223, 0.0225]
  omega_cdm: [0.118 , 0.122 ]
  h:         [0.67  , 0.69  ]
  n_s:       [0.96  , 0.97  ]

sampler:
  mcmc:
    Rminus1_stop: 0.01
    max_tries:    900000
""")

run(info, resume=False)
