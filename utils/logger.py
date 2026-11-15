# one json line per agent step

import json
import os
from datetime import datetime, timezone
from pathlib import Path

log_file = Path("runs") / "experiment_logs.jsonl"
run_id = ""


def set_log_file(path):
    global log_file
    log_file = Path(path)


def set_run_id(new_id):
    global run_id
    run_id = new_id


def scrub(text):
    if text is None:
        return None
    text = str(text)
    api_key = os.getenv("GROQ_API_KEY", "")
    if len(api_key) > 10:
        text = text.replace(api_key, "[REDACTED]")
    return text


def log_span(task_id, loop, agent, event_type, input_text, output_text,
             input_tokens, output_tokens, time_seconds, error_msg=None):
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "run_id": run_id,
        "task_id": str(task_id),
        "loop": loop,
        "agent": agent,
        "event_type": event_type,
        "input": scrub(input_text),
        "output": scrub(output_text),
        "tokens": {"input": input_tokens, "output": output_tokens},
        "time_seconds": time_seconds,
        "error_msg": scrub(error_msg),
    }
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
