import json
import re
from typing import Any, Dict, List, Optional


def _normalize(text: str) -> str:
    """Basic whitespace normalization."""
    return re.sub(r"\s+", " ", text.strip())


def _summarize_source(text: Optional[str], max_len: int = 200) -> Optional[str]:
    if not text:
        return None
    text = text.strip()
    if not text:
        return None
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def _extract_intent(text: str) -> Optional[str]:
    """Heuristic: use the first non-empty sentence or line as the intent line."""
    cleaned = text.strip()
    if not cleaned:
        return None
    # Very short inputs are considered unclear.
    if len(cleaned.split()) < 3:
        return None
    parts = re.split(r"[\n\.!?]", cleaned)
    for part in parts:
        candidate = part.strip()
        if len(candidate.split()) >= 3:
            return candidate
    return None


def _extract_functional_requirements(lines: List[str]) -> List[str]:
    reqs: List[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        # Bullet or numbered list lines.
        if re.match(r"^([-*+]\s+|\d+\.\s+)", stripped):
            reqs.append(stripped)
            continue
        # Lines with strong requirement verbs.
        if re.search(r"\b(must|should|need to|required to|have to)\b", stripped, re.IGNORECASE):
            reqs.append(stripped)
    # Deduplicate while preserving order.
    seen = set()
    unique_reqs = []
    for r in reqs:
        if r not in seen:
            seen.add(r)
            unique_reqs.append(r)
    return unique_reqs


def _extract_constraints(lines: List[str]) -> List[str]:
    cons: List[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if re.search(r"\b(must not|should not|do not|dont|don't|limitations?|constraints?)\b", stripped, re.IGNORECASE):
            cons.append(stripped)
    seen = set()
    unique_cons = []
    for c in cons:
        if c not in seen:
            seen.add(c)
            unique_cons.append(c)
    return unique_cons


def _infer_expected_output(text: str) -> str:
    lowered = text.lower()
    if "json" in lowered and "schema" in lowered:
        return "A JSON object following the specified schema, populated from the user input."
    if "json" in lowered:
        return "A structured JSON representation of the refined prompt."
    if "summary" in lowered or "summarize" in lowered:
        return "A concise summary capturing the user intent and key requirements."
    return "A refined, structured interpretation of the request that satisfies the extracted requirements."


def _estimate_confidence(intent: Optional[str], reqs: List[str], cons: List[str], missing: List[str], combined_text: str) -> float:
    score = 0.4
    if intent:
        score += 0.25
    if reqs:
        score += 0.15
    if cons:
        score += 0.05
    # Reward richer input length up to a point.
    length = len(combined_text.split())
    if length > 20:
        score += 0.05
    if length > 80:
        score += 0.05
    # Penalize missing information.
    score -= 0.05 * len(missing)
    return max(0.0, min(1.0, score))


def refine_prompt(
    text_source: Optional[str] = None,
    image_source: Optional[str] = None,
    document_source: Optional[str] = None,
) -> Dict[str, Any]:
    """Core refinement engine.

    Returns either the full JSON structure or a rejection JSON if input is
    clearly irrelevant/empty.
    """
    sources = [s for s in [text_source, image_source, document_source] if s]
    combined = " ".join(sources).strip() if sources else ""

    # Empty or non-linguistic input handling.
    if not combined:
        return {"rejected": True, "reason": "Empty input; no text, image caption, or document content provided."}

    alpha_chars = sum(1 for c in combined if c.isalpha())
    if alpha_chars < 3:
        return {"rejected": True, "reason": "Input appears non-linguistic; cannot infer intent."}

    combined_norm = _normalize(combined)
    lines = combined.splitlines()

    intent = _extract_intent(combined_norm)
    missing: List[str] = []
    if intent is None:
        missing.append("User intent is unclear or underspecified in the provided input.")

    functional_requirements = _extract_functional_requirements(lines)
    constraints = _extract_constraints(lines)

    # Very simple context heuristic: second sentence or a generic fallback.
    context: str
    sentences = re.split(r"[\.!?]", combined_norm)
    if len(sentences) > 1 and sentences[1].strip():
        context = sentences[1].strip()
    else:
        context = "General user request without additional explicit context."

    # Simple assumptions based on modalities present.
    assumptions: List[str] = []
    if image_source:
        assumptions.append("Image content has already been converted into a textual caption or summary.")
    if document_source:
        assumptions.append("Document content is provided as extracted text or a readable summary (no OCR required).")
    if not assumptions:
        assumptions.append("Downstream AI systems can consume concise, high-level summaries rather than exhaustive detail.")

    expected_output = _infer_expected_output(combined_norm)

    confidence_score = _estimate_confidence(intent, functional_requirements, constraints, missing, combined_norm)

    result: Dict[str, Any] = {
        "intent": intent,
        "context": context,
        "input_sources": {
            "text": _summarize_source(text_source),
            "image": _summarize_source(image_source),
            "document": _summarize_source(document_source),
        },
        "functional_requirements": functional_requirements,
        "constraints": constraints,
        "assumptions": assumptions,
        "missing_information": missing,
        "expected_output": expected_output,
        "confidence_score": round(confidence_score, 2),
    }

    return result


def refine_prompt_to_json(**kwargs: Any) -> str:
    """Helper to return a pretty-printed JSON string."""
    return json.dumps(refine_prompt(**kwargs), indent=2)
