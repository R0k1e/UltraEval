
import random

def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    prompt = data['prompt'].strip().replace("    ", "\t")
    temp_input = f"""<|user|>\nCréez un script Python pour cette question. Le script Python doit être entouré de ```python```.\n{prompt.strip()}\n\n<|assistant|>\n"""
    return {"input": temp_input, "output": "", "processed_output": ""}
    