import sys
import os 
import json
import warnings
import unittest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app 

"""
URL: http://<host>:<port>/daily
Method: GET
Description: Provide daily data of covid cases.
"""
class DailyTest(unittest.TestCase):
    def setUp(self): # To Ignore Deprecation Warning when doing unit test
        warnings.simplefilter('ignore', category=DeprecationWarning)     
    # Check for status code 200 
    def test_status_200(self):
        tester = app.test_client(self)
        response = tester.get("/daily/?since=2021.01.01&upto=2021.04.20")
        status_code = response.status_code
        self.assertEqual(status_code,200)
    # Check method not allowed : POST, PUT, PATCH, DELETE
    def test_method(self):
        tester=  app.test_client(self)
        response = tester.post("/daily/")
        self.assertEqual(response.status_code,405)
        response = tester.put("/daily/")
        self.assertEqual(response.status_code,405)
        response = tester.patch("/daily/")
        self.assertEqual(response.status_code,405)
        response = tester.delete("/daily/")
        self.assertEqual(response.status_code,405)        
    # Check if content return is application/json
    def test_content_return(self):
        tester=  app.test_client(self)
        response = tester.get("/daily/")
        self.assertEqual(response.content_type,"application/json")          
    # Check Query String since
    def test_query_string_since(self):
        tester = app.test_client(self)
        # Send non-valid year for testing
        # Test 1 : include non numeric character
        response = tester.get("/daily/?since=2021.0z.0x")    
        self.assertEqual(response.status_code,400)             
        # Test 2 : Newer than current date
        response = tester.get("/daily/?since=2025.01.01")    
        self.assertEqual(response.status_code,400)      
        # Test 3 : Wrong month or day format 
        response = tester.get("/daily/?since=2025.3.1")    
        self.assertEqual(response.status_code,400)      
        # Test 4 : Wrong month or day number 
        response = tester.get("/daily/?since=2021.13.01")    
        self.assertEqual(response.status_code,400)      
        response = tester.get("/daily/?since=2021.10.32")    
        self.assertEqual(response.status_code,400)      
        # Test 6 : Wrong date format
        response = tester.get("/daily/?since=2021-01-01")    
        self.assertEqual(response.status_code,400)    
    # Check Query String upto
    def test_query_string_upto(self):
        tester = app.test_client(self)
        # Send non-valid year for testing
        # Test 1 : include non numeric character
        response = tester.get("/daily/?upto=2021.0z.0x")    
        self.assertEqual(response.status_code,400)             
        # Test 2 : Newer than current date
        response = tester.get("/daily/?upto=2025.01.01")    
        self.assertEqual(response.status_code,400)      
        # Test 3 : Wrong month or day format 
        response = tester.get("/daily/?upto=2025.3.1")    
        self.assertEqual(response.status_code,400)      
        # Test 4 : Wrong month or day number 
        response = tester.get("/daily/?upto=2021.13.01")    
        self.assertEqual(response.status_code,400)      
        response = tester.get("/daily/?upto=2021.10.32")    
        self.assertEqual(response.status_code,400)      
        # Test 6 : Wrong date format
        response = tester.get("/daily/?upto=2021-01-01")    
        self.assertEqual(response.status_code,400)        
    # Check Query String since and upto  
    def test_query_string_since_and_upto(self):
        tester = app.test_client(self)
        # Check since > upto
        response = tester.get("/daily/?since=2021.01.01&upto=2020.03.05")    
        self.assertEqual(response.status_code,400)   
           
    # Check response JSON Body
    def test_response_body(self):
        tester = app.test_client(self)
        response = tester.get("/daily/?since=2021.01.01&upto=2021.12.31")    
        key_needed= ['active',"deaths","positive","recovered","date"]
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
        response = tester.get("/daily/?since=2017.01.01&upto=2019.02.15")    
        self.assertEqual(response.status_code,404)           
        
"""
URL: http://<host>:<port>/daily/<year>
Method: GET
Description: Provide daily data of covid cases in the year provided in <year>
"""        

class DailyProvidedYearTest(unittest.TestCase):
    def setUp(self): # To Ignore Deprecation Warning when doing unit test
        warnings.simplefilter('ignore', category=DeprecationWarning)     
    # Check for status code 200 
    def test_status_200(self):
        tester = app.test_client(self)
        response = tester.get("/daily/2021/?since=2021.01.01&upto=2021.12.31")
        status_code = response.status_code
        self.assertEqual(status_code,200)
        
    # Check method not allowed : POST, PUT, PATCH, DELETE
    def test_method(self):
        tester=  app.test_client(self)
        response = tester.post("/daily/2021/")
        self.assertEqual(response.status_code,405)
        response = tester.put("/daily/2021/")
        self.assertEqual(response.status_code,405)
        response = tester.patch("/daily/2021/")
        self.assertEqual(response.status_code,405)
        response = tester.delete("/daily/2021/")
        self.assertEqual(response.status_code,405)    
        
    # Check if content return is application/json
    def test_content_return(self):
        tester=  app.test_client(self)
        response = tester.get("/daily/2021/")
        self.assertEqual(response.content_type,"application/json")
              
    # Check Query String since
    def test_query_string_since(self):
        tester = app.test_client(self)
        # Send non-valid year for testing
        # Test 1 : include non numeric character
        response = tester.get("/daily/2021/?since=2021.0z.0x")    
        self.assertEqual(response.status_code,400)             
        # Test 2 : Newer than current date
        response = tester.get("/daily/2021/?since=2025.01.01")    
        self.assertEqual(response.status_code,400)      
        # Test 3 : Wrong month or day format 
        response = tester.get("/daily/2021/?since=2025.3.1")    
        self.assertEqual(response.status_code,400)      
        # Test 4 : Wrong month or day number 
        response = tester.get("/daily/2021/?since=2021.13.01")    
        self.assertEqual(response.status_code,400)      
        response = tester.get("/daily/2021/?since=2021.10.32")    
        self.assertEqual(response.status_code,400)      
        # Test 6 : Wrong date format
        response = tester.get("/daily/2021/?since=2021-01-01")    
        self.assertEqual(response.status_code,400) 
              
    # Check Query String upto
    def test_query_string_upto(self):
        tester = app.test_client(self)
        # Send non-valid year for testing
        # Test 1 : include non numeric character
        response = tester.get("/daily/2021/?upto=2021.0z.0x")    
        self.assertEqual(response.status_code,400)             
        # Test 2 : Newer than current date
        response = tester.get("/daily/2021/?upto=2025.01.01")    
        self.assertEqual(response.status_code,400)      
        # Test 3 : Wrong month or day format 
        response = tester.get("/daily/2021/?upto=2025.3.1")    
        self.assertEqual(response.status_code,400)      
        # Test 4 : Wrong month or day number 
        response = tester.get("/daily/2021/?upto=2021.13.01")    
        self.assertEqual(response.status_code,400)      
        response = tester.get("/daily/2021/?upto=2021.10.32")    
        self.assertEqual(response.status_code,400)      
        # Test 6 : Wrong date format
        response = tester.get("/daily/2021/?upto=2021-01-01")    
        self.assertEqual(response.status_code,400)  
            
    # Check Query String since and upto  
    def test_query_string_since_and_upto(self):
        tester = app.test_client(self)
        # Check since > upto
        response = tester.get("/daily/2021/?since=2021.01.01&upto=2020.03.05")    
        self.assertEqual(response.status_code,400)   
        
    # Check path parameter   
    def test_path_parameter(self):
        tester=  app.test_client(self)
        response = tester.post("/")        
        # Send non-valid year for testing
        # Test 1 : include non numeric character
        response = tester.get("/daily/20zs/")    
        self.assertEqual(response.status_code,400)        
        # Test 2 : not a valid modern year 
        response = tester.get("/daily/900/")    
        self.assertEqual(response.status_code,400)        
        response = tester.get("/daily/10/")    
        self.assertEqual(response.status_code,400)        
        # Test 3 : Newer than current date
        response = tester.get("/daily/2025/")    
        self.assertEqual(response.status_code,400)    

    # Check response JSON Body
    def test_response_body(self):
        tester = app.test_client(self)
        response = tester.get("/daily/2021/?since=2021.01.01&upto=2021.12.31")    
        key_needed= ['active',"deaths","positive","recovered","date"]
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
        response = tester.get("/daily/2021/?since=2017.01.01&upto=2019.02.15")    
        self.assertEqual(response.status_code,404)           
        
"""
URL: http://<host>:<port>/daily/<year>/<month>
Method: GET
Description: Provide daily data of covid cases in the year and month provided in <year> and <month>.
Response Body (JSON), example: /daily/2020/05
"""        
class DailyProvidedYearMonthTest(unittest.TestCase):
    def setUp(self): # To Ignore Deprecation Warning when doing unit test
        warnings.simplefilter('ignore', category=DeprecationWarning)     
    # Check for status code 200 
    def test_status_200(self):
        tester = app.test_client(self)
        response = tester.get("/daily/2021/03/?since=2021.03.01&upto=2021.03.25")
        status_code = response.status_code
        self.assertEqual(status_code,200)
    # Check method not allowed : POST, PUT, PATCH, DELETE
    def test_method(self):
        tester=  app.test_client(self)
        response = tester.post("/daily/2021/01/")
        self.assertEqual(response.status_code,405)
        response = tester.put("/daily/2021/01/")
        self.assertEqual(response.status_code,405)
        response = tester.patch("/daily/2021/01/")
        self.assertEqual(response.status_code,405)
        response = tester.delete("/daily/2021/01/")
        self.assertEqual(response.status_code,405)      
    # Check if content return is application/json
    def test_content_return(self):
        tester=  app.test_client(self)
        response = tester.get("/daily/2021/01/")
        self.assertEqual(response.content_type,"application/json")            
    # Check Query String since
    def test_query_string_since(self):
        tester = app.test_client(self)
        # Send non-valid year for testing
        # Test 1 : include non numeric character
        response = tester.get("/daily/2021/01/?since=2021.0z.0x")    
        self.assertEqual(response.status_code,400)             
        # Test 2 : Newer than current date
        response = tester.get("/daily/2021/01/?since=2025.01.01")    
        self.assertEqual(response.status_code,400)      
        # Test 3 : Wrong month or day format 
        response = tester.get("/daily/2021/03/?since=2021.3.1")    
        self.assertEqual(response.status_code,400)      
        # Test 4 : Wrong month or day number 
        response = tester.get("/daily/2021/12/?since=2021.13.01")    
        self.assertEqual(response.status_code,400)      
        response = tester.get("/daily/2021/12/?since=2021.10.32")    
        self.assertEqual(response.status_code,400)      
        # Test 6 : Wrong date format
        response = tester.get("/daily/2021/12/?since=2021-01-01")    
        self.assertEqual(response.status_code,400)    
           
    # Check Query String upto
    def test_query_string_upto(self):
        tester = app.test_client(self)
        # Send non-valid year for testing
        # Test 1 : include non numeric character
        response = tester.get("/daily/2021/01/?upto=2021.0z.0x")    
        self.assertEqual(response.status_code,400)             
        # Test 2 : Newer than current date
        response = tester.get("/daily/2021/01/?upto=2025.01.01")    
        self.assertEqual(response.status_code,400)      
        # Test 3 : Wrong month or day format 
        response = tester.get("/daily/2021/03/?upto=2021.3.1")    
        self.assertEqual(response.status_code,400)      
        # Test 4 : Wrong month or day number 
        response = tester.get("/daily/2021/12/?upto=2021.13.01")    
        self.assertEqual(response.status_code,400)      
        response = tester.get("/daily/2021/12/?upto=2021.10.32")    
        self.assertEqual(response.status_code,400)      
        # Test 6 : Wrong date format
        response = tester.get("/daily/2021/12/?upto=2021-01-01")    
        self.assertEqual(response.status_code,400)  
            
    # Check Query String since and upto  
    def test_query_string_since_and_upto(self):
        tester = app.test_client(self)
        # Check since > upto
        response = tester.get("/daily/2021/01/?since=2021.01.01&upto=2020.01.05")    
        self.assertEqual(response.status_code,400)   
        
    # Check path parameter   
    def test_path_parameter(self):
        tester=  app.test_client(self)
        # Send non-valid year for testing
        # Test 1 : include non numeric character
        response = tester.get("/daily/20zs/12/")    
        self.assertEqual(response.status_code,400)        
        # Test 2 : Newer than current date
        response = tester.get("/daily/2025/12/")    
        self.assertEqual(response.status_code,400)     
        # Test 3 : Wrong month
        response = tester.get("/daily/2021/51/")    
        self.assertEqual(response.status_code,400)  

    # Check response JSON Body
    def test_response_body(self):
        tester = app.test_client(self)
        response = tester.get("/daily/2021/01/?since=2021.01.01&upto=2021.01.31")    
        key_needed= ['active',"deaths","positive","recovered","date"]
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
        response = tester.get("/daily/2021/01/?since=2017.01.01&upto=2019.02.15")    
        self.assertEqual(response.status_code,404)           
        
"""
URL: http://<host>:<port>/daily/<year>/<month>/<date>
Method: GET
Description: Provide daily data of covid cases on the day provided in <year>, <month> and, <date>.
Response Body (JSON), example: /daily/2020/05/01
"""        
class DailyProvidedYearMonthDateTest(unittest.TestCase):
    def setUp(self): # To Ignore Deprecation Warning when doing unit test
        warnings.simplefilter('ignore', category=DeprecationWarning)     
    # Check for status code 200 
    def test_status_200(self):
        tester = app.test_client(self)
        response = tester.get("/daily/2021/03/02/")
        status_code = response.status_code
        self.assertEqual(status_code,200)
    # Check method not allowed
    def test_method(self):
        tester=  app.test_client(self)
        response = tester.post("/daily/2021/01/01/")
        self.assertEqual(response.status_code,405)
        response = tester.put("/daily/2021/01/01/")
        self.assertEqual(response.status_code,405)
        response = tester.patch("/daily/2021/01/01/")
        self.assertEqual(response.status_code,405)
        response = tester.delete("/daily/2021/01/01/")
        self.assertEqual(response.status_code,405)    
    # Check if content return is application/json
    def test_content_return(self):
        tester=  app.test_client(self)
        response = tester.get("/daily/2021/01/01/")
        self.assertEqual(response.content_type,"application/json")                    
        
    # Check path parameter   
    def test_path_parameter(self):
        tester=  app.test_client(self)
        # Send non-valid year for testing
        # Test 1 : include non numeric character
        response = tester.get("/daily/20zs/12/0x/")    
        self.assertEqual(response.status_code,400)        
        # Test 2 : Newer than current date
        response = tester.get("/daily/2025/12/01/")    
        self.assertEqual(response.status_code,400)     
        # Test 3 : Wrong month / date 
        response = tester.get("/daily/2021/51/01/")    
        self.assertEqual(response.status_code,400)  
        response = tester.get("/daily/2021/02/40/")    
        self.assertEqual(response.status_code,400)  

    # Check response JSON Body
    def test_response_body(self):
        tester = app.test_client(self)
        response = tester.get("/daily/2021/01/05/")    
        key_needed= ['active',"deaths","positive","recovered","date"]
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
        response = tester.get("/daily/2020/01/01/")    
        self.assertEqual(response.status_code,404)            
        
if __name__ == "__main__":
    unittest.main(verbosity=2, exit=False)