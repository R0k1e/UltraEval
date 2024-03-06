import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    temp_input = f"[INST] Implement the following Python function according to the enclosed comments. [/INST] {data['prompt'].strip()}"
    return {"input": temp_input, "output": "", "processed_output": ""}
