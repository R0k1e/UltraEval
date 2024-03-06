import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    prompt = data['prompt'].strip().replace("    ", "\t")
    temp_input = f"""<|user|>
请为以下问题写一个Python脚本：
{prompt}

<|assistant|>
"""
    # temp_input = f"[INST] Create a Python script for this problem: {data['prompt']} [/INST]"
    return {"input": temp_input, "output": "", "processed_output": ""}
