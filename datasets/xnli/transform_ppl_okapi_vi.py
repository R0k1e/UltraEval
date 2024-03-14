
import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = f"Tiền đề: \"{data['passage'][0]}\"\nGiả thuyết: \"{data['passage'][1]}\"\nMối quan hệ giữa hai phát biểu này là gì?\nA. mâu thuẫn\nB. trung lập\nC. suy luận\nVui lòng chọn từ \"A\", \"B\", \"C\".\nCâu trả lời: "
    index_of_correct_answer = list(data["target_scores"].values()).index(1)
    answers = ["A", "B", "C"]
    correct_answer = answers[index_of_correct_answer]

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}

    