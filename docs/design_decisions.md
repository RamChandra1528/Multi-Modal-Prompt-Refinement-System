# Design Decisions

## Why this template

The JSON template closely follows the problem statement:
- It forces separation between **intent**, **context**, **requirements**, **constraints**, **assumptions**, and **missing information**.
- It keeps multi-modal input explicit via `input_sources`.
- It adds a `confidence_score` to reflect that not all refinements are equally certain.

This structure makes it easy for downstream AI components to:
- Decide whether to proceed (e.g., reject vs. low confidence vs. high confidence).
- Inspect assumptions and missing information explicitly.
- Reason about functional requirements and constraints separately.

## Alternatives considered

1. **Single free-form "analysis" field**
   - Pros: Simpler to generate.
   - Cons: Harder for downstream systems to parse and act on; ambiguity is buried in prose.
   - Rejected in favor of explicit fields.

2. **Very strict, rule-based slot filling with no free-text context**
   - Pros: Easy to validate.
   - Cons: Too rigid for messy real-world inputs; context and nuance get lost.
   - Rejected in favor of keeping a short `context` and `expected_output` field.

3. **Adding many more fields (priority, user role, domain, etc.)**
   - Pros: Potentially richer representation.
   - Cons: Overkill for a simple prototype; higher cognitive load on both implementer and reviewer.
   - Rejected for this iteration to keep the system focused.

## Trade-offs

- **Simplicity vs. accuracy**: The heuristics are intentionally simple, which keeps the code readable but means it will miss nuanced intents and subtle constraints.
- **Generality vs. specialization**: The logic is domain-agnostic. It does not try to recognize specific domains (e.g., UI design vs. data science). This improves reuse but reduces domain-specific accuracy.
- **Prototype vs. production**: There is no heavy validation, no logging framework, and no external dependencies. This is sufficient for a coding exercise but not for production.

## Limitations

- Intent extraction is naive and often just returns the first reasonably long sentence.
- Functional requirements and constraints rely on a small set of keywords and bullet formats.
- Image and document handling assumes that text has already been extracted; no OCR or real PDF parsing is performed.
- Confidence scores are heuristic and not calibrated against any dataset.

These limitations are acceptable for demonstrating the overall design and reasoning process.

## Future improvements

If given more time, the following enhancements would be valuable:
- Add lightweight NLP (e.g., part-of-speech tagging or dependency parsing) to better identify verbs, objects, and requirement phrasing.
- Introduce a small rule engine or configuration file to tune keyword lists and patterns per domain.
- Add basic schema validation and error reporting for the generated JSON.
- Improve multi-modal handling by accepting separate text inputs for each modality rather than a single file per run.
- Add tests that cover both typical and adversarial inputs.

## AI Usage Declaration

LLMs were used for **brainstorming and validating ideas** around the architecture, template design, heuristic rules, and documentation structure. The final project structure, JSON template, refinement logic, and implementation choices were curated and assembled as a coherent prototype by the author.
