
import random

def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    prompt = data['prompt'].strip().replace("    ", "\t")
    temp_input = f"""### Input:User:Создайте скрипт Python для этой задачи. Скрипт Python должен быть включен в ```python``` теги.{prompt}### Response:"""
    return {"input": temp_input, "output": "", "processed_output": ""}
    