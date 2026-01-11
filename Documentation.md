# Prompt Refinement System

This is a simple prototype of an AI-oriented **Prompt Refinement Engine**. It accepts raw, potentially messy user input (text, image captions, or document text/summaries) and converts it into a clean JSON structure suitable for downstream AI processing.

## Project Structure

- `src/`
  - `main.py` — CLI entry point.
  - `text_processor.py` — core refinement logic (rule-based heuristics).
  - `image_processor.py` — lightweight adapter for image captions.
  - `document_processor.py` — lightweight adapter for document text.
- `samples/`
  - `input_1_text.txt` — example of a text-only specification.
  - `input_2_image.png` — example image placeholder (treated as caption text in this prototype).
  - `input_3_document.pdf` — example document placeholder.
- `outputs/`
  - `output_1.json` — example refined JSON output.
- `docs/`
  - `problem_understanding.md`
  - `prompt_template.md`
  - `refinement_logic.md`
  - `design_decisions.md`

## Running the Prototype

From the `prompt-refinement-system` directory:

```bash
python -m src.main --type text --input samples/input_1_text.txt --output outputs/output_1.json
```

or, depending on your environment:

```bash
python src/main.py --type text --input samples/input_1_text.txt --output outputs/output_1.json
```

Supported input types:

- `--type text` — treats the input file as plain text describing the request.
- `--type image` — treats the input file content as a human-readable caption/summary of an image.
- `--type document` — treats the input file content as document text or a document summary (no real PDF/OCR processing).

The tool prints the resulting JSON to stdout and, if `--output` is provided, writes it to the indicated file as well.

For more details on the logic, see `docs/refinement_logic.md` and `docs/design_decisions.md`.
