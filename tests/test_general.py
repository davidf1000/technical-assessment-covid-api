import sys
import os 
import unittest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
        

if __name__ == "__main__":
    unittest.main(argv=[''],verbosity=2, exit=False)