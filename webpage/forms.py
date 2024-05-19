from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FileField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo

# Form for creating a new request
class CreateRequestForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=100)])  # Request title with length validation
    descr = StringField('Description', validators=[DataRequired(), Length(min=2, max=500)])  # Description with length validation
    quantity = IntegerField('Quantity', validators=[DataRequired()])  # Quantity of items requested
    image = FileField('Image')  # Optional image upload
    submit = SubmitField('Create Request')  # Submit button

# Form for editing user profile details
class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])  # Username field
    email = StringField('Email', validators=[DataRequired(), Email()])  # Email field with email validation
    bio = TextAreaField('Bio')  # New bio field for user profile
    profile_picture = FileField('Profile Picture')  # Optional profile picture upload
    submit = SubmitField('Save Changes')  # Submit button

# Form for changing user password
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])  # Current password
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])  # New password with length validation
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])  # Confirmation for new password
    submit = SubmitField('Change Password')  # Submit button
