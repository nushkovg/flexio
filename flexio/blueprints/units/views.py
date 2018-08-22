from flask import (
    render_template,
    url_for,
    flash,
    redirect,
    request,
    Blueprint
)
from flask_login import current_user, login_required

from flexio.blueprints.user.models import Unit
from flexio.blueprints.units.forms import UnitForm, DeleteUnitForm


units = Blueprint('units', __name__, template_folder='templates')


@units.route('/unit/create', methods=['GET', 'POST'])
@login_required
def create_unit():
    form = UnitForm()

    if form.validate_on_submit():

        blog_unit = Unit(title=form.title.data,
                         text=form.text.data,
                         user_id=current_user.id)

        blog_unit.create_unit()
        flash('Unit successfully created.', 'success')
        return redirect(url_for('core.home'))
    
    return render_template('units/create_unit.html', form=form)


@units.route('/unit/<int:blog_unit_id>')
@login_required
def blog_unit(blog_unit_id):
    blog_unit = Unit.query.get_or_404(blog_unit_id)

    form = DeleteUnitForm()

    return render_template('/units/blog_unit.html', title=blog_unit.title,
                           date=blog_unit.date, unit=blog_unit, form=form)


@units.route('/unit/<int:blog_unit_id>/update', methods=['GET', 'POST'])
@login_required
def update_unit(blog_unit_id):
    blog_unit = Unit.query.get_or_404(blog_unit_id)

    if blog_unit.author != current_user:
        flash('You are not the author of this unit.', 'warning')
        return redirect(url_for('units.blog_unit', blog_unit_id=blog_unit.id))

    form = UnitForm()

    if form.validate_on_submit():
        blog_unit.title = form.title.data
        blog_unit.text = form.text.data

        blog_unit.update_unit()

        flash('Unit successfully updated.', 'success')
        return redirect(url_for('units.blog_unit', blog_unit_id=blog_unit.id))

    elif request.method == 'GET':
        form.title.data = blog_unit.title
        form.text.data = blog_unit.text

    return render_template('units/update_unit.html', title='Update',
                           form=form, unit=blog_unit)


@units.route('/unit/<int:blog_unit_id>/delete', methods=['POST'])
@login_required
def delete_unit(blog_unit_id):
    blog_unit = Unit.query.get_or_404(blog_unit_id)

    if blog_unit.author != current_user:
        flash('You are not the author of this unit.', 'warning')
        return redirect(url_for('units.blog_unit', blog_unit_id=blog_unit.id))

    blog_unit.delete()

    flash('The unit has been successfully deleted.', 'success')
    return redirect(url_for('core.home'))
