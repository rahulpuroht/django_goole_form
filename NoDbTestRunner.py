from django.test.runner import DiscoverRunner


class NoDbTestRunner(DiscoverRunner):
    """
    Test runner to by pass db creation.
    Before running tests, django tries to create a test db, it will fire syncdb command to do so.
    This in turn fires model validation and the following code gets executed.
    SuperReceptionist.utils imports selfserve.helpers.country_code.lookup function.
    However, country_code module calls country_code.loadup function to load country codes from database.
    At this point of time, the database doesn't exist and syncdb will fail because of model validation.
    To bypass this, we need to use this TestRunner which ignores creating/dropping the test db.
    Use --testrunner=NoDbTestRunner.NoDbTestRunner switch while running unit tests from django.
    For any db related operations, use mock.
    """
    def setup_databases(self, **kwargs):
        pass

    def teardown_databases(self, old_config, **kwargs):
        pass
