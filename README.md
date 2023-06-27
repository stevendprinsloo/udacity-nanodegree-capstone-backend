# Casting Agency Backend

Frontend live at : [https://sdprin-casting-agency-fronted.herokuapp.com](https://sdprin-casting-agency-fronted.herokuapp.com)

Backend live at : [https://sdprin-casting-agency-backend.herokuapp.com](https://sdprin-casting-agency-backend.herokuapp.com)

This coding project marks the second part my Capstone Project for my Udacity Fullstack Web Developer Nanodegree.

It was developed to model a Casting Agency Software, where users can track and manage which actors were assigned to which movies.

Authorized users can interact with the API to view,add,update,delete Movies and Actors details.

## API

In order to use the API users need to be authenticated. Jwt tokens can be generated by logging in with the provided credentials on the frontend site.

### Endpoints

#### GET /movies

- General:

  - Returns all the movies.
  - Authorised roles: Casting Assistant,Casting Director,Executive Producer.

- Sample: `curl http://127.0.0.1:5000/movies`

```json
{
  "data": [
    {
      "id": 1,
      "release_date": "2022-05-27",
      "image": "https://m.media-amazon.com/images/...jpg",
      "title": "Top Gun: Maverick"
    },
    {
      "id": 2,
      "release_date": "2022-06-25",
      "image": "https://m.media-amazon.com/images/...jpg",
      "title": "Thor: Love & Thunder"
    }
  ],
  "total": 2,
  "pages": 1,
  "success": true
}
```

#### GET /movies/\<int:id\>

- General:

  - Route for getting a specific movie.
  - Authorised roles: Casting Assistant,Casting Director,Executive Producer.

- Sample: `curl http://127.0.0.1:5000/movies/1`

```json
{
  "data": {
    "id": 1,
    "release_date": "2022-05-27",
    "image": "https://m.media-amazon.com/images/...jpg",
    "title": "Top Gun: Maverick"
  },
  "success": true
}
```

#### POST /movies

- General:

  - Creates a new movie based on a payload.
  - Authorised roles: Executive Producer.

- Sample: `curl http://127.0.0.1:5000/movies -X POST -H "Content-Type: application/json" -d '{ "title": "Natasha romanov", "release_date": "2020-05-06" }'`

```json
{
  "data": {
    "id": 2,
    "release_date": "2022-05-27",
    "image": "https://m.media-amazon.com/images/...jpg",
    "title": "John Wick"
  },
  "success": true
}
```

#### PATCH /movies/\<int:id\>

- General:

  - Patches a movie based on a payload.
  - Authorised roles: Casting Director, Executive Producer.

- Sample: `curl http://127.0.0.1:5000/movies/3 -X POST -H "Content-Type: application/json" -d '{ "title": "Natasha romanov patched", "release_date": "2020-05-06" }'`

```json
{
  "message": "Movie John Wick updated!",
  "success": true
}
```

#### DELETE /movies/<int:id\>

- General:

  - Deletes a movies by id form the url parameter.
  - Authorised roles: Executive Producer.

- Sample: `curl http://127.0.0.1:5000/movies/3 -X DELETE`

```json
{
  "message": "Movie John Wick has been successfully deleted!",
  "success": true
}
```

#### GET /actors

- General:

  - Returns all the actors.
  - Authorised roles: Casting Assistant,Casting Director,Executive Producer.

- Sample: `curl http://127.0.0.1:5000/actors`

```json
{
  "data": [
    {
      "id": 2,
      "age": 32,
      "gender": "male",
      "image": "https://m.media-amazon.com/images/...jpg",
      "name": "Chris Hemsworth"
    },
    {
      "id": 1,
      "age": 52,
      "gender": "male",
      "image": "https://m.media-amazon.com/images/...jpg",
      "name": "Tom Cruise"
    }
  ],
  "total": 2,
  "pages": 1,
  "success": true
}
```

#### GET /actors/\<int:id\>

- General:

  - Route for getting a specific actor.
  - Authorised roles: Casting Assistant,Casting Director,Executive Producer.

- Sample: `curl http://127.0.0.1:5000/actors/1`

```json
{
  "data": {
    "id": 1,
    "age": 52,
    "gender": "male",
    "image": "https://m.media-amazon.com/images/...jpg",
    "name": "Tom Cruise"
  },
  "success": true
}
```

#### POST /actors

- General:

  - Creates a new actor based on a payload.
  - Authorised roles: Casting Director,Executive Producer.

- Sample: `curl http://127.0.0.1:5000/actors -X POST -H "Content-Type: application/json" -d '{ "name": "Mary", "age": 22, "gender": "female" }'`

```json
{
  "data": {
    "id": 1,
    "age": 43,
    "gender": "female",
    "image": "https://m.media-amazon.com/images/...jpg",
    "name": "Natalie Portman"
  },
  "success": true
}
```

#### PATCH /actors/\<int:id\>

- General:

  - Patches an actor based on a payload.
  - Authorised roles: Casting Director, Executive Producer.

- Sample: `curl http://127.0.0.1:5000/actors/3 -X POST -H "Content-Type: application/json" -d '{ "name": "John", "age": 22, "gender": "female" }'`

```json
{
  "message": "Natalie Portman updated!",
  "success": true
}
```

#### DELETE /actors/<int:id\>

- General:

  - Deletes an actor by id form the url parameter.
  - Authorised roles: Casting Director,Executive Producer.

- Sample: `curl http://127.0.0.1:5000/actors/3 -X DELETE`

```json
{
  "message": "Actor Natalie Portman has been successfully deleted!",
  "success": true
}
```

## Project dependencies

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

To setup vurtual environment run the following command

```bash
pipenv shell
```

#### Installing Dependencies

```bash
pipenv install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

## Database Setup

The project uses Postgresql as its database, you would need to create one locally and update the environment variable for the DATABASE_URL in setup.sh.

The AUTH0 configuration settings are also set as environmental variables in the setup.sh file. You can run the following to set them up: 

```bash
source setup.sh
```
To update the database and add data run the following :

```bash
python manage.py db upgrade
python manage.py initialise
```

- Start server by running

```bash
export FLASK_APP=flaskr
flask run --reload
```

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Testing

Replace the jwt tokens in test_flask.py with the ones generated on the website - You can access them easily on the Profile page of the webapp after login.

For testing locally, we need to reset database.
To reset database, run

```
python manage.py db downgrade
python manage.py db upgrade
```
Then run:

```
python manage.py initalise
```

OR import the `test-movie-import.sql` file into the database.

### Error Handling

- 401 errors due to RBAC are returned as

```json
{
  "code": "unauthorized",
  "description": "Permission not found."
}
```

Other Errors are returned in the following json format:

```json
{
  "success": "False",
  "error": 400,
  "message": "bad request"
}
```
```json
{
  "success": "False",
  "error": 404,
  "message": "resource not found"
}
```
```json
{
  "success": "False",
  "error": 405,
  "message": "method not allowed"
}
```

The error codes currently returned are:

- 400 – bad request
- 401 – unauthorized
- 404 – resource not found
- 422 – unprocessable
- 500 – internal server error