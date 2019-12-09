import numpy as np
from datetime import datetime
import time

from lightcurve import LC
import models
import fitting
import bolometric

start_time = time.time()

print('Initializing data . . .')
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
lc_early = lc.where(MJD_min=57821., MJD_max=57871.)
model = models.CompanionShocking

# t_0, a, M*v^7, T_max, s, r_r, r_i, r_U
griffin_numbers = np.array([57821.9, 0.392, 3.84, 57840.8458, 1.04, 0.95, 0.85, 0.61])
p_min = griffin_numbers-0.3
p_max = griffin_numbers+0.3
#p_min[0] = 57821.9 - 1
#p_min[0] = 57821.9 + 1
p_min[1] = 0.15
p_max[1] = 0.4
p_min[2] = 0.5
p_max[2] = 4.2
p_max[3] = 57840.8458 - 1
p_max[3] = 57840.8458 + 1
#p_min = np.array([57819.9, 0.1, 2, 57838.8458, 0.90, 0.80, 0.70, 0.50])
#p_min = np.array([57823.9, 1.0, 5, 57842.8458, 1.28, 1.10, 1.00, 0.72])

print('Fitting lightcurve . . .')
result = None
while result is None:
    try:
        sampler = fitting.lightcurve_mcmc(lc_early, model, model_kwargs={'z': z},
                                  p_min=p_min, p_max=p_max,
                                  nwalkers=64, nsteps=1000, nsteps_burnin=1000, show=True)
        print()
        print('    Retrying . . .')
        print()
        result = True
    except:
        result = None

label = datetime.utcnow().strftime('%Y%m%d%H%M%S')
fit_name = '17cbv_{label}.png'.format(label=label)
print('Plotting fit, saving as  {fit_name}. . .'.format(fit_name=fit_name))
fig = fitting.lightcurve_corner(lc_early, model, sampler.flatchain, model_kwargs={'z': z})
fig.savefig(fit_name)

end_time = time.time()
print('Total runtime: {t:.1f} s'.format(t=end_time-start_time))
print()

