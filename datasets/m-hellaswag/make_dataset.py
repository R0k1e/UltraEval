import json
import os
import pdb


def transform_entry(data_entry):
    return {
        "passage": "",
        "question": data_entry["ctx"],
        "target_scores": {
            choice: int(idx == data_entry["label"])
            for idx, choice in enumerate(data_entry["endings"])
        },
        "answer": "",
    }


def convert(input_file_path, output_file_path):
    with open(input_file_path, "r", encoding="utf-8") as infile, open(
        output_file_path, "w", encoding="utf-8"
    ) as outfile:
        for line in infile:
            data_entry = json.loads(line.strip())
            transformed_entry = transform_entry(data_entry)
            outfile.write(json.dumps(transformed_entry, ensure_ascii=False) + "\n")


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    input_dir = "../../ultraeval_format_multi_language_datasets/m_hellaswag"
    for dirpath, dirnames, filenames in os.walk(input_dir):
        for file in filenames:
            input_file_path = os.path.join(input_dir, file)
            output_file_path = os.path.join("./datasets/m-hellaswag/data", file)
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
            convert(input_file_path, output_file_path)


if __name__ == "__main__":
    main()
