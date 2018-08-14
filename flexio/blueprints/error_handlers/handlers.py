from flask import Blueprint, render_template


error_handlers = Blueprint('error_handlers', __name__,
                           template_folder='templates')


@error_handlers.app_errorhandler(400)
def error_400(error):
    return render_template('error_handlers/400.html'), 400


@error_handlers.app_errorhandler(401)
def error_401(error):
    return render_template('error_handlers/401.html'), 401


@error_handlers.app_errorhandler(403)
def error_403(error):
    return render_template('error_handlers/403.html'), 403


@error_handlers.app_errorhandler(404)
def error_404(error):
    return render_template('error_handlers/404.html'), 404


@error_handlers.app_errorhandler(405)
def error_405(error):
    return render_template('error_handlers/405.html'), 405


@error_handlers.app_errorhandler(500)
def error_500(error):
    return render_template('error_handlers/500.html'), 500
