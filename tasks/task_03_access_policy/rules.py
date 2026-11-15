"""Single access checks. Each takes (user, resource) and returns True or False."""


def not_suspended(user, resource):
    return not user.suspended


def is_admin(user, resource):
    return "admin" in user.roles


def is_member(user, resource):
    return user.name in resource.members or is_admin(user, resource)


def is_owner_or_admin(user, resource):
    return resource.owner == user.name or is_admin(user, resource)


def within_quota(user, resource):
    return user.exports_today < user.export_limit
