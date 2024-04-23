#  ../zsim/build/opt/zsim test.cfg

import h5py
import numpy as np
from readable_number import ReadableNumber
import pandas as pd
#import h5pandas as h5pd

rn = ReadableNumber

f = h5py.File("zsim.h5", 'r')

print(f.keys())

dset = f["stats"]["root"]

#totalInstrs = np.sum(dset[-1]['beefy']['instrs'])
# to get core N, do dset[-1]['beefy'][N]['instrs']
print(dset.shape)
print(type(dset))
print(dset.dtype.names)
print(dset['l1d'].dtype.names)
print(dset['l1d']['fhGETS'][:, 0])
#print(type(np.indices(dset[0])))
#print(type(dset[0]))

#dataframes = [pd.DataFrame(np.array(h5py.File("zsim.h5")['stats']['root'][x])) for x in range(256)]

