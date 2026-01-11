import argparse
import json
from pathlib import Path
from typing import Optional

from text_processor import refine_prompt
from image_processor import prepare_image_caption
from document_processor import prepare_document_text


def _read_file(path: Path) -> str:
    # For the prototype, treat all files as text and decode with UTF-8 where possible.
    # This keeps the implementation simple and avoids external dependencies.
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        # Fallback: binary read and best-effort decode.
        data = path.read_bytes()
        return data.decode("utf-8", errors="ignore")


def run(input_type: str, input_path: Path, output_path: Optional[Path]) -> None:
    raw_content = _read_file(input_path)

    text_source: Optional[str] = None
    image_source: Optional[str] = None
    document_source: Optional[str] = None

    if input_type == "text":
        text_source = raw_content
    elif input_type == "image":
        # For this prototype, we assume the file contains or represents a
        # caption; we simply feed its textual content to the adapter.
        image_source = prepare_image_caption(raw_content)
    elif input_type == "document":
        document_source = prepare_document_text(raw_content)
    else:
        raise ValueError(f"Unsupported input type: {input_type}")

    result = refine_prompt(
        text_source=text_source,
        image_source=image_source,
        document_source=document_source,
    )

    json_str = json.dumps(result, indent=2)
    print(json_str)

    if output_path is not None:
        output_path.write_text(json_str, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Simple Prompt Refinement Engine prototype.",
    )
    parser.add_argument(
        "--type",
        dest="input_type",
        required=True,
        choices=["text", "image", "document"],
        help="Type of input to process.",
    )
    parser.add_argument(
        "--input",
        dest="input_path",
        required=True,
        help="Path to input file (text, image caption, or document text).",
    )
    parser.add_argument(
        "--output",
        dest="output_path",
        required=False,
        help="Optional path to write the resulting JSON.",
    )

    args = parser.parse_args()
    input_path = Path(args.input_path)
    output_path = Path(args.output_path) if args.output_path else None

    run(args.input_type, input_path, output_path)


if __name__ == "__main__":
    main()
