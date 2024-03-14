
import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = f"前提：\"{data['passage'][0]}\"\n假设：\"{data['passage'][1]}\"\n这两个陈述之间有什么关系？ \nA.矛盾\nB.中立\nC.蕴含\n请从\"A\"、\"B\"、\"C\"中选择。\n答案: \n"
    index_of_correct_answer = list(data["target_scores"].values()).index(1)
    answers = ["A", "B", "C"]
    correct_answer = answers[index_of_correct_answer]

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}

    