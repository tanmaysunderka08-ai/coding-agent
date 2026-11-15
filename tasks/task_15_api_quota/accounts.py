from dataclasses import dataclass


@dataclass
class Account:
    name: str
    plan: str
    used: int


def parse_accounts(text):
    accounts = {}
    for line in text.strip().splitlines():
        if not line.strip():
            continue
        name, plan, used = [p.strip() for p in line.split(",")]
        accounts[name] = Account(name, plan, int(used))
    return accounts
