from output import format_problems, summary, with_context

CODE = "x = 1  \n\ty = 2\nz = 3  # TODO: fix\ntry:\n    pass\nexcept:\n    pass\n"


def test_summary():
    assert summary("a.py", CODE) == {"E722": 1, "T001": 1, "W191": 1, "W291": 1}


def test_long_line():
    text = "ok\n" + "a" * 45 + "\n"
    assert format_problems("b.py", text) == ["b.py:2:41: E501 line too long (45 > 40)"]


def test_report():
    assert format_problems("a.py", CODE) == [
        "a.py:1:6: W291 trailing whitespace",
        "a.py:2:1: W191 indentation contains tabs",
        "a.py:3:8: T001 TODO comment",
        "a.py:6:1: E722 bare except",
    ]


def test_context_lines():
    assert with_context("a.py", CODE)[1:] == ["2| y = 2  <- W191", "3| z = 3  # TODO: fix  <- T001", "6| except:  <- E722"]


def test_first_line_problem():
    assert format_problems("c.py", "\tx = 1\n") == ["c.py:1:1: W191 indentation contains tabs"]
