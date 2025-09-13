E2E Tests Execution Guide
========================

Before running tests, make sure you are in the root directory of the project.

For Bash / Zsh:

    export PYTHONPATH=$(pwd)
    pytest -s -vv --maxfail=1 tests/e2e

For Fish shell:

    set -x PYTHONPATH (pwd)
    pytest -s -vv --maxfail=1 tests/e2e
