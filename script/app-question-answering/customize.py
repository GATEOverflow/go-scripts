from mlc import utils
import os
import subprocess
import json

def preprocess(i):

    env = i['env']
    automation = i['automation']
    os_info = i['os_info']
    mlc = automation.action_object

    questions_file = env['MLC_GATE_QUESTIONS_JSON_FILE_PATH']
    with open(questions_file, 'r') as f:
        questions = json.load(f)
    
    openai_model = env.get('MLC_OPENAI_MODEL', 'gpt-4.1')
    openai_api_key = env['MLC_OPENAI_API_KEY']
    system_prompt = """You are an expert GATE Computer Science assistant. For every question, provide only the final answer in a strict format:

- For MCQ (Single Correct): respond with a single uppercase letter — A, B, C, or D.
- For MSQ (Multiple Select): respond with multiple uppercase letters separated by semicolons (e.g., A;C;D). No spaces.
- For NAT (Numerical Answer Type): respond with a number (e.g., 42 or 2.56).

Do not include any explanation, reasoning, labels, prefixes like "Answer:", or extra text. Output only the answer key in the required format.
"""
    outs = []
    state= {}
    count = 0
    for question in questions:
        question_content = question['content'].replace('"', '\\"')
        user_prompt = f"""Question Text: {question_content}, Question Type: {question['question_type']}"""
        state['user_prompt'] = user_prompt
        state['system_prompt'] = system_prompt
        r = mlc.access({'action': 'run',
            'target': 'script',
            'tags': 'query,openai-call',
            'state': state,
            'api_key': openai_api_key,
            'model': openai_model
            })
        if r['return'] > 0:
            return r
        predicted_key = r['new_state']['MLC_OPENAI_RESPONSE']
        outs.append({'Question Title': question['title'], 'Question Type': question['question_type'], 'Actual Key': question['answer'], 'Predicted': predicted_key})
        count += 1
        if count > 20:
            break

    #print(outs)
    i['state']['output'] = outs
    return {'return': 0}


def postprocess(i):

    env = i['env']
    state = i['state']
    os_info = i['os_info']

    output = state['output']
    correct = 0
    wrong = 0
    for out in output:
        if out['Actual Key'] == out['Predicted']:
            correct += 1
        elif out['Question Type'] == 'NAT':
            pred = out['Predicted']
            act = out['Actual Key'].split(":")
            try:
                pred_num = float(pred)
                low = float(act[0])
                high = float(act[1]) if len(act) > 1 else low
                c = low <= pred_num <= high
                if c:
                    correct += 1
                else:
                    wrong += 1

            except ValueError:
                wrong += 1
        else:
            wrong += 1

    print(output)
    print(f""" Correct: {correct}, Wrong: {wrong}, Total: {len(output)}""")
    return {'return': 0}
