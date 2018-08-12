from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail
from flask_wtf.csrf import CsrfProtect

debug_toolbar = DebugToolbarExtension()
mail = Mail()
csrf = CsrfProtect()
