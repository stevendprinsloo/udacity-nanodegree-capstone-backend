import os
from sqlalchemy import Column, String, Integer, Date
from flask_sqlalchemy import SQLAlchemy

# database_name = 'casting_agency'

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

"""
Setup the Database

"""


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


"""
Setup Models

"""

castings = db.Table('castings',
    Column('actor_id', db.Integer, db.ForeignKey('actors.id', ondelete="CASCADE", onupdate="CASCADE")),
    Column('movie_id', db.Integer, db.ForeignKey('movies.id', ondelete="CASCADE", onupdate="CASCADE")),
)

"""
Movie Class

"""

class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(Date, nullable=False)
    image = Column(String, nullable=True)
    cast = db.relationship('Actor', secondary='castings', back_populates="castings", lazy=True)

    def __init__(self, title, release_date, image):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def append(self, backref, data):
        backref.append(data)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date.strftime(format('%a, %d %b %Y')),
            'image': self.image,
            'cast': [actor.format_no_castings() for actor in self.cast]
        }
    def format_no_cast(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date.strftime(format('%a, %d %b %Y')),
            'image': self.image,
        }
    def format_edit(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date.strftime(format('%Y-%m-%d')),
            'image': self.image,
            'cast': [actor.format_no_castings() for actor in self.cast]
        }


"""
Actor Class

"""


class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    image = Column(String, nullable=True)
    castings = db.relationship('Movie', secondary='castings', back_populates='cast', lazy=True)

    def __init__(self, name, age, gender, image):
        self.name = name
        self.age = age
        self.gender = gender
        self.image = image

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'image': self.image,
            'castings': [movie.format_no_cast() for movie in self.castings]
        }
    def format_no_castings(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'image': self.image,
        }