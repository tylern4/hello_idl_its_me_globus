import globus_compute_sdk
from globus_compute_sdk import Client
from dotenv import load_dotenv
from fusion_compute import ENV_PATH
import os, time
import argparse
from scipy import stats
import json
from fusion_compute.machine_settings import machine_settings
from matplotlib import pyplot as plt

gc = Client()

ENV_PATH = "./hello.env"
load_dotenv(dotenv_path=ENV_PATH)

def hello_python_world():
    import subprocess
    command = f"python /fusion/projects/results/ionorbgpu/workflow_files/ionorbgpu/v2/tools/hello.py"
    res = subprocess.run(command.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return res

def hello_idl_world():
    import subprocess
    command = f"idl /fusion/projects/results/ionorbgpu/workflow_files/ionorbgpu/v2/tools/hello.pro"
    res = subprocess.run(command.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return res

def register_functions(functions={"HELLO_PYTHON":hello_python_world, 
                                  "HELLO_IDL": hello_idl_world}):
    function_ids = {}
    for envvar in functions:
        func = gc.register_function(functions[envvar])
        with open(ENV_PATH, "a") as f:
            f.write(f"\n{envvar}={func}\n")
        print(f"{envvar}={func}")
        function_ids[envvar] = func

    return function_ids

if __name__ == '__main__':
    
    register_functions()
