
import random

def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = f"""### Human: {data['question']}\n### Assistant:"""
    return {
        "input": text, 
        #"input": text.strip(), 
        "output": "", 
        "processed_output": ""
        }
    