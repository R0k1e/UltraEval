
import random

def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    prompt = data['prompt'].strip().replace("    ", "\t")
    temp_input = f"""### Input:User:Créez un script Python pour cette question. Le script Python doit être entouré de ```python```.{prompt}### Response:"""
    return {"input": temp_input, "output": "", "processed_output": ""}
    