from logfmt import parse_lines
from metrics import error_messages, errors_by_user, slow, status_classes
from records import to_request


def summary(text):
    requests = [to_request(f) for f in parse_lines(text)]
    return {
        "requests": len(requests),
        "statuses": status_classes(requests),
        "slow_paths": slow(requests),
        "errors_by_user": errors_by_user(requests),
        "error_messages": error_messages(requests),
    }
