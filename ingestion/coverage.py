def find_numeric_lines(lines):
    numeric_lines = []
    for line in lines:
        if any(char.isdigit() for char in line):
            numeric_lines.append(line)
    return numeric_lines


def detect_missed_lines(lines, extracted_tests):
    extracted_lines = [
        test["raw_line"].strip()
        for test in extracted_tests
        if test.get("raw_line")
    ]

    missed = []

    for line in lines:
        if any(char.isdigit() for char in line):
            if not any(line in ext for ext in extracted_lines):
                missed.append(line)

    return missed
