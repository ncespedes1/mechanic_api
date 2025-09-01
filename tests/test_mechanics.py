from app import create_app
from app.models import Mechanics, db
import unittest 
from werkzeug.security import check_password_hash, generate_password_hash
from app.util.auth import encode_token


# python -m unittest discover tests

class TestMechanics(unittest.TestCase):

    #Runs before each test_method
    def setUp(self): 
        self.app = create_app('TestingConfig') #Create a testing version of my app for these testcases
        self.mechanic = Mechanics(firstname="Nik", lastname="Nak", email="tester@email.com",  password=generate_password_hash('abc123'), salary=155000, address="888 Best St.") #Creating a starter user, to test things like get, login, update, and delete
        with self.app.app_context(): 
            db.drop_all() #removing any lingering table
            db.create_all() #creating fresh for another round of testing
            db.session.add(self.mechanic)
            db.session.commit()
        self.token = encode_token(1) #encoding a token for my starter Mechanic defined above ^
        self.client = self.app.test_client() #creates a test client that will send requests to our API


    def test_login(self):
        login_creds = {
            "email": "tester@email.com",
            "password": "abc123"
        }

        response = self.client.post('mechanics/login', json=login_creds)
        self.assertTrue(response.status_code, 200)
        self.assertIn('token', response.json)

    def test_invalid_login(self):
        login_creds = {
            "email": "tester@email.com",
            "password": "not123"
        }

        response = self.client.post('/mechanics', json=login_creds)
        self.assertEqual(response.status_code, 400)

    def test_create_mechanic(self):
        mechanic_payload = {
            "firstname": "Test",
            "lastname": "Mech",
            "email": "test@email.com",
            "password": "abc123",
            "salary": "123000",
            "address": "123 Fun St."
        }

        response = self.client.post('/mechanics', json=mechanic_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['firstname'], "Test")
        self.assertTrue(check_password_hash(response.json['password'], "abc123"))


    #Negative check:
    def test_invalid_create(self):
        #missing email
        mechanic_payload = {
            "firstname": "Test",
            "lastname": "Mech",
            "password": "abc123",
            "salary": "123000",
            "address": "123 Fun St."
        }

        response = self.client.post('/mechanics', json=mechanic_payload)
        self.assertEqual(response.status_code, 400)

    def test_nonunique_email(self):
        mechanic_payload = {
            "firstname": "Test",
            "lastname": "Mech",
            "email": "tester@email.com",
            "password": "abc123",
            "salary": "123000",
            "address": "123 Fun St."
        }

        response = self.client.post('/mechanics', json=mechanic_payload)
        self.assertEqual(response.status_code, 400)

    def test_read_mechanics(self):

        response = self.client.get('/mechanics')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['firstname'], 'Nik')

    def test_read_mechanic(self):
        
        response = self.client.get('/mechanics/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['firstname'], 'Nik')
        

    def test_delete(self):
        headers = {"Authorization": "Bearer " + self.token}

        response = self.client.delete("/mechanics", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Successfully deleted mechanic 1')
    
    def test_unauthorized_delete(self):

        response = self.client.delete("/mechanics")
        self.assertEqual(response.status_code, 401)

    def test_update(self):
        headers = {"Authorization": "Bearer " + self.token}

        update_payload = {
            "firstname": "Nik",
            "lastname": "Nak",
            "email": "tester@email.com",
            "password": "abc123",
            "salary": "188000",
            "address": "888 Best St."
            }

        response = self.client.put('/mechanics', headers=headers, json=update_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['salary'], '188000')

    def test_invalid_update(self):
        headers = {"Authorization": "Bearer " + self.token}

        update_payload = {
            "firstname": "Nik",
            "lastname": "Nak",
            "password": "abc123",
            "salary": "188000",
            "address": "888 Best St."
            }
        
        response = self.client.put('/mechanics', headers=headers, json=update_payload)
        self.assertEqual(response.status_code, 400)
    
    def test_my_tickets(self):
        headers = {"Authorization": "Bearer " + self.token}

        response = self.client.get('/mechanics/my-tickets', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_my_tickets(self):
        response = self.client.get('/mechanics/my-tickets')
        self.assertEqual(response.status_code, 401) #401 is unauthorized
        

    def test_most_tickets(self):
        response = self.client.get('/mechanics/most-tickets')
        self.assertEqual(response.status_code, 200)