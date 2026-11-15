# the planner's reply is one json object, checked here with pydantic.

import json
from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from utils.text import strip_fences
from utils.workspace import source_files

BugType = Literal["off_by_one", "wrong_condition", "wrong_variable",
                  "missing_edge_case", "wrong_data_type", "logic_error", "other"]


class FixPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    root_cause: str = Field(min_length=10)
    bug_type: BugType
    files: List[str] = Field(min_length=1)
    functions: List[str] = Field(min_length=1)
    steps: List[str] = Field(min_length=1, max_length=6)


def extract_json(text):
    # the {...} part of the reply, even with fences or text around it
    text = strip_fences(text)
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end <= start:
        return text
    return text[start:end + 1]


def short_errors(err):
    parts = []
    for e in err.errors()[:4]:
        where = ".".join(str(p) for p in e["loc"]) or "the object"
        parts.append(f"'{where}': {e['msg']}")
    return "; ".join(parts)


def clean_path(name):
    name = name.strip().strip("`").replace("\\", "/")
    if name.startswith("./"):
        name = name[2:]
    return name


def check_plan(task_dir, text):
    # returns (plan, None) or (None, what is wrong)
    try:
        data = json.loads(extract_json(text))
    except json.JSONDecodeError as e:
        return None, (f"the reply is not valid JSON ({e.msg} at line {e.lineno}, column {e.colno}). "
                      "Reply with exactly one JSON object and nothing else.")
    if not isinstance(data, dict):
        return None, "the reply must be one JSON object ({...}), not a list or a value."
    try:
        plan = FixPlan.model_validate(data)
    except ValidationError as e:
        return None, f"the JSON does not match the required keys and types: {short_errors(e)}."

    allowed = set()
    for rel in source_files(task_dir):
        allowed.add(rel.as_posix())

    cleaned = []
    unknown = []
    for f in plan.files:
        name = clean_path(f)
        cleaned.append(name)
        if name not in allowed:
            unknown.append(name)
    if unknown:
        return None, (f"'files' may only contain paths from CURRENT CODE: {', '.join(sorted(allowed))}. "
                      f"Not found: {', '.join(unknown)}.")
    plan.files = cleaned
    return plan, None


def plan_problem(task_dir, text):
    return check_plan(task_dir, text)[1]


def format_plan(plan):
    # plan as plain text, for the coder's prompt and the planner's history
    steps = []
    for i, s in enumerate(plan.steps, start=1):
        steps.append(f"{i}. {s}")
    return (f"Root cause: {plan.root_cause}\n"
            f"Bug type: {plan.bug_type}\n"
            f"Files to change: {', '.join(plan.files)}\n"
            f"Functions to change: {', '.join(plan.functions)}\n"
            f"Steps:\n" + "\n".join(steps))
