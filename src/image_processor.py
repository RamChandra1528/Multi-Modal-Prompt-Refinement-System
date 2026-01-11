from typing import Optional


def prepare_image_caption(raw_image_content: Optional[str]) -> Optional[str]:
    """Prepare an image caption/summary for the core text processor.

    In a real system this might call OCR or vision models; for this prototype
    we assume `raw_image_content` is already a human-readable caption or
    description (or None).
    """
    if not raw_image_content:
        return None
    caption = raw_image_content.strip()
    return caption or None
