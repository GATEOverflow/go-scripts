from mlc import utils
import os
import json
import google.generativeai as genai
import time

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def ask_gemini(question, options_dict, model):
    options_text = "\n".join([f"{k}. {v}" for k, v in options_dict.items()])
    prompt = f"""Assuming you have know topics covered in GATE CS Exam syllabus in detail, answer the following question with no explanation.
    Question: {question}
    Options:
    {options_text}

    If MCQ, Respond with only the letter of the correct option (A, B, C, or D),
    else if MSQ, respond with the letter(s) of the correct option(s) (A, B, C, or D) separated by a semicolon (;), no spaces,
    else if NAT, respond with the number only, no explanation just the final answer value (e.g., 4 or 1.8).
    """
    # For any question if you are not sure about the answer or did not understand the question or if you feel the question is incomplete or wrong, you can skip the question by leaving the question and move on.
    response = model.generate_content(prompt)
    answer = response.text.strip().upper()
    return answer

def preprocess(i):
    env = i['env']
    automation = i['automation']
    marks = 0
    # Configure Gemini
    genai.configure(api_key=env['GEMINI_API_KEY'])
    model = genai.GenerativeModel(model_name=env.get('MLC_GEMINI_MODEL', 'models/gemini-1.5-flash'))

    # Load questions
    questions_file = env.get('MLC_GATE_QUESTIONS_JSON_FILE_PATH', '/home/sujith/MLC/repos/gateoverflow@go-scripts/data/CS25Set2.json')
    with open(questions_file, 'r') as f:
        questions = json.load(f)

    results = []
    for q in questions:
        # print("\n*******************************************************************************************************\n")
        # print(f"Processing Q{q['question_number']}...")
        # print(f"Question: {q['question']}")
        # print(f"Options: {q['options']}")
        # print(f"Answer: {q['answer']}")
        # model_answer = ask_gemini(q["question"], q["options"], model)
        # if q["type"] != "MCQ":  # For now, only MCQs
        #     continue
        model_answer = ask_gemini(q["question"], q["options"], model)
        if isinstance(q["answer"], list):
            correct_answer = ";".join([ans.strip().upper() for ans in q["answer"]])  # Join MSQ answers with ';'
        else:
            correct_answer = q["answer"].strip().upper()  # Handle MCQ/NAT answers

        is_correct = model_answer == correct_answer

        results.append({
            "question_number": q["question_number"],
            "model_answer": model_answer,
            "correct_answer": correct_answer,
            "type": q["type"],
            "is_correct": is_correct,
        })
        # Marks
        marks = q.get("marks", 0)  # Default to 0 if "marks" is missing
        if is_correct:
            marks += q.get("marks", 0)  # Add full marks if the answer is correct
        else:
            if q["type"] == "MCQ":
                if q.get("marks", 0) == 1:
                    marks -= 0.33
                elif q.get("marks", 0) == 2:
                    marks -= 0.67
            elif q["type"] == "MSQ":
                marks += 0  # No negative marking for MSQ
            elif q["type"] == "NAT":
                marks += 0  # No negative marking for NAT
        print(f"Q{q['question_number']}: Model: {model_answer}, Correct: {correct_answer} — {'[✓]' if is_correct else '[x]'}")
        time.sleep(1)  # Avoid rate limits

    i['state']['output'] = results
    return {'return': 0}

def postprocess(i):
    state = i['state']
    results = state['output']

    correct = sum(1 for r in results if r['is_correct'])
    wrong = len(results) - correct
    accuracy = 100 * correct / len(results) if results else 0

    # Save results with checksum
    results_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "results")
    os.makedirs(results_dir, exist_ok=True)
    
    output_file = os.path.join(results_dir, f"gemini_results.json")
    with open(output_file, "w") as f:
        json.dump({
            "results": results,
            "summary": {
                "correct": correct,
                "wrong": wrong,
                "total": len(results),
                "total_marks": sum(q.get("marks", 0) for q in results),
                "accuracy": accuracy
            },
        }, f, indent=2)

    print(f"Results saved to: {output_file}")
    print(f"Correct: {correct}, Wrong: {wrong}, Total: {len(results)}")
    print(f"Accuracy: {accuracy:.2f}%")

    return {'return': 0}