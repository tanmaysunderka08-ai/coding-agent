from rules import is_admin, is_member, is_owner_or_admin, not_suspended, within_quota

RULES = {
    "document": [not_suspended, is_member],
    "project": [not_suspended, is_member],
    "settings": [not_suspended, is_owner_or_admin],
    "export": [not_suspended, is_member, within_quota],
    "audit_log": [not_suspended, is_admin],
}


def rules_for(kind):
    return RULES.get(kind, [])


def decide(user, resource):
    results = [rule(user, resource) for rule in rules_for(resource.kind)]
    return all(results)
