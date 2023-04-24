import pytest
import os

@pytest.mark.parametrize('url', ['/', '/queue/', '/logs/', '/archive/'])
def test_app_get_request(test_app, url):

    response = test_app.get(url)
    assert response.status_code == 200

def test_make_render_start_log(test_app):

    # TODO
    assert True

def test_make_render_end_log(test_app):

    # TODO
    assert True

def test_database_folder_generation(test_app, test_database):

    assert os.path.exists(test_database)