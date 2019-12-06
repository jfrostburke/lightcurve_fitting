from lightcurve import LC
import models
import fitting
import bolometric

lc = LC.read('example/SN2016bkv.table')
extinction = {
 'U': 0.069,
 'B': 0.061,
 'g': 0.055,
 'V': 0.045,
 '0': 0.035,
 'r': 0.038,
 'R': 0.035,
 'i': 0.028,
 'I': 0.025,
}
z = 0.002
lc.calcAbsMag(dm=30.79, extinction=extinction)
lc.calcLum()

lc_early = lc.where(MJD_min=57468., MJD_max=57485.)
model = models.ShockCooling2
p_min = [0., 0., 0., 57468.]
p_max = [100., 100., 100., 57468.7]
p_lo = [20., 2., 20., 57468.5]
p_up = [50., 5., 50., 57468.7]

sampler = fitting.lightcurve_mcmc(lc_early, model, model_kwargs={'z': z},
                                  p_min=p_min, p_max=p_max, p_lo=p_lo, p_up=p_up, 
                                  nwalkers=10, nsteps=100, nsteps_burnin=100, show=True)

fig = fitting.lightcurve_corner(lc_early, model, sampler.flatchain, model_kwargs={'z': z})
fig.savefig('16bkv_test.png')
