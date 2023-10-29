from datetime import datetime
from app import db, db_session

class UserToken(db.Model):
    """
    UserToken model represents the association between an Instagram user's ID and their access token.

    Attributes:
        id (int): The primary key for the table.
        user_id (str): The user's ID from Instagram.
        access_token (str): The access token for the user.
        timestamp (datetime): The timestamp of when the token was added to the database.
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(120), index=True)
    access_token = db.Column(db.String(120))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @classmethod
    def add_token(cls, user_id, access_token):
        user_token = cls(user_id=user_id, access_token=access_token)
        db_session.add(user_token)
        db_session.commit()

class PhotoBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    user_id = db.Column(db.String(120), index=True)
    photos = db.Column(db.PickleType)

    @classmethod
    def create_photobook(cls, name, user_id, photos):
        photobook = cls(name=name, user_id=user_id, photos=photos)
        db_session.add(photobook)
        db_session.commit()

    @classmethod
    def get_photobooks_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def get_photos_by_name_and_user(cls, photobook_name, user_id):
        photobook = cls.query.filter_by(name=photobook_name, user_id=user_id).first()
        return photobook
