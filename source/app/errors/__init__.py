# Errors blueprint init 
from flask import Blueprint

errors = Blueprint('errors', __name__)

from .handlers import * 