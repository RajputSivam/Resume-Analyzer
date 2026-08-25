from __future__ import annotations

import re

from models.resume import Education, Experience, Project, Resume


class ParserAgent:
    """Rule-based resume parser used as the reliable offline baseline."""

    SECTION_ALIASES = {
        "summary": {"summary", "profile", "objective", "career objective", "professional summary"},
        "education": {"education", "academic background", "academics"},
        "experience": {"experience", "work experience", "professional experience", "employment"},
        "projects": {"projects", "academic projects", "personal projects"},
        "skills": {"skills", "technical skills", "core skills", "technologies"},
        "certifications": {"certifications", "certificates", "courses"},
        "achievements": {"achievements", "awards", "honors", "accomplishments"},
    }

    DEGREE_RE = re.compile(
        r"\b(b\.?tech|m\.?tech|bachelor|master|b\.?e\.?|m\.?e\.?|bsc|msc|mba|phd|diploma)\b",
        re.IGNORECASE,
    )

    def parse(self, text: str) -> Resume:
        lines = [line.strip(" -\u2022\t") for line in text.splitlines() if line.strip()]
        sections = self._split_sections(lines)

        return Resume(
            name=self._extract_name(lines),
            email=self._first_match(text, r"[\w.+-]+@[\w-]+\.[\w.-]+"),
            phone=self._first_match(text, r"(?:\+?\d[\d\s().-]{8,}\d)"),
            links=self._extract_links(text),
            summary=self._join_first(sections.get("summary", [])),
            education=self._extract_education(sections.get("education", [])),
            experience=self._extract_experience(sections.get("experience", [])),
            projects=self._extract_projects(sections.get("projects", [])),
            skills=self._extract_skills(sections.get("skills", []), text),
            certifications=self._clean_items(sections.get("certifications", [])),
            achievements=self._clean_items(sections.get("achievements", [])),
            raw_sections=sections,
        )

    def _split_sections(self, lines: list[str]) -> dict[str, list[str]]:
        sections: dict[str, list[str]] = {}
        current = "header"

        for line in lines:
            section = self._section_name(line)
            if section:
                current = section
                sections.setdefault(current, [])
            else:
                sections.setdefault(current, []).append(line)

        return sections

    def _section_name(self, line: str) -> str | None:
        normalized = re.sub(r"[^a-z ]", "", line.lower()).strip()
        if len(normalized.split()) > 4:
            return None

        for section, aliases in self.SECTION_ALIASES.items():
            if normalized in aliases:
                return section
        return None

    def _extract_name(self, lines: list[str]) -> str:
        for line in lines[:8]:
            if "@" in line or re.search(r"https?://|linkedin|github|\d{4,}", line, re.IGNORECASE):
                continue
            if 1 <= len(line.split()) <= 4:
                return line
        return ""

    def _first_match(self, text: str, pattern: str) -> str | None:
        match = re.search(pattern, text)
        return match.group(0).strip() if match else None

    def _extract_links(self, text: str) -> list[str]:
        explicit = re.findall(r"https?://[^\s,)]+", text)
        implicit = re.findall(r"\b(?:linkedin\.com|github\.com|leetcode\.com|kaggle\.com)/[^\s,)]+", text, re.IGNORECASE)
        return self._unique([*explicit, *implicit])

    def _extract_education(self, lines: list[str]) -> list[Education]:
        items: list[Education] = []
        for index, line in enumerate(lines):
            if self.DEGREE_RE.search(line):
                institution = lines[index - 2] if index >= 2 and not self._looks_like_date(lines[index - 2]) else ""
                year = self._first_match(line, r"(?:19|20)\d{2}(?:\s*-\s*(?:19|20)\d{2}|present)?")
                if not year and index > 0:
                    year = self._first_match(lines[index - 1], r"(?:19|20)\d{2}(?:\s*-\s*(?:19|20)\d{2}|present)?")
                items.append(Education(degree=line, institution=institution, year=year))
        return items

    def _extract_experience(self, lines: list[str]) -> list[Experience]:
        if not lines:
            return []

        groups = self._group_bullets(lines)
        experiences: list[Experience] = []
        for title, bullets in groups:
            duration = self._first_match(title, r"(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|\d{4}).*(?:present|\d{4})")
            parts = [part.strip() for part in re.split(r"\s[-|]\s|,", title) if part.strip()]
            experiences.append(
                Experience(
                    role=parts[0] if parts else title,
                    company=parts[1] if len(parts) > 1 else "",
                    duration=duration,
                    description=bullets,
                )
            )
        return experiences

    def _extract_projects(self, lines: list[str]) -> list[Project]:
        groups = self._group_projects(lines)
        projects: list[Project] = []
        for title, bullets in groups:
            body = " ".join(bullets) if bullets else title
            searchable = f"{title} {body}"
            projects.append(Project(name=title, description=body, technologies=self._extract_known_skills(searchable)))
        return projects

    def _group_projects(self, lines: list[str]) -> list[tuple[str, list[str]]]:
        groups: list[tuple[str, list[str]]] = []
        title = ""
        bullets: list[str] = []

        for line in lines:
            if self._looks_like_date(line):
                continue

            is_project_title = ("|" in line or "github.com" in line.lower() or "http" in line.lower()) and len(line.split()) <= 14
            if not title:
                title = line
            elif is_project_title:
                groups.append((title, bullets))
                title = line
                bullets = []
            else:
                bullets.append(line)

        if title:
            groups.append((title, bullets))
        return groups

    def _group_bullets(self, lines: list[str]) -> list[tuple[str, list[str]]]:
        groups: list[tuple[str, list[str]]] = []
        title = ""
        bullets: list[str] = []

        for line in lines:
            looks_like_bullet = len(line.split()) > 8 or line.startswith(("-", "*", "\u2022"))
            if not title:
                title = line
            elif looks_like_bullet:
                bullets.append(line)
            else:
                groups.append((title, bullets))
                title = line
                bullets = []

        if title:
            groups.append((title, bullets))
        return groups

    def _extract_skills(self, section_lines: list[str], full_text: str) -> list[str]:
        found = self._extract_known_skills(full_text)
        section_skills: list[str] = []
        for line in section_lines:
            _, _, value = line.partition(":")
            section_skills.extend(re.split(r"[,|;/]", value or line))
        return self._unique([self._canonical_skill(skill) for skill in [*self._clean_items(section_skills), *found]])

    def _extract_known_skills(self, text: str) -> list[str]:
        known = [
            "Python", "Java", "C++", "C", "JavaScript", "TypeScript", "SQL", "HTML", "CSS",
            "Next.js", "React.js", "React", "Node.js", "Django", "Flask", "FastAPI", "Pandas", "NumPy", "Scikit-learn",
            "TensorFlow", "PyTorch", "Machine Learning", "Deep Learning", "NLP", "OpenCV",
            "Power BI", "Tableau", "Excel", "Git", "GitHub", "Docker", "AWS", "Azure", "GCP", "MongoDB",
            "MySQL", "PostgreSQL", "REST API", "Data Analysis", "Data Visualization",
        ]
        return [skill for skill in known if re.search(rf"\b{re.escape(skill)}\b", text, re.IGNORECASE)]

    def _looks_like_date(self, line: str) -> bool:
        return bool(re.search(r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|january|february|march|april|june|july|august|september|october|november|december|\d{4})\b", line, re.IGNORECASE))

    def _canonical_skill(self, skill: str) -> str:
        aliases = {
            "react": "React.js",
            "rest api": "REST APIs",
            "rest apis": "REST APIs",
            "git & github": "Git/GitHub",
            "git": "Git/GitHub",
            "github": "Git/GitHub",
        }
        return aliases.get(skill.strip().lower(), skill.strip())

    def _clean_items(self, lines: list[str]) -> list[str]:
        return self._unique([line.strip(" -\u2022\t") for line in lines if line.strip(" -\u2022\t")])

    def _join_first(self, lines: list[str]) -> str | None:
        value = " ".join(lines).strip()
        return value or None

    def _unique(self, items: list[str]) -> list[str]:
        seen: set[str] = set()
        result: list[str] = []
        for item in items:
            normalized = re.sub(r"\s+", " ", item).strip()
            key = normalized.lower()
            if normalized and key not in seen:
                seen.add(key)
                result.append(normalized)
        return result
