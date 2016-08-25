from jinja2 import FileSystemLoader, Environment
from flask import (
    Blueprint,
    current_app,
    render_template,
)


bp = Blueprint('main_bp', __name__)
file_system_loader = FileSystemLoader('web/app')
environment = Environment(loader=file_system_loader)


@bp.route('/', defaults={'path': ''})
@bp.route('/<path:path>')
def index(path):
    dev = current_app.config['DEBUG']
    template_name = 'index.dev.html' if dev else 'index.html'
    template = environment.get_template(template_name)
    return template.render()
