from urllib.parse import parse_qs, urlsplit


def parse_url(url):
    parts = urlsplit(url)
    params = {key: values[-1] for key, values in parse_qs(parts.query).items()}
    return parts.path, params
