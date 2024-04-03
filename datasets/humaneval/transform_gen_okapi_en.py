
import random

def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    prompt = "Create a Python script for this problem. The Python script should be enclosed by ```python``` tags. " + data['prompt'].strip().replace("    ", "\t")
    temp_input = f"""[INST] {prompt} [/INST]"""
    return {"input": temp_input, "output": "", "processed_output": ""}
    