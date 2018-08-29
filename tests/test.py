import pytest
import requests


def call_model(model_type="mosaic", file_path="assets/beach-city.jpg"):

    model_endpoint = 'http://localhost:5000/model/predict?model=' + model_type

    with open(file_path, 'rb') as file:
        file_form = {'image': (file_path, file, 'image/jpeg')}
        r = requests.post(url=model_endpoint, files=file_form)
        return r


def test_response():

    r = call_model(model_type="mosaic")
    assert r.status_code == 200
    # TODO - add tests here

    r = call_model(model_type="candy")
    assert r.status_code == 200
    # TODO - add tests here

    r = call_model(model_type="rain_princess")
    assert r.status_code == 200
    # TODO - add tests here

    r = call_model(model_type="udnie")
    assert r.status_code == 200
    # TODO - add tests here


if __name__ == '__main__':
    pytest.main([__file__])
