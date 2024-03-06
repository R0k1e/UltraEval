import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--model_name", type=str, help="Model name on hugginface")
parser.add_argument("--gpuid", type=str, default="0", help="GPUid to be deployed")
parser.add_argument("--port", type=int, default=5002, help="the port")
parser.add_argument("--weight", type=float, default=0, help="linear")
parser.add_argument("--use_peft", default=None,action="store_true",help="linear")
parser.add_argument("--use_vllm", default=None,action="store_true",help="linear")
parser.add_argument("--use_gate", default=None,action="store_true",help="linear")
parser.add_argument("--gate_path", type=str,help="linear")
parser.add_argument("--temperature", type=float, default=1.0, help="linear")
parser.add_argument("--language_model", type=str, default="", help="linear")
parser.add_argument("--task_model", type=str, default="", help="linear")
args = parser.parse_args()

import re
import os
os.environ["CUDA_VISIBLE_DEVICES"] = args.gpuid
from flask import Flask, jsonify, request
# from optimum.bettertransformer import BetterTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, GenerationConfig
import torch

"""
reference:https://github.com/vllm-project/vllm/blob/main/vllm/sampling_params.py
"""

tokenizer = AutoTokenizer.from_pretrained(args.model_name)
tokenizer.padding_side = 'left'
tokenizer.pad_token = tokenizer.eos_token

print("model load finished")

app = Flask(__name__)

# 模型的模型参数
params_dict = {
    "temperature": 1.0,
    "top_p": 1.0,
    "max_tokens": 16,
    "prompt_logprobs": None,
}

def Generate(prompts,model, params_dict, ppl_mode=False):
    print("Generate function")
    inputs = tokenizer(
        prompts,
        max_length=2048,
        return_tensors="pt",
        padding=True,
    ).to(device)
    
    
    if ppl_mode:   
        outputs = model.generate(
            input_ids=inputs["input_ids"],attention_mask=inputs["attention_mask"], 
            max_length=params_dict["max_tokens"],
            output_scores=True,
            return_dict_in_generate=True,
        )
        all_logits = outputs.scores
        for logits in all_logits:            
            logits = torch.nn.functional.softmax(logits, dim=-1)
            logits = torch.log(logits)
        return all_logits
        
    else:
        outputs = model.generate(
            input_ids=inputs["input_ids"],attention_mask=inputs["attention_mask"], 
            max_new_tokens=params_dict["max_tokens"],
            do_sample=True,
            temperature=params_dict["temperature"],
            top_p=params_dict["top_p"],
        )
        print("finish generate")
        outputs = tokenizer.batch_decode(
            outputs.to("cpu"), skip_special_tokens=True
        )
        print("decode finish")
        for i in range(len(outputs)):
            if outputs[i].startswith(prompts[i]):
                outputs[i] = outputs[i][len(prompts[i]):]
        return outputs


device = "cuda" if torch.cuda.is_available() else "cpu"

def load_model():
    pretrained_model = AutoModelForSeq2SeqLM.from_pretrained(
    args.model_name,
    device_map="auto",
        )
    return pretrained_model


model = load_model()

@app.route("/infer", methods=["POST"])
def main():
    datas = request.get_json()
    params = datas["params"]
    prompts = datas["instances"]
    
    for key, value in params.items():
        if key in params_dict:
            params_dict[key] = value
            
    if "prompt_logprobs" in params and params["prompt_logprobs"] is not None:
        ppl_mode = True
    else:
        ppl_mode = False
        
    
    outputs = Generate(prompts=prompts,model=model, ppl_mode=ppl_mode, params_dict=params_dict)
        
    res = []
    if "prompt_logprobs" in params and params["prompt_logprobs"] is not None:
        for logits in outputs:
            prompt_logprobs = logits
            logp_list = [list(d.values())[0] for d in prompt_logprobs[1:]]
            res.append(logp_list)
        return jsonify(res)
    else:
        for output in outputs:
                    
            if args.use_vllm:
                generated_text = output.outputs[0].text
            else:
                generated_text = output
            res.append(generated_text)
        return jsonify(res)


if __name__ == "__main__":
    app.run(port=args.port, debug=False)