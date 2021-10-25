import pytest
from pytest import fixture

from main import create_app


@fixture
def app():
    app = create_app()
    app.testing = True
    return app
