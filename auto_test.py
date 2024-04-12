import os
import subprocess
from transform_humaneval import transform_humaneval
from omgeval import omg_eval
import time
import signal
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--gpu_id', type=str, help='gpu id')
parser.add_argument('--port', type=int, help='port')
parser.add_argument('--model_list', type=str, help='model list')
# model_path: If not specified, use the default path. 
#             If specified, each model have to specify a path at its corresponding position.
parser.add_argument('--model_path', type=str, default="default", help='model path')
parser.add_argument('--test_list', type=str, help='test list')
parser.add_argument('--languages', type=str,  help='languages')
#config_tag: ${SEED}_${BATCH}_${LR}_${WARMUP}_${MAX_STEPS}_${WEIGHT_DECAY}
parser.add_argument('--config_tag', type=str, default="default", help='config tag')
args = parser.parse_args()




# languages = ['en', 'zh', 'es', 'ru', 'fr']
languages = args.languages.split(',')
# model_list = ['okapi', 'bloom', 'polyalpaca', 'polychat', 'guanaco', 'phoenix', "guanaco-13b", 'aya', 'aya-101', "UltraLink", 'minicpm']
model_list = args.model_list.split(',')
# test_list = ['humaneval', 'mgsm', 'omgeval', 'm-mmlu', 'belebele', 'xwinograd', 'm-arc', 'm-hellaswag']
model_path = args.model_path.split(',')
test_list = args.test_list.split(',')
port = args.port
gpu_id= args.gpu_id
print(f"gpu_id: {gpu_id}")
print(f"port: {port}")
print(f"model_list: {model_list}")
print(f"test_list: {test_list}")
print(f"languages: {languages}")
all_test_list = ['belebele','xwinograd']

template_dict = {
    'llama-7b': 'llama',
    'llama-13b': 'llama',
    'llama-70b': 'llama',
    'guanaco-13b': 'guanaco-13b',
    'guanaco-7b': 'guanaco',
    'phoenix-7b': 'phoenix',
    'chimera-13b': 'phoenix',
    'UltraLink': 'okapi',
    'aya': 'okapi',
    'aya-new': 'okapi',
    'aya-101': 'null',
    'aya-hf': 'okapi',
    'bloom': 'bloom',
    'okapi': 'okapi',
    'polyalpaca': 'polyalpaca',
    'polychat': 'polychat',
    'minicpm': "minicpm",
    'minicpm-raw': "minicpm",
}

default_model_path = {
    'UltraLink': "/data/public/wangshuo/UltraLink/models/UltraLink",
    'aya-101': "/data/public/wangshuo/UltraLink/models/aya-101",
    'aya-5lang': "/data/public/wangshuo/UltraLink/models/aya-5lang",
    'bloom': "/data/public/wangshuo/UltraLink/models/bloomz-7b1-mt",
    'okapi': "/data/public/wangshuo/UltraLink/models/okapi",
    'polychat': "/data/public/wangshuo/UltraLink/models/polylm-chat-13b",
    'polyalpaca': "/data/public/wangshuo/UltraLink/models/PolyLM-multialpaca-13b",
    'llama-7b': "/data/public/opensource_models/meta-llama/Llama-2-7b-chat-hf",
    'llama-13b': "/data/public/opensource_models/meta-llama/Llama-2-13b-hf",
    'llama-70b': "/data/public/opensource_models/meta-llama/Llama-2-70b-chat-hf",
    'phoenix-7b': "/data/public/wangshuo/UltraLink/models/phoenix-inst-chat-7b",
    'chimera-13b': "/data/public/wangshuo/UltraLink/models/chimera-inst-chat-13b",
    'guanaco-13b': "/data/public/wangshuo/UltraLink/models/guanaco-13b-hf",
    'guanaco-7b': "/data/public/wangshuo/UltraLink/models/Guanaco",
    'minicpm': "/data/public/wangshuo/UltraLink/models/MiniCPM-2B-sft-bf16-vllm",
    'minicpm-raw': "/data/public/wangshuo/UltraLink/models/MiniCPM-2B-history-vllm",
}

def auto_test(model):
    if model == 'aya-101':
        batch_size = 1
    else:
        batch_size = 128   
    print(f"batch_size: {batch_size}")
    model_tag = model_path[model].split('/')[-1]
    template_type = template_dict[model]
    config_tag = args.config_tag
    config_tag = args.config_tag
    for test_set in test_list:
        if model == 'aya-101':
                p = subprocess.Popen(f"""python URLs/transformer_url.py \
                --model_name  {model_path[model]}\
                --gpuid  {gpu_id}\
                --port {port}""", 
                shell=True)
        else:
            p = subprocess.Popen(f"""python URLs/vllm_url.py \
            --model_name  {model_path[model]}\
            --gpuid  {gpu_id}\
            --port {port}""", 
            shell=True)
        time.sleep(150)
        if test_set in all_test_list:
            template_type = "all"
        for lang in languages:
            os.system(f"bash scripts/{test_set}.sh {port} {model} {test_set}-{template_type}-{lang} {batch_size} {model_tag}  {config_tag}")
        os.system(f"kill -9 {p.pid}")
        os.system(f"kill -9 {p.pid + 1}")
        # os.system(f"kill -9 %")
        # os.system(f"kill -9 %")
        time.sleep(10)
if __name__ == '__main__':

    # no model_path specified, use the default path
    if model_path[0] == "default":
        model_path = {model:default_model_path[model] for model in model_list}
    else:
        model_path = {model:model_path[i] for i, model in enumerate(model_list)}
    
    print(f"model_path: {model_path}")
    for model in model_list:
        auto_test(model)
    
    # 原数据集bug，现已解决        
    # if 'humaneval' in test_list:
    #     input_dir = "./result/humaneval"
    #     result = transform_humaneval(input_dir)
    #     for item in result:
    #         print(result[item])
            
    if 'omgeval' in test_list:
        omg_eval(model_list, languages)