"""Small, dependency-light helpers for reading study material."""
from pathlib import Path
from typing import BinaryIO, TextIO, Union
import PyPDF2

def read_file(file: Union[str, Path, BinaryIO, TextIO]) -> str:
    """Read a PDF or UTF-8 text file from a path or an open file object."""
    if isinstance(file, (str, Path)):
        path = Path(file)
        suffix = path.suffix.lower()
        if suffix == ".txt":
            return path.read_text(encoding="utf-8")
        if suffix == ".pdf":
            with path.open("rb") as stream:
                return _read_pdf(stream)
        raise ValueError(f"Unsupported file type: {suffix or '(no extension)'}")
    suffix = Path(str(getattr(file, "name", ""))).suffix.lower()
    if suffix == ".txt":
        content = file.read()
        return content.decode("utf-8") if isinstance(content, bytes) else content
    if suffix == ".pdf":
        return _read_pdf(file)
    raise ValueError(f"Unsupported file type: {suffix or '(no extension)'}")

def _read_pdf(stream: BinaryIO) -> str:
    """Extract selectable text from a PDF stream."""
    reader = PyPDF2.PdfReader(stream)
    return "\n".join(page.extract_text() or "" for page in reader.pages).strip()
