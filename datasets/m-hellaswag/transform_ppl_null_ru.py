
import random    
        
def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = f"{text}"
    correct_answer = [
        key for key, value in data["target_scores"].items() if value == 1
    ]
    try:
        correct_answer = correct_answer[0].strip()
    except Exception:
        correct_answer = ""

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}
    