import sys
import os 
import json
import warnings
import unittest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app 

"""
URL: http://<host>:<port>/monthly
Method: GET
Description: Provide monthly data of total covid cases.
"""
class MonthlyTest(unittest.TestCase):
    def setUp(self): # To Ignore Deprecation Warning when doing unit test
        warnings.simplefilter('ignore', category=DeprecationWarning)        
    # Check for status code 200 
    
    def test_status_200(self):
        tester = app.test_client(self)
        response = tester.get("/monthly")
        status_code = response.status_code
        self.assertEqual(status_code,200)
        
    # Check method not allowed
    def test_method(self):
        tester=  app.test_client(self)
        response = tester.post("/monthly")
        self.assertEqual(response.status_code,405)
        response = tester.put("/monthly")
        self.assertEqual(response.status_code,405)
        response = tester.patch("/monthly")
        self.assertEqual(response.status_code,405)
        response = tester.delete("/monthly")
        self.assertEqual(response.status_code,405)        
    # Check if content return is application/json
    def test_content_return(self):
        tester=  app.test_client(self)
        response = tester.get("/monthly")
        self.assertEqual(response.content_type,"application/json")    
    # Check Query String since
    def test_query_string_since(self):
        tester = app.test_client(self)
        # Send non-valid year for testing
        # Test 1 : include non numeric character
        response = tester.get("/monthly?since=2021.0z")    
        self.assertEqual(response.status_code,400)        
        # Test 2 : not a valid modern year 
        # (while technically year 900 or 10 is still a year, but it's not allowed)
        response = tester.get("/monthly?since=900.02")    
        self.assertEqual(response.status_code,400)        
        response = tester.get("/monthly?since=10.05")    
        self.assertEqual(response.status_code,400)        
        # Test 3 : Newer than current date
        response = tester.get("/monthly?since=2025.01")    
        self.assertEqual(response.status_code,400)      
        # Test 4 : Wrong month format 
        response = tester.get("/monthly?since=2025.3")    
        self.assertEqual(response.status_code,400)      
        # Test 5 : Wrong month number 
        response = tester.get("/monthly?since=2021.13")    
        self.assertEqual(response.status_code,400)      
        # Test 6 : Wrong date format
        response = tester.get("/monthly?since=2021-01")    
        self.assertEqual(response.status_code,400)      
    # Check Query String upto
    def test_query_string_upto(self):
        tester = app.test_client(self)
        # Send non-valid year for testing
        # Test 1 : include non numeric character
        response = tester.get("/monthly?upto=2021.0z")    
        self.assertEqual(response.status_code,400)        
        # Test 2 : not a valid modern year 
        # (while technically year 900 or 10 is still a year, but it's not allowed)
        response = tester.get("/monthly?upto=900.02")    
        self.assertEqual(response.status_code,400)        
        response = tester.get("/monthly?upto=10.05")    
        self.assertEqual(response.status_code,400)        
        # Test 3 : Newer than current date
        response = tester.get("/monthly?upto=2025.01")    
        self.assertEqual(response.status_code,400)      
        # Test 4 : Wrong month format 
        response = tester.get("/monthly?upto=2025.3")    
        self.assertEqual(response.status_code,400)      
        # Test 5 : Wrong month number 
        response = tester.get("/monthly?upto=2021.13")    
        self.assertEqual(response.status_code,400)      
        # Test 6 : Wrong date format
        response = tester.get("/monthly?upto=2021-01")    
        self.assertEqual(response.status_code,400)
        
    # Check Query String since and upto    
    def test_query_string_since_and_upto(self):
        tester = app.test_client(self)
        # Check since > upto
        response = tester.get("/monthly?since=2021.01&upto=2020.03")    
        self.assertEqual(response.status_code,400)          
        
    # Check response body JSON OK
    def test_response_body(self):
        tester = app.test_client(self)
        response = tester.get("/monthly?since=2020.01&upto=2022.01")    
        key_needed= ['active',"deaths","positive","recovered","month"]
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
        response = tester.get("/monthly?since=2017.01&upto=2019.02")    
        self.assertEqual(response.status_code,404)     
        
"""
URL: http://<host>:<port>/monthly/<year>
Method: GET
Description: Provide monthly data of total covid cases in the year provided in <year>.
"""        
class MonthlyProvidedYearTest(unittest.TestCase):
    # Check for status code 200 
    def test_status_200(self):
        tester = app.test_client(self)
        response = tester.get("/monthly/2021?since=2021.01&upto=2021.04")
        status_code = response.status_code
        self.assertEqual(status_code,200)
    # Check method not allowed : POST, PUT, PATCH, DELETE
    def test_method(self):
        tester=  app.test_client(self)
        response = tester.post('/monthly/2021')
        self.assertEqual(response.status_code,405)
        response = tester.put('/monthly/2021')
        self.assertEqual(response.status_code,405)
        response = tester.patch('/monthly/2021')
        self.assertEqual(response.status_code,405)
        response = tester.delete('/monthly/2021')
        self.assertEqual(response.status_code,405)        
    # Check Query String since
    def test_query_string_since(self):
        tester = app.test_client(self)
        # Send non-valid year for testing
        # Test 1 : include non numeric character
        response = tester.get("/monthly/2021?since=2021.0z")    
        self.assertEqual(response.status_code,400)        
        # Test 2 : not a valid modern year 
        # (while technically year 900 or 10 is still a year, but it's not allowed)
        response = tester.get("/monthly/2021?since=900.02")    
        self.assertEqual(response.status_code,400)        
        response = tester.get("/monthly/2021?since=10.05")    
        self.assertEqual(response.status_code,400)        
        # Test 3 : Newer than current date
        response = tester.get("/monthly/2021?since=2025.01")    
        self.assertEqual(response.status_code,400)      
        # Test 4 : Wrong month format 
        response = tester.get("/monthly/2021?since=2025.3")    
        self.assertEqual(response.status_code,400)      
        # Test 5 : Wrong month number 
        response = tester.get("/monthly/2021?since=2021.13")    
        self.assertEqual(response.status_code,400)      
        # Test 6 : Wrong date format
        response = tester.get("/monthly/2021?since=2021-01")    
        self.assertEqual(response.status_code,400)      
    # Check Query String upto
    def test_query_string_upto(self):
        tester = app.test_client(self)
        # Send non-valid year for testing
        # Test 1 : include non numeric character
        response = tester.get("/monthly/2021?upto=2021.0z")    
        self.assertEqual(response.status_code,400)        
        # Test 2 : not a valid modern year 
        # (while technically year 900 or 10 is still a year, but it's not allowed)
        response = tester.get("/monthly/2021?upto=900.02")    
        self.assertEqual(response.status_code,400)        
        response = tester.get("/monthly/2021?upto=10.05")    
        self.assertEqual(response.status_code,400)        
        # Test 3 : Newer than current date
        response = tester.get("/monthly/2021?upto=2025.01")    
        self.assertEqual(response.status_code,400)      
        # Test 4 : Wrong month format 
        response = tester.get("/monthly/2021?upto=2025.3")    
        self.assertEqual(response.status_code,400)      
        # Test 5 : Wrong month number 
        response = tester.get("/monthly/2021?upto=2021.13")    
        self.assertEqual(response.status_code,400)      
        # Test 6 : Wrong date format
        response = tester.get("/monthly/2021?upto=2021-01")    
        self.assertEqual(response.status_code,400)
        
    # Check Query String since and upto    
    def test_query_string_since_and_upto(self):
        tester = app.test_client(self)
        # Check since > upto
        response = tester.get("/monthly/2020?since=2021.01&upto=2020.03")    
        self.assertEqual(response.status_code,400)  
        
    # Check path parameter   
    def test_path_parameter(self):
        tester=  app.test_client(self)
        response = tester.post("/")        
        # Send non-valid year for testing
        # Test 1 : include non numeric character
        response = tester.get("/monthly/20zs")    
        self.assertEqual(response.status_code,400)        
        # Test 2 : not a valid modern year 
        # (while technically year 900 or 10 is still a year, but it's not allowed)
        response = tester.get("/monthly/900")    
        self.assertEqual(response.status_code,400)        
        response = tester.get("/monthly/10")    
        self.assertEqual(response.status_code,400)        
        # Test 3 : Newer than current date
        response = tester.get("/monthly/2025")    
        self.assertEqual(response.status_code,400)      
          
    # Check response JSON OK
    def test_response_body(self):
        tester = app.test_client(self)
        response = tester.get("/monthly/2021?since=2021.01&upto=2021.04")    
        key_needed= ['active',"deaths","positive","recovered","month"]
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
        response = tester.get("/monthly/2021?since=2017.01&upto=2019.02")    
        self.assertEqual(response.status_code,404)             
"""
URL: http://<host>:<port>/monthly/<year>/<month>
Method: GET
Description: Provide monthly data of total covid cases in the month and year provided in <year> and
<month>.
"""        
class MonthlyProvidedYearMonthTest(unittest.TestCase):
    # Check for status code 200 
    def test_status_200(self):
        tester = app.test_client(self)
        response = tester.get("/monthly/2021/03")
        status_code = response.status_code
        self.assertEqual(status_code,200)
    # Check method not allowed : POST, PUT, PATCH, DELETE
    def test_method(self):
        tester=  app.test_client(self)
        response = tester.post("/monthly/2021/03")
        self.assertEqual(response.status_code,405)
        response = tester.put("/monthly/2021/03")
        self.assertEqual(response.status_code,405)
        response = tester.patch("/monthly/2021/03")
        self.assertEqual(response.status_code,405)
        response = tester.delete("/monthly/2021/03")
        self.assertEqual(response.status_code,405)  
    # Check if content return is application/json
    def test_content_return(self):
        tester=  app.test_client(self)
        response = tester.get("/monthly/2021/03")
        self.assertEqual(response.content_type,"application/json")                
    # Check path parameter   
    def test_path_parameter(self):
        tester=  app.test_client(self)
        # Send non-valid year for testing
        # Test 1 : include non numeric character
        response = tester.get("/monthly/20zs/12")    
        self.assertEqual(response.status_code,400)        
        # Test 2 : Newer than current date
        response = tester.get("/monthly/2025/32")    
        self.assertEqual(response.status_code,400)     
        # Test 3 : Wrong month
        response = tester.get("/monthly/2021/51")    
        self.assertEqual(response.status_code,400)             
    # Check response JSON OK
    def test_response_body(self):
        tester = app.test_client(self)
        response = tester.get("/monthly/2021/03")    
        key_needed= ['active',"deaths","positive","recovered","month"]
        data = response.data.decode("UTF-8")
        data_dict = json.loads(data)
        for key in key_needed:
            self.assertTrue(key in data)
        self.assertEqual(data_dict['message'],'Request Successfull')        
        self.assertEqual(data_dict['ok'],True)        
    # Check response 404           
    def test_reponse_404(self):
        tester = app.test_client(self)
        # In January 2020 there should be no record
        response = tester.get("/monthly/2020/01")    
        self.assertEqual(response.status_code,404)          
        
if __name__ == "__main__":
    unittest.main(verbosity=2, exit=False)