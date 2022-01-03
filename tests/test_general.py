import sys
import os 
import unittest
import ast
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.checker.utils import keys_exists
from app import app 
"""
URL: http://<host>:<port>/
Method: GET
Description: Entry point for all API, provide general information of covid cases.
"""
class GeneralTest(unittest.TestCase):
    # Check for status code 200 
    def test_status_200(self):  
        tester = app.test_client(self)
        response = tester.get("/")
        status_code = response.status_code
        self.assertEqual(status_code,200)
        
    # Check method not allowed : POST, PUT, PATCH, DELETE
    def test_method(self):
        tester=  app.test_client(self)
        response = tester.post("/")
        self.assertEqual(response.status_code,405)
        response = tester.put("/")
        self.assertEqual(response.status_code,405)
        response = tester.patch("/")
        self.assertEqual(response.status_code,405)
        response = tester.delete("/")
        self.assertEqual(response.status_code,405)
        
    # Check if content return is application/json
    def test_content_return(self):
        tester=  app.test_client(self)
        response = tester.get("/")
        self.assertEqual(response.content_type,"application/json")

    # Check response keys and value returned
    def test_response(self):
        tester = app.test_client(self)
        response = tester.get("/")
        key_needed= ['new_active',"new_deaths","new_positive","new_recovered","total_active",
                     "total_deaths","total_positive","total_recovered","message","ok"]
        data = response.data.decode("UTF-8")
        data_dict = json.loads(data)
        for key in key_needed:
            self.assertTrue(key in data)
        self.assertEqual(data_dict['message'],'Request Successfull')        
        self.assertEqual(data_dict['ok'],True)        
    

if __name__ == "__main__":
    unittest.main(argv=[''],verbosity=2, exit=False)