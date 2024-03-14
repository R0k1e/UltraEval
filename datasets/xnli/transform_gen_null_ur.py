
import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = f"مقدمہ: \"{data['passage'][0]}\"\nفرض: \"{data['passage'][1]}\"\nان دو بیانات کے درمیان تعلق کیا ہے؟\nA. تضاد\nB. غیر جانبدار\nC. استدلال\nبراہ کرم \"A\", \"B\", \"C\" میں سے ایک کا انتخاب کریں۔\nجواب: "
    index_of_correct_answer = list(data["target_scores"].values()).index(1)
    answers = ["A", "B", "C"]
    correct_answer = answers[index_of_correct_answer]

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}

    