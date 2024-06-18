from falcon import testing
import pytest

from .app import create_app


# Depending on your testing strategy and how your application
# manages state, you may be able to broaden the fixture scope
# beyond the default 'function' scope used in this example.

@pytest.fixture()
def client():
    # Assume the hypothetical `app` package has a function called
    # create_app which returns a `falcon.asgi.App` instance.
    return testing.TestClient(create_app())
