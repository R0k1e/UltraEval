import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    instruction = "Given the following passage, query, and answer choices, output the letter corresponding to the correct answer.\n"
    options = list(data["target_scores"].keys())
    text = f"###\nPassage:\n{data['passage']}\n"
    text += f"###\nQuery:\n{data['question']}\n"
    text += f"###\nChoices:\n"
    for idx, option in enumerate(options):
        text += f"({chr(65+idx)}) {option}\n "
    text += "###\nAnswer:\n"
    try:
        index_of_correct_answer = list(data["target_scores"].values()).index(1)
    except:
        print(data)
        exit()
    correct_answer = f"({chr(65 + index_of_correct_answer)})"
    return {"input": text, "output": correct_answer, "processed_output": correct_answer}
