default: check lint format

run:
    python -m eco

run-admin:
    python -m admin

check:
    mypy common eco admin

lint:
    ruff common eco admin

format:
    black common eco admin
    isort common eco admin

clean:
    rm -rf **/__pycache__

install-hooks:
    pre-commit install
