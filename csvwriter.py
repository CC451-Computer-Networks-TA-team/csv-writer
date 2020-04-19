def extract_name_id(name_id: str):
    """
    >>> extract_name_id("test_example[6-36]")
    ["test_example", "6-36"]
    """
    # Extract the name of the test function ("test_example")
    test_name = name_id.split('[')[0]
    # Extract the id of the test ("6-36")
    submission_id = name_id[name_id.find('[')+1:-1]
    return [test_name, submission_id]


class SubmissionsResult:
    def __init__(self):
        # fieldnames represents the column names in the csv file
        # it consists of an 'id' column followed by a column for each test function name
        self.fieldnames = ['id']
        # results example value:
        # {'1234_4321': {'id': '1234_4321', 'test_func1': passed, 'test_func2': failed} }
        self.results = {}

    def add_submission_result(self, submission_id, test_name, outcome):
        if submission_id in self.results:
            self.results[submission_id][test_name] = outcome
        else:
            self.results[submission_id] = {'id': submission_id, test_name: outcome}