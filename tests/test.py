import pytest
import requests
import io
from PIL import Image


def test_swagger():

    model_endpoint = 'http://localhost:5000/swagger.json'

    r = requests.get(url=model_endpoint)
    assert r.status_code == 200
    assert r.headers['Content-Type'] == 'application/json'

    json = r.json()
    assert 'swagger' in json
    assert json.get('info') and json.get('info').get('title') == 'MAX Fast Neural Style Transfer'
    assert json.get('info') and json.get('info').get('description') == 'Generate a new image that mixes the ' \
                                                                       'content of a source image with the style of ' \
                                                                       'another image.'


def test_metadata():

    model_endpoint = 'http://localhost:5000/model/metadata'

    r = requests.get(url=model_endpoint)
    assert r.status_code == 200

    metadata = r.json()
    assert metadata['id'] == 'max-fast-neural-style-transfer'
    assert metadata['name'] == 'MAX Fast Neural Style Transfer'
    assert metadata['description'] == 'Pytorch Neural Style Transfer model trained on COCO 2014'
    assert metadata['type'] == 'Image-To-Image Translation'
    assert metadata['license'] == 'BSD-3-Clause'
    assert 'max-fast-neural-style-transfer' in metadata['source']


def call_model(model_type="mosaic", file_path="assets/flowers.jpg"):
    """helper function"""

    model_endpoint = 'http://localhost:5000/model/predict?model=' + model_type

    with open(file_path, 'rb') as file:
        file_form = {'image': (file_path, file, 'image/jpeg')}
        r = requests.post(url=model_endpoint, files=file_form)
        assert r.status_code == 200
        im = Image.open(io.BytesIO(r.content))
        return im


def test_invalid():
    model_endpoint = 'http://localhost:5000/model/predict'
    file_path="README.md"
    with open(file_path, 'rb') as file:
        file_form = {'image': (file_path, file, 'image/jpeg')}
        r = requests.post(url=model_endpoint, files=file_form)
    assert r.status_code == 400


def test_predict():

    """Test the mosaic model"""
    im = call_model(model_type="mosaic", file_path="assets/flowers.jpg")
    assert im.size == (640, 284)

    px_ctr_l_flower = im.getpixel((75, 170))  # the center of the flower on the left
    px_ctr_sky = im.getpixel((300, 30))  # near the center of the sky
    px_weeds = im.getpixel((240, 250))  # the brown weeds near the base of the 2nd flower

    # the center of the flower should be yellow (red + green but no blue)
    assert px_ctr_l_flower[0] > 150
    assert px_ctr_l_flower[1] > 150
    assert px_ctr_l_flower[2] < 50

    # the sky in this model is either blue or tan
    assert px_ctr_sky[0] > 125
    assert px_ctr_sky[1] > 125
    assert px_ctr_sky[2] > 125

    # the weeds should be dark
    assert px_weeds[0] < 50
    assert px_weeds[1] < 50
    assert px_weeds[2] < 50

    """Test the candy model"""
    im = call_model(model_type="candy", file_path="assets/flowers.jpg")
    assert im.size == (640, 284)

    px_ctr_l_flower = im.getpixel((75, 170))  # the center of the flower on the left
    px_ctr_sky = im.getpixel((300, 30))  # near the center of the sky
    px_weeds = im.getpixel((240, 250))  # the brown weeds near the base of the 2nd flower

    # the center of the flower should be orange (red + green but no blue)
    assert px_ctr_l_flower[0] > 150
    assert px_ctr_l_flower[1] > 100
    assert px_ctr_l_flower[2] < 50

    # the sky in this model the sky is orange
    assert px_ctr_sky[0] > 200
    assert px_ctr_sky[1] > 150
    assert px_ctr_sky[2] > 100

    # the weeds should be dark with a tint of red
    assert px_weeds[0] < 100
    assert px_weeds[1] < 50
    assert px_weeds[2] < 50

    """Test the rain princess model"""

    im = call_model(model_type="rain_princess", file_path="assets/flowers.jpg")
    assert im.size == (640, 284)

    px_ctr_l_flower = im.getpixel((75, 170))  # the center of the flower on the left
    px_ctr_sky = im.getpixel((300, 30))  # near the center of the sky
    px_weeds = im.getpixel((240, 250))  # the brown weeds near the base of the 2nd flower

    # the center of the flower should be yellow (red + green but no blue)
    assert px_ctr_l_flower[0] > 225
    assert px_ctr_l_flower[1] > 150
    assert px_ctr_l_flower[2] < 50

    # the sky in this model is dark blue
    assert px_ctr_sky[0] < 50
    assert px_ctr_sky[1] < 50
    assert px_ctr_sky[2] < 75
    assert px_ctr_sky[2] > px_ctr_sky[0]  # the sky is more blue than red
    assert px_ctr_sky[2] > px_ctr_sky[1]  # the sky is more blue than green

    # the weeds should be dark with a red tint
    assert 25 < px_weeds[0] < 75  # red tint
    assert px_weeds[1] < 50
    assert px_weeds[2] < 50

    """Test the udnie model"""
    im = call_model(model_type="udnie", file_path="assets/flowers.jpg")
    assert im.size == (640, 284)
    px_ctr_l_flower = im.getpixel((75, 170))  # the center of the flower on the left
    px_ctr_sky = im.getpixel((300, 30))  # near the center of the sky
    px_weeds = im.getpixel((240, 250))  # the brown weeds near the base of the 2nd flower

    # the center of the flower should be brown
    assert px_ctr_l_flower[0] > 25
    assert px_ctr_l_flower[1] > 20
    assert px_ctr_l_flower[2] < 25
    assert px_ctr_l_flower[0] > px_ctr_l_flower[1] > px_ctr_l_flower[2]  # mostly red, some green, tiny bit of blue

    # this pixel is milky, every value should be ~150
    assert 175 > px_ctr_sky[0] > 125
    assert 175 > px_ctr_sky[1] > 125
    assert 175 > px_ctr_sky[2] > 125

    # the weeds should be very dark brown
    assert px_weeds[0] < 25
    assert px_weeds[1] < 25
    assert px_weeds[2] < 25
    assert px_weeds[0] > px_weeds[1] > px_weeds[2]


if __name__ == '__main__':
    pytest.main([__file__])
