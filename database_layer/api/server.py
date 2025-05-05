from http.server import SimpleHTTPRequestHandler, BaseHTTPRequestHandler, HTTPServer
import http.server
import socketserver
import json
from dotenv import load_dotenv
from datetime import datetime

import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(project_root)

from database_layer.db_setup import DatabaseManager
from database_layer.storage_managers.employee_db_manager import EmployeeDBManager
from database_layer.storage_managers.education_db_manager import EducationDBManager
from database_layer.storage_managers.experience_db_manager import ExperienceDBManager

PORT = 8000
load_dotenv()

config = {
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'host': os.getenv("DB_HOST"),
    'database': os.getenv("DB_NAME"),
    'raise_on_warnings': True
}
db_manager = DatabaseManager(config)
employee_db_manager = EmployeeDBManager(db_manager)
education_db_manager = EducationDBManager(db_manager)
experience_db_manager = ExperienceDBManager(db_manager)

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path == "/api":
                self.send_response(200, "OK")
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"message": "Hello World"}).encode())
                
            elif self.path == "/api/employees":
                employees = employee_db_manager.get_all_employee()
                employee_dict = [employee.__dict__ for employee in employees]
                print(employee_dict)
                self.send_response(200, "OK")
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"employees": employee_dict}).encode())
            
            elif self.path.startswith("/api/employees/search?q="):
                search_text = self.path.split("=")[1]
                employees = employee_db_manager.search_employee(search_text)
                self.send_response(200, "OK")
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"employees": employees}).encode())
                
            else:
                self.send_response(404)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid route"}).encode())

        except Exception as e:
            self.send_response(500, {"error": str(e)})
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
            
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        
        if content_length:
            input_json = self.rfile.read(content_length)
            input_data = json.loads(input_json)
        else:
            input_data = None
            
        print(input_data)
        
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()
        
        output_data = {'status': 'OK', 'result': 'HELLO WORLD!'}
        output_json = json.dumps(output_data)
        
        self.wfile.write(output_json.encode('utf-8'))


def run(server_class=HTTPServer, handler_class=Server):
    server_address = ('', PORT)
    print(f"Starting http://0.0.0.0:{PORT}")
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == "__main__":
    run()

