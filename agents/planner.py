# planner agent: finds the bug and returns a fix plan as json. never writes code.

import time
from pathlib import Path

from agents.plan_schema import check_plan, format_plan, plan_problem
from agents.prompts import PLANNER_SYSTEM
from state import AgentState
from utils.llm import call_llm
from utils.logger import log_span


def build_planner_prompt(state: AgentState):
    parts = []

    # compiler_msg[0] is the first failure, compiler_msg[i + 1] is what plan i led to
    if state.strategy:
        parts.append("=== PREVIOUS ATTEMPTS (these plans did not fix the bug; do not repeat them) ===")
        for i, past in enumerate(state.strategy):
            result = "Unknown"
            if i + 1 < len(state.compiler_msg):
                result = state.compiler_msg[i + 1]
            parts.append(f"--- Attempt {i + 1} ---\nPlan:\n{past}\n\nPytest output after this attempt:\n{result}\n")

    parts.append("=== CURRENT CODE ===")
    parts.append(state.code[-1])
    parts.append("=== LATEST PYTEST OUTPUT ===")
    parts.append(state.compiler_msg[-1])
    parts.append("Reply with the JSON fix plan only.")
    return "\n\n".join(parts)


def run_planner(state: AgentState):
    task_dir = Path(state.task_dir)
    user_prompt = build_planner_prompt(state)
    start = time.time()

    res = call_llm(PLANNER_SYSTEM, user_prompt, model=state.model_name,
                   max_retries=state.max_llm_retries,
                   validate=lambda text: plan_problem(task_dir, text))

    log_span(
        task_id=state.task_id,
        loop=state.main_loop_count + 1,
        agent="Planner",
        event_type="llm_call" if res.accepted else "plan_invalid",
        input_text=f"SYSTEM:\n{PLANNER_SYSTEM}\n\nUSER:\n{user_prompt}",
        output_text=res.text,
        input_tokens=res.input_tokens,
        output_tokens=res.output_tokens,
        time_seconds=round(time.time() - start, 2),
        error_msg=res.error,
    )

    if not res.got_response:
        raise RuntimeError(f"Planner: no response from the model ({res.error})")

    if res.accepted:
        plan, _ = check_plan(task_dir, res.text)
        strategy_text = format_plan(plan)
        plan_record = {"valid": True}
        plan_record.update(plan.model_dump())
    else:
        # no valid plan after all retries: pass the raw reply on and keep going
        strategy_text = f"(Unstructured plan - the Planner's JSON was invalid)\n{res.text}"
        plan_record = {"valid": False, "files": [], "functions": [], "bug_type": None}

    return {
        "strategy": state.strategy + [strategy_text],
        "plans": state.plans + [plan_record],
        "llm_retry_count": state.llm_retry_count + res.calls,
        "input_tokens": state.input_tokens + res.input_tokens,
        "output_tokens": state.output_tokens + res.output_tokens,
    }
