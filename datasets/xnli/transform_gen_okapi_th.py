
import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = f"ข้อตั้ง: \"{data['passage'][0]}\"\nสมมติฐาน: \"{data['passage'][1]}\"\nความสัมพันธ์ระหว่างสองข้อความนี้คืออะไร?\nA. ขัดแย้ง\nB. กลาง\nC. สัมพันธ์\nโปรดเลือกจาก \"A\", \"B\", \"C\".\nคำตอบ: "
    index_of_correct_answer = list(data["target_scores"].values()).index(1)
    answers = ["A", "B", "C"]
    correct_answer = answers[index_of_correct_answer]

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}

    