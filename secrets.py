"""Secret keys for Flask Cafe.
For a real app proper security practices require secret keys
to be added to .gitignore
Heroku throws error when not using secret key with WTForms,
login, CSRF protection, etc
"""


FLASK_SECRET_KEY = "oh-so-secret"
