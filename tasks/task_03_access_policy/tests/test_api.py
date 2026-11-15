from api import handle


def test_members_and_strangers():
    assert handle("alice", "doc-1") == (200, "ok")
    assert handle("bob", "doc-1") == (403, "forbidden")
    assert handle("alice", "prj-1") == (200, "ok")


def test_suspended_member():
    assert handle("eve", "doc-1") == (403, "forbidden")


def test_admin_and_settings():
    assert handle("dana", "log-1") == (200, "ok")
    assert handle("alice", "log-1") == (403, "forbidden")
    assert handle("carol", "set-1") == (200, "ok")
    assert handle("bob", "set-1") == (403, "forbidden")


def test_export_quota():
    assert handle("alice", "exp-1") == (200, "ok")
    assert handle("frank", "exp-1") == (403, "forbidden")


def test_unknown_user_and_resource():
    assert handle("mallory", "doc-1") == (401, "unknown user")
    assert handle("alice", "nope") == (404, "not found")


def test_invoice_and_payroll_access():
    for user in ("carol", "bob", "dana"):
        assert handle(user, "inv-7") == (403, "forbidden"), user
        assert handle(user, "pay-1") == (403, "forbidden"), user
