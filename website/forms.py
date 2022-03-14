from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf import FlaskForm


class FlashcardForm(FlaskForm):
    firstside = TextAreaField('First side', validators=[DataRequired()])
    secondside = TextAreaField('Second side', validators=[DataRequired()])
    submit = SubmitField('Add')