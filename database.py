import uuid
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
            user_id = str(uuid.uuid4())  # Generate a random UUID
            while db.session.query(self.users).filter_by(user_id=user_id).first():
                user_id = str(uuid.uuid4())  # Keep generating until unique
            new_user = self.users.insert().values(
                user_id=user_id,
                username=name,
                email=email,
                password=password,
                address=address,
                phone_number=phone
            )
            db.session.execute(new_user)

    def show_details(self):
        pass


class Authors:
    def __int__(self):
        metadata.reflect(db.engine)
        self.authors = metadata.tables['author']
