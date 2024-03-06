
import random

def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    prompt = data['prompt'].strip().replace("    ", "\t")
    temp_input = f"""### Input:User:Cree un script Python para esta pregunta. El script Python debe estar enmarcado por ```python```.{prompt}### Response:"""
    return {"input": temp_input, "output": "", "processed_output": ""}
    