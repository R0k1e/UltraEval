import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--model_name", type=str, help="Model name on hugginface")
parser.add_argument("--gpuid", type=str, default="0", help="GPUid to be deployed")
parser.add_argument("--port", type=int, default=5002, help="the port")
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

print("model load finished")

app = Flask(__name__)

# 模型的模型参数
params_dict = {
    "temperature": 1.0,
    "top_p": 1.0,
    "max_tokens": 100,
    "top_k": 0,
    "prompt_logprobs": None,
}

def Generate(prompts,model, params_dict, ppl_mode=False):
    outputs = []
    for prompt in prompts:


        if ppl_mode:   
            question_text, answer_text = prompt.split('[SPLIT]')
            question_text = question_text.strip()
            answer_text = answer_text.strip()
        
            q_input = tokenizer.batch_encode_plus([question_text], return_tensors='pt').to(device)
            a_input = tokenizer.batch_encode_plus([answer_text], return_tensors='pt').to(device)
            y = a_input['input_ids'].to(device)
            y_ids = y[:, :-1].contiguous().to(device)
            lm_labels = y[:, 1:].clone().detach().to(device)
            
            output = model(
                input_ids=q_input['input_ids'].to(device),
                attention_mask=q_input['attention_mask'].to(device),
                decoder_input_ids=y_ids.to(device),
                labels=lm_labels.to(device),
            )
            
            logits = output.logits
            logits = torch.nn.functional.softmax(logits, dim=-1)
            logits = torch.log(logits)
            
            
            
            #取出input_ids对应的logits
            input_logits = []
            for i in range(len(logits)):
                a_ids = a_input['input_ids'][i][1:].tolist()
                for seq_len in range(len(logits[i])):
                    cur_token_id = a_ids[seq_len]
                    input_logits.append(logits[i][seq_len][cur_token_id].item())
            
            outputs.append(input_logits)

        else:
            q_input = tokenizer.batch_encode_plus([prompt.strip()], return_tensors='pt').to(device)
            if params_dict['temperature'] != 0:
                output = model.generate(
                    input_ids=q_input['input_ids'].to(device),
                    attention_mask=q_input['attention_mask'].to(device),
                    max_new_tokens=params_dict["max_tokens"],
                    do_sample=True,
                    temperature=params_dict["temperature"],
                    top_p=params_dict["top_p"],
                    top_k=params_dict["top_k"],
                )
            else:
                output = model.generate(
                    input_ids=q_input['input_ids'].to(device),
                    attention_mask=q_input['attention_mask'].to(device),
                    max_new_tokens=params_dict["max_tokens"],
                    do_sample=False,
                    top_p=params_dict["top_p"],
                    top_k=params_dict["top_k"],
                )
            output = tokenizer.decode(output[0], skip_special_tokens=True)
            if output.startswith(prompt):
                output = output[len(prompt):]
            outputs.append(output)
    return outputs


device = "cuda" if torch.cuda.is_available() else "cpu"

def load_model():
    pretrained_model = AutoModelForSeq2SeqLM.from_pretrained(
    args.model_name,
        )
    return pretrained_model.to(device)


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
        res = outputs
        return jsonify(res)
    else:
        for output in outputs:
            generated_text = output
            res.append(generated_text)
        return jsonify(res)


if __name__ == "__main__":
    app.run(port=args.port, debug=False)