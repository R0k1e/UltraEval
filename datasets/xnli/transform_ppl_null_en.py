
import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = f"premise:\"{data['passage'][0]}\"\nhypothesis:\"{data['passage'][1]}\"\nWhat is the relationship between these two statements?\nA. contradiction\nB. neutral\nC. entailment\nPlease choose from \"A\", \"B\", \"C\".\nAnswer: \n"
    index_of_correct_answer = list(data["target_scores"].values()).index(1)
    answers = ["A", "B", "C"]
    correct_answer = answers[index_of_correct_answer]

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}

    