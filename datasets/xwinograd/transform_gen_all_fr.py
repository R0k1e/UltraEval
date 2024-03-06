
import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    options = list(data["target_scores"].keys())
    textA, textB = options
    text = f"""Passage : {data['question']}\nLequel des énoncés suivants est une bonne phrase: \nA. {textA}\nB. {textB}\noptions: """
    index_of_correct_answer = list(data["target_scores"].values()).index(1)
    answers = ["A", "B"]
    correct_answer = answers[index_of_correct_answer]

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}
    