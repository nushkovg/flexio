from flask import Blueprint, render_template, request

from flexio.blueprints.user.models import Unit


core = Blueprint('core', __name__, template_folder='templates')


@core.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    blog_units = Unit.query.order_by(Unit.date.desc()).paginate(page=page,
                                                                per_page=10)
    return render_template('core/home.html', blog_units=blog_units)


@core.route('/privacy')
def privacy():
    return render_template('core/privacy.html')


@core.route('/terms-of-service')
def terms():
    return render_template('core/terms.html')


@core.route('/about')
def about():
    return render_template('core/about.html')
