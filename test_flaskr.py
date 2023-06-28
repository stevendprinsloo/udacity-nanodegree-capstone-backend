import os
import warnings

import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from auth import auth

from flaskr import create_app
from models import setup_db, Movie, Actor


CASTING_ASSISTANT = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkRMeGp1SWxzNjNuOGVoSnlBaUVDWCJ9.eyJpc3MiOiJodHRwczovL2Rldi1jaWtvNnF4ZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjI0YzkyZmUxYmFlNGUwMDY3ZjM3YjRiIiwiYXVkIjpbImNhc3RpbmdfYWdlbmN5IiwiaHR0cHM6Ly9kZXYtY2lrbzZxeGQudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTY1NDkzNjE4MSwiZXhwIjoxNjU1MDIyNTgxLCJhenAiOiJOSExiM08wTDJvSmdxMXVCc2RaQWJEZ1BaanNSZW02NyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJsaXN0OmFjdG9ycyIsImxpc3Q6bW92aWVzIiwidmlldzphY3RvciIsInZpZXc6bW92aWUiXX0.ohWZzkuudbuVsdvZfv3l7H_i44JzKroCy6tdvQiwlFZvz31uCqdc2wSLBlKrV90l6AN2C7BIT66q6Lk_HP9ZmFELevrhsIrUyF3OwAzPHUslSRqPKY5xboMCfJ8lp2rQuC64coh5US2jOPqQOIe5KGAK_lUftBpK32Bv01Oe4FAku3AdVk4foBz0sqJHSR9XOPm2DEqPLMTyrvdSKWCBHZUQmjU-JDZO8puyauYh-S_BTFyoI48UvfEWRHm-LYwhoAWfm3Zym48wDm7jhF8sE1N18GlDMwIbhxPgsIXttB2isWa4BfFNZ_Wy9pONuXCk1hE7VMhOTem9KTFhN9t0vA')

CASTING_DIRECTOR = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkRMeGp1SWxzNjNuOGVoSnlBaUVDWCJ9.eyJpc3MiOiJodHRwczovL2Rldi1jaWtvNnF4ZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjI5ZGNjNWYzMzdjNmMwMDcwOGY0MTUwIiwiYXVkIjpbImNhc3RpbmdfYWdlbmN5IiwiaHR0cHM6Ly9kZXYtY2lrbzZxeGQudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTY1NDk0NDA4NCwiZXhwIjoxNjU1MDMwNDg0LCJhenAiOiJOSExiM08wTDJvSmdxMXVCc2RaQWJEZ1BaanNSZW02NyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJhZGQ6YWN0b3IiLCJkZWxldGU6YWN0b3IiLCJlZGl0OmFjdG9yIiwiZWRpdDptb3ZpZSIsImxpc3Q6YWN0b3JzIiwibGlzdDptb3ZpZXMiLCJ2aWV3OmFjdG9yIiwidmlldzptb3ZpZSJdfQ.h6AczruRH8dw1qCXIKnqYO8t5D0QgbxMZ6Tp8UJhY1CyMBbAIPuFzPpL0UUeZsVwyPFmxagchj1Ulw2KjbDvaTVL6yAvyv8_Aof-MNYK9ru_Jc0HmKcbvAS2sJ2Fe-8vZzZJT5nIITuAlnzMgCTIxWW-wisEbwml2pf3ewooPHOpkNstpT5LvNRuAWF78kCzCXs3Lrspb-_-x8VH5HGc7c6pZlOoM3mPL9kX_ZZ9at1ZkuyBShjPRWWnszibllo4GJSQgQaHnSsLWl46gk54CxUue1ccTfRYBJ0x8N2EmXkAPkA5X7lCA5ZVrP9-ZinGM58ffrFmTYk5YqJAhhrcEw')

EXECUTIVE_PRODUCER = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkRMeGp1SWxzNjNuOGVoSnlBaUVDWCJ9.eyJpc3MiOiJodHRwczovL2Rldi1jaWtvNnF4ZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjI5M2NmMmRhNmMxMzAwMDY4MGRiODM3IiwiYXVkIjpbImNhc3RpbmdfYWdlbmN5IiwiaHR0cHM6Ly9kZXYtY2lrbzZxeGQudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTY1NDk0NDAyNSwiZXhwIjoxNjU1MDMwNDI1LCJhenAiOiJOSExiM08wTDJvSmdxMXVCc2RaQWJEZ1BaanNSZW02NyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJhZGQ6YWN0b3IiLCJhZGQ6bW92aWUiLCJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJlZGl0OmFjdG9yIiwiZWRpdDptb3ZpZSIsImxpc3Q6YWN0b3JzIiwibGlzdDptb3ZpZXMiLCJ2aWV3OmFjdG9yIiwidmlldzptb3ZpZSJdfQ.JMzz_3yHxtMgOIpOcB7sCc0Yj5z2_ngfJopAInxUwEehVepcpm5wct6qHHIhYM3X6ZX_D2767t5-pcvsw3pFghHO2QRnElgv0vSuyWEEr29e9Fdub4VSWYv66x1qbRO7gWmSOhgiPEQdd7yPO5TAjJApTgP5pxc7hVPDxM6998hH4l0m_YZYATFONpUXnTMuCRjxsEhAEFjFlV5tpZmXDIeetMrLe7Y3dLCRLId-CV08O-kdKXOcPrF1ZmjBn9SsmQIlcbVn-fJp090zHe7HCbko1lJSLC0XeUPZIj0Rba6J6XbiMI8C4nDI2jNltxEqfxob7DFFJexBjqPqABiXLg')

MOVIE_ID = 1


class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_agency_test"
        self.database_path = "postgresql://{}/{}".format('postgres:postgres@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_actor = {
            'name': 'Steven Prinsloo',
            'age': 26,
            'gender': 'male',
            'image': 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FAcademy_Award_for_Best_Actor&psig=AOvVaw0LK_WUqO3Ao6zfOqlOAMxu&ust=1654275448556000&source=images&cd=vfe&ved=0CAwQjRxqFwoTCMDHwLuej_gCFQAAAAAdAAAAABAa'
        }

        self.new_movie = {
            'title': 'Shark 2',
            'release_date': '2022-07-14',
            'image': 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FAcademy_Award_for_Best_Actor&psig=AOvVaw0LK_WUqO3Ao6zfOqlOAMxu&ust=1654275448556000&source=images&cd=vfe&ved=0CAwQjRxqFwoTCMDHwLuej_gCFQAAAAAdAAAAABAa',
            'actors': [1,2],
        }

        self.movie_id = None

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_movies(self):
        """TEST GET MOVIES"""
        res = self.client().get(
            '/movies',
            headers = {'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['data']))
        self.assertTrue(['total'])
        self.assertTrue(['pages'])

    def test_get_actors(self):
        """TEST GET ACTORS"""
        res = self.client().get(
            '/actors',
            headers = {'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['data']))
        self.assertTrue(['total'])
        self.assertTrue(['pages'])

    def test_get_paginated_movies(self):
        """TEST GET PAGINATED MOVIES"""
        res = self.client().get('/movies?page=1',
            headers = {'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['data']))
        self.assertTrue(['total'])
        self.assertTrue(['pages'])

    def test_get_single_movie(self):
        """TEST GET SINGLE MOVIE"""
        res = self.client().get('/movies/1',
            headers = {'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['data']))

    def test_get_single_actor(self):
        """TEST GET SINGLE MOVIE"""
        res = self.client().get('/actors/1',
            headers = {'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['data']))

    def test_get_paginated_actors(self):
        """TEST GET PAGINATED ACTORS"""
        res = self.client().get('/actors?page=1',
            headers = {'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['data']))
        self.assertTrue(['total'])
        self.assertTrue(['pages'])

    def test_create_new_movie(self):
        """TEST CREATING NEW MOVIE"""
        res = self.client().post(
            '/movies/create',
            headers = {'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'},
            json=self.new_movie
         )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'], True)
        self.assertTrue(data['message'], True)

    def test_create_new_actor(self):
        """TEST CREATING NEW ACTOR"""
        res = self.client().post(
            '/actors/create',
            headers = {'Authorization': f'Bearer {CASTING_DIRECTOR}'},
            json=self.new_actor
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'], True)
        self.assertTrue(data['message'], True)

    def test_delete_movie(self):
        """TEST DELETE MOVIE"""
        res = self.client().delete(
            '/movies/' + str(MOVIE_ID),
            headers = {'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'},
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # RBAC TESTS =========================================

    def test_401_unauthorized_delete_actor(self):
        """TEST 401 UNAUTHORIZED DELETING MOVIE"""
        res = self.client().delete(
            '/movies/3',
            headers = {'Authorization': f'Bearer {CASTING_DIRECTOR}'},
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_401_unauthorized_creating_movie(self):
        """TEST 401 UNAUTHORIZED CREATING MOVIE"""
        res = self.client().post(
            '/movies/create',
            headers={'Authorization': f'Bearer {CASTING_DIRECTOR}'},
            json=self.new_movie
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_401_unauthorized_editing_movie(self):
        """TEST 401 UNAUTHORIZED EDITING MOVIE"""
        res = self.client().patch(
            '/movies/3',
            headers = {'Authorization': f'Bearer {CASTING_ASSISTANT}'},
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_401_unauthorized_creating_actor(self):
        """TEST 401 UNAUTHORIZED CREATING ACTOR"""
        res = self.client().post(
            '/actors/create',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'},
            json=self.new_actor
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # RBAC TESTS END =========================================

    def test_401_unauthorized(self):
        """TEST 401 INVALID METHOD"""
        res = self.client().get(
            '/actors',
            headers = {'Authorization': f'Bearer '},
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'invalid_header')
        self.assertEqual(data['description'], 'Token not found.')

    def test_405_sent_invalid_method(self):
        """TEST 405 INVALID METHOD"""
        res = self.client().delete(
            '/actors',
            headers = {'Authorization': f'Bearer {CASTING_DIRECTOR}'},
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_400_sent_invalid_body(self):
        """TEST 400 SENT INVALID DATA SENT IN BODY"""
        res = self.client().post(
            '/movies/create',
            headers = {'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'},
            json={},
        )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'bad request')

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    from collections import Sequence


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
