from __future__ import annotations

from models.resume import Resume


class WeaknessAgent:
    def analyze(self, resume: Resume, text: str) -> list[str]:
        weaknesses: list[str] = []

        if not resume.email:
            weaknesses.append("Missing email address.")
        if not resume.phone:
            weaknesses.append("Missing phone number.")
        if not resume.links:
            weaknesses.append("No portfolio, GitHub, LinkedIn, or project link found.")
        if not resume.summary:
            weaknesses.append("Missing professional summary or objective.")
        if len(resume.skills) < 6:
            weaknesses.append("Skills section is thin; add more role-relevant tools and technologies.")
        if not resume.experience:
            weaknesses.append("No work experience or internship section detected.")
        if not resume.projects:
            weaknesses.append("No project section detected.")
        if not resume.education:
            weaknesses.append("Education details were not clearly detected.")
        if not any(char.isdigit() for char in text):
            weaknesses.append("Resume lacks numbers or metrics that show impact.")
        if len(text.split()) < 250:
            weaknesses.append("Resume content looks short; add concrete responsibilities, projects, and outcomes.")
        if len(text.split()) > 900:
            weaknesses.append("Resume may be too long; tighten repeated details and prioritize recent impact.")

        return weaknesses
