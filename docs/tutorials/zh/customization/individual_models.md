## 用户部署自己的模型


### 1.模版代码

对于该部分，我们提供一个适配gunicorn框架的模板，用户只需实现/替换其中的初始化方法和推理函数适配：

```
from flask import Flask, request, jsonify
import torch
import os
from gevent.pywsgi import WSGIServer
from URLs.dispatcher import GPUDispatcher as gdp
gdp.bind_worker_gpus()

app = Flask(__name__)

print("Initializing model and tokenizer...")

# model_name = os.environ.get('HF_MODEL_NAME')
port = os.environ.get('PORT')

# Load the model and tokenizer
model = ####模型初始化####
tokenizer = ####Tokenizer初始化####

print("Model and tokenizer initialized.")

#参数字典可根据自有模型特点自定义
params_dict = {
    "max_new_tokens": 100,
    "temperature": 0.1,
    "top_p": 0.95
}

@app.route('/infer', methods=['POST'])
def main():
    datas = request.get_json()
    params = datas["params"]
    prompt = datas["instances"]

    for key, value in params.items():
        if key == "max_tokens":
            params_dict["max_new_tokens"] = value
        elif key in params_dict:
            params_dict[key] = value
    if prompt == "":
        return jsonify({'error': 'No prompt provided'}), 400
    
    #调用tokenizer，需自定义接口
    inputs = tokenizer(prompt)  # Prepare the input tensor

    #调用模型的推理函数，需自定义接口
    generate_ids = model.generate(inputs.input_ids, **params_dict)

    # Decoding the generated ids to text
    generated_text = tokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)
    assert len(prompt) == len(generated_text)
    for j in range(len(prompt)):
        generated_text[j] = generated_text[j][len(prompt[j]):]
    return jsonify(generated_text)

if __name__ == '__main__':
    # Run the Flask app
    http_server = WSGIServer(('127.0.0.1', port), app)
    http_server.serve_forever()
```

### 2.示例：使用transformers部署模型

下面以transformers部署的方式为例，演示模版的使用，同时，假设该文件命名为"transformers_url_m.py"

```
from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os
from gevent.pywsgi import WSGIServer
from URLs.dispatcher import GPUDispatcher as gdp
gdp.bind_worker_gpus()

app = Flask(__name__)

print("Initializing model and tokenizer...")

# Set the device to GPU if available
device = 'cuda' if torch.cuda.is_available() else 'cpu'

model_name = os.environ.get('HF_MODEL_NAME')
port = os.environ.get('PORT')

# Load the model and tokenizer
####模型初始化####
model = AutoModelForCausalLM.from_pretrained(model_name).to(device)
####tokenizer初始化####
tokenizer = AutoTokenizer.from_pretrained(model_name)

# 此处为transformers库部署模型的特殊适配
if tokenizer.pad_token is None:
    tokenizer.add_special_tokens({'pad_token': '[PAD]'})
    model.resize_token_embeddings(len(tokenizer))

print("Model and tokenizer initialized.")

#参数字典可根据自有模型特点自定义
params_dict = {
    "max_new_tokens": 100,
    "temperature": 0.1,
    "top_p": 0.95
}

@app.route('/infer', methods=['POST'])
def main():
    datas = request.get_json()
    params = datas["params"]
    prompt = datas["instances"]

    for key, value in params.items():
        if key == "max_tokens":
            params_dict["max_new_tokens"] = value
        elif key in params_dict:
            params_dict[key] = value
    if prompt == "":
        return jsonify({'error': 'No prompt provided'}), 400
    
    #调用tokenizer，需自定义接口
    inputs = tokenizer(prompt, padding=True, return_tensors="pt").to(device)  # Prepare the input tensor

    #调用模型的推理函数，需自定义接口
    generate_ids = model.generate(inputs.input_ids, **params_dict)

    # Decoding the generated ids to text
    generated_text = tokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)
    assert len(prompt) == len(generated_text)
    for j in range(len(prompt)):
        generated_text[j] = generated_text[j][len(prompt[j]):]
    return jsonify(generated_text)

if __name__ == '__main__':
    # Run the Flask app
    http_server = WSGIServer(('127.0.0.1', port), app)
    http_server.serve_forever()
```

### 3.配置和启动

修改 `gunicorn_conf.py` 和 `start_gunicorn.sh` 文件，以适应新部署的模型。

- **start_gunicorn.sh**: 无需修改，但请注意传入参数 `INFER_TYPE` 的新可能值，它需要与 `gunicorn_conf.py` 中的修改相对应。
- **gunicorn_conf.py**: 根据变量 `infer_type` 的值，为变量 `wsgi_app` 赋予相应值。

```
import os
import sys
from URLs.dispatcher import GPUDispatcher

# gunicorn config & hook

gdp = GPUDispatcher()

port = os.environ.get('PORT')
infer_type = os.environ.get('INFER_TYPE')

bind = '127.0.0.1:' + port
workers = gdp.workers_num()

# determine deploy type, currently support 'vLLM' and 'transformers'
if infer_type == "vLLM":
    wsgi_app = 'URLs.vllm_url_m:app'
#### ADD YOUR CODE BELOW ####
elif infer_type == "transformers":
    wsgi_app = 'URLs.transformers_url_m:app'

proc_name = 'infer' 
accesslog = '-'
timeout=300

...........(other part of code)..............
```