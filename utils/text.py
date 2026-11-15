def strip_fences(text):
    # removes a ```python ... ``` wrapper if the model added one
    text = text.strip()

    if text.startswith("```") and "\n" in text:
        first_line, rest = text.split("\n", 1)
        lang = first_line[3:].rstrip()
        if lang == "" or lang.isalpha():
            text = rest
            while "\n" in text and text.split("\n", 1)[0].strip() == "":
                text = text.split("\n", 1)[1]

    end = text.rstrip()
    if end.endswith("```"):
        text = end[:-3]
        if text.endswith("\n"):
            text = text[:-1]
    return text
