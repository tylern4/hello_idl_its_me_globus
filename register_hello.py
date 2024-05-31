from globus_compute_sdk import Client
from dotenv import load_dotenv

gc = Client()

ENV_PATH = "./hello.env"
load_dotenv(dotenv_path=ENV_PATH)


def hello_python_world():
    import subprocess
    command = [
        "/global/common/software/nersc/pe/conda-envs/24.1.0/python-3.11/nersc-python/bin/python",
        "/dvs_ro/cfs/cdirs/m3792/tylern/DIII-D/hello_idl_its_me_globus/hello.py"
    ]
    res = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return res


def hello_idl_world():
    import subprocess
    command = [
        "/global/common/software/nersc/pm-2022q2/sw/idl/idl89/idl/bin/idl",
        "/dvs_ro/cfs/cdirs/m3792/tylern/DIII-D/hello_idl_its_me_globus/hello.pro"
    ]
    res = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return res


def register_functions(functions={"HELLO_PYTHON": hello_python_world,
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
