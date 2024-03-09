import json
import os
import copy

def make_mgsm_config():
    input_path = "/home/wanghaoyu/UltraEval/datasets/mgsm/config/mgsm_gen.json"
    os.makedirs(os.path.dirname(input_path), exist_ok=True)
    lang_list = ['en', 'zh', 'es', 'fr', 'ru']
    model_list = ['okapi', 'bloom', 'polyalpaca', 'polychat', 'guanaco', 'phoenix', "guanaco-13b", "null"]

    with open(input_path, 'r') as f:
        origin_data = json.load(f)

    for lang in lang_list:
        for model in model_list:
            output_path = os.path.join("/home/wanghaoyu/UltraEval/datasets/mgsm/config/", f"mgsm_{model}_{lang}_gen.json")
            data = copy.deepcopy(origin_data)
            data['task_name'] = f'mgsm_{model}_{lang}'
            data['path'] = f"datasets/mgsm/data/mgsm_{lang}.jsonl"
            data['transform'] = f"datasets/mgsm/transform_gen_{model}_{lang}.py"
            data['fewshot'] = 0
            data['generate']['params'] = "models/model_params/vllm_sample_math_zero.json"
            data['postprocess'] = 'mgsm_zero_post'
            with open(output_path, 'w') as f:
                json.dump(data, f)
    
    input_path = "/home/wanghaoyu/UltraEval/datasets/mgsm/"

    instructions = {
        "en": "Please answer the following question:",
        "zh": "请回答以下问题：",
        "es": "Por favor responda la siguiente pregunta:",
        "fr": "Veuillez répondre à la question suivante:",
        "ru": "Пожалуйста, ответьте на следующий вопрос:"
    }

    templates = {
        'okapi': "[INST] {data['question']} [/INST]",
        'bloom': "{data['question']}", #instruction + question
        'polyalpaca': r"{data['question'].strip()}\n\n",
        'polychat': r"<|user|>\n{data['question'].strip()}<|assistant|>\n",
        'guanaco': r"### Input:\nUser: {data['question']}\n### Response:\n",
        'phoenix': r"Human: <s>{data['question']}</s>Assistant: <s>",
        'guanaco-13b': r"### Human: {data['question']}\n### Assistant:",
        'null': r"{data['question']}"
    }


    for lang in lang_list:
        for model in model_list:
            if model == 'bloom':
                text = instructions[lang] + templates[model]
            else:
                text = templates[model]
            origin_code = f'''
import random
from UltraEval.tasks.postprocess import GSM8KPost
def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = f"{text}"
    correct_answer = data["answer"]
    gsm8kp = GSM8KPost()
    _, processed_correct_answer = gsm8kp([], correct_answer)
    return {{
        "input": text,
        "output": correct_answer,
        "processed_output": processed_correct_answer,
        }}
    '''
            output_path = os.path.join(input_path, f"transform_gen_{model}_{lang}.py")  
            with open(output_path, 'w') as f:
                f.write(origin_code)
                
def make_humaneval_config():
    input_path = "/home/wanghaoyu/UltraEval/datasets/humaneval/config/humaneval_gen.json"
    os.makedirs(os.path.dirname(input_path), exist_ok=True)
    lang_list = ['en', 'zh', 'es', 'fr', 'ru']
    model_list = ['okapi', 'guanaco', 'phoenix', "guanaco-13b", 'null']

    with open(input_path, 'r') as f:
        origin_data = json.load(f)

    for lang in lang_list:
        for model in model_list:
            output_path = os.path.join("/home/wanghaoyu/UltraEval/datasets/humaneval/config/", f"humaneval_{model}_{lang}_gen.json")
            data = copy.deepcopy(origin_data)
            data['task_name'] = f'humaneval_{model}_{lang}'
            if lang == 'en':
                data['path'] = f"datasets/humaneval/data/humaneval.jsonl"
            else:
                data['path'] = f"datasets/humaneval/data/{lang}_humaneval.jsonl"
            data['transform'] = f"datasets/humaneval/transform_gen_{model}_{lang}.py"
            data['fewshot'] = 0
            data['generate']['params'] = "models/model_params/vllm_sample_wizardcode.json"
            data['postprocess'] = 'humaneval_post_wizardcode'
            with open(output_path, 'w') as f:
                json.dump(data, f)
    
    input_path = "/home/wanghaoyu/UltraEval/datasets/humaneval/"

    instructions = {
        "en": "Create a Python script for this problem. The Python script should be enclosed by ```python``` tags. ",
        'zh': "请为以下问题写一个Python脚本。Python脚本需要用```python```标签包裹。",
        'es': "Cree un script Python para esta pregunta. El script Python debe estar enmarcado por ```python```.",
        'fr': "Créez un script Python pour cette question. Le script Python doit être entouré de ```python```.",
        'ru': "Создайте скрипт Python для этой задачи. Скрипт Python должен быть включен в ```python``` теги."
    }

    templates = {
        'okapi': r"[INST]INSTRUCTION\n{prompt}\n\n[/INST]",
        'bloom': r"INSTRUCTION{prompt}", #instruction + question
        'polyalpaca': r"{prompt.strip()}\n\n",
        'polychat': r"<|user|>\nINSTRUCTION\n{prompt.strip()}\n\n<|assistant|>\n",
        'guanaco': r"### Input:User:INSTRUCTION{prompt}### Response:",
        'phoenix': r"Human: <s>INSTRUCTION{prompt}</s>Assistant: <s>",
        'guanaco-13b': r"### Human: INSTRUCTION{prompt}\n### Assistant:",
        'null': r"INSTRUCTION{prompt}"
    }


    for lang in lang_list:
        for model in model_list:
            text = templates[model].replace("INSTRUCTION", instructions[lang])
            origin_code = f'''
import random

def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    prompt = data['prompt'].strip().replace("    ", "\\t")
    temp_input = f"""{text}"""
    return {{"input": temp_input, "output": "", "processed_output": ""}}
    '''
            output_path = os.path.join(input_path, f"transform_gen_{model}_{lang}.py")  
            with open(output_path, 'w') as f:
                f.write(origin_code)
                
def make_omgeval_config():
    input_path = "/home/wanghaoyu/UltraEval/datasets/omgeval/config/omgeval-en_gen.json"
    os.makedirs(os.path.dirname(input_path), exist_ok=True)
    lang_list = ['en', 'zh', 'es', 'fr', 'ru', 'ar']
    model_list = ['okapi', 'guanaco', 'phoenix', 'llama', 'guanaco-13b', 'null']

    with open(input_path, 'r') as f:
        origin_data = json.load(f)

    for lang in lang_list:
        for model in model_list:
            output_path = os.path.join("/home/wanghaoyu/UltraEval/datasets/omgeval/config/", f"omgeval_{model}_{lang}_gen.json")
            data = copy.deepcopy(origin_data)
            data['task_name'] = f'omgeval_{model}_{lang}'
            data['path'] = f"datasets/omgeval/data/{lang}.jsonl"
            data['transform'] = f"datasets/omgeval/transform_gen_{model}_{lang}.py"
            data['fewshot'] = 0
            data['generate']['params'] = "models/model_params/vllm_sample_omg.json"
            data['postprocess'] = ''
            with open(output_path, 'w') as f:
                json.dump(data, f)
    
    input_path = "/home/wanghaoyu/UltraEval/datasets/omgeval/"
    templates = {
        'okapi': "[INST] {data['question']} [/INST]",
        'guanaco': r"### Input:\nUser: {data['question']}\n### Response:\n",
        'phoenix': r"Human: <s>{data['question']}</s>Assistant: <s>",
        'guanaco-13b': r"### Human: {data['question']}\n### Assistant:",
        'llama' : r"""[INST] {data['question']} [/INST]""",
        'null' : r"{data['question']}"
    }
    
    instructions = {
        "en": "You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature. If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.",
        'zh': "你是一个乐于助人、尊重他人、诚实守信的助手。在保证安全的前提下，尽可能回答问题。 您的回答不得包含任何有害、不道德、种族主义、性别歧视、有毒、危险或非法内容。请确保您的回答不带任何社会偏见并具有积极意义。如果问题没有任何意义或与事实不符，请解释原因，而不要回答不正确的问题。如果您不知道问题的答案，请不要分享虚假信息。",
        'es': "Eres un asistente servicial, respetuoso y honesto. Responde siempre de la forma más útil posible, sin dejar de ser seguro.  Sus respuestas no deben incluir ningún contenido nocivo, poco ético, racista, sexista, tóxico, peligroso o ilegal. Asegúrese de que sus respuestas sean socialmente imparciales y de naturaleza positiva. Si una pregunta no tiene sentido o no es coherente con los hechos, explica por qué en lugar de responder algo que no es correcto. Si no sabes la respuesta a una pregunta, por favor, no compartas información falsa.",
        'ru': "Вы - полезный, уважительный и честный помощник. Всегда отвечайте максимально полезно и при этом безопасно.  Ваши ответы не должны содержать вредных, неэтичных, расистских, сексистских, токсичных, опасных или незаконных материалов. Пожалуйста, следите за тем, чтобы ваши ответы были социально объективными и позитивными по своей сути. Если вопрос не имеет смысла или не соответствует действительности, объясните, почему, вместо того чтобы отвечать на него неправильно. Если вы не знаете ответа на вопрос, пожалуйста, не сообщайте ложную информацию.",
        'fr': "Vous êtes un assistant utile, respectueux et honnête. Répondez toujours de la manière la plus utile possible, tout en restant prudent.  Vos réponses ne doivent pas comporter de contenu nuisible, contraire à l'éthique, raciste, sexiste, toxique, dangereux ou illégal. Veillez à ce que vos réponses soient socialement impartiales et positives. Si une question n'a pas de sens ou n'est pas cohérente sur le plan des faits, expliquez pourquoi au lieu de répondre quelque chose d'incorrect. Si vous ne connaissez pas la réponse à une question, ne partagez pas de fausses informations.",
        'ar': "أنتِ مساعدة مفيدة ومحترمة وصادقة. أجب دائمًا بشكل مفيد قدر الإمكان، مع الحفاظ على سلامتك.  يجب ألا تتضمن إجاباتك أي محتوى ضار أو غير أخلاقي أو عنصري أو متحيز جنسيًا أو سام أو خطير أو غير قانوني. يرجى التأكد من أن إجاباتك غير متحيزة اجتماعياً وإيجابية بطبيعتها. إذا كان السؤال غير منطقي، أو غير متماسك من الناحية الواقعية، اشرح السبب بدلاً من الإجابة على شيء غير صحيح. إذا كنت لا تعرف إجابة سؤال ما، يُرجى عدم مشاركة معلومات خاطئة.",
    }


    for lang in lang_list:
        for model in model_list:
            # if model == 'llama':
            #     text = templates[model].replace("INSTRUCTION", instructions[lang])
            # else:
            #     text = templates[model]
            text = templates[model]
            origin_code = f'''
import random

def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = f"""{text}"""
    return {{
        "input": text, 
        #"input": text.strip(), 
        "output": "", 
        "processed_output": ""
        }}
    '''
            output_path = os.path.join(input_path, f"transform_gen_{model}_{lang}.py")  
            with open(output_path, 'w') as f:
                f.write(origin_code)
                
def make_mmlu_config():
    input_path = "./datasets/m-mmlu/config/m-mmlu_gen.json"
    os.makedirs(os.path.dirname(input_path), exist_ok=True)
    lang_list = ['en', 'zh', 'es', 'fr', 'ru']
    model_list = ["okapi", 'null']

    with open(input_path, 'r') as f:
        origin_data = json.load(f)

    for lang in lang_list:
        for model in model_list:
            output_path = os.path.join("./datasets/m-mmlu/config/", f"m-mmlu-{model}-{lang}-gen.json")
            data = copy.deepcopy(origin_data)
            data['task_name'] = f'm-mmlu_{model}_{lang}'
            data['path'] = f"datasets/m-mmlu/data/{lang}.jsonl"
            data['transform'] = f"datasets/m-mmlu/transform_gen_v0.py"
            data['fewshot'] = 5
            data['generate']['params'] = "models/model_params/vllm_sample_v1.json"
            data['postprocess'] = ''
            with open(output_path, 'w') as f:
                json.dump(data, f)
    
    input_path = "/home/wanghaoyu/UltraEval/datasets/m-mmlu/"
    
    templates = {
        'okapi': r"[INST] {prompt} [/INST]",
        'null': r"{prompt}"
    }


    instructions = {
        "en": r'"Question\n{{question}}\n\nOptions\n{{options}}\n\nAnswer\n"',
        'zh': r'"问题\n{{question}}\n\n选项\n{{options}}\n\n答案\n"',
        'es': r'"Pregunta\n{{question}}\n\nOpción\n{{options}}\n\nContesta\n"',
        'fr': r'"Question\n{{question}}\n\nOptions\n{{options}}\n\nAnswer\n"',
        'ru': r'"Вопрос\n{{question}}\n\nВарианты\n{{options}}\n\nОтвет\n"',
    }


    for lang in lang_list:
        for model in model_list:
            text = instructions[lang]
            template = templates[model]
            origin_code = f'''
import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    choices = []
    answer = None
    for i, (kw, val) in enumerate(data["target_scores"].items()):
        if val > 0:
            answer = i
        choices.append(kw)
    if answer is None:
        raise ValueError("Invalid data `{{}}`".format(data))

    choice_style = "({{}})"

    sep_style = " "

    idx_style = "ABCD"
    
    prompt = {text}

    options = []
    for i, choice in enumerate(choices):
        options.append(choice_style.format(idx_style[i]) + sep_style + choice)

    answer = choice_style.format(idx_style[answer]) + "\\n"

    prompt = prompt.format(question=data["question"], options="\\n".join(options))
    
    prompt = f"""{template}"""

    return {{"input": prompt, "output": answer, "processed_output": answer}}

    '''
            output_path = os.path.join(input_path, f"transform_gen_{model}_{lang}.py")  
            with open(output_path, 'w') as f:
                f.write(origin_code)
                
def make_belebele_config():
    input_path = "datasets/Belebele/config/Belebele-en_gen.json"
    os.makedirs(os.path.dirname(input_path), exist_ok=True)
    lang_list = ['en', 'zh', 'es', 'fr', 'ru', "ja"]
    model_list = ["all"]

    with open(input_path, 'r') as f:
        origin_data = json.load(f)

    for lang in lang_list:
        for model in model_list:
            model = 'all'
            output_path = os.path.join("./datasets/Belebele/config/", f"Belebele-{model}-{lang}-gen.json")
            data = copy.deepcopy(origin_data)
            data['task_name'] = f'belebele_{model}_{lang}'
            data['path'] = f"datasets/Belebele/data/{lang}.jsonl"
            data['transform'] = f"datasets/Belebele/transform_gen_v0.py"
            data['fewshot'] = 5
            data['generate']['params'] = "models/model_params/vllm_sample_v1.json"
            data['postprocess'] = ''
            with open(output_path, 'w') as f:
                json.dump(data, f)
                
def make_xcopa_config():
    input_path = "datasets/xcopa/config/copa_gen.json"
    os.makedirs(os.path.dirname(input_path), exist_ok=True)
    lang_list = ['en', 'zh', 'es', 'fr', 'ru', "ja"]
    model_list = ["all"]

    with open(input_path, 'r') as f:
        origin_data = json.load(f)

    for lang in lang_list:
        for model in model_list:
            model = 'all'
            output_path = os.path.join("./datasets/xcopa/config/", f"xcopa-{model}-{lang}-gen.json")
            data = copy.deepcopy(origin_data)
            data['task_name'] = f'xcopa_{model}_{lang}'
            data['path'] = f"datasets/xcopa/data/{lang}.jsonl"
            data['transform'] = f"datasets/xcopa/transform_gen_v0.py"
            data['fewshot'] = 5
            data['generate']['params'] = "models/model_params/vllm_sample_v1.json"
            data['postprocess'] = ''
            with open(output_path, 'w') as f:
                json.dump(data, f)
                
def make_xwinograd_config():
    input_path = "datasets/xwinograd/config/xwinograd_gen.json"
    os.makedirs(os.path.dirname(input_path), exist_ok=True)
    lang_list = ['en', 'zh', 'fr', 'ru', "ja"]
    model_list = ["okapi"]

    with open(input_path, 'r') as f:
        origin_data = json.load(f)

    for lang in lang_list:
        for model in model_list:
            model = 'all'
            output_path = os.path.join("./datasets/xwinograd/config/", f"xwinograd-{model}-{lang}-gen.json")
            data = copy.deepcopy(origin_data)
            data['task_name'] = f'xwinograd_{model}_{lang}'
            data['path'] = f"datasets/xwinograd/data/{lang}.jsonl"
            data['transform'] = f"datasets/xwinograd/transform_gen_{model}_{lang}.py"
            data['fewshot'] = 0
            data['generate']['params'] = "models/model_params/vllm_sample_v1.json"
            data['postprocess'] = ''
            with open(output_path, 'w') as f:
                json.dump(data, f)
    
    input_path = "/home/wanghaoyu/UltraEval/datasets/xwinograd/"
    

    instructions = {
        "en": r"Passage: {data['question']}\nWhich of the following is a good sentence:\nA. {textA}\nB. {textB}\nOption: ",
        'zh': r"上文： {data['question']}\n哪一个句子是一个更好的下文：\nA. {textA}\nB. {textB}\n选项： ",
        'ja': r"前文： {data['question']}\nどの文章がより適切か：\nA. {textA}\nB. {textB}\nオプション： ",
        'fr': r"Passage : {data['question']}\nLequel des énoncés suivants est une bonne phrase: \nA. {textA}\nB. {textB}\noptions: ",
        'ru': r"предыдущий пункт: {data['question']}\nКакое предложение лучше: \nA. {textA}\nB. {textB}\nопционы: "
    }


    for lang in lang_list:
        for model in model_list:
            text = instructions[lang]
            origin_code = f'''
import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    options = list(data["target_scores"].keys())
    textA, textB = options
    text = f"""{text}"""
    text = f"""{template}"""
    index_of_correct_answer = list(data["target_scores"].values()).index(1)
    answers = ["A", "B"]
    correct_answer = answers[index_of_correct_answer]

    return {{"input": text, "output": correct_answer, "processed_output": correct_answer}}
    '''
            output_path = os.path.join(input_path, f"transform_gen_{model}_{lang}.py")  
            with open(output_path, 'w') as f:
                f.write(origin_code)
                
def make_marc_config():
    input_path = "datasets/m-arc/config/m-arc_gen.json"
    os.makedirs(os.path.dirname(input_path), exist_ok=True)
    lang_list = ['en', 'zh', 'fr', 'ru', "es"]
    model_list = ["okapi", 'null']

    with open(input_path, 'r') as f:
        origin_data = json.load(f)

    for lang in lang_list:
        for model in model_list:
            output_path = os.path.join("./datasets/m-arc/config/", f"m-arc-{model}-{lang}-gen.json")
            data = copy.deepcopy(origin_data)
            data['task_name'] = f'm-arc_{model}_{lang}'
            data['path'] = f"datasets/m-arc/data/{lang}.jsonl"
            data['transform'] = f"datasets/m-arc/transform_gen_{model}_{lang}.py"
            data['fewshot'] = 0
            data['generate']['params'] = "models/model_params/vllm_sample.json"
            data['postprocess'] = ''
            with open(output_path, 'w') as f:
                json.dump(data, f)
                
    input_path = "datasets/m-arc/config/m-arc_ppl.json"
    with open(input_path, 'r') as f:
        origin_data = json.load(f)
    for lang in lang_list:
        for model in model_list:
            output_path = os.path.join("./datasets/m-arc/config/", f"m-arc-{model}-{lang}-ppl.json")
            data = copy.deepcopy(origin_data)
            data['task_name'] = f'm-arc_{model}_{lang}'
            data['path'] = f"datasets/m-arc/data/{lang}.jsonl"
            data['transform'] = f"datasets/m-arc/transform_ppl_{model}_{lang}.py"
            data['fewshot'] = 0
            data['metric']['accuracy']['evaluation']['type']= 'log_prob'
            data['generate']['method'] = 'loglikelihood'
            data['postprocess'] = ''
            with open(output_path, 'w') as f:
                json.dump(data, f)
    
    input_path = "/home/wanghaoyu/UltraEval/datasets/m-arc/"
    
    templates = {
        'okapi': r"[INST] {text} [/INST]",
        'null': r"{text}"
    }

    #有一句你只需要给出选项字母即可
    # instructions = {
    #     "en": r'"Question:\n" + data["question"] + "\n" + "Requirement:\nChoose and answer the letter of the correct answer. You just need to give the option letters.\n" + "Options:\n" + text',
    #     'zh': r'"问题：\n" + data["question"] + "\n" + "要求：\n选择并回答正确答案的字母。你只需要给出选项字母即可。\n" + "选项：\n" + text ',
    #     'es': r'"Pregunta:\n" + data["question"] + "\n" + "Petición:\nElige y contesta la letra de la respuesta correcta. Sólo tienes que dar las letras de opción.\n" + "Opciones:\n" + text ',
    #     'fr': r'"Question:\n" + data["question"] + "\n" + "Exigence:\nChoisissez et répondez à la lettre de la bonne réponse. Il suffit de donner les lettres d\'option.\n" + "Option:\n" + text ',
    #     'ru': r'"Вопрос:\n" + data["question"] + "\n" + "Требование:\nВыберите и ответьте на букву правильного ответа. Вам просто нужно указать буквы опций.\n" + "Варианты:\n" + text '
    # }
    
    instructions = {
        "en": r'"Question:\n" + data["question"] + "\n" + "Requirement:\nChoose and answer the letter of the correct answer.\n" + "Options:\n" + text',
        'zh': r'"问题：\n" + data["question"] + "\n" + "要求：\n选择并回答正确答案的字母。\n" + "选项：\n" + text ',
        'es': r'"Pregunta:\n" + data["question"] + "\n" + "Petición:\nElige y contesta la letra de la respuesta correcta. Coloque la letra de su elección al principio de su respuesta.\n" + "Opciones:\n" + text ',
        'fr': r'"Question:\n" + data["question"] + "\n" + "Exigence:\nChoisissez et répondez à la lettre de la bonne réponse.\n" + "Option:\n" + text ',
        'ru': r'"Вопрос:\n" + data["question"] + "\n" + "Требование:\nВыберите и ответьте на букву правильного ответа.\n" + "Варианты:\n" + text '
    }
    
    question_template = {
        "en": r"Question:\n{data['question']}\n",
        'zh': r"问题：\n{data['question']}\n",
        'es': r"Pregunta:\n{data['question']}\n",
        'fr': r"Question:\n{data['question']}\n",
        'ru': r"Вопрос:\n{data['question']}\n"
    }
    lead_in = {
        "en": r"Answer:\n",
        'zh': r"答案：\n",
        'es': r"Respuesta:\n",
        'fr': r"Answer:\n",   
        'ru': r"Ответ:\n"
    }


    for lang in lang_list:
        for model in model_list:
            origin_code = f'''
import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    options = list(data["target_scores"].keys())
    text = ""
    for idx, option in enumerate(options):
        text += f"{{chr(65+idx)}}. {{option}}\\n"
    text = {instructions[lang]}
    text = f"""{templates[model]}""" + "{lead_in[lang]}"
    index_of_correct_answer = list(data["target_scores"].values()).index(1)
    correct_answer = chr(65 + index_of_correct_answer)
    #一个俄语字母，一个英语字母
    if correct_answer == "A":
        correct_answer = ["A","А"]
    elif correct_answer == "B":
        correct_answer = ["B","Б"]
    elif correct_answer == "C":
        correct_answer = ["C","В","С"]
    elif correct_answer == "D":
        correct_answer = ["D","Д"]
    return {{"input": text, "output": correct_answer, "processed_output": correct_answer}}
    '''
            output_path = os.path.join(input_path, f"transform_gen_{model}_{lang}.py")  
            with open(output_path, 'w') as f:
                f.write(origin_code)

    for lang in lang_list:
        for model in model_list:
            origin_code = f'''
import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = f"{question_template[lang]}"
    text = f"""{templates[model]}"""
    answer_prompt = f"{lead_in[lang]}"
    text = text + answer_prompt
    processed_correct_answer = correct_answer = [
        key for key, value in data["target_scores"].items() if value == 1
    ][0].strip()
    return {{
        "input": text,
        "output": correct_answer,
        "processed_output": processed_correct_answer,
    }}
    '''
            output_path = os.path.join(input_path, f"transform_ppl_{model}_{lang}.py")  
            with open(output_path, 'w') as f:
                f.write(origin_code)
                
                
def make_mhellaswag_config():
    input_path = "datasets/hellaswag/config/hellaswag_ppl.json"
    os.makedirs(os.path.dirname(input_path), exist_ok=True)
    lang_list = ['en', 'zh', 'fr', 'ru', "es"]
    model_list = ["okapi", 'null']

    with open(input_path, 'r') as f:
        origin_data = json.load(f)

    templates = {
        'okapi': r"[INST] {text} [/INST]",
        'null': r"{text}"
    }

    for lang in lang_list:
        for model in model_list:
            output_path = os.path.join("./datasets/m-hellaswag/config/", f"m-hellaswag-{model}-{lang}-ppl.json")
            data = copy.deepcopy(origin_data)
            data['task_name'] = f'm-hellaswag_{model}_{lang}'
            data['path'] = f"datasets/m-hellaswag/data/{lang}.jsonl"
            data['transform'] = f"datasets/m-hellaswag/transform_ppl_{model}_{lang}.py"
            data['fewshot'] = 0
            data['generate']['params'] = ""
            data['generate']['method'] = "loglikelihood"
            if model != 'null':
                data['postprocess'] = 'general_torch_ppl_norm'
            else:
                data['postprocess'] = 'transformer_ppl_norm'
            with open(output_path, 'w') as f:
                json.dump(data, f)
                
    input_path = "/home/wanghaoyu/UltraEval/datasets/m-hellaswag/"

    for lang in lang_list:
        for model in model_list:
            text = templates[model]
            origin_code = f'''
import random    
        
def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    text = f"{text}"
    correct_answer = [
        key for key, value in data["target_scores"].items() if value == 1
    ]
    try:
        correct_answer = correct_answer[0].strip()
    except Exception:
        correct_answer = ""

    return {{"input": text, "output": correct_answer, "processed_output": correct_answer}}
    '''
            output_path = os.path.join(input_path, f"transform_ppl_{model}_{lang}.py")  
            with open(output_path, 'w') as f:
                f.write(origin_code)
                
    input_path = "datasets/hellaswag/config/hellaswag_gen.json"
    os.makedirs(os.path.dirname(input_path), exist_ok=True)
    lang_list = ['en', 'zh', 'fr', 'ru', "es"]
    model_list = ["okapi", 'null']

    with open(input_path, 'r') as f:
        origin_data = json.load(f)

    for lang in lang_list:
        for model in model_list:
            output_path = os.path.join("./datasets/m-hellaswag/config/", f"m-hellaswag-{model}-{lang}-gen.json")
            data = copy.deepcopy(origin_data)
            data['task_name'] = f'm-hellaswag_{model}_{lang}'
            data['path'] = f"datasets/m-hellaswag/data/{lang}.jsonl"
            data['transform'] = f"datasets/m-hellaswag/transform_gen_{model}_{lang}.py"
            data['fewshot'] = 0
            data['generate']['params'] = "models/model_params/vllm_sample.json"
            data['metric']['accuracy']['evaluation']['type'] = 'qa_match'
            data['generate']['method'] = "generate"
            with open(output_path, 'w') as f:
                json.dump(data, f)
                
    input_path = "/home/wanghaoyu/UltraEval/datasets/m-hellaswag/"
    
    templates = {
        'okapi': r"[INST] {text} [/INST]",
        'null': r"{text}"
    }


    instructions = {
        "en": r'''"Context:\n {data['question']}\nQuestion:\nWhich ending makes the most sense?\nRequirement:\nChoose and respond with the letter of the correct answer, including the parentheses.\nOptions:\n"''',
        'zh': r'''"背景：\n {data['question']}\n问题：\n哪个结尾最合理？\n要求：\n选择并回答正确答案的字母，包括括号。\n选项：\n"''',
        'es': r'''"Contexto:\n {data['question']}\nPregunta:\n¿Qué final tiene más sentido?\nRequisito:\nElige y responde con la letra de la respuesta correcta, incluyendo el paréntesis.\nOpciones:\n"''',
        'fr': r'''"Contexte:\n {data['question']}\nQuestion:\nQuelle est la fin la plus logique?\nExigence:\nChoisissez et répondez avec la lettre de la bonne réponse, y compris les parenthèses.\nOptions:\n"''',
        'ru': r'''"Контекст:\n {data['question']}\nВопрос:\nКакая концовка имеет наибольший смысл?\nТребования:\nВыберите и укажите букву правильного ответа, включая скобки.\nОпции:\n"''',
    }
    
    lead_in = {
        "en": r"Answer:\n",
        'zh': r"答案：\n",
        'es': r"Respuesta:\n",
        'fr': r"Answer:\n",   
        'ru': r"Ответ:\n"
    }

    for lang in lang_list:
        for model in model_list:
            text = templates[model]
            origin_code = f'''
import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    options = ""
    for idx, item in enumerate(data["target_scores"].keys()):
        options += f"({{chr(65 + idx)}}) {{item}}\\n"
    text = f{instructions[lang]} + options
    text = f"""{templates[model]}""" + "{lead_in[lang]}"
    index_of_correct_answer = list(data["target_scores"].values()).index(1)
    correct_answer = chr(65 + index_of_correct_answer)
    if correct_answer == "A":
        correct_answer = ["A","А"]
    elif correct_answer == "B":
        correct_answer = ["B","Б"]
    elif correct_answer == "C":
        correct_answer = ["C","В","С"]
    elif correct_answer == "D":
        correct_answer = ["D","Д"]
    new = []

    for c in correct_answer:
        new.append(f'({{c}})')
    correct_answer = new
    processed_correct_answer = correct_answer
    return {{
        "input": text,
        "output": correct_answer,
        "processed_output": processed_correct_answer,
    }}

    '''
            output_path = os.path.join(input_path, f"transform_gen_{model}_{lang}.py")  
            with open(output_path, 'w') as f:
                f.write(origin_code)
                
if __name__ == '__main__':
    # make_belebele_config()
    # make_xwinograd_config()
    make_mgsm_config()
    make_omgeval_config()
    make_humaneval_config()
    make_marc_config()
    make_mhellaswag_config()
    make_mmlu_config()