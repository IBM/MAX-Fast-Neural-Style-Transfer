from flask_restplus import Namespace, Resource, fields
from flask import send_file, make_response
from werkzeug.datastructures import FileStorage

from config import MODEL_META_DATA, DEFAULT_MODEL, MODELS
from core.backend import ModelWrapper, read_image, write_image

api = Namespace('model', description='Model information and inference operations')

model_meta = api.model('ModelMetadata', {
    'id': fields.String(required=True, description='Model identifier'),
    'name': fields.String(required=True, description='Model name'),
    'description': fields.String(required=True, description='Model description'),
    'license': fields.String(required=False, description='Model license'),
    'type': fields.String(required=False, description='Model type')
})

@api.route('/metadata')
class Model(Resource):
    @api.doc('get_metadata')
    @api.marshal_with(model_meta)
    def get(self):
        '''Return the metadata associated with the model'''
        return MODEL_META_DATA

# set up parser for image input data
image_parser = api.parser()
image_parser.add_argument('image', type=FileStorage, location='files', required=True,
                            help='An image file (in PNG or JPG/JPEG format)')
image_parser.add_argument('model', type=str, default=DEFAULT_MODEL, choices=MODELS, 
                            help='Style transfer model to use for inference')

@api.route('/predict')
class Predict(Resource):

    model_wrapper = ModelWrapper()

    @api.doc('predict')
    @api.expect(image_parser)
    @api.doc(produces=['image/jpeg'])
    def post(self):
        '''Make a prediction given input data'''
        args = image_parser.parse_args()
        image_data = args['image'].read()
        image = read_image(image_data)
        model = args['model']
        output_image = self.model_wrapper.predict(image, model)
        return send_file(write_image(output_image), mimetype='image/jpeg', attachment_filename='img.jpg')
