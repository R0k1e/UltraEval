import os
import json
import argparse


# parameters below are for the old version
test_list = ["humaneval", "m-arc", "m-hellaswag", "m-mmlu", "mgsm", "omgeval"]
model_list = ["minicpm"]#"bloom", "chimera-13b", "guanaco-7b", "guanaco-13b", "okapi", "phoenix-7b", "polyalpaca", "polychat"]

# should be configured
language_list = ["en","es","ru","zh","fr"]#, "es", "fr", "ru", "zh"]
result_directory = './result/'

# specify an output path
output_file = './merged_results.jsonl'
parser = argparse.ArgumentParser()
parser.add_argument('--target', type=str, default="auto", help='the target directory containing results')
args = parser.parse_args()


# old one, not be compatible with the new version of path yet
def merge_auto():
    merged_results=[]
    for test in test_list:
        test_path = os.path.join(result_directory, test)
        print(test_path)

        for model in model_list:
            model_path = os.path.join(test_path, model)
            print(model_path)

            time_dirs = [dir for dir in os.listdir(model_path)]
            
            # Sort by last modified time
            # CAUTION: No modification of result files after creation! Only if you know the meaning of modification.
            time_dirs.sort(key=lambda x: os.path.getmtime(os.path.join(model_path, x)), reverse=True)
            
            languages=language_list.copy()
            for time_dir in time_dirs:
                time_dir=os.path.join(model_path, time_dir)
                lang_file=[res_dir for res_dir in os.listdir(time_dir) if os.path.isdir(os.path.join(time_dir,res_dir))][0]
                print(lang_file)
                lang_id=lang_file.split("_")[1].split("-")[-1]
                print(lang_id)
                # fix bug: continuous same languages
                if lang_id not in languages:
                    continue
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

    with open(output_file, 'w') as f:
        for result in merged_results:
            f.write(json.dumps(result) + '\n')


# specify a path(under result and above time are all acceptable)
# Eg ././result/testset, ./result/testset/model , ./result/testset/model/config_tag , ./result/testset/model/config_tag/model_tag
# all are valid
def merge_results(target: str):
    merged_results=[]
    test=""
    model=""
    max_depth=4
    depth_ret=0
    model_paths=[]
    abs_path=os.path.abspath(target)   

    for i,item in enumerate(abs_path.split("/")):
        if item == "result":
            test = abs_path[i+1]
            depth_ret = i+1
            
    
    for root, dirs, files in os.walk(abs_path):
        for dir in dirs:
            abs_dir=os.path.join(root, dir)
            if len(abs_dir.split("/"))-depth_ret == max_depth:
                model=abs_dir.split("/")[-3]
                model_paths.append(abs_dir)


    for model_path in model_paths:   
        time_dirs = [dir for dir in os.listdir(model_path)]
                
        # Sort by last modified time
        # CAUTION: No modification of result files after creation! Only if you know the meaning of modification.
        time_dirs.sort(key=lambda x: os.path.getmtime(os.path.join(model_path, x)), reverse=True)

        languages=language_list.copy()
        for time_dir in time_dirs:
            time_dir=os.path.join(model_path, time_dir)
            lang_file=[res_dir for res_dir in os.listdir(time_dir) if os.path.isdir(os.path.join(time_dir,res_dir))][0]
            lang_id=lang_file.split("_")[1].split("-")[-1]
            
            if lang_id not in languages:
                continue
            languages.remove(lang_id)
            if test == "humaneval":
                real_path = os.path.join(time_dir,lang_file, 'results.txt')
            if test == "omgeval":
                real_path = os.path.join(time_dir,lang_file, "alpaca_eval_gpt4_" + lang_id + "/leaderboard.csv")
            file_path = os.path.join(time_dir, '_all_results.json')
            print(file_path)
            
            with open(file_path, 'r') as f:
                data = json.load(f)
                data["model_path"]=model_path
                data['model']=model
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
        
    with open(output_file, 'a') as f:
        for result in merged_results:
            f.write(json.dumps(result) + '\n')
    

if __name__=="__main__":

    with open(output_file, 'w') as f:
        pass

    if args.target == "auto":
        merge_auto()
    else:
        targets = args.target.split(',')
        for target in targets:
            merge_results(target)