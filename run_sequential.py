import os
import subprocess
import time
import glob
import shutil

# This script runs zsim jobs in parallel.
# - The directory format for your experiments that this script expects is:
# ./experiments/<experiment_name>/<config1>/<config1>.cfg
#                               <config2>/<config2>.cfg
#                               ...
# where <config1>, <config2> can be anything but must be unique

# - The script will make a 'data' folder in config1, config2, etc that stores zsim's output for each experiment
# - The cfg files themselves need to store the path to the benchmark used (with process0.command)
# - Right now, only one experiment can be run, which has several top-level configs. In the future
#       this can be extended to multiple experiments, each with multiple benchmark suites of configs

# ./zsim/build/opt/zsim base_config.cfg
top_dir = os.getcwd()

experiment = "capacity_sensitivity"

if (not os.path.exists(f"experiments/{experiment}")):
    print(f"Failure: experiments/{experiment} does not exist")
    exit(0)

config_folders = os.listdir(f"experiments/{experiment}")
config_folders.sort()
print(f"config_folders = {config_folders}")
for config_folder in config_folders:
    # Make data folder in the config folder and cd into it
    # If it already exists, delete it (can change this in future)
    os.chdir(f"{top_dir}/experiments/{experiment}/{config_folder}")
    try:
        os.mkdir(f"{top_dir}/experiments/{experiment}/{config_folder}/data")
    except:
        shutil.rmtree(f"{top_dir}/experiments/{experiment}/{config_folder}/data")
        os.mkdir(f"{top_dir}/experiments/{experiment}/{config_folder}/data")
    os.chdir(f"{top_dir}/experiments/{experiment}/{config_folder}/data")

    # Change dir into the data folder and run the job
    print(f"Changing working directory to: {top_dir}/experiments/{experiment}/{config_folder}/data")
    command = f"../../../../zsim/build/opt/zsim ../{config_folder}.cfg"
    print(f"Executing command: {command}")
    """
    proc = subprocess.Popen(command,  shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    while (proc.poll() is None):
        time.sleep(10)
    """

print("All tests finished")