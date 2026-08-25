# Resume Analyzer

A Python command-line resume analyzer that reads a PDF resume, extracts structured
details, scores the resume, identifies weaknesses, and suggests improvements.

The project works offline with a rule-based parser. If `GROQ_API_KEY` is available
in `.env`, it can use Groq for richer structured extraction and automatically falls
back to the local parser if the LLM call fails.

## Features

- Extract text from PDF resumes with PyMuPDF.
- Clean resume text before analysis.
- Parse contact details, education, experience, projects, skills, certifications,
  and achievements.
- Score resume completeness and quality.
- Detect missing or weak areas.
- Compare resume skills with a target job description.
- Print Markdown or JSON reports.
- Save reports to a file.

## Setup

```powershell
pip install -r requirements.txt
```

Optional `.env`:

```env
GROQ_API_KEY=your_key_here
MODEL=llama-3.1-8b-instant
TEMPERATURE=0
```

## Usage

Analyze the sample resume:

```powershell
python main.py
```

Analyze a specific PDF:

```powershell
python main.py path\to\resume.pdf
```

Use a target job description:

```powershell
python main.py path\to\resume.pdf --job path\to\job_description.txt
```

Generate JSON:

```powershell
python main.py path\to\resume.pdf --json
```

Save a report:

```powershell
python main.py path\to\resume.pdf --output report.md
```

Force offline mode:

```powershell
python main.py path\to\resume.pdf --no-llm
```
