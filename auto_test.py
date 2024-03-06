import os
import subprocess
from transform_humaneval import transform_humaneval
from omgeval import omg_eval
import time
import signal


# languages = ['en', 'zh', 'es', 'ru', 'fr']
# languages = ['en', 'es', 'ru', 'fr']
# languages = ['zh', 'es', 'ru']
languages = ['zh']
# model_list = ['okapi', 'bloom', 'polyalpaca', 'polychat', 'guanaco', 'phoenix', "guanaco-13b", 'aya', 'aya-101', "UltraLink"]
# model_list = ['aya', 'aya-101']
# model_list = ['aya-101']
# model_list = ['llama-7b']
model_list = ['UltraLink']
# test_list = ['humaneval', 'mgsm', 'omgeval', 'm-mmlu', 'belebele', 'xwinograd', 'm-arc', 'm-hellaswag']
# test_list = ['m-mmlu']
# port = 6325
# gpu_id= "0,1"
# test_list = ['m-hellaswag']
test_list = ['m-arc']
port = 6327
gpu_id= "2,3"
print(f"gpu_id: {gpu_id}")
print(f"port: {port}")
print(f"model_list: {model_list}")
print(f"test_list: {test_list}")
print(f"languages: {languages}")
all_test_list = ['belebele','m-mmlu', 'xwinograd', 'm-arc', 'm-hellaswag']

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
    'aya-101': 'null',
}

model_path = {
    'UltraLink': "/data/public/wangshuo/exp/ft-5lang-omg-13b/ckpts/checkpoints/epoch_2_hf",
    'aya': "/home/wanghaoyu/mAlign-shuo-dev/aya-5lang-lr2e-5/checkpoints/step_23400/_hf",
    'aya-101': "/home/wanghaoyu/aya/aya-101",
    'bloom': "/data/public/wangshuo/bloomz-7b1-mt",
    'okapi': "/data/public/wangshuo/PolyLM-multialpaca-13b",
    'polychat': "/data/public/wangshuo/polylm-chat-13b",
    'llama-7b': "/data/public/opensource_models/meta-llama/Llama-2-7b-chat-hf",
    'llama-13b': "/data/public/opensource_models/meta-llama/Llama-2-13b-hf",
    'llama-70b': "/data/public/opensource_models/meta-llama/Llama-2-70b-chat-hf",
    'phoenix-7b': " /home/wanghaoyu/analyse_data/phoenix-inst-chat-7b",
    'chimera-13b': " /home/wanghaoyu/analyse_data/chimera-inst-chat-13b",
    'guanaco-13b': " /home/wanghaoyu/analyse_data/guanaco-13b-hf",
    'guanaco-7b': " /home/wanghaoyu/analyse_data/Guanaco",
}

def auto_test(model):
    if model == 'aya-101':
        batch_size = 4
    else:
        batch_size = 64
    print(f"batch_size: {batch_size}")
    template_type = template_dict[model]
    for test_set in test_list:
        if test_set in all_test_list:
            template_type = "all"
        for lang in languages:
            os.system(f"bash scripts/{test_set}.sh {port} {model} {test_set}-{template_type}-{lang} {batch_size}")
        
if __name__ == '__main__':
    for model in model_list:
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
        time.sleep(90)
        auto_test(model)
        os.system(f"kill -9 %")
        os.system(f"kill -9 %")
        
    if 'humaneval' in test_list:
        input_dir = "/home/wanghaoyu/UltraEval/result/humaneval"
        result = transform_humaneval(input_dir)
        for item in result:
            print(result[item])
    if 'omgeval' in test_list:
        omg_eval(model_list, languages)