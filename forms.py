"""Forms for Flask Cafe."""

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, PasswordField
from wtforms.validators import InputRequired, Length, URL, Optional, Email


class CafeAddEditForm(FlaskForm):
    """Form for adding/editing cafes."""

    name = StringField("Name", validators=[InputRequired()])
    description = TextAreaField("Description")
    url = StringField("URL", validators=[Optional(), URL()])
    address = StringField("Address", validators=[InputRequired()])
    city_code = SelectField("City")
    image_url = StringField("Image URL (optional)", validators=[Optional(), URL()])


class SignupForm(FlaskForm):
    """Form for registering new user"""

    username = StringField("Username", validators=[InputRequired()])
    first_name = StringField("First name", validators=[InputRequired()])
    last_name = StringField("Last name", validators=[InputRequired()])
    description = TextAreaField("Description", validators=[Optional()])
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[Length(min=6)])
    image_url = StringField("Image URL", validators=[Optional(), URL()])


class LoginForm(FlaskForm):
    """Login form"""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


class EditUserForm(FlaskForm):
    """Form for editing a user profile"""

    first_name = StringField("First name", validators=[InputRequired()])
    last_name = StringField("Last name", validators=[InputRequired()])
    description = TextAreaField("Description", validators=[Optional()])
    email = StringField("Email", validators=[InputRequired(), Email()])
    image_url = StringField("Image URL (optional)", validators=[Optional(), URL()])
