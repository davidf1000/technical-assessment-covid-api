import sys
import os 
import unittest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app 

"""
URL: http://<host>:<port>/daily
Method: GET
Description: Provide daily data of covid cases.
"""
class DailyTest(unittest.TestCase):
    # Check for status code 200 
    def test_status_200(self):
        tester = app.test_client(self)
        response = tester.get("/daily?since=2021.01.01&upto=2021.04.20")
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
URL: http://<host>:<port>/daily/<year>
Method: GET
Description: Provide daily data of covid cases in the year provided in <year>
"""        
class DailyProvidedYearTest(unittest.TestCase):
    # Check for status code 200 
    def test_status_200(self):
        tester = app.test_client(self)
        response = tester.get("/daily/2021?since=2021.01.01&upto=2021.04.20")
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
    # Check path parameter   
    # Check response JSON OK
    # Check response 404             
        
"""
URL: http://<host>:<port>/daily/<year>/<month>
Method: GET
Description: Provide daily data of covid cases in the year and month provided in <year> and <month>.
Response Body (JSON), example: /daily/2020/05
"""        
class DailyProvidedYearMonthTest(unittest.TestCase):
    # Check for status code 200 
    def test_status_200(self):
        tester = app.test_client(self)
        response = tester.get("/daily/2021/03?since=2021.03.01&upto=2021.03.25")
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
    # Check path parameter   
    # Check response JSON OK
    # Check response 404             
        
"""
URL: http://<host>:<port>/daily/<year>/<month>/<date>
Method: GET
Description: Provide daily data of covid cases on the day provided in <year>, <month> and, <date>.
Response Body (JSON), example: /daily/2020/05/01
"""        
class DailyProvidedYearMonthDateTest(unittest.TestCase):
    # Check for status code 200 
    def test_status_200(self):
        tester = app.test_client(self)
        response = tester.get("/daily/2021/03/02")
        status_code = response.status_code
        self.assertEqual(status_code,200)
    # Check method not allowed
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