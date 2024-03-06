
import random

def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = f"""[INST] {data['question']} [/INST]"""
    return {
        "input": text, 
        #"input": text.strip(), 
        "output": "", 
        "processed_output": ""
        }
    