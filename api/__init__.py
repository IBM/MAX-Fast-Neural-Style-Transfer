from flask_restplus import Api
from flask import render_template, url_for

from config import API_TITLE, API_VERSION, API_DESC
from .model import api as model_ns

api = Api(
	title=API_TITLE,
	version=API_VERSION,
	description=API_DESC)

api.namespaces.clear()
api.add_namespace(model_ns)
