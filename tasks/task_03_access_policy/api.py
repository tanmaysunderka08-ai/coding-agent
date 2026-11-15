from models import Resource, User
from policy import decide

USERS = {
    "alice": User("alice"),
    "bob": User("bob"),
    "carol": User("carol"),
    "dana": User("dana", roles=("admin",)),
    "eve": User("eve", suspended=True),
    "frank": User("frank", exports_today=5),
}

RESOURCES = {
    "doc-1": Resource("document", owner="alice", members=("alice", "eve")),
    "prj-1": Resource("project", owner="bob", members=("bob", "alice")),
    "set-1": Resource("settings", owner="carol"),
    "exp-1": Resource("export", owner="alice", members=("alice", "frank")),
    "log-1": Resource("audit_log", owner="dana"),
    "inv-7": Resource("invoice", owner="carol", members=("carol",)),
    "pay-1": Resource("payroll", owner="dana", members=("dana",)),
}


def handle(username, resource_id):
    user = USERS.get(username)
    if user is None:
        return 401, "unknown user"
    resource = RESOURCES.get(resource_id)
    if resource is None:
        return 404, "not found"
    try:
        allowed = decide(user, resource)
    except Exception:
        return 500, "error"
    return (200, "ok") if allowed else (403, "forbidden")
