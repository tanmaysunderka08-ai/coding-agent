import shlex
import subprocess
import uuid
from pathlib import Path

IMAGE = "sandbox"
DEFAULT_TIMEOUT = 30
PYTEST_CMD = "python -m pytest tests/ -q -p no:cacheprovider"
TIMEOUT_EXIT_CODE = 124


def run_in_sandbox(folder, command, timeout=DEFAULT_TIMEOUT):
    folder = Path(folder).resolve()
    if isinstance(command, str):
        args = shlex.split(command)
    else:
        args = list(command)
    name = f"sbx-{uuid.uuid4().hex[:12]}"

    docker_cmd = [
        "docker", "run", "--rm", "--name", name,
        "--network", "none",
        "--memory", "512m", "--memory-swap", "512m",
        "--cpus", "1",
        "--pids-limit", "128",
        "-e", "PYTHONDONTWRITEBYTECODE=1",
        "-v", f"{folder}:/app",
    ]
    tests_dir = folder / "tests"
    if tests_dir.is_dir():
        docker_cmd += ["-v", f"{tests_dir}:/app/tests:ro"]
    docker_cmd += ["-w", "/app", IMAGE] + args

    try:
        result = subprocess.run(docker_cmd, capture_output=True, text=True,
                                encoding="utf-8", errors="replace", timeout=timeout)
        return result.stdout + result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        subprocess.run(["docker", "rm", "-f", name], capture_output=True)
        return f"TIMEOUT: command did not finish within {timeout} seconds", TIMEOUT_EXIT_CODE


if __name__ == "__main__":
    here = Path(".").resolve()
    print(run_in_sandbox(here, "python -c \"print('hello from sandbox')\""))
    print(run_in_sandbox(here, "sleep 60", timeout=10))
    print(run_in_sandbox(here, "python -c \"import urllib.request as u; u.urlopen('http://google.com', timeout=5)\""))
