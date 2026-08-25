from __future__ import annotations

import argparse
import json
from pathlib import Path

from agents.extractor_agent import ExtractorAgent
from agents.skill_agent import SkillAgent
from agents.suggestion_agent import SuggestionAgent
from agents.weakness_agent import WeaknessAgent
from models.resume import ResumeAnalysis
from services.pdf_service import PDFService
from services.text_cleaner import TextCleaner


def analyze_resume(pdf_path: str, job_description: str | None = None, use_llm: bool = True) -> ResumeAnalysis:
    pdf = PDFService()
    cleaner = TextCleaner()
    extractor = ExtractorAgent()
    skill_agent = SkillAgent()
    weakness_agent = WeaknessAgent()
    suggestion_agent = SuggestionAgent()

    text = cleaner.clean(pdf.extract_text(pdf_path))
    if not text:
        raise ValueError("No readable text was extracted from the PDF.")

    resume = extractor.extract(text, use_llm=use_llm)
    skill_match = skill_agent.analyze(resume, job_description)
    weaknesses = weakness_agent.analyze(resume, text)

    return ResumeAnalysis(
        resume=resume,
        score=suggestion_agent.score(resume, weaknesses),
        strengths=suggestion_agent.strengths(resume),
        weaknesses=weaknesses,
        suggestions=suggestion_agent.suggest(resume, weaknesses, skill_match),
        skill_match=skill_match,
        metadata={
            "pdf_path": str(Path(pdf_path)),
            "word_count": len(text.split()),
            "llm_requested": use_llm,
        },
    )


def render_markdown(analysis: ResumeAnalysis) -> str:
    resume = analysis.resume
    lines = [
        "# Resume Analysis",
        "",
        f"**Candidate:** {resume.name or 'Not detected'}",
        f"**Score:** {analysis.score}/100",
        f"**Email:** {resume.email or 'Not detected'}",
        f"**Phone:** {resume.phone or 'Not detected'}",
        "",
        "## Strengths",
        *format_items(analysis.strengths),
        "",
        "## Weaknesses",
        *format_items(analysis.weaknesses),
        "",
        "## Suggestions",
        *format_items(analysis.suggestions),
        "",
        "## Skills",
        *format_items(resume.skills),
    ]

    if analysis.skill_match.missing_from_job_description:
        lines.extend([
            "",
            "## Missing Skills From Job Description",
            *format_items(analysis.skill_match.missing_from_job_description),
        ])

    if resume.projects:
        lines.extend(["", "## Projects"])
        lines.extend(format_items([f"{project.name}: {project.description}" for project in resume.projects]))

    if resume.experience:
        lines.extend(["", "## Experience"])
        lines.extend(format_items([f"{item.role} {f'at {item.company}' if item.company else ''}".strip() for item in resume.experience]))

    return "\n".join(lines)


def format_items(items: list[str]) -> list[str]:
    return [f"- {item}" for item in items] if items else ["- None detected."]


def read_job_description(path_or_text: str | None) -> str | None:
    if not path_or_text:
        return None

    path = Path(path_or_text)
    if path.exists():
        return path.read_text(encoding="utf-8")
    return path_or_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze a resume PDF and generate improvement suggestions.")
    parser.add_argument("pdf", nargs="?", default="data/resume.pdf", help="Path to the resume PDF.")
    parser.add_argument("--job", help="Target job description text, or path to a text file.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of Markdown.")
    parser.add_argument("--no-llm", action="store_true", help="Disable Groq parsing even when GROQ_API_KEY is set.")
    parser.add_argument("--output", "-o", help="Write the report to this file.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    analysis = analyze_resume(args.pdf, read_job_description(args.job), use_llm=not args.no_llm)
    report = analysis.model_dump_json(indent=2) if args.json else render_markdown(analysis)

    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")

    print(report)

if __name__ == "__main__":
    main()
