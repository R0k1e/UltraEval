
import random

def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = f"""Human: <s>{data['question']}</s>Assistant: <s>"""
    return {
        "input": text, 
        #"input": text.strip(), 
        "output": "", 
        "processed_output": ""
        }
    