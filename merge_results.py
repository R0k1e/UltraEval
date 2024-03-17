import os
import json

result_directory = './result/'
merged_results = []
test_list = ["m-arc", "m-hellaswag", "m-mmlu"]
model_list = ["bloom", "chimera-13b", "guanaco-7b", "guanaco-13b", "okapi", "phoenix-7b", "polyalpaca", "polychat"]


for test in test_list:
    test_path = os.path.join(result_directory, test)
    print(test_path)

    for model in model_list:
        model_path = os.path.join(test_path, model)
        print(model_path)

        time_dir = [dir for dir in os.listdir(model_path)]
        
        time_dir.sort(key=lambda x: os.path.getmtime(os.path.join(model_path, x)), reverse=True)
        
        last_5_time_dir = time_dir[:5]
        
        for dir in last_5_time_dir:
            file_path = os.path.join(model_path, dir, '_all_results.json')
            print(file_path)
            
            with open(file_path, 'r') as f:
                data = json.load(f)
                merged_results.append(data)

output_file = './merged_results.jsonl'

with open(output_file, 'w') as f:
    for result in merged_results:
        f.write(json.dumps(result) + '\n')