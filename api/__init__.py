from flask_restplus import Api
from flask import render_template, url_for

from config import API_TITLE, API_VERSION, API_DESC
from .model import api as model_ns

api = Api(
	title=API_TITLE,
	version=API_VERSION,
	description=API_DESC)

@api.documentation
def custom_ui():
	swagger_static = url_for('static', filename='swagger-ui-dist')
	return render_template('index.html', swagger_static=swagger_static)

api.add_namespace(model_ns)