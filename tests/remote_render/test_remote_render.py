import pytest

@pytest.mark.parametrize('url', ['/', '/queue/', '/logs/', '/archive/'])
def test_app_get_request(test_app, url):

    response = test_app.test_client().get(url)
    assert response.status_code == 200

def test_make_render_start_log(test_app):

    # TODO
    assert False

def test_make_render_end_log(test_app):

    # TODO
    assert False

