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
print(dset['l3'].dtype.names)
#print(dset['l3']['profNumReclaimedSets'][:, 0])

print(np.sum(dset['l3']['profNumReclaimedSets'], 1)) # get the stat summed for all banks at each phase
# calculate num sets
# cache_size = 1073741824
# num_lines = 1073741824/64 = 16777216
# num_sets = 16777216/16 = 1048576
# num_sets_per_bank = 4096



#print(type(np.indices(dset[0])))
#print(type(dset[0]))

#dataframes = [pd.DataFrame(np.array(h5py.File("zsim.h5")['stats']['root'][x])) for x in range(256)]

