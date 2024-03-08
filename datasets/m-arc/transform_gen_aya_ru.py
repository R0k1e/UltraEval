
import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    options = list(data["target_scores"].keys())
    text = ""
    for idx, option in enumerate(options):
        text += f"{chr(65+idx)}. {option}\n"
    text = "Вопрос:\n" + data["question"] + "\n" + "Требование:\nВыберите и ответьте на правильный вариант.\n" + "Варианты:\n" + text + "Ответ:\n"
    text = f"""{text}"""
    index_of_correct_answer = list(data["target_scores"].values()).index(1)
    correct_answer = chr(65 + index_of_correct_answer)
    #俄语字母和英语字母长得一样，实际不同，aya-101需要改这里
    if correct_answer == "A":
        correct_answer = "А"
    elif correct_answer == "B":
        correct_answer = "Б"
    elif correct_answer == "C":
        correct_answer = "В"
    elif correct_answer == "D":
        correct_answer = "Д"
    return {"input": text, "output": correct_answer, "processed_output": correct_answer}
    