import re
import json
from pathlib import Path
import pdfplumber

BASE = Path(__file__).resolve().parent.parent
CV = BASE / 'anish_cv (9).pdf'

def extract_text(pdf_path):
    text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text.append(t)
    return "\n\n".join(text)

def find_email(text):
    m = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    return m.group(0) if m else None

def find_name(text):
    for line in text.splitlines():
        s = line.strip()
        if s and len(s.split())<=4 and len(s)<60 and not re.search(r'Email|Phone|Curriculum|Resume', s, re.I):
            return s
    return 'Anish Mulay'

def extract_sections(text):
    # crude heuristics for education and projects
    edu = []
    proj = []
    # find lines that contain degree keywords
    for line in text.splitlines():
        l = line.strip()
        if not l: continue
        if re.search(r'B\.?Sc|Bachelors|Bachelor|M\.?Sc|Master|Ph\.?D|PhD|Doctor', l, re.I):
            edu.append(l)
        if re.search(r'project|implemented|developed|paper|publication', l, re.I):
            proj.append(l)
    return edu[:5], proj[:6]

def main():
    text = extract_text(CV)
    name = find_name(text)
    email = find_email(text) or ''
    education, projects = extract_sections(text)
    out = {
        'name': name,
        'email': email,
        'education': education,
        'projects': projects,
        'text_head': text[:800]
    }
    print(json.dumps(out, indent=2, ensure_ascii=False))

if __name__=='__main__':
    main()
