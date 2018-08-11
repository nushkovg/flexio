from flask import Blueprint, render_template


core = Blueprint('core', __name__, template_folder='templates')


@core.route('/')
def home():
    return render_template('core/home.html')


@core.route('/privacy')
def privacy():
    return render_template('core/privacy.html')


@core.route('/terms-of-service')
def terms():
    return render_template('core/terms.html')


@core.route('/about')
def about():
    return render_template('core/about.html')
