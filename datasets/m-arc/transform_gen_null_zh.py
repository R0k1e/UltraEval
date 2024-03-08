
import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    options = list(data["target_scores"].keys())
    text = ""
    for idx, option in enumerate(options):
        text += f"{chr(65+idx)}. {option}\n"
    text = "问题：\n" + data["question"] + "\n" + "要求：\n选择并回答正确答案的字母。你只需要给出选项字母即可。\n" + "选项：\n" + text 
    text = f"""{text}""" + "答案：\n"
    index_of_correct_answer = list(data["target_scores"].values()).index(1)
    correct_answer = chr(65 + index_of_correct_answer)
    return {"input": text, "output": correct_answer, "processed_output": correct_answer}
    