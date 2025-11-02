import logging

pytest_plugins = [
    "tests.e2e.fixtures.fxt_base",
    "tests.e2e.fixtures.users",
    "tests.e2e.fixtures.category",
]


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
