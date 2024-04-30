from globus_compute_sdk import Client
from dotenv import load_dotenv
import os
import argparse

import json

gc = Client()

ENV_PATH = "./hello.env"
load_dotenv(dotenv_path=ENV_PATH)


def run_batch(function, nbatch=200):
   
    function_id = os.getenv(function)
    endpoint_id = os.getenv("ENDPOINT_ID")

    batch = gc.create_batch()

    for i in range(nbatch):
        batch.add(function_id=function_id)
 
    batch_ret = gc.batch_run(endpoint_id,batch=batch)
    with open(f"hello_test_{function}_{nbatch}.json","w") as f:
        json.dump(batch_ret,f)
    
    return batch_ret

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', default='idl', help=f'Language for hello', choices=["idl","python"])
    return parser.parse_args()
    
if __name__ == '__main__':

    args = arg_parse()

    if args.type == "idl":
        run_batch("HELLO_IDL")
    elif args.type == "python":
        run_batch("HELLO_PYTHON")
    else:
        print("Unknown Language")
