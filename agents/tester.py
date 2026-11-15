# tester: no llm, just runs pytest in the sandbox

import time
from pathlib import Path

from sandbox.run_in_sandbox import PYTEST_CMD, run_in_sandbox
from state import AgentState
from utils.logger import log_span
from utils.workspace import read_workspace_code


def run_tester(state: AgentState):
    task_dir = Path(state.task_dir)

    # first visit: save the original code. after that the coder adds the new code.
    if state.code:
        code_list = state.code
    else:
        code_list = [read_workspace_code(task_dir)]

    
    if state.strategy:
        attempt = state.main_loop_count + 1
    else:
        attempt = 0

    start = time.time()
    output, exit_code = run_in_sandbox(task_dir, PYTEST_CMD)

    log_span(
        task_id=state.task_id,
        loop=attempt,
        agent="Tester",
        event_type="sandbox_execution",
        input_text=PYTEST_CMD,
        output_text=output,
        input_tokens=0,
        output_tokens=0,
        time_seconds=round(time.time() - start, 2),
        error_msg=None if exit_code == 0 else f"exit code {exit_code}",
    )

    return {
        "code": code_list,
        "compiler_msg": state.compiler_msg + [output],
        "sandbox_exit_code": exit_code,
        "main_loop_count": attempt,
    }
