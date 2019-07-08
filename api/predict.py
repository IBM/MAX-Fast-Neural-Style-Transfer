#
# Copyright 2018-2019 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from flask import send_file
from werkzeug.datastructures import FileStorage

from maxfw.core import MAX_API, PredictAPI
from core.model import ModelWrapper

model_wrapper = ModelWrapper()


input_parser = MAX_API.parser()
input_parser.add_argument('image', type=FileStorage, location='files', required=True)
input_parser.add_argument('model', type=str, default=model_wrapper.DEFAULT_MODEL, choices=model_wrapper.MODELS)


class ModelPredictAPI(PredictAPI):

    @MAX_API.doc('predict')
    @MAX_API.expect(input_parser)
    def post(self):
        """Make a prediction given input data"""
        args = input_parser.parse_args()
        output_image = model_wrapper.predict(args)
        return send_file(model_wrapper.write_image(output_image), mimetype='image/jpeg', attachment_filename='img.jpg')
