from ingestion.extractor import extract_text
from ingestion.normalizer import normalize_lines
from ingestion.lab_parser import extract_structured_labs
from ingestion.coverage import detect_missed_lines
from ingestion.validator import validate_lab_data


def run_extraction_pipeline(file, model):

    raw_text = extract_text(file, model)

    lines = normalize_lines(raw_text)

    structured = extract_structured_labs(raw_text, model)

    missed = detect_missed_lines(lines, structured.get("tests", []))

    # Optional: second recovery pass if needed
    if missed:
        recovery_prompt = f"""
The following lines were not extracted:
{missed}

Extract them using the same schema.
Return ONLY JSON.
"""
        recovery_response = model.generate_content(recovery_prompt)
        import json
        recovered = json.loads(recovery_response.text)
        structured["tests"].extend(recovered.get("tests", []))

    validated = validate_lab_data(structured)

    return {
        "raw_text": raw_text,
        "structured_data": validated
    }
