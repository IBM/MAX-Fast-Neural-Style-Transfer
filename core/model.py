import io
import logging
import torch
from torch.autograd import Variable as V
from torchvision import transforms as trn
from PIL import Image
from core.transformer_net import TransformerNet
from maxfw.model import MAXModelWrapper


logger = logging.getLogger()


class ModelWrapper(MAXModelWrapper):

    MODELS = ['mosaic', 'candy', 'rain_princess', 'udnie']
    MODEL_NAME = 'Fast Neural Style Transfer'
    DEFAULT_MODEL_PATH = 'assets'
    DEFAULT_MODEL = 'mosaic'
    MODEL_INPUT_IMG_SIZE = (256, 256)
    MODEL_LICENSE = 'BSD-3-Clause'
    MODEL_META_DATA = {
        'id': '{}-pytorch'.format(MODEL_NAME.lower().replace(' ', '-')),
        'name': '{} in Pytorch'.format(MODEL_NAME),
        'description': 'Pytorch Neural Style Transfer model trained on COCO 2014',
        'type': 'image_style_transfer',
        'license': '{}'.format(MODEL_LICENSE),
        'source': 'https://github.com/IBM/MAX-Fast-Neural-Style-Transfer'
    }

    models = {}

    """Model wrapper for PyTorch models"""
    def __init__(self, path=DEFAULT_MODEL_PATH):
        logger.info('Loading models from: {}...'.format(path))
        for m in self.MODELS:
            style_model = TransformerNet()
            model_path = '{}/{}.pth'.format(path, m)
            model = torch.load(model_path, map_location=lambda storage, loc: storage)  # cpu only for now ...
            style_model.load_state_dict(model)
            self.models[m] = style_model
        logger.info('Loaded models')
        self._load_assets(path)

    def read_image(self, image_data):
        return Image.open(io.BytesIO(image_data)).convert("RGB")

    def write_image(self, image):
        bio = io.BytesIO()
        image.save(bio, 'JPEG')
        bio.seek(0)
        return bio

    def _pre_process(self, image):
        # load the image transformer
        content_transform = trn.Compose([
            trn.ToTensor(),
            trn.Lambda(lambda x: x.mul(255))
        ])
        return V(content_transform(image).unsqueeze(0), volatile=True)

    def _post_process(self, x):
        return Image.fromarray(x)

    def _load_assets(self, path):
        pass

    def predict(self, args):
        image_data = args['image'].read()
        x = self.read_image(image_data)
        model = args['model']

        m = self.models[model]
        x = self._pre_process(x)
        output = m.forward(x)
        output_img = output.data[0].clone().clamp(0, 255).numpy()
        output_img = output_img.transpose(1, 2, 0).astype('uint8')
        return self._post_process(output_img)
