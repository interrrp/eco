default: check lint format

run:
    python -m eco

check:
    mypy eco

lint:
    ruff eco

format:
    black eco
    isort eco

clean:
    rm -rf **/__pycache__

install-hooks:
    pre-commit install
