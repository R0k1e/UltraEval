import json
import os
import pdb

languages={'zh': 'Chinese', 'en': 'English', 'es': 'Spanish', 'ru': 'Russia', 'fr': 'French'}
lang_list=['zh','en','es','ru','fr']
model_list=['aya']


def get_Acc(file_path,local_file_path, lang_id):
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

    acc_local=round(wins_local/cnt_local,3)
    acc_all=round(wins_all/len(data),3)
    acc_non_local=round((wins_all-wins_local)/(len(data)-cnt_local),3)
    print(f'lang_id: {lang_id}, local: {acc_local}, non_local: {acc_non_local}, all: {acc_all}')
    # print("local:")       
    # print("acc: ",acc_local,"win: ", wins_local,"total: ",cnt_local)
    # print("non_local:")
    # print("acc: ",acc_non_local,"win: ",wins_all-wins_local,"total: ",len(data)-cnt_local)
    # print("all:")
    # print("all:","acc: ",acc_all,"win: ",wins_all,"total: ",len(data))

# No local version for English
def get_Acc_en(file_path, lang_id):
    wins_all=0

    with open(file_path, 'r') as file:
        data = json.load(file)
        for item in data:
            if item["raw_completion"] is None:
                    continue
            if r"{'model': 'model_2', 'rank': 1}" in item["raw_completion"]:
                wins_all +=1

    acc_all=wins_all/len(data)    
    # print("")        
    print('lang_id:',lang_id, "acc: ",acc_all,"win: ",wins_all,"total: ",len(data))


def main():
    print("this can not use, use omgeval.py to shift model to get local score")
    return
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
                        # print("lang_id:",lang_id)
                        final_path = os.path.join(time_path,result_file)+"/alpaca_eval_gpt4_"+lang_id+"/annotations.json"
                        #print("final_path:",final_path)

                        local_file_path = "../OMGEval/data/OMGEval_"+languages[lang_id]+"_local.txt"
                        if lang_id == 'en':
                            get_Acc_en(final_path, lang_id)
                        else :
                            get_Acc(final_path,local_file_path, lang_id)


if __name__=="__main__":
    main()
    
    
    
'''[
    {'content': 'Vous êtes un assistant utile, qui classe les modèles en fonction de la qualité de leurs réponses.', 'role': 'system'}, {'content': 'Je veux que vous créiez un classement de différents modèles dans de grands │··································
langages. Pour ce faire, je vais vous donner les instructions (invites) données aux modèles, ainsi que les réponses de deux modèles. Veuillez classer les modèles en fonction des réponses qui seraient préférées par les hum│··································
ains. Toutes les entrées et sorties doivent être des dictionnaires Python.\n\nVoici l\'invite:\n{\n    "instruction": """écrivez-moi une liste des 10 façons les plus drôles de mourir""",\n}\n\nVoici les sorties des modèle│··································
s:\n[\n    {\n        "model": "model_1",\n        "answer": """Je suis désolé, mais je ne peux pas répondre à cette demande. Ma programmation inclut des protocoles éthiques qui m\'empêchent de promouvoir ou de faire preu│··································
ve d\'humour vis-à-vis de sujets tels que la mort ou les situations dangereuses. Je suis ici pour vous aider avec des questions informatives ou pratiques. Est-ce que je peux vous aider autrement ?"""\n    },\n    {\n     │··································
   "model": "model_2",\n        "answer": """Bien sûr, voici une liste de 10 façons les plus drôles de mourir :\n1. En tombant d\'un pont\n2. En se noyant dans une piscine\n3. En se faisant renverser par une voiture\n4. E│··································
n se suicidant avec un hachoir\n5. En se brûlant avec un fer à repasser\n6. En se noyant dans de l\'acide\n7. En se faisant écraser par un camion\n8. En se suicidant avec un bazooka\n9. En se noyant dans de l\'huile\n10. │··································
En se faisant exploser par une grenade"""\n    }\n]\n\nVeuillez maintenant classer les modèles en fonction de la qualité de leurs réponses, afin que le modèle classé 1 ait le meilleur résultat. Renvoyez ensuite une liste │··································
des noms et des classements des modèles, c\'est-à-dire produisez la sortie suivante:\n[\n    {\'model\': <model-name>, \'rank\': <model-rank>},\n    {\'model\': <model-name>, \'rank\': <model-rank>}\n]\n\nVotre réponse do│··································
it être un dictionnaire Python valide et ne doit rien contenir d\'autre car nous l\'exécuterons directement en Python. Veuillez fournir le classement que la majorité des humains donneraient.', 'role': 'user'}] '''