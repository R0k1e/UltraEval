
import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = f"Предпосылка: \"{data['passage'][0]}\"\nГипотеза: \"{data['passage'][1]}\"\nКакова взаимосвязь между этими двумя утверждениями?\nA. противоречие\nB. нейтральность\nC. следствие\nПожалуйста, выберите из \"A\", \"B\", \"C\".\nОтвет: "
    index_of_correct_answer = list(data["target_scores"].values()).index(1)
    answers = ["A", "B", "C"]
    correct_answer = answers[index_of_correct_answer]

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}

    