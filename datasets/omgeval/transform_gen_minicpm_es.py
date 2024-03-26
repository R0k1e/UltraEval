
import random

def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = f"""<用户>{prompt}<AI>"""
    return {
        "input": text, 
        #"input": text.strip(), 
        "output": "", 
        "processed_output": ""
        }
    