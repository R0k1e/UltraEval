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
parser.add_argument("--gpu_id", type=int, default=0, help="gpu id to use")
parser.add_argument("--port", type=int, default=6325, help="port to use")
parser.add_argument("--model_type", type=str, default="minicpm-raw", help="model list to use")
parser.add_argument("--test_list", type=str, default="humaneval", help="test list to use")
parser.add_argument("--languages", type=str, default="ru", help="languages to use")
parser.add_argument("--model_path", type=str, default=None, help="model path to use")
args = parser.parse_args()
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
for i in gpu_list:
    process_list[i] = None

for id,ckpt in enumerate(ckpt_list):
    id = id % len(gpu_list)
    port_id = base_port + id
    gpu_id = gpu_list[id]
    config_tag= ckpt_path.split("/")[-2]
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
        time.sleep(30)
    process_list[id] = p
    print(f"Process {id} started with ckpt {ckpt}")
    print("sleep 90 seconds before next process")
    time.sleep(90)