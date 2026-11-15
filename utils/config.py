from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def load_config(path=None):
    if path is None:
        path = ROOT / "config.yaml"
    with open(path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}

    cfg.setdefault("mode", "team")
    cfg.setdefault("model_name", "openai/gpt-oss-120b")
    cfg.setdefault("strategy", "whole_files")
    cfg.setdefault("limits", {})
    cfg["limits"].setdefault("max_loops", 3)
    cfg["limits"].setdefault("max_llm_retries", 5)
    return cfg
