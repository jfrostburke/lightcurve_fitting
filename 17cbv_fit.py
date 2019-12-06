import numpy as np
from lightcurve import LC
import models
import fitting
import bolometric

lc = LC.read('example/SN2017cbv.table')
extinction = {
 'U': 0.7106,
 'B': 0.5944,
 'g': 0.5382,
 'V': 0.4461,
 'r': 0.3711,
 'i': 0.2745,
}
z = 0.003999
lc.calcAbsMag(dm=31.14, extinction=extinction)
lc.calcLum()

#lc_early = lc.where(MJD_min=57821., MJD_max=57841.)
model = models.CompanionShocking

# t_0, a, M*v^7, T_max, s, r_r, r_i, r_U
griffin_numbers = np.array([57821.9, 0.392, 3.84, 57840.8458, 1.04, 0.95, 0.85, 0.61])
p_min = griffin_numbers-0.3
p_max = griffin_numbers+0.3

sampler = fitting.lightcurve_mcmc(lc, model, model_kwargs={'z': z},
                                  p_min=p_min, p_max=p_max,
                                  nwalkers=16, nsteps=100, nsteps_burnin=100, show=True)

fig = fitting.lightcurve_corner(lc, model, sampler.flatchain, model_kwargs={'z': z})
fig.savefig('16bkv_test.png')
