import re
import json
from pathlib import Path
import pdfplumber

BASE = Path(__file__).resolve().parent.parent
CV = BASE / 'anish_cv (9).pdf'
OUT = BASE / 'data'
OUT.mkdir(exist_ok=True)

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
    # heuristic: first non-empty line
    for line in text.splitlines():
        s = line.strip()
        if s:
            # ignore lines that look like addresses or headings
            if re.search(r'\bCurriculum Vitae\b|Resume|Email|Phone|Address', s, re.I):
                continue
            # return first short line
            if 2 <= len(s.split()) <= 4 and len(s) < 60:
                return s
    return None

def split_sections(text):
    # naive split by common headings
    headings = ['Education','Research','Projects','Publications','Experience','Skills','Contact','Areas of interest','Interests']
    pattern = '|'.join([fr'(?m)^\s*{h}\b' for h in headings])
    parts = re.split(pattern, text)
    # re.split drops the separators; collect by searching headings
    sections = {}
    for h in headings:
        m = re.search(fr'(?s){h}(.+?)(?=(?:\n[A-Z][a-zA-Z ]{{1,40}}:|\Z))', text)
        if m:
            sections[h.lower()] = m.group(1).strip()
    return sections

def extract_education(sec_text):
    if not sec_text: return []
    lines = [l.strip() for l in sec_text.splitlines() if l.strip()]
    items = []
    for l in lines[:8]:
        # look for years
        if re.search(r'\b(19|20)\d{2}\b', l):
            items.append(l)
        elif len(l) > 30:
            items.append(l)
    return items

def extract_projects(sec_text):
    if not sec_text: return []
    paras = [p.strip() for p in sec_text.split('\n\n') if p.strip()]
    return paras[:6]

def main():
    print('Reading PDF...')
    text = extract_text(CV)
    name = find_name(text) or 'Anish Mulay'
    email = find_email(text) or 'your.email@example.com'
    sections = split_sections(text)
    education = extract_education(sections.get('education',''))
    projects = extract_projects(sections.get('projects','') or sections.get('research',''))

    data = {
        'name': name,
        'email': email,
        'education': education,
        'projects': projects,
        'raw_text_snippet': text[:300]
    }

    OUT.joinpath('parsing.json').write_text(json.dumps(data, indent=2, ensure_ascii=False))
    print('Wrote', OUT.joinpath('parsing.json'))

    # Also write HTML snippets for quick injection
    edu_html = '\n'.join([f"<div class=\"item\"><h3>{e.split(',')[0]}</h3><p class=\"muted small\">{e}</p></div>" for e in education])
    proj_html = '\n'.join([f"<article class=\"project\"><h3>{p.split('\n')[0][:60]}</h3><p>{p}</p></article>" for p in projects])
    OUT.joinpath('education.html').write_text(edu_html)
    OUT.joinpath('projects.html').write_text(proj_html)
    print('Wrote HTML snippets')

if __name__ == '__main__':
    main()
