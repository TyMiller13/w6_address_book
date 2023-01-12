from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TextAreaField, PasswordField, SubmitField, IntegerField
from wtforms.validators import EqualTo, InputRequired

class SignUpForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    email = EmailField('Email', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired()] )
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_pass = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField()


#create a class for Address 
class AddressForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    phone_number = IntegerField('Phone Number', validators=[InputRequired()])
    address = TextAreaField('Address', validators=[InputRequired()])
    submit = SubmitField()