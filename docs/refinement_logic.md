# Refinement Logic

This prototype uses simple, rule-based heuristics to transform raw input into the JSON template. The goal is **clarity and explicitness**, not linguistic perfection.

## Core Steps

1. **Normalize and combine sources**
   - Concatenate any provided text, image caption, and document text into a single string.
   - Normalize whitespace.

2. **Reject clearly unusable input**
   - If there is no content at all, return `{ "rejected": true, ... }`.
   - If the content contains fewer than a few alphabetic characters, treat it as non-linguistic and reject.

3. **Extract intent**
   - Take the first non-empty sentence or line with at least a few words.
   - If nothing suitable is found, set `intent` to `null` and record a message in `missing_information`.

4. **Extract functional requirements**
   - Scan line by line for:
     - Bullet/numbered lines (e.g., `- ...`, `1. ...`).
     - Lines containing requirement verbs: `must`, `should`, `need to`, `required to`, `have to`.
   - Deduplicate while preserving order.

5. **Extract constraints**
   - Scan for lines mentioning negative or limiting phrases: `must not`, `should not`, `do not`, `don't`, `limitations`, `constraints`.

6. **Infer context**
   - Use the second sentence (if present) as a rough context.
   - Otherwise, fall back to a generic string like `"General user request without additional explicit context."`.

7. **Assumptions**
   - If an image caption is present, assume: `"Image content has already been converted into a textual caption or summary."`.
   - If document text is present, assume: `"Document content is provided as extracted text or a readable summary (no OCR required)."`.
   - If neither is present, add a generic assumption about downstream systems tolerating concise summaries.

8. **Expected output**
   - If the text mentions both `json` and `schema`, describe success as a JSON object following the schema.
   - If it mentions `json`, describe success as a structured JSON representation.
   - If it mentions `summary`/`summarize`, describe success as a concise summary.
   - Otherwise, use a generic description of a refined, structured interpretation.

9. **Confidence score**
   - Start from a base score.
   - Add points if an intent is found, if there are requirements, and if there are constraints.
   - Add small bonuses for longer inputs (up to a limit).
   - Subtract points for each item recorded in `missing_information`.
   - Clamp the final score between 0 and 1.

## Sample Inputs and Outputs

### 1. Text-only specification

**Input:** `samples/input_1_text.txt`

A short, well-structured description of the Prompt Refinement Engine, listing bullet-point requirements and constraints.

**Output (conceptual):**
- `intent`: A one-line paraphrase of the description.
- `functional_requirements`: Populated from the bullet list.
- `constraints`: Populated from lines mentioning what must *not* be done or kept simple.
- `assumptions`: Generic assumptions about downstream AI systems.
- `missing_information`: Empty or minimal.
- `confidence_score`: Relatively high (e.g., > 0.8).

### 2. Text + image caption

**Input:**
- Text: High-level description of a dashboard generator.
- Image caption: A description of a wireframe showing a dashboard layout.

**Behavior:**
- Both sources are combined for analysis.
- `input_sources.image` contains a summarized caption.
- An extra assumption notes that image content is already captured in text form.

### 3. Document-only

**Input:** `samples/input_3_document.pdf`

A longer explanation (stored as plain text for this prototype) describing a document analysis tool.

**Behavior:**
- Treated as a plain text source passed through the document adapter.
- Intent and requirements pulled from early and bulleted parts of the text.

### 4. Image-only

**Input:** `samples/input_2_image.png`

A file whose content is a textual caption describing a mobile UI screenshot.

**Behavior:**
- The caption is treated as the primary source.
- If the caption is very short or vague, `intent` may be `null` and an item is added to `missing_information`.

### 5. Messy / incomplete input

**Input:** A few short, fragmented phrases without clear verbs or goals.

**Behavior:**
- If the engine cannot find a meaningful sentence with at least a few words, it sets `intent` to `null`.
- `missing_information` records that the intent is unclear.
- `confidence_score` is lower due to missing information and lack of structure.

These examples are illustrative of how the heuristics behave and where they are limited.
