from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.fields.datetime import DateField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=255)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=255)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=255)])
    profession = SelectField('Profession', choices=[('administrator', 'Administrator'), ('doctor', 'Doctor'), ('asistenta', 'Asistentă'), ('rezident', 'Rezident')], validators=[DataRequired()])
    hospital = SelectField('Hospital', choices=[], validators=[DataRequired()])  # Choices will be populated dynamically
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=255)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already in use. Please choose a different one.')


class AddPatientForm(FlaskForm):
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=255)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=255)])
    birth_date = DateField('Birth Date', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    cnp = StringField('CNP', validators=[DataRequired(), Length(min=13, max=13)])
    sex = SelectField('Sex', choices=[('masculin', 'M'), ('feminin', 'F')], validators=[DataRequired()])
    medical_record = StringField('Medical Record', validators=[DataRequired(), Length(min=1, max=255)])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=255)])
    address = StringField('Address', validators=[DataRequired(), Length(min=1, max=255)])
    hospital = SelectField('Hospital', choices=[], validators=[DataRequired()])
    submit = SubmitField('Add Patient')