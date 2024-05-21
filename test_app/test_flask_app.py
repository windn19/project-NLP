import os

import pytest
print(os.getcwd())
from app import app


@pytest.fixture()
def test_app1():
    test_app = app
    test_app.config['TESTING'] = True
    yield test_app


@pytest.fixture()
def client(test_app1):
    return test_app1.test_client()


def test_predict(client):
    resource = client.post('/predict', data={'file': open('RpprU19wXUI.jpg', mode='rb')})
    assert resource.status_code == 200, 'Not a file'
