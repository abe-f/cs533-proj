import os
import subprocess
import time
import glob
import shutil
import sys 

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

# The top-level keys here are the different experiments.
# The value for those keys is another dictionary, that contains the benchmark names and commands
graph_dataset = "synth_large.el"

runs = {"eval" : {
    'bc' : f"../../../../benchmarks/gapbs/bc     -f ../../../../benchmarks/gapbs/{graph_dataset} -n 1",
    'cc' : f"../../../../benchmarks/gapbs/cc     -f ../../../../benchmarks/gapbs/{graph_dataset} -n 1",
    'pr' : f"../../../../benchmarks/gapbs/pr     -f ../../../../benchmarks/gapbs/{graph_dataset} -n 1",
    'sssp' : f"../../../../benchmarks/gapbs/sssp -f ../../../../benchmarks/gapbs/{graph_dataset} -n 1",
    'bfs' : f"../../../../benchmarks/gapbs/bfs   -f ../../../../benchmarks/gapbs/{graph_dataset} -n 1",
    #'tc' : f"../../../../benchmarks/gapbs/tc     -s -f ../../../../benchmarks/gapbs/{graph_dataset} -n 1",
}}

for experiment in runs.keys():
    if (not os.path.exists(f"experiments/{experiment}")):
        print(f"Failure: experiments/{experiment} does not exist")
        exit(0)

proc_dict = {}
total_proc_counter = 0;
for experiment in runs.keys():
    config_folders = os.listdir(f"experiments/{experiment}")
    config_folders.sort()

    print(f"config_folders = {config_folders}")

    for config_folder in config_folders:
        # Make data folder in the config folder and cd into it
        # If it already exists, delete it (can change this in future)
        os.chdir(f"{top_dir}/experiments/{experiment}/{config_folder}")

        for benchmark in runs[experiment].keys():
            data_folder_path = f"{top_dir}/experiments/{experiment}/{config_folder}/{benchmark}_data"
            try:
                os.mkdir(data_folder_path)
            except:
                shutil.rmtree(data_folder_path)
                os.mkdir(data_folder_path)
            os.chdir(data_folder_path)
            
            # Change dir into the data folder
            print(f"Changing working directory to: {data_folder_path}")

            config_path = f"../{config_folder}.cfg"
            # Replace the command = "" line in the config with the right command
            with open(config_path, 'r', encoding='utf-8') as file: 
                lines = file.readlines() 
            
            benchmark_command = runs[experiment][benchmark]
            for i in range(len(lines)):
                if ("command =" in lines[i]):
                    lines[i] = f"  command = \"{benchmark_command}\"\n"
            
            with open(config_path, 'w') as file: 
                file.writelines(lines) 
                file.flush()
                file.close()

            # adding a wait here because the subprocess may not see the updates to the cfg in time
            time.sleep(.1)

            # Now, run the actual job
            command = f"../../../../zsim/build/opt/zsim ../{config_folder}.cfg > command_out.txt"
            print(f"Executing command: {command}")
            proc_dict[f"{experiment}.{config_folder}.{benchmark}"] = subprocess.Popen(command,  shell=True)
            sys.stdout.flush()
            total_proc_counter += 1
            time.sleep(.1)

        os.chdir(f"{top_dir}")

proc_counter = 0;
while (bool(proc_dict.copy())):
    for config in proc_dict.copy().keys():
        if proc_dict[config].poll() is not None:
            proc_counter += 1
            print(f"[{proc_counter}/{total_proc_counter}] {config} ---> FINISHED")
            proc_dict.pop(config)
            
    time.sleep(2)

exit()

config_folders = os.listdir(f"experiments/{experiment}")
config_folders.sort()
print(f"config_folders = {config_folders}")
proc_dict = {}
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
    proc_dict[f"{config_folder}"] = subprocess.Popen(command,  shell=True)
    sys.stdout.flush()


 
print("All tests finished")