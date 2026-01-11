# Problem Understanding

The goal is to build a small, focused **Prompt Refinement Engine**. This engine takes raw, messy, and potentially multi-modal input from a user and converts it into a clean, structured JSON representation suitable for downstream AI models.

The inputs can include:
- Plain text descriptions of tasks or problems.
- Image information that has already been converted into text (captions/summaries).
- Document text or summaries (e.g., extracted from longer documents).

The output must follow a strict JSON schema that captures:
- The core intent of the request.
- Context or background.
- Functional requirements.
- Constraints.
- Assumptions.
- Missing or ambiguous information.
- What a successful output should look like.
- A confidence score.

Additionally, the system must:
- Detect and explicitly handle unclear or irrelevant inputs.
- Be simple and easy to understand rather than over-engineered.
- Include documentation of design decisions, trade-offs, and limitations.

Success is defined not by sophisticated NLP, but by **clean structure, explicit assumptions, and transparent handling of ambiguity**.
