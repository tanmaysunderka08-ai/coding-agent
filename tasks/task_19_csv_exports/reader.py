def parse_csv(text):
    lines = [line for line in text.strip().splitlines() if line.strip()]
    header = [h.strip() for h in lines[0].split(",")]
    rows = []
    for line in lines[1:]:
        values = [v.strip() for v in line.split(",")]
        rows.append(dict(zip(header, values)))
    return header, rows
