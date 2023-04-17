import pytest
import os
import shutil
from remote_render import app

@pytest.fixture
def test_app():
    return app


@pytest.fixture
def test_database():
    # Reads database path from env (which should be .test.env by way of pytest.ini and pytest-dotenv)
    DATABASE = os.getenv('DATABASE_FOLDER')
    yield DATABASE

    # Clean up test database
    shutil.rmtree(DATABASE, ignore_errors=True)