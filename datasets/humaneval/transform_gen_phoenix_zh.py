
import random

def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    prompt = data['prompt'].strip().replace("    ", "\t")
    temp_input = f"""Human: <s>请为以下问题写一个Python脚本。Python脚本需要用```python```标签包裹。{prompt}</s>Assistant: <s>"""
    return {"input": temp_input, "output": "", "processed_output": ""}
    