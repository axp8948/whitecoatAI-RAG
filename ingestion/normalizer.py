def normalize_lines(raw_text):
    lines = raw_text.split("\n")
    cleaned = [line.strip() for line in lines if line.strip()]
    return cleaned
