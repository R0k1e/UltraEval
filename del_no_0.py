{"passage": "", "question": "水在哪种物态下有确定的形状和体积？", "target_scores": {"气体": 0, "液体": 0, "固体": 1}, "answer": ""}

import json
import os

input_dir = "/home/wanghaoyu/UltraEval/datasets/m-hellaswag/data"
for file in os.listdir(input_dir):
    if file.endswith(".json"):
        saved_data = []
        with open(os.path.join(input_dir, file), "r", encoding="utf-8") as f:
            for line in f:
                data = json.loads(line)
                target_scores = data["target_scores"]
                if any(score == 1 for score in target_scores.values()):
                    saved_data.append(data)
        with open(os.path.join(input_dir, file), "w", encoding="utf-8") as f:
            for data in saved_data:
                f.write(json.dumps(data, ensure_ascii=False) + "\n")