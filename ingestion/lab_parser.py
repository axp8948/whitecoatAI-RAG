import json
import re


EXTRACTION_PROMPT = """
You are a strict medical data extraction engine.

Extract EVERY measurable laboratory component.

Return STRICT JSON in this schema:

{
  "tests": [
    {
      "raw_line": "",
      "panel": "",
      "name": "",
      "value": null,
      "unit": "",
      "reference_range": {
        "min": null,
        "max": null
      },
      "flag": ""
    }
  ]
}

Rules:
- Extract ALL measurable lab values.
- Include original raw_line.
- If unsure, include it.
- Convert "<148" or ">200" to numeric.
- If qualitative (Positive/Negative), set value to null.
- Do NOT summarize.
- Do NOT omit lines.
- Return ONLY valid JSON.
"""


def _clean_json(text):
    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group() if match else text


def extract_structured_labs(raw_text, llm):
    prompt = EXTRACTION_PROMPT + f"\n\nMedical Report:\n{raw_text}"

    response = llm.generate(prompt)

    cleaned = _clean_json(response)

    try:
        return json.loads(cleaned)
    except Exception as e:
        raise ValueError("Invalid JSON returned from LLM.") from e
