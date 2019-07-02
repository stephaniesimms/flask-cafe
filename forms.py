"""Forms for Flask Cafe."""
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField, BooleanField
from wtforms.validators import InputRequired, Length, NumberRange, URL, Optional


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


class SignUpForm(FlaskForm):
    """Form for registering new user"""