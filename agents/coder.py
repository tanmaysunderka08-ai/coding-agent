# coder agent: gets the code, the pytest output and the planner's plan,
# and replies with whole files in the "### FILE: <path>" format.
# it may only overwrite source files that already exist (no new files, no tests).

import time
from pathlib import Path

from agents.prompts import CODER_SYSTEM
from state import AgentState
from utils.llm import call_llm
from utils.logger import log_span
from utils.text import strip_fences
from utils.workspace import read_workspace_code, source_files


def header_name(line):
    # "### FILE: a.py" -> "a.py", anything else -> None
    if not line.startswith("###"):
        return None
    rest = line[3:].lstrip()
    if not rest.startswith("FILE:"):
        return None
    name = rest[5:].strip()
    return name if name else None


def split_file_blocks(text):
    # [(name, code), ...] for every "### FILE:" block, in order
    lines = text.split("\n")
    blocks = []
    name = None
    body = []
    for i, line in enumerate(lines):
        new_name = header_name(line)
        # a header on the very last line has no code after it, ignore it
        if new_name is not None and i < len(lines) - 1:
            if name is not None:
                blocks.append((name, "\n".join(body)))
            name = new_name
            body = []
        elif name is not None:
            body.append(line)
    if name is not None:
        blocks.append((name, "\n".join(body)))
    return blocks


def is_diff_line(line):
    if line.startswith("@@") or line.startswith("+++ ") or line.startswith("--- "):
        return True
    
    return line[:1] in ("+", "-") and line[1:2] not in ("+", "-")


def looks_like_diff(code):
    if code.lstrip().startswith("@@"):
        return True
    count = 0
    for line in code.split("\n"):
        if is_diff_line(line):
            count += 1
    return count >= 2


def clean_path(raw):
    rel = raw.strip().strip("`*").replace("\\", "/")
    if rel.startswith("./"):
        rel = rel[2:]
    return rel


def check_llm_files(task_dir, reply):
    # returns (files, None) if the reply can be written, else (None, what is wrong)
    allowed = set()
    for rel in source_files(task_dir):
        allowed.add(rel.as_posix())

    files = {}
    refused = []
    blocks = split_file_blocks(reply)
    if blocks:
        for raw_name, code in blocks:
            rel = clean_path(raw_name)
            if rel not in allowed:
                refused.append(rel)
                print(f"[coder] refused write to {rel!r}")
                continue
            files[rel] = strip_fences(code).strip()
    elif len(allowed) == 1:
        # one file only and the model forgot the header
        only = list(allowed)[0]
        files[only] = strip_fences(reply).strip()
    else:
        return None, "there is no '### FILE: <path>' header before the code."

    non_empty = {}
    for rel, code in files.items():
        if code:
            non_empty[rel] = code
    files = non_empty

    if not files:
        if refused:
            return None, (f"you may only edit existing files: {', '.join(sorted(allowed))}. "
                          f"Not allowed: {', '.join(refused)}.")
        return None, "no file content was found after the '### FILE:' header."

    for rel, code in files.items():
        try:
            compile(code, rel, "exec")
        except SyntaxError as e:
            if looks_like_diff(code):
                return None, (f"the content for {rel} looks like a diff/patch. Send the COMPLETE file "
                              f"content (every line of {rel}), not only the changed lines.")
            return None, f"{rel} is not valid Python: {e.msg} (line {e.lineno})."
    return files, None


def parse_llm_files(task_dir, reply):
    return check_llm_files(task_dir, reply)[0]


def llm_files_problem(task_dir, reply):
    return check_llm_files(task_dir, reply)[1]


def write_files(task_dir, files):
    task_dir = Path(task_dir)
    for rel, code in files.items():
        (task_dir / rel).write_text(code.rstrip() + "\n", encoding="utf-8")


def run_coder(state: AgentState):
    task_dir = Path(state.task_dir)

    history = ""
    if len(state.strategy) > 1:
        lines = ["=== PREVIOUS ATTEMPTS (these did not fix the bug) ==="]
        for i in range(len(state.strategy) - 1):
            err = ""
            if i + 1 < len(state.compiler_msg):
                err = state.compiler_msg[i + 1]
            lines.append(f"--- Attempt {i + 1} ---\nPlan:\n{state.strategy[i]}\n\nPytest output after this attempt:\n{err}\n")
        history = "\n".join(lines) + "\n\n"

    user_prompt = (
        f"{history}"
        f"=== CURRENT CODE ===\n{state.code[-1]}\n\n"
        f"=== LATEST PYTEST OUTPUT ===\n{state.compiler_msg[-1]}\n\n"
        f"=== FIX PLAN ===\n{state.strategy[-1]}\n\n"
        "Reply with the ### FILE: blocks only."
    )

    start = time.time()
    res = call_llm(CODER_SYSTEM, user_prompt, model=state.model_name,
                   max_retries=state.max_llm_retries,
                   validate=lambda text: llm_files_problem(task_dir, text))

    if res.accepted:
        write_files(task_dir, parse_llm_files(task_dir, res.text))

    log_span(
        task_id=state.task_id,
        loop=state.main_loop_count + 1,
        agent="Coder",
        event_type="file_write" if res.accepted else "file_write_failed",
        input_text=f"SYSTEM:\n{CODER_SYSTEM}\n\nUSER:\n{user_prompt}",
        output_text=res.text,
        input_tokens=res.input_tokens,
        output_tokens=res.output_tokens,
        time_seconds=round(time.time() - start, 2),
        error_msg=res.error,
    )

    if not res.got_response:
        raise RuntimeError(f"Coder: no response from the model ({res.error})")
    # if the model answered but the code was never usable

    return {
        "code": state.code + [read_workspace_code(task_dir)],
        "llm_retry_count": state.llm_retry_count + res.calls,
        "input_tokens": state.input_tokens + res.input_tokens,
        "output_tokens": state.output_tokens + res.output_tokens,
    }
