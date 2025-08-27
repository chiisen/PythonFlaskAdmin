from flask import Blueprint

bp = Blueprint('main', __name__)

@bp.route("/hello")
def say_hello():
    return "Hello from /hello route!"