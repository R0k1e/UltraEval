
import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = f"Premisa: \"{data['passage'][0]}\"\nHipótesis: \"{data['passage'][1]}\"\n¿Cuál es la relación entre estas dos declaraciones?\nA. contradicción\nB. neutral\nC. implicación\nPor favor, elija entre \"A\", \"B\", \"C\".\nRespuesta: "
    index_of_correct_answer = list(data["target_scores"].values()).index(1)
    answers = ["A", "B", "C"]
    correct_answer = answers[index_of_correct_answer]

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}

    