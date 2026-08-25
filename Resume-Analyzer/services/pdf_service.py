from pathlib import Path
import fitz  # PyMuPDF


class PDFService:
    """
    Responsible only for reading PDF files.
    """

    def extract_text(self, pdf_path: str) -> str:
        path = Path(pdf_path)

        if not path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        text = []

        with fitz.open(pdf_path) as document:
            for page in document:
                text.append(page.get_text())

        return "\n".join(text).strip()