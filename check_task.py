# the real grader. the agent never grades itself:
# its source files are copied next to the ORIGINAL tests and run again in the sandbox.

import shutil
import tempfile
from pathlib import Path

from sandbox.run_in_sandbox import PYTEST_CMD, TIMEOUT_EXIT_CODE, run_in_sandbox
from utils.hashing import hash_directory

SKIP = shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache")


def check_task(master_task_dir, student_dir, grader_dir, allowed_files):
    master = Path(master_task_dir)
    student = Path(student_dir)
    grader = Path(grader_dir)

    if hash_directory(master / "tests") != hash_directory(student / "tests"):
        return False, "test_tampering", ""

    if grader.exists():
        shutil.rmtree(grader)
    grader.mkdir(parents=True)

    # only the allowed source files, so an extra conftest.py etc. is never copied
    for rel in allowed_files:
        src = student / rel
        if src.exists():
            dst = grader / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    shutil.copytree(master / "tests", grader / "tests", ignore=SKIP)

    output, exit_code = run_in_sandbox(grader, PYTEST_CMD)
    if exit_code == 0:
        return True, "passed", output
    if exit_code == TIMEOUT_EXIT_CODE:
        return False, "timeout", output
    return False, "tests_failed", output


def validate_task(task_dir):
    task_dir = Path(task_dir)
    with tempfile.TemporaryDirectory() as tmp:
        copy = Path(tmp) / task_dir.name
        shutil.copytree(task_dir, copy, ignore=SKIP)
        output, exit_code = run_in_sandbox(copy, PYTEST_CMD)
    return exit_code != 0, output


if __name__ == "__main__":
    for task in sorted(Path("tasks").iterdir()):
        if not task.is_dir() or task.name.startswith("__"):
            continue
        ok, _ = validate_task(task)
        print(f"{task.name:30s} {'OK' if ok else 'BAD (tests pass on buggy code)'}")
