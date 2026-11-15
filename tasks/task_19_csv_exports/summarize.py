def as_number(text):
    try:
        return int(text)
    except ValueError:
        try:
            return float(text)
        except ValueError:
            return None


def summarize(header, rows):
    totals = {}
    for column in header:
        values = [as_number(row.get(column, "")) for row in rows]
        if rows and all(v is not None for v in values):
            totals[column] = round(sum(values), 2)
    return {"rows": len(rows), "columns": header, "totals": totals}
