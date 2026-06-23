#!/usr/bin/env python3
"""Build Quartz site into docs/ and push to GitHub.

Usage:
    python deploy.py
    python deploy.py "custom commit message"
"""
import subprocess
import sys
from datetime import datetime


def run(cmd):
    print(f"$ {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"Failed: {cmd}")
        sys.exit(1)


def main():
    message = sys.argv[1] if len(sys.argv) > 1 else f"Update site - {datetime.now():%Y-%m-%d %H:%M}"

    run("npx quartz build -o docs")
    run("git add -A")

    commit = subprocess.run(f'git commit -m "{message}"', shell=True)
    if commit.returncode != 0:
        print("Nothing to commit. Exiting.")
        return

    run("git push")
    print("Deployed.")


if __name__ == "__main__":
    main()