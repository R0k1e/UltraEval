
import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = f"Prämisse: \"{data['passage'][0]}\"\nHypothese: \"{data['passage'][1]}\"\nWas ist die Beziehung zwischen diesen beiden Aussagen?\nA. Widerspruch\nB. neutral\nC. Folgerung\nBitte wählen Sie zwischen \"A\", \"B\", \"C\".\nAntwort: "
    index_of_correct_answer = list(data["target_scores"].values()).index(1)
    answers = ["A", "B", "C"]
    correct_answer = answers[index_of_correct_answer]

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}

    