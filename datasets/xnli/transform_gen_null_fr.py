
import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = f"Prémisse : \"{data['passage'][0]}\"\nHypothèse : \"{data['passage'][1]}\"\nQuelle est la relation entre ces deux énoncés ?\nA. contradiction\nB. neutre\nC. implication\nVeuillez choisir parmi \"A\", \"B\", \"C\".\nRéponse : "
    index_of_correct_answer = list(data["target_scores"].values()).index(1)
    answers = ["A", "B", "C"]
    correct_answer = answers[index_of_correct_answer]

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}

    