def coerce(text):
    text = text.strip()
    if text.lower() in ("true", "false"):
        return text.lower() == "true"
    if text.lstrip("-").isdigit():
        return int(text)
    return text


def parse_env(text, prefix="APP__"):
    pairs = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, value = line.split("=", 1)
        name = name.strip()
        if name.startswith(prefix):
            pairs.append((name[len(prefix):].lower().replace("__", "."), coerce(value)))
    return pairs


def set_path(tree, dotted, value):
    keys = dotted.split(".")
    node = tree
    for key in keys[:-1]:
        node = node.setdefault(key, {})
    node[keys[-1]] = value
