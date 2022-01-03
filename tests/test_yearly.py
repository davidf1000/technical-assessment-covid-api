import sys
import os 
import json
import warnings
import unittest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app 

"""
URL: http://<host>:<port>/yearly
Method: GET
Description: Provide yearly data of total covid cases.
"""

class YearlyTest(unittest.TestCase):
    def setUp(self): # To Ignore Deprecation Warning when doing unit test
        warnings.simplefilter('ignore', category=DeprecationWarning)    
    # Check for status code 200 
    def test_status_200(self):
        tester = app.test_client(self)
        response = tester.get("/yearly?since=2020&upto=2022")
        status_code = response.status_code
        self.assertEqual(status_code,200)
    # Check method not allowed : POST, PUT, PATCH, DELETE
    def test_method(self):
        tester=  app.test_client(self)
        response = tester.post("/yearly")
        self.assertEqual(response.status_code,405)
        response = tester.put("/yearly")
        self.assertEqual(response.status_code,405)
        response = tester.patch("/yearly")
        self.assertEqual(response.status_code,405)
        response = tester.delete("/yearly")
        self.assertEqual(response.status_code,405)    
    # Check if content return is application/json
    def test_content_return(self):
        tester=  app.test_client(self)
        response = tester.get("/yearly")
        self.assertEqual(response.content_type,"application/json")        
    # Check Query String since
    def test_query_string_since(self):
        tester = app.test_client(self)
        # Send non-valid year for testing
        # Test 1 : include non numeric character
        response = tester.get("/yearly?since=20v")    
        self.assertEqual(response.status_code,400)        
        # Test 2 : not a valid modern year 
        # (while technically year 900 or 10 is still a year, but it's not allowed)
        response = tester.get("/yearly?since=900")    
        self.assertEqual(response.status_code,400)        
        response = tester.get("/yearly?since=10")    
        self.assertEqual(response.status_code,400)        
        # Test 3 : Newer than current date
        response = tester.get("/yearly?since=2025")    
        self.assertEqual(response.status_code,400)        
        
    # Check Query String upto
    def test_query_string_upto(self):
        tester = app.test_client(self)
        # Send non-valid year for testing
        # Test 1 : include non numeric character
        response = tester.get("/yearly?upto=20v")    
        self.assertEqual(response.status_code,400)        
        # Test 2 : not a valid modern year 
        # (while technically year 900 or 10 is still a year, but it's not allowed)
        response = tester.get("/yearly?upto=900")    
        self.assertEqual(response.status_code,400)        
        response = tester.get("/yearly?upto=10")    
        self.assertEqual(response.status_code,400)        
        # Test 3 : Newer than current date
        response = tester.get("/yearly?upto=2025")    
        self.assertEqual(response.status_code,400) 
               
    # Check Query String since and upto 
    def test_query_string_since_and_upto(self):
        tester = app.test_client(self)
        # Check since > upto
        response = tester.get("/yearly?since=2021&upto=2020")    
        self.assertEqual(response.status_code,400)        
            
    # Check response JSON OK
    def test_response_body(self):
        tester = app.test_client(self)
        response = tester.get("/yearly?since=2020&upto=2022")    
        key_needed= ['active',"deaths","positive","recovered","year"]
        data = response.data.decode("UTF-8")
        data_dict = json.loads(data)
        for key in key_needed:
            self.assertTrue(key in data)
        self.assertEqual(data_dict['message'],'Request Successfull')        
        self.assertEqual(data_dict['ok'],True)         
              
    # Check response 404 
    def test_reponse_404(self):
        tester = app.test_client(self)
        # 2017 - 2019 is still valid query string, but there's no data record in that time frame
        response = tester.get("/yearly?since=2017&upto=2019")    
        self.assertEqual(response.status_code,404)                
        
"""
URL: http://<host>:<port>/yearly/<year>
Method: GET
Description: Provide yearly data of total covid cases of the year provided in <year>.
Response Body (JSON), example: /yearly/2020
"""        

class YearlyProvidedYearTest(unittest.TestCase):
    def setUp(self): # To Ignore Deprecation Warning when doing unit test
        warnings.simplefilter('ignore', category=DeprecationWarning)      
    # Check for status code 200 
    def test_status_200(self):
        tester = app.test_client(self)
        response = tester.get("/yearly/2021")
        status_code = response.status_code
        self.assertEqual(status_code,200)
    # Check method not allowed : POST, PUT, PATCH, DELETE
    def test_method(self):
        tester=  app.test_client(self)
        response = tester.post("/yearly/2021")
        self.assertEqual(response.status_code,405)
        response = tester.put("/yearly/2021")
        self.assertEqual(response.status_code,405)
        response = tester.patch("/yearly/2021")
        self.assertEqual(response.status_code,405)
        response = tester.delete("/yearly/2021")
        self.assertEqual(response.status_code,405)     
    # Check if content return is application/json
    def test_content_return(self):
        tester=  app.test_client(self)
        response = tester.get("/yearly/2021")
        self.assertEqual(response.content_type,"application/json")           
    # Check path parameter
    def test_path_parameter(self):
        tester=  app.test_client(self)
        # Send non-valid year for testing
        # Test 1 : include non numeric character
        response = tester.get("/yearly/20zs")    
        self.assertEqual(response.status_code,400)        
        # Test 2 : not a valid modern year 
        # (while technically year 900 or 10 is still a year, but it's not allowed)
        response = tester.get("/yearly/900")    
        self.assertEqual(response.status_code,400)        
        response = tester.get("/yearly/10")    
        self.assertEqual(response.status_code,400)        
        # Test 3 : Newer than current date
        response = tester.get("/yearly/2025")    
        self.assertEqual(response.status_code,400)           
    # Check response JSON OK
    def test_response_body(self):
        tester = app.test_client(self)
        response = tester.get("/yearly/2021")    
        key_needed= ['active',"deaths","positive","recovered","year"]
        data = response.data.decode("UTF-8")
        data_dict = json.loads(data)
        for key in key_needed:
            self.assertTrue(key in data)
        self.assertEqual(data_dict['message'],'Request Successfull')        
        self.assertEqual(data_dict['ok'],True)       
    # Check response 404 
    def test_reponse_404(self):
        tester = app.test_client(self)
        # no covid cases in 2019
        response = tester.get("/yearly/2019")    
        self.assertEqual(response.status_code,404)   
    
if __name__ == "__main__":
    unittest.main(verbosity=2, exit=False)