import json
import os
from human_eval.data import HUMAN_EVAL
from human_eval.evaluation import evaluate_functional_correctness


def entry_point(
    sample_file: str,
    k: str = "1,10,100",
    n_workers: int = 4,
    timeout: float = 3.0,
    problem_file: str = HUMAN_EVAL,
):
    """
    Evaluates the functional correctness of generated samples, and writes
    results to f"{sample_file}_results.jsonl.gz"
    """
    k = list(map(int, k.split(",")))
    results = evaluate_functional_correctness(sample_file, k, n_workers, timeout, problem_file)
    results_file = sample_file.replace("reform.jsonl", f"results.txt")
    print(f"Writing results to {results_file}")
    with open(results_file, "w") as f:
        f.write(str(results))
    
def reformat(input_file):
    with open(input_file, "r") as f:
        data = [json.loads(line) for line in f]

    new_data = []
    for instance in data:
        new_instance = {}
        new_instance["task_id"] = instance["data"]["task_id"]
        new_instance["completion"] = instance["processed_outputs"][0]
        new_instance["all_code"] = instance["raw_outputs"][0]
        new_data.append(new_instance)

    output_dir = os.path.dirname(input_file)
    output_file = os.path.join(output_dir, "reform.jsonl")
    with open(output_file, "w") as f:
        for instance in new_data:
            f.write(json.dumps(instance, ensure_ascii=False) + "\n")
    
    return output_file

def transform_humaneval(input_dir):
    dirs = os.listdir(input_dir)
    result_dict = {}
    for model in dirs:
        for dir in os.listdir(os.path.join(input_dir, model)):
            if os.path.isdir(os.path.join(input_dir, model, dir)):
                for subdir in os.listdir(os.path.join(input_dir, model, dir)):
                    if "humaneval" not in subdir:
                        continue
                    tag = subdir.split("_")[-2]
                    cur_dir = os.path.join(input_dir, model, dir, subdir)
                    if os.path.isdir(cur_dir):
                        if "results.txt" in os.listdir(cur_dir):
                            print(f"Skipping {subdir}")
                            continue
                        input_file = os.path.join(cur_dir, "instance.jsonl")
                        reformat_file = reformat(input_file)
                        if os.path.exists(reformat_file):
                            entry_point(reformat_file)
                            with open(os.path.join(cur_dir, "results.txt"), "r") as f:
                                result_dict[tag] = eval(f.read())['pass@1']
    return result_dict

if __name__ == "__main__":
    input_dir = "/home/wanghaoyu/UltraEval/result/humaneval"
    transform_humaneval(input_dir)
    