
import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = f"Предпоставка: \"{data['passage'][0]}\"\nХипотеза: \"{data['passage'][1]}\"\nКаква е връзката между тези две твърдения?\nA. противоречие\nB. неутрално\nC. извод\nМоля, изберете от \"A\", \"B\", \"C\".\nОтговор: "
    index_of_correct_answer = list(data["target_scores"].values()).index(1)
    answers = ["A", "B", "C"]
    correct_answer = answers[index_of_correct_answer]

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}

    