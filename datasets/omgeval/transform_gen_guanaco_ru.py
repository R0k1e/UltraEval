
import random

def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = f"""### Input:\nUser: {data['question']}\n### Response:\n"""
    return {
        "input": text, 
        #"input": text.strip(), 
        "output": "", 
        "processed_output": ""
        }
    