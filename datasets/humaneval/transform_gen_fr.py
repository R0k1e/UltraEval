import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    prompt = data['prompt'].strip().replace("    ", "\t")
    temp_input = f"""[INST]Veuillez écrire un script Python pour le problème suivant:
{prompt}

[/INST]"""
    # temp_input = f"[INST] Create a Python script for this problem: {data['prompt']} [/INST]"
    return {"input": temp_input, "output": "", "processed_output": ""}
