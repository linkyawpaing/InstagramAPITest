import os

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://admin:admin@database/photobook'
SQLALCHEMY_TRACK_MODIFICATIONS = False