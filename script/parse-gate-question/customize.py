from mlc import utils
import pdfplumber
import json
import re
import os
import warnings

warnings.filterwarnings("ignore", message=".*CropBox missing.*")
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", message=".*CropBox.*", category=UserWarning)
warnings.filterwarnings("ignore", message=".*CropBox.*", module="pdfminer.*")

# Step 1: Extract all text from PDFs
def extract_text(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
    
# Clean the questions and answers text
def clean_text(text: str) -> str:
    """Clean and format text properly"""
    # Replace special symbols 
    text = text.replace("(cid:46)(cid:47)", "⋈")  # Join symbol
    text = text.replace("(cid:107)", "‖")  # Norm symbol
    text = text.replace("(cid:88)", "∑")  # Sum symbol
    text = text.replace("(cid:48)", "′")  # Prime symbol
    text = text.replace("(cid:54)", "≠")  # Not equal symbol
    text = text.replace("(cid:62)", "ᵀ")  # Transpose symbol
    text = text.replace("(cid:90)", "∫")  # Integral symbol
    text = text.replace("(cid:98)", "⌊")  # Floor symbol
    text = text.replace("(cid:99)", "⌋")  # Floor symbol
    
    # Add spaces around mathematical operators
    text = re.sub(r'([=<>+\-*/])', r' \1 ', text)
    
    # Remove organizing institute footer
    text = re.sub(r'Organizing Institute:.*?(?=\n|$)', '', text)
    text = re.sub(r'GATE\d+.*?(?=\n|$)', '', text)
    
    # Fix spacing
    text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
    text = text.replace('\\n', '\n')  # Preserve intended line breaks
    text = re.sub(r'\n\s*\n', '\n', text)  # Remove multiple blank lines
    
    return text.strip()



# Step 2: Parse questions and answers into dictionary
# Step 2: Parse answers into dictionary
def parse_answers(answer_text):
    answers = {}
    for line in answer_text.splitlines():
        match = re.match(r"^(\d+)\s+\d+\s+\w+\s+\S+\s+(.*)\s+\d$", line)
        if match:
            qid = f"Q{match.group(1)}"
            answer = match.group(2) or match.group(3)
            if ";" in answer:  # MSQ
                answers[qid] = answer.split(";")
            elif re.match(r"^[A-D]$", answer):  # MCQ
                answers[qid] = answer
            else:  # NAT
                answers[qid] = answer
    return answers

# Step 3: Parse questions
def parse_questions(text, answer_dict):
    # First clean up text blocks
    text = clean_text(text)
    question_blocks = re.findall(r"(Q\.\d+[\s\S]*?)(?=Q\.\d+|\Z)", text)
    questions = []

    for block in question_blocks:
        q_match = re.match(r"Q\.(\d+)\s+(.*)", block.strip(), re.DOTALL)
        if not q_match:
            continue

        q_number = int(q_match.group(1))
        qid = f"Q{q_number}"
        content = q_match.group(2).strip()

        # Extract question text before options
        question_text = re.split(r'\([A-D]\)', content)[0].strip()
        question_text = clean_text(question_text)

        # Extract options with better formatting
        options = {}
        option_matches = re.findall(r'\(([A-D])\)\s*([^(]+)(?=\([A-D]\)|$)', content)
        for opt, text in option_matches:
            options[opt] = clean_text(text)
        
        # Skip meta text or garbage
        if question_text in {"–", "", "Carry ONE mark Each", "Carry TWO marks Each"}:
            continue

        # Get the answer (if available)
        answer = answer_dict.get(qid, None)

        # Determine type from answer
        if isinstance(answer, list):
            qtype = "MSQ"
        elif isinstance(answer, str) and re.match(r"^[A-D]$", answer):
            qtype = "MCQ"
        elif answer is not None:
            qtype = "NAT"
        else:
            qtype = "Unknown"
        
        # Determine marks based on question number
        if 1 <= q_number <= 5 or 11 <= q_number <= 35:
            marks = 1
        elif 6 <= q_number <= 10 or 36 <= q_number <= 65:
            marks = 2
        else:
            marks = 1  # default fallback


        questions.append({
            "question_number": q_number,
            "question": question_text,
            "options": options,
            "type": qtype,
            "marks": marks,
            "answer": answer
        })

    return questions

def preprocess(i):
    env = i['env']
    mlc_repo_path = env.get('MLC_REPO_PATH', '')
    # Get input paths from environment
    question_pdf = env.get('MLC_GATE_QUESTION_PDF_PATH', '/home/sujith/MLC/repos/gateoverflow@go-scripts/data/paper.pdf')
    answer_pdf = env.get('MLC_GATE_ANSWER_PDF_PATH', '/home/sujith/MLC/repos/gateoverflow@go-scripts/data/key.pdf')
    
    # Extract and clean text
    qtext = extract_text(question_pdf)
    cleaned_qtext = clean_text(qtext)
    atext = extract_text(answer_pdf)
    cleaned_atext = clean_text(atext)
    
    # Parse answers and questions
    answer_key = parse_answers(cleaned_atext)
    questions = parse_questions(cleaned_qtext, answer_key)
    
    # Store in state
    i['state']['questions'] = questions
    i['state']['answers'] = answer_key
    
    return {'return': 0}

def postprocess(i):
    env = i['env']
    state = i['state']
    
    questions = state['questions']
    output_path = env.get('MLC_GATE_OUTPUT_JSON_PATH', '/home/sujith/MLC/repos/gateoverflow@go-scripts/data/output.json')
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save to JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
    
    print(f"Generated {output_path} with {len(questions)} questions.")
    
    return {'return': 0}
