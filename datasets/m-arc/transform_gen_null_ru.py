
import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    options = list(data["target_scores"].keys())
    text = ""
    for idx, option in enumerate(options):
        text += f"{chr(65+idx)}. {option}\n"
    text = "Вопрос:\n" + data["question"] + "\n" + "Требование:\nВыберите и ответьте на букву правильного ответа. Вам просто нужно указать буквы опций.\n" + "Варианты:\n" + text 
    text = f"""{text}""" + "Ответ:\n"
    index_of_correct_answer = list(data["target_scores"].values()).index(1)
    correct_answer = chr(65 + index_of_correct_answer)
    return {"input": text, "output": correct_answer, "processed_output": correct_answer}
    