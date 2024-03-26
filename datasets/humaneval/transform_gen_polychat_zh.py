
import random

def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    prompt = data['prompt'].strip().replace("    ", "\t")
    temp_input = f"""<|user|>\n请为以下问题写一个Python脚本。Python脚本需要用```python```标签包裹。\n{prompt.strip()}\n\n<|assistant|>\n"""
    return {"input": temp_input, "output": "", "processed_output": ""}
    