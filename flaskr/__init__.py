from flask import Flask, abort, jsonify, request
from models import setup_db, Movie, Actor, db, castings
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy import func, desc, text, asc
from auth.auth import AuthError, requires_auth
from datetime import datetime
import math
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# ----------------------------------------------------------------------------#
# Filters
# ----------------------------------------------------------------------------#

ITEMS_PER_PAGE = 4


def paginate(req, selection):
    page = req.args.get('page', 1, type=int)
    current_selection = []
    if page == -1:
        current_selection = selection
    else:
        start = (page - 1) * ITEMS_PER_PAGE
        end = start + ITEMS_PER_PAGE
        current_selection = selection[start:end]

    return current_selection


# ----------------------------------------------------------------------------#
# Endpoints
# ----------------------------------------------------------------------------#


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    migrate = Migrate(app, db)

    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    """
    API endpoints
    """

    @app.route('/actors', methods=['GET'])
    def init():
        return jsonify({
            'success': True,
            'data': [],
            'message': 'You have accessed the API directly.'
        })

    @app.route('/actors', methods=['GET'])
    @requires_auth('list:actors')
    def get_actors(payload):
        by_castings = request.args.get('by_castings')
        pages = None
        try:
            actors = None
            total_actors = Actor.query.count()
            if by_castings is None:
                actors = Actor.query.order_by('id').all()
                pages = math.ceil(len(actors) / ITEMS_PER_PAGE)

            else:
                actors = Actor.query.join(castings) \
                    .add_columns(func.count(castings.c.movie_id).label('total')) \
                    .group_by(Actor.id) \
                    .order_by(text('total DESC')) \
                    .all()

            if actors is None:
                abort(404)

            if len(actors) == 0:
                paginated_actors = []

            else:
                if by_castings is None:
                    formatted_actors = [actor.format() for actor in actors]
                    paginated_actors = paginate(request, formatted_actors)
                else:
                    formatted_actors = [actor[0].format() for actor in actors]
                    paginated_actors = paginate(request, formatted_actors)

            return jsonify({
                'success': True,
                'data': paginated_actors,
                'total': total_actors,
                'pages': pages
            })

        except Exception as e:
            print(e)
            abort(400)

    @app.route('/actors/<int:actor_id>', methods=['GET'])
    @requires_auth('view:actor')
    def get_actor(payload, actor_id):
        try:
            actor = Actor.query.get(actor_id)

            if actor is None:
                abort(404)

            formatted_actor = actor.format()

            return jsonify({
                'success': True,
                'data': formatted_actor
            })

        except Exception as e:
            print(e)
            abort(400)

    @app.route('/movies', methods=['GET'])
    @requires_auth('list:movies')
    def get_movies(payload):
        by_date = request.args.get('by_date')
        pages = None
        try:
            movies = None
            total_movies = Movie.query.count()

            if by_date is None:
                movies = Movie.query.order_by(asc('title')).all()
                pages = math.ceil(len(movies) / ITEMS_PER_PAGE)
            else:
                movies = Movie.query.filter(Movie.release_date >= datetime.today()).order_by(desc('release_date')).all()

            paginated_movies = []

            if movies is None:
                abort(404)

            if len(movies) == 0:
                paginated_movies = []

            formatted_movies = [movie.format() for movie in movies]
            paginated_movies = paginate(request, formatted_movies)

            return jsonify({
                'success': True,
                'data': paginated_movies,
                'total': total_movies,
                'pages': pages,
            })

        except Exception as e:
            print(e)
            abort(400)

    @app.route('/movies/<int:movie_id>', methods=['GET'])
    @requires_auth('view:movie')
    def get_movie(payload, movie_id):
        try:
            movie = Movie.query.get(movie_id)

            if movie is None:
                abort(404)

            formatted_movie = movie.format_edit()

            return jsonify({
                'success': True,
                'data': formatted_movie
            })

        except Exception as e:
            print(e)
            abort(400)

    @app.route('/actors/create', methods=['POST'])
    @requires_auth('add:actor')
    def create_actor(payload):
        body = request.get_json()

        print('\n payload \n')

        print(payload)

        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
        image = body.get('image', None)

        if name is None:
            print('body is empty')
            abort(400)

        try:

            actor = Actor(name=name, age=age, gender=gender, image=image)

            actor.insert()
            print('returned')

            return jsonify({
                'success': True,
                'id': actor.id,
                'message': 'Actor ' + name + ' created!'
            })



        except Exception as e:
            print(e)
            print('not returned')
            abort(400)

    @app.route('/movies/create', methods=['POST'])
    @requires_auth('add:movie')
    def create_movie(payload):
        body = request.get_json()

        title = body.get('title', None)
        release_date = body.get('release_date', None)
        image = body.get('image', None)
        actors = body.get('actors', None)

        if title is None or release_date is None:
            abort(400)

        try:

            movie = Movie(title=title, release_date=release_date, image=image)

            for actor_id in actors:
                actor_model = Actor.query.get(actor_id)
                movie.cast.append(actor_model)
            db.session.add(movie)
            db.session.commit()

            return jsonify({
                'success': True,
                'id': movie.id,
                'message': 'Movie ' + title + ' created!'
            })

        except Exception as e:
            print(e)
            abort(400)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('edit:actor')
    def update_actor(payload, actor_id):
        actor = Actor.query.get(actor_id)

        body = request.get_json()

        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
        image = body.get('image', None)

        try:

            if actor:

                actor.name = name
                actor.age = age
                actor.gender = gender
                actor.image = image

                actor.update()

                return jsonify({
                    "success": True,
                    "message": actor.name + " updated!"
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "Actor " + actor_id + " not found"
                }), 404

        except Exception as e:
            print(e)
            abort(400)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('edit:movie')
    def update_movie(payload, movie_id):
        movie = Movie.query.get(movie_id)

        body = request.get_json()

        title = body.get('title', None)
        release_date = body.get('release_date', None)
        actors = body.get('actors', None)
        image = body.get('image', None)

        try:

            if movie:

                movie.title = title
                movie.release_date = release_date
                movie.image = image

                movie.cast = []

                for actor_id in actors:
                    actor_model = Actor.query.get(actor_id)
                    movie.cast.append(actor_model)

                db.session.commit()

                return jsonify({
                    "success": True,
                    "message": "Movie " + title + " updated!"
                })

            else:
                return jsonify({
                    "success": False,
                    "message": "Movie " + movie_id + " not found"
                }), 404

        except Exception as e:
            print(e)
            abort(400)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(payload, actor_id):
        actor = Actor.query.get(actor_id)

        try:

            if actor:

                name = actor.name

                actor.delete()

                return jsonify({
                    "success": True,
                    "message": "Actor " + name + " has been successfully deleted!"
                })

            else:
                return jsonify({
                    "success": False,
                    "message": "Actor " + actor_id + " not found"
                }), 404

        except Exception as e:
            print(e)
            abort(400)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(payload, movie_id):
        movie = Movie.query.get(movie_id)

        try:

            if movie:

                title = movie.title

                movie.delete()

                return jsonify({
                    "success": True,
                    "message": "Movie " + title + " has been successfully deleted!"
                })

            else:
                return jsonify({
                    "success": False,
                    "message": "Movie not found"
                }), 404

        except Exception as e:
            print(e)
            abort(400)


    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(401)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "unauthorized"
        }), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(AuthError)
    def auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    if __name__ == "__main__":
        context = ('../cert/cert.pem', '../cert/key.pem')
        app.run(port=5000, ssl_context=context)

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
