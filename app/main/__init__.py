from flask import Blueprint

main = Blueprint(
    'main', __name__,
    template_folder='main-templates',
    static_folder='main-static'
)

from . import views
