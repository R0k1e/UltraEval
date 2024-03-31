import json
import os
import subprocess
import argparse
import sys

def omg_eval(models, languages, mode='all'):
    instance_path = "./result/omgeval"
    for model in os.listdir(instance_path):
        if model not in models:
            continue
        cur_path = os.path.join(instance_path, model)
        for exec_date in os.listdir(cur_path):
            cur_path = os.path.join(instance_path, model, exec_date)
            for task_name in os.listdir(cur_path):
                cur_path = os.path.join(instance_path, model, exec_date, task_name)
                if 'omgeval' not in task_name:
                        continue
                lang = task_name.split('_')[1].split('-')[-1]
                if lang not in languages:
                    continue
                for file in os.listdir(cur_path):
                    input_file_path = os.path.join(cur_path, 'instance.jsonl')
                    output_file_path = os.path.join(cur_path, 'processed.json')
                    print(f"Processing {input_file_path}...")
    
                    # 读取 JSONL 文件，并提取所需字段
                    all_data = []
                    with open(input_file_path, 'r', encoding='utf-8') as input_file:
                    
                        for line in input_file:
                            # 解析 JSONL 行
                            data = json.loads(line)
    
                            # 提取 'question' 和 'raw_outputs' 字段
                            extracted_data ={}
                            extracted_data["instruction"] = data['data']['question']
                            extracted_data["output"] = data['raw_outputs'][0] if data['raw_outputs'] else ""
                            extracted_data["generator"] = model
                            all_data.append(extracted_data)
                            #print(all_data)
    
    
    
                    with open(output_file_path, 'w', encoding='utf-8') as file:
                        json.dump(all_data, file, ensure_ascii=False, indent=4)
    
                    print(f"Processed data has been written to {output_file_path}")
                    break
                    
                model_outputs = output_file_path
                annotators_config = "alpaca_eval_gpt4_" + lang
                # reference_outputs = "/home/wanghaoyu/alpaca_eval/baseline/gpt-3.5-turbo-0301/" + lang + ".json"
                if mode == 'all':
                    reference_outputs = "../alpaca_eval/baseline/gpt-3.5-turbo-0613/" + lang + ".json"
                elif mode == 'local':
                    reference_outputs = "../alpaca_eval/baseline/local/gpt3.5-turbo-" + lang + ".json"
                elif mode == 'global':
                    reference_outputs = "../alpaca_eval/baseline/global/" + lang + ".json"
    
    
                os.system("alpaca_eval --model_outputs " + model_outputs + " --annotators_config " + annotators_config + " --reference_outputs " + reference_outputs)
    
    
    
    
if __name__ == '__main__':
    models = ['chimera-13b', 'guanaco-7b', 'guanaco-13b', 'phoenix-7b', 'omg-lm', 'aya', 'aya-101']
    # models = ['chimera-13b']
    languages = ['en','zh','es','ru','fr', 'ar']
    # languages = ['en','zh','es','ru','fr']
    
    mode = 'all'
    # mode = 'local'
    # mode = 'global'
    
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--models', type=str, default=models)
    # parser.add_argument('--languages', type=str, default=languages)
    # args = parser.parse_args()
    
    # models = args.models.split(',')
    # languages = args.languages.split(',')
    
    omg_eval(models, languages, mode)