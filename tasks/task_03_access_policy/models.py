from dataclasses import dataclass, field


@dataclass
class User:
    name: str
    roles: tuple = ()
    suspended: bool = False
    exports_today: int = 0
    export_limit: int = 5


@dataclass
class Resource:
    kind: str
    owner: str
    members: tuple = field(default_factory=tuple)
