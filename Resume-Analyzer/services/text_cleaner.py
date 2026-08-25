import re


class TextCleaner:
    """
    Cleans extracted resume text.

    This class performs deterministic preprocessing only.
    It never changes the meaning of the content.
    """

    def clean(self, text: str) -> str:

        # Normalize line endings
        text = text.replace("\r\n", "\n")

        # Remove PDF icon glyph artifacts while preserving normal text.
        text = re.sub(r"[^\x09\x0A\x0D\x20-\x7E\u2013\u2014\u2022]", "", text)

        # Replace tabs with spaces
        text = text.replace("\t", " ")

        # Remove multiple spaces
        text = re.sub(r"[ ]{2,}", " ", text)

        # Remove excessive blank lines
        text = re.sub(r"\n{3,}", "\n\n", text)

        # Remove leading/trailing spaces on every line
        lines = [line.strip() for line in text.split("\n")]

        return "\n".join(lines).strip()
