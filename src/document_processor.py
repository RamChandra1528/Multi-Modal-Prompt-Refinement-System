from typing import Optional


def prepare_document_text(raw_document_content: Optional[str]) -> Optional[str]:
    """Prepare document text/summary for the core text processor.

    For this prototype, we assume the document content is already provided as
    readable text or a short summary, even if the original file extension is
    something like .pdf. No real PDF parsing or OCR is performed.
    """
    if not raw_document_content:
        return None
    text = raw_document_content.strip()
    return text or None
