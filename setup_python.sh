#!/usr/bin/env bash

set -euo pipefail

PYTHON_VERSION="3.12.1"

install_uv() {
    if command -v uv &> /dev/null; then
        echo "uv is already installed."
    else
        echo "Installing uv..."
        curl -LsSf https://astral.sh/uv/0.5.24/install.sh | sh

        echo 'eval "$(uv generate-shell-completion bash)"' >> ~/.bashrc
        source ~/.bashrc
        echo "uv installation complete. Please restart your terminal or run 'source ~/.bashrc' to apply changes."
    fi
}

init_uv_project() {
    install_uv
    if [ ! -f "pyproject.toml" ]; then
        echo "Initializing new poetry project..."
        uv init --python "${PYTHON_VERSION}"
        uv add --dev dash ipykernel mypy nbformat plotly pre-commit pytest ruff tqdm
    else
        echo "Poetry project already initialized. Updating dependencies..."
        uv sync
    fi
}

setup_python_project() {
    init_uv_project
    echo "All setup tasks completed successfully."
}

setup_python_project
