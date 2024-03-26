
import random

def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    prompt = data['prompt'].strip().replace("    ", "\t")
    temp_input = f"""<|user|>\nCreate a Python script for this problem. The Python script should be enclosed by ```python``` tags. \n{prompt.strip()}\n\n<|assistant|>\n"""
    return {"input": temp_input, "output": "", "processed_output": ""}
    