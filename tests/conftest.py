import pytest
import os
import shutil
from remote_render import app

# - pytest.ini contains pytest configuration details
# - .test.env is the testing environment file
# - pytest-dotenv will automatically read .env and then .test.env

# pytest fixtures:

@pytest.fixture
def test_app(test_database):

    app.testing = True
    app.check_database(test_database)
    with app.test_client() as test_client:
        with app.app_context():
            yield test_client


@pytest.fixture
def test_database():
    # Reads database path from env (which should be .test.env by way of pytest.ini and pytest-dotenv)
    DATABASE = os.getenv('DATABASE_FOLDER')
    yield DATABASE
    # Clean up test database
    shutil.rmtree(DATABASE, ignore_errors=True)