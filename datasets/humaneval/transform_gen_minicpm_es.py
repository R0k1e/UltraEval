
import random

def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    prompt = data['prompt'].strip().replace("    ", "\t")
    temp_input = f"""<用户>{prompt}<AI>"""
    return {"input": temp_input, "output": "", "processed_output": ""}
    