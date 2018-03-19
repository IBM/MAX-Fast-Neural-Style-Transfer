import torch
from torch.autograd import Variable as V
from torchvision import transforms as trn
from torch.nn import functional as F

import io
from PIL import Image
import logging

from config import MODEL_INPUT_IMG_SIZE, MODELS, DEFAULT_MODEL_PATH, DEFAULT_MODEL
from core.transformer_net import TransformerNet

logger = logging.getLogger()

def read_image(image_data):
    image = Image.open(io.BytesIO(image_data))
    return image

def write_image(image):
    bio = io.BytesIO()
    image.save(bio, 'JPEG')
    bio.seek(0)
    return bio

def preprocess_image(image, target):
    # load the image transformer
    content_transform = trn.Compose([
        trn.ToTensor(),
        trn.Lambda(lambda x: x.mul(255))
    ])
    return V(content_transform(image).unsqueeze(0), volatile=True)

def post_process_result(x):
    result = Image.fromarray(x)
    return result
    

class ModelWrapper(object):
 
    models = {}

    """Model wrapper for PyTorch models"""
    def __init__(self, path=DEFAULT_MODEL_PATH):
        logger.info('Loading models from: {}...'.format(path))
        for m in MODELS:
            style_model = TransformerNet()
            model_path = '{}/{}.pth'.format(path, m)
            model = torch.load(model_path, map_location=lambda storage, loc: storage) # cpu only for now ...
            style_model.load_state_dict(model)
            self.models[m] = style_model
        logger.info('Loaded models')
        self._load_assets(path)

    def _load_assets(self, path):
        pass

    def predict(self, x, model):
        m = self.models[model]
        x = preprocess_image(x, MODEL_INPUT_IMG_SIZE)
        output = m.forward(x)
        output_img = output.data[0].clone().clamp(0, 255).numpy()
        output_img = output_img.transpose(1, 2, 0).astype('uint8')
        return post_process_result(output_img)
