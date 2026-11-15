# runs one task once with the mode in config.yaml (team or single).

import shutil
import sys
import time
from pathlib import Path

from utils.config import ROOT, load_config
from utils.hashing import hash_directory
from utils.llm import DailyLimitReached

ACTIVE_RUN_DIR = ROOT / "sandbox" / "active_run"


def prepare_active_workspace(source_task_dir, active_run_dir):
    if not source_task_dir.exists():
        raise FileNotFoundError(f"task folder not found: {source_task_dir}")
    if active_run_dir.exists():
        shutil.rmtree(active_run_dir)
    active_run_dir.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source_task_dir, active_run_dir,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache"))


def run_team(task_id, config):
    from graph import app
    from state import AgentState

    max_loops = config["limits"]["max_loops"]
    start_state = AgentState(
        task_dir=str(ACTIVE_RUN_DIR),
        task_id=task_id,
        model_name=config["model_name"],
        max_loops=max_loops,
        max_llm_retries=config["limits"]["max_llm_retries"],
    )
    out = app.invoke(start_state, config={"recursion_limit": 3 * max_loops + 5})
    if isinstance(out, dict):
        return out
    return out.model_dump()


def run_task(task_path, config=None, verbose=True):
    if config is None:
        config = load_config()
    source_task_dir = Path(task_path).resolve()
    task_id = source_task_dir.name

    prepare_active_workspace(source_task_dir, ACTIVE_RUN_DIR)
    tests_dir = ACTIVE_RUN_DIR / "tests"
    hash_before = hash_directory(tests_dir)

    start = time.time()
    error = None
    final = {}
    try:
        if config["mode"] == "team":
            final = run_team(task_id, config)
        elif config["mode"] == "single":
            from agents.single_agent import run_single_agent
            final = run_single_agent(ACTIVE_RUN_DIR, task_id, config)
        else:
            raise ValueError(f"unknown mode: {config['mode']}")
    except DailyLimitReached:
        raise
    except Exception as e:
        error = f"{type(e).__name__}: {e}"
        print(f"run crashed: {error}")

    tests_intact = hash_before == hash_directory(tests_dir)
    result = {
        "task_id": task_id,
        "mode": config["mode"],
        "agent_says_pass": final.get("sandbox_exit_code") == 0 and tests_intact,
        "tests_intact": tests_intact,
        "attempts": final.get("main_loop_count", 0),
        "llm_calls": final.get("llm_retry_count", 0),
        "input_tokens": final.get("input_tokens", 0),
        "output_tokens": final.get("output_tokens", 0),
        "duration_sec": round(time.time() - start, 2),
        "error": error,
        "plans": final.get("plans", []),
    }

    if verbose:
        print(f"\ntask: {task_id}, mode: {config['mode']}")
        print(f"agent says: {'pass' if result['agent_says_pass'] else 'fail'}")
        if not tests_intact:
            print("tests were changed, run does not count")
        print(f"attempts: {result['attempts']}/{config['limits']['max_loops']}, llm calls: {result['llm_calls']}")
        print(f"tokens in/out: {result['input_tokens']}/{result['output_tokens']}")
        if error:
            print(f"error: {error}")
        if final.get("compiler_msg"):
            print("\nlast pytest output:")
            print(final["compiler_msg"][-1])

    return result


if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = "tasks/task_01_active_users"
    run_task(target)
