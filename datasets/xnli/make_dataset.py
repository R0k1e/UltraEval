import json
import os


def transform_entry(data_entry, vocab):
    #0: entailment, 1: neutral, 2: contradiction
    target_scores = {
        vocab["contradiction"]: int(data_entry["label"] == 2),
        vocab["neutral"]: int(data_entry["label"] == 1),
        vocab["entailment"]: int(data_entry["label"] == 0),
    }
    
    return {
        "passage": [data_entry["premise"], data_entry["hypothesis"]],
        "question": "",
        "target_scores": target_scores,
        "answer": "",
    }


def convert(input_file_path, output_file_path, vocab):
    with open(input_file_path, "r", encoding="utf-8") as infile, open(
        output_file_path, "w", encoding="utf-8"
    ) as outfile:
        for line in infile:
            data_entry = json.loads(line.strip())
            transformed_entry = transform_entry(data_entry, vocab)
            if transformed_entry:
                outfile.write(json.dumps(transformed_entry, ensure_ascii=False) + "\n")


def get_vocab(lang):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(script_dir, "vocab.jsonl"), "r", encoding="utf-8") as vocab_file:
        for line in vocab_file:
            data_entry = json.loads(line.strip())
            if data_entry["lang"] == lang:
                return {
                    "contradiction": data_entry["contradiction"],
                    "neutral": data_entry["neutral"],
                    "entailment": data_entry["entailment"]
                }
    return None


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    input_dir = "../../RawData/xnli/"
    output_path="./data/"
    for dir, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".jsonl"):
                lang = file[:2]
                print(lang)
                vocab = get_vocab(lang)
                input_file_path = os.path.join(dir, file)
                output_file_path = os.path.join(output_path, file)
                os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
                convert(input_file_path, output_file_path, vocab)

    
if __name__ == "__main__":
    main()
