#!/usr/bin/env python3
"""Install and launch the OpenCode CLI on Ubuntu/Debian-based Linux."""

from __future__ import annotations

import shutil
import subprocess
import sys
import time


def run(command: list[str], *, check: bool = True) -> subprocess.CompletedProcess:
    """Run a command and show its output."""
    print(f"\n$ {' '.join(command)}", flush=True)
    return subprocess.run(command, check=check)


def require_linux() -> None:
    if not sys.platform.startswith("linux"):
        raise SystemExit("This installer is intended for Linux, especially Ubuntu/Debian.")
    if shutil.which("apt-get") is None:
        raise SystemExit("APT was not found. This script supports Ubuntu/Debian-based systems.")


def main() -> int:
    print("=" * 56)
    print(" OpenCode CLI installer")
    print(" Ubuntu / Debian")
    print("=" * 56)
    print("This script installs system packages and the OpenCode CLI.")
    print("You may be asked for your sudo password.")
    time.sleep(1)

    require_linux()

    run(["sudo", "apt-get", "update"])
    run(["sudo", "apt-get", "install", "-y", "nodejs", "npm"])

    if shutil.which("npm") is None:
        raise SystemExit("npm was not found after installation. Check the package installation.")

    # Install globally for the current system, matching the original script's intent.
    run(["sudo", "npm", "install", "--global", "opencode-ai"])

    print("\nInstallation finished.")
    print("Starting OpenCode. If the command is not found, reopen the terminal and check PATH.")
    time.sleep(1)

    if shutil.which("opencode") is None:
        print("The 'opencode' command is not currently on PATH.", file=sys.stderr)
        print("Try: npm bin -g (or check npm's global bin directory).", file=sys.stderr)
        return 1

    return subprocess.run(["opencode"], check=False).returncode


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        print(f"\nError: command failed with exit code {exc.returncode}.", file=sys.stderr)
        raise SystemExit(exc.returncode)
    except KeyboardInterrupt:
        print("\nCancelled by user.", file=sys.stderr)
        raise SystemExit(130)
