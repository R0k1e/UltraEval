import json
import os

def main():
    in_files = os.listdir('./RawData/mkqa')
    os.makedirs('./data', exist_ok=True)
    languages = ['ja', "ru", 'es', 'zh_cn', 'fr', "en"]
    results = {}
    for lan in languages:
        results[lan] = []
    for file in in_files:
        with open('./RawData/mkqa/' + file, 'r', encoding='utf-8') as f:
            data = [json.loads(line) for line in f.readlines()]
            for d in data:
                for lan in languages:   
                    newd = {}
                    newd['passage'] = [""]
                    newd['question'] = d['queries'][lan]
                    newd['target_scores'] = {}
                    try:
                        alias = d['answers'][lan][0]['aliases']
                    except:
                        alias = None
                    text = d['answers'][lan][0]['text']
                    if alias:
                        newd['answer'] = [text] + alias
                    else:
                        newd['answer'] = [text]
                    try:
                        assert newd["answer"] is not []
                    except:
                        continue
                    results[lan].append(newd)
                    
            for lan in languages:
                with open(os.path.join('./data', lan+'.jsonl'), 'w', encoding='utf-8') as f:
                    for d in results[lan]:
                        json.dump(d, f, ensure_ascii=False)
                        f.write('\n')
if __name__ == "__main__":
    main()