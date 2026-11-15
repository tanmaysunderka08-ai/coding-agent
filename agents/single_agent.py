# single agent baseline: one llm finds the bug and writes the fix.


import time
from pathlib import Path

from agents.coder import llm_files_problem, parse_llm_files, write_files
from agents.prompts import SINGLE_SYSTEM
from sandbox.run_in_sandbox import PYTEST_CMD, run_in_sandbox
from utils.llm import call_llm
from utils.logger import log_span
from utils.workspace import read_workspace_code


def run_tests(task_dir, task_id, attempt):
    start = time.time()
    output, exit_code = run_in_sandbox(task_dir, PYTEST_CMD)
    log_span(task_id=task_id, loop=attempt, agent="SingleAgent", event_type="sandbox_execution",
             input_text=PYTEST_CMD, output_text=output, input_tokens=0, output_tokens=0,
             time_seconds=round(time.time() - start, 2),
             error_msg=None if exit_code == 0 else f"exit code {exit_code}")
    return output, exit_code


def run_single_agent(task_dir, task_id, config):
    task_dir = Path(task_dir)
    model = config["model_name"]
    max_loops = config["limits"]["max_loops"]
    max_retries = config["limits"]["max_llm_retries"]

    calls = 0
    tokens_in = 0
    tokens_out = 0
    history = []

    output, exit_code = run_tests(task_dir, task_id, 0)
    attempt = 0

    while exit_code != 0 and attempt < max_loops:
        attempt += 1
        prompt = ""
        if history:
            prompt += "=== PREVIOUS ATTEMPTS (these did not fix the bug; do not repeat them) ===\n" + "\n".join(history) + "\n\n"
        prompt += (f"=== CURRENT CODE ===\n{read_workspace_code(task_dir)}\n\n"
                   f"=== LATEST PYTEST OUTPUT ===\n{output}\n\n"
                   "Reply with the ### FILE: blocks only.")

        start = time.time()
        res = call_llm(SINGLE_SYSTEM, prompt, model=model, max_retries=max_retries,
                       validate=lambda t: llm_files_problem(task_dir, t))
        calls += res.calls
        tokens_in += res.input_tokens
        tokens_out += res.output_tokens

        if res.accepted:
            write_files(task_dir, parse_llm_files(task_dir, res.text))

        log_span(task_id=task_id, loop=attempt, agent="SingleAgent",
                 event_type="llm_call_and_write" if res.accepted else "file_write_failed",
                 input_text=f"SYSTEM:\n{SINGLE_SYSTEM}\n\nUSER:\n{prompt}", output_text=res.text,
                 input_tokens=res.input_tokens, output_tokens=res.output_tokens,
                 time_seconds=round(time.time() - start, 2), error_msg=res.error)

        if not res.got_response:
            raise RuntimeError(f"SingleAgent: no response from the model ({res.error})")

        output, exit_code = run_tests(task_dir, task_id, attempt)
        history.append(f"--- Attempt {attempt} ---\nYou generated:\n{res.text}\n"
                       f"Which resulted in this pytest output:\n{output}\n")

    return {
        "sandbox_exit_code": exit_code,
        "main_loop_count": attempt,
        "llm_retry_count": calls,
        "input_tokens": tokens_in,
        "output_tokens": tokens_out,
        "compiler_msg": [output],
    }
