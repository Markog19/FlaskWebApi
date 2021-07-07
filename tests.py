
from datetime import datetime, timedelta
from os import stat
import jwt
from werkzeug.utils import header_property
from werkzeug.wrappers import request, response
from app import app
import unittest


class ApiTest(unittest.TestCase):
    API_URL = "https://127.0.0.1:5000"
    user = {
        "ime":"Marko",
        "prezime":"Galic",
        "email":"Markog19@gmail.com",
        "korisnicko_ime":"Markogalic",
        "lozinka":"1234"
    }
    fake_user = {
        "ime":"Marko",
        "prezime":"Galic",
        "email":"Markog19@gmail.com",
        "korisnicko_ime":"Mgalic",
        "lozinka":"1234"
    }
    update = {
        "ime":"Marko",
        "stara_lozinka":"1234",
        "nova_lozinka":"12345"
    }
  
    def test_create_user(self):
        tester = app.test_client(self)
        response = tester.post("/register",json = ApiTest.user)
        statusCode = response.status_code
        self.assertEqual(statusCode,200)
        

    def test_update_user(self):
        tester = app.test_client(self)
        
        response =  tester.put("/user",json = ApiTest.update)
        statusCode = response.status_code
        self.assertEqual(statusCode,200)
        

    def test_activate_user(self):
        tester = app.test_client(self)
        token = jwt.encode({
            'id': 1, 
            },
            app.config['SECRET_KEY'],algorithm="HS256")  
        headers = {
            "x-access-token":token
        }

        response =  tester.put("/user/activate",headers = headers)
        statusCode = response.status_code
        self.assertEqual(statusCode,200)
     
    
    def test_deactivate_user(self):
        tester = app.test_client(self)
        token = jwt.encode({
            'id': 1, 
            },
            app.config['SECRET_KEY'],algorithm="HS256")  
        headers = {
            "x-access-token":token
        }

        response =  tester.delete("/user",headers = headers)
        statusCode = response.status_code
        self.assertEqual(statusCode,200)
     
    def test_fail_deactivate_user(self):
        tester = app.test_client(self)
        response = tester.delete("/user")
        statusCode = response.status_code
        self.assertEqual(401,statusCode)

    def test_fail_activate_user(self):
        tester = app.test_client(self)
        response = tester.put("/user/activate")
        statusCode = response.status_code
        self.assertEqual(401,statusCode)
    
    def test_fail_create_user(self):
        tester = app.test_client(self)
        response = tester.post("/register",json = ApiTest.fake_user)
        statusCode = response.status_code
        self.assertEqual(statusCode,500)
    def test_fail_update_user(self):
        tester = app.test_client(self)
        response =  tester.put("/user",json = ApiTest.fake_user)
        statusCode = response.status_code
        self.assertEqual(statusCode,500)
        
        
if __name__ == "__main__":      
    unittest.main()
