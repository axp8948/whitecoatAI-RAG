import base64


def extract_text(file, llm):
    """
    Extract raw text from PDF or TXT file.
    Uses LLM only for PDF parsing.
    """

    if file.type == "application/pdf":
        pdf_bytes = file.getvalue()
        base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")

        prompt = (
            "Extract all text content from this PDF document. "
            "Preserve structure. Do NOT summarize."
        )

        response = llm.generate_with_file(
            prompt=prompt,
            file_data=base64_pdf,
            mime_type="application/pdf"
        )

        return response

    elif file.type == "text/plain":
        return file.read().decode("utf-8")

    return ""
