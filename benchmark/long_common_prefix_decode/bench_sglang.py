# Benchmark with long common prefixes. Used to benchmark cascade attention performance.
import os
import random
import string
import sys
import time

from tqdm import tqdm
from transformers import AutoTokenizer

import sglang as sgl
from sglang import set_default_backend
from sglang.lang.backend.runtime_endpoint import RuntimeEndpoint

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

def generate_unique_suffix():
    tasks = ["bubble sort", "quick sort", "merge sort", "tarverse tree", "Dijkstra"]
    languages = ["Python", "Java", "C++", "JavaScript", "Rust", "Go"]
    suffixes = []
    for task in  tasks:
        for language in languages:
            suffixes.append(f"write a {task} program in {language}")


@sgl.function
def text_gen(s, system, user):
    s += "System: " + system + "\n"
    s += "User: " + user + "\n"
    s += "Assisstant:" + sgl.gen("answer", temperature=0, max_tokens=256)


def test_send_all(all_prompts, gen_len):
    backend.flush_cache()

    all_prompts = [x for prompt_list in all_prompts for x in prompt_list]

    tic = time.time()
    text_qa.run_batch(
        list(zip(all_prompts, [gen_len] * len(all_prompts))),
    )
    tot_time = time.time() - tic

    return tot_time


if __name__ == "__main__":
    backend = RuntimeEndpoint("http://127.0.0.1:30000")
    set_default_backend(backend)
    with open('claude_system_prompt', 'r') as file:
        prefix = file.read()
    suffixes = generate_unique_suffix()

    cost = test_send_all(all_prompts, gen_len)
    print(f"Latency of test_send_all                : {cost:.4f} s\n")
