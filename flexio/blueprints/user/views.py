from flask import (
    Blueprint,
    redirect,
    request,
    flash,
    url_for,
    render_template
)
from flask_login import (
    login_required,
    login_user,
    current_user,
    logout_user
)

from lib.safe_next_url import safe_next_url
from flexio.blueprints.user.decorators import anonymous_required
from flexio.blueprints.user.models import User
from flexio.blueprints.user.forms import (
    LoginForm,
    BeginPasswordResetForm,
    PasswordResetForm,
    SignupForm,
    WelcomeForm,
    UpdateCredentials,
    DeleteUserForm
)

user = Blueprint('user', __name__, template_folder='templates')


@user.route('/login', methods=['GET', 'POST'])
@anonymous_required()
def login():
    form = LoginForm(next=request.args.get('next'))

    if form.validate_on_submit():
        u = User.find_by_identity(request.form.get('identity'))

        if u and u.authenticated(password=request.form.get('password')):
            # As you can see remember me is always enabled, this was a
            # design decision I made because more often than not users
            # want this enabled.
            # This allows for a less complicated login form.
            #
            # If you want them to be able to select whether or not they
            # should remain logged in then perform the following 3 steps:
            # 1) Replace 'True' below with:
            #    request.form.get('remember', False)
            # 2) Uncomment the 'remember' field in user/forms.py#LoginForm
            # 3) Add checkbox to the login form with id/name 'remember'
            if u.deleted is True and u.active is False:
                flash('This account has been deleted.', 'warning')

            elif login_user(u, remember=True) and u.is_active():
                u.update_activity_tracking(request.remote_addr)

                # Handle optionally redirecting to the next URL safely.
                next_url = request.form.get('next')
                if next_url:
                    return redirect(safe_next_url(next_url))

                return redirect(url_for('user.settings'))
            else:
                flash('This account has been disabled.', 'warning')
        else:
            flash('Identity or password is incorrect.', 'warning')

    return render_template('user/login.html', form=form)


@user.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('user.login'))


@user.route('/account/begin_password_reset', methods=['GET', 'POST'])
@anonymous_required()
def begin_password_reset():
    form = BeginPasswordResetForm()

    if form.validate_on_submit():
        u = User.initialize_password_reset(request.form.get('identity'))

        flash('An email has been sent to {0}.'.format(u.email), 'success')
        return redirect(url_for('user.login'))

    return render_template('user/begin_password_reset.html', form=form)


@user.route('/account/password_reset', methods=['GET', 'POST'])
@anonymous_required()
def password_reset():
    form = PasswordResetForm(reset_token=request.args.get('reset_token'))

    if form.validate_on_submit():
        u = User.deserialize_token(request.form.get('reset_token'))

        if u is None:
            flash('Your reset token has expired or was tampered with.',
                  'warning')
            return redirect(url_for('user.begin_password_reset'))

        form.populate_obj(u)
        u.password = User.encrypt_password(request.form.get('password'))
        u.save()

        if login_user(u):
            flash('Your password has been reset.', 'success')
            return redirect(url_for('user.settings'))

    return render_template('user/password_reset.html', form=form)


@user.route('/signup', methods=['GET', 'POST'])
@anonymous_required()
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        u = User()

        form.populate_obj(u)
        u.password = User.encrypt_password(request.form.get('password'))
        u.save()

        if login_user(u):
            flash('Awesome, thanks for signing up!', 'success')
            return redirect(url_for('user.welcome'))

    return render_template('user/signup.html', form=form)


@user.route('/welcome', methods=['GET', 'POST'])
@login_required
def welcome():
    if current_user.username:
        flash('You already picked a username.', 'warning')
        return redirect(url_for('user.settings'))

    form = WelcomeForm()

    if form.validate_on_submit():
        current_user.username = request.form.get('username')
        current_user.save()

        flash('Sign up is complete, enjoy our services.', 'success')
        return redirect(url_for('user.settings'))

    return render_template('user/welcome.html', form=form)


@user.route('/settings')
@login_required
def settings():
    form = DeleteUserForm()
    return render_template('user/settings.html', form=form)


@user.route('/settings/update_credentials', methods=['GET', 'POST'])
@login_required
def update_credentials():
    form = UpdateCredentials(current_user, uid=current_user.id)

    if form.validate_on_submit():
        new_password = request.form.get('password', '')
        current_user.email = request.form.get('email')

        if new_password:
            current_user.password = User.encrypt_password(new_password)

        current_user.save()

        flash('Your sign in settings have been updated.', 'success')
        return redirect(url_for('user.settings'))

    return render_template('user/update_credentials.html', form=form)


@user.route('/settings/delete', methods=['POST'])
@login_required
def delete():
    form = DeleteUserForm()

    if form.validate_on_submit():
        if current_user.role == 'admin':
            flash('You cannot delete an admin account.', 'warning')
            return redirect(url_for('user.settings'))

        else:
            current_user.soft_delete()
            logout_user()

            flash('Your account has been successfully deleted.', 'success')
            return redirect(url_for('user.login'))

    return render_template('user/login.html', form=form)


@user.route('/user/<username>')
@login_required
def user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()

    if user.role == 'admin' and current_user.role == 'member':
        flash('You do not have permission to view that.', 'warning')
        return redirect(url_for('core.home'))

    return render_template('user/user_profile.html', user=user)
