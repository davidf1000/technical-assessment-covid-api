import sys
import os 
import unittest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app 

"""
URL: http://<host>:<port>/yearly
Method: GET
Description: Provide yearly data of total covid cases.
"""
class YearlyTest(unittest.TestCase):
    # Check for status code 200 
    def test_status_200(self):
        tester = app.test_client(self)
        response = tester.get("/yearly?since=2020&upto=2021")
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
    # Check Query String since
    # Check Query String upto
    # Check Query String since and upto 
    # Check response JSON OK
    # Check response 404 
        
"""
URL: http://<host>:<port>/yearly/<year>
Method: GET
Description: Provide yearly data of total covid cases of the year provided in <year>.
Response Body (JSON), example: /yearly/2020
"""        
class YearlyProvidedYearTest(unittest.TestCase):
    # Check for status code 200 
    def test_status_200(self):
        tester = app.test_client(self)
        response = tester.get("/yearly/2021")
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
    # Check path parameter
    # Check response JSON OK
    # Check response 404 
    
if __name__ == "__main__":
    unittest.main(argv=[''],verbosity=2, exit=False)