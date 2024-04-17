import os
import sys
import time
import subprocess
import argparse

ckpt_path = "/home/wanghaoyu/MiniCPM/finetune/MiniCPM-2B-history/ru_all/42_14_5e-5_100_1278_0.01/20240331111234"
gpu_list = [0, 1, 2, 3]
base_port = 6325
model_type = "minicpm-raw"
test_list = 'humaneval'
languages = 'ru'

parser = argparse.ArgumentParser()
parser.add_argument("--gpu_id", type=str, help="gpu id to use")
parser.add_argument("--port", type=int, help="port to use")
parser.add_argument("--model_type", type=str, help="model list to use")
parser.add_argument("--test_list", type=str, help="test list to use")
parser.add_argument("--languages", type=str, help="languages to use")
parser.add_argument("--model_path", type=str, default=None, help="model path to use")
args = parser.parse_args()

if __name__ == "__main__":
    gpu_list = args.gpu_id.split(",")
    base_port = args.port
    model_type = args.model_type
    test_list = args.test_list
    languages = args.languages
    ckpt_path = args.model_path
    
    ckpt_list = []
    for ckpt_dir in os.listdir(ckpt_path):
        if not ckpt_dir.endswith("-vllm"):
            continue
        ckpt_list.append(os.path.join(ckpt_path, ckpt_dir))
        
    process_list = {}
    for i, _ in enumerate(gpu_list):
        process_list[i] = None
    
    for id,ckpt in enumerate(ckpt_list):
        id = id % len(gpu_list)
        port_id = base_port + id
        gpu_id = gpu_list[id]
        config_tag= "-".join(ckpt_path.split("/")[-3:-1])
        p = subprocess.Popen(f"""
                python auto_test.py \
                    --gpu_id {gpu_id} \
                    --port {port_id} \
                    --model_list {model_type} \
                    --test_list {test_list} \
                    --languages {languages} \
                    --model_path {ckpt} \
                    --config_tag {config_tag} \
                        """, 
                shell=True)
        
        while process_list[id] is not None:
            if process_list[id].poll() is not None:
                process_list[id] = None
                break
            time.sleep(10)
        process_list[id] = p
        seconds = 30
        print(f"Process {id} started with ckpt {ckpt}")
        print(f"sleep {seconds} seconds before next process")
        time.sleep(seconds)