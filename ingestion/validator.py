def validate_lab_data(data):

    cleaned = []

    for test in data.get("tests", []):

        try:
            value = float(test["value"]) if test["value"] is not None else None
        except:
            value = None

        try:
            ref_min = float(test["reference_range"]["min"]) \
                if test["reference_range"]["min"] is not None else None
        except:
            ref_min = None

        try:
            ref_max = float(test["reference_range"]["max"]) \
                if test["reference_range"]["max"] is not None else None
        except:
            ref_max = None

        cleaned.append({
            "raw_line": test.get("raw_line"),
            "panel": test.get("panel"),
            "name": test.get("name"),
            "value": value,
            "unit": test.get("unit"),
            "reference_min": ref_min,
            "reference_max": ref_max,
            "flag": test.get("flag")
        })

    data["tests"] = cleaned
    return data
