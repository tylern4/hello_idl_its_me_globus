from globus_compute_sdk import Client
from dotenv import load_dotenv

import os
import argparse

import json
from matplotlib import pyplot as plt

gc = Client()

ENV_PATH = "./hello.env"
load_dotenv(dotenv_path=ENV_PATH)

n_workers = 20
sleep_time = 30


def plot_batch(outfiles=[
    "./hello_test_HELLO_PYTHON_200.json",
    "./hello_test_HELLO_IDL_200.json"
]):
    fig = plt.figure()
    max_time = 0
    not_complted = 0
    for outfile in outfiles:
        with open(outfile, "r") as f:
            batch_ret = json.load(f)

        label = outfile.split("_")[3]
        function_id = os.getenv(f"HELLO_{label}")

        results = gc.get_batch_result(batch_ret['tasks'][function_id])

        completion_times = []
        for tid in results:
            # print(results[tid])
            try:
                completion_times.append(float(results[tid]["completion_t"]))
            except KeyError:
                not_complted += 1
                continue
            except Exception as exp:
                print(exp)

        if len(completion_times) > 0:
            tinit = min(completion_times)-sleep_time  # Fudge the start time of the first function
            completion_times = [(t-tinit)/60. for t in completion_times]
            number_completed = [i+1 for i in range(len(completion_times))]
            completion_times.sort()

            plt.plot(completion_times, number_completed, label=label)
            max_time = max(max_time, max(completion_times))

    # Theoretical slope
    slope = n_workers/(sleep_time/60)
    plt.plot([sleep_time/60, max_time],
             [slope*(sleep_time/60), slope*max_time],
             "--", label="Theoretical Maximum Throughput")

    plt.legend(loc=0)
    plt.xlabel("Time (minutes)")
    plt.ylabel("Tasks Completed")
    plt.title(f"{n_workers} workers, sleep time {sleep_time} s")

    fig.savefig("hello_idl.png", dpi=360)
    if not_complted != 0:
        print(f"Still waiting on {not_complted} tasks")


if __name__ == '__main__':

    plot_batch()
