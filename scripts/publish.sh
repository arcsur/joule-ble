#!/usr/bin/env bash
# Script to build and upload joule-ble to PyPI using twine.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${ROOT_DIR}"

TARGET="${1:-pypi}"

echo "==> Cleaning previous build artifacts..."
rm -rf dist/ build/ *.egg-info

echo "==> Running lint and test suite..."
./.venv/bin/ruff check src tests
./.venv/bin/ruff format --check src tests
./.venv/bin/mypy src/joule_ble
PYTHONPATH=src ./.venv/bin/pytest tests/ -v

echo "==> Building distribution packages (sdist & wheel)..."
./.venv/bin/python3 -m build

echo "==> Checking distribution packages with twine..."
./.venv/bin/twine check dist/*

if [ "${TARGET}" = "testpypi" ]; then
    echo "==> Uploading to TestPyPI..."
    ./.venv/bin/twine upload --repository testpypi dist/*
    echo "==> Successfully published to TestPyPI!"
    echo "    Install with: pip install --index-url https://test.pypi.org/simple/ --no-deps joule-ble"
elif [ "${TARGET}" = "pypi" ]; then
    echo "==> Uploading to PyPI (production)..."
    ./.venv/bin/twine upload dist/*
    echo "==> Successfully published to PyPI!"
    echo "    Install with: pip install joule-ble"
else
    echo "Unknown target: ${TARGET}. Use 'pypi' or 'testpypi'."
    exit 1
fi
