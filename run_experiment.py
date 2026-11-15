# runs one design (team or single) on all tasks, n runs each.
# writes runs/<design>_<time>.csv (one row per run) and a .jsonl log next to it.
#
#   python run_experiment.py --mode single --runs 1
#   python run_experiment.py --resume runs/<file>.csv

import argparse
import csv
from datetime import datetime
from pathlib import Path

from check_task import check_task, validate_task
from main import ACTIVE_RUN_DIR, run_task
from utils.config import ROOT, load_config
from utils.llm import DailyLimitReached
from utils.logger import set_log_file, set_run_id
from utils.workspace import source_files

COLUMNS = [
    "design", "mode", "strategy", "model", "task_id", "run", "passed", "reason",
    "attempts", "llm_calls", "input_tokens", "output_tokens", "duration_sec", "agent_says_pass",
    "plan_valid", "plan_files", "plan_bug_type", "plan_file_hit",
]


def load_task_info():
    # docs/tasks.csv is made by make_tasks.py, it has the real buggy file of each task
    path = ROOT / "docs" / "tasks.csv"
    info = {}
    if not path.exists():
        return info
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            info[row["task_id"]] = row
    return info


def first_plan_columns(plans, task_info):
    # what the planner said in its first plan (empty in single mode)
    cols = {"plan_valid": "", "plan_files": "", "plan_bug_type": "", "plan_file_hit": ""}
    if not plans:
        return cols

    first = plans[0]
    files = first.get("files") or []
    cols["plan_valid"] = 1 if first.get("valid") else 0
    cols["plan_files"] = "|".join(files)
    cols["plan_bug_type"] = first.get("bug_type") or ""
    # did the first plan point at the file that really has the bug?
    if first.get("valid") and task_info.get("buggy_file"):
        cols["plan_file_hit"] = 1 if task_info["buggy_file"] in files else 0
    return cols


def read_finished_runs(csv_path):
    # keep finished runs, drop crashed ones so they run again
    with open(csv_path, newline="", encoding="utf-8") as f:
        old_rows = list(csv.DictReader(f))

    kept = []
    for row in old_rows:
        if not row["reason"].startswith("agent_error"):
            kept.append(row)

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(kept)
    return old_rows, kept


def get_tasks(names):
    tasks = []
    for t in sorted((ROOT / "tasks").iterdir()):
        if not t.is_dir() or t.name.startswith("__") or t.name.startswith("."):
            continue
        if names and t.name not in names:
            continue
        tasks.append(t)
    return tasks


def main():
    cfg = load_config()
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=["team", "single"], default=cfg["mode"])
    p.add_argument("--model", default=cfg["model_name"])
    p.add_argument("--runs", type=int, default=3)
    p.add_argument("--tasks", nargs="*")
    p.add_argument("--name")
    p.add_argument("--resume")
    args = p.parse_args()

    cfg["mode"] = args.mode
    cfg["model_name"] = args.model
    design = args.name or f"{cfg['mode']}_{cfg['strategy']}"
    (ROOT / "runs").mkdir(exist_ok=True)

    done = set()
    if args.resume:
        csv_path = Path(args.resume)
        old_rows, kept = read_finished_runs(csv_path)
        for row in kept:
            done.add((row["task_id"], int(row["run"])))
        if old_rows:
            # same design and model as the rows already in the file
            first = old_rows[0]
            design = first["design"]
            cfg["mode"] = first["mode"]
            cfg["model_name"] = first["model"]
        print(f"resuming {csv_path.name}: {len(kept)} done ({cfg['mode']}, {cfg['model_name']})")
    else:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_path = ROOT / "runs" / f"{design}_{stamp}.csv"
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=COLUMNS).writeheader()
    set_log_file(csv_path.with_suffix(".jsonl"))

    # a task only counts if its tests fail on the buggy code
    tasks = []
    for t in get_tasks(args.tasks):
        ok, _ = validate_task(t)
        if ok:
            tasks.append(t)
        else:
            print(f"skipping {t.name}: tests already pass on the buggy code")

    grader_dir = ROOT / "sandbox" / "secure_evaluation"
    task_info = load_task_info()

    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        try:
            for task in tasks:
                allowed = [rel.as_posix() for rel in source_files(task)]
                for run in range(1, args.runs + 1):
                    if (task.name, run) in done:
                        continue
                    print(f"\n--- {task.name} run {run}/{args.runs} ---")
                    set_run_id(f"{task.name}#{run}")
                    result = run_task(str(task), cfg, verbose=False)

                    if result["error"]:
                        passed = False
                        reason = "agent_error: " + result["error"][:150]
                    else:
                        passed, reason, _ = check_task(task, ACTIVE_RUN_DIR, grader_dir, allowed)

                    print(f"{'PASS' if passed else 'FAIL'} ({reason}), attempts={result['attempts']}, "
                          f"tokens={result['input_tokens']}+{result['output_tokens']}")

                    row = {
                        "design": design,
                        "mode": cfg["mode"],
                        "strategy": cfg["strategy"],
                        "model": cfg["model_name"],
                        "task_id": task.name,
                        "run": run,
                        "passed": int(passed),
                        "reason": reason,
                        "attempts": result["attempts"],
                        "llm_calls": result["llm_calls"],
                        "input_tokens": result["input_tokens"],
                        "output_tokens": result["output_tokens"],
                        "duration_sec": result["duration_sec"],
                        "agent_says_pass": int(result["agent_says_pass"]),
                    }
                    row.update(first_plan_columns(result["plans"], task_info.get(task.name, {})))
                    writer.writerow(row)
                    f.flush()
        except DailyLimitReached as e:
            # the run in progress is lost, finished rows are already in the csv
            print("\ndaily token limit reached, stopping.")
            print(str(e)[:300])
            return

    print(f"\ndone, results in {csv_path}")


if __name__ == "__main__":
    main()
