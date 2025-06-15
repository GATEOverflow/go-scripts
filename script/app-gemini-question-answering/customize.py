import os
import json
import google.generativeai as genai
import time
from dotenv import load_dotenv
load_dotenv()

def ask_gemini(question, options_dict, model, q_type):
    options_text = "\n".join([f"{k}. {v}" for k, v in options_dict.items()]) if options_dict else ""

    if q_type == "MCQ":
        prompt = f""""Assume you are an expert in Computer Science and Engineering fundamentals, especially the subjects typically covered in a Bachelor's degree in Computer Science like:
        Data Structures, Algorithms, Operating Systems, Computer Networks, Databases, Theory of Computation, Digital Logic, Computer Architecture, Compiler Design, Discrete Mathematics, Linear Algebra, Probability, and Genral Aptitude.

        Answer the following question based on your deep subject knowledge. Do not give explanation, just the final answer.
        Solve the following multiple choice question carefully.

        Question: {question}

        Options:
        {options_text}

        Choose the **one correct option** among A, B, C, or D.
        Respond with only the **option letter** (A, B, C, or D). Do **not** provide any explanation."""
    
    elif q_type == "MSQ":
        prompt = f"""Assume you are an expert in Computer Science and Engineering fundamentals, especially the subjects typically covered in a Bachelor's degree in Computer Science like:
        Data Structures, Algorithms, Operating Systems, Computer Networks, Databases, Theory of Computation, Digital Logic, Computer Architecture, Compiler Design, Discrete Mathematics, Linear Algebra, Probability and Genral Aptitude.

        Answer the following question based on your deep subject knowledge. Do not give explanation, just the final answer.
        Solve the following multiple select question carefully.

        Question: {question}

        Options:
        {options_text}

        Choose **all correct options** from A, B, C, or D. There may be more than one correct answer.

        Respond using **only the letters of correct options**, separated **strictly by semicolons (;)**, and **no spaces**.
        For example: A;C or B;C;D
        Do **not** provide any explanation."""

    elif q_type == "NAT":
        prompt = f"""Assume you are an expert in Computer Science and Engineering fundamentals, especially the subjects typically covered in a Bachelor's degree in Computer Science like:
        Data Structures, Algorithms, Operating Systems, Computer Networks, Databases, Theory of Computation, Digital Logic, Computer Architecture, Compiler Design, Discrete Mathematics, Linear Algebra, Probability and Genral Aptitude.

        Answer the following question based on your deep subject knowledge. Do not give explanation, just the final answer. If the question allows decimals, round the answer to **1 or 2 decimal places** as appropriate.
        Example: 4 or 1.8 or 23.67
        Solve the following numerical answer type (NAT) question carefully and confidentally. Do not ask for clarification or provide any explanation.

        Question: {question}

        Provide **only the final numeric answer** with **no units and no explanation**."""

    else:
        raise ValueError("Invalid question type. Choose from 'MCQ', 'MSQ', or 'NAT'.")

    response = model.generate_content(prompt)
    answer = response.text.strip().upper()

    if q_type == "MSQ":
        # Normalize MSQ answers
        answer = answer.replace(",", ";").replace(" ", "")
        if all(c in "ABCD;" for c in answer) and ";" not in answer and len(answer) > 1:
            answer = ";".join(answer)

    return answer


def geminiProcess(i):
    env = i['env']
    marks = 0
    marksObtained = 0
    negativeMarks = 0
    mcqCorrect = 0
    mcqWrong = 0
    msqCorrect = 0
    msqWrong = 0
    natCorrect = 0
    natWrong = 0
    totalMarks = 0
    total_sleep_time = 0
    process_start = time.time()
    # Configure Gemini
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set in environment or .env file!")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name=env.get('MLC_GEMINI_MODEL', 'models/gemini-1.5-flash'))

    # Load questions
    questions_file = os.path.expanduser(env.get('MLC_GATE_OUTPUT_JSON_PATH', '~/MLC/repos/local/cache/gate-exam-data/output.json'))
    with open(os.path.expanduser(questions_file), 'r') as f:
       questions = json.load(f)

    results = []
    cnt = 0
    print("------------------------------------------------------------------------------------------------------------------------------------")
    for q in questions:
        print(f"Processing Q{q['question_number']}..")
        # print(f"Question: {q['question']}")
        # print(f"Options: {q['options']}")
        # print(f"Answer: {q['answer']}")
        model_answer = ask_gemini(q["question"], q["options"], model, q["type"])
        if isinstance(q["answer"], list):
            correct_answer = ";".join([ans.strip().upper() for ans in q["answer"]])  # Join MSQ answers with ';'
        else:
            correct_answer = q["answer"].strip().upper()  # Handle MCQ/NAT answers

        #Evaluate Model's Answer
        if q["type"] == "NAT" and isinstance(q["answer"], str) and "TO" in q["answer"].upper():
        # Handle NAT range answers like "0.5 TO 0.6"
            try:
                a, b = [float(x.strip()) for x in q["answer"].upper().split("TO")]
                # print(f"a = {a}, b = {b}")
                try:
                    model_ans_float = float(model_answer)
                    # Use round to avoid floating point issues, or use a small epsilon if needed
                    is_correct = a <= model_ans_float <= b
                except ValueError:
                    print(f"Model answer '{model_answer}' could not be converted to float.")
                    is_correct = False  # Model answer is not a number
            except Exception as e:
                print(f"Error parsing NAT range: {e}")
                is_correct = False  # Fallback if parsing fails
        else:
            is_correct = model_answer == correct_answer

        # Marks
        # marks = q.get("marks", 0)  # Default to 0 if "marks" is missing
        totalMarks += q.get("marks",0)
        if is_correct:
            marks = q.get("marks", 0)  # Add full marks if the answer is correct
            if q["type"] == "MCQ":
                mcqCorrect += 1
            if q["type"] == "MSQ":
                msqCorrect += 1
            if q["type"] == "NAT":
                natCorrect += 1    
        else:
            if q["type"] == "MCQ":
                mcqWrong += 1
                if q.get("marks", 0) == 1:
                    marks = -0.33
                    negativeMarks += 0.33
                elif q.get("marks", 0) == 2:
                    marks = -0.67
                    negativeMarks += 0.67
            elif q["type"] == "MSQ":
                marks = 0  # No negative marking for MSQ
                msqWrong += 1
            elif q["type"] == "NAT":
                marks = 0  # No negative marking for NAT
                natWrong += 1
        marksObtained += marks
        # Print results        
        print(f"Q{q['question_number']}: Model: {model_answer}, Correct: {correct_answer} — {'[✓]' if is_correct else '[x]'}")
        # Marks of question, and mark obtained for the question
        print(f"Marks for the question:" f" {q.get('marks', 0)} (Marks recieved: {marks} )")
        print(f"Type: {q['type']}")
        # Save result to results json file
        results.append({
            "question_number": q["question_number"],
            "model_answer": model_answer,
            "correct_answer": correct_answer,
            "type": q["type"],
            "is_correct": is_correct,
            "marks": marks,
        })
        print("------------------------------------------------------------------------------------------------------------------------------------")
        cnt+=1
        if cnt%10==0:
            print("Pause of 1 min due to rate limiting")
            sleep_start = time.time()
            for remaining in range(60, 0, -1):
                print(f"\rResuming in {remaining} seconds...", end="", flush=True)
                time.sleep(1)
            sleep_end = time.time()
            total_sleep_time += (sleep_end - sleep_start)
            print("Resuming now!")
            print("********************************************************************************************************************************")

    i['state']['output'] = results
    process_end = time.time()
    total_time = process_end - process_start
    effective_time = total_time - total_sleep_time
    # marks 
    print(f"Results for {env.get('MLC_GEMINI_MODEL', 'gemini-1.5-flash')}:")
    print("*******************************************************")
    print(f"Marks Obtained by {model.model_name} is {marksObtained} out of total {totalMarks} marks")
    print(f"# MCQ Correct: {mcqCorrect}, Wrong: {mcqWrong}")
    print(f"# MSQ Correct: {msqCorrect}, Wrong: {msqWrong}")
    print(f"# NAT Correct: {natCorrect}, Wrong: {natWrong}")
    print(f"Total Questions: {len(questions)}")
    print(f"Negative Marks: {negativeMarks}")
    print(f"Total Marks Obtained: {marksObtained:.2f}")
    print(f"Total Marks: {totalMarks}")
    print(f"Total Time Taken: {total_time:.2f} seconds (Effective Time: {effective_time:.2f} seconds, Sleep Time: {total_sleep_time:.2f} seconds)")
    print("*****************************************************************************************************************************************")
    return {'return': 0}

def resultProcess(i):
    state = i['state']
    results = state['output']

    correct = sum(1 for r in results if r['is_correct'])
    wrong = len(results) - correct
    accuracy = 100 * correct / len(results) if results else 0

    # Save results in a JSON file
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
    print("*********************************************************************************************************************************")
    print(f"Results saved to: {output_file}")
    print("*********************************************************************************************************************************")
    print("Summary of results:")
    print("*********************************************************************************************************************************")
    print(f"Correct: {correct}, Wrong: {wrong}, Total: {len(results)}")
    print("---------------------")
    print(f"| Accuracy: {accuracy:.2f}%  |")
    print("---------------------")
    return {'return': 0}

if __name__ == "__main__":
    i = {'env': os.environ, 'state': {}}
    geminiProcess(i)
    resultProcess(i)
