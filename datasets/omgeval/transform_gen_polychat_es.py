
import random

def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = f"""<|user|>\n{data['question'].strip()}<|assistant|>\n"""
    return {
        "input": text, 
        #"input": text.strip(), 
        "output": "", 
        "processed_output": ""
        }
    