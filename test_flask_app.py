from PIL import Image
import pytest

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
    resource = client.post('/predict', data={'file': Image.open('RpprU19wXUI.jpg')})
    assert resource.status_code == 200, 'Not a file'
