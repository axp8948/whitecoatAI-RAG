def detect_missed_lines(lines, extracted_tests):
    """
    Detects numeric lines not extracted.
    """

    extracted_lines = [
        test.get("raw_line", "").strip()
        for test in extracted_tests
    ]

    missed = []

    for line in lines:
        if any(char.isdigit() for char in line):
            if not any(line in ext for ext in extracted_lines):
                missed.append(line)

    return missed
