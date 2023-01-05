from flask import Blueprint


admin_panel = Blueprint(
    'admin_panel', __name__,
    template_folder='admin-templates'
    # static_folder='admin-static'
)

from . import views


