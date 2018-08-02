# Application settings

# Flask settings 
DEBUG = False

# Flask-restplus settings
RESTPLUS_MASK_SWAGGER = False
SWAGGER_UI_DOC_EXPANSION = 'none'

# API metadata
API_TITLE = 'Model Asset Exchange Server'
API_DESC = 'An API for serving models'
API_VERSION = '0.1'

# models
MODELS = ['mosaic', 'candy', 'rain_princess', 'udnie']
# default model
MODEL_NAME = 'Fast Neural Style Transfer'
DEFAULT_MODEL_PATH = 'assets'
DEFAULT_MODEL = 'mosaic'
# for image models, may not be required
MODEL_INPUT_IMG_SIZE = (256, 256)
MODEL_LICENSE = 'BSD-3-Clause'

MODEL_META_DATA = {
    'id': '{}-pytorch'.format(MODEL_NAME.lower().replace(' ', '-')),
    'name': '{} in Pytorch'.format(MODEL_NAME),
    'description': 'Pytorch Neural Style Transfer model trained on COCO 2014',
    'type': 'image_style_transfer',
    'license': '{}'.format(MODEL_LICENSE)
}
