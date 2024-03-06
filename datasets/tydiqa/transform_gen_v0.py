import random

from UltraEval.tasks.postprocess import ExactMatchPost

_prompt = {
    "english":["Answer the following question based on the information in the given passage.\n\nPassage:", "\nQuestion: ", "\nAnswer:" ],
    "arabic":["الرجاء الإجابة على السؤال التالي استنادًا إلى المعلومات الموجودة في المقطع التالي.\n\nالمقطع:","\nالسؤال:","\nالجواب:"],
    "russian":["Ответьте на следующий вопрос, опираясь на информацию, содержащуюся в данном отрывке.\n\nОтрывок:","\nВопрос:","\nОтвет:"]
}

def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    prompt = _prompt[data["language"]]
    text = prompt[0] + f"{data['passage'][1]}"+ prompt[1] +f"{data['question']}" + prompt[2]
    correct_answer = data["answer"]
    emp = ExactMatchPost()
    _, processed_correct_answer = emp([], correct_answer)

    return {
        "input": text,
        "output": correct_answer,
        "processed_output": processed_correct_answer,
    }