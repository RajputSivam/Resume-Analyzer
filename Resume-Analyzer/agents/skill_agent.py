from __future__ import annotations

import re

from models.resume import Resume, SkillMatch


class SkillAgent:
    CATEGORIES = {
        "Programming": {"python", "java", "c++", "c", "javascript", "typescript", "sql"},
        "Web": {"html", "css", "react", "node.js", "django", "flask", "fastapi", "rest api"},
        "Data/ML": {
            "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "machine learning",
            "deep learning", "nlp", "opencv", "data analysis", "data visualization",
        },
        "Tools/Cloud": {"git", "docker", "aws", "azure", "gcp", "power bi", "tableau", "excel"},
        "Databases": {"mysql", "postgresql", "mongodb"},
    }

    def analyze(self, resume: Resume, job_description: str | None = None) -> SkillMatch:
        normalized_skills = {skill.lower(): skill for skill in resume.skills}
        categories: dict[str, list[str]] = {}

        for category, keywords in self.CATEGORIES.items():
            matched = [original for key, original in normalized_skills.items() if key in keywords]
            if matched:
                categories[category] = sorted(matched)

        missing = self._missing_job_skills(normalized_skills, job_description or "")
        return SkillMatch(found=sorted(resume.skills), missing_from_job_description=missing, categories=categories)

    def _missing_job_skills(self, resume_skills: dict[str, str], job_description: str) -> list[str]:
        if not job_description.strip():
            return []

        missing: list[str] = []
        all_keywords = sorted(set().union(*self.CATEGORIES.values()))
        for keyword in all_keywords:
            if re.search(rf"\b{re.escape(keyword)}\b", job_description, re.IGNORECASE) and keyword not in resume_skills:
                missing.append(keyword.title() if keyword.islower() else keyword)
        return missing
