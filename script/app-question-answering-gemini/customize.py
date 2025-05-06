from mlc import utils
import os
import json
import csv
import time
from datetime import datetime
def preprocess(i):
    env = i['env']
    automation = i['automation']
    os_info = i['os_info']
    mlc = automation.action_object

    questions_file = env['MLC_GATE_QUESTIONS_JSON_FILE_PATH']
    with open(questions_file, 'r') as f:
        questions = json.load(f)

    gemini_model = env.get('MLC_GEMINI_MODEL', 'gemini-2.0-flash')
    gemini_api_key = env['MLC_GEMINI_API_KEY']

    system_prompt = """You are an expert GATE Computer Science assistant. For every question, provide only the final answer in a strict format:

- For MCQ (Single Correct): respond with a single uppercase letter — A, B, C, or D.
- For MSQ (Multiple Select): respond with multiple uppercase letters separated by semicolons (e.g., A;C;D). No spaces.
- For NAT (Numerical Answer Type): respond with a number (e.g., 42 or 2.56).

Do not include any explanation, reasoning, labels, prefixes like "Answer:", or extra text. Output only the answer key in the required format.
"""

    outs = []
    state = {}
    count = 1
    for question in questions:
        question_content = question['content'].replace('"', '\\"')
        user_prompt = f"""Question Text: {question_content}, Question Type: {question['question_type']}"""
        state['user_prompt'] = user_prompt
        state['system_prompt'] = system_prompt
        print(f"Analyzing question: #######{count+1}\n")
        r = mlc.access({
            'action': 'run',
            'target': 'script',
            'tags': 'query,gemini-call',
            'state': state,
            'api_key': gemini_api_key,
            'model': gemini_model
        })

        if r['return'] > 0:
            return r

        predicted_key = r['new_state']['MLC_GEMINI_RESPONSE']
        outs.append({
            'Question Title': question['title'],
            'Question Type': question['question_type'],
            'Actual Key': question['answer'],
            'Predicted': predicted_key.rstrip('\n')

        })
        count += 1
        if count%15==0:
            print("Pause of 1 minute due to rate limiting")
            time.sleep(60)    

    i['state']['output'] = outs

    script_dir = os.path.dirname(os.path.abspath(__file__))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"gemini_results_{timestamp}.csv"
    csv_path = os.path.join(script_dir, csv_filename)


    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Question Title', 'Question Type', 'Actual Key', 'Predicted'])
        writer.writeheader()
        writer.writerows(outs)

    return {'return': 0}


def postprocess(i):
    state = i['state']
    env = i['env']
    gemini_model = env.get('MLC_GEMINI_MODEL', 'gemini-2.0-flash')
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

    print(f""" Correct: {correct}, Wrong: {wrong}, Total: {len(output)}""")
    accuracy = correct/(correct+wrong)
    print(f"""The accuracy of {gemini_model} is, {accuracy}""")
    
    return {'return': 0}
