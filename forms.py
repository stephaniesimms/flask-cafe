"""Forms for Flask Cafe."""
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField, BooleanField, PasswordField
from wtforms.validators import InputRequired, Length, NumberRange, URL, Optional, Email


class AddCafeForm(FlaskForm):
    """Form for adding cafes."""

    name = StringField(
        "Name",
        validators=[InputRequired()],
    )

    description = TextAreaField(
        "Description",
        validators=[Optional()],
    )

    url = StringField(
        "URL",
        validators=[Optional(), URL()],
    )

    address = StringField(
        "Address",
        validators=[InputRequired()],
    )

    city_code = SelectField(
        "City"
    )

    image_url = StringField(
        "Image URL",
        validators=[Optional(), URL()],
    )


class EditCafeForm(FlaskForm):
    """Form for editing cafes."""

    name = StringField(
        "Name",
        validators=[InputRequired()],
    )

    description = TextAreaField(
        "Description",
        validators=[Optional()],
    )

    url = StringField(
        "URL",
        validators=[Optional(), URL()],
    )

    address = StringField(
        "Address",
        validators=[InputRequired()],
    )

    city_code = SelectField(
        "City",
        validators=[InputRequired()],
    )

    image_url = StringField(
        "Image URL",
        validators=[Optional(), URL()],
    )


class SignupForm(FlaskForm):
    """Form for registering new user"""

    username = StringField("Username", validators=[InputRequired()])
    first_name = StringField("First name", validators=[InputRequired()])
    last_name = StringField("Last name", validators=[InputRequired()])
    description = TextAreaField("Description", validators=[Optional()])
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[
                           InputRequired(), Length(min=6)])
    image_url = StringField("Image URL", validators=[Optional(), URL()])
