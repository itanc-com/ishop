import pytest

if __name__ == "__main__":
    # List the test directories
    test_directories = ["tests/unit", "tests/integration", "tests/e2e"]

    # Run all the tests from the specified directories
    pytest.main(test_directories)
