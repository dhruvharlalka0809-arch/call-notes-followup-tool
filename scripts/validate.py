import subprocess
import sys


COMMANDS = [
    [sys.executable, "-m", "py_compile", "streamlit_app.py", "followup.py", "followup_preview.py", "tests/test_followup_preview.py"],
    [sys.executable, "-m", "unittest", "discover", "-s", "tests"],
]


def main() -> int:
    for command in COMMANDS:
        print("+", " ".join(command))
        completed = subprocess.run(command, check=False)
        if completed.returncode:
            return completed.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
