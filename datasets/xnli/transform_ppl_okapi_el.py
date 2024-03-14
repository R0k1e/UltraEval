
import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = f"Πρόταση: \"{data['passage'][0]}\"\nΥπόθεση: \"{data['passage'][1]}\"\nΠοια είναι η σχέση μεταξύ αυτών των δύο δηλώσεων;\nA. αντίφαση\nB. ουδέτερο\nC. συνέπεια\nΠαρακαλώ επιλέξτε από \"A\", \"B\", \"C\".\nΑπάντηση: "
    index_of_correct_answer = list(data["target_scores"].values()).index(1)
    answers = ["A", "B", "C"]
    correct_answer = answers[index_of_correct_answer]

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}

    