import os
import json


arc_c = "/home/wanghaoyu/UltraEval/RawData/arc-c/ARC-Challenge-Test.jsonl"
arc_e = "/home/wanghaoyu/UltraEval/RawData/arc-c/ARC-Easy-Test.jsonl"
arc = "/home/wanghaoyu/UltraEval/RawData/arc_selected/ARC-Test.jsonl"
m_arc = "/home/wanghaoyu/UltraEval/ultraeval_format_multi_language_datasets/m_hellaswag/zh_validation.json"

os.makedirs(arc, exist_ok=True)

m_data = json.load(open(m_arc, 'r'))
data = json.load(open(arc_c, 'r'))
new_data = []
for d in data:
    if d['id'] in m_data:
        new_data.append(d)
data = json.load(open(arc_e, 'r'))
for d in data:
    if d['id'] in m_data:
        new_data.append(d)
with open(arc, 'w') as f:
    for j in new_data:
        json.dump(j, f)