#from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from extensions import db

metadata = MetaData()


class Genre:
    def __init__(self):
        metadata.reflect(db.engine)
        self.genre = metadata.tables['genre']
        self.genre_id = db.session.query(self.genre.c.genre_id).all()
        self.genres = db.session.query(self.genre.c.genre_name).all()
        self.genre_names = [genre[0] for genre in self.genres]


class Users:
    def __init__(self):
        metadata.reflect(db.engine)
        self.users = metadata.tables['users']

    def insert_user(self, name, email, password, address, phone):
        with db.session.begin():
            new_user = self.users.insert().values(
                username=name,
                email=email,
                password=password,
                address=address,
                phone_number=phone
            )
            db.session.execute(new_user)

