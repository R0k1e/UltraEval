import argparse
import pandas as pd
import pdb
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
    if ppl_mode:   
        for prompt in prompts:
            question_list = []
            answer_list = []
            question_text, answer_text = prompt.split('[SPLIT]')
            question_text = question_text.strip()
            answer_text = answer_text.strip()
            question_list.append(question_text)
            answer_list.append(answer_text)

            # pdb.set_trace()
            q_input = tokenizer.batch_encode_plus(question_list, return_tensors='pt', padding=True).to(device)
            a_input = tokenizer.batch_encode_plus(answer_list, return_tensors='pt', padding=True).to(device)


            # pdb.set_trace()
            y = a_input['input_ids'].to(device)
            y_ids = y[:, :-1].contiguous().to(device)
            lm_labels = y[:, 1:].clone().detach().to(device)
            lm_labels[y[:, 1:] == tokenizer.pad_token_id] = -100
            # pdb.set_trace()

            output = model(
                input_ids=q_input['input_ids'].to(device),
                attention_mask=q_input['attention_mask'].to(device),
                decoder_input_ids=y_ids.to(device),
                labels=lm_labels.to(device),
            )
            # pdb.set_trace()
            
            # 计算交叉熵损失
            loss = output.loss
            outputs.append(loss.item())
        
        
        # # pdb.set_trace()
        # a_input_ids = a_input['input_ids'][:, :-1].to(device)
        # logits = output.logits
        # prompt_logits = logits.gather(-1, a_input_ids.unsqueeze(-1)).squeeze(-1)

        # # pdb.set_trace()
        # # 计算logprobs
        # outputs = torch.log_softmax(prompt_logits, dim=-1).tolist()
        
    else:
        q_input = tokenizer.batch_encode_plus(prompts, return_tensors='pt', padding=True, max_length=params_dict['max_tokens']).to(device)
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
        outputs = tokenizer.batch_decode(output, skip_special_tokens=True)
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