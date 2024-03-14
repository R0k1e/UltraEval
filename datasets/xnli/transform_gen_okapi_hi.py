
import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = f"प्रस्तावना: \"{data['passage'][0]}\"\nपरिकल्पना: \"{data['passage'][1]}\"\nइन दो कथनों के बीच का संबंध क्या है?\nA. विरोध\nB. तटस्थ\nC. अनुमान\nकृपया \"A\", \"B\", \"C\" में से चुनें।\nउत्तर: "
    index_of_correct_answer = list(data["target_scores"].values()).index(1)
    answers = ["A", "B", "C"]
    correct_answer = answers[index_of_correct_answer]

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}

    