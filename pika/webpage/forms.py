from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FileField
from wtforms.validators import DataRequired, Length, Email

class CreateRequestForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=100)])
    descr = StringField('Description', validators=[DataRequired(), Length(min=2, max=500)])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    image = FileField('Image')
    submit = SubmitField('Create Request')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Save Changes')