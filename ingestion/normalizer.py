def normalize_lines(raw_text):
    """
    Splits raw text into clean lines.
    """
    lines = raw_text.split("\n")
    return [line.strip() for line in lines if line.strip()]
