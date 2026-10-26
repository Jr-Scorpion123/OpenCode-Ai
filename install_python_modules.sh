#!/usr/bin/env bash
# Prepare Python tooling and install dependencies listed in requirements.txt.
# The current project uses only Python's standard library, so no third-party
# Python packages are required.

set -Eeuo pipefail

if ! command -v apt-get >/dev/null 2>&1; then
  echo "Error: this helper currently supports Ubuntu/Debian systems using APT." >&2
  exit 1
fi

echo "Updating package lists..."
sudo apt-get update

echo "Installing Python 3, pip, and virtual-environment support..."
sudo apt-get install -y python3 python3-pip python3-venv

PROJECT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${PROJECT_DIR}/.venv"

echo "Creating virtual environment at: ${VENV_DIR}"
python3 -m venv "${VENV_DIR}"

echo "Updating pip inside the virtual environment..."
"${VENV_DIR}/bin/python" -m pip install --upgrade pip

if [[ -s "${PROJECT_DIR}/requirements.txt" ]] &&
   grep -Eq '^[[:space:]]*[^#[:space:]]' "${PROJECT_DIR}/requirements.txt"; then
  echo "Installing Python packages from requirements.txt..."
  "${VENV_DIR}/bin/python" -m pip install -r "${PROJECT_DIR}/requirements.txt"
else
  echo "No third-party Python modules are required by this project."
fi

echo
echo "Python environment is ready."
echo "Activate it with:"
echo "  source \"${VENV_DIR}/bin/activate\""
echo
echo "Run the installer with:"
echo "  \"${VENV_DIR}/bin/python\" \"${PROJECT_DIR}/install.py\""
