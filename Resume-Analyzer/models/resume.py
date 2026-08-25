from typing import Any
from pydantic import BaseModel, Field


class Education(BaseModel):
    degree: str = ""
    institution: str = ""
    year: str | None = None


class Experience(BaseModel):
    company: str = ""
    role: str = ""
    duration: str | None = None
    description: list[str] = Field(default_factory=list)


class Project(BaseModel):
    name: str = ""
    description: str = ""
    technologies: list[str] = Field(default_factory=list)


class Resume(BaseModel):
    name: str = ""
    email: str | None = None
    phone: str | None = None
    links: list[str] = Field(default_factory=list)
    summary: str | None = None
    education: list[Education] = Field(default_factory=list)
    experience: list[Experience] = Field(default_factory=list)
    projects: list[Project] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    achievements: list[str] = Field(default_factory=list)
    raw_sections: dict[str, list[str]] = Field(default_factory=dict)


class SkillMatch(BaseModel):
    found: list[str] = Field(default_factory=list)
    missing_from_job_description: list[str] = Field(default_factory=list)
    categories: dict[str, list[str]] = Field(default_factory=dict)


class ResumeAnalysis(BaseModel):
    resume: Resume
    score: int
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)
    skill_match: SkillMatch = Field(default_factory=SkillMatch)
    metadata: dict[str, Any] = Field(default_factory=dict)
