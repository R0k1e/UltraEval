
import random

def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    prompt = data['prompt'].strip().replace("    ", "\t")
    temp_input = f"""<|user|>\nСоздайте скрипт Python для этой задачи. Скрипт Python должен быть включен в ```python``` теги.\n{prompt.strip()}\n\n<|assistant|>\n"""
    return {"input": temp_input, "output": "", "processed_output": ""}
    