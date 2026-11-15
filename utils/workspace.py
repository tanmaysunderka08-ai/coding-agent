from pathlib import Path

SKIP_DIRS = {"tests", "__pycache__", ".pytest_cache", ".git"}


def source_files(task_dir):
    task_dir = Path(task_dir)
    files = []
    for path in sorted(task_dir.rglob("*.py")):
        rel = path.relative_to(task_dir)
        if SKIP_DIRS.intersection(rel.parts):
            continue
        files.append(rel)
    return files


def read_workspace_code(task_dir):
    task_dir = Path(task_dir)
    blocks = []
    for rel in source_files(task_dir):
        content = (task_dir / rel).read_text(encoding="utf-8")
        blocks.append(f"### FILE: {rel.as_posix()}\n{content}")
    return "\n\n".join(blocks)
