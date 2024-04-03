
import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    options = list(data["target_scores"].keys())
    text = ""
    for idx, option in enumerate(options):
        text += f"{chr(65+idx)}. {option}\n"
    text = "Вопрос:\n" + data["question"] + "\n" + "Требование:\nВыберите и ответьте на букву правильного ответа.\n" +"Пожалуйста, поместите выбранный вариант в начало ответа.\n"+ "Варианты:\n" + text 
    prompt = text
    text = f"""<用户>{prompt}<AI>""" + "Ответ:\n"
    index_of_correct_answer = list(data["target_scores"].values()).index(1)
    correct_answer = chr(65 + index_of_correct_answer)
    #一个俄语字母，一个英语字母
    if correct_answer == "A":
        correct_answer = ["A","А"]
    elif correct_answer == "B":
        correct_answer = ["B","Б"]
    elif correct_answer == "C":
        correct_answer = ["C","В","С"]
    elif correct_answer == "D":
        correct_answer = ["D","Д"]
    return {"input": text, "output": correct_answer, "processed_output": correct_answer}
    