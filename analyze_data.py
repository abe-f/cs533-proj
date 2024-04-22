import h5py
import numpy as np
import os
from readable_number import ReadableNumber
import matplotlib
rn = ReadableNumber

experiment = "capacity_sensitivity"

# config_folders = os.listdir(f"experiments/{experiment}")
configs = ['768MBLLC', '1024MBLLC', '1280MBLLC', '1408MBLLC', '1536MBLLC',  '1792MBLLC', '2048MBLLC']
data_dict = {config:(h5py.File(f"experiments/{experiment}/{config}/data/zsim-ev.h5", 'r')["stats"]["root"]) for config in configs}

# Create plot for IPC
ipcs = []
for k in data_dict.keys():
    print( k + " : " + str(np.max(data_dict[k][-1]['beefy']['cycles'])))
    # Maybe we can add all instructions and all cycles, then divide?
    print( k + " : " + str(np.max(data_dict[k][-1]['beefy']['instrs']/data_dict[k][-1]['beefy']['cycles'])))
    ipcs.append(np.max(data_dict[k][-1]['beefy']['instrs']/data_dict[k][-1]['beefy']['cycles']))

plt.bar(configs, ipc)