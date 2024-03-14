
import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = f"المقدمة: \"{data['passage'][0]}\"\nالفرضية: \"{data['passage'][1]}\"\nما هو العلاقة بين هذين البيانين؟\nA. تناقض\nB. محايد\nC. استنتاج\nالرجاء الاختيار من بين \"A\", \"B\", \"C\".\nالإجابة: \n"
    index_of_correct_answer = list(data["target_scores"].values()).index(1)
    answers = ["A", "B", "C"]
    correct_answer = answers[index_of_correct_answer]

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}

    