from plans import UNLIMITED, limit_for


def blocked(account):
    limit = limit_for(account.plan)
    if limit is UNLIMITED:
        return False
    return account.used is limit or account.used > limit


def remaining(account):
    limit = limit_for(account.plan)
    if limit is UNLIMITED:
        return None
    return max(limit - account.used, 0)


def warning(account, share=0.8):
    limit = limit_for(account.plan)
    return limit is not UNLIMITED and account.used >= share * limit
