from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from flaskr import app
from models import db, Actor, Movie

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def initialise():
    Movie(title='Top Gun: Maverick', release_date='2022-05-27',
          image='https://m.media-amazon.com/images/M/MV5BMmIwZDMyYWUtNTU0ZS00ODJhLTg2ZmEtMTk5ZmYzODcxODYxXkEyXkFqcGdeQXVyMTEyMjM2NDc2._V1_FMjpg_UX1000_.jpg').insert()
    Actor(name='Tom Cruise', age=52, gender='male',
          image='https://www.hellomagazine.com/imagenes/royalty/20220516140314/tom-cruise-wants-to-take-after-prince-philip/0-683-162/tom-cruise-wants-to-take-after-prince-philip-t.jpg').insert()


if __name__ == '__main__':
    manager.run()
