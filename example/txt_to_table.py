import numpy as np
from astropy.io import ascii

name = 'SN2017cbv'

data_in = np.genfromtxt('{name}.txt'.format(name=name),dtype=str)

mjd = [float(x[1])-2400000.5 for x in data_in]
mag = [float(x[2]) for x in data_in]
dmag = [float(x[3]) for x in data_in]
filt = [x[5] for x in data_in]
source = ['Las Cumbres']*len(data_in)
nondet = ['False']*len(data_in)

data_out = [mjd,mag,dmag,filt,source,nondet]

ascii.write(data_out,
	output='{name}.table'.format(name=name),
	names=['MJD', 'mag', 'dmag', 'filt', 'source', 'nondet'],
	delimiter='|',
	format='fixed_width')
