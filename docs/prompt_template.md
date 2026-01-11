# Prompt Template (JSON Schema)

The Prompt Refinement Engine produces JSON in the following shape:

```json
{
  "intent": "Clear one-line description of what the user wants or null if unclear",
  "context": "Short background or domain context inferred from input",
  "input_sources": {
    "text": "Summary of text input or null",
    "image": "Summary of image caption/description or null",
    "document": "Summary of document content or null"
  },
  "functional_requirements": [
    "List of concrete actions or features expected"
  ],
  "constraints": [
    "Technical, business, or design limitations if mentioned"
  ],
  "assumptions": [
    "Reasonable assumptions made due to missing information"
  ],
  "missing_information": [
    "Critical information required but not provided"
  ],
  "expected_output": "What a successful output should look like",
  "confidence_score": 0.0
}
```

For irrelevant or clearly unusable input, the engine instead returns:

```json
{
  "rejected": true,
  "reason": "short reason string"
}
```

Notes:
- `confidence_score` is a float in the range `[0, 1]` and is heuristic, not statistically calibrated.
- `functional_requirements`, `constraints`, `assumptions`, and `missing_information` are always lists of strings (possibly empty).
- `input_sources` fields are short summaries, not full verbatim copies, to keep the structure compact.
