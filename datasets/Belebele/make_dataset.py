import json
import os


def main():
    in_files = os.listdir('./RawData/Belebele')
    os.makedirs('./data', exist_ok=True)
    languages = ['jpn_Jpan', "rus_Cyrl", 'spa_Latn', 'zho_Hans', 'fra_Latn', "eng_Latn"]
    for file in in_files:
        if all([lang not in file for lang in languages]):
            continue
        with open('../../RawData/Belebele/' + file, 'r', encoding='utf-8') as f:
            data = [json.loads(line) for line in f.readlines()]
            result = []
            for d in data:
                newd = {}
                newd['passage'] = d['flores_passage']
                newd['question'] = d['question']
                newd['target_scores'] = {}
                correct_num = int(d['correct_answer_num'])
                newd['target_scores'][d['mc_answer1']] = int(correct_num == 1)
                if d['mc_answer2'] not in newd['target_scores']:
                    newd['target_scores'][d['mc_answer2']] = int(correct_num == 2)
                if d['mc_answer3'] not in newd['target_scores']:
                    newd['target_scores'][d['mc_answer3']] = int(correct_num == 3)
                if d['mc_answer4'] not in newd['target_scores']:
                    newd['target_scores'][d['mc_answer4']] = int(correct_num == 4)
                newd['answer'] = ""
                try:
                    index_of_correct_answer = list(newd["target_scores"].values()).index(1)
                except:
                    continue
                result.append(newd)
            with open(os.path.join('./data', file), 'w', encoding='utf-8') as f:
                for d in result:
                    json.dump(d, f, ensure_ascii=False)
                    f.write('\n')
            
                


if __name__ == "__main__":
    main()