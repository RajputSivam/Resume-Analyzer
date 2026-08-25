from __future__ import annotations

import json
import re
from pathlib import Path

from agents.parser_agent import ParserAgent
from config import Config
from models.resume import Resume
from services.llm_service import LLMService


class ExtractorAgent:
    """Extract structured resume data, using Groq when configured."""

    def __init__(self) -> None:
        self.parser = ParserAgent()

    def extract(self, text: str, use_llm: bool = True) -> Resume:
        if use_llm and Config.GROQ_API_KEY:
            llm_resume = self._extract_with_llm(text)
            if llm_resume:
                return llm_resume
        return self.parser.parse(text)

    def _extract_with_llm(self, text: str) -> Resume | None:
        try:
            prompt = Path("prompts/extractor.txt").read_text(encoding="utf-8")
            response = LLMService().chat(
                prompt,
                f"Resume text:\n{text}\n\nReturn only JSON matching the resume schema.",
            )
            payload = self._json_from_response(response)
            return Resume.model_validate(payload)
        except Exception:
            return None

    def _json_from_response(self, response: str) -> dict:
        match = re.search(r"\{.*\}", response, re.DOTALL)
        if not match:
            raise ValueError("LLM response did not contain JSON.")
        return json.loads(match.group(0))
