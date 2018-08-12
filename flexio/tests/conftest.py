import pytest

from flexio.app import create_app


@pytest.yield_fixture(scope='session')
def app():
    """
    Setup for the test app, gets executed only once.

    :return: Flask app
    """
    params = {
        'DEBUG': False,
        'TESTING': True,
        'WTF_CSRF_ENABLED': False
    }

    _app = create_app(settings_override=params)

    # Establich an app context before running the tests.
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.yield_fixture(scope='function')
def client(app):
    """
    Setup an app client, gets executed for each test function.

    :param app: Pytest fixture
    :return: Flask app client
    """
    yield app.test_client()
