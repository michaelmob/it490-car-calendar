from flask import Blueprint, request, render_template
blueprint = Blueprint('general', __name__, url_prefix='/')


@blueprint.route('/')
def index():
    """
    Display index template.
    """
    return render_template('index.html')
