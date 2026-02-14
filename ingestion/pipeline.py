import json
from ingestion.extractor import extract_text
from ingestion.normalizer import normalize_lines
from ingestion.lab_parser import extract_structured_labs
from ingestion.coverage import detect_missed_lines
from ingestion.validator import validate_lab_data


def run_extraction_pipeline(file, llm):
    """
    Full high-recall extraction pipeline.
    """

    # 1️⃣ Extract raw text
    raw_text = extract_text(file, llm)

    # 2️⃣ Normalize lines
    lines = normalize_lines(raw_text)

    # 3️⃣ Structured extraction
    structured = extract_structured_labs(raw_text, llm)

    # 4️⃣ Coverage detection
    missed = detect_missed_lines(lines, structured.get("tests", []))

    # 5️⃣ Recovery pass if needed
    if missed:
        recovery_prompt = f"""
The following lines were not extracted:
{missed}

Extract them using the same JSON schema.
Return ONLY valid JSON.
"""
        try:
            recovery_response = llm.generate(recovery_prompt)
            recovered_data = json.loads(recovery_response)
            structured["tests"].extend(recovered_data.get("tests", []))
        except (json.JSONDecodeError, KeyError):
            pass  # Recovery failed — continue with what we have

    # 6️⃣ Validate
    validated = validate_lab_data(structured)

    return {
        "raw_text": raw_text,
        "structured_data": validated
    }
