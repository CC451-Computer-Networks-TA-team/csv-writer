import pytest
import csv
from csvwriter import extract_name_id, SubmissionsResult
from pathlib import Path
from _pytest.nodes import Item
from _pytest.runner import CallInfo
from _pytest.main import Session

submissions_result = SubmissionsResult()
RESULT_CSV = Path() / "result.csv"



@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: Item, call: CallInfo):
    """
    This hook will run after each test, it will construct the result dictionary 
    that will be written to the csv after all the tests are finished  
    """
    outcome = yield  # Run all other pytest_runtest_makereport non wrapped hooks
    test_result = outcome.get_result()
    # Proceed if the test is in the call stage and it's a parametrized test
    if test_result.when == "call" and 'parametrize' in test_result.keywords:
        # Get the test function name and the submission ID (one or more student IDs)
        test_name, submission_id = extract_name_id(item.name)
        # If this test function is seen for the first time append it to the list of fields
        if test_name not in submissions_result.fieldnames:
            submissions_result.fieldnames.append(test_name)
        # Add the result of the current test to the corresponding submission
        submissions_result.add_submission_result(submission_id, test_name, test_result.outcome)


@pytest.hookimpl
def pytest_sessionfinish(session: Session):
    # write the results to the csv file
    with open(str(RESULT_CSV), 'w', newline='') as csvfile:
        try:
            writer = csv.DictWriter(csvfile, fieldnames=submissions_result.fieldnames)
            writer.writeheader()
            for sub in submissions_result.results.values():
                writer.writerow(sub)
        except Exception as err:
            print(err)