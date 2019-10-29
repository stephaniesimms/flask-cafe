import os

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgres:///flaskcafe')
MAPQUEST_API_KEY = os.environ.get('MAPQUEST_API_KEY')
