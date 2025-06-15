import pdfplumber
import requests
import json
import re
import os
import warnings
from dotenv import load_dotenv
load_dotenv()

warnings.filterwarnings("ignore", message=".*CropBox missing.*")

# Step 0: Download paper
def download_pdf(url, local_path):
     # Ensure the directory exists
    os.makedirs(os.path.dirname(os.path.expanduser(local_path)), exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()  # Raises an error for bad status
    with open(local_path, 'wb') as f:
        f.write(response.content)
    print(f"Downloaded File to {local_path}")

# Step 1: Extract all text from PDFs
def extract_text(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
    
# Clean the questions and answers text
def clean_text(text: str) -> str:
    # Remove all lines that are just the CS header
    text = re.sub(r"Computer Science and Information Technology \(CS\d+\)\n?", "", text)

    # Remove lines like: Organising Institute: IIT Roorkee Page X of Y
    text = re.sub(r"Organising Institute: IIT Roorkee Page \d+ of \d+\n?", "", text)
    text = re.sub(r"Organising Institute:.*(?:\n|$)", "", text)

    # Optional: strip excessive blank lines
    text = re.sub(r'\n\s*\n', '\n\n', text)
    

    return text.strip()


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
    question_blocks = re.findall(r"(Q\.\d+[\s\S]*?)(?=Q\.\d+|\Z)", text)
    questions = []

    for block in question_blocks:
        q_match = re.match(r"Q\.(\d+)\s+(.*)", block.strip(), re.DOTALL)
        if not q_match:
            continue

        q_number = int(q_match.group(1))
        qid = f"Q{q_number}"
        content = q_match.group(2).strip()

        # Extract options
        options = dict(re.findall(r"\((A|B|C|D)\)\s*(.*?)(?=\n\(|$)", content, re.DOTALL))

        # Extract question text
        split_match = re.split(r"\(A\)", content)
        question_text = split_match[0].strip() if split_match else content.strip()
        
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

def extractProcess(i):
    env = i['env']

    # Get input paths from environment
    question_pdf = os.path.expanduser(env.get('MLC_GATE_QUESTION_PDF_PATH', '~/MLC/repos/local/cache/gate-exam-data/paper.pdf'))
    answer_pdf = os.path.expanduser(env.get('MLC_GATE_ANSWER_PDF_PATH', '~/MLC/repos/local/cache/gate-exam-data/key.pdf'))

    # Download the paper from site
    questionpdf_url = env.get('MLC_GATE_QUESTION_PDF_URL', "https://github.com/user-attachments/files/20423322/CS25set2-questionPaper.pdf")
    answerpdf_url = env.get('MLC_GATE_ANSWER_PDF_URL', "https://github.com/user-attachments/files/20423320/CS25set2-answerKey.pdf")
    print("Downloading Question Paper PDF ..")
    download_pdf(questionpdf_url, question_pdf)
    print("Downloading Answer Key PDF ..")
    download_pdf(answerpdf_url, answer_pdf)

    # Extract and clean text
    print("Extracting text from PDFs...")
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

def outputProcess(i):
    env = i['env']
    state = i['state']
    
    questions = state['questions']
    output_path = os.path.expanduser(env.get('MLC_GATE_OUTPUT_JSON_PATH', '~/MLC/repos/local/cache/gate-exam-data/output.json'))
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save to JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
    
    print("********************************************************************************************************************************")
    print(f"Generated {output_path} with {len(questions)} questions.")
    print("********************************************************************************************************************************")
    return {'return': 0}

if __name__ == "__main__":
    i = {'env': os.environ, 'state': {}}
    extractProcess(i)
    outputProcess(i)
