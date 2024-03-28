import os
import json

result_directory = './result/'
merged_results = []
test_list = ["humaneval", "m-arc", "m-hellaswag", "m-mmlu", "mgsm", "omgeval"]
model_list = ["minicpm"]#"bloom", "chimera-13b", "guanaco-7b", "guanaco-13b", "okapi", "phoenix-7b", "polyalpaca", "polychat"]
language_list = ["en","es","ru","zh","fr"]#, "es", "fr", "ru", "zh"]

def merge_results():
    for test in test_list:
        test_path = os.path.join(result_directory, test)
        print(test_path)

        for model in model_list:
            model_path = os.path.join(test_path, model)
            print(model_path)

            time_dirs = [dir for dir in os.listdir(model_path)]
            
            # Sort by last modified time
            # CAUTION: No modification of result files after creation!
            time_dirs.sort(key=lambda x: os.path.getmtime(os.path.join(model_path, x)), reverse=True)
            
            languages=language_list.copy()
            for time_dir in time_dirs:
                time_dir=os.path.join(model_path, time_dir)
                lang_file=[res_dir for res_dir in os.listdir(time_dir) if os.path.isdir(os.path.join(time_dir,res_dir))][0]
                print(lang_file)
                lang_id=lang_file.split("_")[1].split("-")[-1]
                print(lang_id)
                languages.remove(lang_id)
                if test == "humaneval":
                    real_path = os.path.join(time_dir,lang_file, 'results.txt')
                if test == "omgeval":
                    real_path = os.path.join(time_dir,lang_file, "alpaca_eval_gpt4_" + lang_id + "/leaderboard.csv")
                file_path = os.path.join(time_dir, '_all_results.json')
                print(file_path)
                
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    data["model"]=model
                    if test == "humaneval":
                        with open(real_path, 'r') as f:
                            lines = f.readlines()
                            data["processed_ac"] = lines[0]
                    if test == "omgeval":
                        with open(real_path, 'r') as f:
                            lines = f.readlines()
                            data["processed_ac"] = lines[1].split(",")[1]
                    merged_results.append(data)
                
                if len(languages)==0:
                    break
    
    # specify an output path
    output_file = './merged_results4.jsonl'

    with open(output_file, 'w') as f:
        for result in merged_results:
            f.write(json.dumps(result) + '\n')

    
if __name__=="__main__":
    merge_results()