import json
import os

languages={'zh': 'Chinese', 'en': 'English', 'es': 'Spanish', 'ru': 'Russia', 'fr': 'French'}
lang_list=['zh','en','es','ru','fr']
model_list=['minicpm']


def get_Acc(file_path,local_file_path):
    cnt_local=0
    wins_local=0
    wins_all=0
    win=0
    with open(local_file_path, 'r') as local_file:
        all_local=local_file.read().splitlines()
        with open(file_path, 'r') as file:
            data = json.load(file)
            for item in data:
                win=0
                if item["raw_completion"] is None:
                    continue
                if r"{'model': 'model_2', 'rank': 1}" in item["raw_completion"]:
                    win=1
                    wins_all +=1
                if item["instruction"].strip() in all_local:
                    cnt_local+=1
                    if win == 1:
                        wins_local+=1
                        # print(item["instruction"])
                        # print("===")

    acc_local=wins_local/cnt_local
    acc_all=wins_all/len(data)     
    acc_non_local=(wins_all-wins_local)/(len(data)-cnt_local)
    print("local:")       
    print("acc: ",acc_local,"win: ", wins_local,"total: ",cnt_local)
    print("non_local:")
    print("acc: ",acc_non_local,"win: ",wins_all-wins_local,"total: ",len(data)-cnt_local)
    print("all:")
    print("all:","acc: ",acc_all,"win: ",wins_all,"total: ",len(data))

# No local version for English
def get_Acc_en(file_path):
    wins_all=0

    with open(file_path, 'r') as file:
        data = json.load(file)
        for item in data:
            if r"{'model': 'model_2', 'rank': 1}" in item["raw_completion"]:
                wins_all +=1

    acc_all=wins_all/len(data)    
    print("all:")        
    print("acc: ",acc_all,"win: ",wins_all,"total: ",len(data))


def main():
    for model in model_list:
        print("model:",model)
        file_path = './result/omgeval/' + model
        time_dirs=os.listdir(file_path)
        for time_dir in time_dirs:
            time_path= os.path.join(file_path,time_dir)
            result_files=os.listdir(time_path)
            for result_file in result_files:
                #print("result_file:",result_file)
                if os.path.isdir(os.path.join(time_path,result_file)):
                    lang_id=result_file.split('_')[1][-2:]
                    if lang_id in lang_list:
                        print("lang_id:",lang_id)
                        final_path = os.path.join(time_path,result_file)+"/alpaca_eval_gpt4_"+lang_id+"/annotations.json"
                        #print("final_path:",final_path)

                        local_file_path = "../OMGEval/data/OMGEval_"+languages[lang_id]+"_local.txt"
                        if lang_id == 'en':
                            get_Acc_en(final_path)
                        else :
                            get_Acc(final_path,local_file_path)


if __name__=="__main__":
    main()