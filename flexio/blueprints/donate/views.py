import stripe
from flask import (
    request,
    flash,
    url_for,
    Blueprint,
    render_template,
    redirect
)


donate = Blueprint('donate', __name__)


@donate.route('/donate', methods=['POST'])
def charge():
    # Amount in cents
    amount = 500

    if request.method == 'POST':
        donator = stripe.Customer.create(
            email='flexio@donate.com',
            source=request.form['stripeToken']
        )

        charge = stripe.Charge.create(
            customer=donator.id,
            amount=amount,
            currency='usd',
            description='Flexio Donation System'
        )

        flash('Thanks for your donation. Much appreciated!', 'success')
        return redirect(url_for('core.home'))

    return render_template('core/home.html', amount=amount)
