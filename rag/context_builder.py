def build_summary_context(structured_labs):
    lines = []
    lines.append("LAB RESULTS:\n")

    for lab in structured_labs:
        test = lab.get("name")
        value = lab.get("value")
        unit = lab.get("unit", "")
        ref_min = lab.get("reference_min")
        ref_max = lab.get("reference_max")
        flag = lab.get("flag", "")

        # Build reference range string
        if ref_min is not None and ref_max is not None:
            ref = f"{ref_min}-{ref_max}"
        elif ref_min is not None:
            ref = f">={ref_min}"
        elif ref_max is not None:
            ref = f"<={ref_max}"
        else:
            ref = "N/A"

        status = "Normal"
        if flag and flag.upper() in ("H", "HIGH"):
            status = "High"
        elif flag and flag.upper() in ("L", "LOW"):
            status = "Low"

        line = f"- {test}: {value} {unit} | Reference: {ref} | Status: {status}"
        lines.append(line)

    return "\n".join(lines)
