from __future__ import annotations

from models.resume import Resume, SkillMatch


class SuggestionAgent:
    def suggest(self, resume: Resume, weaknesses: list[str], skill_match: SkillMatch) -> list[str]:
        suggestions: list[str] = []

        if resume.projects:
            suggestions.append("Rewrite project bullets with action verbs, technologies used, and measurable outcomes.")
        else:
            suggestions.append("Add 2-3 strong projects with problem, tech stack, implementation, and result.")

        if resume.experience:
            suggestions.append("For each role, include impact metrics such as time saved, accuracy improved, users served, or revenue affected.")
        else:
            suggestions.append("Add internship, freelance, open-source, academic, or volunteer experience if available.")

        if skill_match.missing_from_job_description:
            missing = ", ".join(skill_match.missing_from_job_description[:8])
            suggestions.append(f"Match the target job better by adding evidence for these skills if you have them: {missing}.")

        if any("summary" in weakness.lower() for weakness in weaknesses):
            suggestions.append("Add a 2-3 line summary tailored to the target role and your strongest technical proof.")

        if not resume.links:
            suggestions.append("Add clickable LinkedIn, GitHub, portfolio, or deployed project links near your contact details.")

        suggestions.append("Keep formatting ATS-friendly: simple section headings, consistent dates, and standard bullet points.")
        return self._unique(suggestions)

    def strengths(self, resume: Resume) -> list[str]:
        strengths: list[str] = []
        if resume.email and resume.phone:
            strengths.append("Contact details are present.")
        if resume.skills:
            strengths.append(f"Detected {len(resume.skills)} skills.")
        if resume.projects:
            strengths.append(f"Detected {len(resume.projects)} project entry/entries.")
        if resume.experience:
            strengths.append(f"Detected {len(resume.experience)} experience entry/entries.")
        if resume.education:
            strengths.append("Education section is present.")
        return strengths

    def score(self, resume: Resume, weaknesses: list[str]) -> int:
        score = 100
        score -= min(len(weaknesses) * 8, 56)
        if len(resume.skills) >= 8:
            score += 3
        if resume.projects and resume.experience:
            score += 4
        if resume.links:
            score += 3
        return max(0, min(100, score))

    def _unique(self, items: list[str]) -> list[str]:
        result: list[str] = []
        seen: set[str] = set()
        for item in items:
            key = item.lower()
            if key not in seen:
                seen.add(key)
                result.append(item)
        return result
