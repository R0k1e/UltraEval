
import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    options = ""
    for idx, item in enumerate(data["target_scores"].keys()):
        options += f"({chr(65 + idx)}) {item}\n"
    text = f"Contexto:\n {data['question']}\nPregunta:\n¿Qué final tiene más sentido?\nRequisito:\nElige y responde con la letra de la respuesta correcta, incluyendo el paréntesis.\nOpciones:\n" + options
    text = f"""{text}""" + "Respuesta:\n"
    index_of_correct_answer = list(data["target_scores"].values()).index(1)
    correct_answer = chr(65 + index_of_correct_answer)
    if correct_answer == "A":
        correct_answer = ["A","А"]
    elif correct_answer == "B":
        correct_answer = ["B","Б"]
    elif correct_answer == "C":
        correct_answer = ["C","В","С"]
    elif correct_answer == "D":
        correct_answer = ["D","Д"]
    new = []

    for c in correct_answer:
        new.append(f'({c})')
    correct_answer = new
    processed_correct_answer = correct_answer
    return {
        "input": text,
        "output": correct_answer,
        "processed_output": processed_correct_answer,
    }

    