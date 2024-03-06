
import random
from UltraEval.tasks.postprocess import GSM8KPost
def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = f"<|user|>\n{data['question'].strip()}<|assistant|>\n"
    correct_answer = data["answer"]
    gsm8kp = GSM8KPost()
    _, processed_correct_answer = gsm8kp([], correct_answer)
    return {
        "input": text,
        "output": correct_answer,
        "processed_output": processed_correct_answer,
        }
    