import click
import unittest

from dotenv import load_dotenv

DEFAULT_RUN_COUNT = 1
DEFAULT_TEST_NAME = "fake_agent_test.test_chat"


@click.command()
@click.option(
    "--test_name",
    help="Name of the test suite and (optionally) the test case in the format 'suite.TestCase'",
)
@click.option("--run_count", help="Number of times to run the test")
def run_tests(test_name, run_count):

    if not test_name:
        click.secho(
            f"Warning: Not test name provided, using default {DEFAULT_TEST_NAME}. There will be no LLM apis calls for this test.",
            fg="yellow",
        )
        test_name = DEFAULT_TEST_NAME

    if not run_count:
        click.secho(
            f"Warning: No run count provided, using default {DEFAULT_RUN_COUNT}.",
            fg="yellow",
        )
        run_count = DEFAULT_RUN_COUNT

    test_suite = test_name.split(".")[0] if "." in test_name else test_name
    test_case = test_name.split(".")[1] if "." in test_name else None

    suite = find_test_file(test_suite)
    if suite.countTestCases() == 0:
        click.secho(f"No test file found for '{test_name}'", fg="red")
        return None

    if test_case is None or suite.countTestCases() == 1:
        click.secho(f"Running all tests in '{test_name}'", fg="green")
        runner = unittest.TextTestRunner()
        runner.run(suite)
    else:
        click.secho(f"Running test case '{test_case}' in '{test_name}'", fg="green")
        all_tests = get_all_tests_from_suite(suite)
        for test in all_tests:
            if test.id().endswith(test_case):
                runner = unittest.TextTestRunner()
                runner.run(test)
                break


def get_all_tests_from_suite(suite):
    """Recursively extracts all TestCase objects from a TestSuite."""
    tests = []
    for test in suite:
        if isinstance(test, unittest.TestCase):  # Check if it's a TestCase
            tests.append(test)
        else:
            tests.extend(
                get_all_tests_from_suite(test)
            )  # Recurse if it's another TestSuite
    return tests


def find_test_file(test_module):
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir="./py-server", pattern=f"{test_module}.py")
    return suite


if __name__ == "__main__":
    load_dotenv()
    run_tests()
