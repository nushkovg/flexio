from flask_wtf import Form
from wtforms import TextAreaField, StringField
from wtforms.validators import DataRequired, Length, Email


class ContactForm(Form):
    email = StringField("What's your e-mail address?",
                        [Email(), DataRequired(), Length(3, 254)])
    message = TextAreaField("What's your question or issue?",
                            [DataRequired(), Length(1, 8192)])
