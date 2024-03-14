
import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = f"Dhana: \"{data['passage'][0]}\"\nHypothesis: \"{data['passage'][1]}\"\nUhusiano kati ya kauli hizi mbili ni upi?\nA. mgongano\nB. kati\nC. utekelezaji\nTafadhali chagua kati ya \"A\", \"B\", \"C\".\nJibu: "
    index_of_correct_answer = list(data["target_scores"].values()).index(1)
    answers = ["A", "B", "C"]
    correct_answer = answers[index_of_correct_answer]

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}

    