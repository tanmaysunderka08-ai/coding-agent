import json

import pytest

from pipeline import run

SMALL = "a, b\n1, 2\n3, 4.5\n"


def test_single_export():
    out = run({"data.csv": SMALL, "notes.txt": "hello"})
    assert sorted(out) == ["data_summary.json", "index.json"]
    assert json.loads(out["data_summary.json"]) == {"rows": 2, "columns": ["a", "b"], "totals": {"a": 4, "b": 6.5}}


def test_text_columns_have_no_total():
    out = run({"Sales Q3.csv": "region, amount\nnorth, 10\nsouth, 5\n"})
    assert json.loads(out["sales_q3_summary.json"])["totals"] == {"amount": 15}


def test_same_name_twice():
    with pytest.raises(ValueError):
        run({"Sales Q3.csv": SMALL, "sales_q3.csv": SMALL})


def test_nightly_exports():
    out = run({"jobs.csv": SMALL, "metrics.csv": SMALL, "report.v2.csv": SMALL, "access.csv": SMALL})
    assert json.loads(out["index.json"]) == {
        "access.csv": "access_summary.json",
        "jobs.csv": "jobs_summary.json",
        "metrics.csv": "metrics_summary.json",
        "report.v2.csv": "report.v2_summary.json",
    }


def test_similar_names():
    out = run({"job.csv": SMALL, "jobs.csv": SMALL})
    assert sorted(out) == ["index.json", "job_summary.json", "jobs_summary.json"]
