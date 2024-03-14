
import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = f"Öncül: \"{data['passage'][0]}\"\nHipotez: \"{data['passage'][1]}\"\nBu iki ifade arasındaki ilişki nedir?\nA. çelişki\nB. nötr\nC. çıkarım\nLütfen \"A\", \"B\", \"C\" arasından birini seçin.\nCevap: "
    index_of_correct_answer = list(data["target_scores"].values()).index(1)
    answers = ["A", "B", "C"]
    correct_answer = answers[index_of_correct_answer]

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}

    