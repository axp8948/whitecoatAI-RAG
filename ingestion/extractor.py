import base64


def extract_text(file, model):
    if file.type == "application/pdf":
        pdf_bytes = file.getvalue()
        base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")

        prompt = (
            "Extract all text content from this PDF document. "
            "Preserve formatting and structure. Do not summarize."
        )

        parts = [
            {"text": prompt},
            {
                "inline_data": {
                    "mime_type": "application/pdf",
                    "data": base64_pdf
                }
            }
        ]

        response = model.generate_content(parts)
        return response.text

    elif file.type == "text/plain":
        return file.read().decode("utf-8")

    return ""
